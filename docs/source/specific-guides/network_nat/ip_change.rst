.. _guide_ip_change:

Handling IP address change
=========================================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

This article describes how to handle IP-address changes in PJSIP
applications, with a focus on the mobile case (Wi-Fi / cellular
hand-off, AP roaming, VPN connect/disconnect). It targets PJSIP 2.7
and later, where the high-level API
:cpp:func:`pj::Endpoint::handleIpChange` was introduced (PJSUA-LIB:
:cpp:any:`pjsua_handle_ip_change`).

PJSIP does **not** detect IP changes on its own; the application
observes the change via platform APIs and then calls into PJSIP to
have it clean up. Detection pointers are at the end of this page;
the bulk of the article is about the cleanup.


Problem description
----------------------

IP-address change and access-point reconnection are common on mobile.
Typical scenarios:

- Wi-Fi disconnect → cellular fallback
- Cellular → Wi-Fi when re-entering coverage
- Wi-Fi → Wi-Fi between two APs with different subnets
- VPN connect / disconnect

In each case the local IP that PJSIP was using disappears or is
replaced. Without intervention, this manifests as long send timeouts,
stale registrations, and dropped calls — particularly painful when
TCP/TLS transports are involved, because lingering connections bound
to the dead interface can wedge the SIP path for tens of seconds
before the OS gives up.

:cpp:func:`pj::Endpoint::handleIpChange` (PJSUA-LIB:
:cpp:any:`pjsua_handle_ip_change`) lets the application announce
"my IP changed; clean up" and have the library do the work
(transport restart, optional shutdown of stale transports, account
re-registration, optional re-INVITE / UPDATE on active calls). The
application is still responsible for **detecting** the change
(platform-specific, see below).

.. important::

   Call ``handleIpChange`` **after the new network connection is
   established and a usable IP is available**, not at the moment the
   old interface goes down. Listener restart, transport reopen, and
   re-REGISTER all need the new stack to be up — calling too early
   means the steps fail and have to be retried by the application.
   On a Wi-Fi-off → cellular-on transition, wait for the platform's
   "default network changed / reachable" event before invoking.


High-level flow
---------------

When :cpp:func:`pj::Endpoint::handleIpChange` is invoked, PJSUA-LIB
runs the following in order. Parameters live on
:cpp:any:`pj::IpChangeParam` (global) and
:cpp:any:`pj::AccountIpChangeConfig` (per-account, on
``AccountConfig::ipChangeConfig``).

1. **Shut down all TCP/TLS transports** (if
   :cpp:any:`pj::IpChangeParam::shutdownTransport` is set).
   This is the key step for mobile responsiveness — sockets still
   alive on the old interface won't sit waiting for a remote FIN
   while the OS retransmits over a dead path. Added in :pr:`3781`,
   default ``true``. UDP is *not* covered here; UDP "transports"
   are the listener itself, handled by the next step.

2. **Restart the SIP transport listener** (if
   :cpp:any:`pj::IpChangeParam::restartListener` is set, the
   default). This rebinds the listening socket so it picks up the
   new IP. See :ref:`listener_restart_caveats` below.

3. **Per account: shut down the registration transport** (if
   :cpp:any:`pj::AccountIpChangeConfig::shutdownTp` is set on the
   account, default ``true``). Even if the account shares its
   transport with another, the transport is force-closed — required
   on platforms where the kernel doesn't deliver disconnect
   notifications promptly (iOS in particular).

4. **Re-register**: send REGISTER with the new Contact URI, per
   :cpp:any:`pj::AccountNatConfig::contactRewriteUse` /
   :cpp:any:`pj::AccountNatConfig::contactRewriteMethod`.

5. **Active calls**: either hang up
   (:cpp:any:`pj::AccountIpChangeConfig::hangupCalls`) or refresh
   them with re-INVITE or SIP UPDATE
   (:cpp:any:`pj::AccountIpChangeConfig::reinviteFlags`,
   :cpp:any:`pj::AccountIpChangeConfig::reinvUseUpdate`). When
   ``reinviteFlags`` is 0, neither is sent.


Tuning for fast switching (mobile)
----------------------------------

On a mobile hand-off, the total time between "old IP gone" and
"calls flowing on the new IP" is dominated by three things:

- **Stale TCP/TLS sockets on the old interface.** A REGISTER or
  in-dialog request that lands on a still-open connection bound to
  the now-dead interface will queue / retransmit until the OS gives
  up — typically tens of seconds. Set
  :cpp:any:`pj::IpChangeParam::shutdownTransport` to ``true`` (the
  default since :pr:`3781`) to force-close all TCP/TLS transports
  immediately.

- **Stale UDP listener bound to the old IP.** If you created the
  UDP transport with a specific bound address (a literal IP rather
  than ``0.0.0.0`` / ``::``), the socket can't receive on the new
  IP. :cpp:any:`pj::IpChangeParam::restartListener` rebinds the
  listener — but as a side-effect it **resets the bound address to
  wildcard** (see :ref:`listener_restart_caveats`).

- **REGISTER on a dead transport.** If your application calls
  :cpp:func:`pj::Account::modify` during IP change to update
  account config (IPv6 preference, etc.), the default behaviour is
  to fire a REGISTER immediately — on the *old* transport, which is
  dead. Set
  :cpp:any:`pj::AccountRegConfig::disableRegOnModify` to ``true``
  (added in :pr:`3910`) to suppress that, then let
  :cpp:func:`pj::Endpoint::handleIpChange` drive the re-REGISTER on
  the new transport.

For active calls, prefer **UPDATE** over re-INVITE when the peer
supports it: set
:cpp:any:`pj::AccountIpChangeConfig::reinvUseUpdate` to ``true``
(added in :pr:`3146`). Both methods carry a new SDP offer / answer
with the post-change addresses; the win of UPDATE (:rfc:`3311`) is
that it's a generally lighter exchange than re-INVITE. PJSUA-LIB
falls back to re-INVITE if the peer didn't advertise UPDATE in
``Allow``.

.. note::

   **Do you need a TCP/TLS listener at all?** Mobile clients almost
   never accept incoming SIP connections — they REGISTER and receive
   on the same outbound connection. Two build-time macros in
   ``config_site.h`` skip listener creation entirely (both default
   ``0``):

   - :c:macro:`PJSIP_TCP_TRANSPORT_DONT_CREATE_LISTENER`
   - :c:macro:`PJSIP_TLS_TRANSPORT_DONT_CREATE_LISTENER`

   With listeners disabled, outbound TCP/TLS still works and the
   listener-restart step on IP change is a graceful no-op (per
   :pr:`3873`). See the macro doxygen for the additional
   ``contact_use_src_port`` setting they require. To remove TLS code
   entirely for footprint, set :c:macro:`PJSIP_HAS_TLS_TRANSPORT` to
   ``0`` (TCP cannot be disabled at build time).

A reasonable mobile-tuned configuration in PJSUA2:

.. code-block:: c++

    // Per-account knobs — set before account.create() / account.modify().
    AccountConfig acc_cfg;
    // ... existing config (id, registrar, credentials) ...
    acc_cfg.regConfig.disableRegOnModify        = true;  // if you call modify()
    acc_cfg.ipChangeConfig.shutdownTp           = true;  // default
    acc_cfg.ipChangeConfig.reinvUseUpdate       = true;  // prefer UPDATE
    acc->modify(acc_cfg);  // or set on AccountConfig before account.create()

    // On the IP-change event, hand off to PJSUA-LIB:
    IpChangeParam param;            // defaults: restartListener=true,
                                    // shutdownTransport=true
    Endpoint::instance().handleIpChange(param);

PJSUA-LIB equivalent:

.. code-block:: c

    pjsua_ip_change_param ip_change_param;
    pjsua_ip_change_param_default(&ip_change_param);
    /* All three already default to PJ_TRUE; shown for clarity. */
    ip_change_param.shutdown_transport = PJ_TRUE;
    ip_change_param.restart_listener   = PJ_TRUE;

    /* On the account config: */
    acc_cfg.ip_change_cfg.shutdown_tp      = PJ_TRUE;
    acc_cfg.ip_change_cfg.reinv_use_update = PJ_TRUE;  /* prefer UPDATE */
    acc_cfg.disable_reg_on_modify          = PJ_TRUE;  /* if you call modify() */

    pjsua_handle_ip_change(&ip_change_param);


On ``bound_addr`` and OS routing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Binding a transport to a literal local IP via
:cpp:any:`pj::TransportConfig::boundAddress` /
:cpp:any:`pjsua_transport_config::bound_addr` indirectly pins the
outbound interface — the kernel routes by destination but is
constrained by the bound source, and each IP normally belongs to
one interface. Two caveats matter on mobile:

- If the bound IP no longer exists on any interface after the IP
  change (the Wi-Fi case), the socket's sends fail with
  ``EADDRNOTAVAIL``. If you set ``bound_addr`` explicitly, you're
  responsible for updating it to the new IP **before** calling
  ``handleIpChange``.
- On Android, the per-app default network is enforced *above*
  ``bind()`` — binding to a non-default-network IP isn't sufficient
  on its own. Pair it with
  ``ConnectivityManager.bindProcessToNetwork(newNetwork)`` (Java
  side) so all subsequently-created sockets use that network.

For most apps the simplest pattern is to leave ``bound_addr`` empty
(wildcard) and let the kernel pick — that picks up route-table
changes immediately. Set ``bound_addr`` only when you have a real
need to pin to a specific interface.

If you do need to pin, the field lives in two places — SIP transport
and per-account media (RTP/RTCP):

.. code-block:: c++

   // PJSUA2 — call before recreating SIP transport / modifying account.
   const std::string new_local_ip = "10.0.0.5";

   // SIP transport: pass on the TransportConfig at transportCreate() time.
   TransportConfig sip_tp_cfg;
   sip_tp_cfg.boundAddress = new_local_ip;
   ep.transportDestroy(old_sip_tp_id);
   ep.transportCreate(PJSIP_TRANSPORT_UDP, sip_tp_cfg);

   // Media (RTP/RTCP): on the account config, then re-apply.
   acc_cfg.mediaConfig.transportConfig.boundAddress = new_local_ip;
   acc->modify(acc_cfg);

   ep.handleIpChange(IpChangeParam());

.. code-block:: c

   /* PJSUA-LIB */
   pj_str_t new_local_ip = pj_str("10.0.0.5");

   /* SIP transport: recreate with the new bound_addr. */
   pjsua_transport_config tp_cfg;
   pjsua_transport_config_default(&tp_cfg);
   tp_cfg.bound_addr = new_local_ip;
   pjsua_transport_close(old_sip_tp_id, PJ_TRUE);
   pjsua_transport_create(PJSIP_TRANSPORT_UDP, &tp_cfg, NULL);

   /* Media (RTP/RTCP) lives on the account's rtp_cfg. */
   acc_cfg.rtp_cfg.bound_addr = new_local_ip;
   pjsua_acc_modify(acc_id, &acc_cfg);

   pjsua_ip_change_param param;
   pjsua_ip_change_param_default(&param);
   pjsua_handle_ip_change(&param);

Note that an existing SIP transport can't have its ``bound_addr``
changed in place; recreate the transport (close the old, create the
new). The media ``rtp_cfg.bound_addr`` updated through
``acc_modify`` / ``modify`` is picked up the next time a media
transport is created — for new calls, and for existing calls that
are refreshed with :c:macro:`PJSUA_CALL_REINIT_MEDIA` (which is part
of the default ``reinviteFlags``, so ``handleIpChange`` itself
triggers it).


.. _listener_restart_caveats:

Listener restart caveats
~~~~~~~~~~~~~~~~~~~~~~~~

Two pieces of behaviour to be aware of when
``restartListener = true``:

- **Bound address is reset to wildcard.** If you originally created
  the listener with a specific bound IP (via
  :cpp:any:`pj::TransportConfig::boundAddress` /
  :cpp:any:`pjsua_transport_config::bound_addr`), the restart in
  :cpp:any:`pjsip_tcp_transport_restart` /
  :cpp:any:`pjsip_tls_transport_restart` rebinds to ``0.0.0.0``
  (IPv4) or ``::`` (IPv6). This is documented in :pr:`3873`. If
  you require the listener to stay bound to a specific interface,
  set ``restartListener = false`` and manage the listener yourself
  after IP change.

- **Restart can race the underlying socket.** Some platforms
  (notably iOS) need a moment between "old socket released" and
  "new socket can bind" — see
  :cpp:any:`pj::IpChangeParam::restartLisDelay`
  (default ``PJSUA_TRANSPORT_RESTART_DELAY_TIME``). If a restart
  attempt returns any non-success status and ``restartLisDelay`` is
  non-zero, PJSUA-LIB schedules one retry after the delay; the
  per-attempt result is logged at level 3.


Maintaining a call during IP change
-----------------------------------

By default, :cpp:func:`pj::Endpoint::handleIpChange` keeps active
calls alive and refreshes them via re-INVITE (or UPDATE, see above)
once re-registration completes. The refresh uses
:cpp:any:`pj::AccountIpChangeConfig::reinviteFlags`, defaulting to
:c:macro:`PJSUA_CALL_REINIT_MEDIA` |
:c:macro:`PJSUA_CALL_UPDATE_CONTACT` |
:c:macro:`PJSUA_CALL_UPDATE_VIA`.

Two situations the automatic flow doesn't cover and the application
must handle:

- **IP change during ongoing SDP negotiation** (offer sent, answer
  not yet received). A new SDP offer can't be sent. Do this in two
  steps:

  1. Update Contact only (no new offer) via UPDATE with
     :c:macro:`PJSUA_CALL_NO_SDP_OFFER` so the peer can route its
     pending answer to the new address. Not every endpoint
     supports UPDATE — if a proxy is in the path you can usually
     skip this step.
  2. Update media after the answer arrives, via UPDATE / re-INVITE
     with :c:macro:`PJSUA_CALL_REINIT_MEDIA`.

- **IP change before a call is confirmed.** For *outgoing* calls
  the call is disconnected and reported via
  :cpp:func:`pj::Call::onCallState` (PJSUA-LIB:
  :cpp:any:`pjsua_callback::on_call_state`). For *incoming* calls
  the dialog stays active; hang up manually if the new IP makes
  the call infeasible.


Network change to a different IP version (IPv4 ↔ IPv6)
------------------------------------------------------

For same-family IP changes (IPv4 → IPv4 or IPv6 → IPv6) the call to
:cpp:func:`pj::Endpoint::handleIpChange` is sufficient. For
cross-family changes, the application has to set up a transport for
the new family first and then update account preferences. See
:ref:`IPv6 modes and defaults <ipv6_modes>` in the
:doc:`IPv6 and NAT64 guide <ipv6>` for the mode reference.

PJSUA2 (keep your own :cpp:any:`pj::AccountConfig` around since the
class doesn't expose a getter):

.. code-block:: c++

    void ip_change_to_ip6(Account *acc, AccountConfig &acc_cfg)
    {
        // Create new IPv6 transport if needed; e.g. TLS6
        Endpoint &ep = Endpoint::instance();
        TransportConfig tp_cfg;
        ep.transportCreate(PJSIP_TRANSPORT_TLS6, tp_cfg);

        acc_cfg.sipConfig.ipv6Use   = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.mediaConfig.ipv6Use = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;

        // Prevent modify() from sending a REGISTER on the old transport.
        acc_cfg.regConfig.disableRegOnModify = true;
        acc->modify(acc_cfg);

        IpChangeParam param;
        ep.handleIpChange(param);
    }

PJSUA-LIB:

.. code-block:: c

    static void ip_change_to_ip6()
    {
        ...
        // Create new IPv6 transport, if it's not yet available. e.g: TLS6
        status = pjsua_transport_create(PJSIP_TRANSPORT_TLS6,
                                        &tp_cfg, &transport_id);
        ...

        // For PJSIP earlier than 2.14
        // Bind account to IPv6 transport
        // pjsua_acc_set_transport(acc_id, transport_id);

        // Modify account configuration
        pjsua_acc_get_config(acc_id, app_config.pool, &acc_cfg);

        // ******************************************************
        // ** For PJSIP 2.14 and above:
        acc_cfg.ipv6_sip_use   = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        // ** For PJSIP earlier than 2.14:
        // acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED;
        // ******************************************************

        // acc_cfg.ip_change_cfg.hangup_calls = PJ_TRUE;

        // Available since #3910, prevents pjsua_acc_modify() from
        // prematurely sending a REGISTER on the old (dead) transport.
        acc_cfg.disable_reg_on_modify = PJ_TRUE;
        pjsua_acc_modify(acc_id, &acc_cfg);

        ...
        // Handle ip change
        pjsua_ip_change_param_default(&param);
        pjsua_handle_ip_change(&param);
    }

.. note::

   The example forces ``USE_IPV6_ONLY`` to tear down existing IPv4
   state entirely. If you set ``ipv6_sip_use = PREFER_IPV6`` instead,
   the account is dual-stack and **existing calls that were negotiated
   over IPv4 continue to run over IPv4** — the new preference only
   affects subsequent outgoing offers/requests. Choose
   ``USE_IPV6_ONLY`` when the old family is truly gone.


Diagnostics
-----------

Progress callback
~~~~~~~~~~~~~~~~~

:cpp:func:`pj::Endpoint::onIpChangeProgress` (PJSUA2) and the
underlying :cpp:any:`pjsua_callback::on_ip_change_progress`
(PJSUA-LIB) fire for each stage of the operation:

- :c:macro:`PJSUA_IP_CHANGE_OP_RESTART_LIS` — listener restart
- :c:macro:`PJSUA_IP_CHANGE_OP_ACC_SHUTDOWN_TP` — per-account
  transport shutdown
- :c:macro:`PJSUA_IP_CHANGE_OP_ACC_UPDATE_CONTACT` — re-REGISTER
- :c:macro:`PJSUA_IP_CHANGE_OP_ACC_HANGUP_CALLS` — call hang-up
- :c:macro:`PJSUA_IP_CHANGE_OP_ACC_REINVITE_CALLS` — call refresh
  (re-INVITE / UPDATE)
- :c:macro:`PJSUA_IP_CHANGE_OP_COMPLETED` — all stages done

Each invocation carries a status code and per-stage info — use this
for UI feedback or to time the overall switch.

Log lines
~~~~~~~~~

At log level 3, ``pjsua_core.c`` emits ``"Start handling IP address
change"`` on entry. At level 4 it logs the staged steps:

- ``IP change shutting down transports..``
- ``IP change temporarily ignores request timeout``
- per-listener restart attempts (with the listener's name)

The TCP/TLS listener restart helpers
(:cpp:any:`pjsip_tcp_transport_restart` /
:cpp:any:`pjsip_tls_transport_restart`) also log at level 3 when a
restart is requested but no listener exists — that's the no-op
"update published address only" path from :pr:`3873`.


IP address change detection
----------------------------------

PJSIP doesn't poll for IP changes; the application has to detect
and call :cpp:func:`pj::Endpoint::handleIpChange` (PJSUA-LIB:
:cpp:any:`pjsua_handle_ip_change`). Platform pointers:

iOS
~~~

Use the `Reachability API
<https://developer.apple.com/library/content/samplecode/Reachability/Introduction/Intro.html>`__
or modern Network framework path monitor. Note that iOS aggressively
suspends sockets when the app backgrounds — see also the iOS push
notification guide if your app needs to wake on incoming SIP traffic.

Android
~~~~~~~

Use `ConnectivityManager
<https://developer.android.com/training/monitoring-device-state/connectivity-monitoring.html>`__
with a ``NetworkCallback`` registered via
``registerDefaultNetworkCallback`` (API 24+). On older API levels,
``CONNECTIVITY_ACTION`` broadcast is the fallback.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::IpChangeParam::restartListener`
     - :cpp:any:`pjsua_ip_change_param::restart_listener`
   * - :cpp:any:`pj::IpChangeParam::restartLisDelay`
     - :cpp:any:`pjsua_ip_change_param::restart_lis_delay`
   * - :cpp:any:`pj::IpChangeParam::shutdownTransport`
     - :cpp:any:`pjsua_ip_change_param::shutdown_transport`
   * - :cpp:func:`pj::Endpoint::handleIpChange`
     - :cpp:any:`pjsua_handle_ip_change`
   * - :cpp:func:`pj::Endpoint::onIpChangeProgress`
     - :cpp:any:`pjsua_callback::on_ip_change_progress`
   * - :cpp:any:`pj::AccountRegConfig::disableRegOnModify`
     - :cpp:any:`pjsua_acc_config::disable_reg_on_modify`
   * - :cpp:any:`pj::AccountIpChangeConfig::shutdownTp`
     - :cpp:any:`pjsua_ip_change_acc_cfg::shutdown_tp`
   * - :cpp:any:`pj::AccountIpChangeConfig::hangupCalls`
     - :cpp:any:`pjsua_ip_change_acc_cfg::hangup_calls`
   * - :cpp:any:`pj::AccountIpChangeConfig::reinviteFlags`
     - :cpp:any:`pjsua_ip_change_acc_cfg::reinvite_flags`
   * - :cpp:any:`pj::AccountIpChangeConfig::reinvUseUpdate`
     - :cpp:any:`pjsua_ip_change_acc_cfg::reinv_use_update`


References
----------

- Shutdown all TCP/TLS transports on IP change: :pr:`3781`
- SIP UPDATE for refreshing calls: :pr:`3146`
- Listener restart checks: :pr:`3872`
- Listener restart: skip if no listener, doc bound-addr reset: :pr:`3873`
- ``disable_reg_on_modify``: :pr:`3910`

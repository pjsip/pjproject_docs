.. _guide_upnp:

UPnP NAT Traversal
==================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

UPnP IGD (Internet Gateway Device) lets a host behind a NAT request
a public-side port mapping directly from the router, without
involving any server in the network path. When it works, the
result is the same shape as a STUN-discovered server-reflexive
address — a ``public_ip:public_port → local_ip:local_port``
mapping — but established locally rather than discovered.

PJSIP can use UPnP to request port mappings for the SIP UDP transport
and for the RTP/RTCP media sockets of each call. The implementation
was added in :pr:`3184` and later moved into PJNATH (:pr:`3195`); it
ships as the optional :doc:`PJNATH UPnP module </api/generated/pjnath/group/group__PJNATH__UPNP>`.

When to use UPnP
~~~~~~~~~~~~~~~~

- **Residential / SOHO deployment** behind a UPnP-capable consumer
  router, where a STUN/TURN server isn't available or desirable.
- **Peer-to-peer** scenarios where you control both endpoints but
  not a relay.
- As a **fallback** when STUN cannot be used (UDP blocked outbound,
  but the local router still accepts UPnP requests).

When *not* to use UPnP
~~~~~~~~~~~~~~~~~~~~~~

- **Enterprise / corporate** networks — UPnP IGD is usually disabled
  on managed routers, and even when enabled, security policy
  frequently considers it a risk vector.
- **Carrier-grade NAT / double NAT** — UPnP only talks to the first
  hop; it cannot punch through a second NAT upstream.
- **IPv6-only or NAT64-only paths** — see *Limitations* below.
- **Mobile carriers** — typically no IGD on the carrier's NAT.

UPnP and STUN are alternatives for the same job (discovering the
public address); pick one. If both are configured, PJSUA-LIB
prefers STUN — UPnP is consulted only when no STUN server is set
(see *Interaction with STUN, TURN and ICE* below).


Build prerequisites
-------------------

UPnP is gated by the ``PJNATH_HAS_UPNP`` preprocessor macro and
depends on the **libupnp** library (also known as *Portable SDK for
UPnP Devices*, ``pupnp.sourceforge.net`` — not *miniupnpc*).
Both build systems default to *enabled if libupnp is present*; the
macro is set only when the library is actually found.

GNU autotools
~~~~~~~~~~~~~

UPnP is enabled by default and auto-disables when ``libupnp`` and
``libixml`` are not available. Options:

.. code-block:: shell

    ./configure --disable-upnp        # skip UPnP even if libupnp is present
    ./configure --with-upnp=DIR       # libupnp installed under a custom prefix

A successful detection appends ``-DPJNATH_HAS_UPNP=1`` to ``CFLAGS``
and ``-lupnp -lixml`` to ``LDFLAGS`` in ``build.mak``.

CMake
~~~~~

The relevant CMake option is :samp:`PJNATH_WITH_UPNP` (default
``ON``). When the bundled :sourcedir:`cmake/FindUPNP.cmake` module
fails to locate ``libupnp``, the option is force-set to ``OFF`` and
``PJNATH_HAS_UPNP`` is not defined. To force-disable even when
libupnp is installed:

.. code-block:: shell

    cmake -DPJNATH_WITH_UPNP=OFF ...

Verifying the build
~~~~~~~~~~~~~~~~~~~

Autotools: ``grep PJNATH_HAS_UPNP build.mak``. CMake: inspect the
CMake cache for ``PJNATH_WITH_UPNP``. When the macro is undefined,
the UPnP code paths compile out — ``enableUpnp = true`` on
:cpp:any:`pj::UaConfig` is silently ignored.


Enabling UPnP
-------------

UPnP is configured at the endpoint / global level (one IGD search
per process) and may then be selectively disabled per account.
There is no per-account *enable*; you can only opt **out** of the
global setting.

PJSUA2
~~~~~~

Endpoint-level enable, then optional per-account opt-out:

.. code-block:: c++

   EpConfig epcfg;
   // ... existing config ...
   epcfg.uaConfig.enableUpnp  = true;
   epcfg.uaConfig.upnpIfName  = "";          // optional; empty = first usable iface

   endpoint.libInit(epcfg);
   endpoint.libStart();

   AccountConfig acfg;
   // ... id, registration, credentials ...
   // optional per-account opt-out:
   acfg.natConfig.sipUpnpUse   = PJSUA_UPNP_USE_DISABLED;  // SIP transport
   acfg.natConfig.mediaUpnpUse = PJSUA_UPNP_USE_DEFAULT;   // RTP/RTCP

   try {
       account.create(acfg);
   } catch(Error& err) {
   }

The :cpp:any:`pjsua_upnp_use` enum has two values:
:c:macro:`PJSUA_UPNP_USE_DEFAULT` (follow the global setting) and
:c:macro:`PJSUA_UPNP_USE_DISABLED` (opt this account out).
SIP-signalling and media-transport use are configured
independently via ``sipUpnpUse`` and ``mediaUpnpUse``.

PJSUA-LIB
~~~~~~~~~

Mirror configuration on :cpp:any:`pjsua_config` (global) and
:cpp:any:`pjsua_acc_config` (per account):

.. code-block:: c

    pjsua_config cfg;
    pjsua_config_default(&cfg);
    cfg.enable_upnp = PJ_TRUE;
    cfg.upnp_if_name = pj_str("");

    pjsua_init(&cfg, NULL, NULL);

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);
    /* ... id, registration, credentials ... */
    acc_cfg.sip_upnp_use   = PJSUA_UPNP_USE_DEFAULT;
    acc_cfg.media_upnp_use = PJSUA_UPNP_USE_DEFAULT;

The helper :cpp:any:`pjsua_media_acc_is_using_upnp` reports the
effective combined state (global ``enable_upnp`` AND not
account-disabled AND init successful).

pjsua CLI
~~~~~~~~~

The sample app exposes a single ``--upnp`` flag. The option takes
an optional interface-name argument (getopt's
``optional_argument``), so the value, if any, must be attached with
``=``. The space form ``--upnp eth0`` does not work — GNU getopt
treats ``eth0`` as a separate positional, not as the option's
value.

.. code-block:: shell

    $ ./pjsua --upnp              # enable, default interface
    $ ./pjsua --upnp=eth0         # enable, specific interface

Setting ``--upnp`` flips ``enable_upnp`` to ``PJ_TRUE`` and copies
the argument (if present) into ``upnp_if_name``.


How it works
------------

When ``enable_upnp`` is set, :cpp:any:`pjsua_init()` calls
:cpp:any:`pj_upnp_init()` which issues four SSDP M-SEARCH probes
(``upnp:rootdevice``, ``InternetGatewayDevice``, ``WANIPConnection``
and ``WANPPPConnection``) and waits up to
:c:macro:`PJ_UPNP_DEFAULT_SEARCH_TIME` seconds (default 5 s) for
responses. The result is recorded in
``pjsua_var.upnp_status`` — only ``PJ_SUCCESS`` enables subsequent
mapping requests.

SIP UDP transport
~~~~~~~~~~~~~~~~~

When the SIP UDP transport is created, PJSUA-LIB calls
:cpp:any:`pj_upnp_add_port_mapping` for the transport socket and
uses the returned public address/port as the transport's public
address. If the call fails, PJSUA-LIB falls back to the local
bind address (the same fallback used when neither STUN nor UPnP is
configured).

Media RTP/RTCP
~~~~~~~~~~~~~~

For each call that uses the non-ICE UDP media transport,
:cpp:any:`pj_upnp_add_port_mapping` is called with *two* sockets
(RTP + RTCP) and the returned external addresses are stored on the
call and advertised in the SDP ``c=`` / ``a=rtcp`` lines.

UPnP for media runs **only on the non-ICE path** — the call that
maps the sockets lives in ``create_rtp_rtcp_sock``
(:sourcedir:`pjsip/src/pjsua-lib/pjsua_media.c`), invoked
exclusively by ``create_udp_media_transport``. When ICE is enabled
(``ice_cfg.enable_ice = PJ_TRUE``), PJSUA-LIB takes the
``create_ice_media_transport`` branch instead and the UPnP code is
not reached. See *Interaction with STUN, TURN and ICE* for what
this implies.

Cleanup
~~~~~~~

When the call ends or the SIP UDP transport is destroyed, PJSUA-LIB
calls :cpp:any:`pj_upnp_del_port_mapping` for each mapped address.
At endpoint shutdown :cpp:any:`pj_upnp_deinit()` is invoked.

Direct PJNATH API
~~~~~~~~~~~~~~~~~

For standalone PJNATH applications (no PJSUA / PJSUA2), the four
public functions in :sourcedir:`pjnath/include/pjnath/upnp.h` are:

- :cpp:any:`pj_upnp_init` — start IGD discovery, takes a
  :cpp:any:`pj_upnp_init_param` (factory, optional interface name,
  optional local port, search timeout, completion callback).
- :cpp:any:`pj_upnp_add_port_mapping` — map one or more local UDP
  sockets to external ports on the discovered IGD.
- :cpp:any:`pj_upnp_del_port_mapping` — remove a previously
  added mapping.
- :cpp:any:`pj_upnp_deinit` — shut down the UPnP client.


Interaction with STUN, TURN and ICE
-----------------------------------

UPnP is a NAT-traversal mechanism in its own right, not a primitive
that composes with the others. In the current PJSUA-LIB
implementation:

- **vs STUN (SIP UDP transport).** STUN wins. The relevant code in
  :sourcedir:`pjsip/src/pjsua-lib/pjsua_core.c` uses an
  ``if (stun) ... else if (upnp) ...`` chain when discovering the
  SIP UDP transport's public address. Setting both ``stun_srv`` and
  ``enable_upnp`` means UPnP is not consulted for SIP signalling.
- **vs STUN (media, non-ICE).** Same pattern in
  :sourcedir:`pjsip/src/pjsua-lib/pjsua_media.c` —
  ``create_rtp_rtcp_sock`` tries STUN first and falls through to
  UPnP only if STUN is not configured for the account.
- **vs ICE (media).** UPnP and ICE are **mutually exclusive for
  media**. PJSUA-LIB chooses between ``create_udp_media_transport``
  (which can do UPnP) and ``create_ice_media_transport`` (which
  does not) based on ``ice_cfg.enable_ice``. If you want ICE-based
  NAT traversal for media — including TURN candidates — UPnP for
  RTP/RTCP is bypassed.
- **vs TURN.** TURN belongs to ICE, so the same exclusivity
  applies for media. UPnP does not insert relay candidates and TURN
  does not request UPnP port mappings.

UPnP for the **SIP UDP transport** is independent of media-side ICE
— you can run ICE for media while still using UPnP to publish the
SIP transport's contact address, as long as no STUN server is
configured for SIP.

For TCP/TLS TURN see :doc:`turn_tcp_tls`; for ICE specifics see
:doc:`trickle_ice` and :doc:`manual_ice_host_cand`.


Limitations
-----------

- **IPv4 only.** UPnP mapping is skipped on IPv6 transports unless
  NAT64 is enabled (see
  :sourcedir:`pjsip/src/pjsua-lib/pjsua_media.c` — the check is
  ``!use_ipv6 || use_nat64``). For dual-stack hosts the IPv6 side
  uses the bound local address directly; no UPnP request is sent.
- **UDP transports only.** TCP and TLS SIP transports are not
  mapped via UPnP — they require ``public_addr`` or a STUN-style
  external configuration.
- **Router must speak UPnP IGD** and have it enabled. Many
  enterprise / business-grade routers disable IGD by default for
  security reasons.
- **Carrier-grade NAT** — UPnP cannot traverse an upstream NAT that
  the local router doesn't control. Mappings on the local router
  still won't be reachable from the public internet.
- **Mapping eviction.** Some consumer routers expire UPnP mappings
  silently after a few hours. PJSIP does not refresh mappings;
  the application would need to handle re-mapping itself for very
  long-lived connections.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::UaConfig::enableUpnp`
     - :cpp:any:`pjsua_config::enable_upnp`
   * - :cpp:any:`pj::UaConfig::upnpIfName`
     - :cpp:any:`pjsua_config::upnp_if_name`
   * - :cpp:any:`pj::AccountNatConfig::sipUpnpUse`
     - :cpp:any:`pjsua_acc_config::sip_upnp_use`
   * - :cpp:any:`pj::AccountNatConfig::mediaUpnpUse`
     - :cpp:any:`pjsua_acc_config::media_upnp_use`
   * - *(not exposed)*
     - :cpp:any:`pj_upnp_init`, :cpp:any:`pj_upnp_deinit`,
       :cpp:any:`pj_upnp_add_port_mapping`,
       :cpp:any:`pj_upnp_del_port_mapping`
       (standalone PJNATH API)


References
----------

- Initial implementation: :pr:`3184`
- Moved to PJNATH: :pr:`3195`
- :doc:`PJNATH UPnP module </api/generated/pjnath/group/group__PJNATH__UPNP>`
- *libupnp* upstream: http://pupnp.sourceforge.net/

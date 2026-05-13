.. _guide_server_affinity:

Account-Scoped Server Affinity
==============================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

.. warning::

   This feature is in master (:pr:`4964` for TCP/TLS, :pr:`4977` for
   the UDP follow-up) but is **not yet part of a released PJSIP
   version**. It will ship in the next release after 2.17.


Overview
--------

When an account's registrar / proxy resolves to a pool of addresses
(DNS SRV, A/AAAA round-robin, multiple IPv4/IPv6 alternates), each
REGISTER and outbound request can land on a different server. That's
usually fine — but it breaks two common deployment shapes:

- **Server pools with per-session state** — when the registrar /
  proxy hostname resolves to a pool of backend servers visible to
  the client (multiple DNS SRV targets, multiple A/AAAA records, or
  several explicitly-configured proxies), the client itself picks
  which backend to contact on each request. Without affinity,
  successive REGISTER refreshes / INVITEs may land on different
  backends, so dialog / subscription state on a given server gets
  stale or lost. (A transparent load balancer in front of the pool
  hides this from the client and handles backend selection itself —
  affinity isn't needed there.)
- **TLS connection reuse** — TLS-to-cluster setups want to amortise
  the handshake across many requests. Re-resolving on every REGISTER
  forces a new connection, defeats coalescing, and pays the TLS
  setup cost again.

Server affinity solves both. When enabled, the account pins the
**resolved next-hop server (address + transport)** on the first
successful REGISTER and reuses it across subsequent same-account
requests, instead of re-resolving on every send. The pin is dropped
automatically when the pinned target stops working, so failover to
other DNS alternates still happens.

For an unrelated (manual) approach to failover that doesn't rely on
this pin, see :doc:`dns_failover`.


How pinning works
-----------------

Two mechanisms, one per transport family:

TCP / TLS
~~~~~~~~~

The pin is a reference to a specific
:cpp:any:`pjsip_transport` instance held in the account's transport
selector (:c:macro:`PJSIP_TPSELECTOR_TRANSPORT`). All subsequent
account-originated requests — REGISTER refresh, outgoing INVITE,
SUBSCRIBE, etc. — route through that exact transport. Because TLS
trust is asserted at handshake, this also skips the per-request
CVE-2020-15260 hostname check on reuse.

UDP
~~~

UDP listeners are shared, so the pin can't be a transport reference.
Instead, server affinity injects a hidden Route header
(``<sip:HOST:PORT;lr;hide>``) at the head of the account's route set.
The ``;hide`` URI parameter suppresses the Route from the wire (it's
filtered out by ``pjsip_routing_hdr_print``), but loose-routing still
uses it as the request destination. Net effect: REGISTER and INVITE
go to the pinned address even though the UDP listener is shared.

Setting the pin
~~~~~~~~~~~~~~~

A pin can be established two ways:

- **Auto-captured** on the first successful 2xx REGISTER, from the
  response's transport info. This is the common case — the
  application just enables affinity and the first registration takes
  care of pinning.
- **Set explicitly** by the application via
  :cpp:any:`pjsua_acc_set_affinity_addr` (PJSUA-LIB) or
  :cpp:func:`pj::Account::setAffinityAddr` (PJSUA2). Useful when the
  account doesn't register (no auto-capture available), or to force
  a specific back-end regardless of what REGISTER would otherwise
  pick.

The two kinds are tracked separately with an internal
``sa_pin_explicit`` flag and behave differently on auto-rereg retry
— see *Clearing the pin* below.

Clearing the pin
~~~~~~~~~~~~~~~~

- **Transport down** — if the pinned ``pjsip_transport`` reports
  disconnect, the pin is dropped and the next REGISTER re-pins
  against fresh resolution.
- **``reg_uri`` change** in :cpp:any:`pjsua_acc_modify` — the
  previous pin no longer points at the same server hostname / FQDN,
  so the next REGISTER re-resolves against the new URI.
- **Registration retry after failure** — when a REGISTER fails with
  a retry-eligible status (408 / 5xx / 6xx) or the connection drops,
  PJSUA schedules another REGISTER attempt (the built-in
  *automatic re-registration* mechanism, configured via
  :cpp:any:`pjsua_acc_config::reg_retry_interval` and
  :cpp:any:`pjsua_acc_config::reg_first_retry_interval`). On that
  retry, **auto-captured pins are dropped** so the retry can resolve
  fresh and pick a different alternate. Explicitly-set pins are
  preserved so applications that pinned for a reason aren't silently
  rerouted.
- **On demand** via :cpp:any:`pjsua_acc_refresh_transport`
  (PJSUA-LIB) or :cpp:func:`pj::Account::refreshTransport` (PJSUA2)
  — useful for forcing a fresh DNS resolution without modifying the
  account config.

The pin-drop on retry is what makes graceful failover work: when the
pinned server starts returning 503 or the connection drops, the
retry attempt can pick a different alternate from the resolved set
rather than hammering the same dead address.


Enabling server affinity
------------------------

The setting is a tristate at the account level, with a boolean global
default. The tristate means an account can explicitly opt **in**, opt
**out**, or fall back to the global default.

PJSUA2
~~~~~~

Global default on :cpp:any:`pj::UaConfig`, per-account override on
:cpp:any:`pj::AccountSipConfig`:

.. code-block:: c++

   EpConfig epcfg;
   // ... existing config ...
   epcfg.uaConfig.accServerAffinityDefault = true;      // global default ON
   endpoint.libInit(epcfg);
   endpoint.libStart();

   AccountConfig acfg;
   // ... id, registration URI, credentials ...
   acfg.sipConfig.serverAffinity = PJSUA_SERVER_AFFINITY_UNSPECIFIED;
        // inherit from the global default (default value)
   // alternatives:
   //   PJSUA_SERVER_AFFINITY_ENABLED    -> force on for this account
   //   PJSUA_SERVER_AFFINITY_DISABLED   -> force off for this account

   try {
       account.create(acfg);
   } catch(Error& err) {
   }

Two runtime helpers on :cpp:any:`pj::Account`:

- :cpp:func:`pj::Account::refreshTransport` — discard the cached
  pin so the next REGISTER re-resolves. No-op when affinity is
  disabled.
- :cpp:func:`pj::Account::setAffinityAddr` — explicitly pin to a
  specific address (useful for accounts that don't register, or to
  override the address REGISTER would otherwise pick). Throws
  ``Error`` with ``PJ_EINVALIDOP`` if affinity is disabled or
  :cpp:any:`pj::AccountSipConfig::transportId` is set.
  The address is a :cpp:any:`pj::SocketAddress` — a string typedef
  parsed via :cpp:any:`pj_sockaddr_parse`, so use the standard
  ``host:port`` form (or just ``host`` to let the parser pick a
  default port).

.. code-block:: c++

   // Pin explicitly (e.g. force a known active back-end)
   try {
       account.setAffinityAddr("198.51.100.10:5061");
   } catch(Error& err) {
   }

   // Later, force a re-resolution
   try {
       account.refreshTransport();
   } catch(Error& err) {
   }

PJSUA-LIB
~~~~~~~~~

Same shape on the C structs:

.. code-block:: c

    pjsua_config cfg;
    pjsua_config_default(&cfg);
    cfg.acc_server_affinity_default = PJ_TRUE;           // global default ON

    pjsua_init(&cfg, NULL, NULL);

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);
    acc_cfg.server_affinity = PJSUA_SERVER_AFFINITY_UNSPECIFIED;
        /* or PJSUA_SERVER_AFFINITY_ENABLED / DISABLED */

The tristate :cpp:any:`pjsua_server_affinity_mode` has values
``UNSPECIFIED``, ``DISABLED``, ``ENABLED``. UNSPECIFIED is the default
on a freshly initialised :cpp:any:`pjsua_acc_config` and inherits
from ``pjsua_config.acc_server_affinity_default``. This is also
what :cpp:any:`pjsua_acc_modify` uses when the caller wants to leave
the inherited setting intact.

Runtime helpers:

- :cpp:any:`pjsua_acc_refresh_transport` — drop the cached pin.
- :cpp:any:`pjsua_acc_set_affinity_addr` — explicitly pin to an
  address. Returns ``PJ_EINVALIDOP`` if affinity is disabled or if
  the account has ``transport_id`` set (``transport_id`` already
  expresses pinning, and the affinity layer is bypassed in that
  case).

pjsua CLI
~~~~~~~~~

A single flag controls both the global default and the current
account's setting:

.. code-block:: shell

    $ ./pjsua --server-affinity              # equivalent to =on
    $ ./pjsua --server-affinity=on
    $ ./pjsua --server-affinity=off

The flag sets :cpp:any:`pjsua_config::acc_server_affinity_default`
and the currently-being-built account's ``server_affinity`` together,
so runtime ``+a`` (add-account) commands inherit the same default.


Behaviour and caveats
---------------------

- **Bypassed when ``transport_id`` is set.** If
  :cpp:any:`pjsua_acc_config::transport_id` is non-default,
  affinity is silently bypassed — ``transport_id`` already pins
  the account to a specific local listener, which is a stronger
  form of pinning. :cpp:any:`pjsua_acc_set_affinity_addr`
  (and :cpp:func:`pj::Account::setAffinityAddr`) return
  ``PJ_EINVALIDOP`` in that case.

- **UDP + ``reg_use_proxy=0``.** When REGISTER is configured to
  bypass both outbound and account proxies (``reg_use_proxy = 0``)
  and UDP affinity is enabled, the configured proxies may still
  appear in REGISTER routing alongside the affinity pin, partially
  defeating the ``reg_use_proxy=0`` intent. Use the default
  :c:macro:`PJSUA_REG_USE_ALL_PROXY` together with UDP affinity if
  this matters.

- **Pinned host unreachable, alternates exist.** Failover to a
  different alternate from the resolved set happens via the
  automatic-re-registration retry path described above — i.e. only
  after a retry-eligible REGISTER failure or a transport disconnect.
  There is no live health probe.

- **Mid-call re-resolution.** Existing dialogs / calls hold their
  own transport refs and are unaffected by
  :cpp:any:`pjsua_acc_refresh_transport` /
  :cpp:func:`pj::Account::refreshTransport`; only the *next*
  REGISTER (and any new request after that) sees the fresh
  resolution.


Diagnostics
-----------

Server affinity emits a handful of log lines under
``THIS_FILE = "pjsua_acc.c"``:

.. list-table::
   :header-rows: 1
   :widths: 12 40 48

   * - Level
     - Message (paraphrased)
     - When it fires
   * - 3 (INFO)
     - ``Account N: server affinity pinned to transport <name>``
     - Auto-capture on first successful REGISTER. ``<name>`` is the
       transport's ``obj_name`` (e.g. ``tcp:1.2.3.4:5061``,
       ``tls:...``, or ``udp...`` for the shared listener).
   * - 3 (INFO)
     - ``Account N: server affinity explicitly pinned via API to transport <name>``
     - :cpp:any:`pjsua_acc_set_affinity_addr` /
       :cpp:func:`pj::Account::setAffinityAddr` succeeded.
   * - 4 (DEBUG)
     - ``Account N: dropping server affinity pin before re-registration retry``
     - Auto-captured pin dropped on retry path. Explicit pins do not
       fire this.
   * - 2 (WARN)
     - ``Account N: pjsua_acc_set_affinity_addr failed; existing pin (if any) is preserved``
     - Transport acquisition or address parsing failed.

Quiet operations (no dedicated log line):

- Pin cleared because the pinned transport went down — the
  underlying transport disconnect is logged by the transport layer
  itself.
- Pin cleared by :cpp:any:`pjsua_acc_refresh_transport` /
  :cpp:func:`pj::Account::refreshTransport`.
- Pin cleared because ``reg_uri`` changed in
  :cpp:any:`pjsua_acc_modify`.

.. note::

   The log message identifies the pinned target by *transport
   object name*, not by IP address. For TCP/TLS this is usually
   informative (e.g. ``tls:198.51.100.10:5061``); for UDP the
   listener is shared, so the destination IP isn't in the log line
   — inspect the SIP trace (REGISTER's request URI / Route) at log
   level 5 if you need to confirm where requests are actually
   going.


Interaction with related features
---------------------------------

- :doc:`dns_failover` — server affinity is the automatic counterpart
  to the manual approach described there. Either approach can pin
  the account to a specific server; pick one.
- **Automatic re-registration** — PJSUA's built-in registration
  retry loop drives pin recovery by dropping the auto-captured pin
  on retryable failures, so the retry attempt can pick a different
  server from the resolved set.
- **Contact rewrite** — orthogonal; the account's Contact still
  follows whatever ``allow_contact_rewrite`` /
  ``contact_rewrite_method`` say. Affinity only changes the
  *destination* the request is sent to, not the Contact published.
- **NAT keep-alive** — orthogonal; keep-alive timers run as
  configured. Affinity does not change the keep-alive cadence.
- **Account-level transport ID** — strictly stronger than affinity.
  Setting the account's transport ID (via
  :cpp:any:`pjsua_acc_config::transport_id` at create-time,
  :cpp:any:`pjsua_acc_set_transport` at runtime, or
  :cpp:any:`pj::AccountSipConfig::transportId` in PJSUA2) pins the
  account to a specific local listener — a stronger form of pinning
  that bypasses the affinity layer entirely.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::UaConfig::accServerAffinityDefault`
       (``bool``)
     - :cpp:any:`pjsua_config::acc_server_affinity_default`
   * - :cpp:any:`pj::AccountSipConfig::serverAffinity`
       (tristate :cpp:any:`pjsua_server_affinity_mode`)
     - :cpp:any:`pjsua_acc_config::server_affinity`
   * - :cpp:func:`pj::Account::refreshTransport`
     - :cpp:any:`pjsua_acc_refresh_transport`
   * - :cpp:func:`pj::Account::setAffinityAddr`
     - :cpp:any:`pjsua_acc_set_affinity_addr`


References
----------

- TCP/TLS pinning: :pr:`4964` (merged via :pr:`4966`)
- UDP destination-pinning + auto-rereg retry fixes: :pr:`4977`
- Smoke test: :source:`tests/pjsua/scripts-run/210_server_affinity.py`
- Available in PJSIP **master** — first release will be after 2.17.

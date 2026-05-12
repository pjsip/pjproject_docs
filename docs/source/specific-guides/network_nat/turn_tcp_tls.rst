.. _guide_turn_tcp_tls:

TURN over TCP and TLS
=====================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

By default a TURN client reaches the TURN server over UDP and the
allocated relay also runs over UDP (:rfc:`5766`, updated by
:rfc:`8656`). On networks that block outbound UDP — restrictive
corporate firewalls, some hotel/airport networks, certain mobile
carriers — the TURN allocation never completes and TURN candidates
are unavailable. The remedy is to reach the TURN server over TCP
or TLS instead. Connection-oriented transports traverse most
firewalls that block UDP outright, and TLS additionally encrypts
the client-server leg.

PJSIP supports all three client-server transports via the
:cpp:any:`pj_turn_tp_type` enum:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ``pj_turn_tp_type`` value
     - Client-to-server transport
   * - ``PJ_TURN_TP_UDP``
     - UDP datagrams (default; lowest latency)
   * - ``PJ_TURN_TP_TCP``
     - TCP connection
   * - ``PJ_TURN_TP_TLS``
     - TLS over TCP

All three are part of base TURN (:rfc:`5766` / :rfc:`8656`). The
same enum is reused for the *allocation* transport requested from
the server, but ``PJ_TURN_TP_TLS`` is only valid as a client-server
transport, never as an allocation transport — see *Allocations vs
the data path* below.

Client-server TCP and TLS support is long-standing in PJNATH
(the TURN integration originally landed via ticket #485 and TURN
TLS via :pr:`1017`). :pr:`2754` is a separate, later addition that
implements RFC 6062 *TCP allocations*, i.e. TCP between the TURN
server and a peer — useful for application protocols that need a
reliable byte stream end-to-end. SIP media does not use this.


Choosing a connection type
--------------------------

- **UDP** — start here. Lowest latency, fewest moving parts. Use unless
  you have evidence UDP is being blocked.
- **TCP** — fall back when UDP is dropped. Slightly higher latency
  (head-of-line blocking when the network is lossy) but reliable
  through almost every firewall.
- **TLS** — use when network policy specifically requires encrypted
  traffic to leave the network (e.g. corporate compliance, DPI
  bypass), or when the TURN server only exposes a TLS listener on
  port 5349.

Some deployments configure two account-level TURN entries — one UDP
primary, one TLS backup on a different port — and let the application
decide which to use based on local probing. PJSIP itself does not do
automatic UDP→TCP→TLS fallback; the application picks one.


PJSUA2 — TURN over UDP or TCP
-----------------------------

Set :cpp:any:`pj::AccountNatConfig::turnConnType` to one of
``PJ_TURN_TP_UDP`` or ``PJ_TURN_TP_TCP``:

.. code-block:: c++

   AccountConfig acfg;
   // ... existing config ...
   acfg.natConfig.iceEnabled    = true;
   acfg.natConfig.turnEnabled   = true;
   acfg.natConfig.turnServer    = "turn.example.com:3478";
   acfg.natConfig.turnConnType  = PJ_TURN_TP_TCP;
   acfg.natConfig.turnUserName  = "user";
   acfg.natConfig.turnPassword  = "secret";

   try {
       account.create(acfg);
   } catch(Error& err) {
   }

.. warning::

   The PJSUA2 ``AccountNatConfig`` does not currently surface the TURN
   TLS settings struct (:cpp:any:`pj_turn_sock_tls_cfg`). The doxygen
   on :cpp:any:`pj::AccountNatConfig::turnConnType` lists only
   ``PJ_TURN_TP_UDP`` and ``PJ_TURN_TP_TCP``. Setting ``turnConnType``
   to ``PJ_TURN_TP_TLS`` in PJSUA2 will attempt a TLS connection, but
   with the TLS configuration left at its zero-initialised default
   the verification behaviour is whatever the SSL backend defaults
   to — typically no CA verification, which is insecure. To configure
   TURN TLS properly — CA file, client cert, ciphers — drop down to
   the PJSUA-LIB :cpp:any:`pjsua_turn_config` struct (next section).


PJSUA-LIB — TURN over UDP, TCP, or TLS
--------------------------------------

The PJSUA-LIB :cpp:any:`pjsua_turn_config` struct exposes the full
TURN configuration including TLS:

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);

    acc_cfg.turn_cfg_use = PJSUA_TURN_CONFIG_USE_CUSTOM;

    pjsua_turn_config *t = &acc_cfg.turn_cfg;
    t->enable_turn   = PJ_TRUE;
    t->turn_server   = pj_str("turn.example.com:5349");
    t->turn_conn_type = PJ_TURN_TP_TLS;

    t->turn_auth_cred.type = PJ_STUN_AUTH_CRED_STATIC;
    t->turn_auth_cred.data.static_cred.username    = pj_str("user");
    t->turn_auth_cred.data.static_cred.data_type   = PJ_STUN_PASSWD_PLAIN;
    t->turn_auth_cred.data.static_cred.data        = pj_str("secret");
    t->turn_auth_cred.data.static_cred.realm       = pj_str("example.com");

    /* TLS-specific bits — only applicable when turn_conn_type is TLS */
    t->turn_tls_setting.ca_list_file = pj_str("/etc/ssl/certs/turn-ca.pem");
    t->turn_tls_setting.cert_file    = pj_str("/etc/pjsip/turn-client.pem");
    t->turn_tls_setting.privkey_file = pj_str("/etc/pjsip/turn-client.key");

    pjsua_acc_id acc_id;
    pjsua_acc_add(&acc_cfg, PJ_TRUE, &acc_id);

For the global default (applied to accounts that keep
``turn_cfg_use = PJSUA_TURN_CONFIG_USE_DEFAULT``) the same fields
exist on :cpp:any:`pjsua_media_config` directly (``enable_turn``,
``turn_server``, ``turn_conn_type``, ``turn_auth_cred``,
``turn_tls_setting``).

The :cpp:any:`pj_turn_sock_tls_cfg` struct in
:sourcedir:`pjnath/include/pjnath/turn_sock.h` includes additional
fields:

- ``ca_buf`` / ``cert_buf`` / ``privkey_buf`` — for in-memory
  credentials instead of file paths (useful on platforms without a
  writable filesystem)
- ``cert_lookup`` / ``cert_direct`` — backend-specific options
  (Windows Schannel certificate store; OpenSSL direct credentials)
- ``password`` — passphrase for an encrypted private key
- ``ssock_param`` — full :cpp:any:`pj_ssl_sock_param` (protocols,
  ciphers, ECDH curves, signature algorithms, renegotiation,
  socket options, timeout). Default protocol is
  :c:macro:`PJ_TURN_TLS_DEFAULT_PROTO` (TLS 1.0 + 1.1 + 1.2).


pjsua CLI
~~~~~~~~~

The pjsua sample app exposes the full set:

.. code-block:: shell

    $ ./pjsua --use-ice --use-turn \
              --turn-srv turn.example.com:5349 \
              --turn-tls \
              --turn-tls-ca-file /etc/ssl/certs/turn-ca.pem \
              --turn-tls-cert-file /etc/pjsip/turn-client.pem \
              --turn-tls-privkey-file /etc/pjsip/turn-client.key \
              --turn-user user --turn-passwd secret

Relevant flags:

- ``--turn-srv NAME:PORT`` — TURN server (mandatory)
- ``--turn-tcp`` — use TCP connection to TURN
- ``--turn-tls`` — use TLS connection to TURN
- ``--turn-tls-ca-file`` — CA bundle for server verification
- ``--turn-tls-cert-file`` / ``--turn-tls-privkey-file`` /
  ``--turn-tls-privkey-pwd`` — client cert (when mutual TLS is
  required)
- ``--turn-tls-cipher`` — preferred cipher list
- ``--turn-tls-neg-timeout`` — TLS handshake timeout

Without ``--turn-tcp`` or ``--turn-tls`` the default is UDP.


Allocations vs the data path
----------------------------

TURN has two layers of transport:

1. **Client-to-server (control + data tunnel)** — set by
   ``turn_conn_type``. Carries TURN messages and (via channel data /
   Send indications) the media itself.
2. **Server-to-peer (the actual relayed media)** — set by
   :cpp:any:`pj_turn_alloc_param::peer_conn_type`. UDP by default.

For typical SIP-over-ICE applications, leaving ``peer_conn_type`` at
its UDP default is correct — the peer reaches the relay over UDP
even if you reach the server over TCP/TLS. RFC 6062 TCP allocations
(where the peer-side transport is also TCP) require an extra
:cpp:any:`pj_turn_sock_connect()` call per peer and are rarely useful
in SIP/SDP media; they are intended for application-specific
protocols that need reliable byte streams.

.. note::

   PJSIP does not surface the TURN allocation's
   ``peer_conn_type`` through :cpp:any:`pjsua_turn_config` —
   PJSUA-LIB and PJSUA2 always allocate a UDP relay regardless of
   ``turn_conn_type``. Standalone PJNATH applications can set
   :cpp:any:`pj_turn_alloc_param::peer_conn_type` when needed.


Defaults and ports
------------------

- **Default UDP/TCP port** — 3478 (IANA-registered)
- **Default TLS port** — 5349 (IANA-registered)
- :c:macro:`PJ_TURN_KEEP_ALIVE_SEC` — 15 s (TURN keep-alive interval)
- :c:macro:`PJ_TURN_PERM_TIMEOUT` — 300 s (permission timeout)
- :c:macro:`PJ_TURN_CHANNEL_TIMEOUT` — 600 s (channel binding lifetime)
- :c:macro:`PJ_TURN_SSL_SOCK_DEFAULT_TIMEOUT` — 10 s (TLS handshake)

These are compile-time settings, overridable in
``pjlib/include/pj/config_site.h``.


Interaction with ICE
--------------------

The TURN connection type only affects how the relayed candidate is
*allocated*. Once the allocation succeeds, the relayed candidate is
just another entry in the ICE candidate list and pairs against the
peer's candidates by normal ICE rules. Whether ICE picks the relayed
candidate or some other (cheaper) candidate depends on the
connectivity-check outcome — TURN is the path of last resort.

Trickle ICE (:doc:`trickle_ice`) and TURN TCP/TLS combine well — the
TURN allocation handshake is the largest single source of pre-trickle
ICE setup latency, so the speedup from trickling is most visible on
calls that actually use the relayed candidate.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::AccountNatConfig::turnEnabled`
     - :cpp:any:`pjsua_turn_config::enable_turn`
   * - :cpp:any:`pj::AccountNatConfig::turnServer`
     - :cpp:any:`pjsua_turn_config::turn_server`
   * - :cpp:any:`pj::AccountNatConfig::turnConnType` (UDP/TCP only)
     - :cpp:any:`pjsua_turn_config::turn_conn_type` (UDP/TCP/TLS)
   * - :cpp:any:`pj::AccountNatConfig::turnUserName` /
       ``turnPassword`` / ``turnPasswordType``
     - :cpp:any:`pjsua_turn_config::turn_auth_cred`
   * - *(not exposed)*
     - :cpp:any:`pjsua_turn_config::turn_tls_setting`
       (:cpp:any:`pj_turn_sock_tls_cfg`)


References
----------

- TURN (UDP relays): :rfc:`5766`
- TURN TCP Allocations: :rfc:`6062`
- TURN TCP implementation: :pr:`2754`
- ICE: :rfc:`8445`

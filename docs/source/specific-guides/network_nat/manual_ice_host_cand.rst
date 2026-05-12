.. _guide_manual_ice_host_cand:

Manual ICE Host Candidates
==========================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

ICE host candidates are normally discovered by enumerating the local
network interfaces and binding the media socket to each. That works
well on a typical desktop or mobile device but breaks in environments
where the address the rest of the network reaches you on isn't an
address the host's kernel sees:

- **Docker / container deployments** — the application sees the
  container's private bridge address (``172.17.0.x`` on
  ``docker0``), but peers reach it on the host's published address.
- **NAT'd virtualisation** — VMs that use host-only or NAT
  networking from the hypervisor.
- **Split-tunnel VPNs** — the tunnel address is correct, but the
  physical-NIC address is not.
- **Multi-homed servers** — a service-discovery system that hands
  out only one of several local addresses for the media path.

Before this feature existed, the workaround was to point ICE at a
STUN server that observed the correct external mapping and rely on
the srflx candidate. That still works, but adds a STUN dependency
for the simplest case — a single static mapping known up front.

PJSIP 2.17 (:pr:`4618`) adds *manual host candidates*: the
application supplies extra host candidate addresses up front and
ICE treats them as if they had been auto-discovered from a local
interface.


How it works
------------

Manual candidates are **additive** — they augment, not replace, the
auto-detected host candidates. ICE will offer all of them as host
candidates in the initial SDP and the peer will pair-test against
each one as part of normal ICE connectivity checks.

Each manual address is processed as follows
(:sourcedir:`pjnath/src/pjnath/ice_strans.c`):

- **Address family must match the transport.** Manual entries for
  IPv4 are added only on IPv4 STUN transports, and IPv6 entries only
  on IPv6 transports. Mixed-family entries are filtered out for the
  wrong-family transport.
- **Port is inherited from the media socket.** The port byte you set
  on the manual address is overwritten with the port of the
  auto-detected base — i.e. the actual port the media socket is
  bound to. Use any value (e.g. 0) when initialising the address.
- **Foundation is computed from the base address**, matching how
  auto-detected hosts are foundationed, so pairing behaves the same.
- **Priority follows declaration order**: manual hosts are inserted
  with descending local preference, so the first manual entry is
  preferred over the second, and so on.
- **Total host count is capped** by
  :cpp:any:`pj::AccountNatConfig::iceMaxHostCands` /
  :cpp:any:`pjsua_ice_config::ice_max_host_cands` (default ``-1``,
  i.e. :c:macro:`PJ_ICE_ST_MAX_CAND`, currently 64). Auto-detected
  and manual host candidates share this budget. PJSUA2 additionally
  raises :c:macro:`PJ_ETOOMANY` if the input vector exceeds the
  internal array size.

The feature does not change SIP-layer addressing. SIP requests and
the SDP ``c=`` line still reflect the addresses chosen by the SIP
transport (``pjsua_transport_config::public_addr``, etc.). Manual
host candidates only affect the ICE candidate list inside the SDP.


PJSUA2 usage
------------

Set :cpp:any:`pj::AccountNatConfig::iceManualHost` to a vector of
bare IP-address strings. Both IPv4 and IPv6 literals work; hostnames
are not resolved, so the value must already be a numeric address.

.. code-block:: c++

   AccountConfig acfg;
   // ... existing config ...
   acfg.natConfig.iceEnabled       = true;
   acfg.natConfig.iceManualHost.clear();
   acfg.natConfig.iceManualHost.push_back("203.0.113.5");          // public IPv4
   acfg.natConfig.iceManualHost.push_back("2001:db8::5");          // public IPv6

   try {
       account.create(acfg);   // or account.modify(acfg);
   } catch(Error& err) {
       // PJ_EINVAL if any string failed to parse,
       // PJ_ETOOMANY if vector exceeds the internal cap.
   }

Notes:

- Strings are parsed via :cpp:any:`pj_sockaddr_set_str_addr()`. Use
  a bare host address (e.g. ``"10.0.0.5"`` or ``"2001:db8::5"``) —
  not ``host:port``, and not a bracketed IPv6 literal like
  ``[::1]``. Hostnames are resolved via the platform resolver, but
  manual host candidates are normally a literal IP.
- The field is a :cpp:any:`pj::SocketAddressVector`, a typedef for
  :cpp:any:`pj::StringVector`. It is serialised by
  :cpp:any:`pj::AccountConfig::readObject` /
  :cpp:any:`pj::AccountConfig::writeObject` so settings persist
  through XML/JSON config.


PJSUA-LIB usage
---------------

Populate :cpp:any:`pjsua_ice_config::ice_manual_host` (an array of
:cpp:any:`pj_sockaddr`) and set
:cpp:any:`pjsua_ice_config::ice_manual_host_cnt`.

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);

    acc_cfg.ice_cfg_use            = PJSUA_ICE_CONFIG_USE_CUSTOM;
    acc_cfg.ice_cfg.enable_ice     = PJ_TRUE;

    pj_str_t v4 = pj_str("203.0.113.5");
    pj_str_t v6 = pj_str("2001:db8::5");
    pj_sockaddr_set_str_addr(pj_AF_INET(),
                             &acc_cfg.ice_cfg.ice_manual_host[0], &v4);
    pj_sockaddr_set_str_addr(pj_AF_INET6(),
                             &acc_cfg.ice_cfg.ice_manual_host[1], &v6);
    acc_cfg.ice_cfg.ice_manual_host_cnt = 2;

    pjsua_acc_id acc_id;
    pjsua_acc_add(&acc_cfg, PJ_TRUE, &acc_id);

Manual host candidates are configured per account; the global
:cpp:any:`pjsua_media_config` does **not** expose
``ice_manual_host`` / ``ice_manual_host_cnt``. To apply the same
manual addresses to every account, set them on each account config.

A standalone PJNATH application configures the array on
:cpp:any:`pj_ice_strans_stun_cfg::manual_host` (with
:cpp:any:`pj_ice_strans_stun_cfg::manual_host_cnt`) inside
:cpp:any:`pj_ice_strans_cfg`, before calling
:cpp:any:`pj_ice_strans_create()`.


pjsua CLI
~~~~~~~~~

There is no ``--ice-manual-host`` command-line option in the
pjsua sample app at present. Applications that want to set manual
hosts have to use the API.


When manual hosts are not enough
--------------------------------

Manual host candidates only solve the ICE side of the address
mismatch. If the SIP signalling path also goes through NAT, the
addresses in the SIP request URI, ``Contact`` header, and SDP
``c=`` line still need their own handling — typically via
:cpp:any:`pjsua_transport_config::public_addr` for the SIP
transport, and STUN or :cpp:any:`pjsua_acc_config::nat64_opt` for
SDP. See :doc:`nat_guide` for the broader NAT picture.

Manual host candidates also won't help when the inbound address is
not directly routable to the media socket — for example, when the
container's NAT does not forward UDP at all. In that case TURN
relaying is still required; configure a TURN server in addition to
the manual host. See :doc:`turn_tcp_tls`.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::AccountNatConfig::iceManualHost`
       (``SocketAddressVector`` of address strings)
     - :cpp:any:`pjsua_ice_config::ice_manual_host` /
       :cpp:any:`pjsua_ice_config::ice_manual_host_cnt`
       (``pj_sockaddr`` array)
   * - :cpp:any:`pj::AccountNatConfig::iceMaxHostCands`
     - :cpp:any:`pjsua_ice_config::ice_max_host_cands`
   * - (configured via
       :cpp:any:`pj::AccountNatConfig::iceManualHost`)
     - Standalone PJNATH:
       :cpp:any:`pj_ice_strans_stun_cfg::manual_host` /
       :cpp:any:`pj_ice_strans_stun_cfg::manual_host_cnt`


References
----------

- Feature PR: :pr:`4618`
- ICE candidate types and pairing: :rfc:`8445`

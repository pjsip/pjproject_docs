IPv6 and NAT64 support
=======================

.. contents:: Table of Contents
    :depth: 2


Availability
------------

IPv6 support is available on the following platforms:

- Windows
- Linux / Unix / macOS
- iOS
- Android

Both the GNU autotools (``./configure``) and CMake builds auto-detect
the host's IPv6 socket capabilities (``getaddrinfo``, ``IPV6_V6ONLY``)
at configure time. ``PJ_HAS_IPV6`` itself remains an explicit opt-in
via ``config_site.h`` (see below).


IPv6 Support in pjlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The work for adding IPv6 support in pjlib is documented by ticket :pr:`415`.

pjlib supports IPv6; enable it in ``pj/config_site.h``:

.. code-block:: c

    #define PJ_HAS_IPV6 1

**Socket Addresses**:

- An IPv4 socket address is represented by :cpp:any:`pj_sockaddr_in` structure, while an IPv6 socket address is represented by :cpp:any:`pj_sockaddr_in6` structure. The :cpp:any:`pj_sockaddr` is a union which may contain IPv4 or IPv6 socket address, depending on the address family field. 
- pjlib provides socket address APIs that work on both IPv4 and IPv6, including:

    - :cpp:any:`pj_inet_pton()`
    - :cpp:any:`pj_inet_ntop()`
    - :cpp:any:`pj_inet_ntop2()`
    - :cpp:any:`pj_sockaddr_init()`
    - :cpp:any:`pj_sockaddr_get_addr()`
    - :cpp:any:`pj_sockaddr_has_addr()`
    - :cpp:any:`pj_sockaddr_get_addr_len()`
    - :cpp:any:`pj_sockaddr_set_str_addr()`
    - :cpp:any:`pj_sockaddr_get_port()`
    - :cpp:any:`pj_sockaddr_set_port()`
    - :cpp:any:`pj_sockaddr_get_len()`

**Socket and IOQueue API**:

- The :cpp:any:`pj_sockaddr` structure is a union which may contain IPv4 or IPv6 socket address. Application may pass this structure to various pjlib socket functions which take :cpp:any:`pj_sockaddr_t` as an argument, such as :cpp:any:`pj_sock_bind()`, :cpp:any:`pj_sock_sendto()`, :cpp:any:`pj_sock_recvfrom()`, :cpp:any:`pj_sock_accept()`, etc. 
- The :cpp:any:`pj_ioqueue_t` also supports IPv6 sockets.


**Address Resolution API**:

- Use :cpp:any:`pj_getaddrinfo()` to resolve both IPv4 and IPv6 addresses. The older :cpp:any:`pj_gethostbyname()` is IPv4-only and is kept for backward compatibility.
- :cpp:any:`pj_gethostip()` and :cpp:any:`pj_getdefaultipinterface()` take an address family argument.

**IP Helper API:**

- :cpp:any:`pj_enum_ip_interface()` takes an address family argument.


IPv6 Support in pjsip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The work for adding IPv6 support in pjsip is documented by ticket :pr:`421`.


**IPv6 SIP Transport**:

- The SIP UDP transport supports IPv6 sockets via :cpp:any:`pjsip_udp_transport_start6()` and :cpp:any:`pjsip_udp_transport_attach2()`. To serve both IPv4 and IPv6 UDP, create two separate UDP transport instances, one per address family.
- The SIP TCP and TLS transports also support IPv6 sockets (ticket :pr:`1585`).


**IPv6 Address Representation**:

- IPv6 address may appear in two types of places in the SIP message: in a host part of a header field (such as host part of an URI, or host part in a Via header), and as a parameter value (such as the value of *received* and *maddr* parameter). 
- Although in the SIP ABNF grammar an IPv6 may or may not be enclosed in square brackets (**[** and **]** characters), in pjsip all IPv6 addresses will be represented **without** the square brackets, for consistency. This means pjsip will remove the square brackets, if they are present, during parsing process, and will enclose the address with square brackets as necessary when pjsip prints the Ipv6 address in a packet for transmission. When application inspects a message component that contains IPv6 address, it will always find it without the enclosing brackets.


IPv6 Support in pjlib-util (DNS SRV and AAAA resolution)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The work for adding IPv6 support in pjlib-util is documented by ticket :pr:`419` and continued in ticket :pr:`1927`.

DNS AAAA resolution will be performed for each DNS SRV record when flag :cpp:any:`PJ_DNS_SRV_RESOLVE_AAAA` or  :cpp:any:`PJ_DNS_SRV_RESOLVE_AAAA_ONLY` is set in ``option`` param when invoking :cpp:any:`pj_dns_srv_resolve()`. Also flag :cpp:any:`PJ_DNS_SRV_FALLBACK_AAAA` will allow resolver to fallback to DNS AAAA resolution when the SRV resolution fails.


IPv6 Support in pjmedia (SDP, media transport)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The work for adding IPv6 support in pjmedia is documented by ticket :issue:`420`.

The SDP representation and the UDP media transport both support IPv6
addresses. The following pjmedia fields carry addresses as a
:cpp:any:`pj_sockaddr` union (either IPv4 or IPv6):

- :cpp:any:`pjmedia_sock_info::rtp_addr_name` and
  :cpp:any:`pjmedia_sock_info::rtcp_addr_name`.
- :cpp:any:`pjmedia_stream_info::rem_addr` and
  :cpp:any:`pjmedia_stream_info::rem_rtcp`.


IPv6 Support in pjnath (ICE)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The work for adding IPv6 support in pjnath is documented by ticket :issue:`422`.

STUN, TURN, and ICE stream transports all support IPv6. An ICE stream
transport may carry multiple STUN and TURN transports, each of which
may use either IPv4 or IPv6 independently.

Fields in :cpp:any:`pj_ice_strans_cfg`:

- Deprecated ``af`` field, if it is set, the value will be ignored, address family setting is now specified via STUN/TURN transport setting, i.e: ``stun_tp.af`` and ``turn_tp.af``. 
- Deprecated ``stun`` and ``turn`` fields, but for backward compatibility, those fields will still be used only if ``stun_tp_cnt`` and/or ``turn_tp_cnt`` is set to zero. 
- Added ``stun_tp`` and ``turn_tp`` as replacement of ``stun`` and ``turn`` respectively, and they are array so application can have multiple STUN/TURN transports. 
- Added function :cpp:any:`pj_ice_strans_stun_cfg_default()` and :cpp:any:`pj_ice_strans_turn_cfg_default()` to initialize ``stun_tp`` and ``turn_tp`` respectively with default values.
- Added compile-time settings :c:macro:`PJ_ICE_MAX_STUN` and :c:macro:`PJ_ICE_MAX_TURN` to specify maximum number of STUN/TURN transports in each ICE component.


.. _ipv6_modes:

IPv6 Modes and Defaults (PJSIP 2.14+)
--------------------------------------

Starting from PJSIP 2.14 (:pr:`3590`), an account carries two independent
IPv6 preferences:

- :cpp:any:`pjsua_acc_config::ipv6_sip_use` — IP version preference for
  SIP signalling.
- :cpp:any:`pjsua_acc_config::ipv6_media_use` — IP version preference for
  RTP/RTCP media.

In PJSUA2 these map to ``AccountConfig::sipConfig.ipv6Use`` and
``AccountConfig::mediaConfig.ipv6Use`` respectively.

The two preferences are intentionally independent because signalling
and media usually traverse different paths:

- **SIP signalling** is endpoint-to-server (PBX, SBC, registrar). The
  address family is largely determined by what the provider supports,
  so ``ipv6_sip_use`` is a deployment decision against a single known
  peer.
- **RTP/RTCP media** is peer-to-peer (endpoint-to-endpoint, possibly
  relayed through a TURN server or media gateway). The remote peer's
  address family varies per call and is often outside your control, so
  ``ipv6_media_use`` is set to match the population of remotes your
  endpoint talks to (typically dual-stack).

Because of this split, it is common and valid to have, for example,
IPv6-only signalling (``PJSUA_IPV6_ENABLED_USE_IPV6_ONLY``) to a cloud
SIP provider while media stays dual-stack
(``PJSUA_IPV6_ENABLED_PREFER_IPV4`` or ``PJSUA_IPV6_ENABLED_PREFER_IPV6``)
so calls to legacy IPv4 peers still work.

The :cpp:any:`pjsua_ipv6_use` enum values:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Value
     - Meaning
   * - ``PJSUA_IPV6_DISABLED``
     - IPv4 only; IPv6 addresses/candidates are not used.
   * - ``PJSUA_IPV6_ENABLED_NO_PREFERENCE``
     - IPv6 is enabled; the actual IP version comes from whatever the OS
       resolver returns (typically RFC 6724 destination address
       selection). Legacy alias ``PJSUA_IPV6_ENABLED`` has the same
       meaning.
   * - ``PJSUA_IPV6_ENABLED_PREFER_IPV4``
     - Dual stack; the outgoing offer/request prefers IPv4 when both
       are available.
   * - ``PJSUA_IPV6_ENABLED_PREFER_IPV6``
     - Dual stack; the outgoing offer/request prefers IPv6 when both
       are available.
   * - ``PJSUA_IPV6_ENABLED_USE_IPV6_ONLY``
     - IPv6 only; IPv4 addresses/candidates are not used. Required for
       NAT64-only networks.

.. note::

   For brevity the rest of this page refers to each value by its
   suffix, e.g. ``USE_IPV6_ONLY`` for
   ``PJSUA_IPV6_ENABLED_USE_IPV6_ONLY`` and ``DISABLED`` for
   ``PJSUA_IPV6_DISABLED``. Use the full identifier names in code.

Preference only applies to the **outgoing** direction. For incoming
messages or offers, PJSIP accepts whichever IP version the remote
actually used, provided that family is enabled by the account's
configuration. In practice this means:

- ``DISABLED`` excludes IPv6 in both directions; an incoming IPv6
  offer on that account is rejected.
- ``USE_IPV6_ONLY`` excludes IPv4 in both directions; an incoming
  IPv4 offer on that account is rejected.
- The three dual-stack modes (``ENABLED_NO_PREFERENCE``,
  ``PREFER_IPV4``, ``PREFER_IPV6``) accept either family on incoming.

Defaults are asymmetric:

- ``ipv6_sip_use`` → ``PJSUA_IPV6_ENABLED_NO_PREFERENCE`` (SIP follows
  DNS/OS resolution).
- ``ipv6_media_use`` → ``PJSUA_IPV6_ENABLED_PREFER_IPV4`` (media is
  dual-stack capable but the offer prefers IPv4).

**Choosing a mode**:

- **IPv4-only deployment** — leave both at defaults, or set both to
  ``DISABLED`` to guarantee no IPv6 code paths are exercised.
- **Dual-stack deployment, v4-first network** — defaults are fine.
- **Dual-stack deployment, v6-first SIP provider** — set
  ``ipv6_sip_use = PJSUA_IPV6_ENABLED_PREFER_IPV6``.
- **IPv6-only SIP provider** — set both to ``USE_IPV6_ONLY``.
- **Mobile / NAT64 network** — set both to ``USE_IPV6_ONLY`` and enable
  ``nat64_opt = PJSUA_NAT64_ENABLED``; see :ref:`ipv6_nat64`. Required
  for iOS apps submitted to the App Store.

**Best practices for dual-stack deployments**:

- **Use hostnames, not IP literals.** Configure ``id``, ``reg_uri``,
  ``proxy`` and similar fields with DNS names (``sip:user@example.com``)
  rather than numeric IP literals. PJSIP's resolver then issues A and
  AAAA queries and lets the chosen mode decide which address family to
  use — no change to the account config is needed when the provider
  adds IPv6 (or vice versa).
- **Enable ICE for media.** With ICE, every call gathers both IPv4 and
  IPv6 candidates (plus server-reflexive and relayed candidates when
  STUN/TURN are configured) and picks whichever pair actually works
  with the remote. This is the only robust way to connect media across
  peers whose address families you don't control in advance. See the
  :doc:`ICE/STUN/TURN documentation <standalone_ice>`.
- **Provision a dual-stack TURN server.** On networks where direct
  peer-to-peer connectivity is flaky (cellular, corporate, NAT64), a
  TURN server that can allocate both IPv4 and IPv6 relays guarantees a
  fallback path across address families.
- **Plan for IP changes.** Hand-off between Wi-Fi (often IPv4) and
  cellular (often IPv6) frequently flips the address family of the
  endpoint. See :ref:`ipv6_ip_change` below.


Enabling IPv6 support in application using PJSUA-LIB
------------------------------------------------------------------
Application needs to configure SIP transport and SIP account with IPv6
support.


**Creating SIP transport**

Here is sample code for IPv6 SIP transport initializations.

.. code-block:: c

    pjsua_transport_config tp_cfg; 
    pjsip_transport_type_e tp_type;
    pjsua_transport_id tp_id = -1;

    pjsua_transport_config_default(&tp_cfg); 
    tp_cfg.port = 5060;

    /* TCP */ 
    tp_type = PJSIP_TRANSPORT_TCP6; 
    status = pjsua_transport_create(tp_type, &tp_cfg, &tp_id); 
    if (status != PJ_SUCCESS)
        ...

    /* UDP */ 
    tp_type = PJSIP_TRANSPORT_UDP6; 
    status = pjsua_transport_create(tp_type, &tp_cfg, &tp_id); 
    if (status != PJ_SUCCESS)
        ...

    /* TLS */ 
    tp_type = PJSIP_TRANSPORT_TLS6; 
    tp_cfg.port = 5061;
    tp_cfg.tls_setting.ca_list_file = pj_str("<path to CA file>");
    tp_cfg.tls_setting.cert_file = ...; 
    tp_cfg.tls_setting.privkey_file = ...;
    tp_cfg.tls_setting.password = ... 
    status = pjsua_transport_create(tp_type, &tp_cfg, &tp_id); 
    if (status != PJ_SUCCESS)
        ...


**SIP Account (PJSIP 2.14+)**

On 2.14 and later, configure the account's IP version preferences
directly via :cpp:any:`pjsua_acc_config::ipv6_sip_use` and
:cpp:any:`pjsua_acc_config::ipv6_media_use`. The runtime will then pick
an appropriate transport (or create one on demand) based on DNS
resolution and the chosen mode — no explicit ``transport_id`` binding
is required in the dual-stack case:

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);

    acc_cfg.id             = pj_str("sip:user@example.com");
    acc_cfg.reg_uri        = pj_str("sip:example.com");
    acc_cfg.cred_count     = 1;
    acc_cfg.cred_info[0].realm     = pj_str("*");
    acc_cfg.cred_info[0].scheme    = pj_str("digest");
    acc_cfg.cred_info[0].username  = pj_str("user");
    acc_cfg.cred_info[0].data_type = PJSIP_CRED_DATA_PLAIN_PASSWD;
    acc_cfg.cred_info[0].data      = pj_str("pwd");

    /* Dual-stack SIP and media; tune per deployment (see Modes above). */
    acc_cfg.ipv6_sip_use   = PJSUA_IPV6_ENABLED_NO_PREFERENCE;
    acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED_PREFER_IPV4;

    status = pjsua_acc_add(&acc_cfg, PJ_TRUE, NULL);

The equivalent PJSUA2 setup:

.. code-block:: c++

    AccountConfig acc_cfg;
    acc_cfg.idUri = "sip:user@example.com";
    acc_cfg.regConfig.registrarUri = "sip:example.com";
    AuthCredInfo cred("digest", "*", "user", 0, "pwd");
    acc_cfg.sipConfig.authCreds.push_back(cred);

    acc_cfg.sipConfig.ipv6Use   = PJSUA_IPV6_ENABLED_NO_PREFERENCE;
    acc_cfg.mediaConfig.ipv6Use = PJSUA_IPV6_ENABLED_PREFER_IPV4;

    Account *acc = new MyAccount();
    acc->create(acc_cfg);

**SIP Account (PJSIP < 2.14)**

On older releases, explicitly bind the account to an IPv6 transport
via :cpp:any:`pjsua_acc_config::transport_id` (or
:cpp:any:`pjsua_acc_set_transport()`), and set
``ipv6_media_use = PJSUA_IPV6_ENABLED``:

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);
    /* ... id, reg_uri, cred_info as above ... */

    /* Bind the account to the IPv6 transport created earlier. */
    acc_cfg.transport_id   = udp6_tp_id;  /* or tcp6_tp_id / tls6_tp_id */

    /* Enable IPv6 for media. */
    acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED;

    status = pjsua_acc_add(&acc_cfg, PJ_TRUE, NULL);


.. _ipv6_ip_change:

IPv4 ↔ IPv6 transitions during IP address change
--------------------------------------------------

Mobile endpoints frequently hop between IPv4 and IPv6 networks — for
example Wi-Fi (often IPv4) to cellular (often IPv6), or a corporate
VPN dropping and leaving only the native connection. When the address
family of the active interface changes, several things can break:

- **Existing dialogs still reference the old family.** The Contact and
  Via URIs in an established call contain the old address; once the
  interface goes away, the remote has no way to reach the endpoint.
- **SIP transports bound to the old family are unusable.** A
  UDP6/TCP6/TLS6 transport bound to a now-gone IPv6 address cannot
  send, and the registrar's re-registration attempts time out.
- **Media (RTP/RTCP) is pointed at the old address.** Even if
  signalling survives, media won't flow without a new offer/answer.
- **If ICE wasn't enabled**, there is no pre-gathered alternative
  candidate to fall back to — the call typically has to be dropped.

**Mechanism.** Call :cpp:any:`pjsua_handle_ip_change()` when the OS
reports a network change. It re-resolves, re-creates transports if
needed, re-registers, and issues re-INVITEs on active calls so media
addresses are updated. :pr:`3910` improved the v4↔v6 path so the
transition works when the address family flips. :pr:`4067` further
refined the IP-version selection in the re-generated SDP offer so it
matches the account's ``ipv6_media_use`` mode after the transport is
re-created. See the dedicated :doc:`IP address change guide
<ip_change>` for the full mechanism.

**Design guidance.** To make these transitions survivable:

- **Configure the account for the union of address families you expect
  to see.** An endpoint that might move to an IPv6-only cellular leg
  should not be ``ipv6_sip_use = DISABLED``; use
  ``ENABLED_NO_PREFERENCE`` or ``ENABLED_PREFER_IPV6`` so PJSIP can
  actually pick the new family after the hand-off.
- **Enable ICE for media** (see best practices above) so both families'
  candidates are already gathered at call setup; re-INVITEs after an
  IP change can then nominate a new candidate pair without a full
  media renegotiation stall.
- **Use DNS names for the registrar and proxy.** After the
  hand-off, re-resolution picks whichever family works from the new
  interface; an IP literal may be unreachable from the new network.


.. _ipv6_nat64:

NAT64
-----

In its doc, Apple suggests/requires that applications are capable of
`supporting IPv6 DNS64/NAT64 Networks <https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/NetworkingOverview/UnderstandingandPreparingfortheIPv6Transition/UnderstandingandPreparingfortheIPv6Transition.html>`__.
A common misconception in the SIP world is that by using NAT64, IPv4 and
IPv6 interoperability can be automatically achieved (i.e. SIP
registration, calls, and media flow will work seamlessly and smoothly
between any two endpoints regardless of their address families
(IPv4/IPv6)). As the doc says:
``This (DNS64/NAT64) is an IPv6-only network that continues to provide access to IPv4 content through translation``,
so a client behind a NAT64 network can reach an IPv4 endpoint, but not
necessarily the other way around.

In more detail, an IPv6-only SIP client behind a NAT64 can communicate
with IPv6 (or dual stack) server or clients just fine, but will
experience problems with IPv4-only server or clients, because there are
IPv6 address literals in the SIP/SDP fields (Via, Contact, SDP), which
the IPv4 instance cannot understand.

According to :rfc:`6157` (IPv6 Transition in the Session Initiation Protocol (SIP)): 

* Section 3.1:

  *In order to support both IPv4-only and IPv6-only user agents, it is RECOMMENDED that domains deploy dual-stack outbound proxy servers or, alternatively, deploy both IPv4-only and IPv6-only outbound proxies.*

* Section 4:

  *An IPv6 node SHOULD also be able to send and receive media using IPv4 addresses, but if it cannot, it SHOULD support Session Traversal Utilities for NAT (STUN) relay usage [8].*

* Section 4.2:

  *When following the ICE procedures, in addition to local addresses, user agents may need to obtain addresses from relays; for example, an IPv6 user agent would obtain an IPv4 address from a relay.*

* Section 4.2:

  *Implementations are encouraged to use ICE; however, the normative strength of the text above is left at a SHOULD since in some managed networks (such as a closed enterprise network) it is possible for the administrator to have control over the IP version utilized in all nodes and thus deploy an IPv6-only network, for example.  The use of ICE can be avoided for signaling messages that stay within such managed networks.*

  (our note:⇒ which means when network is not standardized to one IP version, the use of ICE is a "must").

Therefore, to support IPv6-IPv4 interoperability in NAT64 environment:

#. Our RECOMMENDATION is that when the client is put with an IPv6-only connectivity, the SIP server must also support IPv6  connectivity. For  the media, user needs a "dual stack" TURN (a TURN server which supports IPv6 connectivity and able to provide an IPv4 relay address upon request). Then all the application needs to do is enable ICE and use TURN (support for dual stack TURN is only available in PJSIP 2.6 or later). 
#. If 1) is not possible (no IPv6 server or not desirable to use TURN), we will need to replace all IPv6 occurrences with IPv4 in the SIP messages and SDP. This feature is available in release 2.7.

   a. Set :cpp:any:`pjsua_config::stun_try_ipv6` so PJSIP will resolve
      the STUN server(s) via AAAA as well as A.
   b. Create a UDP6 transport; the STUN server on the IPv4 network will
      hand back an IPv4-mapped address through the NAT64 translator.
   c. Configure the account as IPv6-only for both signalling and media,
      and enable NAT64.

   PJSIP 2.14+ (PJSUA-LIB):

   .. code-block:: c

        cfg->stun_try_ipv6 = PJ_TRUE;

        tp_type = PJSIP_TRANSPORT_UDP6;
        status = pjsua_transport_create(tp_type, &tp_cfg, &udp6_tp_id);

        acc_cfg.ipv6_sip_use   = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.nat64_opt      = PJSUA_NAT64_ENABLED;

   PJSIP 2.14+ (PJSUA2):

   .. code-block:: c++

        ep_cfg.uaConfig.stunTryIpv6 = true;

        acc_cfg.sipConfig.ipv6Use   = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.mediaConfig.ipv6Use = PJSUA_IPV6_ENABLED_USE_IPV6_ONLY;
        acc_cfg.natConfig.nat64Opt  = PJSUA_NAT64_ENABLED;

   For PJSIP < 2.14, replace the ``ipv6_*_use`` fields with an
   explicit ``acc_cfg.transport_id = udp6_tp_id`` binding and
   ``acc_cfg.ipv6_media_use = PJSUA_IPV6_ENABLED``.


References
------------

* Dual-stack IPv4&IPv6 account config (PJSIP 2.14): :pr:`3590`
* Improve IP address change IPv4 ↔ IPv6 (PJSIP 2.15): :pr:`3910`
* Update IP version choosing logic in media transport for SDP offer
  (PJSIP 2.15): :pr:`4067`
* Enable IPv6 in ICE transport/TURN in PJSUA: :pr:`1971`
* NAT64 support for IPv4 interoperability: :pr:`2032`
* IPv6 support in PJNATH: :issue:`422`
* Address resolution: :pr:`1926`
* DNS SRV resolution: :pr:`1927`



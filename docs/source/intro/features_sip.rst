SIP Capabilities
----------------

List of supported SIP features and link to the relevant PJSIP documentation and/or the standard document.


-  Base specs:

   -  Core methods: `RFC 3261 <http://tools.ietf.org/html/rfc3261>`__:
      INVITE, CANCEL, BYE, REGISTER, OPTIONS, INFO
   -  Digest authentication (`RFC
      2617 <http://tools.ietf.org/html/rfc2617>`__)

-  Transports:

   -  UDP, TCP, TLS (server or mutual)
   -  DNS SRV resolution (`RFC
      3263 <http://tools.ietf.org/html/rfc3263>`__)
   -  IPv6
   -  `QoS <QoS>`__ (DSCP, WMM)

-  Routing/NAT:

   -  rport (`RFC 3581 <http://tools.ietf.org/html/rfc3581>`__)
   -  Service-Route header (`RFC
      3608 <http://tools.ietf.org/html/rfc3608>`__)
   -  SIP outbound for TCP/TLS (`RFC
      5626 <http://tools.ietf.org/html/rfc5626>`__)
   -  Path header (with SIP outbound) (`RFC
      3327 <http://tools.ietf.org/html/rfc3327>`__)

-  Call:

   -  Offer/answer (`RFC 3264 <http://tools.ietf.org/html/rfc3264>`__)
   -  hold, unhold
   -  `redirection <SIP_Redirection>`__
   -  transfer/REFER (attended and unattended):

      -  Base (`RFC 3515 <http://tools.ietf.org/html/rfc3515>`__)
      -  replaces (`RFC 3891 <http://tools.ietf.org/html/rfc3891>`__)
      -  Referred-by (`RFC 3892 <http://tools.ietf.org/html/rfc3892>`__)

   -  sipfrag support (`RFC
      3420 <http://tools.ietf.org/html/rfc3420>`__)
   -  norefersub (`RFC 4488 <http://tools.ietf.org/html/rfc4488>`__)
   -  UPDATE (`RFC 3311 <http://tools.ietf.org/html/rfc3311>`__)
   -  100rel/PRACK (`RFC 3262 <http://tools.ietf.org/html/rfc3262>`__)
   -  tel: URI (`RFC 3966 <http://tools.ietf.org/html/rfc3966>`__)
   -  Session Timers (`RFC 4028 <http://tools.ietf.org/html/rfc4028>`__)
   -  Reason header (`RFC 3326 <http://tools.ietf.org/html/rfc3326>`__,
      `partially
      supported <https://trac.pjsip.org/repos/wiki/FAQ#custom-header>`__)
   -  P-Header (`RFC 3325 <http://tools.ietf.org/html/rfc3325>`__,
      `partially
      supported <https://trac.pjsip.org/repos/wiki/FAQ#custom-header>`__)

-  SDP:

   -  `RFC 2327 <http://tools.ietf.org/html/rfc2327>`__ (obsoleted by
      `RFC 4566 <http://tools.ietf.org/html/rfc4566>`__)
   -  RTCP attribute (`RFC 3605 <http://tools.ietf.org/html/rfc3605>`__)
   -  IPv6 support (`RFC 3266 <http://tools.ietf.org/html/rfc3266>`__)

-  Multipart (`RFC 2046 <http://tools.ietf.org/html/rfc2046>`__, `RFC
   5621 <http://tools.ietf.org/html/rfc5621>`__)
-  Presence and IM:

   -  Event framework (SUBSCRIBE, NOTIFY) (`RFC
      3265 <http://tools.ietf.org/html/rfc3265>`__)
   -  Event publication (PUBLISH) (`RFC
      3903 <http://tools.ietf.org/html/rfc3903>`__)
   -  MESSAGE (`RFC 3428 <http://tools.ietf.org/html/rfc3428>`__)
   -  typing indication (`RFC
      3994 <http://tools.ietf.org/html/rfc3994>`__)
   -  pidf+xml (`RFC 3856 <http://tools.ietf.org/html/rfc3856>`__, `RFC
      3863 <http://tools.ietf.org/html/rfc3863>`__)
   -  xpidf+xml
   -  RPID (subset) (`RFC 4480 <http://tools.ietf.org/html/rfc4480>`__)

-  Other extensions:

   -  INFO (`RFC 2976 <http://tools.ietf.org/html/rfc2976>`__)
   -  AKA, AKA-v2 authentication (`RFC
      3310 <http://tools.ietf.org/html/rfc3310>`__, `RFC
      4169 <http://tools.ietf.org/html/rfc4169>`__)
   -  ICE option tag (`RFC 5768 <http://tools.ietf.org/html/rfc5768>`__)
   -  `Message summary/message waiting
      indication <https://trac.pjsip.org/repos/ticket/982>`__ (MWI, `RFC
      3842 <http://tools.ietf.org/html/rfc3842>`__)

-  Compliance, best current practices:

   -  Issues with Non-INVITE transaction (`RFC
      4320 <http://tools.ietf.org/html/rfc4320>`__)
   -  Issues with INVITE transaction (`RFC
      4321 <http://tools.ietf.org/html/rfc4321>`__)
   -  Multiple dialog usages (`RFC
      5057 <http://tools.ietf.org/html/rfc5057>`__)
   -  SIP torture messages (`RFC
      4475 <http://tools.ietf.org/html/rfc4475>`__, tested when
      applicable)
   -  SIP torture for IPv6 (`RFC
      5118 <http://tools.ietf.org/html/rfc5118>`__)
   -  Message Body Handling (`RFC
      5621 <http://tools.ietf.org/html/rfc5621>`__. Partial compliance:
      multipart is supported, but *Content-Disposition* header is not
      handled)
   -  The use of SIPS (`RFC 5630 <http://tools.ietf.org/html/rfc5630>`__. Partial compliance:
      SIPS is supported, but still make use of *transport=tls*
      parameter)


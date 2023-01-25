SIP Capabilities
-----------------

List of supported SIP features and link to the relevant PJSIP documentation and/or the standard document.


Base specs
~~~~~~~~~~~~~~~~~

- Core methods: `RFC 3261 <https://datatracker.ietf.org/doc/html/rfc3261>`__:
  INVITE, CANCEL, BYE, REGISTER, OPTIONS, INFO
- Digest authentication (`RFC 2617 <https://datatracker.ietf.org/doc/html/rfc2617>`__)
- Encoding and parsing of Bearer authenticaion (OAuth 2.0)
  (`RFC 8898 <https://datatracker.ietf.org/doc/html/rfc8898>`__)

Transports
~~~~~~~~~~~~~~
-  UDP, TCP, TLS (server or mutual)
-  DNS SRV resolution (`RFC  3263 <https://datatracker.ietf.org/doc/html/rfc3263>`__)
-  IPv6
-  `QoS <QoS>`__ (DSCP, WMM)

Routing/NAT
~~~~~~~~~~~~~~~
- rport (`RFC 3581 <https://datatracker.ietf.org/doc/html/rfc3581>`__)
- Service-Route header (`RFC 3608 <https://datatracker.ietf.org/doc/html/rfc3608>`__)
- SIP outbound for TCP/TLS (`RFC 5626 <https://datatracker.ietf.org/doc/html/rfc5626>`__)
- Path header (with SIP outbound) (`RFC 3327 <https://datatracker.ietf.org/doc/html/rfc3327>`__)
- ICE option tag (`RFC 5768 <https://datatracker.ietf.org/doc/html/rfc5768>`__)
- Trickle ICE on SIP: (`RFC 8840 <https://datatracker.ietf.org/doc/html/rfc8840>`__)


Call
~~~~~~~~~~~~~~~~
-  Offer/answer (`RFC 3264 <https://datatracker.ietf.org/doc/html/rfc3264>`__)
-  hold, unhold
-  `redirection <SIP_Redirection>`__
-  transfer/REFER (attended and unattended):

   -  Base (`RFC 3515 <https://datatracker.ietf.org/doc/html/rfc3515>`__)
   -  replaces (`RFC 3891 <https://datatracker.ietf.org/doc/html/rfc3891>`__)
   -  Referred-by (`RFC 3892 <https://datatracker.ietf.org/doc/html/rfc3892>`__)

-  sipfrag support (`RFC 3420 <https://datatracker.ietf.org/doc/html/rfc3420>`__)
-  norefersub (`RFC 4488 <https://datatracker.ietf.org/doc/html/rfc4488>`__)
-  UPDATE (`RFC 3311 <https://datatracker.ietf.org/doc/html/rfc3311>`__)
-  100rel/PRACK (`RFC 3262 <https://datatracker.ietf.org/doc/html/rfc3262>`__)
-  tel: URI (`RFC 3966 <https://datatracker.ietf.org/doc/html/rfc3966>`__)
-  Session Timers (`RFC 4028 <https://datatracker.ietf.org/doc/html/rfc4028>`__)
-  Reason header (`RFC 3326 <https://datatracker.ietf.org/doc/html/rfc3326>`__,
   :ref:`partially supported <guide_adding_custom_header>`)
-  P-Header (`RFC 3325 <https://datatracker.ietf.org/doc/html/rfc3325>`__,
   :ref:`partially supported <guide_adding_custom_header>`)

SDP
~~~~~~~~~~~~~
- `RFC 2327 <https://datatracker.ietf.org/doc/html/rfc2327>`__ (obsoleted by
  `RFC 4566 <https://datatracker.ietf.org/doc/html/rfc4566>`__)
- RTCP attribute (`RFC 3605 <https://datatracker.ietf.org/doc/html/rfc3605>`__)
- IPv6 support (`RFC 3266 <https://datatracker.ietf.org/doc/html/rfc3266>`__)
- SDP media ID (`RFC 5888 <https://datatracker.ietf.org/doc/html/rfc5888>`__)
- SDP for ICE (`RFC 8839 <https://datatracker.ietf.org/doc/html/rfc8839>`__)

   
Presence and IM
~~~~~~~~~~~~~~~~~~~~~
-  Event framework (SUBSCRIBE, NOTIFY) (`RFC 3265 <https://datatracker.ietf.org/doc/html/rfc3265>`__)
-  Event publication (PUBLISH) (`RFC 3903 <https://datatracker.ietf.org/doc/html/rfc3903>`__)
-  MESSAGE (`RFC 3428 <https://datatracker.ietf.org/doc/html/rfc3428>`__)
-  typing indication (`RFC 3994 <https://datatracker.ietf.org/doc/html/rfc3994>`__)
-  pidf+xml (`RFC 3856 <https://datatracker.ietf.org/doc/html/rfc3856>`__, 
   `RFC 3863 <https://datatracker.ietf.org/doc/html/rfc3863>`__)
-  xpidf+xml 
-  RPID (subset) (`RFC 4480 <https://datatracker.ietf.org/doc/html/rfc4480>`__)


Other extensions
~~~~~~~~~~~~~~~~~~~~~~~~
-  INFO (`RFC 2976 <https://datatracker.ietf.org/doc/html/rfc2976>`__)
-  AKA, AKA-v2 authentication (`RFC 3310 <https://datatracker.ietf.org/doc/html/rfc3310>`__, 
   `RFC 4169 <https://datatracker.ietf.org/doc/html/rfc4169>`__)
-  ICE option tag (`RFC 5768 <https://datatracker.ietf.org/doc/html/rfc5768>`__)
-  `Message summary/message waiting indication <https://github.com/pjsip/pjproject/issues/982>`__ 
   (MWI, `RFC 3842 <https://datatracker.ietf.org/doc/html/rfc3842>`__)
-  Multipart (`RFC 2046 <https://datatracker.ietf.org/doc/html/rfc2046>`__, 
   `RFC 5621 <https://datatracker.ietf.org/doc/html/rfc5621>`__)


Compliance, best current practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-  Issues with Non-INVITE transaction (`RFC 4320 <https://datatracker.ietf.org/doc/html/rfc4320>`__)
-  Issues with INVITE transaction (`RFC 4321 <https://datatracker.ietf.org/doc/html/rfc4321>`__)
-  Multiple dialog usages (`RFC 5057 <https://datatracker.ietf.org/doc/html/rfc5057>`__)
-  SIP torture messages (`RFC 4475 <https://datatracker.ietf.org/doc/html/rfc4475>`__, tested when
   applicable)
-  SIP torture for IPv6 (`RFC 5118 <https://datatracker.ietf.org/doc/html/rfc5118>`__)
-  Message Body Handling (`RFC 5621 <https://datatracker.ietf.org/doc/html/rfc5621>`__. 
   Partial compliance: multipart is supported, but *Content-Disposition* header is not
   handled)
-  The use of SIPS (`RFC 5630 <https://datatracker.ietf.org/doc/html/rfc5630>`__. 
   Partial compliance: SIPS is supported, but still make use of *transport=tls*
   parameter)

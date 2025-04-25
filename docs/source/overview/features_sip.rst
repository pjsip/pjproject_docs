SIP Capabilities
-----------------

.. contents:: Table of Contents
    :depth: 2

List of supported SIP features and link to the relevant PJSIP documentation and/or the standard document.


Base specs
~~~~~~~~~~~~~~~~~

- Core methods: :rfc:`3261`:
  INVITE, CANCEL, BYE, REGISTER, OPTIONS, INFO
- Digest authentication (:rfc:`2617`)
- Encoding and parsing of Bearer authentication (OAuth 2.0)
  (:rfc:`8898`)

Transports
~~~~~~~~~~~~~~
-  UDP, :any:`TCP </specific-guides/network_nat/sip_tcp>`, 
   :any:`TLS (server or mutual) </specific-guides/security/ssl>`
-  DNS SRV resolution (:rfc:`3263`)
-  :any:`IPv6 </specific-guides/network_nat/ipv6>`
-  :any:`QoS </specific-guides/network_nat/qos>` (DSCP, WMM)

Routing/NAT
~~~~~~~~~~~~~~~
- rport (:rfc:`3581`)
- Service-Route header (:rfc:`3608`)
- SIP outbound for TCP/TLS (:rfc:`5626`)
- Path header (with SIP outbound) (:rfc:`3327`)
- ICE option tag (:rfc:`5768`)
- :any:`Trickle ICE </specific-guides/network_nat/trickle_ice>` on SIP: (:rfc:`8840`)


Call
~~~~~~~~~~~~~~~~
-  Offer/answer (:rfc:`3264`)
-  hold, unhold
-  :any:`redirection </specific-guides/sip/redirection>`
-  transfer/REFER (attended and unattended):

   -  Base (:rfc:`3515`)
   -  replaces (:rfc:`3891`)
   -  Referred-by (:rfc:`3892`)

-  sipfrag support (:rfc:`3420`)
-  norefersub (:rfc:`4488`)
-  UPDATE (:rfc:`3311`)
-  100rel/PRACK (:rfc:`3262`)
-  tel: URI (:rfc:`3966`)
-  Session Timers (:rfc:`4028`)
-  Reason header (:rfc:`3326`,
   :ref:`partially supported <guide_adding_custom_header>`)
-  P-Header (:rfc:`3325`,
   :ref:`partially supported <guide_adding_custom_header>`)

SDP
~~~~~~~~~~~~~
- :rfc:`2327` (obsoleted by
  :rfc:`4566`)
- RTCP attribute (:rfc:`3605`)
- :any:`IPv6 support </specific-guides/network_nat/ipv6>` (:rfc:`3266`)
- SDP media ID (:rfc:`5888`)
- SDP for ICE (:rfc:`8839`)

   
Presence and IM
~~~~~~~~~~~~~~~~~~~~~
-  Event framework (SUBSCRIBE, NOTIFY) (:rfc:`3265`)
-  Event publication (PUBLISH) (:rfc:`3903`)
-  MESSAGE (:rfc:`3428`)
-  typing indication (:rfc:`3994`)
-  pidf+xml (:rfc:`3856`, 
   :rfc:`3863`)
-  xpidf+xml 
-  RPID (subset) (:rfc:`4480`)


Other extensions
~~~~~~~~~~~~~~~~~~~~~~~~
-  INFO (:rfc:`2976`)
-  AKA, AKA-v2 authentication (:rfc:`3310`, 
   :rfc:`4169`)
-  ICE option tag (:rfc:`5768`)
-  `Message summary/message waiting indication <https://github.com/pjsip/pjproject/issues/982>`__ 
   (MWI, :rfc:`3842`)
-  Multipart (:rfc:`2046`, 
   :rfc:`5621`)


Compliance, best current practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-  Issues with Non-INVITE transaction (:rfc:`4320`)
-  Issues with INVITE transaction (:rfc:`4321`)
-  Multiple dialog usages (:rfc:`5057`)
-  SIP torture messages (:rfc:`4475`, tested when
   applicable)
-  SIP torture for IPv6 (:rfc:`5118`)
-  Message Body Handling (:rfc:`5621`. 
   Partial compliance: multipart is supported, but *Content-Disposition* header is not
   handled)
-  The use of SIPS (:rfc:`5630`. 
   Partial compliance: SIPS is supported, but still make use of *transport=tls*
   parameter)

NAT Traversal
-------------

-  :ref:`ice`:

   -  `RFC 5245 <https://datatracker.ietf.org/doc/html/rfc5245>`__
   -  host, srflx, and relayed candidates
   -  aggressive and regular nomination
   -  ICE option tag (`RFC 5768 <https://datatracker.ietf.org/doc/html/rfc5768>`__)
   -  IPv4, IPv6, NAT64 support
   -  `Trickle ICE <https://github.com/pjsip/pjproject/pull/2588>`__, with support for the following standards:

      * Trickle ICE (`RFC 8838 <https://datatracker.ietf.org/doc/html/rfc8838>`__)
      * Trickle ICE on SIP: (`RFC 8840 <https://datatracker.ietf.org/doc/html/rfc8840>`__)
      * SIP INFO Package (`RFC 6086 <https://datatracker.ietf.org/doc/html/rfc6086>`__)
      * SDP for ICE (`RFC 8839 <https://datatracker.ietf.org/doc/html/rfc8839>`__)
      * SDP media ID (`RFC 5888 <https://datatracker.ietf.org/doc/html/rfc5888>`__)

-  :ref:`TURN <turn>`:

   -  `RFC 5766 <https://datatracker.ietf.org/doc/html/rfc5766>`__
   -  DNS SRV resolution
   -  UDP, TCP, :doc:`TLS </specific-guides/security/ssl>` client connection
   -  TCP allocations, `accept <https://github.com/pjsip/pjproject/issues/2197>`__ and 
      `connect <https://github.com/pjsip/pjproject/pull/2754>`__ mode 
      (`RFC 6062 <https://datatracker.ietf.org/doc/html/rfc6062>`__)
   - IPv4/IPv6 allocations

-  :ref:`uPnP <upnp>`
-  :ref:`STUN <stun>`:

   -  `RFC 5389 <https://datatracker.ietf.org/doc/html/rfc5389>`__
   -  Some `RFC 3489 <https://datatracker.ietf.org/doc/html/rfc3489>`__
      compatibility
   -  DNS SRV resolution
   -  short/long term authentication
   -  fingerprinting

-  :ref:`NAT type detection <nat_detect>`:

   -  legacy `RFC 3489 <https://datatracker.ietf.org/doc/html/rfc3489>`__

-  Other:

   -  :ref:`qos`


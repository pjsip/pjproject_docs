NAT Traversal
-------------

-  :ref:`ICE <ice>`:

   -  `RFC 5245 <http://tools.ietf.org/html/rfc5245>`__
   -  host, srflx, and relayed candidates
   -  aggressive and regular nomination
   -  ICE option tag (`RFC 5768 <http://tools.ietf.org/html/rfc5768>`__)
   -  IPv4, IPv6, NAT64 support
   -  `Trickle ICE <https://github.com/pjsip/pjproject/pull/2588>`_, with support for the following standards:

      * Trickle ICE: https://tools.ietf.org/html/draft-ietf-ice-trickle-21
      * Trickle ICE on SIP: https://tools.ietf.org/html/draft-ietf-mmusic-trickle-ice-sip-18
      * SIP INFO Package: https://tools.ietf.org/html/rfc6086
      * SDP for ICE: https://tools.ietf.org/html/draft-ietf-mmusic-ice-sip-sdp-39
      * SDP media ID: https://tools.ietf.org/html/rfc5888      

-  :ref:`TURN <turn>`:

   -  `RFC 5766 <http://tools.ietf.org/html/rfc5766>`__
   -  DNS SRV resolution
   -  UDP, TCP, TLS client connection
   -  TCP allocations, `accept <https://github.com/pjsip/pjproject/issues/2197>`_ and 
      `connect <https://github.com/pjsip/pjproject/pull/2754>`_ mode 
      (`RFC 6062 <http://tools.ietf.org/html/rfc6062>`__)
   - IPv4/IPv6 allocations

-  :ref:`uPnP <upnp>`
-  :ref:`STUN <stun>`:

   -  `RFC 5389 <http://tools.ietf.org/html/rfc5389>`__
   -  Some `RFC 3489 <http://tools.ietf.org/html/rfc3489>`__
      compatibility
   -  DNS SRV resolution
   -  short/long term authentication
   -  fingerprinting

-  :ref:`NAT type detection <nat_detect>`:

   -  legacy `RFC 3489 <http://tools.ietf.org/html/rfc3489>`__

-  Other:

   -  :ref:`qos`


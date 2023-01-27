NAT Traversal
-------------

-  :ref:`ice`:

   -  :rfc:`5245`
   -  host, srflx, and relayed candidates
   -  aggressive and regular nomination
   -  ICE option tag (:rfc:`5768`)
   -  IPv4, IPv6, NAT64 support
   -  `Trickle ICE <https://github.com/pjsip/pjproject/pull/2588>`__, with support for the following standards:

      * Trickle ICE (:rfc:`8838`)
      * Trickle ICE on SIP: (:rfc:`8840`)
      * SIP INFO Package (:rfc:`6086`)
      * SDP for ICE (:rfc:`8839`)
      * SDP media ID (:rfc:`5888`)

-  :ref:`TURN <turn>`:

   -  :rfc:`5766`
   -  DNS SRV resolution
   -  UDP, TCP, :doc:`TLS </specific-guides/security/ssl>` client connection
   -  TCP allocations, `accept <https://github.com/pjsip/pjproject/issues/2197>`__ and 
      `connect <https://github.com/pjsip/pjproject/pull/2754>`__ mode 
      (:rfc:`6062`)
   - IPv4/IPv6 allocations

-  :ref:`uPnP <upnp>`
-  :ref:`STUN <stun>`:

   -  :rfc:`5389`
   -  Some :rfc:`3489`
      compatibility
   -  DNS SRV resolution
   -  short/long term authentication
   -  fingerprinting

-  :ref:`NAT type detection <nat_detect>`:

   -  legacy :rfc:`3489`

-  Other:

   -  :ref:`qos`


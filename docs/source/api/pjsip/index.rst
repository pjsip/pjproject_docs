PJSIP
============================================

PJSIP is an Open Source SIP prototol stack, designed to be very small in footprint, 
have high performance, and very flexible.



API Reference
---------------------

Compile Time Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`PJSIP </api/generated/pjsip/group/group__PJSIP__CONFIG>`
- :doc:`Error codes </api/generated/pjsip/group/group__PJSIP__CORE__ERRNO>`

Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Endpoint </api/generated/pjsip/group/group__PJSIP__ENDPT>`
- :doc:`Event </api/generated/pjsip/group/group__PJSIP__EVENT>`
- :doc:`Modules </api/generated/pjsip/group/group__PJSIP__MOD>`
- :doc:`Message Creation and Stateless Operations </api/generated/pjsip/group/group__PJSIP__ENDPT__STATELESS>`

Message Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Methods </api/generated/pjsip/group/group__PJSIP__MSG__METHOD>`
- :doc:`Header Fields </api/generated/pjsip/group/group__PJSIP__MSG__HDR>`
- :doc:`Request and Status Liine </api/generated/pjsip/group/group__PJSIP__MSG__LINE>`
- :doc:`Message Structure </api/generated/pjsip/group/group__PJSIP__MSG__MSG>`
- :doc:`Multipart Message Body </api/generated/pjsip/group/group__PJSIP__MULTIPART>`
- :doc:`The Parser </api/generated/pjsip/group/group__PJSIP__PARSER>`
- URI:

  - :doc:`Generic URI </api/generated/pjsip/group/group__PJSIP__URI__GENERIC>`
  - :doc:`SIP URI </api/generated/pjsip/group/group__PJSIP__SIP__URI>`
  - :doc:`tel URI </api/generated/pjsip/group/group__PJSIP__TEL__URI>`
  - :doc:`Other URI schemes </api/generated/pjsip/group/group__PJSIP__OTHER__URI>`
  - :doc:`URI Parameter Container</api/generated/pjsip/group/group__PJSIP__URI__PARAM>`
  
- :doc:`Media/MIME </api/generated/pjsip/group/group__PJSIP__MSG__MEDIA>`
- :doc:`Message Body </api/generated/pjsip/group/group__PJSIP__MSG__BODY>`


Transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Transport API </api/generated/pjsip/group/group__PJSIP__TRANSPORT>`
- :doc:`DNS SRV Resolution </api/generated/pjsip/group/group__PJSIP__RESOLVE>`
- :doc:`Loop </api/generated/pjsip/group/group__PJSIP__TRANSPORT__LOOP>`
- :doc:`TCP </api/generated/pjsip/group/group__PJSIP__TRANSPORT__TCP>`
- :doc:`TLS </api/generated/pjsip/group/group__PJSIP__TRANSPORT__TLS>`
- :doc:`UDP </api/generated/pjsip/group/group__PJSIP__TRANSPORT__UDP>`


Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Authentication </api/generated/pjsip/group/group__PJSIP__AUTH__API>`
- :doc:`Digest AKAv1 and AKAv2 </api/generated/pjsip/group/group__PJSIP__AUTH__AKA__API>`

Transaction Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Transaction </api/generated/pjsip/group/group__PJSIP__TRANSACT__TRANSACTION>`
- :doc:`Stateful Operations </api/generated/pjsip/group/group__PJSIP__TRANSACT__UTIL>`

Base UA/Common Dialog Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Dialog </api/generated/pjsip/group/group__PJSIP__DIALOG>`
- :doc:`UA Module </api/generated/pjsip/group/group__PJSUA__UA>`
- :doc:`Core Proxy Layer </api/generated/pjsip/group/group__PJSIP__PROXY__CORE>`

User Agent Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`INVITE Session </api/generated/pjsip/group/group__PJSIP__INV>`
- :doc:`100rel/PRACK - Reliability of Provisional Responses </api/generated/pjsip/group/group__PJSIP__100REL>`
- :doc:`Client Registration </api/generated/pjsip/group/group__PJSUA__REGC>`
- :doc:`SIP Replaces support (RFC 3891 - "Replaces" Header) </api/generated/pjsip/group/group__PJSIP__REPLACES>`
- :doc:`SIP Session Timers support (RFC 4028 - Session Timers in SIP) </api/generated/pjsip/group/group__PJSIP__TIMER>`
- :doc:`SIP REFER (RFC 3515) for Call Transfer etc. </api/generated/pjsip/group/group__PJSUA__XFER>`

Event and Presence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Event Notification (RFC 3265) Module </api/generated/pjsip/group/group__PJSIP__EVENT__NOT>`
- :doc:`Additional Event Header Fields </api/generated/pjsip/group/group__PJSIP__EVENT__HDRS>`
- :doc:`Message Composition Indication (RFC 3994) </api/generated/pjsip/group/group__PJSIP__ISCOMPOSING>`
- :doc:`SIP Message Summary and Message Waiting Indication (RFC 3842) </api/generated/pjsip/group/group__mwi>`
- :doc:`PIDF/Presence Information Data Format (RFC 3863) </api/generated/pjsip/group/group__PJSIP__SIMPLE__PIDF>`
- :doc:`SIP Extension for Presence (RFC 3856) </api/generated/pjsip/group/group__PJSIP__SIMPLE__PRES>`
- :doc:`SIP Event State Publication (PUBLISH, RFC 3903) </api/generated/pjsip/group/group__PJSIP__SIMPLE__PUBLISH>`
- :doc:`RPID/Rich Presence Extensions to PIDF (RFC 4480) </api/generated/pjsip/group/group__PJSIP__SIMPLE__RPID>`
- :doc:`XPIDF/Presence Information Data Format </api/generated/pjsip/group/group__PJSIP__SIMPLE__XPIDF>`

PJSIP
============================================

PJSIP is an Open Source SIP prototol stack, designed to be very small in footprint, 
have high performance, and very flexible.



API Reference
---------------------

Compile Time Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`PJSIP <generated/pjsip/group/group__PJSIP__CONFIG>`
- :doc:`Error codes <generated/pjsip/group/group__PJSIP__CORE__ERRNO>`

Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Endpoint <generated/pjsip/group/group__PJSIP__ENDPT>`
- :doc:`Event <generated/pjsip/group/group__PJSIP__EVENT>`
- :doc:`Modules <generated/pjsip/group/group__PJSIP__MOD>`
- :doc:`Message Creation and Stateless Operations <generated/pjsip/group/group__PJSIP__ENDPT__STATELESS>`

Message Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Methods <generated/pjsip/group/group__PJSIP__MSG__METHOD>`
- :doc:`Header Fields <generated/pjsip/group/group__PJSIP__MSG__HDR>`
- :doc:`Request and Status Liine <generated/pjsip/group/group__PJSIP__MSG__LINE>`
- :doc:`Message Structure <generated/pjsip/group/group__PJSIP__MSG__MSG>`
- :doc:`Multipart Message Body <generated/pjsip/group/group__PJSIP__MULTIPART>`
- :doc:`The Parser <generated/pjsip/group/group__PJSIP__PARSER>`
- URI:

  - :doc:`Generic URI <generated/pjsip/group/group__PJSIP__URI__GENERIC>`
  - :doc:`SIP URI <generated/pjsip/group/group__PJSIP__SIP__URI>`
  - :doc:`tel URI <generated/pjsip/group/group__PJSIP__TEL__URI>`
  - :doc:`Other URI schemes <generated/pjsip/group/group__PJSIP__OTHER__URI>`
  - :doc:`URI Parameter Container<generated/pjsip/group/group__PJSIP__URI__PARAM>`
  
- :doc:`Media/MIME <generated/pjsip/group/group__PJSIP__MSG__MEDIA>`
- :doc:`Message Body <generated/pjsip/group/group__PJSIP__MSG__BODY>`


Transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Transport API <generated/pjsip/group/group__PJSIP__TRANSPORT>`
- :doc:`DNS SRV Resolution <generated/pjsip/group/group__PJSIP__RESOLVE>`
- :doc:`Loop <generated/pjsip/group/group__PJSIP__TRANSPORT__LOOP>`
- :doc:`TCP <generated/pjsip/group/group__PJSIP__TRANSPORT__TCP>`
- :doc:`TLS <generated/pjsip/group/group__PJSIP__TRANSPORT__TLS>`
- :doc:`UDP <generated/pjsip/group/group__PJSIP__TRANSPORT__UDP>`


Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Authentication <generated/pjsip/group/group__PJSIP__AUTH__API>`
- :doc:`Digest AKAv1 and AKAv2 <generated/pjsip/group/group__PJSIP__AUTH__AKA__API>`

Transaction Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Transaction <generated/pjsip/group/group__PJSIP__TRANSACT__TRANSACTION>`
- :doc:`Stateful Operations <generated/pjsip/group/group__PJSIP__TRANSACT__UTIL>`

Base UA/Common Dialog Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Dialog <generated/pjsip/group/group__PJSIP__DIALOG>`
- :doc:`UA Module <generated/pjsip/group/group__PJSUA__UA>`
- :doc:`Core Proxy Layer <generated/pjsip/group/group__PJSIP__PROXY__CORE>`

User Agent Layer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`INVITE Session <generated/pjsip/group/group__PJSIP__INV>`
- :doc:`100rel/PRACK - Reliability of Provisional Responses <generated/pjsip/group/group__PJSIP__100REL>`
- :doc:`Client Registration <generated/pjsip/group/group__PJSUA__REGC>`
- :doc:`SIP Replaces support (RFC 3891 - "Replaces" Header) <generated/pjsip/group/group__PJSIP__REPLACES>`
- :doc:`SIP Session Timers support (RFC 4028 - Session Timers in SIP) <generated/pjsip/group/group__PJSIP__TIMER>`
- :doc:`SIP REFER (RFC 3515) for Call Transfer etc. <generated/pjsip/group/group__PJSUA__XFER>`

Event and Presence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SIP Event Notification (RFC 3265) Module <generated/pjsip/group/group__PJSIP__EVENT__NOT>`
- :doc:`Additional Event Header Fields <generated/pjsip/group/group__PJSIP__EVENT__HDRS>`
- :doc:`Message Composition Indication (RFC 3994) <generated/pjsip/group/group__PJSIP__ISCOMPOSING>`
- :doc:`SIP Message Summary and Message Waiting Indication (RFC 3842) <generated/pjsip/group/group__mwi>`
- :doc:`PIDF/Presence Information Data Format (RFC 3863) <generated/pjsip/group/group__PJSIP__SIMPLE__PIDF>`
- :doc:`SIP Extension for Presence (RFC 3856) <generated/pjsip/group/group__PJSIP__SIMPLE__PRES>`
- :doc:`SIP Event State Publication (PUBLISH, RFC 3903) <generated/pjsip/group/group__PJSIP__SIMPLE__PUBLISH>`
- :doc:`RPID/Rich Presence Extensions to PIDF (RFC 4480) <generated/pjsip/group/group__PJSIP__SIMPLE__RPID>`
- :doc:`XPIDF/Presence Information Data Format <generated/pjsip/group/group__PJSIP__SIMPLE__XPIDF>`

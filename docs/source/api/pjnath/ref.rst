API Reference
-------------------

Basic Types and Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :doc:`Basic Initialization </api/generated/pjnath/group/group__PJNATH>`
- :doc:`Configurations </api/generated/pjnath/group/group__PJNATH__CONFIG>`
- :doc:`Error Codes </api/generated/pjnath/group/group__PJNATH__ERROR>`


.. _ice:

ICE and Trickle ICE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Interactive Connectivity Establishment (:rfc:`5245`)

- :doc:`Introduction </api/generated/pjnath/group/group__PJNATH__ICE>`
- :doc:`High-level ICE Transport </api/generated/pjnath/group/group__PJNATH__ICE__STREAM__TRANSPORT>`
- :doc:`Transport-independent ICE Session </api/generated/pjnath/group/group__PJNATH__ICE__SESSION>`
- TCP
-  Trickle ICE, see: https://github.com/pjsip/pjproject/pull/2588


STUN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _stun:

Session Traversal Utilities for NAT (:rfc:`5389`)

- :doc:`Introduction </api/generated/pjnath/group/group__PJNATH__STUN>`
- :doc:`High-level STUN Transport </api/generated/pjnath/group/group__PJNATH__STUN__SOCK>`
- :doc:`Transport-independent STUN Session </api/generated/pjnath/group/group__PJNATH__STUN__SESSION>`
- Basic Objects:

  - :doc:`STUN Authentication </api/generated/pjnath/group/group__PJNATH__STUN__AUTH>`
  - :doc:`STUN Config </api/generated/pjnath/group/group__PJNATH__STUN__CONFIG>`
  - :doc:`STUN Message and Parsing </api/generated/pjnath/group/group__PJNATH__STUN__MSG>`
  - :doc:`STUN Client Transaction </api/generated/pjnath/group/group__PJNATH__STUN__TRANSACTION>`


.. _turn:

TURN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Traversal Using Relays around NAT

- :doc:`Introduction </api/generated/pjnath/group/group__PJNATH__TURN>`
- :doc:`High-level UDP/TCP/TLS TURN Client Transport </api/generated/pjnath/group/group__PJNATH__TURN__SOCK>`
- :doc:`Transport-independent TURN Client Session </api/generated/pjnath/group/group__PJNATH__TURN__SESSION>`


.. _upnp:

uPnP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal Plug and Play support for SIP UDP and media UDP transports.

- See ticket :pr:`3184` for build and use instructions.
- :doc:`uPnP API reference </api/generated/pjnath/group/group__PJNATH__UPNP>`


NAT Type Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _nat_detect:

- :doc:`NAT Type Detection Tool </api/generated/pjnath/group/group__PJNATH__NAT__DETECT>`



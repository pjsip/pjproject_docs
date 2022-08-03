Overview
*******************************

PJSIP is a free and open source multimedia communication library written in C language
implementing standard based protocols such as SIP, SDP, RTP, STUN, TURN, and ICE. 
It combines signaling protocol (SIP) with rich multimedia framework and NAT traversal
functionality into high level API that is portable and suitable for almost any type of
systems ranging from desktops, embedded systems, to mobile handsets.

PJSIP is both compact and feature rich. It supports audio, video, presence, and instant
messaging, and has extensive documentation. PJSIP is very portable. On mobile devices,
it abstracts system dependent features and in many cases is able to utilize the native
multimedia capabilities of the device.

PJSIP has been developed by a small team working exclusively for the project since 2005,
with participation of hundreds of developers from around the world, and is routinely
tested at SIP Interoperability Event (`SIPit <https://www.sipit.net>`_) since 2007.

PJSIP development is hosted at https://github.com/pjsip/pjproject


Libraries Architecture
=========================================

PJSIP contains several libraries, which can be grouped into three main components:

 - SIP protocol stack, in PJSIP
 - Media stack, in PJMEDIA
 - NAT traversal stack, in PJNATH

There are also high level libraries that integrate the above components (PJSUA, for
SIP User Agent), as well as low level libraries that abstracts operating system 
differences.

To avoid naming confusion between PJSIP as organization name (as in 
`PJSIP.ORG <https://pjsip.org>`_) and PJSIP as libraries that provide SIP protocol
implementation  above, we also call this project **PJPROJECT**.

Below is architecture diagram of libraries in PJPROJECT. Click the link on the 
diagram to go to the documentation.

.. raw:: html
    :file: architecture.svg



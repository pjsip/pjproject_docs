Introduction
******************************
PJSUA2 is an object-oriented abstraction above PJSUA API. It provides high level 
API for constructing Session Initiation Protocol (SIP) multimedia user agent 
applications (a.k.a Voice over IP/VoIP softphones). It wraps together the signaling, 
media, and NAT traversal functionality into easy to use call control API, 
account management, buddy list management, presence, and instant messaging, along 
with multimedia features such as local audio andvideo conferencing, file streaming, 
local playback,  and voice recording, and powerful NAT traversal techniques 
utilizing STUN, TURN, ICE, and uPnP.

PJSUA2 is implemented on top of `PJSUA-LIB API </api/pjsua-lib/index.html>`_. 
The SIP and media features and object modelling follows what PJSUA-LIB provides 
(for example, we still have accounts, 
call, buddy, and so on), but the API to access them is different. These features 
will be described later in this chapter. PJSUA2 is a C++ library, which you can 
find under ``pjsip`` directory in the PJSIP distribution. The C++ library can be 
used by native C++ applications directly. But PJSUA2 is not just a C++ library. 
From the beginning, it has been designed to be accessible from high level 
non-native languages such as Java and Python. This is achieved by SWIG binding. 
And thanks to SWIG, binding to other languages can be added relatively easily in 
the future.

PJSUA2 API declaration can be found in ``pjsip/include/pjsua2`` while the source 
codes are located in ``pjsip/src/pjsua2``. It will be automatically built when 
you compile PJSIP.


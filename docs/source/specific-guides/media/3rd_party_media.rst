Integrating Third Party Media Stack into PJSUA-LIB
========================================================

Starting with PJSIP 2.0, support for integrating third party media stack into PJSUA-LIB was added. By following the steps below, application can use third party media stack to perform audio and video functionality while still making use of the full SIP, NAT, and security (including SRTP) features provided by PJSUA-LIB API.

By disabling PJMEDIA, the following features will not be available in PJSUA-LIB (unless the equivalent implementation is provided by the third party media library):

 - sound device management
 - echo cancellation
 - codecs
 - jitter buffer
 - RTP and RTCP
 - WAV playback and recording
 - conference bridge
 - DTMF with :rfc:`2833`
 - and so on, except explicitly mentioned below

The following features will still be available:

 - all SIP features, including SIP registration, etc.
 - SDP and SDP negotiation
 - NAT traversal features (including ICE)
 - security features including TLS and SRTP
 - media transports

Follow these steps to integrate third party media library with PJSUA-LIB:

 #. Declare this in :any:`config_site.h`:
    
    .. code-block:: c

       #define PJSUA_MEDIA_HAS_PJMEDIA    0
  
    to exclude PJMEDIA specific implementation from PJSUA-LIB library. Understandably you will loose all media features in PJSUA-LIB (this will be handled by your third party media stack).
 #. Also copy suggested settings from :source:`pjsip-apps/src/3rdparty_media_sample/config_site.h` into :any:`config_site.h`. These settings are mostly used to exclude unneeded media components from the link process.
 #. Build the libraries, but this time using 

    .. code-block:: c

       $ make lib
  
    instead of just ``make`` or ``make all``. This is because most samples will no longer build due to missing media in PJSUA-LIB, hence normal ``make`` will fail on these apps. The ``make lib`` command only builds the libraries and unit tests for the libraries.
 #. Go to directory :sourcedir:`pjsip-apps/src/3rdparty_media_sample`. This is a sample application with hook points to integrate   third party media library. Fill in the media implementation in the ``alt_pjsua_xxx.c`` files, following the "TODO" notes.   Run ``make`` to build the application. Once it's built, run ``alt_pjsua`` just as you run the usual ``pjsua`` application (it's essentially the same app!).


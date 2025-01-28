PJSIP for Android features
=======================================

PJSIP is a comprehensive, open source, portable SIP, media, and NAT traversal library/SDK to develop SIP
applications supporting voice/VoIP calls, video, secure communication using TLS and
secure RTP (SRTP), and NAT traversal resolution helper for Android, iOS/iPhone, Linux, Windows, MacOS,
embedded OSes, RTOSes, and other platforms.

This page presents the features of PJSIP for Android.

.. contents:: In this page:
   :depth: 2
   :local:


SIP features
-----------------------------------

All SIP features in :doc:`PJSIP SIP features datasheet </overview/features_sip>` are supported,
including but not limited to:

.. include:: ../../common/common_sip_features_overview.rst


Security features
-----------------------------------

The following SIP security and secure media features are supported and included in this tutorial:

- :doc:`/specific-guides/security/ssl`
- :doc:`/specific-guides/security/srtp`


NAT traversal features
-----------------------------------

The PJNATH Android NAT traversal stack supports most NAT traversal features in
:doc:`PJSIP NAT features datasheet </overview/features_nat>`, including but not limited to:

- :ref:`ice`
- :ref:`STUN <stun>`
- :ref:`TURN <turn>`
- :ref:`NAT type detection <nat_detect>`

By default the features above are included in the build (including in this tutorial), but may not be
enabled by the sample Android applications (this will be explained later in the sample application
documentation).

Below are currently not supported:

- :ref:`uPnP <upnp>`, unless you're able to build libupnp on Android.


Audio features
-----------------------------------

General audio features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All audio features in :doc:`PJSIP media features datasheet </overview/features_media>`
are supported (they are platform independent).

Audio devices, codecs, and video will be discussed separately below.


Android audio codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refer to :doc:`PJSIP codecs datasheet </overview/features_codec>` for list of all supported codecs.
PJSIP supports some of highly versatile audio codecs for Android, including:

- :ref:`Native Android AMR-NB/WB <amediacodec>` (included in this tutorial)
- :ref:`opus`
- :ref:`silk`


These codecs are supported and included in this tutorial:

- :ref:`g711`
- :ref:`g722`
- :ref:`gsm`
- :ref:`ilbc`
- :ref:`speex`

These codecs are supported for Android, but are not built by default nor included in this tutorial:

- :ref:`g7221`
- :ref:`l16`
- :ref:`bcg729`


Android audio devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following audio devices are supported:

- :ref:`oboe` (the one used in this tutorial)
- :ref:`jnisound`
- :ref:`opensl`


Android Video Features
-----------------------------------

General video features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Video call is supported by PJSIP SIP and media SDK for Android since version 2.4. General video features
as listed in :doc:`PJMEDIA video features </overview/features_video>` are supported and built by default
(they are platform independent), including but not limited to:

- :ref:`guide_vidconf` (CPU permitting!)
- :ref:`AVI streaming <avi_device>`
- :ref:`Sending/receiving missing video keyframe indication <vid_key>`
- :doc:`Video source duplicator </api/generated/pjmedia/group/group__PJMEDIA__VID__TEE>`

Android specific video codecs and devices are discussed in the next sections below.


Android video codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PJMEDIA Android video framework supports some of highly versatile video codecs, including:

- :ref:`native H264 AVC and VP8/VP9 codecs <amediacodec>` (included in this tutorial)
- :ref:`openh264`
- :ref:`libvpx`
- :ref:`ffmpeg`


Android video devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PJMEDIA Android video device implementation include the following video devices:

- :ref:`native capture <android_cam>`
- :ref:`native OpenGL ES 2.0 renderer <opengl>` (requires Android 2.2 (API level 8) or higher).
- :ref:`colorbar`
- :ref:`avi_device`


Sample applications
-----------------------------------
Yes, we include the batteries as well. The Android implementation comes with three sample
applications:

- :doc:`Android Java SIP voice and video client application <java-sip-client>`

  A very simple softphone demo but yet already packed with powerful features.

- :doc:`Android Kotlin SIP client application <kotlin-sip-client>`

  An even simpler sample app (about 500 lines of codes) supporting voice and video with AMR-WB and H.264 codecs.

- :doc:`Android CLI based remote controllable (telnet) SIP application <cli-sip-client>`

  Simple remote controllable app for rapid feature development and testing.


What's next
-----------------

Coming up, we will install the required libraries and tools to build our Android SIP VoIP and
video call client application.

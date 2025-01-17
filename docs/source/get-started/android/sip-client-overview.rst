Android SIP Client Development Overview
========================================

This section gives you a brief overview about the outcomes of this guide and the general tasks
to accomplish them.

.. contents:: In this page:
   :depth: 2
   :local:

..
   :backlinks: none


Objectives and general tasks
---------------------------------------

The general tasks (and also the objectives) of this guide are:

1. Install the required tools and library
2. Configure and build PJSIP for Android development
3. Build sample applications:

   * Android Java SIP client
   * Android Kotlin SIP client
   * Android JAVA CLI (telnet) SIP client

4. Demonstrate dialing and receiving voice and video SIP calls.


The following are the features of PJSIP, a comprehensive, open source SIP, media, and NAT Traversal
stack for Android.


SIP features
-----------------------------------

All SIP features in :doc:`PJSIP SIP features datasheet </overview/features_sip>` are supported.


Security features
-----------------------------------

The following SIP security and secure media features are supported:

- :doc:`SIP TLS </specific-guides/security/ssl>`
- :doc:`Secure RTP (SRTP) </specific-guides/security/srtp>`


NAT traversal features
-----------------------------------

The PJNATH Android NAT traversal library supports most NAT traversal features in
:doc:`PJSIP NAT features datasheet </overview/features_nat>`, including but not limited to:

-  :ref:`ice`
-  :ref:`STUN <stun>`
-  :ref:`TURN <turn>`
-  :ref:`NAT type detection <nat_detect>`

Below are currently not supported:

-  :ref:`uPnP <upnp>`, unless you're able to build libupnp on Android.


Audio features
-----------------------------------

General audio features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All audio features in :doc:`PJSIP media features datasheet </overview/features_media>`
are supported.

Audio devices, codecs, and video will be discussed separately below.


Android audio codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refer to :doc:`PJSIP codecs datasheet </overview/features_codec>` for list of all supported codecs.
PJSIP supports some of highly versatile audio codecs for Android, including:

- :ref:`Native Android AMR-NB/WB <amediacodec>`
- :ref:`opus`
- :ref:`silk`


Many other codecs are supported, including but not limited to:

- :ref:`g711`
- :ref:`g722`
- :ref:`g7221`
- :ref:`bcg729`
- :ref:`gsm`
- :ref:`ilbc`
- :ref:`l16`
- :ref:`speex`



Android audio devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following audio devices are supported:

- :ref:`oboe`
- :ref:`jnisound`
- :ref:`opensl`


Android Video Features
-----------------------------------

General video features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Video is supported by PJSIP SIP and media SDK for Android since version 2.4. General video features
as listed in :doc:`PJMEDIA video features </overview/features_video>` are supported, including but
not limited to:

- :ref:`guide_vidconf` (CPU permitting!)
- :ref:`AVI streaming <avi_device>`
- :ref:`Sending/receiving missing video keyframe indication <vid_key>`
- :doc:`Video source duplicator </api/generated/pjmedia/group/group__PJMEDIA__VID__TEE>`

Android specific video codecs and devices are discussed in the next sections below.


Android video codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The PJMEDIA Android video framework supports some of highly versatile video codecs, including:

- :ref:`native H264 AVC and VP8/VP9 codecs <amediacodec>`
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


Coming up
-----------------

Coming up, we will install the required libraries and tools to build our Android SIP VoIP and
video call client application.

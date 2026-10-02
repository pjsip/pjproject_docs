CMake Options
=======================================================================================

.. contents:: Table of Contents
    :depth: 2

Options are set with ``-D<option>=<value>`` when configuring. Their current
values, with help text, are shown by ``cmake -LAH -N <build-dir>``, and
``cmake-gui`` or ``ccmake`` edit them interactively. Option names are
case-sensitive.

In the tables below, **auto** means the option is ``ON`` by default, but is
switched off at configure time when its dependency is not found; configure
then prints a ``[!] ... was not found`` line. An option for a platform the
build is not targeting is always ``OFF``.


General
-------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Option
     - Default
     - Notes
   * - ``CMAKE_BUILD_TYPE``
     - none
     - ``Debug``, ``Release``, ``RelWithDebInfo`` or ``MinSizeRel``. Without
       one, a single-config build has no optimization flags. Ignored by
       multi-config generators (Visual Studio, Xcode).
   * - ``BUILD_SHARED_LIBS``
     - ``OFF``
     - Shared libraries instead of static ones.
   * - ``BUILD_TESTING``
     - ``ON``
     - Build the test applications and register them with CTest.
   * - ``CMAKE_INSTALL_PREFIX``
     - platform default
     - Install destination.
   * - ``PJ_SKIP_EXPERIMENTAL_NOTICE``
     - ``OFF``
     - Silence the experimental-status banner.


PJLIB
-----

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Option
     - Default
     - Notes
   * - ``PJLIB_WITH_SSL``
     - ``openssl``
     - ``openssl``, ``gnutls``, ``mbedtls``, ``darwin``, ``apple``,
       ``schannel``, or empty for no SSL. Falls back to no SSL when
       OpenSSL is not found. ``apple`` needs the ``select`` I/O queue;
       ``schannel`` needs MSVC. See :any:`/specific-guides/security/ssl`.
   * - ``PJLIB_WITH_IOQUEUE``
     - ``select``
     - ``select``, ``epoll`` (Linux), ``kqueue`` (macOS, BSD), ``iocp``
       (Windows).
   * - ``PJLIB_WITH_THREADS``
     - ``ON``
     - ``OFF`` builds without threads (``PJ_HAS_THREADS=0``); also turn off
       the components that need them, such as the WebRTC AEC.
   * - ``PJLIB_WITH_FLOATING_POINT``
     - ``ON``
     - Floating-point support.
   * - ``PJLIB_WITH_LIBUUID``
     - auto (Linux)
     - Use libuuid for GUID generation.


PJNATH
------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Option
     - Default
     - Notes
   * - ``PJNATH_WITH_UPNP``
     - auto
     - UPnP port mapping, with libupnp. See
       :any:`/specific-guides/network_nat/upnp`.


PJMEDIA
-------

General
^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Option
     - Default
     - Notes
   * - ``PJMEDIA_WITH_VIDEO``
     - ``ON``
     - Video support. ``OFF`` for an audio-only build.
   * - ``PJMEDIA_WITH_SRTP``
     - ``ON``
     - SRTP and DTLS-SRTP, with libsrtp.
   * - ``PJMEDIA_WITH_RESAMPLE``
     - ``libresample``
     - ``libresample`` (bundled), ``libsamplerate`` (system), ``speex``, or
       ``none``.
   * - ``PJMEDIA_WITH_SPEEX_AEC``
     - ``ON``
     - Speex echo canceller.
   * - ``PJMEDIA_WITH_WEBRTC_AEC``
     - ``ON``
     - WebRTC echo canceller. Not available on Apple platforms, MinGW or
       Cygwin.
   * - ``PJMEDIA_WITH_WEBRTC_AEC3``
     - ``ON``
     - WebRTC AEC3 echo canceller. Same availability as above.
   * - ``PJMEDIA_WITH_LIBYUV``
     - ``ON`` with video
     - libyuv for video format conversion.
   * - ``PJMEDIA_WITH_FFMPEG``
     - auto, with video
     - FFMPEG. Needs ``avutil``; ``PJMEDIA_WITH_FFMPEG_SWSCALE``,
       ``_AVCODEC``, ``_AVFORMAT`` and ``_AVDEVICE`` select the optional
       components, each auto.

Audio codecs
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Option
     - Default
     - Notes
   * - ``PJMEDIA_WITH_G711_CODEC``
     - ``ON``
     -
   * - ``PJMEDIA_WITH_L16_CODEC``
     - ``ON``
     -
   * - ``PJMEDIA_WITH_G722_CODEC``
     - ``ON``
     -
   * - ``PJMEDIA_WITH_G7221_CODEC``
     - ``ON``
     - Bundled.
   * - ``PJMEDIA_WITH_GSM_CODEC``
     - ``ON``
     - Bundled.
   * - ``PJMEDIA_WITH_ILBC_CODEC``
     - ``ON``
     - Bundled.
   * - ``PJMEDIA_WITH_SPEEX_CODEC``
     - ``ON``
     - Bundled.
   * - ``PJMEDIA_WITH_OPUS_CODEC``
     - auto
     - libopus.
   * - ``PJMEDIA_WITH_SILK_CODEC``
     - auto
     - SILK SDK.
   * - ``PJMEDIA_WITH_OPENCORE_AMRNB_CODEC``
     - auto
     - opencore-amrnb.
   * - ``PJMEDIA_WITH_OPENCORE_AMRWB_CODEC``
     - auto
     - opencore-amrwb and vo-amrwbenc.
   * - ``PJMEDIA_WITH_BCG729_CODEC``
     - auto
     - bcg729.
   * - ``PJMEDIA_WITH_LYRA_CODEC``
     - auto
     - Lyra.
   * - ``PJMEDIA_WITH_ANDROID_MEDIACODEC_CODEC``
     - auto (Android)
     - MediaCodec audio and video codecs.

Video codecs
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Option
     - Default
     - Notes
   * - ``PJMEDIA_WITH_OPEN_H264_CODEC``
     - auto, with video
     - OpenH264.
   * - ``PJMEDIA_WITH_VPX_CODEC``
     - auto, with video
     - libvpx, VP8 and VP9.
   * - ``PJMEDIA_WITH_VID_TOOLBOX_CODEC``
     - auto (Apple), with video
     - VideoToolbox H.264.

Audio devices
^^^^^^^^^^^^^

``PJMEDIA_WITH_AUDIODEV`` (``ON``) is the master switch; ``OFF`` builds no
audio device support at all.

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Option
     - Default
     - Platform
   * - ``PJMEDIA_WITH_AUDIODEV_ALSA``
     - auto
     - Linux
   * - ``PJMEDIA_WITH_AUDIODEV_COREAUDIO``
     - auto
     - macOS, iOS
   * - ``PJMEDIA_WITH_AUDIODEV_WMME``
     - ``ON``
     - Windows
   * - ``PJMEDIA_WITH_AUDIODEV_WASAPI``
     - ``OFF``
     - Windows desktop
   * - ``PJMEDIA_WITH_AUDIODEV_OBOE``
     - auto
     - Android; needs ``-DOboe_ROOT=``
   * - ``PJMEDIA_WITH_AUDIODEV_JNI``
     - ``ON``
     - Android

Video devices
^^^^^^^^^^^^^

``PJMEDIA_WITH_VIDEODEV`` (``ON`` with video) is the master switch.

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Option
     - Default
     - Notes
   * - ``PJMEDIA_WITH_VIDEODEV_SDL``
     - auto
     - SDL2 renderer, all platforms.
   * - ``PJMEDIA_WITH_VIDEODEV_AVI``
     - ``ON``
     - AVI file playback as a capture device.
   * - ``PJMEDIA_WITH_VIDEODEV_FFMPEG``
     - ``ON`` with FFMPEG ``avdevice``
     - FFMPEG capture.
   * - ``PJMEDIA_WITH_VIDEODEV_V4L2``
     - auto
     - Linux capture.
   * - ``PJMEDIA_WITH_VIDEODEV_DARWIN``
     - auto
     - macOS and iOS capture (AVFoundation).
   * - ``PJMEDIA_WITH_VIDEODEV_METAL``
     - ``OFF``
     - macOS and iOS renderer.
   * - ``PJMEDIA_WITH_VIDEODEV_QT``
     - ``OFF``
     - macOS renderer.
   * - ``PJMEDIA_WITH_VIDEODEV_OPENGL``
     - auto
     - OpenGL ES renderer, Android and iOS.
   * - ``PJMEDIA_WITH_VIDEODEV_ANDROID``
     - ``ON``
     - Android capture.
   * - ``PJMEDIA_WITH_VIDEODEV_DSHOW``
     - ``OFF``
     - Windows capture (DirectShow).


PJSIP
-----

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Option
     - Default
     - Notes
   * - ``PJSIP_WITH_TLS``
     - ``ON`` with SSL
     - SIP over TLS.
   * - ``PJSIP_WITH_DIGEST_AKA_AUTH``
     - ``OFF``
     - Digest AKAv1/AKAv2 authentication, with the bundled milenage.


Platform Integration
--------------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Option
     - Default
     - Notes
   * - ``PJ_BUILD_SWIG_JAVA``
     - ``OFF`` (Android)
     - Build the pjsua2 JNI bindings, ``libpjsua2.so`` and the Java
       sources. Needs SWIG 4.0+.
   * - ``PJ_IOS_SAMPLE_LIBS``
     - ``ON`` (iOS)
     - Copy the built libraries into the bundled iOS sample projects.
   * - ``PJ_IOS_SAMPLE_HEADERS``
     - ``ON`` (iOS)
     - Also copy the generated headers into the source tree, where the
       sample projects look for them.


Third-party Libraries
---------------------

The libraries in :source:`third_party/` are built from source
(``bundled``). Those with a ``system`` provider can use an installed copy
instead, found with ``find_package()``.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Option
     - Values
     - Library
   * - ``PJ_DEP_SRTP``
     - ``bundled``, ``system``
     - libsrtp. The bundled copy uses OpenSSL's AES-GCM when OpenSSL is
       found (``SRTP_WITH_OPENSSL``, ``ON``).
   * - ``PJ_DEP_SPEEX``
     - ``bundled``, ``system``
     - Speex codec. With ``system``, the Speex AEC and resampler use
       libspeexdsp.
   * - ``PJ_DEP_GSM``
     - ``bundled``, ``system``
     - GSM 06.10.
   * - ``PJ_DEP_G7221``
     - ``bundled``, ``system``
     - G.722.1.
   * - ``PJ_DEP_YUV``
     - ``bundled``, ``system``
     - libyuv.
   * - ``PJ_DEP_RESAMPLE``
     - ``bundled``, ``system``
     - libresample.
   * - ``PJ_DEP_ILBC``
     - ``bundled``
     - iLBC.
   * - ``PJ_DEP_WEBRTC``, ``PJ_DEP_WEBRTC_AEC3``
     - ``bundled``
     - WebRTC AEC and AEC3. Not available on Apple platforms, MinGW or
       Cygwin.

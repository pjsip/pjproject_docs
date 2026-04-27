Video User's Guide
========================

Video is available on PJSIP version 2.0 and later (2.3 support video for
iOS, 2.4 support video for Android). This document describes how to use
the video feature, mostly with PJSUA-LIB.

.. tip::

   For PJSUA2 video tutorial, please see :any:`/pjsua2/using/media_video`.

.. contents:: Table of Contents
   :depth: 4




Building with Video Support
---------------------------

Follow :any:`get_started_toc` for your platform
on building pjsip with video support.

.. _vid_ug_samples:

Sample Applications with Video
----------------------------------------------

PJPROJECT ships several sample applications that exercise the video
feature. They are the recommended starting points for learning the API
and for verifying that a video build works end-to-end.

- **Desktop (Windows, macOS, Linux)** — :sourcedir:`pjsip-apps/src/pjsua` is
  the cross-platform PJSUA-LIB (C) console app. It is the most
  thoroughly exercised sample and effectively serves as the reference
  full-featured SIP video client: interactive command-line UI, video
  calls and preview, codec selection and parameter tuning, video
  conference, AVI playback, key-frame request, etc. Use this when you
  need to verify that a video build works or when you want a feature to
  copy from.

- **iOS, PJSUA-LIB (C / Objective-C)** — :sourcedir:`pjsip-apps/src/pjsua/ios`
  contains *ipjsua*, the maintained iOS reference. It is a usable SIP
  video client built directly on the C API, and the most complete iOS
  sample. See :doc:`/get-started/ios/build_instructions` for build
  steps.

- **iOS, PJSUA-LIB with Swift** — :sourcedir:`pjsip-apps/src/pjsua/ios-swift`
  contains *ipjsua-swift*, a smaller demo that shows how to call the
  PJSUA-LIB C API from Swift via a bridging header. Useful as a starting
  template; not as feature-complete as *ipjsua*.

- **iOS, PJSUA2 with Swift (C++)** — :sourcedir:`pjsip-apps/src/pjsua2/ios-swift-pjsua2`
  is a proof-of-concept showing how to consume PJSUA2 (C++) from Swift
  via an Objective-C++ bridge. Scope is narrow — it demonstrates the
  binding pattern rather than acting as a full client.

- **Android, PJSUA2 (Java)** — :sourcedir:`pjsip-apps/src/swig/java/android/app`
  is a working Android sample that supports TLS, AMR-NB/WB audio, and
  H.264 video over PJSUA2. It also demonstrates handling device
  orientation changes and preserving the video aspect ratio in the
  renderer view. The UI is intentionally minimal so the PJSUA2 usage
  stands out. See :doc:`/get-started/android/java-sip-client`.

- **Android, PJSUA2 (Kotlin)** — :sourcedir:`pjsip-apps/src/swig/java/android/app-kotlin`
  is a Kotlin port of the Java sample, with most settings hard-coded.
  It is primarily a proof-of-concept for using PJSUA2 from Kotlin
  rather than a feature showcase. See
  :doc:`/get-started/android/kotlin-sip-client`.

.. note::

   A Qt-based desktop GUI sample, *vidgui*, also exists at
   :sourcedir:`pjsip-apps/src/vidgui`. It is provided as an example of
   embedding video into a GUI toolkit but is rarely tested and may not
   build or run on current toolchains. Prefer one of the samples above.


Topics
-------

The user's guide is organized into the following topics:

.. toctree::
   :maxdepth: 1

   users_guide/call_video
   users_guide/codec_params
   users_guide/orientation
   users_guide/conference


Additional Info
-------------------

Using OpenGL with SDL
~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP supports OpenGL video rendering with SDL. Follow these steps to enable and use the OpenGL backend.

1. Install OpenGL development libraries for your system. The instructions vary, and some platforms may have OpenGL development libraries installed by default.

   - For Ubuntu 12.04, you can run the following:

     .. code-block:: shell

        $ sudo apt-get install freeglut3 freeglut3-dev
        $ sudo apt-get install binutils-gold

   - Alternatively, you can use libgl-dev which is smaller. Please note that since Ubuntu 14.04 LTS, libsdl2-dev is available which comes with libgl-dev automatically, so it might not be needed anymore.

      .. code-block:: shell

         $ sudo apt-get install libgl-dev

2. Enable SDL OpenGL support in PJSIP, by declaring this in your :any:`config_site.h`:

   .. code-block:: c

      #define PJMEDIA_VIDEO_DEV_SDL_HAS_OPENGL    1

3. If you're not using Visual Studio, add OpenGL library in your application's input library list. If you're using GNU tools, you can add this in **user.mak** file in root PJSIP directory:


   .. code-block::

      export LDFLAGS += -lGL

4. Rebuild PJSIP
5. Now **"SDL openGL renderer"** device should show up in video device list. Simply just use this device.


Mac OS X Video Threading Issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On Mac OS X, our video implementation uses Cocoa frameworks, which require handling user events and drawing window content to be done in the main thread. Hence, to avoid deadlock, application should not call any PJSIP API which can potentially block from the main thread. We provide an API :cpp:any:`pj_run_app()` to simplify creating a GUI app on Mac OS X, please refer to *pjsua* app located in :sourcedir:`pjsip-apps/src/pjsua` for sample usage. Basically, :cpp:any:`pj_run_app()` will setup an event loop management in the main thread and create a multi-threading environment, allowing PJSIP to be called from another thread.

.. code-block:: c

   int main_func(int argc, char *argv[])
   {
       // This is your real main function
   }

   int main(int argc, char *argv[])
   {
       // pj_run_app() will call your main function from another thread (if necessary)
       // this will free the main thread to handle GUI events and drawing
       return pj_run_app(&main_func, argc, argv, 0);
   }


.. _vid_key:

Video key frame transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Sending/receiving missing video keyframe indication using the following techniques:

  * SIP INFO with XML Schema for Media Control (:rfc:`5168#section-7.1`), using:

     - Full Intra Request (:rfc:`5104#section-3.5.1`)
     - Picture Loss Indication feedback (:rfc:`4585#section-6.3.1`)
     - See issue :issue:`1234` for more info

  * RTCP Picture Loss Indication feedback (:rfc:`4585#section-6.3.1`):

     - See issue :issue:`1437` for more info

- Key frame at the start of the call (see issue :issue:`1910`)
- See also RTCP key frame request


.. _vid_ug_api_ref:

Video API Reference (pjsua-lib)
------------------------------------------

This section explains and lists the Video API as it was available when
this document is written. For a richer and more up to date list, please
see :doc:`Video API reference </api/generated/pjsip/group/group__PJSUA__LIB__VIDEO>`

The Video API is classified into the following categories.

Device enumeration API
~~~~~~~~~~~~~~~~~~~~~~

- :cpp:any:`pjsua_vid_dev_count()`
- :cpp:any:`pjsua_vid_dev_get_info()`
- :cpp:any:`pjsua_vid_enum_devs()`

In addition, the :any:`PJMEDIA videodev </api/generated/pjmedia/group/group__video__device__reference>`
also provides this API to detect change in device availability:

- - :cpp:any:`pjmedia_vid_dev_refresh()`

Video preview API
~~~~~~~~~~~~~~~~~

The video preview API can be used to show the output of capture device
to a video window:

- struct :cpp:any:`pjsua_vid_preview_param`
- :cpp:any:`pjsua_vid_preview_start()`
- :cpp:any:`pjsua_vid_preview_get_win()`
- :cpp:any:`pjsua_vid_preview_stop()`

Video Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video is enabled/disabled on :cpp:any:`pjsua_call_setting`.

Video settings are mostly configured on the :cpp:any:`pjsua_acc_config` with the
following fields:

- :cpp:any:`pjsua_acc_config::vid_in_auto_show`
- :cpp:any:`pjsua_acc_config::vid_out_auto_transmit`
- :cpp:any:`pjsua_acc_config::vid_cap_dev`
- :cpp:any:`pjsua_acc_config::vid_rend_dev`


.. _vid_ug_vcm:

Video Call Manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default video behavior for a call is controlled by the account
settings above. On top of that, the application can manipulate video of
an already-going call by using :cpp:any:`pjsua_call_set_vid_strm()` API.

Use :cpp:any:`pjsua_call_get_vid_stream_idx()` to get the media stream index of
the default video stream in the call.


Video Call Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video media information are available in :cpp:any:`pjsua_call_info`.


Video Call Stream Information and Statistic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the following API to query call's stream information and statistic.


- :cpp:any:`pjsua_call_get_stream_info()`
- :cpp:any:`pjsua_call_get_stream_stat()`
- :cpp:any:`pjsua_call_get_med_transport_info()`

.. note::

   The :cpp:any:`pjsua_call_get_media_session()` has been deprecated since its use is unsafe.


Video Window API
~~~~~~~~~~~~~~~~~~~~~~~~

A video window is a rectangular area in your monitor to display video
content. The video content may come from remote stream, local camera (in
case of preview), AVI playback, or any other video playback. Application
mostly will be interested in the native handle of the video window so
that it can embed it in its application window, however we also provide
simple and commonly used API for manipulating the window.

See:

- :cpp:any:`pjsua_vid_enum_wins()`
- :cpp:any:`pjsua_vid_win_get_info()`
- :cpp:any:`pjsua_vid_win_set_show()`
- :cpp:any:`pjsua_vid_win_set_pos()`
- :cpp:any:`pjsua_vid_win_set_size()`


Video Codec API
~~~~~~~~~~~~~~~~~~~~~~~

API for managing video codecs:

- :cpp:any:`pjsua_vid_enum_codecs()`
- :cpp:any:`pjsua_vid_codec_set_priority()`
- :cpp:any:`pjsua_vid_codec_get_param()`
- :cpp:any:`pjsua_vid_codec_set_param()`

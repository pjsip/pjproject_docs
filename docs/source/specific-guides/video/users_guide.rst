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
   users_guide/av_sync


Additional Info
-------------------

Using OpenGL with SDL
~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP supports an OpenGL-backed renderer on top of SDL. To enable it:

1. Install the OpenGL development headers and the SDL2 development
   package for your system. On Debian/Ubuntu (recent enough to ship
   ``libsdl2-dev``):

   .. code-block:: shell

      $ sudo apt-get install libgl-dev libsdl2-dev

   ``libsdl2-dev`` already pulls in OpenGL on most distributions, so
   the ``libgl-dev`` line is usually optional. Other platforms
   typically install OpenGL via the system SDK and SDL2 from
   `libsdl.org <https://www.libsdl.org/>`__.

2. Enable SDL OpenGL support in PJSIP by declaring this in your
   :any:`config_site.h`:

   .. code-block:: c

      #define PJMEDIA_VIDEO_DEV_SDL_HAS_OPENGL    1

3. Link the OpenGL library into your application. With the GNU build
   system, add to ``user.mak`` in the root PJSIP directory:

   .. code-block::

      export LDFLAGS += -lGL

4. Rebuild PJSIP. The **"SDL OpenGL renderer"** device will then show
   up in the video device list — just use it as the renderer.


Mac OS X Video Threading Issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Mac OS X, the video implementation uses Cocoa frameworks, which
require user-event handling and window drawing to happen on the main
thread. To avoid deadlock, the application **must not** call any
potentially-blocking PJSIP API from the main thread.

PJLIB provides :cpp:any:`pj_run_app()` as a convenience: it sets up an
event-loop manager in the main thread and creates a worker thread for
your real ``main_func``, so PJSIP calls can run from the worker
without blocking the GUI. The pjsua sample app at
:sourcedir:`pjsip-apps/src/pjsua` uses this pattern.

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

PJSIP supports both ends of video keyframe-request signalling so that
a peer that loses the decoder state can ask the sender for an IDR
frame.

- **Outgoing keyframe request** (we lost decode state and need a
  fresh IDR from the peer). Two transports:

  - **SIP INFO with XML Schema for Media Control**
    (:rfc:`5168#section-7.1`), carrying either Full Intra Request
    (:rfc:`5104#section-3.5.1`) or Picture Loss Indication
    (:rfc:`4585#section-6.3.1`). See ticket :issue:`1234` for the
    integration history.
  - **RTCP Picture Loss Indication** (:rfc:`4585#section-6.3.1`).
    See ticket :issue:`1437`.

  Which transports are allowed for a given call is controlled by
  :cpp:any:`pjsua_call_setting::req_keyframe_method` (a bitmask of
  :cpp:any:`pjsua_vid_req_keyframe_method`). The default is
  ``PJSUA_VID_REQ_KEYFRAME_SIP_INFO | PJSUA_VID_REQ_KEYFRAME_RTCP_PLI``.

- **Incoming keyframe request** — when the peer asks us via SIP INFO
  or RTCP PLI/FIR, the encoder is told to emit a keyframe on the next
  frame. Applications can also force an outgoing keyframe explicitly
  via the :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME
  <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>` stream
  operation passed to :cpp:any:`pjsua_call_set_vid_strm()`.

- **Keyframe at the start of a stream** is configurable via
  :cpp:any:`pjsua_acc_config::vid_stream_sk_cfg` (a
  :cpp:any:`pjmedia_vid_stream_sk_config`) — count and interval of
  keyframes the encoder sends right after the stream is created. See
  ticket :issue:`1910` for the rationale.

The associated media events
(:cpp:any:`PJMEDIA_EVENT_KEYFRAME_FOUND
<pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_FOUND>` and
:cpp:any:`PJMEDIA_EVENT_KEYFRAME_MISSING
<pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_MISSING>`) are listed in
the :doc:`Media events
</specific-guides/video/components>` section of the
Video Components and Backends page.


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
- :cpp:any:`pjsua_vid_dev_set_setting()` /
  :cpp:any:`pjsua_vid_dev_get_setting()`

In addition, the :any:`PJMEDIA videodev </api/generated/pjmedia/group/group__video__device__reference>`
provides this API to detect change in device availability:

- :cpp:any:`pjmedia_vid_dev_refresh()`

Video preview API
~~~~~~~~~~~~~~~~~

The video preview API can be used to show the output of a capture
device in a video window:

- struct :cpp:any:`pjsua_vid_preview_param`
- :cpp:any:`pjsua_vid_preview_start()`
- :cpp:any:`pjsua_vid_preview_stop()`
- :cpp:any:`pjsua_vid_preview_get_win()`
- :cpp:any:`pjsua_vid_preview_get_vid_conf_port()`
- :cpp:any:`pjsua_vid_preview_has_native()`

Video Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video is enabled/disabled per call on :cpp:any:`pjsua_call_setting`:

- :cpp:any:`pjsua_call_setting::vid_cnt`
- :cpp:any:`pjsua_call_setting::req_keyframe_method`
- :cpp:any:`pjsua_call_setting::media_dir` (gated by
  :cpp:any:`PJSUA_CALL_SET_MEDIA_DIR`)
- :cpp:any:`PJSUA_CALL_NO_MEDIA_SYNC` flag — see
  :doc:`users_guide/av_sync`

Per-account video settings live on :cpp:any:`pjsua_acc_config`:

- :cpp:any:`pjsua_acc_config::vid_in_auto_show`
- :cpp:any:`pjsua_acc_config::vid_out_auto_transmit`
- :cpp:any:`pjsua_acc_config::vid_cap_dev`
- :cpp:any:`pjsua_acc_config::vid_rend_dev`
- :cpp:any:`pjsua_acc_config::vid_wnd_flags`
- :cpp:any:`pjsua_acc_config::vid_stream_rc_cfg` — encoder-side rate
  control (see :doc:`users_guide/codec_params`)
- :cpp:any:`pjsua_acc_config::vid_stream_sk_cfg` — start-of-stream
  keyframe count/interval


.. _vid_ug_vcm:

Video Call Manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default video behavior for a call is controlled by the account
settings above. On top of that, the application can manipulate the
video of an already-going call:

- :cpp:any:`pjsua_call_set_vid_strm()` — operates on
  :cpp:any:`pjsua_call_vid_strm_op` (ADD, REMOVE, CHANGE_DIR,
  CHANGE_CAP_DEV, START_TRANSMIT, STOP_TRANSMIT, SEND_KEYFRAME)
- :cpp:any:`pjsua_call_get_vid_stream_idx()` — get the default video
  stream's media index
- :cpp:any:`pjsua_call_reinvite2()` /
  :cpp:any:`pjsua_call_update2()` — re-INVITE / UPDATE with a new
  :cpp:any:`pjsua_call_setting`


Video Call Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video media information lives on :cpp:any:`pjsua_call_info` (see
``ci.media[i].stream.vid``: window ID, encoding/decoding bridge slot
IDs, and capture device).


Video Call Stream Information and Statistic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following API to query a call's stream information and
statistics:

- :cpp:any:`pjsua_call_get_stream_info()`
- :cpp:any:`pjsua_call_get_stream_stat()`
- :cpp:any:`pjsua_call_get_med_transport_info()`


Video Window API
~~~~~~~~~~~~~~~~~~~~~~~~

A video window is a rectangular area on screen that displays video
content. The content may come from a remote stream, a local camera
preview, AVI playback, or any other video playback. Most applications
are interested in the underlying native handle so they can embed the
window in their own GUI; PJSUA-LIB also provides a small set of
manipulation APIs for non-native windows. See
:any:`vid_ug_wvw` for the details.

- :cpp:any:`pjsua_call_get_vid_win()` — convenience to get a call's
  incoming-video window
- :cpp:any:`pjsua_vid_enum_wins()`
- :cpp:any:`pjsua_vid_win_get_info()`
- :cpp:any:`pjsua_vid_win_set_show()`
- :cpp:any:`pjsua_vid_win_set_pos()`
- :cpp:any:`pjsua_vid_win_set_size()`
- :cpp:any:`pjsua_vid_win_rotate()`
- :cpp:any:`pjsua_vid_win_set_fullscreen()` (SDL only)
- :cpp:any:`pjsua_vid_win_set_win()` (Android only)


Video Conference API
~~~~~~~~~~~~~~~~~~~~~~~~

The video conference bridge moves frames between calls, capture
devices, renderers, and arbitrary :cpp:any:`pjmedia_port` objects. See
:doc:`users_guide/conference` for the model and routing patterns.

- :cpp:any:`pjsua_call_get_vid_conf_port()`
- :cpp:any:`pjsua_vid_preview_get_vid_conf_port()`
- :cpp:any:`pjsua_vid_conf_get_active_ports()`
- :cpp:any:`pjsua_vid_conf_enum_ports()`
- :cpp:any:`pjsua_vid_conf_get_port_info()`
- :cpp:any:`pjsua_vid_conf_add_port()`
- :cpp:any:`pjsua_vid_conf_remove_port()`
- :cpp:any:`pjsua_vid_conf_connect()`
- :cpp:any:`pjsua_vid_conf_disconnect()`
- :cpp:any:`pjsua_vid_conf_update_port()`
- :cpp:any:`pjsua_callback::on_vid_conf_op_completed`


Video Codec API
~~~~~~~~~~~~~~~~~~~~~~~

API for managing video codecs:

- :cpp:any:`pjsua_vid_enum_codecs()`
- :cpp:any:`pjsua_vid_codec_set_priority()`
- :cpp:any:`pjsua_vid_codec_get_param()`
- :cpp:any:`pjsua_vid_codec_set_param()`

Video Components and Backends
================================

To enable end-to-end video in PJSIP, four pluggable components must be present
in the build:

#. **Capture device** — sources raw frames from a camera (or a virtual
   source such as an AVI file).
#. **Renderer device** — displays decoded frames on screen.
#. **Video codec** — encodes/decodes for transmission over RTP.
#. **Format converter** — performs colour-space conversion and scaling
   between formats produced by capture devices, expected by codecs, and
   accepted by renderers.

In addition, several pieces of *glue* are always built-in and require no
backend choice:

- ``pjmedia_vid_port`` — connects a video device to a media port.
- ``pjmedia_vid_conf`` — the :ref:`video conference bridge <guide_vidconf>`
  that mixes/routes multiple video sources, and the routing fabric that
  PJSUA-LIB uses to wire capture, codec, and renderer slots together.
- ``pjmedia_event`` — media event framework. Applications subscribe to it to
  receive video notifications such as format/resolution change, window
  resize/close, keyframe found/missing, capture orientation change,
  incoming RTCP feedback, and video device errors. See
  :ref:`Media events <video_media_events>` below.
- ``pjmedia_av_sync`` — inter-media synchronizer. Keeps audio and video in
  lipsync within a session by comparing NTP/RTP timestamps from RTCP SR
  reports and asking lagging or leading streams to adjust their delay.
- RTP packetizers for H.263, H.264, and VPX (VP8/VP9).

Each of the four pluggable components is described below, with the available
backends, their platform support, and the build flags that control them.

In the tables, ✓ means the backend is available on that platform,
✗ means it is not, and a backend in **bold** is the default on that
platform when video is enabled.

.. note::

   Availability also depends on whether the relevant third-party SDK
   (e.g. SDL, FFmpeg, OpenH264, libvpx) is installed and detected by the
   build system. See the build instructions linked at the end of this page.


Capture devices
---------------------

+----------------------------------------+---------+--------+--------+--------+----------+
| Backend                                | Windows | macOS  | Linux  | iOS    | Android  |
+========================================+=========+========+========+========+==========+
| :ref:`AVFoundation <avfoundation>`     | ✗       | **✓**  | ✗      | **✓**  | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`Android Camera2 <android_cam>`   | ✗       | ✗      | ✗      | ✗      | **✓**    |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`DirectShow <dshow>`              | **✓**   | ✗      | ✗      | ✗      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`Video4Linux2 <video4linux>`      | ✗       | ✗      | **✓**  | ✗      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`FFmpeg <ffmpeg_capture>`         | ✓       | ✓      | ✓      | ✗      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`AVI virtual device <avi_device>` | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`Colorbar virtual <colorbar>`     | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+

The AVI and Colorbar virtual devices are bundled and enabled by default; they
are useful for testing without a real camera.

Build flags:

- **CMake**: ``PJMEDIA_WITH_VIDEODEV_DSHOW``, ``PJMEDIA_WITH_VIDEODEV_V4L2``,
  ``PJMEDIA_WITH_VIDEODEV_FFMPEG``, ``PJMEDIA_WITH_VIDEODEV_AVI``.
  AVFoundation (Apple) and Android Camera2 are auto-enabled by platform.
- **GNU autoconf**: ``--disable-v4l2`` to drop V4L2; FFmpeg capture rides on
  FFmpeg detection (see ``--with-ffmpeg``); DirectShow on Mingw is enabled
  with ``--enable-video=yes``. AVFoundation and Android Camera2 are
  auto-enabled when building for Apple/Android targets.
- **Visual Studio**: set the corresponding macros in ``config_site.h``,
  e.g. ``PJMEDIA_VIDEO_DEV_HAS_DSHOW=1``.


Renderer devices
---------------------

+----------------------------------------+---------+--------+--------+--------+----------+
| Backend                                | Windows | macOS  | Linux  | iOS    | Android  |
+========================================+=========+========+========+========+==========+
| :ref:`OpenGL / OpenGL ES <opengl>`     | ✓       | ✓      | ✓      | **✓**  | **✓**    |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`Metal <metal>`                   | ✗       | ✓      | ✗      | ✓      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`SDL <sdl>`                       | **✓**   | **✓**  | **✓**  | ✗      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`UIView (iOS) <avfoundation>`     | ✗       | ✗      | ✗      | ✓      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+

An additional renderer-side option exists at the *port* level (not as a
registered video device), available on every platform when video is
enabled:

- **AVI writer** (``pjmedia_avi_writer_create_streams``) — writes the
  incoming video (and optionally audio) frames to an AVI file. Useful for
  recording a call or a local preview to disk.

Build flags:

- **CMake**: ``PJMEDIA_WITH_VIDEODEV_OPENGL``, ``PJMEDIA_WITH_VIDEODEV_SDL``,
  ``PJMEDIA_WITH_VIDEODEV_METAL``.
- **GNU autoconf**: SDL is auto-detected (override with ``--with-sdl=DIR``,
  disable with ``--disable-sdl``). OpenGL/OpenGL ES, Metal, and UIView are
  auto-enabled for Apple/Android targets when their frameworks are
  detected.
- **Visual Studio**: set ``PJMEDIA_VIDEO_DEV_HAS_OPENGL=1`` /
  ``PJMEDIA_VIDEO_DEV_HAS_SDL=1`` in ``config_site.h``.


Video codecs
---------------------

+----------------------------------------+---------+--------+--------+--------+----------+
| Backend                                | Windows | macOS  | Linux  | iOS    | Android  |
+========================================+=========+========+========+========+==========+
| :ref:`OpenH264 <openh264>` (H.264)     | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`libvpx <libvpx>` (VP8, VP9)      | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`FFmpeg <ffmpeg>` (H.261/263/263P,|         |        |        |        |          |
| H.264, MJPEG, VP8, VP9)                | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`Android MediaCodec <amediacodec>`|         |        |        |        |          |
| (H.264, VP8, VP9 — native/HW)          | ✗       | ✗      | ✗      | ✗      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+
| :ref:`VideoToolbox <videotoolbox>`     |         |        |        |        |          |
| (H.264 — native/HW)                    | ✗       | ✓      | ✗      | ✓      | ✗        |
+----------------------------------------+---------+--------+--------+--------+----------+

There is no built-in default video codec; at least one of the above must be
present (and detected) for video calls to negotiate a codec.

Build flags:

- **CMake**: ``PJMEDIA_WITH_OPEN_H264_CODEC``, ``PJMEDIA_WITH_VPX_CODEC``,
  ``PJMEDIA_WITH_FFMPEG``, ``PJMEDIA_WITH_ANDROID_MEDIACODEC_CODEC``.
- **GNU autoconf**: ``--with-openh264=DIR`` / ``--disable-openh264``,
  ``--with-vpx=DIR`` / ``--disable-vpx``, ``--with-ffmpeg`` /
  ``--disable-ffmpeg``. VideoToolbox and Android MediaCodec are
  auto-enabled when building for Apple/Android targets.
- **Visual Studio**: set ``PJMEDIA_HAS_OPENH264_CODEC``,
  ``PJMEDIA_HAS_VPX_CODEC``, or ``PJMEDIA_HAS_FFMPEG`` in ``config_site.h``,
  and link the matching libraries.


.. _guide_libyuv:

Format converter
---------------------

The format converter handles colour-space conversion (e.g. NV12 → I420) and
scaling between the format produced by the capture device, the format
expected by the codec, and the format accepted by the renderer.

Two backends are available:

+----------------------------------------+---------+--------+--------+--------+----------+
| Backend                                | Windows | macOS  | Linux  | iOS    | Android  |
+========================================+=========+========+========+========+==========+
| **libyuv** (bundled, default)          | **✓**   | **✓**  | **✓**  | **✓**  | **✓**    |
+----------------------------------------+---------+--------+--------+--------+----------+
| **libswscale** (from FFmpeg)           | ✓       | ✓      | ✓      | ✓      | ✓        |
+----------------------------------------+---------+--------+--------+--------+----------+

libyuv is shipped with PJPROJECT in ``third_party/yuv`` and is built and
enabled by default on every platform when video is enabled. libswscale is
registered in addition to libyuv when FFmpeg is enabled, and it acts as a
fallback for format/size combinations that libyuv does not support.

Build flags:

- **CMake**: ``PJMEDIA_WITH_LIBYUV`` (default ``ON``);
  ``PJMEDIA_WITH_FFMPEG_SWSCALE`` (rides on ``PJMEDIA_WITH_FFMPEG``).
- **GNU autoconf**: ``--disable-libyuv`` to drop libyuv;
  ``--with-external-libyuv`` to use a system-installed libyuv instead of
  the bundled one. libswscale rides on FFmpeg detection.
- **Visual Studio**: ``PJMEDIA_HAS_LIBYUV`` is set automatically when the
  bundled libyuv project is included; ``PJMEDIA_HAS_LIBSWSCALE`` rides on
  ``PJMEDIA_HAS_FFMPEG``.


.. _video_media_events:

Media events
---------------------

PJMEDIA emits asynchronous events through ``pjmedia_event`` (see
``pjmedia/event.h``). A video application typically needs to subscribe and
handle the following:

- ``PJMEDIA_EVENT_FMT_CHANGED`` — the negotiated stream format has changed
  (commonly a resolution change after re-INVITE or a peer-side codec
  reconfiguration). The application must reconfigure the renderer to the
  new size; otherwise the output will be wrong or blank.
- ``PJMEDIA_EVENT_KEYFRAME_FOUND`` /
  ``PJMEDIA_EVENT_KEYFRAME_MISSING`` — a keyframe was decoded, or the
  decoder cannot proceed because a keyframe is missing. Apps may use
  these to update UI state or to trigger an explicit keyframe request to
  the peer (FIR/PLI).
- ``PJMEDIA_EVENT_ORIENT_CHANGED`` — the capture device's physical
  orientation changed. The app should signal the new orientation to the
  remote peer; the capture device handles its own rotation locally.
- ``PJMEDIA_EVENT_WND_CLOSING`` / ``PJMEDIA_EVENT_WND_CLOSED`` /
  ``PJMEDIA_EVENT_WND_RESIZED`` — the renderer's window was closed or
  resized by the user. Apps typically tear down or reconfigure the call's
  video on these.
- ``PJMEDIA_EVENT_MOUSE_BTN_DOWN`` — the user clicked inside the video
  window. Available where the renderer surfaces it (e.g. SDL).
- ``PJMEDIA_EVENT_RX_RTCP_FB`` — incoming RTCP feedback (e.g. PLI/FIR) was
  received. Apps that drive their own keyframe-on-demand logic can hook
  this.
- ``PJMEDIA_EVENT_VID_DEV_ERROR`` — a video device stopped because of an
  error (e.g. camera unplugged, permission revoked). The app should
  surface the error and recover.


Where to look next
---------------------

- :doc:`CMake build instructions </get-started/cmake/build_instructions>`
- :doc:`POSIX (Linux/macOS) build instructions </get-started/posix/build_instructions>`
- :doc:`Windows / Visual Studio build instructions </get-started/windows/build_instructions>`
- :ref:`Adding FFmpeg support <guide_ffmpeg>`
- :ref:`Adding SDL support <guide_sdl>`
- :ref:`Adding Video4Linux support <guide_video4linux>`

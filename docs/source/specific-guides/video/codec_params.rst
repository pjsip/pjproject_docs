Modifying Video Codec Parameters
=================================

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

Video codec parameters are exposed by :cpp:any:`pj::VidCodecParam`,
which carries separate settings for the encoding and decoding
directions. Read with :cpp:func:`pj::Endpoint::getVideoCodecParam()`,
modify, and write back with
:cpp:func:`pj::Endpoint::setVideoCodecParam()`.

.. code-block:: c++

   VidCodecParam param = Endpoint::instance().getVideoCodecParam("H264");

   // Modify param here
   ...

   Endpoint::instance().setVideoCodecParam("H264", param);

The relevant ``VidCodecParam`` fields used below are
:cpp:any:`pj::VidCodecParam::encFmt` (a :cpp:any:`pj::MediaFormatVideo`,
with ``width`` / ``height`` / ``fpsNum`` / ``fpsDenum`` / ``avgBps`` /
``maxBps``), the same fields on ``decFmt``, and the fmtp lists
``encFmtp`` / ``decFmtp`` (each a vector of ``{name, val}`` strings).


Size or resolution
~~~~~~~~~~~~~~~~~~

Specify the video picture dimension.

a. For the encoding direction, configure ``encFmt``:

   .. code-block:: c++

      // Sending 1280 x 720
      param.encFmt.width  = 1280;
      param.encFmt.height = 720;

   .. note::

       - Both width and height must be even numbers.
       - The value may be adjusted to follow remote capability — for
         example, if the peer signals a maximum of 640 × 480 but you
         set 1280 × 720 locally, the negotiated size will be 640 × 480.
       - The library finds the closest size/ratio that the capture
         device supports. Choose a size ratio the device supports;
         otherwise the video may get stretched. For example, if the
         device supports 640 × 480 and 1280 × 720 and you set 500 × 500,
         the camera opens at 640 × 480 and is later stretched to
         500 × 500.

b. For the decoding direction:

   1. Set ``decFmt.width`` / ``decFmt.height`` to the highest values
      expected for incoming video.
   2. If the resolution exceeds the supported maximum compiled into
      the codec backend, you need to bump the per-codec macro
      (``MAX_RX_WIDTH`` / ``MAX_RX_HEIGHT`` in ``openh264.cpp``,
      ``vid_toolbox.m``, or ``and_vid_mediacodec.cpp``; ``MAX_RX_RES``
      in ``vpx.c`` or ``ffmpeg_vid_codecs.c``). Defaults at the time of
      writing:

      +---------------------------+-------------------------+----------------+
      | Codec source              | Macro                   | Default        |
      +===========================+=========================+================+
      | ``openh264.cpp``          | ``MAX_RX_WIDTH`` /      | 1200 × 800     |
      |                           | ``MAX_RX_HEIGHT``       |                |
      +---------------------------+-------------------------+----------------+
      | ``vid_toolbox.m``         | ``MAX_RX_WIDTH`` /      | 1280 × 800     |
      |                           | ``MAX_RX_HEIGHT``       |                |
      +---------------------------+-------------------------+----------------+
      | ``and_vid_mediacodec.cpp``| ``MAX_RX_WIDTH`` /      | 1280 × 800     |
      |                           | ``MAX_RX_HEIGHT``       |                |
      +---------------------------+-------------------------+----------------+
      | ``vpx.c``                 | ``MAX_RX_RES``          | 1200 (max dim) |
      +---------------------------+-------------------------+----------------+
      | ``ffmpeg_vid_codecs.c``   | ``MAX_RX_RES``          | 1200 (max dim) |
      +---------------------------+-------------------------+----------------+

      Verify in the source if you need to push beyond these — the
      values may have been updated since.

   3. Signal to the remote side via codec-specific SDP fmtp parameters
      on ``decFmtp``:

      - **H.263-1998:**

        .. code-block:: c++

           // 1st preference: 352 × 288 (CIF)
           param.decFmtp.push_back({"CIF",  "1"});
           // 2nd preference: 176 × 144 (QCIF)
           param.decFmtp.push_back({"QCIF", "1"});

        The fmtp value is the framerate divisor — see *Framerate*
        below.

      - **H.264:** size is implicitly specified in the H.264 *level*
        (see the standard or the
        `H.264/MPEG-4 AVC levels table
        <http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels>`__),
        signalled via the H.264 SDP fmtp
        `profile-level-id
        <http://tools.ietf.org/html/rfc6184#section-8.1>`__:

        .. code-block:: c++

           // Can receive up to 1280 × 720 @ 30 fps
           // Set the profile level to "1f", which means level 3.1
           param.decFmtp.push_back({"profile-level-id", "xxxx1f"});


Framerate
~~~~~~~~~

Specify the number of frames processed per second.

a. For the encoding direction, configure ``encFmt``:

   .. code-block:: c++

      // Sending @ 30 fps
      param.encFmt.fpsNum   = 30;
      param.encFmt.fpsDenum = 1;

   .. note::

       - The value may be adjusted to follow remote capability — for
         example, if the peer signals a maximum of 10 fps but you set
         30 fps locally, 10 fps will be used.
       - **Limitation:** if preview is enabled before the call is
         established, the capture device opens at the device's default
         framerate, and subsequent calls reusing that device run at
         that framerate regardless of the encoding framerate set
         above. The current workaround is to disable preview before
         media is established and re-enable it once video media is
         active.

b. For the decoding direction:

   1. Set ``decFmt.fpsNum`` / ``decFmt.fpsDenum`` to the highest
      values expected for incoming video.
   2. Signal to the remote side via codec-specific SDP fmtp on
      ``decFmtp``:

      - **H.263-1998:** maximum framerate is specified per
        size/resolution. See
        `RFC 4629 §8.1.1
        <http://tools.ietf.org/html/rfc4629#section-8.1.1>`__.

        .. code-block:: c++

           // 3000 / (1.001 × 2) fps for CIF
           param.decFmtp.push_back({"CIF",  "2"});
           // 3000 / (1.001 × 1) fps for QCIF
           param.decFmtp.push_back({"QCIF", "1"});

      - **H.264:** like resolution, framerate is implicitly specified
        in the H.264 *level* and signalled via ``profile-level-id``:

        .. code-block:: c++

           // Can receive up to 1280 × 720 @ 30 fps
           param.decFmtp.push_back({"profile-level-id", "xxxx1f"});


Bitrate
~~~~~~~

Specify the bandwidth requirement for the video payload stream.

This is configurable via ``avgBps`` and ``maxBps`` on ``encFmt``:

.. code-block:: c++

   // Bitrate range preferred: 512 – 1024 kbps
   param.encFmt.avgBps = 512000;
   param.encFmt.maxBps = 1024000;

.. note::

   - This setting applies to encoding *and* decoding directions —
     there is currently no way to set asymmetric bitrate. On the
     decoding side it is just queried when generating the bandwidth
     info for the local SDP (next point).
   - The bitrate setting of all codecs is enumerated and the highest
     value is signalled in the bandwidth info of the local SDP (see
     ticket :issue:`1244`).
   - The negotiated encoding bitrate may be adjusted to follow the
     remote setting (read from the SDP ``b=TIAS`` line in the remote
     SDP). For example, if the peer signals a max bitrate of 128 kbps
     but you set 512 kbps locally, 128 kbps will be used.
   - For codec-specific bitrate signalling via SDP fmtp (e.g. *MaxBR*
     for H.263), set the fmtp manually:

     .. code-block:: c++

        // H.263 specific maximum bitrate 512 kbps
        param.decFmtp.push_back({"MaxBR", "5120"});  // = max_bps / 100

The codec's ``avgBps`` / ``maxBps`` only configure the encoder's
target; they do not by themselves shape the actual outgoing packet
stream. Per-stream send rate control is configured separately on the
account, via two fields on ``AccountVideoConfig``:

- ``rateControlMethod`` — selects how transmission is paced. Values
  come from :cpp:any:`pjmedia_vid_stream_rc_method`:

  - :cpp:any:`PJMEDIA_VID_STREAM_RC_NONE
    <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_NONE>`:
    no shaping; RTP packets are sent immediately after encoding.
  - :cpp:any:`PJMEDIA_VID_STREAM_RC_SIMPLE_BLOCKING
    <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SIMPLE_BLOCKING>`
    (PJSUA2 default): the thread invoking ``put_frame()`` (typically
    the capture thread) blocks when transmission is ahead of schedule.
  - :cpp:any:`PJMEDIA_VID_STREAM_RC_SEND_THREAD
    <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SEND_THREAD>`
    (PJMEDIA / PJSUA-LIB default): a dedicated sending thread queues
    and paces RTP packets, so the capture thread never blocks.
    Generally yields better video latency than the blocking method.

  Note the PJSUA2 ``AccountVideoConfig`` constructor initialises
  ``rateControlMethod`` to ``SIMPLE_BLOCKING``, which differs from
  the PJSUA-LIB / PJMEDIA default of ``SEND_THREAD``. Set it
  explicitly if you want ``SEND_THREAD`` from PJSUA2.

- ``rateControlBandwidth`` — explicit upstream bandwidth in bps. When
  ``0`` (default), the rate controller follows the codec's ``maxBps``.
  Set this if you need stricter shaping than the encoder target.

.. code-block:: c++

   AccountConfig acc_cfg;
   // ... other configuration ...
   acc_cfg.videoConfig.rateControlMethod    = PJMEDIA_VID_STREAM_RC_SEND_THREAD;
   acc_cfg.videoConfig.rateControlBandwidth = 0;

   MyAccount *acc = new MyAccount;
   acc->create(acc_cfg);


Choosing a bitrate
^^^^^^^^^^^^^^^^^^

There is no single authoritative table for video bitrates; appropriate
values depend on the **usage** (realtime call vs file/VOD playback),
the codec (H.264 vs VP8/VP9 vs H.265), the codec profile, the target
quality, and the motion characteristics of the content.

The two usages have very different budgets:

- **Realtime SIP/RTC video** — the call must stay responsive, so encoding
  is single-pass with near-CBR rate control to keep the link stable, the
  GOP is kept small, and occasional loss is tolerated via PLI/FIR
  keyframe requests. Content is usually low-motion (head-and-shoulders),
  which compresses well, so the *target bitrates are deliberately
  conservative*. End-to-end one-way latency in practice typically lands
  in the few-hundred-millisecond range rather than the sub-200 ms ideal
  often quoted; the figures below are tuned for this case.
- **File / VOD streaming** — no realtime constraint, so the encoder can
  use multi-pass, large GOPs, and high VBR peaks; targets for the same
  resolution and quality are typically **2–4× higher** than realtime
  calls. PJSIP itself doesn't drive a VOD pipeline (its AVI device just
  plays a file into a call), but bitrate values copied from streaming-
  service tables (YouTube, Twitch, broadcast) will not behave well in a
  realtime call.

As an order-of-magnitude starting point for H.264 (Baseline/Main)
**realtime** calls:

+----------------------+-----------+------------------------+
| Resolution           | Framerate | Typical max bitrate    |
+======================+===========+========================+
| QCIF (176 × 144)     | 15 fps    | 64 – 128 kbps          |
+----------------------+-----------+------------------------+
| CIF (352 × 288)      | 15 fps    | 128 – 384 kbps         |
+----------------------+-----------+------------------------+
| VGA (640 × 480)      | 15 – 30   | 384 – 1024 kbps        |
+----------------------+-----------+------------------------+
| 720p (1280 × 720)    | 30 fps    | 1500 – 4000 kbps       |
+----------------------+-----------+------------------------+
| 1080p (1920 × 1080)  | 30 fps    | 3000 – 8000 kbps       |
+----------------------+-----------+------------------------+

A common rule of thumb for realtime H.264 is
*bitrate ≈ K × W × H × FPS*, with K roughly between 0.05 (low motion,
acceptable quality) and 0.15 (high motion, good quality). VP8/VP9
typically need 20–30% less for similar perceived quality, and H.265
even less.

For codec-level upper bounds (which the negotiated H.264 *level*
imposes), see the
`H.264/MPEG-4 AVC levels table <https://en.wikipedia.org/wiki/Advanced_Video_Coding#Levels>`__.
For H.263 framerate-per-resolution limits, see
`RFC 4629 §8.1.1 <https://tools.ietf.org/html/rfc4629#section-8.1.1>`__.


PJSUA-LIB equivalents
---------------------

+----------------------------------------------------+--------------------------------------------------------+
| PJSUA2                                             | PJSUA-LIB                                              |
+====================================================+========================================================+
| ``VidCodecParam``                                  | :cpp:any:`pjmedia_vid_codec_param`                     |
+----------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Endpoint::getVideoCodecParam()`     | :cpp:any:`pjsua_vid_codec_get_param()`                 |
+----------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Endpoint::setVideoCodecParam()`     | :cpp:any:`pjsua_vid_codec_set_param()`                 |
+----------------------------------------------------+--------------------------------------------------------+
| ``VidCodecParam::encFmt`` /                        | ``pjmedia_vid_codec_param::enc_fmt`` /                 |
| ``decFmt`` (``MediaFormatVideo``)                  | ``dec_fmt`` (``pjmedia_format``); fields below are     |
|                                                    | inside ``.det.vid`` (``pjmedia_video_format_detail``). |
+----------------------------------------------------+--------------------------------------------------------+
| ``MediaFormatVideo::width`` / ``.height``          | ``enc_fmt.det.vid.size.w`` / ``.h``                    |
+----------------------------------------------------+--------------------------------------------------------+
| ``MediaFormatVideo::fpsNum`` / ``.fpsDenum``       | ``enc_fmt.det.vid.fps.num`` / ``.denum``               |
+----------------------------------------------------+--------------------------------------------------------+
| ``MediaFormatVideo::avgBps`` / ``.maxBps``         | ``enc_fmt.det.vid.avg_bps`` / ``.max_bps``             |
+----------------------------------------------------+--------------------------------------------------------+
| ``VidCodecParam::encFmtp`` / ``decFmtp``           | ``pjmedia_vid_codec_param::enc_fmtp`` / ``dec_fmtp``   |
| (``CodecFmtpVector`` of ``{name, val}``)           | (``pjmedia_codec_fmtp`` with ``param[]`` of            |
|                                                    | ``{name, val}``)                                       |
+----------------------------------------------------+--------------------------------------------------------+
| ``AccountVideoConfig::rateControlMethod`` /        | :cpp:any:`pjsua_acc_config::vid_stream_rc_cfg`         |
| ``rateControlBandwidth``                           | (``pjmedia_vid_stream_rc_config``)                     |
+----------------------------------------------------+--------------------------------------------------------+

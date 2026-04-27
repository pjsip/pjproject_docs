Modifying Video Codec Parameters
=================================

Video codec parameters are specified in :cpp:any:`pjmedia_vid_codec_param`. The
codec parameters provide separate settings for each direction, encoding
and decoding. Any modifications on video codec parameters can be applied
using :cpp:any:`pjsua_vid_codec_set_param()`, here is a sample code for
reference:

.. code-block:: c

   const pj_str_t codec_id = {"H264", 4};
   pjmedia_vid_codec_param param;

   pjsua_vid_codec_get_param(&codec_id, &param);

   /* Modify param here */
   ...

   pjsua_vid_codec_set_param(&codec_id, &param);


Size or resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Specify video picture dimension.

a. For encoding direction, configured via ``det.vid.size`` field of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

   .. code-block:: c

      /* Sending 1280 x 720 */
      param.enc_fmt.det.vid.size.w = 1280;
      param.enc_fmt.det.vid.size.h = 720;

   .. note::

       - Both width and height must be even numbers.
       - There is a possibility that the value will be adjusted to follow remote capability. For example, if remote signals  that maximum resolution supported is 640 x 480 and locally the encoding direction size is set to 1280 x 720, then 640 x 480 will be used.
       -  The library will find the closest size/ratio that the capture device supports. Application should choose the size ratio that the capture device supports, otherwise the video might get stretched. For example, if the device capture supports 640x480 and 1280x720 and the size is set to 500x500. The device camera will be opened at 640x480 and later converted to 500x500 and get the image stretched.

b. For decoding direction, the following steps are needed:

   1. The ``det.vid.size`` field of :cpp:any:`pjmedia_vid_codec_param::dec_fmt` should be set to the highest value expected for incoming video size.
   2. If the resolution exceeds the supported maximum specified in the video codecs, you need to modify it (``MAX_RX_WIDTH`` and ``MAX_RX_HEIGHT`` in ``openh264.cpp``, ``vid_toolbox.m``, or ``and_vid_mediacodec.cpp``, or ``MAX_RX_RES`` in ``vpx.c`` or ``ffmpeg_vid_codecs.c``). Defaults at the time of writing:

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

      Verify in the source if you need to push beyond these — the values may have been updated since.
   3. signalling to remote, configured via codec specific SDP format parameter (fmtp): :cpp:any:`pjmedia_vid_codec_param::dec_fmtp`.

       - H263-1998, e.g:

         .. code-block:: c

            /* 1st preference: 352 x 288 (CIF) */
            param.dec_fmtp.param[n].name = pj_str("CIF");
            /* The value actually specifies framerate, see framerate section below */
            param.dec_fmtp.param[n].val = pj_str("1");
            /* 2nd preference: 176 x 144 (QCIF) */
            param.dec_fmtp.param[n+1].name = pj_str("QCIF");
            /* The value actually specifies framerate, see framerate section below */
            param.dec_fmtp.param[n+1].val = pj_str("1");

       - H264, the size is implicitly specified in H264 level (check the standard specification or `this Wikipedia page <http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels>`__) and on SDP, the H264 level is signalled via H264 SDP fmtp `profile-level-id <http://tools.ietf.org/html/rfc6184#section-8.1>`__, e.g:

         .. code-block:: c

            /* Can receive up to 1280×720 @30fps */
            param.dec_fmtp.param[n].name = pj_str("profile-level-id");
            /* Set the profile level to "1f", which means level 3.1 */
            param.dec_fmtp.param[n].val = pj_str("xxxx1f");

Framerate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Specify number of frames processed per second.

a. For encoding direction, configured via ``det.vid.fps`` of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

   .. code-block:: c

      /* Sending @30fps */
      param.enc_fmt.det.vid.fps.num   = 30;
      param.enc_fmt.det.vid.fps.denum = 1;

   .. note::

        - There is a possibility that the value will be adjusted to follow remote capability. For example, if remote signals that maximum framerate supported is 10fps and locally the encoding direction framerate is set to 30fps, then 10fps will be used.
        - **Limitation:** if preview is enabled before the call is established, the capture device will be opened using the device's default framerate, and subsequent calls that use that device will use this framerate regardless of the configured encoding framerate that is set above. Currently the only workaround is to disable preview before establishing media and re-enable it once the video media is established.

b. For decoding direction, two steps are needed:

   1. The ``det.vid.fps`` of :cpp:any:`pjmedia_vid_codec_param::dec_fmt` should be set to the highest value expected for incoming video framerate.
   2. signalling to remote, configured via codec specific SDP format parameter (fmtp): :cpp:any:`pjmedia_vid_codec_param::dec_fmtp`.

      - H263-1998, maximum framerate is specified per size/resolution basis, check `RFC 4629 Section 8.1.1 <http://tools.ietf.org/html/rfc4629#section-8.1.1>`__ for more info.

         .. code-block:: c

            /* 3000/(1.001*2) fps for CIF */
            param.dec_fmtp.param[m].name = pj_str("CIF");
            param.dec_fmtp.param[m].val = pj_str("2");
            /* 3000/(1.001*1) fps for QCIF */
            param.dec_fmtp.param[n].name = pj_str("QCIF");
            param.dec_fmtp.param[n].val = pj_str("1");

      - H264, similar to size/resolution, the framerate is implicitly specified in H264 level (check the standard specification or `MPEG-4 AVC levels <http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels>`__) and the H264 level is signalled via H264 SDP fmtp ``profile-level-id``, e.g:

         .. code-block:: c

            /* Can receive up to 1280×720 @30fps */
            param.dec_fmtp.param[n].name = pj_str("profile-level-id");
            param.dec_fmtp.param[n].val = pj_str("xxxx1f");

Bitrate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Specify bandwidth requirement for video payloads stream delivery.

This is configurable via ``det.vid.avg_bps`` and ``det.vid.max_bps`` fields of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

.. code-block:: c

   /* Bitrate range preferred: 512-1024kbps */
   param.enc_fmt.det.vid.avg_bps = 512000;
   param.enc_fmt.det.vid.max_bps = 1024000;

.. note::

   - This setting is applicable for encoding and decoding direction,
     currently there is no way to set asymmetric bitrate. By decoding
     direction, actually it just means that this setting will be queried when
     generating bandwidth info for local SDP (see next point).
   - The bitrate
     setting of all codecs will be enumerated and the highest value will be
     signalled in bandwidth info in local SDP (see ticket :issue:`1244`).
   - There is
     a possibility that the encoding bitrate will be adjusted to follow
     remote bitrate setting, i.e: read from SDP bandwidth info (b=TIAS line)
     in remote SDP. For example, if remote signals that maximum bitrate is
     128kbps and locally the bitrate is set to 512kbps, then 128kbps will be
     used.
   - If codec specific bitrate setting signalling (via SDP fmtp) is
     desired, e.g: *MaxBR* for H263, application should put the SDP fmtp
     manually, for example:

     .. code-block:: c

        /* H263 specific maximum bitrate 512kbps */
        param.dec_fmtp.param[n].name = pj_str("MaxBR");
        param.dec_fmtp.param[n].val = pj_str("5120"); /* = max_bps / 100 */

The codec's ``avg_bps`` / ``max_bps`` only configure the encoder's
target; they do not by themselves shape the actual outgoing packet
stream. Per-stream send rate control is configured separately via
:cpp:any:`pjmedia_vid_stream_rc_config`, exposed in PJSUA-LIB as
:cpp:any:`pjsua_acc_config::vid_stream_rc_cfg`. Two fields:

- :cpp:any:`pjmedia_vid_stream_rc_config::method` — selects how
  transmission is paced:

  - :cpp:any:`PJMEDIA_VID_STREAM_RC_NONE <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_NONE>`:
    no shaping; RTP packets are sent immediately after encoding.
  - :cpp:any:`PJMEDIA_VID_STREAM_RC_SIMPLE_BLOCKING <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SIMPLE_BLOCKING>`:
    the thread invoking ``put_frame()`` (typically the capture thread)
    blocks when transmission is ahead of schedule.
  - :cpp:any:`PJMEDIA_VID_STREAM_RC_SEND_THREAD <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SEND_THREAD>`
    (default): a dedicated sending thread queues and paces RTP
    packets, so the capture thread never blocks. Generally yields
    better video latency than the blocking method.

- :cpp:any:`pjmedia_vid_stream_rc_config::bandwidth` — explicit upstream
  bandwidth in bps. When ``0`` (default), the rate controller follows
  the codec's ``max_bps``. Set this if you need stricter shaping than
  the encoder target.

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

Low video quality despite good network
========================================

Symptom: the network looks healthy (no obvious loss or jitter), the
CPU is not pegged, and yet the rendered video is soft, blurry, or
visibly compressed compared to what the resolution suggests.

#. **Bitrate target is too low for the resolution.** A
   conservative ``max_bps`` paired with a high resolution forces
   the encoder to compress very aggressively. Raise
   ``enc_fmt.det.vid.max_bps`` and ``avg_bps`` on the codec
   parameters. For typical realtime targets see the table in
   :doc:`/specific-guides/video/users_guide/codec_params` under
   *Choosing a bitrate*.

#. **Resolution / framerate are bumping into the codec's level
   ceiling.** For H.264, the SDP-negotiated *level* (encoded in
   the ``profile-level-id`` fmtp) sets a hard upper bound on
   resolution × framerate × bitrate regardless of the codec
   parameters. If the negotiated level is lower than expected,
   confirm both ends advertise the level you want and that the
   max-resolution macros in the codec source aren't capping you
   (``MAX_RX_WIDTH``/``MAX_RX_HEIGHT`` in the openh264 / videotoolbox
   / and_vid_mediacodec sources, or ``MAX_RX_RES`` in vpx /
   ffmpeg_vid_codecs). See the table in
   :doc:`/specific-guides/video/users_guide/codec_params`.

#. **Codec choice is suboptimal.** H.264 (Main/High) and VP9
   generally produce noticeably better quality than H.263 or VP8
   at the same bitrate. If you have a hardware codec available
   (Android MediaCodec, Apple VideoToolbox), prefer it.

#. **Capture device is opening at a lower resolution than
   requested.** PJSIP picks the closest size the camera natively
   offers. If you set the encoder to e.g. 500×500 on a camera that
   only offers 640×480 or 1280×720, the camera opens at 640×480
   and is then scaled, which both stretches and degrades the
   picture. Pick a size the camera natively supports — see the
   note in :doc:`/specific-guides/video/users_guide/codec_params`
   under *Size or resolution*.

#. **Encoder is being asked to slow down by the AV synchronizer.**
   If audio is leading and video is being constantly slowed to
   match, motion can look jerky. This is a tuning issue rather
   than a quality issue per se; see :doc:`lipsync_drift`.

Related: :doc:`choppy_video` (where the underlying cause is
network or CPU rather than configuration).

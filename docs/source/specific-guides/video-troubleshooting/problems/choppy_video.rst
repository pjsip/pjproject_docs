Choppy / frozen / blocky video
================================

Symptom is video that judders, freezes for a moment then catches up,
or shows visible blockiness/macroblocking after motion. Typical
causes:

#. **Network impairments.** The same diagnostic flow as audio
   applies: see
   :doc:`/specific-guides/audio-troubleshooting/checks/rx_quality`.
   Video is less tolerant than audio because keyframes are large
   and a single lost packet can ruin many subsequent frames until
   the next keyframe.

#. **Encoder send rate exceeds the link's capacity.** If the
   encoder's bitrate target is too high for the available upstream
   bandwidth, the link saturates and packets are dropped. Tune
   ``enc_fmt.det.vid.avg_bps`` / ``max_bps`` and the per-stream
   rate-control settings in
   :cpp:any:`pjsua_acc_config::vid_stream_rc_cfg`. See
   :doc:`/specific-guides/video/users_guide/codec_params`.

#. **CPU saturation.** Encoder/decoder cannot keep up, frames are
   dropped or arrive late at the renderer. Check
   :doc:`/specific-guides/audio-troubleshooting/checks/cpu`. Drop
   to a less CPU-intensive codec (or one of the hardware codecs:
   :ref:`amediacodec` on Android, :ref:`videotoolbox` on Apple),
   lower the resolution / fps, or both.

#. **Excessive jitter on the receiver.** A peer that bursts video
   packets unevenly will produce visible micro-pauses in playback.
   The video stream's jitter buffer absorbs some of this; if the
   buffer is too short, set
   ``PJMEDIA_VID_STREAM_DECODE_MIN_DELAY_MSEC`` to a higher
   value (compile-time tunable in ``pjmedia/config.h``).

#. **Keyframe interval is too long for the link's loss profile.**
   Networks with high loss benefit from more frequent keyframes
   so the decoder can recover sooner. The peer's keyframe
   cadence is its decision; you can prompt with PLI or SIP INFO,
   but those are recovery tools, not bandwidth-shaping ones.

Related: :doc:`green_frames`, :doc:`low_quality`,
:doc:`reducing_latency`.

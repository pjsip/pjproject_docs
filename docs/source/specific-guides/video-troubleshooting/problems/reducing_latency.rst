Reducing video latency
=======================

Symptom: end-to-end one-way video latency feels too high — the
remote sees noticeably delayed motion or a perceptible audio-leads-
video gap (see also :doc:`lipsync_drift`).

In a healthy realtime call the dominant latency contributions on
each side are: capture-to-encoder buffering, encoder processing,
network RTT, jitter buffer fill, decoder processing, and renderer
present. Each can be tuned, with diminishing returns and trade-offs.

#. **Lower the jitter buffer floor.** The compile-time tunable
   :cpp:any:`PJMEDIA_VID_STREAM_DECODE_MIN_DELAY_MSEC` (default
   ``100`` ms in ``pjmedia/config.h``) sets the minimum wait the
   decoder applies before declaring frames present. Reducing it
   lowers latency at the cost of being less tolerant of network
   bursts. Raise it back if :doc:`choppy_video` symptoms appear.

#. **Use a hardware codec where available.** :ref:`amediacodec`
   on Android and :ref:`videotoolbox` on Apple have lower per-frame
   processing overhead than the software codecs and free CPU for
   the rest of the pipeline.

#. **Reduce the target resolution / framerate** if the encoder is
   the bottleneck. Encoding 1080p30 takes more time than 720p30
   on every platform; the saved time becomes lower latency.

#. **Use rate-control mode**
   :cpp:any:`PJMEDIA_VID_STREAM_RC_SEND_THREAD <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SEND_THREAD>`
   (the default). The simple-blocking mode adds latency by holding
   the capture thread until the next sending slot;
   ``SEND_THREAD`` offloads pacing to a dedicated thread. See
   :doc:`/specific-guides/video/codec_params`.

#. **Watch for "preview opened the camera at a fixed framerate"
   limitation.** As noted in
   :doc:`/specific-guides/video/codec_params` (under
   *Framerate*), if local preview is started before the call, the
   camera opens at its default framerate and subsequent calls
   inherit it. Disable preview before establishing media if you
   need the encoder framerate to take effect.

#. **CPU contention.** On busy systems, latency symptoms often
   trace back to scheduling delays rather than the codec itself.
   See :doc:`/specific-guides/audio-troubleshooting/checks/cpu`.

#. **Network RTT.** PJSIP cannot make the network faster, but
   excess latency often comes from a misconfigured TURN relay or
   a roundabout NAT path. If the call is going through a relay
   that is geographically far away, that's the floor.

For an intuition on what end-to-end SIP/RTC video latency looks
like in practice, see the *Choosing a bitrate* note in
:doc:`/specific-guides/video/codec_params`.

The audio-side equivalent — much of which transfers — is
:doc:`/specific-guides/audio-troubleshooting/problems/reducing_latency`.

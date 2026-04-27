Green frames
=============

Green output at the renderer (the typical YUV uninitialised pattern:
full luma, zero chroma offset, which renders as solid green) means
the decoder is failing to produce frames *and* the renderer is
repainting an unset buffer.

Current PJMEDIA pre-fills the renderer's frame buffer with black
via :cpp:any:`pjmedia_video_format_fill_black()` in
``pjmedia_vid_port``, so the pre-decode buffer should never appear
green in recent builds. Persistent green therefore indicates an
active fault, not just startup. Likely causes:

#. **You are on an older build that pre-dates the fill-black
   mitigation.** The simplest fix is to upgrade. As a workaround,
   gate the renderer on the first FMT_CHANGED event so the user
   never sees the pre-decode buffer; see :ref:`vid_ug_show_window`.

#. **Codec-level packetization mismatch with the peer.** This is
   particularly seen with VP8 and H.264 when interoperating with
   some SBCs and gateways: the peer's RTP payload format is
   acceptable enough to negotiate, but bytes inside the frame are
   subtly wrong, so the decoder rejects every frame. Capture an
   RTP trace and compare against the codec's RTP RFC; sometimes
   the only fix is patching the packetizer or routing through a
   different codec.

#. **Decoder consistently rejecting frames.** Watch for
   :cpp:any:`PJMEDIA_EVENT_KEYFRAME_MISSING <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_MISSING>`
   events and for codec WARN-level errors emitted by ``ffmpeg``,
   ``openh264``, ``vpx``, or the platform-native codec. Persistent
   keyframe-missing events without a corresponding
   :cpp:any:`PJMEDIA_EVENT_KEYFRAME_FOUND <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_FOUND>`
   indicate the decoder cannot recover.

#. **Severe packet loss preventing decode.** Diagnose the link the
   same way as for audio rx-quality issues:
   :doc:`/specific-guides/audio-troubleshooting/checks/rx_quality`.

#. **Renderer-specific uninitialised state.** A renderer that
   manages its own GPU surface (Metal, OpenGL, SDL with GL) may
   briefly show its surface's clear colour before the first
   decoded frame is presented. Application code that hides the
   window until FMT_CHANGED (:ref:`vid_ug_show_window`) avoids this
   entirely.

Related: :doc:`no_video_remote`, :doc:`choppy_video`.

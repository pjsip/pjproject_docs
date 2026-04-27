No video at peer (persistent black)
=====================================

Some black at the very start of a video stream is normal — the
codec is initialising, the first keyframe (IDR) hasn't arrived yet,
and the renderer surface may not be wired up. The library
pre-fills the renderer's frame buffer with black via
:cpp:any:`pjmedia_video_format_fill_black()`, so the user does not
see uninitialised colours during this window. The cleanest way to
hide the startup window from the user is to leave the renderer
hidden until :cpp:any:`PJMEDIA_EVENT_FMT_CHANGED
<pjmedia_event_type::PJMEDIA_EVENT_FMT_CHANGED>` arrives — see
:ref:`vid_ug_show_window`.

If the remote side keeps showing black past that initial window,
work through these in order:

#. **Verify outgoing transmission is enabled.** Outgoing video is
   *not* started by default. Either set
   :cpp:any:`pjsua_acc_config::vid_out_auto_transmit` to ``PJ_TRUE``
   on the account, or start it explicitly per call with
   :cpp:any:`pjsua_call_set_vid_strm()` and
   ``PJSUA_CALL_VID_STRM_START_TRANSMIT`` /
   ``PJSUA_CALL_VID_STRM_ADD``. See
   :doc:`/specific-guides/video/users_guide/call_video`.
#. **Verify the SDP carries video sendrecv.** Inspect the
   ``media[i].dir`` field of :cpp:any:`pjsua_call_info` and look for
   video marked ``sendonly`` / ``recvonly`` / ``inactive``. If the call
   setting's :cpp:any:`pjsua_call_setting::media_dir` was used, it
   persists across re-INVITEs.
#. **Verify a video codec is actually negotiated by both ends.**
   At least one video codec must be enabled in the build *and*
   supported by the peer. Use :cpp:any:`pjsua_vid_enum_codecs()` to
   see what we offer; check
   :doc:`/specific-guides/video/components` for which backends
   provide which codecs per platform.
#. **Confirm RTP packets are actually being received.** See
   :doc:`/specific-guides/audio-troubleshooting/checks/no_rx_rtp` —
   the same diagnostic applies to video. If no RTP arrives, the
   problem is at the transport / NAT level, not the codec.
#. **Force a keyframe** if the peer is decoding but stuck without
   one (e.g. lost the original IDR): call
   :cpp:any:`pjsua_call_set_vid_strm()` with
   :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>`.
   Conversely, the peer requests a keyframe from us via SIP INFO or
   RTCP PLI; allowed transports are governed by
   :cpp:any:`pjsua_call_setting::req_keyframe_method`. The default
   already enables both. See :ref:`vid_key`.
#. **Hook the call media-state callback.** Implement
   :cpp:any:`pjsua_callback::on_call_media_state` and read the
   per-stream status from :cpp:any:`pjsua_call_info` to confirm the
   video stream actually transitioned to active.

Related: :doc:`green_frames`, :doc:`mobile_bg_fg`,
:doc:`ip_change`.

Lipsync drift
==============

Symptom: audio and video on the same call are noticeably out of
sync, often a few hundred milliseconds, sometimes worse over a long
call.

PJSIP includes an inter-media synchronizer
(:cpp:any:`pjmedia_av_sync`) that PJSUA-LIB sets up automatically
for every call with two or more media streams. If lipsync is
visibly drifting, the synchronizer is either disabled or unable to
do its job. Things to check:

#. **The call is not opted out of synchronization.** Confirm the
   call setting does **not** include
   :cpp:any:`PJSUA_CALL_NO_MEDIA_SYNC`. With that flag set,
   PJSUA-LIB skips synchronizer creation entirely. See
   :doc:`/specific-guides/video/users_guide/av_sync`.

#. **The peer is sending RTCP Sender Reports.** The synchronizer
   anchors its per-media timeline to wall-clock using the NTP and
   RTP timestamps the peer publishes in RTCP SR. If the peer
   doesn't emit SRs (e.g. an old SBC strips RTCP, or RTCP-mux is
   misconfigured), the synchronizer has nothing to anchor on and
   cannot align the streams. Verify SRs are being received by
   inspecting RTCP traffic or
   :cpp:any:`pjsua_call_get_stream_stat` output.

#. **The lag tolerance is set unreasonably tight or loose.** Two
   compile-time tunables in ``pjmedia/config.h`` shape the
   synchronizer:

   - :cpp:any:`PJMEDIA_AVSYNC_MAX_TOLERABLE_LAG_MSEC` (default
     ``45`` ms) — once lag exceeds this and speed-up requests have
     not closed the gap, the synchronizer slows down the leading
     media. Raise this if your deployment legitimately runs with
     larger jitter (e.g. a flaky mobile link with a generous
     jitter buffer) and the synchronizer is fighting it.
   - :cpp:any:`PJMEDIA_AVSYNC_MAX_SPEEDUP_REQ_CNT` (default ``10``)
     — number of speed-up requests tried before switching to
     slow-down on the leading media. Lower if you want it to fall
     back to slow-down faster.

#. **Audio jitter buffer is unusually large.** A long audio jitter
   buffer can outpace the video pipeline's ability to catch up; the
   sync algorithm tries speed-up first, but there's a limit.
   Consider whether the audio buffer setting is excessive for your
   network conditions.

If the call is two-way video but no audio (uncommon), the
synchronizer is still created (≥2 media streams) but it has
nothing meaningful to align — that's a degenerate case and you can
disable it with :cpp:any:`PJSUA_CALL_NO_MEDIA_SYNC`.

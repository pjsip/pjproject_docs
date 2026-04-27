Check video stream state and statistics
==========================================

Most video troubleshooting starts from one question: *what does
PJSIP think the video stream is doing right now?* The library
exposes per-call stream state and statistics that answer this
without needing to peek at packets.

From an interactive ``pjsua`` session
--------------------------------------

The ``pjsua`` sample app has built-in commands that dump everything
relevant for the current call:

- ``cd`` — call dump. Shows each media stream's index, type
  (audio/video), direction, codec, and the conference-bridge slot
  IDs. Useful for confirming whether a video stream is actually
  active in each direction.
- ``dq`` — dump quality of the current call. Shows per-stream RTP
  reception statistics (packets received, lost, jitter, RTT) for
  both audio and video. The video line tells you whether RTP is
  arriving at all and whether the receive path is healthy.

These two together rule out or confirm the network-level
hypotheses without leaving pjsua.

Programmatic access
--------------------

From application code, the same information is available through
the API:

- :cpp:any:`pjsua_call_get_info` populates
  :cpp:any:`pjsua_call_info`. The per-media entries
  ``ci.media[i]`` include the media's type, direction, status, and
  for video the encoding/decoding bridge slot IDs and the
  incoming-video window ID. Use this to answer "is the stream
  active?" and "what does the local SDP say its direction is?".

- :cpp:any:`pjsua_call_get_stream_info` returns codec-level
  details: the video codec ID, encoded format
  (resolution, frame rate, bitrate), packetization parameters,
  and the negotiated fmtp.

- :cpp:any:`pjsua_call_get_stream_stat` returns RTP/RTCP
  statistics: send/receive packet counts, byte counts, loss, jitter,
  round-trip time, and the most recent RTCP SR/RR.

A typical "is video flowing?" check loop is:

#. Read :cpp:any:`pjsua_call_info`. Confirm the video media's
   ``status`` is active and ``dir`` is what you expect.
#. Read :cpp:any:`pjsua_call_get_stream_stat` periodically. If the
   receive packet count never increases, RTP is not arriving — go
   to :doc:`/specific-guides/audio-troubleshooting/checks/no_rx_rtp`.
#. If RTP is arriving but the renderer shows no decoded video,
   subscribe to media events
   (:cpp:any:`pjsua_callback::on_call_media_event`) and look for
   :cpp:any:`PJMEDIA_EVENT_FMT_CHANGED <pjmedia_event_type::PJMEDIA_EVENT_FMT_CHANGED>`
   (decoder learned a format) and
   :cpp:any:`PJMEDIA_EVENT_KEYFRAME_FOUND <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_FOUND>`
   /
   :cpp:any:`PJMEDIA_EVENT_KEYFRAME_MISSING <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_MISSING>`
   (decoder ability to render). Persistent
   ``KEYFRAME_MISSING`` without a corresponding ``KEYFRAME_FOUND``
   points at a codec or packetization fault — see
   :doc:`/specific-guides/video-troubleshooting/problems/green_frames`.

What to log
-----------

For non-trivial video bugs, application logs that include the
output of the above APIs at the moment of the failure (or at a
periodic cadence) save many round-trips. At minimum:

- The raw negotiated SDP for each direction.
- Per-stream stats every few seconds during the call.
- The full sequence of media events received on the call.

.. _vid_ug_av_sync:

Audio/Video Synchronization
============================

When a session carries audio and video together, the two streams
travel and decode through independent pipelines (jitter buffer,
decoder, renderer, file demuxer, …) and accumulate independent
delays. Without intervention, the streams drift apart and the
speaker's mouth no longer matches their voice. PJMEDIA's inter-media
synchronizer (:cpp:any:`pjmedia_av_sync`, in ``pjmedia/av_sync.h``)
aligns the presentation timestamps of all media in the same session
so they stay in sync.

The synchronizer is **timeline-agnostic**: it just needs each
participating media to report (a) periodic *reference points* that
anchor the media's local timestamp to a common wall-clock-style time,
and (b) per-frame *presentation timestamps*. The most common source
of reference points is RTCP Sender Report (NTP + RTP timestamp pairs),
but the same mechanism is used for non-RTP timelines too — see the
AVI player below.


Default behaviour in PJSUA-LIB
------------------------------

For PJSUA-LIB applications, a per-call synchronizer is set up
automatically and no API calls are required for the standard case:

- When a call has **two or more media streams** (typically one audio
  + one video), PJSUA-LIB creates a :cpp:any:`pjmedia_av_sync` for the
  call and registers each stream with it. Subsequent
  re-INVITE/UPDATEs that add streams reuse the same synchronizer; the
  synchronizer is destroyed when the call ends.
- The synchronizer is created in *streaming mode*
  (:cpp:any:`pjmedia_av_sync_setting::is_streaming = PJ_TRUE`), which
  smooths the delay-adjustment values so already-running media don't
  see surprise increases in delay.
- Each stream calls :cpp:any:`pjmedia_av_sync_update_ref()` whenever
  it receives an RTCP SR packet (the SR's NTP and RTP timestamps
  become the reference point), and calls
  :cpp:any:`pjmedia_av_sync_update_pts()` for every frame it returns
  to its sink, acting on the ``adjust_delay`` output to speed up or
  slow down.

Net effect: in a typical audio + video call, lipsync just works — no
application code is required.

Opting out per call
^^^^^^^^^^^^^^^^^^^

To disable inter-media synchronization on a specific call, set the
:cpp:any:`PJSUA_CALL_NO_MEDIA_SYNC` flag (value ``256`` in
:cpp:any:`pjsua_call_flag`) in :cpp:any:`pjsua_call_setting::flag`.
PJSUA-LIB will skip synchronizer creation, or destroy an existing one
if the flag is set on a re-INVITE/UPDATE.

.. code-block:: c

   pjsua_call_setting opt;

   pjsua_call_setting_default(&opt);
   opt.flag |= PJSUA_CALL_NO_MEDIA_SYNC;

   pjsua_call_make_call(acc_id, &dst, &opt, NULL, NULL, &call_id);

You normally don't want this — disabling sync trades lipsync for
streams running independently at their own rates. Reasons one might
flip it on: instrumented testing where you want raw decoder output,
or a non-AV use case (e.g. a call carrying two video streams with no
audio reference) where the synchronizer's reasoning doesn't apply.


AVI playback
------------

The AVI player (:cpp:any:`pjmedia_avi_player_create_streams()`)
creates its own synchronizer per file so the audio and video tracks
of the file stay aligned during playback. There is no RTP and no RTCP
SR involved here; the player anchors each track's timeline at zero
with :cpp:any:`pjmedia_av_sync_update_ref()` (NTP=0, RTP-ts=0) at
file open and again on every rewind/EOF, then drives
:cpp:any:`pjmedia_av_sync_update_pts()` from each frame's PTS as the
file is read out.

A few differences from the PJSUA-LIB call case:

- The synchronizer is created with default settings —
  ``is_streaming`` is left ``PJ_FALSE``, since the file itself is the
  authoritative source of timing and there is no live network jitter
  to smooth against.
- Synchronization can be disabled at file-open time by passing the
  ``PJMEDIA_AVI_FILE_NO_SYNC`` option to
  ``pjmedia_avi_player_create_streams()``.

This is invisible to PJSUA-LIB applications using the AVI device —
they just see properly lipsynced AVI playback into a call.


How the synchronization works
-----------------------------

Conceptually, the synchronizer maintains a per-media estimate of the
*lag* between that stream's presented frames and the earliest media's
presented frames. The lag is computed from two inputs:

- **Reference points** supplied through ``update_ref(ntp, ts)``. Each
  call records that timestamp ``ts`` on the media's local clock
  corresponds to wall-clock time ``ntp``. RTP streams take the pair
  from incoming RTCP SR; the AVI player anchors at ``(0, 0)``; a
  custom pipeline can supply whatever pair makes its timeline
  meaningful.
- **Per-frame presentation timestamps** supplied through
  ``update_pts(pts)``. The synchronizer converts ``pts`` to wall-clock
  using the latest reference point and compares against the other
  media's most recent presented wall-clock.

When media drift, the synchronizer prefers to **speed up the lagging
media** rather than slow down the leading one (no extra buffering is
added). It tries this for up to
:cpp:any:`PJMEDIA_AVSYNC_MAX_SPEEDUP_REQ_CNT` requests
(default **10**). If after that the lag still exceeds
:cpp:any:`PJMEDIA_AVSYNC_MAX_TOLERABLE_LAG_MSEC` (default **45 ms**),
it switches to **slowing down the leading media** to let the laggard
catch up.

The ``adjust_delay`` value returned by ``update_pts`` is in
milliseconds: ``0`` means in-sync, positive means the stream should
add delay, negative means it should drop delay (or skip a frame).

Both constants are compile-time tunables defined in
``pjmedia/config.h``; raise the tolerable-lag threshold if your
deployment legitimately runs with larger jitter (e.g. a flaky network
plus generous jitter buffers) and the synchronizer is fighting it.


Direct PJMEDIA API (custom pipelines)
-------------------------------------

Applications that build their own media pipeline (using PJMEDIA
directly, without going through PJSUA-LIB or the AVI player) drive
the synchronizer themselves. The lifecycle:

#. **Create** with :cpp:any:`pjmedia_av_sync_create()`. Call
   :cpp:any:`pjmedia_av_sync_setting_default()` first to pre-fill
   defaults, then set ``is_streaming = PJ_TRUE`` for live streams
   (skip it for file/clip playback).
#. **Register each media** with
   :cpp:any:`pjmedia_av_sync_add_media()`, passing a
   :cpp:any:`pjmedia_av_sync_media_setting` that names the media,
   its type (:cpp:any:`PJMEDIA_TYPE_AUDIO` or
   :cpp:any:`PJMEDIA_TYPE_VIDEO`), and its clock rate. Keep the
   returned :cpp:any:`pjmedia_av_sync_media` handle.
#. **At each new reference point** (RTCP SR for RTP, ``(0,0)`` for
   files at open / rewind, etc.), call
   :cpp:any:`pjmedia_av_sync_update_ref()`.
#. **On each frame about to be presented**, call
   :cpp:any:`pjmedia_av_sync_update_pts()` and act on the
   ``adjust_delay`` output (positive: add delay, negative: speed up
   or skip).
#. **On media removal / session teardown**, call
   :cpp:any:`pjmedia_av_sync_del_media()` then
   :cpp:any:`pjmedia_av_sync_destroy()`.

:cpp:any:`pjmedia_av_sync_reset()` clears the running per-media state
without removing the registered media — useful on a re-INVITE/UPDATE
that significantly changes the topology, or on a file rewind.

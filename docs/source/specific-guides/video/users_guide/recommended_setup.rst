.. _vid_ug_recommended_setup:

Recommended Setup for a Video Application
==========================================

This page is a checklist of settings, callbacks, and lifecycle
hooks that a typical video-calling application should configure or
implement. Each item links to the relevant sub-topic page for the
detail; the goal here is just to make sure nothing important is
missed.


Build configuration
-------------------

- Build at least one capture device, one renderer device, one video
  codec, and a format converter into the library; see
  :doc:`/specific-guides/video/components`. The bundled libyuv is
  enabled by default and covers the format-converter requirement.
- For mobile builds, the platform-native devices are auto-enabled by
  the configure script (Android Camera2, AVFoundation/Metal on
  iOS, OpenGL ES). Verify they show up at runtime via
  :cpp:any:`pjsua_vid_enum_devs()`.
- Use a hardware codec where available — :ref:`amediacodec` on
  Android, :ref:`videotoolbox` on Apple — to reduce CPU load and
  battery drain. Software codecs (OpenH264, libvpx, FFmpeg) remain
  the cross-platform fallback.


Per-account settings (:cpp:any:`pjsua_acc_config`)
---------------------------------------------------

Set these on the account before registering it:

- :cpp:any:`pjsua_acc_config::vid_in_auto_show` — leave at the
  default ``PJ_FALSE``. Don't auto-show the renderer; gate showing on
  the FMT_CHANGED event so the window opens with the correct
  size and after decode is actually working. See
  :ref:`Showing the incoming video window <vid_ug_show_window>` below.
- :cpp:any:`pjsua_acc_config::vid_out_auto_transmit` — leave at the
  default ``PJ_FALSE`` so the user explicitly starts outgoing video
  with :cpp:any:`pjsua_call_set_vid_strm()`. Set to ``PJ_TRUE`` only
  if your UX is "video on by default".
- :cpp:any:`pjsua_acc_config::vid_cap_dev` /
  :cpp:any:`pjsua_acc_config::vid_rend_dev` — set explicitly to the
  device IDs you want this account to use. Leave at
  ``PJMEDIA_VID_DEFAULT_CAPTURE_DEV`` /
  ``PJMEDIA_VID_DEFAULT_RENDER_DEV`` to follow the system default.
- :cpp:any:`pjsua_acc_config::vid_wnd_flags` — set if you want
  fullscreen at start (bitmask of :cpp:any:`pjmedia_vid_dev_wnd_flag`).
- :cpp:any:`pjsua_acc_config::vid_stream_rc_cfg` — encoder send-rate
  control. Default
  (:cpp:any:`PJMEDIA_VID_STREAM_RC_SEND_THREAD <pjmedia_vid_stream_rc_method::PJMEDIA_VID_STREAM_RC_SEND_THREAD>`)
  is correct for almost all calls. Adjust ``bandwidth`` if you need
  to enforce a stricter cap than the codec's ``max_bps``. See
  :doc:`codec_params` for details.
- :cpp:any:`pjsua_acc_config::vid_stream_sk_cfg` — number and
  interval of keyframes the encoder sends right after a stream is
  created (helps the peer recover quickly).


Per-call settings (:cpp:any:`pjsua_call_setting`)
--------------------------------------------------

Initialise with :cpp:any:`pjsua_call_setting_default()`, then:

- :cpp:any:`pjsua_call_setting::vid_cnt` — ``1`` to include video,
  ``0`` to keep the call audio-only. To add or remove video on an
  established call, change this and re-INVITE via
  :cpp:any:`pjsua_call_reinvite2()` /
  :cpp:any:`pjsua_call_update2()`. See
  :doc:`call_video`.
- :cpp:any:`pjsua_call_setting::req_keyframe_method` — leave at the
  default (``PJSUA_VID_REQ_KEYFRAME_SIP_INFO |
  PJSUA_VID_REQ_KEYFRAME_RTCP_PLI``) unless you have a specific
  reason to disable a transport.
- :cpp:any:`pjsua_call_setting::media_dir` — only set if you need to
  pin a specific stream's direction (set the
  :cpp:any:`PJSUA_CALL_SET_MEDIA_DIR` flag and assign per-media
  values). Note that direction *persists* once narrowed; see the
  notes in :doc:`call_video`.
- Don't set :cpp:any:`PJSUA_CALL_NO_MEDIA_SYNC` unless you really
  want lipsync disabled. It's normally the wrong choice; see
  :doc:`av_sync`.


Callbacks to implement (:cpp:any:`pjsua_callback` / PJSUA2 ``Call``)
--------------------------------------------------------------------

A video-calling application should at minimum hook the following:

- :cpp:any:`pjsua_callback::on_call_media_state` /
  :cpp:func:`pj::Call::onCallMediaState` — fires every time the
  call's media activates/deactivates. Read the ``media[]`` array on
  :cpp:any:`pjsua_call_info` to discover the per-stream status, slot
  IDs, and incoming-video window ID. Use this to wire up your UI
  state and the bridge connections (if you do any
  manually).
- :cpp:any:`pjsua_callback::on_call_media_event` /
  :cpp:func:`pj::Call::onCallMediaEvent` — receives the video
  events listed in
  :doc:`/specific-guides/video/components` under *Media events*. At
  least handle:

  - :cpp:any:`PJMEDIA_EVENT_FMT_CHANGED <pjmedia_event_type::PJMEDIA_EVENT_FMT_CHANGED>` —
    show the renderer window (see :ref:`vid_ug_show_window`) and
    resize your container to
    match the reported size.
  - :cpp:any:`PJMEDIA_EVENT_KEYFRAME_FOUND <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_FOUND>` /
    :cpp:any:`PJMEDIA_EVENT_KEYFRAME_MISSING <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_MISSING>` —
    update UI state ("loading"/"recovering"); on missing, the
    library will already issue a request based on
    :cpp:any:`pjsua_call_setting::req_keyframe_method`.
  - :cpp:any:`PJMEDIA_EVENT_ORIENT_CHANGED <pjmedia_event_type::PJMEDIA_EVENT_ORIENT_CHANGED>` —
    on mobile, signal the new orientation to the peer (Strategy B in
    :doc:`orientation`) or update the device (Strategy A).
  - :cpp:any:`PJMEDIA_EVENT_VID_DEV_ERROR <pjmedia_event_type::PJMEDIA_EVENT_VID_DEV_ERROR>` —
    surface the error (camera unplugged, permission revoked) and
    recover.

  The callback runs on a media thread. Don't block, don't destroy
  the call from inside it — post the work to your own thread.

- :cpp:any:`pjsua_callback::on_call_rx_offer` /
  :cpp:any:`pjsua_callback::on_call_rx_reinvite` — fire when a
  re-INVITE/UPDATE arrives. Update the supplied
  :cpp:any:`pjsua_call_setting` if you want to accept/reject
  individual media or change ``vid_cnt`` before the answer is built;
  modifications persist onto the call. See :doc:`call_video`.

- :cpp:any:`pjsua_callback::on_vid_conf_op_completed` (only if you
  drive the bridge manually) — fires when an
  add/remove/connect/disconnect/update operation has actually taken
  effect; ``info->status`` tells you success/failure. See
  :doc:`conference`.


Threading rules
---------------

- **Mac OS X**: Cocoa frameworks require user-event handling and
  window drawing on the main thread. Don't call any potentially
  blocking PJSIP API from the main thread; use
  :cpp:any:`pj_run_app()` to set up an event-loop thread for your
  ``main_func``. See *Mac OS X Video Threading Issue* in the
  :any:`Video User's Guide </specific-guides/video/users_guide>`.
- **iOS / Windows / generally**: do not call PJSIP API from the GUI
  thread. It can take time to complete or block on a lock. Post work
  to a worker thread, or use
  :cpp:any:`pj::Endpoint::utilTimerSchedule` (PJSUA2) to defer.
- **Media event callbacks** (``on_call_media_event``,
  ``on_vid_conf_op_completed``) run on media threads. Keep the
  handlers short.


Lifecycle: network change
-------------------------

When the host's IP address changes (Wi-Fi ↔ cellular, VPN connect,
docking, …), call :cpp:any:`pjsua_handle_ip_change()` with a
configured :cpp:any:`pjsua_ip_change_param`. PJSIP will tear down and
restart media transports on the new address. After the
re-registration completes:

- If the video on existing calls does not auto-recover, send a
  re-INVITE via :cpp:any:`pjsua_call_reinvite2()` /
  :cpp:any:`pjsua_call_update2()` to rebuild the SDP.
- Once the stream is live again, force a keyframe with
  :cpp:any:`pjsua_call_set_vid_strm()` /
  :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>`
  so the peer's decoder can re-anchor.


Lifecycle: mobile background/foreground
---------------------------------------

On iOS and (to a lesser extent) Android, going to the background
suspends the camera and the renderer surface; the audio session may
also be reclaimed. On returning to the foreground:

- Re-attach the capture device to the active call:
  :cpp:any:`pjsua_call_set_vid_strm()` with
  ``PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV``.
- Request a keyframe from the peer (the library does this
  automatically via PLI/FIR if the decoder reports a missing
  keyframe; you can also force the peer's response by toggling the
  stream direction).
- Configure the iOS audio session and background modes for VoIP
  (microphone + audio + voip background modes) so audio survives
  backgrounding even when video doesn't.


.. _vid_ug_show_window:

Showing the incoming video window
---------------------------------

Recommended pattern for UX-quality displaying of the remote video:

#. Keep ``vid_in_auto_show`` at ``PJ_FALSE`` so the library does not
   show the window for you.
#. In your ``on_call_media_event`` /
   ``onCallMediaEvent`` handler, watch for
   :cpp:any:`PJMEDIA_EVENT_FMT_CHANGED <pjmedia_event_type::PJMEDIA_EVENT_FMT_CHANGED>`
   on the incoming video stream's media index.
#. On the first FMT_CHANGED for that stream, read the new size from
   the event payload, size your UI container accordingly, then
   either embed the native window handle (from
   :cpp:any:`pjsua_vid_win_info::hwnd`, for native windows) into
   your UI hierarchy, or call
   :cpp:any:`pjsua_vid_win_set_show()` (for non-native windows
   like SDL on desktop) to make the renderer visible.
#. Subsequent FMT_CHANGED events on the same stream indicate that
   the peer changed resolution mid-call; resize the container in
   place.

See :doc:`call_video` for the complete window-handling rules,
including the ``is_native`` distinction.


Permissions
-----------

The OS-level camera and microphone permissions must be granted at
runtime; PJSIP cannot work around them.

- **iOS / macOS**: declare ``NSCameraUsageDescription`` and
  ``NSMicrophoneUsageDescription`` in ``Info.plist`` with a
  user-facing reason. The system prompts on first use.
- **Android**: declare ``android.permission.CAMERA`` and
  ``android.permission.RECORD_AUDIO`` in ``AndroidManifest.xml`` and
  request them at runtime
  (``ActivityCompat.requestPermissions``) before starting capture.
  ``android.permission.INTERNET`` is also required.
- **Linux** (V4L2): the user must have read access to
  ``/dev/video*`` (often via the ``video`` group).

If a permission is denied at runtime, capture device opening fails;
the application typically sees a video device error event
(:cpp:any:`PJMEDIA_EVENT_VID_DEV_ERROR <pjmedia_event_type::PJMEDIA_EVENT_VID_DEV_ERROR>`)
or an error return from
:cpp:any:`pjsua_vid_preview_start` /
:cpp:any:`pjsua_call_set_vid_strm`.

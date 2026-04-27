Mobile: video stops after backgrounding
=========================================

On iOS especially, when the app goes to the background the system
suspends the camera, the renderer surface, and the audio session.
Returning to the foreground does not always restore the video
pipeline by itself; the user typically sees a frozen or black
remote view (and may also lose local preview) until the call is
torn down.

Recovery on returning to the foreground:

#. **Re-attach the capture device** to the active call. Call
   :cpp:any:`pjsua_call_set_vid_strm()` with
   :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV>`
   to re-bind the camera. This is a local-only operation; no SDP
   renegotiation is needed.

#. **Request a keyframe from the peer.** When the decoder pipeline
   has been suspended and resumed, the previous decoder context is
   typically invalid; the peer needs to send a fresh IDR. The
   library will issue a PLI/FIR automatically when the decoder
   reports a missing keyframe (subject to
   :cpp:any:`pjsua_call_setting::req_keyframe_method`). You can also
   force the peer's response by toggling the stream direction or
   sending a re-INVITE with the same call settings.

#. **Force a fresh outgoing keyframe** so the peer's decoder
   recovers quickly:
   :cpp:any:`pjsua_call_set_vid_strm()` with
   :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>`.

#. **Verify the iOS audio session and background modes.**
   Configure ``microphone``, ``audio``, and ``voip`` background
   modes in ``Info.plist``. With these set, audio survives
   backgrounding even when video is suspended; without them, audio
   stops too.

#. **Check Android camera service preemption.** Other apps (e.g.
   the Camera app) can preempt the camera service mid-call. Watch
   ``logcat`` for ``Camera`` / ``Camera2`` errors and listen for
   :cpp:any:`PJMEDIA_EVENT_VID_DEV_ERROR <pjmedia_event_type::PJMEDIA_EVENT_VID_DEV_ERROR>`
   media events; on receiving one, prompt the user to grant the
   camera back to your app.

A general best-practice setup for these lifecycle events is in
:doc:`/specific-guides/video/users_guide/recommended_setup`.

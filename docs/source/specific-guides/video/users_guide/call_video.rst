Using Video API (pjsua-lib)
============================

This section provides several sample scenarios of using video in your
application. Please see :any:`vid_ug_api_ref` section in the parent
:any:`Video User's Guide </specific-guides/video/users_guide>` for a
more complete documentation about the Video API.

Enabling Video
~~~~~~~~~~~~~~

By default, video is enabled in :cpp:any:`pjsua_call_setting::vid_cnt` setting.

Incoming Video Call
~~~~~~~~~~~~~~~~~~~

Incoming video will be accepted/rejected depending on whether video is
enabled in the call setting (see above). You can pass the call setting
using the API :cpp:any:`pjsua_call_answer2()` (so for example, to reject the
video, set ``vid_cnt`` to 0 and call :cpp:any:`pjsua_call_answer2()`). If
video is enabled, incoming video will be accepted as long as we have
matching codec for it. However, this does not necessarily mean that the
video will be displayed automatically to the screen, nor that outgoing
video will be transmitted automatically, as there will be separate
settings for these. Outgoing video behavior will be explained in the
next section.

Display Incoming Video Automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, incoming video **is not** displayed automatically, since the
app may want to seek user approval first. Use the following code to
change this behavior on per account basis:

.. code-block:: c

   pjsua_acc_config cfg;

   pjsua_acc_config_default(&cfg);
   cfg.vid_in_auto_show = PJ_TRUE;



Show or Hide Incoming Video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regardless of the setting above, you can use the following steps to show or hide the display incoming video:

1. Use :cpp:any:`pjsua_call_get_vid_stream_idx()` or enumerate the call's media stream to find the media index of the default video. If there are multiple video streams in a call, the default video is the first active video media in the call.
2. Locate the media information of the specified stream index in the :cpp:any:`pjsua_call_info`, and acquire the window ID associated with the remote video. Sample code:

.. code-block:: c

   int vid_idx; pjsua_vid_win_id wid;

   vid_idx = pjsua_call_get_vid_stream_idx(call_id);
   if (vid_idx >= 0) {
      pjsua_call_info ci;

      pjsua_call_get_info(call_id, &ci);
      wid = ci.media[vid_idx].stream.vid.win_in;

   }

3. Using the video window ID, you may retrieve the associated
   native video handle with :cpp:any:`pjsua_vid_win_get_info()` and then show or
   hide the video window using native API, or use
   :cpp:any:`pjsua_vid_win_set_show()` to show/hide the window using PJSUA API.
   See :any:`vid_ug_wvw` section below for information on
   manipulating video windows.


.. _vid_ug_civs:

Controlling Incoming Video Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Controlling the video window above will not cause any re-INVITE or
UPDATE to be sent to remote, since the operation occurs locally.
However, if you wish, you may alter the incoming video stream with
:cpp:any:`pjsua_call_set_vid_strm()` API, and this **will** cause re-INVITE or
UPDATE to be sent to negotiate the new SDP. The relevant operations
that affect incoming video are:

- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_DIR <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_CHANGE_DIR>`: change the media direction (e.g. to
  "sendonly", or even "inactive")
- :cpp:any:`PJSUA_CALL_VID_STRM_REMOVE <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_REMOVE>`: remove
  the media stream altogether by setting its port to zero
- :cpp:any:`PJSUA_CALL_VID_STRM_ADD <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_ADD>`: add a new video media stream

Since :cpp:any:`pjsua_call_set_vid_strm()` will result in renegotiation of the
SDP in a re-INVITE or UPDATE transaction, the result of this operation
will not be available immediately. Application can monitor the status by
implementing :cpp:any:`pjsua_callback::on_call_media_state()` callback and enumerate the media
stream status with pjsua_call_info.

Incoming Re-offer
^^^^^^^^^^^^^^^^^

If a re-offer contains video, the re-offer is automatically answered
with the current video setting in :cpp:any:`pjsua_call_setting`
(i.e. :cpp:any:`pjsua_call_setting::vid_cnt`). There is no
*video-specific* callback for this; the application uses the generic
re-offer callbacks if it wants to influence the answer:

- :cpp:any:`pjsua_callback::on_call_rx_offer()` — fires when a new SDP
  offer is received. The app can update the supplied
  :cpp:any:`pjsua_call_setting` (including ``vid_cnt``) and accept (200)
  or reject (488) before the answer is built.
- :cpp:any:`pjsua_callback::on_call_rx_reinvite()` — fires for re-INVITEs
  with SDP and additionally lets the app reply asynchronously via
  :cpp:any:`pjsua_call_answer_with_sdp()`.

Updates made to :cpp:any:`pjsua_call_setting` from inside these callbacks
are persisted onto the call and applied before the answer SDP is
generated — for example, setting ``vid_cnt = 0`` will drop video from
the answer, and setting ``vid_cnt = 1`` while the offer contains video
will accept it. The media channel is re-initialized to match the new
setting prior to building the answer.

These callbacks are not video-specific — they receive the full SDP, so
the app must inspect the SDP itself to learn whether video was added,
removed, or had its direction changed. Media activity changes after the
answer is sent can also be observed in
:cpp:any:`pjsua_callback::on_call_media_state()`.

Outgoing Video Call
~~~~~~~~~~~~~~~~~~~

Outgoing video is enabled/disabled depending on the call setting. To
initiate a call with video in the SDP as inactive, you can disable the
video in the call setting and set :cpp:any:`pjsua_call_setting::flag` with
:cpp:any:`PJSUA_CALL_INCLUDE_DISABLED_MEDIA`.

Outgoing Video Transmission
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Outgoing video transmission is independent from the incoming video
transmission; each can be operated separately. Note that outgoing video
transmission **is not started by default**, not even when incoming offer
contains video support. This behavior is controlled by
:cpp:any:`pjsua_acc_config::vid_out_auto_transmit` setting, which default to
*PJ_FALSE*. Setting this to *PJ_TRUE* will cause video transmission to
be started automatically on each outgoing calls and on incoming calls
that indicates video support in its offer. However, it is more flexible
and appropriate to leave this setting at PJ_FALSE, and add video later
during the call by using :cpp:any:`pjsua_call_set_vid_strm()` API, as will be
explained shortly.

Default Capture and Render Devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default capture and render devices used by an account are configured
in :cpp:any:`pjsua_acc_config::vid_cap_dev` and
:cpp:any:`pjsua_acc_config::vid_rend_dev` respectively. Setting them once on
the account is more convenient than passing them into individual API
calls later. Use ``PJMEDIA_VID_DEFAULT_CAPTURE_DEV`` /
``PJMEDIA_VID_DEFAULT_RENDER_DEV`` to keep the system default.

Other video-related fields on :cpp:any:`pjsua_acc_config` worth knowing:

- :cpp:any:`pjsua_acc_config::vid_wnd_flags` — bitmask of
  :cpp:any:`pjmedia_vid_dev_wnd_flag` controlling renderer window flags
  (e.g. fullscreen). Defaults to ``0``.
- :cpp:any:`pjsua_call_setting::req_keyframe_method` — bitmask of
  :cpp:any:`pjsua_vid_req_keyframe_method` selecting which keyframe-request
  mechanisms are allowed for the call. Defaults to
  ``PJSUA_VID_REQ_KEYFRAME_SIP_INFO | PJSUA_VID_REQ_KEYFRAME_RTCP_PLI``.
  See :ref:`vid_key`.

.. _vid_ug_cvs:

Controlling Video Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Application uses :cpp:any:`pjsua_call_set_vid_strm()` API to control the
video stream on a call. The available operations
(:cpp:any:`pjsua_call_vid_strm_op`) are:

- :cpp:any:`PJSUA_CALL_VID_STRM_ADD <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_ADD>`: add a new video stream
- :cpp:any:`PJSUA_CALL_VID_STRM_REMOVE <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_REMOVE>`: remove video stream (set port to
  zero)
- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_DIR <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_CHANGE_DIR>`: change direction or deactivate
  (i.e. set direction to "inactive")
- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV>`: change capture device
- :cpp:any:`PJSUA_CALL_VID_STRM_START_TRANSMIT <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_START_TRANSMIT>`: start previously stopped
  transmission
- :cpp:any:`PJSUA_CALL_VID_STRM_STOP_TRANSMIT <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_STOP_TRANSMIT>`: stop transmission
- :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>`: force the encoder to
  generate and send a keyframe as soon as possible (useful when handling
  an incoming FIR/PLI explicitly)

Operations split into two groups depending on whether they trigger SDP
renegotiation:

+--------------------------------------+-------------------------+
| Operation                            | Effect                  |
+======================================+=========================+
| ``PJSUA_CALL_VID_STRM_ADD``          | Sends re-INVITE/UPDATE  |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_REMOVE``       | Sends re-INVITE/UPDATE  |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_CHANGE_DIR``   | Sends re-INVITE/UPDATE  |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV``| Local only              |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_START_TRANSMIT``| Local only              |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_STOP_TRANSMIT`` | Local only              |
+--------------------------------------+-------------------------+
| ``PJSUA_CALL_VID_STRM_SEND_KEYFRAME`` | Local only              |
+--------------------------------------+-------------------------+

For operations that send re-INVITE/UPDATE the result is not available
immediately; the application can implement
:cpp:any:`pjsua_callback::on_call_media_state()` and inspect the resulting
negotiation in :cpp:any:`pjsua_call_info`. See :any:`vid_ug_vcm` below for
more information.

Add or Remove Video
~~~~~~~~~~~~~~~~~~~

There are two ways to add or remove video on an established call:

#. Update :cpp:any:`pjsua_call_setting::vid_cnt` to the desired video
   count and send a re-INVITE or UPDATE with the new setting using
   :cpp:any:`pjsua_call_reinvite2()` or :cpp:any:`pjsua_call_update2()`
   (the non-``2`` variants reuse the existing call setting and so cannot
   change ``vid_cnt``). For example, to add a single video stream:

   .. code-block:: c

      pjsua_call_setting opt;

      pjsua_call_setting_default(&opt);
      opt.vid_cnt = 1;          /* set to 0 to remove video */

      pjsua_call_reinvite2(call_id, &opt, NULL);

   The same call-setting path can also set or change the SDP direction
   of individual media via :cpp:any:`pjsua_call_setting::media_dir`,
   gated by the :cpp:any:`PJSUA_CALL_SET_MEDIA_DIR` flag. Each entry
   ``media_dir[i]`` corresponds to the provisional media in
   :cpp:any:`pjsua_call_info::prov_media` (audios first, then videos);
   for example, in a call with one audio and one video, ``media_dir[0]``
   targets the audio and ``media_dir[1]`` targets the video. Once set,
   the direction *persists* for subsequent offers and answers (e.g. a
   stream marked :cpp:any:`PJMEDIA_DIR_ENCODING` can only be sendonly or
   inactive thereafter; it will not become sendrecv on its own). To send
   only outgoing video while still accepting the rest of the offer:

   .. code-block:: c

      pjsua_call_setting opt;

      pjsua_call_setting_default(&opt);
      opt.flag |= PJSUA_CALL_SET_MEDIA_DIR;
      opt.media_dir[0] = PJMEDIA_DIR_ENCODING_DECODING;   /* audio */
      opt.media_dir[1] = PJMEDIA_DIR_ENCODING;            /* video: sendonly */

      pjsua_call_reinvite2(call_id, &opt, NULL);

   ``media_dir`` can be supplied in any API or callback that accepts
   :cpp:any:`pjsua_call_setting`, including :cpp:any:`pjsua_call_make_call()`,
   :cpp:any:`pjsua_call_answer2()`, the ``*_reinvite2``/``*_update2``
   APIs, and inside :cpp:any:`pjsua_callback::on_call_rx_offer()` /
   :cpp:any:`pjsua_callback::on_call_rx_reinvite()`.

#. Use :cpp:any:`pjsua_call_set_vid_strm()` with one of the stream
   operations described in :any:`vid_ug_civs` or :any:`vid_ug_cvs`
   above (e.g. ``PJSUA_CALL_VID_STRM_ADD`` to add a stream,
   ``PJSUA_CALL_VID_STRM_REMOVE`` to drop one,
   ``PJSUA_CALL_VID_STRM_CHANGE_DIR`` to change direction).

Both paths trigger SDP renegotiation. Monitor the result via
:cpp:any:`pjsua_callback::on_call_media_state()`.


.. _vid_ug_wvw:

Working with Video Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A video window represents a renderer surface created by the library to
display incoming call video, local capture preview, or other video
playback. The application typically retrieves a window ID
(:cpp:any:`pjsua_vid_win_id`) and then either embeds the underlying
native surface into its own UI or manipulates the window through the
PJSUA window APIs.

Where windows come from
^^^^^^^^^^^^^^^^^^^^^^^

- **From an active call** — read the incoming-video window ID from
  ``ci.media[i].stream.vid.win_in`` (where ``ci`` is
  :cpp:any:`pjsua_call_info`), or use the convenience API
  :cpp:any:`pjsua_call_get_vid_win()`.
- **From a local capture preview** — start the preview with
  :cpp:any:`pjsua_vid_preview_start()` and read the window ID with
  :cpp:any:`pjsua_vid_preview_get_win()`; stop with
  :cpp:any:`pjsua_vid_preview_stop()`.
  :cpp:any:`pjsua_vid_preview_has_native()` reports whether the capture
  device has built-in preview rendering (e.g. iOS UIView-backed
  cameras) so that no extra rendering pass is needed.
- **From any source** — enumerate every window managed by the library
  with :cpp:any:`pjsua_vid_enum_wins()`.

Native vs non-native windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The application retrieves :cpp:any:`pjsua_vid_win_info` for a window via
:cpp:any:`pjsua_vid_win_get_info()`. The most commonly used field is the
native handle in :cpp:any:`pjsua_vid_win_info::hwnd` (a
:cpp:any:`pjmedia_vid_dev_hwnd` structure), which the application can
embed into its own GUI hierarchy.

The :cpp:any:`pjsua_vid_win_info::is_native` flag determines which APIs
are valid for manipulating the window:

- **Non-native windows** (``is_native == PJ_FALSE``, e.g. SDL on
  desktop): use the PJSUA window APIs —
  :cpp:any:`pjsua_vid_win_set_show()`,
  :cpp:any:`pjsua_vid_win_set_pos()`,
  :cpp:any:`pjsua_vid_win_set_size()`,
  :cpp:any:`pjsua_vid_win_rotate()` (angle in multiples of 90°), and
  :cpp:any:`pjsua_vid_win_set_fullscreen()` (currently SDL only).
- **Native windows** (``is_native == PJ_TRUE``, e.g. iOS UIView, OpenGL
  on iOS/Android, Metal): the PJSUA show/pos/size/rotate APIs are not
  valid; the application must operate on ``hwnd`` through the
  platform's own windowing API.

Special case: :cpp:any:`pjsua_vid_win_set_win()` swaps the output
window on-the-fly. It requires the device to support
``PJMEDIA_VIDEO_DEV_CAP_OUTPUT_WINDOW`` and to allow on-the-fly
swapping — currently implemented only on Android.

.. _vid_key:

Video Keyframe Transmission
============================

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

.. contents::
   :local:
   :depth: 2

PJSIP supports both ends of video keyframe-request signalling so that a
peer that loses decoder state can ask the sender for an IDR frame.

Outgoing keyframe request
-------------------------

When the local decoder has lost state and needs a fresh IDR from the
peer, the library can request one via either of two transports:

- **SIP INFO with XML Schema for Media Control**
  (:rfc:`5168#section-7.1`), carrying either a Full Intra Request
  (:rfc:`5104#section-3.5.1`) or a Picture Loss Indication
  (:rfc:`4585#section-6.3.1`). See ticket :issue:`1234` for the
  integration history.
- **RTCP Picture Loss Indication** (:rfc:`4585#section-6.3.1`). See
  ticket :issue:`1437`.

Which transports are allowed for a given call is controlled by
``CallSetting::reqKeyframeMethod`` — a bitmask whose values come from
:cpp:any:`pjsua_vid_req_keyframe_method`. The default,
``PJSUA_VID_REQ_KEYFRAME_SIP_INFO | PJSUA_VID_REQ_KEYFRAME_RTCP_PLI``,
is appropriate for most deployments — leave it alone unless you have a
specific reason to disable a transport.

.. code-block:: c++

   try {
       CallOpParam prm;
       prm.opt.reqKeyframeMethod = PJSUA_VID_REQ_KEYFRAME_RTCP_PLI;
       call.makeCall(dst_uri, prm);
   } catch(Error& err) {
   }


Incoming keyframe request
-------------------------

When the peer asks the encoder via SIP INFO or RTCP PLI/FIR, the
library tells the encoder to emit a keyframe on the next frame. The
application can also force an outgoing keyframe explicitly via
:cpp:func:`pj::Call::vidSetStream()` with the
``PJSUA_CALL_VID_STRM_SEND_KEYFRAME`` operation:

.. code-block:: c++

   try {
       CallVidSetStreamParam param;
       call.vidSetStream(PJSUA_CALL_VID_STRM_SEND_KEYFRAME, param);
   } catch(Error& err) {
   }

Useful after a network change, after the peer reconnects from
background, or when the application detects that a remote viewer has
just joined.


Keyframes at the start of a stream
-----------------------------------

To help the peer's decoder anchor quickly when a stream is first
created, configure how many keyframes the encoder sends right after
the stream goes up via two fields on ``AccountVideoConfig``:

- ``startKeyframeCount`` — how many keyframes to send.
- ``startKeyframeInterval`` — interval between them, in milliseconds.

Defaults are ``PJMEDIA_VID_STREAM_START_KEYFRAME_CNT`` and
``PJMEDIA_VID_STREAM_START_KEYFRAME_INTERVAL_MSEC``.

.. code-block:: c++

   AccountConfig acc_cfg;
   // ... other configuration ...
   acc_cfg.videoConfig.startKeyframeCount    = 3;
   acc_cfg.videoConfig.startKeyframeInterval = 1000;  // ms

   MyAccount *acc = new MyAccount;
   acc->create(acc_cfg);

PJSUA-LIB exposes the same settings on
:cpp:any:`pjsua_acc_config::vid_stream_sk_cfg` (a
:cpp:any:`pjmedia_vid_stream_sk_config`). See ticket :issue:`1910`
for the rationale.


Associated media events
-----------------------

The decoder reports keyframe state via two media events delivered to
:cpp:func:`pj::Call::onCallMediaEvent`:

- :cpp:any:`PJMEDIA_EVENT_KEYFRAME_FOUND <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_FOUND>`
  — the decoder anchored on a keyframe.
- :cpp:any:`PJMEDIA_EVENT_KEYFRAME_MISSING <pjmedia_event_type::PJMEDIA_EVENT_KEYFRAME_MISSING>`
  — the decoder is producing output without an anchor (typically green
  or scrambled frames). On this event the library will also issue a
  keyframe request to the peer based on
  ``CallSetting::reqKeyframeMethod`` above.

Both are listed alongside the rest of the video event types under
:ref:`Media events <video_media_events>` on the
:doc:`Video components and backends <components>` page.


PJSUA-LIB equivalents
---------------------

+----------------------------------------------------+------------------------------------------------------+
| PJSUA2                                             | PJSUA-LIB                                            |
+====================================================+======================================================+
| ``CallSetting::reqKeyframeMethod``                 | :cpp:any:`pjsua_call_setting::req_keyframe_method`   |
+----------------------------------------------------+------------------------------------------------------+
| :cpp:func:`pj::Call::vidSetStream()` +             | :cpp:any:`pjsua_call_set_vid_strm()` +               |
| ``PJSUA_CALL_VID_STRM_SEND_KEYFRAME``              | ``PJSUA_CALL_VID_STRM_SEND_KEYFRAME``                |
+----------------------------------------------------+------------------------------------------------------+
| ``AccountVideoConfig::startKeyframeCount`` /       | :cpp:any:`pjsua_acc_config::vid_stream_sk_cfg`       |
| ``startKeyframeInterval``                          |                                                      |
+----------------------------------------------------+------------------------------------------------------+
| :cpp:func:`pj::Call::onCallMediaEvent`             | :cpp:any:`pjsua_callback::on_call_media_event`       |
+----------------------------------------------------+------------------------------------------------------+

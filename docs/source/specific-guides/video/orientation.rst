Setting Video Capture Orientation
==================================

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

On mobile platforms the device rotates while a call is in progress, but
the camera sensor's orientation does not, so transmitted video can end
up sideways or upside-down at the peer. There are two strategies for
handling this; pick one and use it consistently.

Strategy A — rotate at the capture device (default)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application listens for device-orientation changes from the OS and
forwards each new value to the capture device, which rotates (and may
downsize) the captured frame so the image is always upright at the
peer. Steps:

1. Subscribe to OS-level orientation-change notifications (e.g. iOS
   ``UIDeviceOrientationDidChangeNotification``, Android display
   rotation callbacks).
2. Inside the callback, tell the capture device about the new
   orientation:

   .. code-block:: c++

      Endpoint::instance().vidDevManager()
                          .setCaptureOrient(dev_id, new_orient, true);

For working examples see the iOS and Android entries under
:ref:`Sample Applications with Video <vid_ug_samples>`. Ticket
:issue:`1861` explains the feature in detail.

Strategy B — signal the peer (no device-side rotation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the application can signal orientation to the remote out-of-band
(e.g. SIP INFO or an RTP header extension), it can leave the capture
device alone and let the peer rotate the received video. The advantage
is that the transmitted picture is always full-frame — no letterbox
bands from forcing landscape content into a portrait frame or vice
versa. The trade-off is that the picture is not "upright" on the wire;
the peer must apply rotation using the out-of-band orientation info.

When using this strategy, set the **initial** orientation of the
codec parameters and the capture device to match the device's starting
posture, then **leave them alone** for the rest of the call. PJSIP's
default codec parameters assume landscape; if the call should start in
portrait, configure the encoder format to portrait dimensions
(``width < height``):

.. code-block:: c++

   // Sending 240 x 320
   param.encFmt.width  = 240;
   param.encFmt.height = 320;

…and tell the capture device the initial orientation **once**, after
it is opened (e.g. by :cpp:func:`pj::VideoPreview::start()` or
implicitly by an outgoing/incoming video call):

.. code-block:: c++

   // On Android, portrait corresponds to PJMEDIA_ORIENT_ROTATE_270DEG.
   // On iOS, portrait corresponds to PJMEDIA_ORIENT_ROTATE_90DEG.
   pjmedia_orient current_orient = PJMEDIA_ORIENT_ROTATE_90DEG;

   Endpoint::instance().vidDevManager()
                       .setCaptureOrient(dev_id, current_orient, true);

After this initial setup, the application **must not** call
``setCaptureOrient()`` again on subsequent orientation changes — doing
so puts you back into Strategy A and forces the device to rotate.
Instead, only update the remote peer over the out-of-band signalling
channel.


PJSUA-LIB equivalents
---------------------

+------------------------------------------------------+------------------------------------------------------+
| PJSUA2                                               | PJSUA-LIB                                            |
+======================================================+======================================================+
| ``Endpoint::vidDevManager().setCaptureOrient()``     | :cpp:any:`pjsua_vid_dev_set_setting()` with          |
|                                                      | ``PJMEDIA_VID_DEV_CAP_ORIENTATION``                  |
+------------------------------------------------------+------------------------------------------------------+
| ``VidCodecParam::encFmt.width`` / ``.height``        | ``pjmedia_vid_codec_param::enc_fmt.det.vid.size.w``  |
|                                                      | / ``.h``                                             |
+------------------------------------------------------+------------------------------------------------------+
| :cpp:func:`pj::VideoPreview::start()`                | :cpp:any:`pjsua_vid_preview_start()`                 |
+------------------------------------------------------+------------------------------------------------------+

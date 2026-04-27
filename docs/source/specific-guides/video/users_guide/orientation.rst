Setting Video Capture Orientation
==================================

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
   orientation, using either PJSUA-LIB's
   :cpp:any:`pjsua_vid_dev_set_setting()`:

   .. code-block:: c

      pjsua_vid_dev_set_setting(dev_id, PJMEDIA_VID_DEV_CAP_ORIENTATION,
                                &new_orient, PJ_TRUE);

   or PJSUA2's :cpp:any:`pj::VidDevManager::setCaptureOrient()`:

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

.. code-block:: c

   /* Sending 240 x 320 */
   param.enc_fmt.det.vid.size.w = 240;
   param.enc_fmt.det.vid.size.h = 320;

…and tell the capture device the initial orientation **once**, after
it is opened (e.g. by :cpp:any:`pjsua_vid_preview_start()` or implicitly
by an outgoing/incoming video call):

.. code-block:: c

   /* On Android, portrait corresponds to PJMEDIA_ORIENT_ROTATE_270DEG */
   current_orient = PJMEDIA_ORIENT_ROTATE_270DEG;

   /* On iOS, portrait corresponds to PJMEDIA_ORIENT_ROTATE_90DEG */
   current_orient = PJMEDIA_ORIENT_ROTATE_90DEG;

   pjsua_vid_dev_set_setting(dev_id, PJMEDIA_VID_DEV_CAP_ORIENTATION,
                             &current_orient, PJ_TRUE);

After this initial setup, the application **must not** call
``pjsua_vid_dev_set_setting()`` / ``setCaptureOrient()`` on subsequent
orientation changes — doing so puts you back into Strategy A and forces
the device to rotate. Instead, only update the remote peer over the
out-of-band signaling channel.

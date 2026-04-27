"Invalid video device" / no preview
=====================================

Symptom: starting a preview or a video call fails with an
"Invalid video device" error, or
:cpp:any:`pjsua_vid_dev_count()` returns 0, or no camera shows up
in the enumerated device list.

#. **Confirm the device backend is actually built in.** Use
   :cpp:any:`pjsua_vid_enum_devs()` to list what's registered. If
   the list is empty or missing the camera you expect:

   - The corresponding ``PJMEDIA_VIDEO_DEV_HAS_*`` macro is
     probably unset in your build (DirectShow on Windows, V4L2
     on Linux, ANDROID on Android, DARWIN/AVFoundation on Apple,
     etc.). See
     :doc:`/specific-guides/video/components`.
   - The corresponding native SDK was not detected at configure
     time (e.g. SDL2 dev package not installed). Re-run the
     configure step and check the output.

#. **Check OS-level camera permission.** macOS and iOS require an
   explicit camera privacy entitlement; Android requires the
   ``CAMERA`` runtime permission (and ``RECORD_AUDIO`` for audio).
   The OS surfaces a permission dialog on first use only — once
   denied, the next attempt fails silently until the user changes
   it in System Preferences / Settings.

   - **iOS / macOS**: declare ``NSCameraUsageDescription`` and
     ``NSMicrophoneUsageDescription`` in ``Info.plist`` with a
     user-facing reason. Without these keys, the OS terminates
     the app on first camera access.
   - **Android**: declare ``android.permission.CAMERA`` in
     ``AndroidManifest.xml`` *and* request it at runtime via
     ``ActivityCompat.requestPermissions`` before starting
     capture or making a video call.
   - **Linux** (V4L2): the user must have read access to
     ``/dev/video*`` (often via the ``video`` group). Check
     ``ls -l /dev/video0``.

#. **Capture device already in use.** Some platforms allow only
   one process to hold the camera at a time. Other apps (browser
   tabs with the camera live, recording apps, the Camera app on
   mobile) preempt or block PJSIP's access. Close the other app or
   process and retry.

#. **Native renderer surface is not ready yet.** On platforms
   where the renderer needs a parent native window, calling
   :cpp:any:`pjsua_vid_preview_start()` before that window exists
   can fail. Make sure your UI has created the container before
   you start preview.

A general best-practice for permissions and device setup is in
:doc:`/specific-guides/video/users_guide/recommended_setup`.

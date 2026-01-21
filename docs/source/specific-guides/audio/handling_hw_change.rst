Handling HW insertion/removal
===========================================
PJSIP currently does not automatically handle hot-plugging of audio devices while
the application is running. Hot-plugging can be supported by the application,
by capturing the hot-plug event and reinitialize the audio subsytem when the event
is detected.

The method to detect audio device insertion/removal varies according to the platform,
and it is outside the scope of PJSIP. For example, the Windows Core Audio APIs provide
a mechanism to listen for device events, see the `device events documentation <https://learn.microsoft.com/en-us/windows/win32/coreaudio/device-events>`_.
Once a device change event is detected, call :cpp:any:`pjmedia_aud_dev_refresh()` to cause
PJMEDIA to refresh its sound device list. While the API says that it won't affect active
audio device, we recommend doing this when the sound device is not being opened to avoid
any problems. One way to do this is to call :cpp:any:`pjsua_set_no_snd_dev()` to forcefully
close the currently opened sound device (if any). Once the reinitialization is complete,
tell PJSIP to manage the sound device again by calling :cpp:any:`pjsua_set_snd_dev()`.
Be careful that the sound device indexes may have changed now after the refresh.

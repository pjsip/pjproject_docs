Handling HW insertion/removal
===========================================
PJSIP currently does not automatically handle hot-plugging of audio devices while
the application is running. Hot-plugging can be supported by the application,
by capturing the hot-plug event and reinitialize the audio subsytem when the event
is detected.

The method to detect audio device insertion/removal varies according to the platform,
and it is outside the scope of PJSIP. For Windows XP for example, we can use a sample
generic hardware detection procedure in http://www.codeproject.com/KB/system/HwDetect.aspx,
replacing the device interface class ID with audio device interface below (use any of it): 

.. code-block:: c

    GUID = { 0x65E8773D, 0x8F56, 0x11D0, {0xA3, 0xB9, 0x00, 0xA0, 0xC9, 0x22, 0x31, 0x96} };
    //{ 0x65E8773E, 0x8F56, 0x11D0, {0xA3, 0xB9, 0x00, 0xA0, 0xC9, 0x22, 0x31, 0x96} },
    //{ 0x6994AD04, 0x93EF, 0x11D0, {0xA3, 0xCC, 0x00, 0xA0, 0xC9, 0x22, 0x31, 0x96} }


Once a device change event is detected, call :cpp:any:`pjmedia_aud_dev_refresh()` to cause
PJMEDIA to refresh its sound device list. While the API says that it won't affect active
audio device, we recommend doing this when the sound device is not being opened to avoid
any problems. One way to do this is to call :cpp:any:`pjsua_set_no_snd_dev()` to forcefully
close the currently opened sound device (if any). Once the reinitialization is complete,
tell PJSIP to manage the sound device again by calling :cpp:any:`pjsua_set_snd_dev()`.
Be careful that the sound device indexes may have changed now after the refresh.

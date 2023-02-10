Platform Considerations
========================

.. contents:: Table of Contents
    :depth: 2

Platform selection is usually driven by business motives. The selection will affect all aspects of 
development, and this section will try to cover considerations for each platforms that PJSIP supports.

Android
-------
All features are expected to work. Considerations for Android:

#. You can use PJSUA2 Java binding or C# binding (using Xamarin) for this target.
#. Some audio tuning may be needed to improve the audio quality. Echo cancellation also needs to be checked.

Detailed Android guide is in :doc:`Getting Started for Android  </get-started/android/index>`

iOS for iPhone, iPad, and other Apple devices
---------------------------------------------------
All features are expected to work. Considerations for iOS:

#. You need to use TCP transport for SIP for the background feature to work
#. IP change (for example when user is changing access point) is a feature frequently asked by developers 
   and you can find the documentation in :doc:`Guide to IP Address Change </specific-guides/network_nat/ip_change>`
#. If SSL is needed, native Mac OS/iOS SSL backend is available. See our :ref:`SSL Guide <guide_ssl>`

Detailed iPhone/iOS guide is in :doc:`Getting Started for iPhone/iOS  </get-started/ios/index>`

Windows Desktop
----------------
Windows is supported from Windows 2000 up to Windows 10 and beyond. All features are expected 
to work. 64bit is supported. Development is based on Visual Studio. Considerations for 
this platform include:

#. Because Visual Studio file format keeps changing on every release, we decided to support Visual Studio
   2015. Newer VS should be able to open the projects.

Detailed Windows guide is in :doc:`Getting Started for Windows  </get-started/windows/index>`

MacOS X
-------
All features are expected to work. Considerations include:

#. Development with XCode is currently not supported. This is **not** to say that you cannot use XCode, 
   but PJSIP only provides basic Makefiles and if you want to use XCode you'd need to arrange the project 
   yourself.
#. Mac systems typically provides very good sound device, so we don't expect any problems with audio 
   on Mac. 

Detailed MacOS guide is in :doc:`Getting Started for Mac/Linux/Unix  </get-started/posix/index>`

Linux Desktop
-------------
All features are expected to work. Linux considerations:

#. Use our native ALSA backend instead of PortAudio because ALSA has less jitter than OSS and our backend 
   is more lightweight than PortAudio

Detailed Linux guide is in :doc:`Getting Started for Mac/Linux/Unix  </get-started/posix/index>`

Windows Phone 10 (UWP)
--------------------------
Windows Phone 10/Universal Windows Platform (UWP) support has being added in version 2.6. 
Specific considerations for this platform are:

#. WP8 governs specific interaction with WP8 GUI and framework that needs to be followed by application 
   in order to make VoIP call work seamlessly on the device. Some lightweight process will be created by 
   WP8 framework in order for background call to work and PJSIP needs to put its background processing in 
   this process' context. Currently this feature is under development.

Detailed Windows Phone guide is in :doc:`Getting Started for Windows Phone  </get-started/windows-phone/index>`

Embedded Linux
--------------
In general embedded Linux support is similar to Linux and there should be no problem with it. 
There may be some specific considerations for embedded Linux:

#. The performance of the audio device is probably the one with most issues, as some development boards 
   does not have a decent sound device. Typically there is high audio jitter (or burst) and latency. 
   This will affect end to end audio latency and also the performance of the echo canceller. Also we 
   found that ALSA generally works better than OSS, so if you can have ALSA up and running that will be 
   better. Use the native ALSA backend audio device instead of PortAudio since it is simpler and lighter.

The :doc:`Getting Started for Mac/Linux/Unix  </get-started/posix/index>` may be suitable.

QNX or Other Posix Embedded OS
------------------------------
This is not part of our officially supported OS platforms, but users have run PJSIP on QNX and 
BlackBerry 10 is based on QNX too (we supported BB10 in the past). Since QNX provides Posix API, 
and maybe by using the settings found in the ``configure-bb10 script``, PJSIP should be able to run on it, 
but you need to develop PJMEDIA  sound device wrapper for your audio device. Other than this, we don't have 
enough experience to comment on the platform. 

The :doc:`Getting Started for Mac/Linux/Unix  </get-started/posix/index>` may be suitable.

Other Unix Desktop OSes
-----------------------
Community members, including myself, have occasionally run PJSIP on other Unix OSes such as Solaris, 
FreeBSD, and OpenBSD. We expect PJSIP to run on these platforms (maybe with a little kick). However,
the sound device most likely will be limited to OSS, which is provided by PortAudio.

The :doc:`Getting Started for Mac/Linux/Unix  </get-started/posix/index>` may be suitable.

Porting to Other Embedded OS
------------------------------
It is possible to port PJSIP to other embedded OS or even directly to device without OS and people 
have done so. In general, the closer resemblance the new OS to existing supported OS, the easier 
the porting job will be. The good thing is, PJSIP has been made to be very very portable, and system 
dependent features are localized in PJLIB and PJMEDIA audio device, so the effort is more quantifiable. 
Once you are able to successfully run *pjlib-test*, you are more or less done with your porting effort. 
Other than that, if you really want to port PJSIP to new platform, you probably already know what 
you're doing. 

The remaining sections below are for historical information only.

Symbian
-------
.. note::

   Symbian is no longer supported. For historical information see
   https://trac.pjsip.org/repos/wiki/Getting-Started/Symbian

Symbian has been supported for a long time. In general all features (excluding video) are expected to 
work, but we're not going to do Symbian specific development anymore. Other considerations for Symbian:

#. The MDA audio is not very good (it has high latency), so normally you'd want to use Audio Proxy 
   Server (APS) or VoIP Audio Service (VAS) for the audio device, which we support. Using these audio backends will also provide us with high quality echo cancellation as well as low bitrate codecs such as AMR-NB, G.729, and iLBC. But VAS and APS requires purchase of Nokia development certificate to sign the app, and also since APS and VAS only run on specific device type, you need to package the app carefully and manage the deployment to cover various device types.


BlackBerry 10
-------------
.. note::

   BB10 is no longer supported. For historical information see https://trac.pjsip.org/repos/wiki/Getting-Started/BB10

BlackBerry 10 (BB10) is supported since PJSIP version 2.2. Some considerations for BB10 platform include:

#. IP change (for example when user is changing access point) is a feature frequently asked by developers 
   and you can find the documentation in :doc:`Guide to IP Address Change </specific-guides/network_nat/ip_change>`


Windows Mobile
--------------
.. note::

   Windows Mobile is no longer supported. For historical information see
   https://trac.pjsip.org/repos/wiki/Getting-Started/Windows-Mobile

This is the old Windows Mobile platform that is based on WinCE. This platform has been supported for a 
long time. We expect all features except video to work, but there may be some errors every now and then 
because this target is not actively maintained. No new development will be done for this platform.

Other considerations for Windows Mobile platform are:

#. The quality of audio device on WM varies a lot, and this affects audio latency. Audio latency could go 
   as high as hundreds of millisecond on bad hardware.
#. Echo cancellation could be a problem. We can only use basic echo suppressor due to hardware limitation, 
   and combined with bad quality of audio device, it may cause ineffective echo cancellation. This could be 
   mitigated by setting the audio level to low.



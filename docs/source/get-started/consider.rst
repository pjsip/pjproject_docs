General guidelines
*****************************************

Development guidelines
======================

Preparation
------------
* **Essential:** Familiarise yourself with SIP. While there is no need to be an expert, 
  some SIP knowledge is essential. 
* Check out the features in :doc:`Features/Datasheet </overview/features>`.
* Familiarize with the structure of https://docs.pjsip.org. All documentations
  are hosted here.


Development
-------------
* **Essential:** Follow the :doc:`Getting Started </get-started/getting>`
  instructions to build PJSIP for your platform.
* **Essential:** Interactive debugging capability is essential during development
* Start with default settings in 
  `config_site_sample.h <https://github.com/pjsip/pjproject/blob/master/pjlib/include/pj/config_site_sample.h>`_. 
  One way is to include this in your ``config_site.h``, i.e.:

  .. code-block:: c

        #include <pj/config_site_sample.h>

  The default settings should be good to get you started. You can always optimize later after 
  things are running okay.


Coding Style
-------------
**Essential:** set your editor to use 8 characters tab size in order to see PJSIP source correctly.

Detailed below is the PJSIP coding style. You don't need to follow it unless you are submitting 
patches to PJSIP:

* Indentation uses tabs and spaces. Tab size is 8 characters, indentation 4.
* All public API in header file must be documented in Doxygen format.
* Apart from that, we mostly just use `K & R style <http://en.wikipedia.org/wiki/1_true_brace_style#K.26R_style>`_, 
  which is the only correct style anyway.

.. note::

   We are in the process of changing the indentation style to use only spaces.


Deployment
-----------
* **Essential:** Logging is essential when troubleshooting any problems. The application MUST be 
  equipped with logging capability. Enable PJSIP log at level 5.


Platform Consideration
========================
Platform selection is usually driven by business motives. The selection will affect all aspects of 
development, and this section will try to cover considerations for each platforms that PJSIP supports.

Windows Desktop
----------------
Windows is supported from Windows 2000 up to the recent Windows 10 and beyond. All features are expected 
to work. 64bit support was added recently. Development is based on Visual Studio. Considerations for 
this platform include:

#. Because Visual Studio file format keeps changing on every release, we decided to support Visual Studio
   2015. Newer VS should be able to open the projects.


MacOS X
-------
All features are expected to work. Considerations include:

#. Development with XCode is currently not supported. This is **not** to say that you cannot use XCode, 
   but PJSIP only provides basic Makefiles and if you want to use XCode you'd need to arrange the project 
   yourself.
#. Mac systems typically provides very good sound device, so we don't expect any problems with audio 
   on Mac. 


Linux Desktop
-------------
All features are expected to work. Linux considerations:

#. Use our native ALSA backend instead of PortAudio because ALSA has less jitter than OSS and our backend 
   is more lightweight than PortAudio


iOS for iPhone, iPad, and other Apple devices
---------------------------------------------------
All features are expected to work. Considerations for iOS:

#. You need to use TCP transport for SIP for the background feature to work
#. IP change (for example when user is changing access point) is a feature frequently asked by developers 
   and you can find the documentation in :doc:`Guide to IP Address Change </specific-guides/network_nat/ip_change>`
#. If SSL is needed, native Mac OS/iOS SSL backend is available. See our :ref:`SSL Guide <guide_ssl>`


Android
-------
All features are expected to work. Considerations for Android:

#. You can use PJSUA2 Java binding or C# binding (using Xamarin) for this target.
#. It has been reported that Android audio device is not so good in general, so some audio tuning may be 
   needed. Echo cancellation also needs to be checked.


Symbian
-------
.. note::

   Symbian is no longer supported

Symbian has been supported for a long time. In general all features (excluding video) are expected to 
work, but we're not going to do Symbian specific development anymore. Other considerations for Symbian:

#. The MDA audio is not very good (it has high latency), so normally you'd want to use Audio Proxy 
   Server (APS) or VoIP Audio Service (VAS) for the audio device, which we support. Using these audio backends will also provide us with high quality echo cancellation as well as low bitrate codecs such as AMR-NB, G.729, and iLBC. But VAS and APS requires purchase of Nokia development certificate to sign the app, and also since APS and VAS only run on specific device type, you need to package the app carefully and manage the deployment to cover various device types.


BlackBerry 10
-------------
.. note::

   BB10 is no longer supported

BlackBerry 10 (BB10) is supported since PJSIP version 2.2. Some considerations for BB10 platform include:

#. IP change (for example when user is changing access point) is a feature frequently asked by developers 
   and you can find the documentation in :doc:`Guide to IP Address Change </specific-guides/network_nat/ip_change>`


Windows Mobile
--------------
This is the old Windows Mobile platform that is based on WinCE. This platform has been supported for a 
long time. We expect all features except video to work, but there may be some errors every now and then 
because this target is not actively maintained. No new development will be done for this platform.

Other considerations for Windows Mobile platform are:

#. The quality of audio device on WM varies a lot, and this affects audio latency. Audio latency could go 
   as high as hundreds of millisecond on bad hardware.
#. Echo cancellation could be a problem. We can only use basic echo suppressor due to hardware limitation, 
   and combined with bad quality of audio device, it may cause ineffective echo cancellation. This could be 
   mitigated by setting the audio level to low.


Windows Phone 10 (UWP)
--------------------------
Windows Phone 10/Universal Windows Platform (UWP) support has being added in version 2.6. 
Specific considerations for this platform are:

#. WP8 governs specific interaction with WP8 GUI and framework that needs to be followed by application 
   in order to make VoIP call work seamlessly on the device. Some lightweight process will be created by 
   WP8 framework in order for background call to work and PJSIP needs to put its background processing in 
   this process' context. Currently this feature is under development.



Embedded Linux
--------------
In general embedded Linux support is similar to Linux and there should be no problems with it. 
There may be some specific considerations for embedded Linux as follows:

#. The performance of the audio device is probably the one with most issues, as some development boards 
   does not have a decent sound device. Typically there is high audio jitter (or burst) and latency. 
   This will affect end to end audio latency and also the performance of the echo canceller. Also we 
   found that ALSA generally works better than OSS, so if you can have ALSA up and running that will be 
   better. Use the native ALSA backend audio device instead of PortAudio since it is simpler and lighter.


QNX or Other Posix Embedded OS
------------------------------
This is not part of our officially supported OS platforms, but users have run PJSIP on QNX and 
BlackBerry 10 is based on QNX too. Since QNX provides Posix API, and maybe by using the settings found 
in the ``configure-bb10 script``, PJSIP should be able to run on it, but you need to develop PJMEDIA 
sound device wrapper for your audio device. Other than this, we don't have enough experience to comment 
on the platform. 


Other Unix Desktop OSes
-----------------------
Community members, including myself, have occasionally run PJSIP on other Unix OSes such as Solaris, 
FreeBSD, and OpenBSD. We expect PJSIP to run on these platforms (maybe with a little kick). However,
the sound device most likely will be limited to OSS, which is provided by PortAudio.


Porting to Other Embedded OS
------------------------------
It is possible to port PJSIP to other embedded OS or even directly to device without OS and people 
have done so. In general, the closer resemblance the new OS to existing supported OS, the easier 
the porting job will be. The good thing is, PJSIP has been made to be very very portable, and system 
dependent features are localized in PJLIB and PJMEDIA audio device, so the effort is more quantifiable. 
Once you are able to successfully run *pjlib-test*, you are more or less done with your porting effort. 
Other than that, if you really want to port PJSIP to new platform, you probably already know what 
you're doing. 



Which API to Use
================
Let's have a look at the libraries architecture again:

.. raw:: html
    :file: ../overview/architecture.svg

PJSIP, PJMEDIA, and PJNATH Level
--------------------------------
At the lowest level we have the individual **C** libraries, which 
consist of :doc:`PJSIP </api/pjsip/index>`, :doc:`PJMEDIA </api/pjmedia/index>`, and 
:doc:`PJNATH </api/pjnath/index>`, with :doc:`PJLIB-UTIL </api/pjlib-util/index>` and 
:doc:`PJLIB </api/pjlib/index>` as support libraries. This level provides the most flexibility, but 
it's also the hardest to use. The only reason you'd want to use this level is if:

#. You only need the individual library (say, PJNATH)
#. You need to be very very tight in footprint (say when things need to be measured in Kilobytes instead 
   of Megabytes)
#. You are **not** developing a SIP client

Use the corresponding :doc:`PJSIP </api/pjsip/index>`, :doc:`PJMEDIA </api/pjmedia/index>`, and 
:doc:`PJNATH </api/pjnath/index>` manuals and :doc:`samples </api/samples>` for information on how
to use the libraries. 


PJSUA-LIB API
-------------
Next up is :doc:`PJSUA-LIB API </api/pjsua-lib/index>` that combines all those libraries into a 
high level, integrated client user agent library written in **C**. This is the library that most 
PJSIP users use, and the highest level abstraction before PJSUA2 was created. 

Motivations for using PJSUA-LIB library include:

#. Developing client application (PJSUA-LIB is optimized for developing client app)
#. Better efficiency than higher level API


PJSUA2 C++ API
--------------
:doc:`PJSUA2 API </api/pjsua2/index>` is an objected oriented, C++ API created on top of PJSUA-LIB. 
The API is different than PJSUA-LIB, but it should be even easier to use and it should have better 
documentation too (see :doc:`PJSUA2 Guide </pjsua2/index>`). The PJSUA2 API removes most cruxes 
typically associated with PJSIP, such as :ref:`the pool <pjlib_pool>` and :ref:`pj_str_t <pjlib_string>`, 
and adds new features such as object persistence so you can save your configs to JSON file, for example. 
All data structures are rewritten for more clarity. 

A C++ application can use PJSUA2 natively, while at the same time still has access to the lower level 
**C** objects if it needs to. This means that the C++ application should not lose any information from 
using the C++ abstraction, compared to if it is using PJSUA-LIB directly. The C++ application also 
should not lose the ability to extend the library. It would still be able to register a custom PJSIP module, 
pjmedia_port, pjmedia_transport, and so on.

Benefits of using PJSUA2 C++ API include:

#. Cleaner object oriented API
#. Uniform API for higher level language such as Java, Python, and C#
#. Persistence API
#. The ability to access PJSUA-LIB and lower level libraries when needed (including the ability to extend 
   the libraries, for example creating custom PJSIP module, pjmedia_port, pjmedia_transport, etc.)


Some considerations on PJSUA2 C++ API are:

#. Instead of returning error, the API uses exception for error reporting
#. It uses standard C++ library (STL)
#. The performance penalty due to the API abstraction should be negligible on typical modern device



PJSUA2 API for Java, Python, C#, and Others
------------------------------------------------
The PJSUA2 API is also available for non-native code via SWIG binding. Configurations for Java, Python, and 
C# are provided with the distribution. See :doc:`Building PJSUA2 </pjsua2/building>` section for more
information. Thanks to SWIG, other language bindings may be generated relatively easily in the future.
 
The PJSUA2 API for non-native code is effectively the same as PJSUA2 C++ API. You can peek at the 
:doc:`Hello world </pjsua2/hello_world>` section to see how these look like. However, unlike C++, 
you cannot access PJSUA-LIB and the underlying C libraries from the scripting language, hence you are 
limited to what pjsua2 provides. 

You can use this API if native application development is not available in target platform (such as Android), 
or if you prefer to develop with non-native code instead of C/C++.



Other specific considerations
=========================================
At this point, the best way to move forward is to just try it! We'll go next to the **Getting Started** 
instructions. If you encounter issues, have a look at the **SPECIFIC GUIDES** section of the menu to 
see if the topics are covered.

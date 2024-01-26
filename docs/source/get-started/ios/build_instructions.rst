Build Instructions
===================

.. contents:: Table of Contents
    :depth: 3


Requirements
-------------

* iOS SDK, part of Xcode.
* **Command Line Tools** for Xcode: download from `Apple Developer Downloads <https://developer.apple.com/downloads/index.action>`__ 
  then install.

Build Preparation
------------------

#. :doc:`Getting the source code </get-started/getting>` if you haven't already.
#. Set your :ref:`config_site.h` to the following:

   .. code-block:: c

      #define PJ_CONFIG_IPHONE 1
      #include <pj/config_site_sample.h>

  This will activate iPhone specific settings in the :source:`pjlib/include/pj/config_site_sample.h`.

Building PJSIP
---------------

Just run:

.. code-block:: shell

   $ cd /path/to/your/pjsip/dir
   $ ./configure-iphone
   $ make dep && make clean && make

Open ``ipjsua.xcodeproj`` using Xcode in :source:`pjsip-apps/src/pjsua/ios`. 
If you enable video and use libyuv/libopenh264, add the libraries into the application. 
Build the project and run. 

You will see telnet instructions on the device's screen. Telnet to this address to 
operate the application. 
See :doc:`CLI Manual </specific-guides/other/cli_cmd>` for commands available.

.. note::

   * The ``./configure-iphone`` is a wrapper that calls the standard ``./configure`` 
     script with settings suitable for iPhone target.
   * The latest iPhone SDK version will be selected by default. You may change 
     this by setting ``IPHONESDK`` environment variable to the desired SDK path. 
     For ipjsua, select Project-Edit Project Settings-Base SDK and Targets-ipjsua-Get 
     Info-Base SDK to change the SDK version.
   * You may pass standard ``./configure`` options to this script too.
   * For more info, run ``./configure-iphone --help``
   * Other customizations are similar to what is explained in 
     :doc:`Building with GNU </get-started/posix/build_instructions>` page.

Supporting multiple architectures (e.g. armv7, arm64)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to compile separately for each architecture by setting ``ARCH`` environment 
variable to the desired architecture before running ``configure-iphone``.
For example:

.. code-block:: shell

   export ARCH="-arch arm64"

Setting minimum supported iOS version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to specify the minimum supported iOS version, you can set ``MIN_IOS`` 
environment variable before running ``configure-iphone``, for example:

.. code-block:: shell

   export MIN_IOS="-miphoneos-version-min=8.0"

The default setting is iOS 7.0. If you don't want to specify this flag, you can 
set ``MIN_IOS`` to a single space instead (``export MIN_IOS=" "``) 

.. note:: 

   If you don't set the minimum iOS version, you may encounter linker warning in 
   your XCode app, which may lead to crashes when running on older iOS versions

.. code-block:: shell

   ld: warning: object file (...) was built for newer iOS version (10.0) than being linked (7.0)

Simulator
^^^^^^^^^

To configure the build system for the iPhone simulator:

.. code-block:: shell

   export DEVPATH=/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer
   # arm64 simulator
   ARCH="-arch arm64" CFLAGS="-O2 -m64" LDFLAGS="-O2 -m64" MIN_IOS="-mios-simulator-version-min=13.0" ./configure-iphone
   # x86_64 simulator
   ARCH="-arch x86_64" CFLAGS="-O2 -m64" LDFLAGS="-O2 -m64" MIN_IOS="-mios-simulator-version-min=13.0" ./configure-iphone
   # or 32-bit
   ARCH="-arch i386" CFLAGS="-O2 -m32" LDFLAGS="-O2 -m32" MIN_IOS="-mios-simulator-version-min=13.0" ./configure-iphone 
   make dep && make clean && make

.. note::
   
   The exact paths may vary according to your SDK version.

Creating a framework to support multiple platforms and architectures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each platform you wish to support, you can combine the PJSIP libraries that were built for different architectures using the **lipo** command:

.. code-block:: shell

   # For each architecture, combine the PJSIP libraries into one
   libtool -static -o [arch]/libPJSIP.a pjsip-apps/src/pjsua/ios/*.a

   # For each platform, combine all the architectures
   # Combine iOS armv7 and arm64 build
   lipo -arch armv7 ios-armv7/libPJSIP.a -arch arm64 ios-arm64/libPJSIP.a -create -output ios/libPJSIP.a
   # Combine iOS Simulator x86_64 and arm64 build
   lipo -arch x86_64 sim-x86_64/libPJSIP.a -arch arm64 sim-arm64/libPJSIP.a -create -output sim/libPJSIP.a
   # Combine MacOS x86_64 and arm64 build
   lipo -arch x86_64 mac-x86_64/libPJSIP.a -arch arm64 mac-arm64/libPJSIP.a -create -output mac/libPJSIP.a


Next, you bundle the resulting libraries above into an `XCFramework <https://developer.apple.com/documentation/xcode/creating-a-multi-platform-binary-framework-bundle#Generate-the-XCFramework-bundle>`__:

.. code-block:: shell

   # Delete any existing framework
   rm -rf libPJSIP.xcframework
   # Put all PJSIP headers into one directory [path_to_PJSIP_headers]
   # Create binary framework for iOS, iOS Simulator, and MacOS
   xcodebuild -create-xcframework -library ios/libPJSIP.a -headers [path_to_PJSIP_headers] -library sim/libPJSIP.a -headers [path_to_PJSIP_headers] -library mac/libPJSIP.a -headers [path_to_PJSIP_headers] -output libPJSIP.xcframework

As a result, you will get a binary framework with the name ``libPJSIP.xcframework`` that contains the directories ``ios-arm64_armv7``, ``ios-arm64_x86_64-simulator``, and ``macos-arm64_x86_64``.

Bitcode
^^^^^^^^

To enable bitcode, use the following steps:

#. In running the configure script, add ``-fembed-bitcode`` to ``CFLAGS``, 
   e.g: ``CFLAGS=-fembed-bitcode ./configure-iphone``.
#. Run ``make``.
#. In XCode, ipjsua -> Build Settings, Search "bitcode" -> set "Enable Bitcode" 
   to "Yes".
#. Build.

.. note:: 

   Any third-party dependencies, e.g: OpenSSL, will need to be built with 
   bitcode enabled too.

Using PJSIP in your application
-------------------------------

To use PJSIP in your application, you need to:

* Add the required libraries and frameworks. One way to do this is by drag-and-dropping 
  the libraries and frameworks from our sample app. 
  Then add the library and header search paths in "Build Settings".
* Add the required permissions for camera (if you need video calls) and 
  microphone usages.
* Define ``PJ_AUTOCONF=1`` in your Xcode's project config.

PJSIP in Swift application
^^^^^^^^^^^^^^^^^^^^^^^^^^

For Swift app, you need to create a bridging header (click File-New-Objective-C 
File, and click Yes when asked to create a bridging header). 
In the bridging header file, add all the C headers that you need, 
for example: ``#import <PJSIP/pjsua.h>``. 
You can then directly call any PJSIP C API declared in those headers. 

Please check ``ipjsua-swift.xcodeproj`` located in
:source:`pjsip-apps/src/pjsua/ios-swift` for an example.

If you want to use C++ API such as PJSUA2 however, you need to create your own 
Objective-C wrapper. For a sample pjsua2-Swift app, please check :source:`pjsip-apps/src/pjsua2/ios-swift-pjsua2`.

.. note:: 

   The Swift sample apps require video support.

Video Support
-------------

Features
^^^^^^^^
Some of the highlighted features include:

* :ref:`native capture <avfoundation>`
* :ref:`native preview <avfoundation>`
* :ref:`native OpenGL ES renderer <opengl>`
* :ref:`native H.264 <videotoolbox>` or via :ref:`openh264` (see below)

Requirements
^^^^^^^^^^^^

libyuv
``````

#. If you are using 2.5.5 or newer, libyuv should be built and enabled 
   automatically, see :pr:`1937` for more info.
#. If you are using 2.5.1 or older, follow the instructions in :pr:`1776`.

.. _videotoolbox:

OpenH264 or **VideoToolbox** (if you need H264 codec, choose one of them)
``````````````````````````````````````````````````````````````````````````

* For OpenH264, see :ref:`openh264`
* For **VideoToolbox** (supported since PJSIP version 2.7), define this in 
  your ``config_site.h``:

  .. code-block:: c

     #define PJMEDIA_HAS_VID_TOOLBOX_CODEC 1

libvpx (if you need VP8 or VP9 codec)
`````````````````````````````````````

See See :ref:`libvpx`

Configuring
^^^^^^^^^^^^

Sample invocation of ``./configure-iphone``:

.. code-block:: shell

   $ ./configure-iphone --with-openh264=/Users/me/opt

If you use openh264, make sure it is detected by ``./configure-iphone``:

.. code-block::shell

   ...
   Using OpenH264 prefix... /Users/me/opt
   checking OpenH264 availability... ok
   ...

Set these in your :ref:`config_site.h`:

.. code-block:: c

   #define PJ_CONFIG_IPHONE 			1
   #define PJMEDIA_HAS_VIDEO			1

   #include <pj/config_site_sample.h>

Video capture orientation support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To send video in the proper orientation (i.e. head always up regardless of the 
device orientation), application needs to do the following:

#. Setup the device to get orientation change notification 
   (by calling the API ``UIDevice.beginGeneratingDeviceOrientationNotifications`` 
   and add a callback to receive ``UIDeviceOrientationDidChangeNotification``).
#. Inside the callback, call PJSUA API

.. code-block:: c

   pjsua_vid_dev_set_setting(dev_id, PJMEDIA_VID_DEV_CAP_ORIENTATION, &new_orientation, PJ_TRUE)
 
to set the video device to the correct orientation.

For sample usage, please refer to :source:`ipjsuaAppDelegate.m <pjsip-apps/src/pjsua/ios/ipjsua/ipjsuaAppDelegate.m>`. 
Ticket :pr:`1861` explains this feature in detail.

.. _ios_openssl:

TLS/OpenSSL Support
-------------------

Native TLS backend for iOS and MacOS, i.e: using Network framework, is supported, 
please check :pr:`2482` for more info. Note that currently this backend is still in experimental phase.

Alternatively, using OpenSSL backend is also supported. Follow the instructions 
below to enable TLS transport by using OpenSSL:

#. Build and install OpenSSL-1.1.x, please check this 
   `OpenSSL wiki <https://wiki.openssl.org/index.php/Compilation_and_Installation#iOS>`__. 
   For example, to build for arm64 architecture:

   .. code-block:: shell
 
      export CROSS_TOP=/Applications/XCode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/
      export CROSS_SDK=iPhoneOS11.3.sdk
      export CC="/Applications/XCode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang -arch arm64"
      ./Configure iphoneos-cross --prefix=/Users/teluu/openssl-1.1.0f-iphone64/arm64
      make
      make install

   And check that OpenSSL is detected by the configure script:

   .. code-block::

      ...
      checking for OpenSSL installations..
      checking openssl/ssl.h usability... yes
      checking openssl/ssl.h presence... no
      aconfigure: WARNING: openssl/ssl.h: accepted by the compiler, rejected by the preprocessor!
      aconfigure: WARNING: openssl/ssl.h: proceeding with the compiler's result
      checking for openssl/ssl.h... yes
      checking for ERR_load_BIO_strings in -lcrypto... yes
      checking for SSL_library_init in -lssl... yes
      OpenSSL library found, SSL support enabled
      ...

#. Build the libraries:

   .. code-block:: shell

      make dep && make
 
#. In XCode project setting of your application (for example, ipjsua),
   add **libssl.a** and **libcrypto.a** from OpenSSL ARM directory to the 
   project's Libraries:

   #. In ``Group & Files`` pane, expand ``ipjsua``, then right click ``Libraries``, 
      and select ``Add -> Existing Files...``.
   #. Find ``libssl.a`` and ``libcrypto.a`` from OpenSSL ARM directory 
      (for example, ``${HOME}/openssl/openssl_arm``) and add them to the project.

#. Build the app

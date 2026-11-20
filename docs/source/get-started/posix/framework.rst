PJSIP XCFramework (macOS)
=======================================

``PJSIP.xcframework`` is PJSIP prebuilt for Apple platforms: one file that an Xcode application
adds, instead of building PJSIP itself. It holds static libraries for macOS (arm64 and x86_64),
iOS and the iOS simulator, with their headers, so the same framework serves a Mac and an iOS
application. For iOS, see :doc:`/get-started/ios/framework`.

Its configuration is fixed. To choose the codecs, backends or third party libraries yourself,
build PJSIP with :doc:`build_gnu` or :doc:`build_cmake` instead.

.. note::

   Available since release 2.18.


.. contents:: Steps:
   :depth: 2
   :local:


What it contains
-----------------------------------
* TLS through Apple's Network framework, so no OpenSSL is needed.
* Opus, G.711, G.722, GSM, Speex and iLBC audio codecs.
* Video, with H.264 through VideoToolbox as the only video codec, AVFoundation capture and Metal
  rendering.
* The C API (PJSUA and below), and the :doc:`PJSUA2 </api/pjsua2/index>` C++ API.

It requires macOS 11.0 or later.

Not included: DTLS-SRTP (SDES-SRTP is), the WebRTC echo canceller, AMR, G.729, and the other video
codecs. :source:`build/apple/README.md` lists the configuration and the reasons.


Get the framework
-----------------------------------
Starting from release 2.18, the framework is attached to each release on the
`PJSIP GitHub releases page <https://github.com/pjsip/pjproject/releases>`__, and can be added to
a project in three ways.

**Swift Package Manager.** In Xcode, *File* > *Add Package Dependencies*, with the pjproject
repository URL, ``https://github.com/pjsip/pjproject``, and add the ``PJSIP`` product. In a
``Package.swift``:

.. code-block:: swift

   .package(url: "https://github.com/pjsip/pjproject", from: "2.18.0")

The system frameworks it needs are linked automatically.

**CocoaPods.** The pod is not in the CocoaPods index, so point at the podspec attached to the
release:

.. code-block:: ruby

   pod 'PJSIP', :podspec =>
     'https://github.com/pjsip/pjproject/releases/download/<version>/PJSIP.podspec'

**Manually.** Download ``PJSIP.xcframework.zip`` from the release, unzip it, and continue with
:ref:`posix_framework_use`.


Build the framework
-----------------------------------
Alternatively, to build the framework yourself, :source:`build/apple/build-xcframework.sh` builds
PJSIP with CMake for each platform and packages the result. It needs Xcode, CMake 3.28 or newer,
and network access on the first run, to download Opus:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ ./build/apple/build-xcframework.sh

The framework is written to ``out/dist/PJSIP.xcframework``.

.. tip::

   * ``SLICES=macos`` builds only the macOS part, in a few minutes.
   * The script needs Xcode itself, not only its command line tools. If ``xcode-select -p`` shows
     ``/Library/Developer/CommandLineTools``, run it with
     ``DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer``.
   * The script uses its own configuration and ignores ``config_site.h``. It refuses to run in a
     tree configured with ``./configure``; run ``make distclean`` first.
   * :source:`build/apple/tests/verify-xcframework.sh` checks the result.
   * See :source:`build/apple/README.md` for all the settings.


.. _posix_framework_use:

Use the framework in an application
-----------------------------------
With Swift Package Manager or CocoaPods, the framework is set up already. Otherwise:

#. Drag ``PJSIP.xcframework`` into the Xcode project, and in the target's *General* tab, under
   *Frameworks, Libraries, and Embedded Content*, set it to **Do Not Embed**: it holds static
   libraries.
#. Add these frameworks to the same list: AVFoundation, AudioToolbox, CoreAudio, CoreGraphics,
   CoreMedia, CoreVideo, Foundation, AppKit, Metal, MetalKit, Network, QuartzCore, Security and
   VideoToolbox.
#. Add ``-lc++`` to *Other Linker Flags* in the target's *Build Settings*.

Then, for every application:

* Add ``NSMicrophoneUsageDescription`` and ``NSCameraUsageDescription`` to its ``Info.plist``;
  macOS asks the user for access with these texts.
* With the App Sandbox, enable *Incoming Connections (Server)*, *Outgoing Connections (Client)*,
  *Audio Input* and *Camera*.

Objective-C and C use the headers as usual, e.g. ``#include <pjsua.h>``, and Swift with
``import PJSIP``. PJSUA2 is C++, so it is usable from Objective-C++ (``.mm``) and C++ sources only.

.. tip::

   PJSIP functions may only be called from threads that PJSIP knows. Register any other thread,
   e.g. the main thread when PJSIP was started from another one, with ``pj_thread_register()`` before calling them. See
   :doc:`/specific-guides/develop/init_shutdown_thread`.

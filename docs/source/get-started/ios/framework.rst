PJSIP XCFramework (iOS)
=======================================

``PJSIP.xcframework`` is PJSIP prebuilt for iOS: one file that an Xcode application adds,
instead of building PJSIP itself. It holds static libraries for iOS (arm64) and the iOS simulator
(arm64 and x86_64), with their headers. For macOS applications, see
:doc:`/get-started/posix/framework`.

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
* Video, with H.264 through VideoToolbox as the only video codec, AVFoundation capture, and Metal
  and OpenGL ES rendering.
* Echo cancellation from CoreAudio.
* The C API (PJSUA and below), and the :doc:`PJSUA2 </api/pjsua2/index>` C++ API.

It requires iOS 15.0 or later.

Not included: DTLS-SRTP (SDES-SRTP is), the Speex and WebRTC echo cancellers, AMR, G.729, and the
other video codecs. :source:`build/apple/README.md` lists the configuration and the reasons.


Get the framework
-----------------------------------
Starting from release 2.18, the framework is attached to each release on the
`PJSIP GitHub releases page <https://github.com/pjsip/pjproject/releases>`__, and can be added to
a project in two ways.

**CocoaPods.** The pod is not in the CocoaPods index, so point at the podspec attached to the
release:

.. code-block:: ruby

   pod 'PJSIP', :podspec =>
     'https://github.com/pjsip/pjproject/releases/download/<version>/PJSIP.podspec'

**Manually.** Download ``PJSIP.xcframework.zip`` from the release, unzip it, and continue with
:ref:`ios_framework_use`.


Build the framework
-----------------------------------
Alternatively, to build the framework yourself, :source:`build/apple/build-xcframework.sh` builds
PJSIP with CMake for each platform and packages the result. It needs Xcode, CMake 3.28 or newer,
and network access on the first run, to download Opus. To build it for iOS:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ SLICES="ios-device ios-simulator" ./build/apple/build-xcframework.sh

The framework is written to ``out/dist/PJSIP.xcframework``.

.. tip::

   * The script needs Xcode itself, not only its command line tools. If ``xcode-select -p`` shows
     ``/Library/Developer/CommandLineTools``, run it with
     ``DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer``.
   * The script uses its own configuration and ignores ``config_site.h``. It refuses to run in a
     tree where ``./configure-iphone`` or a :doc:`CMake build <build_cmake>` has left the generated
     headers; use a clean checkout. After ``./configure-iphone``, ``make distclean`` also works.
   * :source:`build/apple/tests/verify-xcframework.sh` checks the result.
   * See :source:`build/apple/README.md` for all the settings.


.. _ios_framework_use:

Use the framework in an application
-----------------------------------
With CocoaPods, the framework is set up already. Otherwise:

#. Drag ``PJSIP.xcframework`` into the Xcode project, and in the target's *General* tab, under
   *Frameworks, Libraries, and Embedded Content*, set it to **Do Not Embed**: it holds static
   libraries.
#. Add these frameworks to the same list: AVFoundation, AudioToolbox, CoreGraphics, CoreMedia,
   CoreVideo, Foundation, Metal, MetalKit, Network, OpenGLES, QuartzCore, Security, UIKit and
   VideoToolbox.
#. Add ``-lc++`` to *Other Linker Flags* in the target's *Build Settings*.

Unlike with libraries built from source, no header search paths and no ``PJ_AUTOCONF``
definition are needed: the framework's headers carry the configuration it was built with.

Then, for every application:

* Add ``NSMicrophoneUsageDescription`` and ``NSCameraUsageDescription`` to its ``Info.plist``;
  iOS asks the user for access with these texts.
* For calls that continue in the background, enable the *Audio* and *Voice over IP* background
  modes.

Objective-C and C use the headers as usual, e.g. ``#include <pjsua-lib/pjsua.h>`` or
``#include <pjsua.h>``, and Swift with ``import PJSIP``. PJSUA2 is C++, so it is usable from
Objective-C++ (``.mm``) and C++ sources only.

.. tip::

   PJSIP functions may only be called from threads that PJSIP knows. Register any other thread,
   e.g. the main thread when PJSIP was started from another one, with ``pj_thread_register()``
   before calling them. See :doc:`/specific-guides/develop/init_shutdown_thread`.


Using the framework in the ipjsua sample
-----------------------------------------
The ``ipjsua`` sample in :source:`pjsip-apps/src/pjsua/ios` links the libraries of a source build.
To build it with the framework instead, in a copy of the ``pjsua`` directory (``ipjsua`` also
compiles the ``pjsua_app*.c`` files next to ``ios``):

#. Remove the ``lib*.a`` libraries from the target's *Frameworks, Libraries, and Embedded
   Content*.
#. Add ``PJSIP.xcframework`` as above. The system frameworks are already in the project.
#. In *Build Settings*, remove the pjproject directories from *Header Search Paths* (keep ``..``,
   for ``pjsua_app.h``), remove ``PJ_AUTOCONF=1`` from *Preprocessor Macros*, and add ``-lc++`` to
   *Other Linker Flags*.

Its configuration is then the framework's. For example, the ``config_site.h`` settings of
:doc:`build_gnu` no longer apply.

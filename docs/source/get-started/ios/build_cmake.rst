Build with CMake
=======================================

This page builds PJSIP for iOS and the iOS simulator with CMake. The result is the same as
:doc:`build_gnu`, and the sample applications use it the same way.

.. note::

   Supported since release 2.18. See :doc:`/get-started/cmake/index` for CMake in general.


.. contents:: Configuration and build steps:
   :depth: 2
   :local:


Requirements
-----------------------------------
* **Xcode**, with the iOS SDK. Its command line tools alone are not enough: they have no iOS SDK.
* **CMake 3.28** or newer, from `cmake.org <https://cmake.org/download/>`__ or Homebrew
  (``brew install cmake``). Check with ``cmake --version``.

.. tip::

   If ``xcode-select -p`` shows ``/Library/Developer/CommandLineTools``, configure stops with
   ``iphoneos is not an iOS SDK``. Select Xcode with
   ``sudo xcode-select -s /Applications/Xcode.app``, or prefix the ``cmake`` commands with
   ``DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer``.


Create *config_site.h*
-----------------------------------
Create :ref:`pjlib/include/pj/config_site.h <dev_start>` file with a text editor and set the
contents to the following:

.. code-block:: c

   /* Activate iPhone specific settings in the 'config_site_sample.h' */
   #define PJ_CONFIG_IPHONE 1
   #include <pj/config_site_sample.h>

This is the same as for :doc:`build_gnu`. Video and the VideoToolbox H.264 codec are on by default
with CMake, so ``PJMEDIA_HAS_VIDEO`` and ``PJMEDIA_HAS_VID_TOOLBOX_CODEC`` are not needed.

.. warning::

   Note that settings in *config_site.h* can clash with CMake options, and silently override them,
   so changing the option later can cause link errors. For anything that has a CMake option, such
   as video, use the option rather than *config_site.h*. See
   :ref:`config_site.h with CMake <cmake_config_site>`.


Configuring PJSIP
---------------------------------
For a device:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ cmake -B build-ios -DCMAKE_SYSTEM_NAME=iOS

``-DCMAKE_SYSTEM_NAME=iOS`` builds for iOS with the Xcode toolchain; no toolchain file is needed.
The architecture is arm64, and the minimum iOS version is 15.0 (see
:ref:`ios_cmake_min_ios`).

Core Audio, AVFoundation capture, Metal and OpenGL ES rendering, and the VideoToolbox H.264 codec
are on by default. TLS is off unless enabled as in :ref:`ios_cmake_tls`.

.. tip::

   * Each build directory holds one configuration: one SDK, one deployment target.
   * Without ``CMAKE_BUILD_TYPE``, the libraries are built with ``-O2``. Add
     ``-DCMAKE_BUILD_TYPE=Debug`` for a debug build, or ``Release`` for ``-O3``.
   * ``-G Xcode`` generates an Xcode project instead of Makefiles.
   * More options, such as disabling a codec, are in :doc:`/get-started/cmake/options`.
   * Everyday CMake commands are in :doc:`/get-started/cmake/build_instructions`.

Configuring for the simulator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use a build directory of its own, with the simulator SDK and the architecture of the Mac:

.. code-block:: shell

   $ cmake -B build-ios-sim -DCMAKE_SYSTEM_NAME=iOS -DCMAKE_OSX_SYSROOT=iphonesimulator \
         -DCMAKE_OSX_ARCHITECTURES=arm64

``"-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64"`` builds both simulator architectures in one pass,
into fat libraries. The bundled WebRTC echo canceller cannot be built that way and is left out,
with a ``[!]`` line in the configure output.

.. _ios_cmake_min_ios:

Setting minimum supported iOS version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the libraries support iOS 15.0 or later, the oldest version the current Xcode supports
and the one the sample applications use. To specify another minimum iOS version, set
``CMAKE_OSX_DEPLOYMENT_TARGET``, for example:

.. code-block:: shell

   $ cmake -B build-ios -DCMAKE_SYSTEM_NAME=iOS -DCMAKE_OSX_DEPLOYMENT_TARGET=16.0

The same applies to the simulator.

To change it in an existing build directory, delete the directory, or add ``--fresh`` to the
``cmake`` command. Configure stops with an error otherwise:

.. code-block::

   CMAKE_OSX_DEPLOYMENT_TARGET changed from "15.0" to "16.0" in a build folder
   configured for the former; its cached configure checks and library paths
   would be wrong.  Reconfigure with 'cmake --fresh' or use a new build
   folder.

.. note::

   Set the application's minimum iOS version to the libraries' or higher. Otherwise you may
   encounter linker warnings in your Xcode app, which may lead to crashes when running on the
   older iOS versions:

   .. code-block:: shell

      ld: warning: object file (...) was built for newer 'iOS' version (16.0) than being linked (15.0)

.. _ios_cmake_tls:

Configuring TLS support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Either use Apple's Network framework, which needs no other library:

.. code-block:: shell

   $ cmake -B build-ios ... -DPJLIB_WITH_SSL=apple

It does not support DTLS-SRTP. Or use OpenSSL built for iOS, as described in :ref:`ios_openssl`:

.. code-block:: shell

   $ cmake -B build-ios ... -DPJLIB_WITH_SSL=openssl -DOPENSSL_ROOT_DIR=/path/to/openssl-ios

``-DPJLIB_WITH_SSL=openssl`` makes configure fail if OpenSSL cannot be used, rather than building
without TLS. As with :doc:`build_gnu`, add ``libssl.a`` and ``libcrypto.a`` to the application.

Other libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Other libraries built for iOS are found the same way, from their ``<Package>_ROOT``, e.g.
``-DOPUS_ROOT=...`` or ``-DOpenH264_ROOT=...``. Build them for the same SDK and architectures,
and add them to the application. See :source:`build/apple/README.md` for how the roots are
searched.


Verifying configuration
---------------------------------
Check that all the intended features are detected by observing the configure output, for example:

.. code-block::

   -- [pjlib] SSL backend: apple
   -- [pjmedia] Checking if CoreAudio is available - yes (PJMEDIA_WITH_AUDIODEV_COREAUDIO)
   -- [pjmedia] Checking if VideoToolbox is available - yes (PJMEDIA_WITH_VID_TOOLBOX_CODEC)

A feature whose library is not found is switched off and configure carries on; look for lines
starting with ``-- [!]``. Lines saying that the iOS sample projects get an empty archive in place
of a library, e.g. ``libg7221codec.a``, are expected: that library is not part of this
configuration.


Building PJSIP
---------------------------------
Now we can build PJSIP with:

.. code-block:: shell

   $ cmake --build build-ios -j

This builds the libraries, in ``build-ios/<module>/lib``, and links them into the sample
applications in :source:`pjsip-apps/src/pjsua/ios`, :source:`pjsip-apps/src/pjsua/ios-swift` and
:source:`pjsip-apps/src/pjsua2/ios-swift-pjsua2`, as :doc:`build_gnu` does. It also copies the
headers it generates into the source tree, where the sample projects include them from.
``-DPJ_IOS_SAMPLE_LIBS=OFF`` leaves the source tree alone.

The command line sample applications are not built for iOS.

.. note::

   The sample projects get the libraries of the last build, device or simulator. Build again for
   the other one before switching the destination in Xcode.


Running the sample application
---------------------------------
Open ``ipjsua.xcodeproj`` using Xcode in :source:`pjsip-apps/src/pjsua/ios`, then build and run it.
You will see telnet instructions on the device's screen. Telnet to this address to operate the
application. See :doc:`CLI Manual </specific-guides/other/cli_cmd>` for commands available.

If you configured TLS with OpenSSL, or other libraries, add them to the project first.

.. tip::

   :source:`build/apple/build-xcframework.sh` refuses to run while the generated headers are in
   the source tree. To build :doc:`framework` after a CMake build, use a clean checkout.

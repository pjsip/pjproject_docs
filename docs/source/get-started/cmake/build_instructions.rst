Build Instructions with CMake
=======================================================================================

.. contents:: Table of Contents
    :depth: 2


Requirements
------------

* **CMake 3.28** or newer.
* A C and C++ compiler: GCC, Clang, Apple Clang, or MSVC.
* A build tool: Ninja or Make, or a Visual Studio or Xcode generator.

The third-party libraries in :source:`third_party/` (Speex, GSM, iLBC,
G.722.1, libsrtp, libyuv, the resampler, WebRTC AEC and AEC3) are built from
source by default. Everything else is optional and found with
``find_package()``: OpenSSL or another SSL backend, Opus, SDL2, OpenH264,
libvpx, FFMPEG, ALSA, Video4Linux2, libuuid, libupnp, and others. See
:doc:`options`.


Quick Start
-----------

.. code-block:: shell

   $ cd pjproject
   $ cmake -S . -B cmake-build -DCMAKE_BUILD_TYPE=Release
   $ cmake --build cmake-build -j
   $ ./cmake-build/pjsip-apps/bin/pjsua

Output goes to the build directory, into ``<build>/<module>/lib`` and
``<build>/<module>/bin``, not into the source tree's ``<module>/lib`` and
``<module>/bin`` as with the GNU build.

.. tip::

   Don't name the build directory ``build``: :source:`build/` is a source
   directory in pjproject, so its build output would mix with tracked files.


Everyday Commands
-----------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Task
     - Command
   * - Debug build
     - ``cmake -S . -B cmake-debug -DCMAKE_BUILD_TYPE=Debug``
   * - Shared libraries
     - ``cmake -S . -B cmake-build -DBUILD_SHARED_LIBS=ON``
   * - Build one target
     - ``cmake --build cmake-build --target pjsua -j``
   * - Verbose build
     - ``cmake --build cmake-build -v``
   * - Clean objects
     - ``cmake --build cmake-build --target clean``
   * - Start over
     - Delete the build directory.
   * - Install
     - ``cmake --install cmake-build --prefix /opt/pjsip``
   * - Run the tests
     - ``ctest --test-dir cmake-build --output-on-failure``
   * - Show all options and their values
     - ``cmake -LAH -N cmake-build``

Without ``CMAKE_BUILD_TYPE``, a Ninja or Make build is compiled with
``-O2`` and assertions enabled, as the GNU build is, unless ``CMAKE_C_FLAGS``
has an ``-O`` flag of its own. The build types ``Debug``, ``Release``,
``RelWithDebInfo`` and ``MinSizeRel`` use CMake's standard flags instead.

Multi-config generators (Visual Studio, Xcode, Ninja Multi-Config) ignore
``CMAKE_BUILD_TYPE``. Choose the configuration at build, test and install
time instead, e.g. ``cmake --build cmake-build --config Release``,
``ctest --test-dir cmake-build -C Release`` and
``cmake --install cmake-build --config Release``.
The configuration is then added to the file names instead, e.g.
``pjlib-test-Release.exe`` or ``libpj-Debug.lib``.


Configuring
-----------

Options
^^^^^^^

Features are selected with cache options passed as ``-D<option>=<value>``,
e.g. ``-DPJLIB_WITH_SSL=gnutls`` or ``-DPJMEDIA_WITH_VIDEO=OFF``. The
:doc:`options` page lists them all. Some common ones:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Goal
     - Option
   * - Another SSL backend, or none
     - ``-DPJLIB_WITH_SSL=gnutls|mbedtls|darwin|apple|schannel``, or
       ``-DPJLIB_WITH_SSL=`` for none
   * - The platform's native I/O queue
     - ``-DPJLIB_WITH_IOQUEUE=epoll|kqueue|iocp``
   * - Audio only
     - ``-DPJMEDIA_WITH_VIDEO=OFF``
   * - Drop a codec
     - e.g. ``-DPJMEDIA_WITH_OPUS_CODEC=OFF``
   * - A system copy of a bundled library
     - e.g. ``-DPJ_DEP_SRTP=system``

Dependencies and what got enabled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A feature whose dependency is not found is switched off and the build
carries on without it. Configure reports this as::

   -- [!] OPUS was not found. setting PJMEDIA_WITH_OPUS_CODEC to OFF

so check the configure output for ``[!]``, or the final values with
``cmake -LA -N cmake-build``.

To make CMake find a library outside the default locations, pass its
install prefix, the directory holding ``include/`` and ``lib/``:

.. code-block:: shell

   $ cmake -S . -B cmake-build -DCMAKE_PREFIX_PATH="/opt/openssl-3;/opt/media"

``<Package>_ROOT`` (e.g. ``-DOPUS_ROOT=...``) and ``-DOPENSSL_ROOT_DIR=...``
work too. A result that has been cached is not searched again, so after
installing a missing library, delete the build directory, or at least
``CMakeCache.txt``, and configure again.

.. _cmake_config_site:

``config_site.h``
^^^^^^^^^^^^^^^^^

CMake does not generate ``pjlib/include/pj/config_site.h``; it stays
user-managed, as in the GNU build, for the settings without a CMake option,
such as ``PJSUA_MAX_CALLS`` or ``PJ_GRP_LOCK_DEBUG``. See
:any:`config_site.h`.

Settings that have a CMake option must **not** also be set in
``config_site.h``, because CMake cannot read that file. A
``config_site.h`` written for the GNU build or the Visual Studio solution
often has some. A clash shows up as macro redefinition warnings (``C4005``
on MSVC, ``"redefined"`` on GCC and Clang) and, for a backend or codec, as
undefined symbols at link time. Remove them and use the option instead:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - ``config_site.h`` macro
     - CMake option
   * - ``PJ_IOQUEUE_IMP``
     - ``PJLIB_WITH_IOQUEUE``
   * - ``PJ_HAS_SSL_SOCK``, ``PJ_SSL_SOCK_IMP``
     - ``PJLIB_WITH_SSL``
   * - ``PJ_HAS_THREADS``
     - ``PJLIB_WITH_THREADS``
   * - ``PJMEDIA_HAS_VIDEO``
     - ``PJMEDIA_WITH_VIDEO``
   * - ``PJMEDIA_HAS_SRTP``
     - ``PJMEDIA_WITH_SRTP``
   * - ``PJMEDIA_HAS_<codec>_CODEC``, ``PJMEDIA_HAS_WEBRTC_AEC3``, ...
     - the matching ``PJMEDIA_WITH_*``
   * - ``PJMEDIA_AUDIO_DEV_HAS_*``, ``PJMEDIA_VIDEO_DEV_HAS_*``
     - ``PJMEDIA_WITH_AUDIODEV_*``, ``PJMEDIA_WITH_VIDEODEV_*``
   * - ``PJSIP_HAS_TLS_TRANSPORT``
     - ``PJSIP_WITH_TLS``
   * - ``PJSIP_HAS_DIGEST_AKA_AUTH``
     - ``PJSIP_WITH_DIGEST_AKA_AUTH``


Platforms
---------

Linux and macOS
^^^^^^^^^^^^^^^

See :doc:`/get-started/posix/build_cmake`, which covers the libraries to
install, the I/O queue and TLS options, and on macOS, builds for the other
architecture and universal binaries. For macOS applications, building PJSIP
into ``PJSIP.xcframework`` (experimental) is described in
:doc:`/get-started/posix/framework`.

Windows, Visual Studio
^^^^^^^^^^^^^^^^^^^^^^

See :doc:`/get-started/windows/build_cmake`, which covers the Visual Studio
requirements, the Windows-native options (IOCP, Schannel, WASAPI,
DirectShow), prebuilt libraries and their C runtime, and building and
debugging in Visual Studio.

.. _cmake_windows_mingw:

Windows, MinGW-w64
^^^^^^^^^^^^^^^^^^

From an MSYS2 *MINGW64* shell:

.. code-block:: shell

   $ pacman -S --needed mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake \
         mingw-w64-x86_64-ninja mingw-w64-x86_64-openssl
   $ cmake -S . -B cmake-build -G Ninja -DCMAKE_BUILD_TYPE=Release
   $ cmake --build cmake-build

A *UCRT64* shell takes the same packages with the
``mingw-w64-ucrt-x86_64-`` prefix instead; this has not been verified.

The Windows-native options in :doc:`/get-started/windows/build_cmake` apply
too, except Schannel, which needs MSVC. The bundled WebRTC AEC and AEC3 are
not available. Run the binaries from the same shell, which provides the GCC
runtime and OpenSSL DLLs.

iOS
^^^

See :doc:`/get-started/ios/build_cmake` in the iOS guide, and
:doc:`/get-started/ios/framework` for the XCFramework.

Android
^^^^^^^

See :doc:`/get-started/android/build_cmake` in the Android guide, and
:doc:`/get-started/android/aar` for the AAR.

Other cross builds
^^^^^^^^^^^^^^^^^^

Use a CMake toolchain file:

.. code-block:: shell

   $ cmake -S . -B cmake-arm -DCMAKE_TOOLCHAIN_FILE=/path/to/toolchain.cmake \
         -DCMAKE_BUILD_TYPE=Release

This is not validated; the GNU build (``./configure --host=...``, see
:doc:`/get-started/posix/build_gnu`) is the tested path.

For an ARM target without an operating system (``CMAKE_SYSTEM_NAME``
``Generic``), :source:`cmake/toolchains/arm-none-eabi.cmake` configures with
a GCC toolchain such as the Arm GNU toolchain; its header lists the
settings:

.. code-block:: shell

   $ cmake -S . -B cmake-arm --toolchain cmake/toolchains/arm-none-eabi.cmake \
         -DPJ_WITH_CXX=OFF -DPJ_BUILD_APPS=OFF -DBUILD_TESTING=OFF \
         -DPJLIB_WITH_SSL=

CI checks this configure, and that the pjlib sources needing only the C
library compile. The socket layer and threads have to come from an RTOS, so
pjlib does not link yet.


Running Tests
-------------

``BUILD_TESTING`` (``ON`` by default) registers ``pjlib-test``,
``pjlib-util-test``, ``pjnath-test``, ``pjmedia-test``, ``pjsip-test`` and
``pjsua2-test`` with CTest. Each suite takes several minutes:

.. code-block:: shell

   $ ctest --test-dir cmake-build --output-on-failure      # all suites
   $ ctest --test-dir cmake-build -R pjlib-util            # one suite

To run single tests, call a test binary directly. Some tests read data
files relative to the source tree's ``<module>/bin/`` directory; the pjlib
SSL tests, for example, load their certificates from ``../build/``. Run
those from ``<module>/bin/``:

.. code-block:: shell

   $ mkdir -p pjlib/bin && cd pjlib/bin
   $ ../../cmake-build/pjlib/bin/pjlib-test --list
   $ ../../cmake-build/pjlib/bin/pjlib-test sock_test ssl_sock_test


Installing
----------

.. code-block:: shell

   $ cmake --install cmake-build --prefix /opt/pjsip

installs:

* headers under ``<prefix>/include/``;
* the PJSIP libraries under ``<prefix>/lib/`` (``lib64`` on some
  distributions), and the bundled third-party ones under
  ``<prefix>/lib/pjproject/third_party/``;
* ``pjsua`` under ``<prefix>/bin/``;
* the CMake package under ``<prefix>/lib/cmake/Pj/``, and a pkg-config
  file, ``<prefix>/lib/pkgconfig/libpjproject.pc``; see :doc:`using`.

.. note::

   Before :pr:`5301`, a static build installed its libraries under
   ``<prefix>/bin/``, and the pkg-config file was empty.

Packagers can split the installation with ``--component PjRuntime``
(shared libraries and executables) and ``--component PjDevelopment``
(headers, static libraries and the package files).


.. _cmake_migrating_from_configure:

Migrating from ``./configure``
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - ``./configure`` flag
     - CMake option
   * - ``--prefix=DIR``
     - ``-DCMAKE_INSTALL_PREFIX=DIR``, or ``cmake --install ... --prefix DIR``
   * - ``--enable-shared``
     - ``-DBUILD_SHARED_LIBS=ON``
   * - ``--disable-threads``
     - ``-DPJLIB_WITH_THREADS=OFF``
   * - ``--disable-pjsua2``
     - ``-DPJ_BUILD_PJSUA2=OFF``
   * - ``--enable-epoll`` / ``--enable-kqueue``
     - ``-DPJLIB_WITH_IOQUEUE=epoll`` / ``kqueue``
   * - ``--disable-ssl``
     - ``-DPJLIB_WITH_SSL=``
   * - ``--with-gnutls=DIR``, ``--with-mbedtls=DIR``
     - ``-DPJLIB_WITH_SSL=gnutls`` / ``mbedtls``, with ``DIR`` in
       ``CMAKE_PREFIX_PATH``
   * - ``--with-ssl=DIR``
     - ``-DOPENSSL_ROOT_DIR=DIR``
   * - ``--disable-video``
     - ``-DPJMEDIA_WITH_VIDEO=OFF``
   * - ``--disable-sound``
     - ``-DPJMEDIA_WITH_AUDIODEV=OFF``
   * - ``--disable-<codec>``, e.g. ``--disable-opus``
     - ``-DPJMEDIA_WITH_<CODEC>_CODEC=OFF``, e.g.
       ``-DPJMEDIA_WITH_OPUS_CODEC=OFF``
   * - ``--disable-speex-aec``, ``--disable-libyuv``, ``--disable-ffmpeg``
     - ``-DPJMEDIA_WITH_SPEEX_AEC=OFF``, ``-DPJMEDIA_WITH_LIBYUV=OFF``,
       ``-DPJMEDIA_WITH_FFMPEG=OFF``
   * - ``--disable-upnp``
     - ``-DPJNATH_WITH_UPNP=OFF``
   * - ``--with-external-srtp``
     - ``-DPJ_DEP_SRTP=system``
   * - ``--with-external-speex``
     - ``-DPJ_DEP_SPEEX=system``
   * - ``--with-external-yuv``
     - ``-DPJ_DEP_YUV=system``
   * - ``--with-external-gsm``
     - ``-DPJ_DEP_GSM=system``
   * - ``CFLAGS``, ``LDFLAGS``, ``user.mak``
     - ``-DCMAKE_C_FLAGS=...``, ``-DCMAKE_CXX_FLAGS=...``,
       ``-DCMAKE_EXE_LINKER_FLAGS=...``

Not available with CMake: ``--disable-small-filter`` /
``--disable-large-filter`` (the resampler always has both), and the Qt
``vidgui`` sample.

The Java, Python and C# bindings, built with ``make`` in
:source:`pjsip-apps/src/swig`, are ``-DPJ_BUILD_SWIG_JAVA=ON``,
``-DPJ_BUILD_SWIG_PYTHON=ON`` and ``-DPJ_BUILD_SWIG_CSHARP=ON``; see
:doc:`options`.


Troubleshooting
---------------

**A feature or backend is missing.** Its dependency was not found, and the
option was switched off; configure printed a ``[!]`` line. Install the
library, or point ``CMAKE_PREFIX_PATH`` at it, then delete the build
directory and configure again.

**Macro redefinition warnings, or undefined symbols at link time.**
``config_site.h`` sets something a CMake option controls; see
`config_site.h`_.

**An option has no effect.** Option names are case-sensitive and a
misspelled one is silently ignored. Check the name in :doc:`options`, or
with ``cmake -LA -N cmake-build``.

**Windows: "Could not create named generator Visual Studio ..."** The
``cmake`` on ``PATH`` is MSYS2's or Cygwin's; see
:ref:`MSYS2, Cygwin or Strawberry Perl on PATH <windows_cmake_path>`.

**A wrong copy of a library is used.** CMake also searches the prefixes of
tools on ``PATH``. Exclude unwanted ones with
``-DCMAKE_IGNORE_PREFIX_PATH=...``.


Known Limitations
-----------------

* **Three build systems.** When adding or removing source files, update the
  GNU ``Makefile``, the Visual Studio ``.vcxproj`` *and* the
  ``CMakeLists.txt``.
* **The Visual Studio solution stays the reference Windows build,** and
  covers targets not yet validated with CMake, such as Windows 32-bit and
  ARM64.
* **System dependencies in 2.17.** ``PJ_DEP_<name>=system`` finds the
  library but sibling modules may not use it (e.g. ``PJMEDIA_WITH_SRTP``
  silently turns ``OFF``). Fixed after 2.17 (:pr:`4942`).

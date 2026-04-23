Build Instructions with CMake
=======================================================================================

.. contents:: Table of Contents
    :depth: 3


Supported Platforms
-------------------

CMake support was introduced in PJSIP 2.16 (:pr:`4494`) and is still
marked **experimental** as of 2.17. Subsequent refinements include
install/export support that makes ``find_package(Pj)`` usable by
downstream projects (:pr:`4900`), version reading from ``version.mak``
(:pr:`4896`), and aarch64 atomics fixes (:pr:`4739`). It is regularly
tested on:

* Linux x86_64
* macOS (Intel and Apple Silicon)

Other targets covered by the GNU build system (Windows, Android, iOS,
mingw, cross-compilation, RTEMS, BSD, etc.) are not yet validated with
CMake. For those platforms, use the autoconf build described in
:any:`/get-started/posix/build_instructions` or the Visual Studio
projects described in :any:`/get-started/windows/index`.

When configuring, CMake prints a warning banner to make the experimental
status explicit. The banner can be silenced once you are aware of the
caveats:

.. code-block:: shell

   $ cmake -S . -B build -DPJ_SKIP_EXPERIMENTAL_NOTICE=ON


Requirements
------------

Tools
^^^^^

* **CMake 3.28** or newer.
* A C and C++ compiler (GCC, Clang, or Apple Clang on macOS).
* A build tool supported by CMake (Ninja or GNU Make recommended).

Optional system libraries
^^^^^^^^^^^^^^^^^^^^^^^^^

The same optional libraries listed for the GNU build apply. CMake locates
them through its ``find_package()`` mechanism, using either CMake's
built-in modules or the Find modules shipped under
:source:`cmake/<cmake/>`:

* SSL/TLS backends: OpenSSL, GnuTLS, Mbed TLS, Apple (darwin), Windows
  Schannel. See :any:`/specific-guides/security/ssl`.
* Audio: ALSA (Linux), Core Audio (macOS), Oboe (Android), WASAPI
  (Windows).
* Video: SDL2, FFMPEG, libyuv, OpenH264, libvpx, Video4Linux2 (Linux),
  Metal (macOS/iOS).
* Audio codecs: OPUS, Speex, SpeexDSP, SILK, OpenCORE AMR, Lyra, bcg729.
* Other: libsrtp, libuuid, libupnp.

The third-party libraries bundled in the :source:`third_party/` directory
(Speex, GSM, iLBC, libsrtp, libyuv, libwebrtc, libwebrtc-aec3, G.722.1,
and the legacy resampler) are built from source by default. Each one can
optionally be switched to a system-provided copy via ``PJ_DEP_<NAME>``;
see `Third-party dependency providers`_ below.


Quick Start
-----------

From the top of the source tree:

.. code-block:: shell

   $ cd pjproject
   $ cmake -S . -B build
   $ cmake --build build -j

The build places its output under ``build/`` rather than in the
``<module>/lib`` and ``<module>/bin`` directories used by the GNU build.

To run the test suite:

.. code-block:: shell

   $ ctest --test-dir build --output-on-failure

To install headers, libraries, and the CMake package config:

.. code-block:: shell

   $ cmake --install build --prefix /usr/local


Common Configurations
---------------------

The recipes below cover the most frequent customizations. They can be
combined freely, and all options can also be set interactively via
``cmake-gui`` or ``ccmake``.

Debug vs release build
^^^^^^^^^^^^^^^^^^^^^^

The CMake build defaults to ``Release``. Build with debug symbols and
no optimization:

.. code-block:: shell

   $ cmake -S . -B build-debug -DCMAKE_BUILD_TYPE=Debug
   $ cmake --build build-debug -j

Use ``RelWithDebInfo`` for an optimized build that keeps debug info.

.. note::

   ``CMAKE_BUILD_TYPE`` is orthogonal to PJSIP's compile-time
   diagnostic switches such as ``PJ_GRP_LOCK_DEBUG`` and
   ``PJ_POOL_DEBUG``; those live in :any:`config_site.h`.

Shared vs static libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^

Static archives are built by default. Enable shared libraries with:

.. code-block:: shell

   $ cmake -S . -B build -DBUILD_SHARED_LIBS=ON

Choosing an SSL/TLS backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^

OpenSSL is the default. Switch backends with ``PJLIB_WITH_SSL``:

.. code-block:: shell

   # GnuTLS
   $ cmake -S . -B build -DPJLIB_WITH_SSL=gnutls

   # Mbed TLS (e.g., embedded)
   $ cmake -S . -B build -DPJLIB_WITH_SSL=mbedtls

   # Apple Secure Transport (macOS / iOS native)
   $ cmake -S . -B build -DPJLIB_WITH_SSL=darwin

   # Windows Schannel (Windows native)
   $ cmake -S . -B build -DPJLIB_WITH_SSL=schannel

If the backend is installed outside the default search paths, point
CMake at it via ``CMAKE_PREFIX_PATH``:

.. code-block:: shell

   $ cmake -S . -B build \
       -DPJLIB_WITH_SSL=openssl \
       -DCMAKE_PREFIX_PATH=/opt/openssl-3

See :any:`/specific-guides/security/ssl` for backend trade-offs.

Choosing an I/O queue backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default ``select`` backend works on every supported OS. For
higher throughput, switch to the platform-native implementation:

.. code-block:: shell

   # Linux
   $ cmake -S . -B build -DPJLIB_WITH_IOQUEUE=epoll

   # macOS / BSD
   $ cmake -S . -B build -DPJLIB_WITH_IOQUEUE=kqueue

   # Windows
   $ cmake -S . -B build -DPJLIB_WITH_IOQUEUE=iocp

Enabling video
^^^^^^^^^^^^^^

``PJMEDIA_WITH_VIDEO`` is ``ON`` by default, but most video codec
stacks are pulled in only when their system libraries are present.
A fully featured video build typically needs SDL2 (preview window),
libyuv (format conversion), and an H.264 or VP8/VP9 codec:

.. code-block:: shell

   $ cmake -S . -B build \
       -DPJMEDIA_WITH_VIDEO=ON \
       -DPJMEDIA_WITH_LIBYUV=ON \
       -DPJMEDIA_WITH_OPEN_H264_CODEC=ON \
       -DPJMEDIA_WITH_VPX_CODEC=ON \
       -DPJMEDIA_WITH_VIDEODEV_SDL=ON

Watch the configure output to confirm that OpenH264, libvpx, libyuv,
and SDL2 were found. Missing libraries silently turn the
corresponding feature ``OFF``.

.. note::

   The CMake build automatically adds ``PJMEDIA_HAS_VIDEO=1`` (and
   the other ``PJMEDIA_HAS_*`` macros) as compile definitions based
   on the selected options, so you do **not** need to duplicate those
   in ``config_site.h``.

Minimal / audio-only build
^^^^^^^^^^^^^^^^^^^^^^^^^^

Skip video and heavier optional components to produce a lean library:

.. code-block:: shell

   $ cmake -S . -B build \
       -DPJMEDIA_WITH_VIDEO=OFF \
       -DPJMEDIA_WITH_FFMPEG=OFF \
       -DPJMEDIA_WITH_WEBRTC_AEC3=OFF

Individual codecs can be disabled the same way,
e.g. ``-DPJMEDIA_WITH_BCG729_CODEC=OFF`` or
``-DPJMEDIA_WITH_OPUS_CODEC=OFF``.

Disabling SIP TLS
^^^^^^^^^^^^^^^^^

SIP TLS transport is enabled whenever an SSL backend is available. To
skip TLS even when the SSL backend is present:

.. code-block:: shell

   $ cmake -S . -B build -DPJSIP_WITH_TLS=OFF

Disabling UPnP
^^^^^^^^^^^^^^

.. code-block:: shell

   $ cmake -S . -B build -DPJNATH_WITH_UPNP=OFF

Customizing compile / link flags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CMake equivalent of ``user.mak`` is the standard set of CMake
flag variables:

.. code-block:: shell

   $ cmake -S . -B build \
       -DCMAKE_C_FLAGS="-msoft-float -fno-builtin" \
       -DCMAKE_CXX_FLAGS="-msoft-float -fno-builtin" \
       -DCMAKE_EXE_LINKER_FLAGS="-Wl,--as-needed"

For per-configuration flags use the suffixed forms
(``CMAKE_C_FLAGS_DEBUG``, ``CMAKE_C_FLAGS_RELEASE``, etc.). Environment
variables ``CC``, ``CXX``, and ``CFLAGS`` are also honoured on the
first configure.

Using a system-provided libsrtp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   $ cmake -S . -B build -DPJ_DEP_SRTP=system

CMake locates libsrtp through the bundled
:source:`cmake/FindSRTP.cmake` module. The same pattern works for
other ``PJ_DEP_*`` entries — see `Third-party dependency providers`_.

.. warning::

   ``PJ_DEP_*=system`` has a known issue in 2.17 where the dependency
   is located successfully but is not picked up by sibling modules
   (e.g., libsrtp found, but ``PJMEDIA_WITH_SRTP`` silently turns
   ``OFF``). The fix (:pr:`4942`) is available on master; users on
   2.17 should either stick with the default ``bundled`` providers or
   apply the patch.

Installing to a custom prefix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   $ cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/opt/pjsip
   $ cmake --build build -j
   $ cmake --install build


Configure Options
-----------------

The tables in this section are the CMake equivalent of the GNU
``./configure --help`` output — every PJSIP option, its default, and
its allowed values. The same information can be queried on a
configured build tree with::

   $ cmake -LAH -N build | less

``-L`` lists cached variables, ``-A`` includes advanced ones, ``-H``
prints the help text, ``-N`` skips reconfiguring. In addition,
``cmake-gui`` and ``ccmake`` provide interactive editors.

Global options
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Option
     - Default
     - Description
   * - ``BUILD_SHARED_LIBS``
     - ``OFF``
     - Build shared libraries instead of static archives.
   * - ``BUILD_TESTING``
     - ``ON``
     - Enable CTest. Test executables are registered automatically.
   * - ``CMAKE_BUILD_TYPE``
     - ``Release``
     - Standard CMake build type (``Debug``, ``Release``,
       ``RelWithDebInfo``, ``MinSizeRel``). Ignored by multi-config
       generators such as Xcode and Visual Studio.
   * - ``CMAKE_INSTALL_PREFIX``
     - platform default
     - Install destination (``/usr/local`` on most Unix-likes).
   * - ``PJ_SKIP_EXPERIMENTAL_NOTICE``
     - ``OFF``
     - Silence the experimental-status warning printed during configure.

Third-party dependency providers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each bundled third-party library can be built from source (``bundled``)
or linked against a system copy (``system``). The default is
``bundled``.

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Option
     - Values
     - Library
   * - ``PJ_DEP_G7221``
     - ``bundled`` / ``system``
     - G.722.1 codec.
   * - ``PJ_DEP_GSM``
     - ``bundled`` / ``system``
     - GSM 06.10 codec.
   * - ``PJ_DEP_iLBC``
     - ``bundled``
     - iLBC codec (bundled only).
   * - ``PJ_DEP_Resample``
     - ``bundled`` / ``system``
     - The legacy ``libresample`` provider.
   * - ``PJ_DEP_Speex``
     - ``bundled`` / ``system``
     - Speex codec. The ``system`` value is also intended to cover the
       Speex resampler backend together with ``PJMEDIA_WITH_RESAMPLE=speex``;
       modern Speex (1.2+) ships the resampler in ``libspeexdsp``, which
       CMake picks up automatically. This flow requires :pr:`4942`
       and is therefore only reliable on master or 2.17.x releases
       that include the fix.
   * - ``PJ_DEP_SRTP``
     - ``bundled`` / ``system``
     - libsrtp for SRTP/DTLS-SRTP.
   * - ``PJ_DEP_WebRTC``
     - ``bundled``
     - WebRTC AEC (not available on Apple, MinGW, Cygwin).
   * - ``PJ_DEP_WebRTC_AEC3``
     - ``bundled``
     - WebRTC AEC3 (not available on Apple, MinGW, Cygwin).
   * - ``PJ_DEP_YUV``
     - ``bundled`` / ``system``
     - libyuv for video colour conversion.

PJLIB options
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Option
     - Default / allowed values
     - Description
   * - ``PJLIB_WITH_FLOATING_POINT``
     - ``ON``
     - Enable floating-point math.
   * - ``PJLIB_WITH_IOQUEUE``
     - ``select`` / ``kqueue`` / ``epoll`` / ``iocp``
     - I/O queue backend.
   * - ``PJLIB_WITH_LIBUUID``
     - ``ON`` on Linux
     - Use ``libuuid`` for UUID generation.
   * - ``PJLIB_WITH_SSL``
     - ``openssl`` / ``gnutls`` / ``mbedtls`` / ``darwin`` / ``apple`` / ``schannel``
     - SSL/TLS backend. See :any:`/specific-guides/security/ssl`.

PJNATH options
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Option
     - Default
     - Description
   * - ``PJNATH_WITH_UPNP``
     - ``ON``
     - Enable UPnP NAT traversal (requires ``libupnp``).

PJMEDIA options
^^^^^^^^^^^^^^^

Core media options:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Option
     - Default / allowed values
     - Description
   * - ``PJMEDIA_WITH_SRTP``
     - ``ON`` (requires ``Pj::Dep::SRTP``)
     - Enable SRTP/DTLS-SRTP.
   * - ``PJMEDIA_WITH_RESAMPLE``
     - ``libresample`` / ``libsamplerate`` / ``speex`` / ``none``
     - Resampling backend. ``libresample`` is bundled;
       ``libsamplerate`` uses system ``libsamplerate``; ``speex`` uses
       the bundled Speex resampler.
   * - ``PJMEDIA_WITH_SPEEX_AEC``
     - ``ON`` (requires Speex + SpeexDSP)
     - Enable Speex acoustic echo cancellation.
   * - ``PJMEDIA_WITH_WEBRTC_AEC``
     - ``ON`` (non-Apple/MinGW/Cygwin)
     - Enable WebRTC AEC.
   * - ``PJMEDIA_WITH_WEBRTC_AEC3``
     - ``ON`` (non-Apple/MinGW/Cygwin)
     - Enable WebRTC AEC3.
   * - ``PJMEDIA_WITH_VIDEO``
     - ``ON``
     - Master switch for video support.
   * - ``PJMEDIA_WITH_LIBYUV``
     - ``ON`` when video is enabled
     - Use libyuv for video format conversion.
   * - ``PJMEDIA_WITH_FFMPEG``
     - ``ON`` when video is enabled
     - Use FFMPEG. The ``avutil`` component is required; ``swscale``,
       ``avcodec``, ``avformat``, and ``avdevice`` are optional and each
       have their own ``PJMEDIA_WITH_FFMPEG_<COMPONENT>`` toggle.

Audio codecs (default ``ON`` when the provider is available, except
where noted):

* ``PJMEDIA_WITH_G711_CODEC``
* ``PJMEDIA_WITH_L16_CODEC``
* ``PJMEDIA_WITH_GSM_CODEC``
* ``PJMEDIA_WITH_SPEEX_CODEC``
* ``PJMEDIA_WITH_ILBC_CODEC``
* ``PJMEDIA_WITH_G722_CODEC``
* ``PJMEDIA_WITH_G7221_CODEC``
* ``PJMEDIA_WITH_OPENCORE_AMRNB_CODEC``
* ``PJMEDIA_WITH_OPENCORE_AMRWB_CODEC``
* ``PJMEDIA_WITH_SILK_CODEC``
* ``PJMEDIA_WITH_OPUS_CODEC``
* ``PJMEDIA_WITH_BCG729_CODEC``
* ``PJMEDIA_WITH_LYRA_CODEC``
* ``PJMEDIA_WITH_ANDROID_MEDIACODEC_CODEC`` (default ``OFF``; enable
  when targeting Android)

Video codecs:

* ``PJMEDIA_WITH_VPX_CODEC`` (via libvpx)
* ``PJMEDIA_WITH_OPEN_H264_CODEC`` (via OpenH264)

Audio device backends (each enabled when the underlying platform library
is found):

* ``PJMEDIA_WITH_AUDIODEV`` (master switch)
* ``PJMEDIA_WITH_AUDIODEV_NULL``
* ``PJMEDIA_WITH_AUDIODEV_JNI``  (Android)
* ``PJMEDIA_WITH_AUDIODEV_OBOE`` (Android)
* ``PJMEDIA_WITH_AUDIODEV_COREAUDIO`` (macOS/iOS)
* ``PJMEDIA_WITH_AUDIODEV_ALSA`` (Linux)
* ``PJMEDIA_WITH_AUDIODEV_WMME`` (Windows)
* ``PJMEDIA_WITH_AUDIODEV_WASAPI`` (Windows)

Video device backends:

* ``PJMEDIA_WITH_VIDEODEV`` (master switch)
* ``PJMEDIA_WITH_VIDEODEV_AVI`` (AVI writer/player)
* ``PJMEDIA_WITH_VIDEODEV_OPENGL``
* ``PJMEDIA_WITH_VIDEODEV_FFMPEG``
* ``PJMEDIA_WITH_VIDEODEV_SDL``
* ``PJMEDIA_WITH_VIDEODEV_METAL`` (macOS/iOS)
* ``PJMEDIA_WITH_VIDEODEV_QT``
* ``PJMEDIA_WITH_VIDEODEV_V4L2`` (Linux)
* ``PJMEDIA_WITH_VIDEODEV_DSHOW`` (Windows)

PJSIP options
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Option
     - Default
     - Description
   * - ``PJSIP_WITH_TLS``
     - ``ON`` when SSL is enabled
     - Enable SIP over TLS transport.

.. tip::

   To list every option and its current value for an already-configured
   build directory, run::

      $ cmake -LAH -N build | less

   ``-L`` lists cached variables, ``-A`` includes advanced ones, ``-H``
   prints the help text, and ``-N`` skips reconfiguring.


Configuring TLS Support
-----------------------

The SSL/TLS backend is selected with ``PJLIB_WITH_SSL``. The supported
values are ``openssl`` (default), ``gnutls``, ``mbedtls``, ``darwin`` /
``apple``, and ``schannel``. CMake locates the chosen backend via the
same Find modules used by the GNU build, plus a config-mode lookup for
Mbed TLS.

Example with GnuTLS:

.. code-block:: shell

   $ cmake -S . -B build -DPJLIB_WITH_SSL=gnutls

See :any:`/specific-guides/security/ssl` for the full backend matrix and
configuration notes. The selected backend is recorded in the installed
``PjConfig.cmake`` so that downstream projects pick up the same
dependency automatically.


Site-Specific Configuration (``config_site.h``)
-----------------------------------------------

CMake does **not** generate ``pjlib/include/pj/config_site.h``; it
remains user-managed, as in the GNU build.

However — unlike the GNU build — the CMake build automatically wires
the ``PJMEDIA_HAS_*`` family of feature macros from the corresponding
``PJMEDIA_WITH_*`` options. You do **not** need to put
``#define PJMEDIA_HAS_VIDEO 1``, ``PJMEDIA_HAS_SRTP``,
``PJMEDIA_HAS_OPUS_CODEC``, etc. into ``config_site.h`` when building
with CMake; toggling ``PJMEDIA_WITH_VIDEO`` / ``PJMEDIA_WITH_SRTP`` /
``PJMEDIA_WITH_OPUS_CODEC`` at configure time is enough.

``config_site.h`` is still needed for knobs that the CMake options do
**not** cover — application-level sizing, debug diagnostics, group
lock debugging, and similar. See :any:`config_site.h` for the full
list. Typical content:

.. code-block:: c

   /* pjlib/include/pj/config_site.h */
   #define PJSUA_MAX_CALLS       32
   #define PJ_GRP_LOCK_DEBUG     1   /* troubleshooting */
   #define PJSIP_MAX_PKT_LEN     8000


Build Targets
-------------

The GNU build uses ``make all``, ``make clean``, ``make distclean``,
``make install``. The CMake equivalents are driver commands that work
with whichever backend generator you selected (Ninja, Make, Xcode,
Visual Studio, …):

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Task
     - Command
   * - Build everything
     - ``cmake --build build -j``
   * - Build one target
     - ``cmake --build build --target pjsua -j``
   * - Clean object files
     - ``cmake --build build --target clean``
   * - Wipe the whole build tree
     - ``rm -rf build`` (no direct CMake equivalent of
       ``make distclean`` — just delete the build directory)
   * - Install
     - ``cmake --install build``
   * - Install with a different prefix than configured
     - ``cmake --install build --prefix /some/path``
   * - Verbose build
     - ``cmake --build build -v``


Running Tests
-------------

``BUILD_TESTING=ON`` (the default) registers all test executables with
CTest. Typical use:

.. code-block:: shell

   $ ctest --test-dir build --output-on-failure          # run everything
   $ ctest --test-dir build -R pjlib                     # regex by name
   $ ctest --test-dir build -j $(nproc)                  # parallel

Individual test binaries can also be invoked directly, for example:

.. code-block:: shell

   $ ./build/pjlib/pjlib-test --list
   $ ./build/pjlib/pjlib-test timer_test

.. note::

   The GNU-style "run a specific test from the ``bin/`` directory" flow
   described elsewhere in the documentation does not apply to the CMake
   build. Test binaries live under ``build/<module>/`` rather than
   ``<module>/bin/``.


Installing
----------

.. code-block:: shell

   $ cmake --install build --prefix /usr/local

The install lays out the tree as:

* Public headers: ``<prefix>/include/``
* Libraries: ``<prefix>/lib/`` (or ``<prefix>/lib64/``, per
  ``GNUInstallDirs``)
* Executables (``pjsua``, test binaries if selected): ``<prefix>/bin/``
* CMake package config: ``<prefix>/lib/cmake/Pj/``

Installation components are defined so that packagers can split the
payload:

* ``PjRuntime`` – shared libraries and executables.
* ``PjDevelopment`` – headers, static libraries, symlinks, and the CMake
  package config.

See :any:`using <using>` for consuming the installed package in a
downstream CMake project.


Cross-Compilation
-----------------

Cross-compilation follows the standard CMake toolchain-file pattern:

.. code-block:: shell

   $ cmake -S . -B build-arm64 \
       -DCMAKE_TOOLCHAIN_FILE=/path/to/my-toolchain.cmake \
       -DPJ_SKIP_EXPERIMENTAL_NOTICE=ON
   $ cmake --build build-arm64 -j

.. warning::

   Cross-compilation with CMake is not regularly tested. If you need a
   validated cross-build, use the GNU build (``./configure --host=...``)
   described in :any:`/get-started/posix/build_instructions`.


CMake vs GNU ``./configure``
----------------------------

The CMake option names do not always match the autoconf flags one-for-one.
The table below lists the common equivalences:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - ``./configure`` flag
     - CMake equivalent
   * - ``--enable-shared``
     - ``-DBUILD_SHARED_LIBS=ON``
   * - ``--disable-video``
     - ``-DPJMEDIA_WITH_VIDEO=OFF``
   * - ``--disable-ssl``
     - (set ``PJLIB_WITH_SSL`` to the desired backend or disable
       individual features)
   * - ``--with-gnutls=DIR``
     - ``-DPJLIB_WITH_SSL=gnutls`` (``DIR`` resolved via
       ``CMAKE_PREFIX_PATH``)
   * - ``--with-external-speex``
     - ``-DPJ_DEP_Speex=system``
   * - ``--with-external-srtp``
     - ``-DPJ_DEP_SRTP=system``
   * - ``--with-external-yuv``
     - ``-DPJ_DEP_YUV=system``
   * - ``--enable-epoll``
     - ``-DPJLIB_WITH_IOQUEUE=epoll``
   * - ``--enable-kqueue``
     - ``-DPJLIB_WITH_IOQUEUE=kqueue``
   * - ``--disable-opus``
     - ``-DPJMEDIA_WITH_OPUS_CODEC=OFF``
   * - ``--disable-speex-aec``
     - ``-DPJMEDIA_WITH_SPEEX_AEC=OFF``
   * - ``--disable-libyuv``
     - ``-DPJMEDIA_WITH_LIBYUV=OFF``
   * - ``--disable-ffmpeg``
     - ``-DPJMEDIA_WITH_FFMPEG=OFF``
   * - ``--prefix=DIR``
     - ``-DCMAKE_INSTALL_PREFIX=DIR``
   * - ``CFLAGS="..."``
     - ``-DCMAKE_C_FLAGS="..."`` (or ``CMAKE_BUILD_TYPE``)

For fine-grained codec/feature toggles that do not appear in this
table, follow the ``--disable-FEATURE`` → ``PJMEDIA_WITH_FEATURE=OFF``
naming pattern.

A few GNU flags have no CMake equivalent today:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ``./configure`` flag
     - CMake status
   * - ``--disable-ssl``
     - No "off" value for ``PJLIB_WITH_SSL``. If the chosen backend
       cannot be located the build silently falls back to no-SSL; to
       deterministically skip TLS, also set
       ``-DPJSIP_WITH_TLS=OFF``.
   * - ``--disable-pjsua2``
     - Not exposed. The ``pjsua2`` library is always built.
   * - ``--disable-sound``
     - Use ``-DPJMEDIA_WITH_AUDIODEV=OFF`` to disable the audio
       device subsystem entirely.
   * - ``--disable-small-filter`` / ``--disable-large-filter``
     - Not exposed; bundled ``libresample`` is always built with both
       filters.


Known Limitations
-----------------

* **Experimental.** Only Linux x86_64 and macOS are tested. Expect rough
  edges on other platforms.
* **No Visual Studio / Xcode project parity.** The CMake build can
  generate VS or Xcode projects, but the bespoke
  :source:`pjlib/build/pjlib.vcxproj <pjlib/build/pjlib.vcxproj>` and
  companion projects are still the reference Windows build.
* **Three build systems must stay in sync.** When adding or removing
  source files in the tree, the GNU ``Makefile``, the MSVC ``.vcxproj``,
  *and* the relevant ``CMakeLists.txt`` must all be updated.
* **No automatic ``config_site.h``.** As with the GNU build,
  ``pjlib/include/pj/config_site.h`` is user-managed.
* **Cross-compilation untested.** Toolchain files work in principle but
  are not exercised in CI.

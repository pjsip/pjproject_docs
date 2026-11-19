Build with CMake
=======================================================================================

This page builds PJSIP with CMake. It follows the same steps as :doc:`build_gnu`, and the result
is the same libraries and applications.

.. note::

   Supported since release 2.18. CMake support is **experimental**; see
   :doc:`/get-started/cmake/index` for its status, and
   :doc:`/get-started/cmake/build_instructions` for CMake in general.

.. contents:: Table of Contents
    :depth: 3


Supported Targets
-----------------

The CMake build is tested on:

* Linux (x86_64),
* macOS (Apple Silicon),
* :any:`mingw/mingw-w64 </specific-guides/build_int/mingw>`, verified manually; see
  :doc:`/get-started/cmake/build_instructions`.

FreeBSD and other BSDs, RTEMS and other cross targets are not validated with CMake. Use
:doc:`build_gnu` for them.


Requirements
-------------

Tools and development libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **CMake 3.28** or newer. Check with ``cmake --version``.
* A C and C++ compiler: GCC, Clang, or Apple Clang (Xcode or its command line tools on macOS).
* A build tool: Make or Ninja. CMake uses Make by default; add ``-G Ninja`` to use Ninja.

On macOS, with `Homebrew <https://brew.sh/>`__:

.. code-block:: shell

   $ brew install cmake ninja

In addition, the following libraries are optional, but they will be used if they are present:

* (For Linux): ALSA (recommended). See :ref:`alsa`.
* SSL libraries such as OpenSSL, GnuTLS, or Mbed TLS (Mac can use native SSL). See
  :ref:`posix_cmake_tls` below.

Other optional libraries, such as Opus, are listed in :doc:`/get-started/cmake/options`.


Video Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following components are used for video:

#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. For format conversion and video manipulation:

   * libyuv (recommended). It is bundled in :source:`third_party/` and built by default.
   * :ref:`FFMPEG <ffmpeg>`.

#. For video codecs:

   * H263: get :ref:`FFMPEG <ffmpeg>`.
   * H264: choose one of the following:

     * :ref:`openh264`.
     * **VideoToolbox** (for Mac only). Used by default on macOS, with nothing to set.
     * :ref:`FFMPEG <ffmpeg>`

   * VP8 and VP9, see :ref:`libvpx`

#. Linux: Video4Linux2 (v4l2) development library.
#. macOS: AVFoundation for capture and Metal for rendering, both part of macOS and used by
   default.

.. note::

   The Qt based :source:`vidgui <pjsip-apps/src/vidgui/>` sample is not built by CMake. It
   reads the GNU build's settings, so it needs :doc:`build_gnu`.

.. tip::

   For more information about using the video, see :any:`/pjsua2/using/media_video` and the
   deep-dive pages under :ref:`video_guide_toc`.


Host requirements
^^^^^^^^^^^^^^^^^

The CMake build is known to work on the following hosts:

* Linux, many types of distributions.
* macOS
* :any:`mingw/mingw-w64 </specific-guides/build_int/mingw>`


Configuring
------------------

Running ``cmake`` to configure, the equivalent of ``./configure``.

Using Default Settings
^^^^^^^^^^^^^^^^^^^^^^

Run ``cmake`` without any options to let it detect the appropriate settings for the host. The
second argument names the build directory, where all the output goes:

.. code-block:: shell

   $ cd pjproject
   $ cmake -B cmake-build

.. note::

   As with ``./configure``, the default settings build the libraries with ``-O2``, and with
   assertions enabled. To build differently, choose a CMake build type, e.g.
   ``-DCMAKE_BUILD_TYPE=Debug`` (``-g``) or ``-DCMAKE_BUILD_TYPE=Release`` (``-O3 -DNDEBUG``),
   or give flags as shown in :ref:`posix_cmake_customizations` below.

.. tip::

   Don't name the build directory ``build``: :source:`build/` is a source directory in
   pjproject. Each build directory holds one configuration, so use a new one to build another
   configuration side by side.

Configuring prints a banner about CMake support being experimental.
``-DPJ_SKIP_EXPERIMENTAL_NOTICE=ON`` silences it.

Configure with Video Support
`````````````````````````````

Video is enabled by default with CMake, so nothing needs to be added to :any:`config_site.h`.
``-DPJMEDIA_WITH_VIDEO=OFF`` builds without video.

Video requirements will be detected by ``cmake``. Pay attention to the following output (the
sample below was taken on a Mac):

.. code-block::

   ...
   -- [pjmedia] Checking if FFMPEG is available - yes (PJMEDIA_WITH_FFMPEG)
   ...
   -- [pjmedia] Checking if VPX is available - yes (PJMEDIA_WITH_VPX_CODEC)
   -- [pjmedia] Checking if VideoToolbox is available - yes (PJMEDIA_WITH_VID_TOOLBOX_CODEC)
   -- [pjmedia] Checking if OpenH264 is available - no (PJMEDIA_WITH_OPEN_H264_CODEC OFF)
   -- [pjmedia] Checking if CoreAudio is available - yes (PJMEDIA_WITH_AUDIODEV_COREAUDIO)
   -- [pjmedia] Checking if SDL2 is available - yes (PJMEDIA_WITH_VIDEODEV_SDL)
   -- [pjmedia] Checking if AVFoundation is available - yes (PJMEDIA_WITH_VIDEODEV_DARWIN)
   -- [pjmedia] Checking if Metal is available - yes (PJMEDIA_WITH_VIDEODEV_METAL)
   ...

The above output shows that SDL2, ffmpeg and libvpx were found, as well as the macOS frameworks,
while OpenH264 was not. Each line names the option that the result sets. libyuv is bundled, so it
has no line of its own.

A library that is not found, or that is found but cannot be linked (for example, one built for
another architecture), is left out, and the build goes on without the feature. Its line then ends
in ``no``, with the option that was turned off. Lines starting with ``[!]`` report other things
left out, such as TLS.

.. note::

   Libraries are searched in the standard locations, and in the prefixes of the directories on
   ``PATH``; this is how Homebrew's libraries are found on a Mac. For a library in another
   location, the equivalent of ``--with-sdl`` and ``--with-ffmpeg``, give its install prefix (the
   directory holding ``include/`` and ``lib/``), either as ``<Package>_ROOT``:

   .. code-block:: shell

      $ cmake -B cmake-build -DSDL2_ROOT=/Users/pjsip/Desktop/opt \
            -DFFMPEG_ROOT=/Users/pjsip/Desktop/opt

   or, for several libraries at once, in ``CMAKE_PREFIX_PATH``:

   .. code-block:: shell

      $ cmake -B cmake-build -DCMAKE_PREFIX_PATH=/Users/pjsip/Desktop/opt

.. note::

   A result is kept in the build directory and not searched again. After installing a missing
   library, delete the build directory, or add ``--fresh`` to the ``cmake`` command, and configure
   again.

Features Customization
^^^^^^^^^^^^^^^^^^^^^^^

Configuration/customization is specified as ``-D<option>=<value>`` arguments, for example
``-DPJMEDIA_WITH_OPUS_CODEC=OFF``. The list of options and their values can be viewed by running:

.. code-block:: shell

   $ cmake -LH -N cmake-build

All the options are described in :doc:`/get-started/cmake/options`, and the CMake equivalent of
each ``./configure`` option is listed in
:ref:`Migrating from ./configure <cmake_migrating_from_configure>`.

.. note::

   PJSIP's settings that are not CMake options still go in :any:`config_site.h`, as with
   ``./configure``. A setting that has a CMake option must not also be set there; see
   :ref:`config_site.h with CMake <cmake_config_site>`.

Configuring Debug Version and Other Customizations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``CMAKE_BUILD_TYPE`` to build a debug version:

.. code-block:: shell

   $ cmake -B cmake-debug -DCMAKE_BUILD_TYPE=Debug

The other build types are ``Release``, ``RelWithDebInfo`` and ``MinSizeRel``.

Below is an example of specifying CFLAGS, as ``./configure CFLAGS=...`` does:

.. code-block:: shell

   $ cmake -B cmake-build -DCMAKE_C_FLAGS="-O3 -DNDEBUG -msoft-float -fno-builtin"

.. _posix_cmake_tls:

Configuring TLS Support
^^^^^^^^^^^^^^^^^^^^^^^

By default, as with ``./configure``, the first SSL library found is used: OpenSSL, then GnuTLS,
then Mbed TLS, and without any, PJSIP is built without TLS. Check which one was chosen in the
output:

.. code-block::

   -- [pjlib] SSL backend: openssl

To choose the backend, use ``PJLIB_WITH_SSL``. Configure then stops if it cannot be used, rather
than building without TLS:

.. code-block:: shell

   $ cmake -B cmake-build -DPJLIB_WITH_SSL=openssl -DOPENSSL_ROOT_DIR=/opt/openssl-3

On a Mac, ``-DPJLIB_WITH_SSL=apple`` uses Apple's Network framework, which needs no SSL library.

See :any:`/specific-guides/security/ssl` for the backends.


Cross Compilation
------------------

General
^^^^^^^^

Cross compilation uses a CMake toolchain file:

.. code-block:: shell

   $ cmake -B cmake-arm -DCMAKE_TOOLCHAIN_FILE=/path/to/toolchain.cmake

Cross builds are not validated, other than for Apple platforms and Android; :doc:`build_gnu` is
the tested path for other targets. Watch the ``cmake`` output for incorrect settings.

Please refer to Porting Guide for further information about porting PJ software.

Building for MacOS x86_64 on MacOS M1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the architecture; no toolchain file is needed:

.. code-block:: shell

   $ cmake -B cmake-x86_64 -DCMAKE_OSX_ARCHITECTURES=x86_64

Homebrew's libraries on an Apple Silicon Mac are built for arm64 only, so they cannot be linked
and are left out, including OpenSSL. Use ``-DPJLIB_WITH_SSL=apple`` for TLS, or point
``CMAKE_PREFIX_PATH`` at libraries built for x86_64.

Building for MacOS M1 on MacOS x86_64
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   $ cmake -B cmake-arm64 -DCMAKE_OSX_ARCHITECTURES=arm64

Building a universal binary for macOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both architectures can be built at once:

.. code-block:: shell

   $ cmake -B cmake-universal "-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64" \
         -DPJLIB_WITH_SSL=apple

Other libraries must then be universal too, or they are left out. The bundled WebRTC echo
canceller cannot be built for two architectures at once and is left out, with a ``[!]`` line.


Building
-------------

Once ``cmake`` completes successfully, start the build process with:

.. code-block:: shell

   $ cmake --build cmake-build -j

This runs Make or Ninja, whichever was chosen when configuring. The output goes into the build
directory, not the source tree: the libraries into ``<module>/lib``, e.g.
``cmake-build/pjlib/lib/libpj.a``, and the applications into ``pjsip-apps/bin``, e.g.
``cmake-build/pjsip-apps/bin/pjsua``.

The ``make`` targets and their equivalents:

.. list-table::
   :header-rows: 1

   * - make
     - CMake
   * - all
     - ``cmake --build cmake-build``
   * - dep, depend
     - Not needed: dependencies are tracked automatically.
   * - clean
     - ``cmake --build cmake-build --target clean``
   * - distclean, realclean
     - Delete the build directory.

A single target, e.g. one library or application, is built with ``--target``:

.. code-block:: shell

   $ cmake --build cmake-build --target pjsua -j

.. _posix_cmake_customizations:

Build Customizations
---------------------

Build features can be customized by specifying the options when running ``cmake`` as described
in Configuring above.

The equivalent of putting CFLAGS and LDFLAGS in ``user.mak`` is to give them when configuring.
Either set the ``CFLAGS``, ``CXXFLAGS`` and ``LDFLAGS`` environment variables for the first
configure of a build directory:

.. code-block:: shell

   $ CFLAGS="-msoft-float -fno-builtin" cmake -B cmake-build

or, at any time, the ``CMAKE_C_FLAGS``, ``CMAKE_CXX_FLAGS`` and ``CMAKE_EXE_LINKER_FLAGS``
options:

.. code-block:: shell

   $ cmake -B cmake-build -DCMAKE_C_FLAGS="-msoft-float -fno-builtin"

Optional: Installing PJSIP
---------------------------

Run ``cmake --install`` to install the header and library files to the target directory,
``/usr/local`` by default. ``--prefix DIR`` installs to another directory, as does the
``CMAKE_INSTALL_PREFIX`` option when configuring:

.. code-block:: shell

   $ cmake --install cmake-build --prefix /opt/pjsip

Besides the headers and libraries, this installs ``pjsua``, a ``libpjproject.pc`` file for
pkg-config, and a CMake package for ``find_package(Pj)``; see :doc:`/get-started/cmake/using`.

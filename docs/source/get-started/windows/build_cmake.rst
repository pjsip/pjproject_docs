Build with CMake
=======================================================================================

This page builds PJSIP with CMake and Visual Studio. CMake generates a Visual Studio solution and
builds it; the result is the same libraries and applications as :doc:`build_vs`.

.. note::

   Supported since release 2.18. See :doc:`/get-started/cmake/index` for its status, and
   :doc:`/get-started/cmake/build_instructions` for CMake in general.

.. contents:: Table of Contents
    :depth: 3


Supported Targets
-----------------

The CMake build is tested on Windows x64 with Visual Studio 2022.

The 32-bit and ARM64 targets are not validated with CMake; use :doc:`build_vs` for them. For
MinGW-w64, see :ref:`Windows, MinGW-w64 <cmake_windows_mingw>` on the CMake page.


Build Preparation
------------------

#. :doc:`Getting the source code </get-started/getting>` if you haven't already.
#. Customize :ref:`config_site.h` if needed, but read :ref:`windows_cmake_config_site` below
   first.


Requirements
-------------

Tools and SDKs
^^^^^^^^^^^^^^

* **Visual Studio 2022**, any edition, or the *Build Tools for Visual Studio 2022*, with the
  **Desktop development with C++** workload. The workload includes the Windows SDK and the
  *C++ CMake tools for Windows*, which is Visual Studio's own CMake.
* **CMake 3.28** or newer: Visual Studio's own, or one from
  `cmake.org <https://cmake.org/download/>`__. Check with ``cmake --version``; Visual Studio's
  shows a ``-msvc`` suffix, e.g. ``cmake version 3.31.6-msvc6``.

Run the commands on this page from a *Developer PowerShell for VS 2022*, which puts Visual Studio's
CMake on ``PATH``. They are written for PowerShell.

.. _windows_cmake_path:

.. warning::

   MSYS2, Cygwin or Strawberry Perl on ``PATH`` cause two problems. Their ``cmake`` can come first
   on ``PATH`` even in a developer shell, because the shell adds Visual Studio's CMake after the
   existing ``PATH``, and it has no Visual Studio generators: configure fails with
   *Could not create named generator Visual Studio 17 2022*, and ``cmake --version`` lacks the
   ``-msvc`` suffix. And CMake can pick up their MinGW builds of OpenSSL and other libraries, which
   MSVC cannot link. To avoid both, in PowerShell:

   .. code-block:: powershell

      > $vsw = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
      > $vs = Join-Path (& $vsw -latest -products * -property installationPath) `
          "Common7\IDE\CommonExtensions\Microsoft\CMake"
      > $env:PATH = "$vs\CMake\bin;$vs\Ninja;$env:PATH"
      > cmake -B cmake-build -G "Visual Studio 17 2022" -A x64 `
          "-DCMAKE_IGNORE_PREFIX_PATH=C:/msys64/mingw64;C:/msys64/ucrt64;C:/msys64/usr;C:/Strawberry/c"

   ``vswhere``, from the Visual Studio Installer, finds the installation of any edition, Build Tools
   included, so this works in a plain PowerShell too.

Optional libraries
^^^^^^^^^^^^^^^^^^

The following libraries are optional, but they will be used if they are found:

* An SSL library for TLS, see :ref:`windows_cmake_tls` below. ``-DPJLIB_WITH_SSL=schannel`` uses
  Windows' own Schannel, which needs no library.
* `Opus <https://opus-codec.org/>`__, and the video libraries below.

Other optional libraries are listed in :doc:`/get-started/cmake/options`.

.. _windows_cmake_crt:

.. important::

   A prebuilt library must use the same C runtime as the PJSIP build. CMake builds with the DLL
   runtime: ``/MDd`` for ``Debug`` and ``/MD`` for the other configurations. Note that this
   differs from the ``Debug`` configuration of :doc:`build_vs`, which uses ``/MTd``.

   A mismatch shows up at link time as ``LNK2038`` (*mismatch detected for 'RuntimeLibrary'*),
   as unresolved symbols such as ``__imp__CrtDbgReportW`` (a library built for ``Debug``, linked
   into ``Release``), or as ``LNK4098`` warnings (*defaultlib ... conflicts with use of other
   libs*). Build each library for the runtime of the configuration that uses it, or build PJSIP
   with the static runtime, see :ref:`windows_cmake_static_crt`.

Video Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following components are used for video:

#. **DirectShow**, for camera capture. It is part of the Windows SDK and used by default.
#. `SDL <http://www.libsdl.org/>`__ **version 2.0**, for rendering. Get the
   ``SDL2-devel-<version>-VC.zip`` development package; CMake finds SDL2 through the CMake package
   files in its ``cmake`` directory, see :ref:`windows_cmake_libs`.
#. libyuv, for format conversion. It is bundled in :source:`third_party/` and built by default.
#. For video codecs:

   * H.264: :ref:`openh264`.
   * VP8 and VP9: :ref:`libvpx`. The libvpx build command in :doc:`build_vs` has
     ``--enable-static-msvcrt``, which builds it for the static runtime; leave it out for the DLL
     runtime, see :ref:`the C runtime <windows_cmake_crt>` above.

.. tip::

   For more information about using the video, see :any:`/pjsua2/using/media_video` and the
   deep-dive pages under :ref:`video_guide_toc`.


Configuring
------------------

Using Default Settings
^^^^^^^^^^^^^^^^^^^^^^

Run ``cmake`` with the Visual Studio generator and the platform. The ``-B`` argument names the build
directory, where all the output goes:

.. code-block:: powershell

   > cd pjproject
   > cmake -B cmake-build -G "Visual Studio 17 2022" -A x64

The defaults are the same as for the Visual Studio solution: the ``select`` I/O queue and WMME
audio. In addition, video is enabled, with DirectShow capture.

.. tip::

   Don't name the build directory ``build``: :source:`build/` is a source directory in pjproject.
   A Visual Studio build directory holds all the configurations, ``Debug``, ``Release`` and
   others; they are chosen when building.

.. _windows_cmake_libs:

Libraries in other locations
````````````````````````````

Libraries are searched in the standard locations. For a library in another location, give its
install prefix, the directory holding ``include/`` and ``lib/``, in ``CMAKE_PREFIX_PATH``:

.. code-block:: powershell

   > cmake -B cmake-build -G "Visual Studio 17 2022" -A x64 "-DCMAKE_PREFIX_PATH=C:/deps"

or as ``<Package>_ROOT``, e.g. ``-DOPUS_ROOT=C:/deps/opus``. For SDL2, point ``SDL2_DIR`` at the
``cmake`` directory of the development package, e.g. ``-DSDL2_DIR=C:/deps/SDL2-2.30.9/cmake``.

.. note::

   A result is kept in the build directory and not searched again. After installing a missing
   library, delete the build directory, or add ``--fresh`` to the ``cmake`` command, and configure
   again.

Verifying configuration
```````````````````````

Check that the intended features are detected by observing the ``cmake`` output, for example:

.. code-block::

   -- [pjlib] SSL backend: openssl
   ...
   -- [pjmedia] Checking if OPUS is available - yes (PJMEDIA_WITH_OPUS_CODEC)
   ...
   -- [pjmedia] Checking if VPX is available - yes (PJMEDIA_WITH_VPX_CODEC)
   -- [pjmedia] Checking if OpenH264 is available - yes (PJMEDIA_WITH_OPEN_H264_CODEC)
   -- [pjmedia] Checking if SDL2 is available - yes (PJMEDIA_WITH_VIDEODEV_SDL)

A library that is not found, or that is found but cannot be linked, is left out, and the build goes
on without the feature. Its line then ends in ``no``, with the option that was turned off. Lines
starting with ``[!]`` report other things left out.

Features Customization
^^^^^^^^^^^^^^^^^^^^^^^

Configuration/customization is specified as ``-D<option>=<value>`` arguments, for example
``-DPJMEDIA_WITH_OPUS_CODEC=OFF``. The list of options and their values can be viewed by running:

.. code-block:: powershell

   > cmake -LH -N cmake-build

All the options are described in :doc:`/get-started/cmake/options`. The Windows-native ones:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Option
     - Effect
   * - ``-DPJLIB_WITH_IOQUEUE=iocp``
     - I/O completion ports, instead of ``select``.
   * - ``-DPJLIB_WITH_SSL=schannel``
     - Windows Schannel for TLS. Needs no SSL library.
   * - ``-DPJMEDIA_WITH_AUDIODEV_WASAPI=ON``
     - WASAPI audio. Add ``-DPJMEDIA_WITH_AUDIODEV_WMME=OFF`` for WASAPI only.
   * - ``-DPJMEDIA_WITH_VIDEODEV_DSHOW=OFF``
     - No DirectShow camera capture.
   * - ``-DPJSIP_WITH_DIGEST_AKA_AUTH=ON``
     - Digest AKA authentication.

.. note::

   PJSIP's libraries are static with Visual Studio; ``-DBUILD_SHARED_LIBS=ON`` is not supported.
   For a single DLL, use the SWIG bindings, see :doc:`/get-started/cmake/options`.

.. _windows_cmake_config_site:

``config_site.h``
^^^^^^^^^^^^^^^^^

PJSIP's settings that are not CMake options, such as ``PJSUA_MAX_CALLS``, still go in
:any:`config_site.h`. A setting that has a CMake option must **not** also be set there. When the
two differ, the value in ``config_site.h`` wins, silently or with ``C4005`` macro redefinition
warnings, and for a backend or codec, the build can then fail with unresolved symbols at link
time. See :ref:`config_site.h with CMake <cmake_config_site>`.

A ``config_site.h`` written for :doc:`build_vs` usually has some. Remove them, and use the options
instead:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - ``config_site.h`` for the Visual Studio solution
     - CMake
   * - ``PJMEDIA_HAS_VIDEO``
     - On by default; ``-DPJMEDIA_WITH_VIDEO=OFF`` for audio only.
   * - ``PJMEDIA_HAS_LIBYUV``
     - On by default (bundled).
   * - ``PJMEDIA_VIDEO_DEV_HAS_DSHOW``
     - On by default.
   * - ``PJMEDIA_VIDEO_DEV_HAS_SDL``, ``PJMEDIA_HAS_OPENH264_CODEC``,
       ``PJMEDIA_HAS_VPX_CODEC``, ``PJMEDIA_HAS_OPUS_CODEC``, ``PJMEDIA_HAS_FFMPEG``
     - On when the library is found.
   * - ``PJ_IOQUEUE_IMP``
     - ``-DPJLIB_WITH_IOQUEUE=iocp``
   * - ``PJ_HAS_SSL_SOCK``, ``PJ_SSL_SOCK_IMP``
     - ``-DPJLIB_WITH_SSL=...``
   * - ``PJMEDIA_AUDIO_DEV_HAS_WASAPI``, ``PJMEDIA_AUDIO_DEV_HAS_WMME``
     - ``-DPJMEDIA_WITH_AUDIODEV_WASAPI=ON``, ``-DPJMEDIA_WITH_AUDIODEV_WMME=OFF``
   * - ``PJSIP_HAS_DIGEST_AKA_AUTH``
     - ``-DPJSIP_WITH_DIGEST_AKA_AUTH=ON``

Settings without a CMake option, such as ``PJMEDIA_HAS_VPX_CODEC_VP9``, stay in
``config_site.h``.

.. _windows_cmake_tls:

Configuring TLS Support
^^^^^^^^^^^^^^^^^^^^^^^

By default, the first SSL library found is used: OpenSSL, then GnuTLS, then Mbed TLS, and without
any, PJSIP is built without TLS. Check which one was chosen in the output:

.. code-block::

   -- [pjlib] SSL backend: openssl

OpenSSL installed with the `Win64 OpenSSL <https://slproweb.com/products/Win32OpenSSL.html>`__
installer, in ``C:\Program Files\OpenSSL-Win64``, is found without any option. For OpenSSL in
another location:

.. code-block:: powershell

   > cmake -B cmake-build -G "Visual Studio 17 2022" -A x64 -DPJLIB_WITH_SSL=openssl `
       "-DOPENSSL_ROOT_DIR=C:/deps/openssl"

To use Windows' own Schannel instead, which needs no SSL library:

.. code-block:: powershell

   > cmake -B cmake-build -G "Visual Studio 17 2022" -A x64 -DPJLIB_WITH_SSL=schannel

With ``PJLIB_WITH_SSL`` set, configure stops if the backend cannot be used, rather than building
without TLS. See :any:`/specific-guides/security/ssl` for the backends.

.. _windows_cmake_static_crt:

Using the static C runtime
^^^^^^^^^^^^^^^^^^^^^^^^^^

To build with the static runtime, ``/MTd`` for ``Debug`` and ``/MT`` for the others, as the
``Debug``, ``Debug-Static`` and ``Release-Static`` configurations of :doc:`build_vs` do:

.. code-block:: powershell

   > cmake -B cmake-mt -G "Visual Studio 17 2022" -A x64 `
       '-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded$<$<CONFIG:Debug>:Debug>' `
       -DOPENSSL_MSVC_STATIC_RT=ON

The single quotes keep PowerShell from reading the ``$``. ``OPENSSL_MSVC_STATIC_RT`` makes CMake
pick the ``/MT`` build of OpenSSL from the Win64 OpenSSL installation; other prebuilt libraries
must be built for the static runtime too.

The configurations of the Visual Studio solution and their CMake equivalent:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Visual Studio solution
     - CMake
   * - ``Debug-Dynamic`` (``/MDd``)
     - ``Debug``
   * - ``Release``, ``Release-Dynamic`` (``/MD``)
     - ``Release``
   * - ``Debug``, ``Debug-Static`` (``/MTd``)
     - ``Debug``, with the static runtime
   * - ``Release-Static`` (``/MT``)
     - ``Release``, with the static runtime

CMake also has ``RelWithDebInfo`` (release with debugging info) and ``MinSizeRel``.


Building
-------------

Once ``cmake`` completes successfully, build a configuration with:

.. code-block:: powershell

   > cmake --build cmake-build --config Release --parallel

Without ``--config``, the ``Debug`` configuration is built. The output goes into the build
directory, not the source tree, and the configuration is added to the file names:

* the libraries into ``<module>\lib``, e.g. ``cmake-build\pjlib\lib\libpj-Release.lib``,
* ``pjsua`` into ``cmake-build\pjsip-apps\bin\pjsua-Release.exe``,
* the samples into ``cmake-build\pjsip-apps\bin\samples``, e.g. ``simple_pjsua-Release.exe``,
* the tests into ``<module>\bin``, e.g. ``cmake-build\pjlib\bin\pjlib-test-Release.exe``.

A single target, e.g. one library or application, is built with ``--target``:

.. code-block:: powershell

   > cmake --build cmake-build --config Release --target pjsua

To clean, use ``--target clean``, or delete the build directory to start over.

Building and debugging in Visual Studio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated solution can also be opened in Visual Studio:

#. Open ``cmake-build\pjproject.sln``.
#. Set ``pjsua`` as the startup project.
#. Select the configuration, e.g. ``Debug``, and build.

Each sample application is a project of its own, e.g. ``simple_pjsua``, so a sample can be set as
the startup project and debugged directly; the ``sample_debug`` project of :doc:`build_vs` is not
needed.

.. note::

   CMake regenerates the projects when the ``CMakeLists.txt`` files change, so changes made in the
   project properties are lost. Change the build with CMake options instead.


Running pjsua
-------------

DLLs that the applications use, e.g. OpenSSL's or SDL2's, must be on ``PATH`` or next to the
executable:

.. code-block:: powershell

   > $env:PATH = "C:\Program Files\OpenSSL-Win64\bin;$env:PATH"
   > cmake-build\pjsip-apps\bin\pjsua-Release.exe


Running the tests
-----------------

The test suites are registered with CTest; choose the configuration with ``-C``. Each suite takes
several minutes:

.. code-block:: powershell

   > ctest --test-dir cmake-build -C Release --output-on-failure      # all suites
   > ctest --test-dir cmake-build -C Release -R pjlib-util            # one suite

To run single tests, call a test binary directly from ``<module>\bin`` in the source tree; the
pjlib SSL tests, for example, load their certificates from ``..\build\``:

.. code-block:: powershell

   > mkdir pjlib\bin -Force | Out-Null
   > Push-Location pjlib\bin
   > ..\..\cmake-build\pjlib\bin\pjlib-test-Release.exe sock_test ssl_sock_test
   > Pop-Location


Optional: Installing PJSIP
---------------------------

Run ``cmake --install`` to install the header and library files to a directory, with the same
configuration as built:

.. code-block:: powershell

   > cmake --install cmake-build --config Release --prefix C:/pjsip

Besides the headers, and the libraries in ``C:\pjsip\lib``, e.g. ``libpj-Release.lib``, this installs
``pjsua``, and a CMake package for ``find_package(Pj)``; see :doc:`/get-started/cmake/using`.

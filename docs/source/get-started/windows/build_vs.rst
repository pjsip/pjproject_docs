Build with the Visual Studio solution
=======================================

This page builds PJSIP with the Visual Studio solution files shipped in pjproject. See
:doc:`build_cmake` for the CMake alternative.

.. contents:: Table of Contents
    :depth: 3

.. note::
   
   For building with mingw-w64 see :any:`/specific-guides/build_int/mingw`. 

.. note:: 

   PJSIP does not provide DLL projects for Windows, but please see 
   :doc:`Building Dynamic Link Libraries </api/generated/pjlib/group/group__pj__dll__target>` 
   page in PJLIB documentation on how to build these DLL.

Build Preparation
------------------

#. :doc:`Getting the source code </get-started/getting>` if you haven't already.
#. Customize :ref:`config_site.h`

Requirements
-------------

Host requirements
^^^^^^^^^^^^^^^^^

A Windows version that Visual Studio 2022 supports, e.g. Windows 10 or 11.


Windows on ARM Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please refer to :pr:`2807` for more information.

Tools and SDKs
^^^^^^^^^^^^^^

The Visual Studio based project files can be used with:

* **Microsoft Visual Studio 2022**, any edition, with the **Desktop development with C++**
  workload, which includes the Windows SDK.

.. warning::

   Since release 2.18:

   * Microsoft Visual Studio 2015, 2017 and 2019 are **deprecated**. They can still open
     ``pjproject-vs14.sln``, but are no longer tested.
   * The Visual Studio 2005 solution, ``pjproject-vs8.sln``, and its projects are **removed**,
     and with them the support for Visual Studio 2005, 2008 and 2012, and the Windows Mobile
     project files. Use release 2.17 or earlier with these.

In addition, the following is optional:

* One of SSL library, as specified in :any:`/specific-guides/security/ssl` (see below for
  installing OpenSSL)


.. _windows_openssl:

Installing OpenSSL
^^^^^^^^^^^^^^^^^^^^^^^^
To install OpenSSL SDK from a binary distribution, e.g. the
`Win64 OpenSSL <https://slproweb.com/products/Win32OpenSSL.html>`__ installer:

#. Install OpenSSL SDK to any folder (e.g. ``C:\Program Files\OpenSSL-Win64``)
#. Add OpenSSL DLL location to the system PATH.
#. Add OpenSSL include path to Visual Studio includes search directory. Make sure that
   OpenSSL header files can be accessed from the program with ``#include <openssl/ssl.h>``
   construct.
#. Add OpenSSL library path to Visual Studio library search directory. Make sure the following
   libraries are accessible:

    * ``libcrypto`` and ``libssl`` (OpenSSL 1.1 or newer), or ``libeay32`` and ``ssleay32``
      (older OpenSSL).

      You must use the same run-time option for PJSIP and the OpenSSL libraries.
      If you compile PJSIP with Multithreaded Debug (/MTd), you need to use the same
      run-time option when compiling the library. Please consult the library's doc for more details.
      The Win64 OpenSSL installer has a library directory for each run-time option, e.g.
      ``lib\VC\x64\MTd`` for /MTd.

PJSIP links these libraries itself, with ``#pragma comment(lib, ...)``. To link them in your
project instead, e.g. as part of a combined library, set ``PJ_AUTO_LINK_SSL_LIBS`` to 0 in
:any:`config_site.h` (since release 2.18).

Then to enable TLS transport support in PJSIP, please check :any:`/specific-guides/security/ssl`.


Video support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Additional requirements
```````````````````````

#. **DirectShow**, for camera capture. Its headers and libraries are part of the Windows SDK,
   and the DirectShow base classes are bundled in :source:`third_party/BaseClasses`, built by the
   ``libbaseclasses`` project of the solution.
#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. libyuv (recommended). It is bundled in :source:`third_party/yuv`, built by the ``libyuv``
   project of the solution. See :any:`libyuv <guide_libyuv>`.

#. OpenH264 (recommended): Follow the instructions in :ref:`openh264`.
#. FFMPEG development library (alternative), see :ref:`ffmpeg_windows` (below) for instructions. 
   If H.263 is not needed, libyuv **and** OpenH264 can be used instead.
#. Optional for H.264: `libx264 <http://www.videolan.org/developers/x264.html>`__. 
   We tested with the latest from git (as of October 2011). In MSYS console:

   .. code-block:: shell

      $ ./configure --enable-static      # add options if needed, e.g: optimization, install dir, search path
      $ make && make install-lib-static  # default install dir is /usr/local

#. Optional for libvpx: `libvpx <https://www.webmproject.org/code/>`__,
   supported since :pr:`2253`. In MSYS console, e.g. for x64 and Visual Studio 2022
   (``./configure --help`` lists the other targets):

   .. code-block:: shell

      $ ./configure --target=x86_64-win64-vs17 --disable-examples --disable-docs --disable-tools --enable-static --enable-vp8 --enable-vp9 --enable-static-msvcrt  # add options if needed, e.g: optimization, install dir, search path
      $ make    #Generate Visual Studio solution
      #Build the static library using Visual Studio solution

   ``--enable-static-msvcrt`` builds libvpx with the static run-time (/MT, /MTd), as PJSIP's
   ``Debug`` and ``*-Static`` configurations use. Leave it out for the ``Release`` and
   ``*-Dynamic`` configurations.

#. Optional: `Qt development SDK <http://qt-project.org/downloads/>`__ for 
   building the video GUI sample. We tested with version 4.6 or later.
   
   * without this you can still enjoy video with pjsua console application


.. _ffmpeg_windows:

Getting/building ffmpeg on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FFMPEG is used for format conversion and video manipulation as well as video codecs such as
H.264 (together with libx264) and H263P/H263-1998.   
If H.263 is not needed, libyuv AND OpenH264 can be used instead.
   
PJMEDIA by default supports FFMPEG version 2.8 or newer (see :issue:`1897`). Using older version of
FFMPEG is possible, see the ticket for information.

.. note::

   For H.264 support, you need newer releases (October 2011 onwards), and it needs libz too.

* You may be able to use a binary distribution of FFMPEG with the development files (headers and
  import libraries), usually called a "shared" or "dev" build. We haven't tested them thoroughly.
* For building FFMPEG on Windows, use MSYS|MinGW. Please see :any:`/specific-guides/build_int/mingw`.

  .. note::

     To avoid problems, put MSYS, libx264, and ffmpeg in folders that do not
     contain space, e.g: **C:\\msys, C:\\devlib\\ffmpeg**.

* Configure and build:

  .. code-block:: shell

     $ ./configure --enable-shared --disable-static
     $ make && make install

* If H.264 support is needed:

  .. code-block:: shell

     $ ./configure --enable-shared --disable-static --enable-gpl --enable-libx264
     $ make && make install


Additional configuration
````````````````````````

#. Add include and library paths for the required components:

   #. SDL
   #. OpenH264
   #. libvpx

   PJSIP links these libraries itself, with ``#pragma comment(lib, ...)``. To link one in your
   project instead, e.g. as part of a combined library, set its switch to 0 in
   ``config_site.h`` (since release 2.18): ``PJMEDIA_AUTO_LINK_SDL_LIBS``,
   ``PJMEDIA_AUTO_LINK_OPENH264_LIBS``, ``PJMEDIA_AUTO_LINK_VPX_LIBS``,
   ``PJMEDIA_AUTO_LINK_OPUS_LIBS`` or ``PJMEDIA_AUTO_LINK_FFMPEG_LIBS``.

#. Add these to your ``config_site.h``:

   .. code-block:: c

      #define PJMEDIA_HAS_VIDEO             1
      #define PJMEDIA_HAS_OPENH264_CODEC    1
      #define PJMEDIA_HAS_LIBYUV            1
      #define PJMEDIA_VIDEO_DEV_HAS_SDL     1
      #define PJMEDIA_VIDEO_DEV_HAS_DSHOW   1

#. For ffmpeg (optional): add the include and library paths, also add this to 
   your ``config_site.h``:

   .. code-block:: c

      #define PJMEDIA_HAS_FFMPEG            1

#. For libvpx (optional): add the include and library paths, also add this to 
   your ``config_site.h``:

   .. code-block:: c

      #define PJMEDIA_HAS_VPX_CODEC         1    //by default VP8 codec is enabled
      #define PJMEDIA_HAS_VPX_CODEC_VP9     1    //enable VP9 codec

Building the Projects
---------------------

Follow the steps below to build the libraries/application using Visual Studio:

#. For Visual Studio 17 (VS 2022): open ``pjproject-vs14.sln`` solution file. The deprecated
   Visual Studio 14, 15 and 16 (VS 2015, 2017 and 2019) open the same solution file.
#. Set ``pjsua`` as Active or Startup Project.
#. Select the platform: ``Win32``, ``x64`` or ``ARM64``.
#. Select ``Debug`` or ``Release`` build as appropriate.
#. Build the project. This will build ``pjsua`` application and all libraries
   needed by ``pjsua``.
#. After successful build, the pjsua application will be placed in ``pjsip-apps/bin``
   directory, e.g. ``pjsua-x86_64-x64-vc14-Release.exe``, and the libraries in lib directory
   under each projects. The ``libpjproject`` project also combines all the libraries into one,
   in the ``lib`` directory of pjproject, e.g. ``lib/libpjproject-x86_64-x64-vc14-Release.lib``.

.. note::

   For Visual Studio 14/15/16/17, you can specify the ``BuildToolset`` used from
   :source:`pjproject-vs14-common-config.props <build/vs/pjproject-vs14-common-config.props#L26>`.
   By default it is set to ``v143``.

To build the samples:

#. (Still using the same workspace)
#. Set samples project as Active Project
#. Select Debug or Release build as appropriate. 
   The complete list of build configuration:

   .. list-table::
      :header-rows: 0

      * - Debug
        - multithreaded, statically linked with LIBC, debug (i.e. the **/MTd** flag).
      * - Release
        - multithreaded, dynamically linked with MSVCRT, release (i.e. the **/MD** flag).
      * - Debug-Static
        - multithreaded, statically linked with LIBC, debug (i.e. the **/MTd** flag).
      * - Debug-Dynamic
        - multithreaded, dynamically linked with MSVCRT, debug (i.e. the **/MDd** flag).
      * - Release-Static
        - multithreaded, statically linked with LIBC, release (i.e. the **/MT** flag).
      * - Release-Dynamic
        - multithreaded, dynamically linked with MSVCRT, release (i.e. the **/MD** flag).

#. Build the project. This will build all sample applications and all libraries 
   needed.
#. After successful build, the sample applications will be placed in 
   ``pjsip-apps/bin/samples`` directory, and the libraries in lib directory 
   under each projects.

Debugging Sample Applications
-----------------------------

Sample applications are built using Samples.mak makefile, therefore it is difficult 
to setup debugging session in Visual Studio for these applications. 

To solve this issue, the pjsip_apps workspace contain one project called 
``sample_debug`` which can be used to debug a sample application.

To setup debugging using ``sample_debug`` project:

#. Set sample_debug project as Active Project
#. Edit debug.c file inside this project.
#. Modify the #include line to include the particular sample application to debug
#. Select Debug build.
#. Build and debug the project.


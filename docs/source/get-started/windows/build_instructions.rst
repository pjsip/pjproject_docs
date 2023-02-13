Build Instructions
===================

.. contents:: Table of Contents
    :depth: 3

This page describes how to use Microsoft Visual Studio to build pjsip libraries:

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

Windows NT, 2000, XP, 2003, Vista, Windows 7, Windows 10, or later.


Windows on ARM Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please refer to :pr:`2807` for more information.

Tools and SDKs
^^^^^^^^^^^^^^

The Visual Studio based project files can be used with one of the following tools:

* Microsoft Visual Studio/C++ 2005 (including Express edition),
* Microsoft Visual Studio 2008. You may need to fix the IP Helper API header bug.
* Microsoft Visual Studio 2012. Tested on Professional version, untested on Express version.
* Microsoft Visual Studio 2015.
* Microsoft Visual Studio 2017.
* Microsoft Visual Studio 2019.
* Microsoft Visual Studio 2022.

.. note::

   Microsoft Visual Studio 2010 **is unsupported** as it does not import
   PJSIP's VS2005 solution files properly.

In addition, the following SDK's are needed:

    * Essential for other than Windows 8/Visual Studio 2012: 
    
      - DirectX SDK (tested with DirectX version 8 and 9). After installing DirectX, add the 
        include and library paths to Visual Studio.

    * Optional if not included in Visual Studio: 
    
      - Platform SDK (tested with Platform SDK for Windows Server 2003 SP1).
  
      .. hint:: 

         By using Visual Studio 2012 (or newer), there's no need to install 
         standalone Windows SDK/DirectX SDK. 
         (`ref <https://en.wikipedia.org/wiki/Microsoft_Windows_SDK>`__ and 
         `ref <https://docs.microsoft.com/en-us/windows/win32/directx-sdk--august-2009=>`__). 

    * Optional: one of SSL library, as specified in :any:`/specific-guides/security/ssl` (see below
      for installing OpenSSL)


.. _windows_openssl:

Installing OpenSSL
^^^^^^^^^^^^^^^^^^^^^^^^
To install OpenSSL SDK from the Win32 binary distribution:

#. Install OpenSSL SDK to any folder (e.g. C:\OpenSSL)
#. Add OpenSSL DLL location to the system PATH.
#. Add OpenSSL include path to Visual Studio includes search directory. Make sure that 
   OpenSSL header files can be accessed from the program with ``#include <openssl/ssl.h>``
   construct.
#. Add OpenSSL library path to Visual Studio library search directory. Make sure the following
   libraries are accessible:
   
    * libeay32 and ssleay32
    
      You must use the same run-time option for PJSIP and the OpenSSL libraries. 
      If you compile PJSIP with Multithreaded Debug (/MTd), you need to use the same 
      run-time option when compiling the library. Please consult the library's doc for more details.

Then to enable TLS transport support in PJSIP, please check :any:`/specific-guides/security/ssl`.


Video support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Additional requirements
```````````````````````

#. **DirectShow SDK**, included in Windows SDK. The minimum component required 
   within the SDK is **Windows Development Headers and Libraris** and **Samples**.

   * If you don't need Windows 7 features, the recommended SDK is 
     `Windows SDK Update for Windows Vista <http://www.microsoft.com/downloads/en/details.aspx?FamilyID=ff6467e6-5bba-4bf5-b562-9199be864d29>`__.
   * If you need Windows 7 features then use `Windows SDK for Windows 7 <http://www.microsoft.com/downloads/en/confirmation.aspx?FamilyID=6B6C21D2-2006-4AFA-9702-529FA782D63B>`__. 
     Also if you are using Visual Studio 2005 then you will need to patch it 
     using `MS Knowledge Base 949009 <http://support.microsoft.com/kb/949009/>`_

#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. libyuv (recommended). See :any:`libyuv <guide_libyuv>`. 

#. OpenH264 (recommended): Follow the instructions in :ref:`openh264`.
#. FFMPEG development library (alternative), see :ref:`ffmpeg_windows` (below) for instructions. 
   If H.263 is not needed, libyuv **and** OpenH264 can be used instead.
#. Optional for H.264: `libx264 <http://www.videolan.org/developers/x264.html>`__. 
   We tested with the latest from git (as of October 2011). In MSYS console:

   .. code-block:: shell

      $ ./configure --enable-static      # add options if needed, e.g: optimization, install dir, search path
      $ make && make install-lib-static  # default install dir is /usr/local

#. Optional for libvpx: `libvpx <https://www.webmproject.org/code/>`__, 
   supported since :pr:`2253`. In MSYS console:

   .. code-block:: shell

      $ ./configure --target=x86-win32-vs15 --disable-examples --disable-docs --disable-tools --disable-examples --enable-static --enable-vp8 --enable-vp9 --enable-static-msvcrt  # add options if needed, e.g: optimization, install dir, search path
      $ make    #Generate Visual Studio solution      
      #Build the static library using Visual Studio solution
      
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

* You may be able to use the binary distributions (such as from 
  `Zeranoe <http://ffmpeg.zeranoe.com/builds/>`__ - get the 'dev' builds). 
  It compiles fine, however we haven't tested them thoroughly.
* For building FFMPEG on Windows, use MSYS|MinGW. Please see :any:`/specific-guides/build_int/mingw`.
      
  .. note:: 

     * It is recommended to use gcc 4 or above to build ffmpeg.
     * To avoid problems, put MSYS, libx264, and ffmpeg in folders that do not 
       contain space, e.g: **C:\\msys, C:\\devlib\\ffmpeg**.
     * To use ffmpeg with VS, **inttypes.h** and **stdint.h** will be needed, 
       check `here <https://code.google.com/p/msinttypes/downloads/detail?name=msinttypes-r26.zip&can=2&q=>`__.

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

   #. **DirectShow SDK**
   #. SDL
   #. OpenH264
   #. libvpx

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

#. For Visual Studio 8 (VS 2005): open ``pjproject-vs8.sln`` solution file.
#. For Visual Studio 9 (VS 2008): open ``pjproject-vs8.sln`` solution file. 
   One-time conversion of projects to VS 2008 format will done automatically.
#. For Visual Studio 11 (VS 2012): open ``pjproject-vs8.sln`` solution file. 
   One-time conversion of projects to VS 2012 format will done automatically.

   #. Warnings about Windows Mobile projects/configurations can be safely ignored, 
      VS 2012 does not support Windows Mobile
   #. Additional tips from `pjsip mailing list <http://lists.pjsip.org/pipermail/pjsip_lists.pjsip.org/2012-December/015574.html>`_
   
#. For Visual Studio 14 (VS 2015): open ``pjproject-vs14.sln`` solution file.
#. For Visual Studio 15 (VS 2017): open ``pjproject-vs14.sln`` solution file.
#. For Visual Studio 16 (VS 2019): open ``pjproject-vs14.sln`` solution file.
#. Set ``pjsua`` as Active or Startup Project.
#. Set ``Win32`` as the platform.
#. Select ``Debug`` or ``Release`` build as appropriate.
#. Build the project. This will build ``pjsua`` application and all libraries 
   needed by ``pjsua``.
#. After successful build, the pjsua application will be placed in ``pjsip-apps/bin`` 
   directory, and the libraries in lib directory under each projects.

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


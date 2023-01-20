Build Instructions
===================

This page describes how to use Microsoft Visual Studio to build pjsip libraries:

.. note::
   
   You can also build for Windows using GNU tools such mingw. Follow the steps 
   in :doc:`Building with GNU Tools/Autoconf </get-started/posix/build_instructions>`. 
   Also note that video feature is currently only supported on Microsoft 
   Visual Studio build tools because some video components, 
   e.g: **DirectShow** video capture device, can only be built using 
   Visual Studio and Windows SDK.

.. note:: 

   We don't provide DLL projects for Windows, but please see 
   :doc:`Building Dynamic Link Libraries </api/generated/pjlib/group/group__pj__dll__target>` 
   page in PJLIB documentation on how to build these DLL yourself.

Build Preparation
------------------

#. :doc:`Getting the source code </get-started/getting>` if you haven't already.
#. Create :ref:`config_site.h <dev_start>`

Requirements
-------------

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

   Microsoft Visual Studio 2010 **is currently unsupported**.

   * This is because Visual Studio 2010 importer for our VS2005 solution files 
     is broken. Use Visual Studio 2012 instead.
   * Workaround tips: `#1 <http://lists.pjsip.org/pipermail/pjsip_lists.pjsip.org/2012-February/014139.html>`__ 
     and `#2 <http://lists.pjsip.org/pipermail/pjsip_lists.pjsip.org/2013-April/016083.html>`__

In addition, the following SDK's are needed:

    * Essential for other than Windows 8/Visual Studio 2012: DirectX SDK 
      (tested with DirectX version 8 and 9). After installing DirectX, add the 
      paths to the include files and the library to Visual Studio.
    * Optional if not using Visual Studio 2008: Platform SDK (tested with 
      Platform SDK for Windows Server 2003 SP1).
  
      .. hint:: 

         By using Visual Studio 2012 (or newer), there's no need to install 
         standalone Windows SDK/DirectX SDK. 
         (`ref <https://en.wikipedia.org/wiki/Microsoft_Windows_SDK>`__ and 
         `ref <https://docs.microsoft.com/en-us/windows/win32/directx-sdk--august-2009=>`__). 

    * Optional: OpenSSL development kit is needed if TLS support is wanted.

Video support (2.0 and above only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Additional requirements
```````````````````````

#. **DirectShow SDK**, included in Windows SDK. The minimum component required 
   within the SDK is **Windows Development Headers and Libraris** and **Samples**.

   * If you don't need Windows 7 features, the recommended SDK is 
     `Windows SDK Update for Windows Vista <http://www.microsoft.com/downloads/en/details.aspx?FamilyID=ff6467e6-5bba-4bf5-b562-9199be864d29>`_.
   * If you need Windows 7 features then use `Windows SDK for Windows 7 <http://www.microsoft.com/downloads/en/confirmation.aspx?FamilyID=6B6C21D2-2006-4AFA-9702-529FA782D63B>`_. 
     Also if you are using Visual Studio 2005 then you will need to patch it 
     using `MS Knowledge Base 949009 <http://support.microsoft.com/kb/949009/>`_

#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. libyuv (Recommended): Follow the instructions in :pr:`1937`. 
   Alternatively, you can use ffmpeg as explained below.
#. OpenH264 (Recommended): Follow the instructions in :pr:`1947`. Alternatively, 
   you can use ffmpeg as explained below.
#. `ffmpeg <http://ffmpeg.org/>`__ development library. ffmpeg is used for format 
   conversion and video manipulation as well as video codecs: 
   H.264 (together with libx264) and H263P/H263-1998.   
   So, if you already use libyuv AND OpenH264, and you don't need H.263, 
   then this is optional. 
   
   We tested with ffmpeg version 1.x (1.2.5) to 0.x (from 0.5.1 (from circa 2009) to 0.10). 
   Since :pr:`1897` we have added support for ffmpeg 2.8, 
   however note that on applying the ticket, older ffmpeg will no longer be supported.

   .. note::

      For H.264 support, you need newer releases (October 2011 onwards), and it needs libz too.
   
   * You may be able to use the binary distributions (such as from 
     `Zeranoe <http://ffmpeg.zeranoe.com/builds/>`_ - get the 'dev' builds). 
     It compiles fine, however we haven't tested them thoroughly.
   * Otherwise, get `MSYS|MinGW <http://www.mingw.org/wiki/MSYS>`_ for building 
     libx264 and ffmpeg. 
     
     .. note:: 

       * It is recommended to use gcc 4 or above to build ffmpeg.
       * To avoid problems, put MSYS, libx264, and ffmpeg in folders that do not 
         contain space, e.g: **C:\\msys, C:\\devlib\\ffmpeg**.
       * To use ffmpeg with VS, **inttypes.h** and **stdint.h** will be needed, 
         check `here <https://code.google.com/p/msinttypes/downloads/detail?name=msinttypes-r26.zip&can=2&q=>`__.

   * In MSYS, build with at least:
  
     .. code-block:: shell

        $ ./configure --enable-shared --disable-static --enable-memalign-hack
        # add other options if needed, e.g: optimization, install dir, search path 
        # particularly CFLAGS and LDFLAGS for x264
        # to enable H264, add "--enable-gpl --enable-libx264"
        $ make && make install

#. Optional for H.264: `libx264 <http://www.videolan.org/developers/x264.html>`_. 
   We tested with the latest from git (as of October 2011). In MSYS console:

   .. code-block:: shell

      $ ./configure --enable-static      # add options if needed, e.g: optimization, install dir, search path
      $ make && make install-lib-static  # default install dir is /usr/local

#. Optional for libvpx: `libvpx <https://www.webmproject.org/code/>`_, 
   supported since :pr:`2253`. In MSYS console:

   .. code-block:: shell

      $ ./configure --target=x86-win32-vs15 --disable-examples --disable-docs --disable-tools --disable-examples --enable-static --enable-vp8 --enable-vp9 --enable-static-msvcrt  # add options if needed, e.g: optimization, install dir, search path
      $ make    #Generate Visual Studio solution      
      #Build the static library using Visual Studio solution
      
#. Optional: `Qt development SDK <http://qt-project.org/downloads/>`_ for 
   building the video GUI sample. We tested with version 4.6 or later.
   
   * without this you can still enjoy video with pjsua console application

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

Host requirements
^^^^^^^^^^^^^^^^^

For the host, the following are required:

* Windows NT, 2000, XP, 2003, Vista, Windows 7, Windows 10, or later.
* Windows 95/98 should work too, but this has not been tested,

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

Using pjproject libraries for your own application
---------------------------------------------------

#. Put these include directories in the include search path of your project:

   * pjlib/include
   * pjlib-util/include
   * pjnath/include
   * pjmedia/include
   * pjsip/include

#. Put the combined library directory **lib** (located in the root directory of 
   pjproject source code) in the library search path
#. Include the relevant PJ header files in the application source file. 
   For example, using these would include ALL APIs exported by PJ:

   .. code-block:: c

      #include <pjlib.h>
      #include <pjlib-util.h>
      #include <pjnath.h>
      #include <pjsip.h>
      #include <pjsip_ua.h>
      #include <pjsip_simple.h>
      #include <pjsua-lib/pjsua.h>
      #include <pjmedia.h>
      #include <pjmedia-codec.h>

   .. note::

      The documentation of the relevant libraries should say which header files 
      should be included to get the declaration of the APIs).

#. Declare PJ_WIN32=1 macro in the project settings (declaring the macro in the 
   source file may not be sufficient).

#. Link with the main pjproject library ``libpjproject``. It includes all the 
   libraries provided. 

   .. note::

      The actual library names will be appended with the target name and the 
      build configuration. For example: The actual library names will look 
      like ``libpjproject-i386-win32-vc6-debug.lib`` depending on whether 
      we are building the Debug or Release version of the library.

#. Link with system specific libraries such as: wsock32.lib, ws2_32.lib, ole32.lib, 
   dsound.lib

#. If you want to use video API see `Video Users Guide <http://trac.pjsip.org/repos/wiki/Video_Users_Guide>`_

Windows on ARM Support
----------------------

Please refer to :pr:`2807` for more information.

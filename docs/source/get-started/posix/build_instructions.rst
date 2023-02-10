Build Instructions with GNU Build Systems
=======================================================================================

.. contents:: Table of Contents
    :depth: 3


Supported Targets
-----------------

The autoconf based GNU build system can be used to build the libraries/applications 
for the following targets:

* Linux/uC-Linux (i386, Opteron, Itanium, MIPS, PowerPC, etc.),
* MacOS X (PowerPC, Intel, Apple M),
* mingw/mingw-w64(i386),
* FreeBSD and maybe other BSD's (i386, Opteron, etc.),
* RTEMS with cross compilation (ARM, powerpc),
* etc.


Requirements
-------------

Tools and development libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use PJSIP's GNU build system, these typical GNU tools are needed:

* GNU make (other make will not work),
* GNU binutils for the target, and
* GNU gcc for the target.

In addition, the following libraries are optional, but they will be used if they 
are present:

* (For Linux): ALSA header files/libraries (optional) if ALSA support is wanted. 
  To install, use the command: ``apt-get install libasound2-dev`` 
  or ``apt-get install alsa-lib-devel`` (depending on the distribution).
* OpenSSL header files/libraries (optional) if TLS support is wanted.


Video Support (for 2.0 and above)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following components are needed for video:

#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. For format conversion and video manipulation, you can use one of the following:

   * :any:`libyuv <guide_libyuv>` (recommended) for format conversion and video manipulation. 
     If you are using PJSIP 2.5.5 or newer, libyuv should be built and enabled 
     automatically.
   * :ref:`FFMPEG <ffmpeg>`.
  
#. For video codecs:

   * H263.
     
     Get :ref:`FFMPEG <ffmpeg>`.
   
   * H264. 
    
     You can use one of the following:

     * OpenH264 (Recommended): Follow the instructions in :ref:`openh264`. 
       Alternatively, you can use **VideoToolbox** (only for Mac) or ffmpeg as 
       explained below.
     * For Mac only: **VideoToolbox** (supported since PJSIP version 2.7). Define this in your :any:`config_site.h`: 

       .. code-block:: c

          #define PJMEDIA_HAS_VID_TOOLBOX_CODEC 1

     * Get :ref:`FFMPEG <ffmpeg>` development library, using libx264. We tested with ffmpeg 
       version 1.x (1.2.5) to 0.x (from 0.5.1 (from circa 2009) to 0.10). 
       
       Since :pr:`1897` we have added support for ffmpeg 2.8, however note that 
       on applying the ticket, older ffmpeg will no longer be supported. 
       To enable H.264 support in ffmpeg (this is not required if you already 
       have H.264 codec (via OpenH264 or **VideoToolbox**)):
       
       * You need newer releases (October 2011 onwards), and it needs libz too. 
         On Mac OS X: You may need to rebuild libbz2 if you have an old libbz2 
         for older system.
       * Build with at least:

         .. code-block:: shell

            $ ./configure --enable-shared --disable-static --enable-memalign-hack
            # add other options if needed, e.g: optimization, install dir, search path 
            # particularly CFLAGS and LDFLAGS for x264
            # to enable H264, add "--enable-gpl --enable-libx264"
            $ make && make install
        
     * Get `libx264 <http://www.videolan.org/developers/x264.html>`__. We tested 
       with the latest from git (as of October 2011):

          .. code-block:: shell

             $ ./configure --enable-static      # add options if needed, e.g: optimization, install dir, search path
             $ make && make install-lib-static  # default install dir is /usr/local

   * VP8 and VP9, see :ref:`libvpx`

#. Linux: Video4Linux2 (v4l2) development library.
#. Optional: `Qt development SDK <http://qt.nokia.com/downloads/>`__ for building 
   the :source:`vidgui <pjsip-apps/src/vidgui/>`. We tested with version 4.6 or 
   later.
   
   .. note:: 

      Without this you can still enjoy video with pjsua console application

Host requirements
^^^^^^^^^^^^^^^^^

The build system is known to work on the following hosts:

* Linux, many types of distributions.
* MacOS X 10.2
* mingw/mingw-w64 (Win2K, XP)
* FreeBSD (must use gmake instead of make)

Building Win32 applications with Cygwin is currently not supported by the 
autoconf script (there are some conflicts with Windows headers), but one can 
still use the old configure script by calling ``./configure-legacy``. 

More over, cross-compilations might also work with Cygwin using this build 
system.

Mingw-w64 is supported since 2.11, including video with DirectShow camera, 
please check :pr:`2598` for more info.

.. _configure:

``./configure``
------------------

Running ``./configure``.

Using Default Settings
^^^^^^^^^^^^^^^^^^^^^^

Run "./configure" without any options to let the script detect the appropriate 
settings for the host:

.. code-block:: shell

   $ cd pjproject
   $ ./configure

.. note:: 
   
   The default settings build the libraries in **release** mode, with default 
   CFLAGS set to "-O2". To change the default CFLAGS, 
   we can use the usual ``./configure CFLAGS='-g'`` construct. 

Configure with Video Support
`````````````````````````````

Add this to your ``config_site.h``:

.. code-block:: c

   #define PJMEDIA_HAS_VIDEO	1

Video requirements will be detected by the ``configure`` script. 
Pay attention to the following output (the sample below was taken on a Mac):

.. code-block:: 

   ...
   Using SDL prefix... /Users/pjsip/Desktop/opt
   checking SDL availability..... 2.0.1
   Using ffmpeg prefix... /Users/pjsip/Desktop/opt
   checking for pkg-config... no
   checking for python... python pkgconfig.py
   checking ffmpeg packages...  libavformat libavcodec libswscale libavutil
   checking for v4l2_open in -lv4l2... no
   checking OpenH264 availability... ok
   checking for I420Scale in -lyuv... yes
   ...

The above output shows the SDL version detected, 2.0.1 in this case. It also 
found OpenH264, libyuv, and ffmpeg packages (libavformat, libavcodec, etc). 

.. note:: 
   
   For this particular build, alternative locations (prefixes) are specified 
   for both SDL and ffmpeg with ``--with-sdl`` and ``-with-ffmpeg`` options 
   respectively. 

.. note:: 

   Regarding ffmpeg libraries dependencies:

   The *pkg-config* tool is used to detect the correct compilation settings and 
   library dependency for the ffmpeg packages. The *pkg-config* is not installed 
   by default on Mac, as the output above shows, hence we use the alternate 
   *pkgconfig.py* script. 
   
   You need to have Python installed to run this script of course, and the 
   configure script detects its availability automatically. 
   
   If Python is not available, you will need to supply the correct CFLAGS and 
   LDFLAGS manually prior to running ``configure`` so that it is able to detect 
   ffmpeg libraries.
   
   For example, if ffmpeg was built with x264 and mp3 encoder support, 
   you will need to pass additional ``-lx264 -lmp3lame``flags when linking libavformat. 
   With manual checking in the configure script, the ``AC_CHECK_LIB(avformat)`` 
   would not be able to detect that it needs to add ``-lx264 -lmp3lame`` 
   as the dependency, hence you need to put this in the LDFLAGS prior to 
   running configure.

Features Customization
^^^^^^^^^^^^^^^^^^^^^^^

With the new autoconf based build system, most configuration/customization can 
be specified as configure arguments. 
The list of customizable features can be viewed by running ``./configure --help`` 
command:

.. code-block:: shell

   $ cd pjproject
   $ ./configure --help

Optional Features:

.. code-block:: shell

   --disable-floating-point   Disable floating point where possible
   --disable-sound            Exclude sound (i.e. use null sound)
   --disable-small-filter     Exclude small filter in resampling
   --disable-large-filter     Exclude large filter in resampling
   --disable-g711-plc         Exclude G.711 Annex A PLC
   --disable-speex-aec        Exclude Speex Acoustic Echo Canceller/AEC
   --disable-g711-codec       Exclude G.711 codecs from the build
   --disable-l16-codec        Exclude Linear/L16 codec family from the build
   --disable-gsm-codec 	      Exclude GSM codec in the build
   --disable-speex-codec      Exclude Speex codecs in the build
   --disable-ilbc-codec       Exclude iLBC codec in the build
   --disable-ssl              Force excluding TLS support (default is autodetected based on OpenSSL availability)
   --disable-sdl              Disable SDL (default: not disabled)
   --disable-ffmpeg           Disable ffmpeg (default: not disabled)
   --disable-v4l2             Disable Video4Linux2 (default: not disabled)
   --disable-openh264         Disable OpenH264 (default: not disabled)
   --disable-libyuv           Exclude libyuv in the build
	
Configuring Debug Version and Other Customizations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The configure script accepts standard customization, which details can be obtained 
by executing ``./configure --help``.

Below is an example of specifying CFLAGS in configure:
  	
.. code-block:: 

   $ ./configure CFLAGS="-O3 -DNDEBUG -msoft-float -fno-builtin"

.. _posix_openssl:

Configuring TLS Support
^^^^^^^^^^^^^^^^^^^^^^^

By default, TLS support is configured based on the availability of OpenSSL 
header files and libraries. If OpenSSL is available at the default include and 
library path locations, TLS will be enabled by the configure script.

You can explicitly disable TLS support by giving the configure script ``--disable-ssl`` 
option.

For MacOS or iOS platforms, native SSL backend using Network framework is also 
supported, please check :pr:`2482` for more info.

Cross Compilation
------------------

General
^^^^^^^^

Cross compilation should be supported, using the usual autoconf syntax:

.. code-block:: 

   $ ./configure --host=arm-elf-linux

Since cross-compilation is not tested as often as the "normal" build, please watch 
for the ``./configure`` output for incorrect settings (well ideally this should 
be done for normal build too).

Please refer to Porting Guide for further information about porting PJ software.

Building for MacOS x86_64 on MacOS M1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run configure script:

.. code-block:: shell

   $ CFLAGS="-arch x86_64" LDFLAGS="-arch x86_64" ./configure --host=x86_64-apple-darwin

Building for MacOS M1 on MacOS x86_64
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run configure script:

.. code-block:: shell

   $ CFLAGS="-arch arm64" LDFLAGS="-arch arm64" ./configure --host=arm-apple-darwin

Running make
-------------

Once the configure script completes successfully, start the build process by 
invoking these commands:

.. code-block:: shell

   $ cd pjproject
   $ make dep
   $ make

.. note:: 
   
   **gmake** may need to be specified instead of **make** for some hosts, to 
   invoke GNU **make** instead of the native **make**. 

Description of all make targets supported by the Makefile's:

.. list-table::
   :header-rows: 0

   * - all
     - The default (or first) target to build the libraries/binaries.
   * - dep, depend
     - Build dependencies rule from the source files.
   * - clean
     - Clean the object files for current target, but keep the output 
       library/binary files intact.
   * - distclean, realclean
     - Remove all generated files (object, libraries, binaries, and dependency 
       files) for current target.

.. note:: 

   **make** can be invoked either in the top-level PJ directory or in build 
   directory under each project to build only the particular project.

Build Customizations
---------------------

Build features can be customized by specifying the options when running 
``./configure`` as described in Running Configure above.

In addition, additional CFLAGS and LDFLAGS options can be put in user.mak file 
in PJ root directory (this file may need to be created if it doesn't exist). 
Below is a sample of ``user.mak`` file contents:

.. code-block:: shell

   export CFLAGS += -msoft-float -fno-builtin
   export LDFLAGS +=

Optional: Installing PJSIP
---------------------------

Run ``make install`` to install the header and library files to the targt directory. 
The default target directory can be customized by specifying ``--prefix=DIR`` 
option to ``configure`` script.

.. code-block:: shell

   $ make install

Using pjsip libraries in your applications
-------------------------------------------

Steps for Building Your Application that Uses PJSIP/PJMEDIA:

#. First, build ``pjproject`` libraries as described above. This normally is 
   accomplished by executing these commands:

   .. code-block:: shell

      $ ./configure && make dep && make

#. Create a directory outside the PJSIP sources for your project and place your 
   source files there.
#. Create a file named **Makefile** in your source directory:
 
   -  After you run ``make install``, **and** you have **pkg-config** tool, 
      you can use this template for your Makefile:

      .. code-block:: makefile

         # If your application is in a file named myapp.cpp or myapp.c
         # this is the line you will need to build the binary.
         all: myapp

         myapp: myapp.cpp
            $(CC) -o $@ $< `pkg-config --cflags --libs libpjproject`

         clean:
            rm -f myapp.o myapp

#. There few things to note when making the **Makefile** above:

   #. First, make sure that you replace **PJBASE** with the location of PJSIP 
      sources in your computer.
   #. If you notice there are spaces towards the bottom of the file 
      (before ``$(CC)`` and ``rm``, these are a single tab, not spaces. 
      **This is important**, or otherwise **make** command will fail
      with "**missing separator**" error.
   #. Change ``myapp.cpp`` to your source filename.

#. Create ``myapp.cpp`` in the same directory as your ``Makefile``. At minimum, 
   it may look like this:

   .. code-block:: c

      #include <pjlib.h>
      #include <pjlib-util.h>
      #include <pjmedia.h>
      #include <pjmedia-codec.h>
      #include <pjsip.h>
      #include <pjsip_simple.h>
      #include <pjsip_ua.h>
      #include <pjsua-lib/pjsua.h>

      int main()
      {
            return 0;
      }

#. Last, run **make** in your source directory.

You can also go to `Video Users Guide <http://trac.pjsip.org/repos/wiki/Video_Users_Guide>`__ 
for video usage instructions for pjsip version 2.x.

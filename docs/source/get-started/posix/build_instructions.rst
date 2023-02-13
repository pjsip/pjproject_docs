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
* :any:`mingw/mingw-w64 </specific-guides/build_int/mingw>`
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

* (For Linux): ALSA (recommended). See :ref:`alsa`.
* SSL libraries such as OpenSSL, GnuTLS, or BoringSSL (Mac/iOS can use
  native SSL). See :any:`/specific-guides/security/ssl`


Video Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following components are needed for video:

#. `SDL <http://www.libsdl.org/>`__ **version 2.0**
#. For format conversion and video manipulation, you can use one of the following:

   * libyuv (recommended). See :any:`libyuv <guide_libyuv>`.
     Alternatively, you can use ffmpeg below.
   * :ref:`FFMPEG <ffmpeg>`.
  
#. For video codecs:

   * H263: get :ref:`FFMPEG <ffmpeg>`.
   * H264: choose one of the following:
    
     * :ref:`openh264`. 
     * **VideoToolbox** (for Mac and iOS only). Define this in your :any:`config_site.h`: 

       .. code-block:: c

          #define PJMEDIA_HAS_VID_TOOLBOX_CODEC 1

     * :ref:`FFMPEG <ffmpeg>`
     * `libx264 <http://www.videolan.org/developers/x264.html>`__

   * VP8 and VP9, see :ref:`libvpx`

#. Linux: Video4Linux2 (v4l2) development library.
#. Optional: `Qt development SDK <http://qt.nokia.com/downloads/>`__ for building 
   the :source:`vidgui <pjsip-apps/src/vidgui/>`. We tested with version 4.6 or 
   later.
   
   .. note:: 

      Without this you can still enjoy video with pjsua console application

   .. tip:: 

      For more information about using the video, see :any:`/specific-guides/video/users_guide`


Host requirements
^^^^^^^^^^^^^^^^^

The build system is known to work on the following hosts:

* Linux, many types of distributions.
* MacOS X 10.2
* :any:`mingw/mingw-w64 </specific-guides/build_int/mingw>`
* FreeBSD (must use gmake instead of make)

.. _configure:

./configure
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

Add this to your :any:`config_site.h`:

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

Configuration/customization can be specified as configure arguments. 
The list of customizable features can be viewed by running ``./configure --help`` 
command:

.. code-block:: shell

   $ cd pjproject
   $ ./configure --help

The following shows output from PJSIP version 2.13:

::

   Optional Features:
      --disable-option-checking  ignore unrecognized --enable/--with options
      --disable-FEATURE       do not include FEATURE (same as --enable-FEATURE=no)
      --enable-FEATURE[=ARG]  include FEATURE [ARG=yes]
      --disable-libuuid       Exclude libuuid(default: autodetect)
      --disable-floating-point
                              Disable floating point where possible
      --enable-kqueue         Use kqueue ioqueue on macos/BSD (experimental)
      --enable-epoll          Use /dev/epoll ioqueue on Linux (experimental)
      --enable-shared         Build shared libraries
      --disable-pjsua2        Exclude pjsua2 library and application from the
                              build
      --disable-upnp          Disable UPnP (default: not disabled)
      --disable-resample      Disable resampling implementations
      --disable-sound         Exclude sound (i.e. use null sound)
      --disable-video         Disable video feature
      --enable-ext-sound      PJMEDIA will not provide any sound device backend
      --disable-small-filter  Exclude small filter in resampling
      --disable-large-filter  Exclude large filter in resampling
      --disable-speex-aec     Exclude Speex Acoustic Echo Canceller/AEC
      --disable-g711-codec    Exclude G.711 codecs from the build
      --disable-l16-codec     Exclude Linear/L16 codec family from the build
      --disable-gsm-codec     Exclude GSM codec in the build
      --disable-g722-codec    Exclude G.722 codec in the build
      --disable-g7221-codec   Exclude G.7221 codec in the build
      --disable-speex-codec   Exclude Speex codecs in the build
      --disable-ilbc-codec    Exclude iLBC codec in the build
      --enable-libsamplerate  Link with libsamplerate when available.
      --enable-resample-dll   Build libresample as shared library
      --enable-speex-resample Enable Speex resample
      --disable-sdl           Disable SDL (default: not disabled)
      --disable-ffmpeg        Disable ffmpeg (default: not disabled)
      --disable-v4l2          Disable Video4Linux2 (default: not disabled)
      --disable-openh264      Disable OpenH264 (default: not disabled)
      --disable-vpx           Disable VPX (default: not disabled)
      --enable-ipp            Enable Intel IPP support. Specify the Intel IPP
                              package and samples location using IPPROOT and
                              IPPSAMPLES env var or with --with-ipp and
                              --with-ipp-samples options
      --disable-android-mediacodec
                              Exclude Android MediaCodec (default: autodetect)
      --disable-darwin-ssl    Exclude Darwin SSL (default: autodetect)
      --disable-ssl           Exclude SSL support the build (default: autodetect)

      --disable-opencore-amr  Exclude OpenCORE AMR support from the build
                              (default: autodetect)

      --disable-silk          Exclude SILK support from the build (default:
                              autodetect)

      --disable-opus          Exclude OPUS support from the build (default:
                              autodetect)

      --disable-bcg729        Disable bcg729 (default: not disabled)
      --disable-libsrtp       Exclude libsrtp in the build
      --disable-libyuv        Exclude libyuv in the build
      --disable-libwebrtc     Exclude libwebrtc in the build
      --enable-libwebrtc-aec3 Build libwebrtc-aec3 that's included in PJSIP

   Optional Packages:
      --with-PACKAGE[=ARG]    use PACKAGE [ARG=yes]
      --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
      --with-upnp=DIR         Specify alternate libupnp prefix
      --with-external-speex   Use external Speex development files, not the one in
                              "third_party" directory. When this option is set,
                              make sure that Speex is accessible to use (hint: use
                              CFLAGS and LDFLAGS env var to set the include/lib
                              paths)
      --with-external-gsm     Use external GSM codec library, not the one in
                              "third_party" directory. When this option is set,
                              make sure that the GSM include/lib files are
                              accessible to use (hint: use CFLAGS and LDFLAGS env
                              var to set the include/lib paths)
      --with-external-srtp    Use external SRTP development files, not the one in
                              "third_party" directory. When this option is set,
                              make sure that SRTP is accessible to use (hint: use
                              CFLAGS and LDFLAGS env var to set the include/lib
                              paths)
      --with-external-yuv     Use external libyuv development files, not the one
                              in "third_party" directory. When this option is set,
                              make sure that libyuv is accessible to use (hint:
                              use CFLAGS and LDFLAGS env var to set the
                              include/lib paths)
      --with-external-webrtc  Use external webrtc development files, not the one
                              in "third_party" directory. When this option is set,
                              make sure that webrtc is accessible to use (hint:
                              use CFLAGS and LDFLAGS env var to set the
                              include/lib paths)
      --with-external-webrtc-aec3
                              Use external webrtc AEC3 development files, not the
                              one in "third_party" directory. When this option is
                              set, make sure that webrtc is accessible to use
                              (hint: use CFLAGS and LDFLAGS env var to set the
                              include/lib paths)
      --with-external-pa      Use external PortAudio development files. When this
                              option is set, make sure that PortAudio is
                              accessible to use (hint: use CFLAGS and LDFLAGS env
                              var to set the include/lib paths)
      --with-oboe             Enable Android Oboe audio device backend.
      --with-sdl=DIR          Specify alternate libSDL prefix
      --with-ffmpeg=DIR       Specify alternate FFMPEG prefix
      --with-openh264=DIR     Specify alternate OpenH264 prefix
      --with-vpx=DIR          Specify alternate VPX prefix
      --with-ipp=DIR          Specify the Intel IPP location
      --with-ipp-samples=DIR  Specify the Intel IPP samples location
      --with-ipp-arch=ARCH    Specify the Intel IPP ARCH suffix, e.g. "64" or
                              "em64t. Default is blank for IA32"
      --with-ssl=DIR          Specify alternate SSL library prefix. This option
                              will try to find OpenSSL first, then if not found,
                              GnuTLS. To skip OpenSSL finding, use --with-gnutls
                              option instead.
      --with-gnutls=DIR       Specify alternate GnuTLS prefix
      --with-opencore-amrnb=DIR
                              This option is obsolete and replaced by
                              --with-opencore-amr=DIR
      --with-opencore-amr=DIR Specify alternate libopencore-amr prefix
      --with-opencore-amrwbenc=DIR
                              Specify alternate libvo-amrwbenc prefix
      --with-silk=DIR         Specify alternate SILK prefix
      --with-opus=DIR         Specify alternate OPUS prefix
      --with-bcg729=DIR       Specify alternate bcg729 prefix	

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

See :any:`/specific-guides/security/ssl`

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
   
   **gmake** may need to be specified instead of **make** for some hosts to 
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

In addition, additional CFLAGS and LDFLAGS options can be put in ``user.mak`` file 
in PJ root directory (this file may need to be created if it doesn't exist). 
See an example in :source:`user.mak.sample` file:

.. code-block:: shell

   export CFLAGS += -msoft-float -fno-builtin
   export LDFLAGS +=

Optional: Installing PJSIP
---------------------------

Run ``make install`` to install the header and library files to the target directory. 
The default target directory can be customized by specifying ``--prefix=DIR`` 
option to ``configure`` script.

.. code-block:: shell

   $ make install


.. _guide_ffmpeg:

Adding FFMPEG support
=======================
PJMEDIA can make use of the following FFMPEG **development** components:

- libavutil
- libavformat
- libavcodec
- libavdevice
- libswscale

Installation
-----------------
PJMEDIA by default supports FFMPEG version 2.8 or newer 
(see `#1897 <https://github.com/pjsip/pjproject/issues/1897>`_). Using older version of
FFMPEG is possible, see the ticket for information.

The instructions to install the above development packages vary.

Debian based distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

   sudo apt-get install libavutil-dev libavformat-dev libavcodec-dev libavdevice-dev libswscale-dev

.. note::
   
   See the list of FFMPEG packages in https://launchpad.net/ubuntu/+source/ffmpeg


Windows
^^^^^^^^^^^^^^
TBD.


Building PJPROJECT with FFMPEG support
----------------------------------------

Autoconf build system
^^^^^^^^^^^^^^^^^^^^^^^^^
#. FFMPEG will be detected automatically by ``configure``, or explicitly with
   ``--with-ffmpeg=DIR`` option. Notice the output:

   .. code-block:: shell

      ...
      checking ffmpeg packages...  libavdevice libavformat libavcodec libswscale libavutil
      ...

   Note that support can be explicitly disabled with ``--disable-ffmpeg`` option.

#. Add video support and **support of ffmpeg capture device** to ``config_site.h``:

   .. code-block:: c

      #define PJMEDIA_HAS_VIDEO             1
      #define PJMEDIA_VIDEO_DEV_HAS_FFMPEG  1


Visual Studio
^^^^^^^^^^^^^^^^^^^^^^^^^
#. Make sure FFMPEG headers and libraries are installed in locations that can be
   found by MSVC projects
#. Add video and FFMPEG support to ``config_site.h``:

   .. code-block:: c

      #define PJMEDIA_HAS_VIDEO   1
      #define PJMEDIA_HAS_FFMPEG  1

   .. note::
      
      The above assumes that all FFMPEG components (libavcodecs, libavformat, etc)
      above are installed. If only partial components are installed, you will need to 
      specify the availability of each components (see ``PJMEDIA_HAS_LIBAVFORMAT`` and
      friends in `pjmedia/config.h <https://github.com/pjsip/pjproject/blob/master/pjmedia/include/pjmedia/config.h>`_)

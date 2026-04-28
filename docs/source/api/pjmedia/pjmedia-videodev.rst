PJMEDIA-VideoDev
---------------------------------------------

PJMEDIA Video Device API is PJMEDIA framework for cross-platform video
device abstraction, with focus to video streaming applications.


API Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- :doc:`Portable Video Device API </api/generated/pjmedia/group/group__video__device__reference>`
- :doc:`Implementor's API </api/generated/pjmedia/group/group__s8__video__device__implementors__api>`
- :doc:`Error Codes </api/generated/pjmedia/group/group__error__codes>`


Supported devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: ../../common/common_videodev.rst


.. _android_cam:

Android Camera2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a capture device based on `Android Camera2 framework <https://developer.android.com/training/camera2>`__. 
Support for this device is enabled automatically for Android build (reference: 
``PJMEDIA_VIDEO_DEV_HAS_ANDROID=1`` macro).

References:

- https://github.com/pjsip/pjproject/pull/2797
- https://github.com/pjsip/pjproject/issues/1822


.. _avi_device:

AVI virtual device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Virtual camera device that reads video from AVI file, enabling streaming of AVI files.

- Code documentation: :doc:`AVI Player Virtual Device </api/generated/pjmedia/group/group__avi__dev>`

.. _avfoundation:

AVFoundation (Mac and iOS) and UIView (iOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AVFoundation capture device is available on Mac OS X and iOS. UIView renderer is
available on iOS. These devices are enabled automatically if ``PJMEDIA_HAS_VIDEO``
is set to ``1`` for Mac OS and iOS build.


.. _colorbar:

Colorbar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A very basic virtual camera that outputs colorbar. Useful for initial porting to new
platform.


.. _dshow:

DirectShow (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On Visual Studio, add this in ``config_site.h`` to enable it:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_DSHOW  1

Experimental: with Mingw64, enable it with ``./configure --enable-video=yes`` 
(see https://github.com/pjsip/pjproject/pull/2589).


.. _ffmpeg_capture:

FFMPEG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PJMEDIA uses FFMPEG to provide codecs and video capture device.

See :ref:`guide_ffmpeg`.


.. _metal:

Metal (Mac and iOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Metal-based renderer for Mac OS X and iOS, using Apple's Metal and MetalKit
frameworks. Enabled automatically when the Metal framework is detected by the
``configure`` script (reference: ``PJMEDIA_VIDEO_DEV_HAS_METAL=1`` macro).


.. _opengl:

OpenGL (desktops)/OpenGL ES 2 (Android, iOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The OpenGL renderer can be used wheverer OpenGL SDK is available (Windows, Mac OS X,
Linux, and so on). The OpenGL ES is available on iOS and Android.

To enable OpenGL in the build, declare this in ``config_site.h``:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_OPENGL     1

In addition to above, declare these to use OpenGL ES:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_OPENGL_ES  1

And add this for iOS:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_IOS_OPENGL 1


References: 

- https://github.com/pjsip/pjproject/issues/1757
- https://github.com/pjsip/pjproject/issues/1790

.. _qtdev:

QuickTime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   Note that QuickTime has been deprecated in favor of AVFoundation framework.
   See :ref:`avfoundation`

This device implement QT capture for Mac and capture and render devices
for iOS.

References:

- https://github.com/pjsip/pjproject/issues/1183


.. _sdl:

SDL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Quoting http://www.libsdl.org/ website:

   *Simple DirectMedia Layer is a cross-platform development library designed to 
   provide low level access to audio, keyboard, mouse, joystick, and graphics 
   hardware via OpenGL and Direct3D*

In PJMEDIA, currently we use SDL as renderer device.

.. _guide_sdl:

Adding SDL support
^^^^^^^^^^^^^^^^^^^^
On Debian based distributions:

.. code-block:: shell

   sudo apt-get install libsdl2-dev

For other systems, follow the instructions in http://www.libsdl.org/. Make sure
headers and libraries are accessible in build search paths after installation.

Building PJPROJECT with SDL support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**autoconf build system**

With the ``configure`` script, SDL support can be detected and enabled automatically,
or explicitly with ``--with-sdl=DIR`` option.

Notice the following output:

.. code-block::

   checking for sdl2-config... /usr/bin/sdl2-config
   checking SDL availability... 2.0.10

Note that support can be explicitly disabled with ``--disable-sdl`` option.

**Visual Studio**

Declare this in  ``config_site.h`` and rebuild:

.. code-block:: cpp

   #define PJMEDIA_VIDEO_DEV_HAS_SDL     1


Using OpenGL with SDL
^^^^^^^^^^^^^^^^^^^^^

PJSIP also supports an OpenGL-backed renderer on top of SDL. To enable
it:

1. Install the OpenGL development headers and the SDL2 development
   package for your system. On Debian/Ubuntu (recent enough to ship
   ``libsdl2-dev``):

   .. code-block:: shell

      sudo apt-get install libgl-dev libsdl2-dev

   ``libsdl2-dev`` already pulls in OpenGL on most distributions, so
   the ``libgl-dev`` line is usually optional. Other platforms
   typically install OpenGL via the system SDK and SDL2 from
   `libsdl.org <https://www.libsdl.org/>`__.

2. Enable SDL OpenGL support in PJSIP by declaring this in your
   :ref:`config_site.h`:

   .. code-block:: c

      #define PJMEDIA_VIDEO_DEV_SDL_HAS_OPENGL    1

3. Link the OpenGL library into your application. With the GNU build
   system, add to ``user.mak`` in the root PJSIP directory:

   .. code-block::

      export LDFLAGS += -lGL

4. Rebuild PJSIP. The **"SDL OpenGL renderer"** device will then show
   up in the video device list — just use it as the renderer.


.. _video4linux:

Video4Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _guide_video4linux:

Adding Video4Linux support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On Debian based systems:

.. code-block:: shell

   sudo apt-get install libv4l-dev

For other systems, find the appropriate instructions. Make sure
headers and libraries are accessible in build search paths after installation.

Building PJPROJECT with V4L support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**autoconf build system**

With the ``configure`` script, support is detected and enabled automatically.
Notice the following output:

.. code-block::

   checking for v4l2_open in -lv4l2... yes

Support for V4L can be disabled by explicitly specifying ``--disable-v4l2``.


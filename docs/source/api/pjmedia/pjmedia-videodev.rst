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

This is a capture device based on `Android Camera2 framework <https://developer.android.com/training/camera2>`_. 
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
The ffmpeg capture device is available where ffmpeg support is available. 
With the ``configure`` script, ffmpeg may be detected and enabled 
automatically or manually via ``--with-ffmpeg`` option.

With Visual Studio, to enable ffmpeg support you need to make sure that
ffmpeg headers and libraries are available in standard location and
declare this in ``config_site.h``:

.. code-block:: c

   #define PJMEDIA_HAS_VIDEO   1
   #define PJMEDIA_HAS_FFMPEG  1

To enable ffmpeg capture device, add this in  ``config_site.h``:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_FFMPEG  1


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

With the ``configure`` script, SDL support is detected and enabled automatically.

With Visual Studio, to enable SDL renderer in the build declare this in 
``config_site.h``:

.. code-block:: c

   #define PJMEDIA_VIDEO_DEV_HAS_SDL     1


.. _video4linux:

Video4Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Video4Linux capture device is detected and enabled automatically by the
``configure`` script.

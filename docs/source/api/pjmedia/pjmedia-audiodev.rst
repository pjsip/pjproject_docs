PJMEDIA-AudioDev
---------------------------------------------

Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PJMEDIA Audio Device API is a cross-platform audio API appropriate for use with VoIP applications 
and other types of audio streaming applications.

.. include:: ../../common/common_audiodev.rst

Core features supported by PJMEDIA Audio Device API:

- Forward compatibility:

  The new API has been designed to be extensible, it will support new API’s as well as new features 
  that may be introduced in the future without breaking compatibility with applications that use 
  this API as well as compatibility with existing device implementations.

- Device capabilities:

  At the heart of the API is device capabilities management, where all possible audio capabilities 
  of audio devices should be able to be handled in a generic manner. With this framework, new 
  capabilities that may be discovered in the future can be handled in manner without breaking 
  existing applications.

- Built-in features:

  The device capabilities framework enables applications to use and control audio features built-in 
  in the device, such as:

    - audio format,
    - echo cancellation,
    - built-in codecs,
    - audio routing (e.g. to earpiece or loudspeaker),
    - volume control,
    - latency control,
    - volume meter,
    - voice activity detector,
    - comfort noise

- Codec support:

  Some audio devices such as Nokia/Symbian Audio Proxy Server (APS) and Nokia VoIP Audio Services (VAS) 
  support built-in hardware audio codecs (e.g. G.729, iLBC, and AMR), and application can use the sound 
  device in encoded mode to make use of these hardware codecs.

- Multiple backends:

  The new API supports multiple audio backends (called factories or drivers in the code) to be active 
  simultaneously, and audio backends may be added or removed during run-time.


Using the Audio Device API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :doc:`Using Audio Device API </api/generated/pjmedia/group/group__audio__device__api>`


API Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- :doc:`Audio Device API </api/generated/pjmedia/group/group__PJMEDIA__AUDIODEV__API>`
- :doc:`Implementor's API </api/generated/pjmedia/group/group__PJMEDIA__AUDIODEV__SUBSYSTEM__API>`: this
  is the API for developers that are implementing new sound device abstraction for the AudioDev framework.
- :doc:`Error Codes </api/generated/pjmedia/group/group__error__codes>`
- :doc:`Audio Test/Benchmark Utility </api/generated/pjmedia/group/group__s30__audio__test__utility>`


Supported devices:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _audiodev_supported_devs:

Follow the instructions below to enable the device. TBD.

.. _alsa:

ALSA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ALSA support is detected and enabled automatically by the ``configure`` script. Check the 
``configure`` output for ALSA detection::

  checking for alsa/version.h... yes
  Checking sound device backend... alsa

If ALSA is not detected, make sure ALSA development package is installed (e.g. on Debian 
it's ``libasound2-dev``).

Once ALSA is built, you should see ALSA device detection results on pjsua log level 5 
like this::

  $ pjsip-apps/bin/pjsua-x86_64-unknown-linux-gnu --log-level 5
  ..
  07:46:25.081             alsa_dev.c  ..ALSA driver found 32 devices
  07:46:25.081             alsa_dev.c  ..ALSA initialized
  ..


.. _opensl:

Android OpenSL (deprecated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that Android OpenSL ES has been deprecated in favor of :ref:`oboe`.


.. _jnisound:

Android JNI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _oboe:

Android Oboe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
From `Oboe GitHub page <https://github.com/google/oboe>`__: *"Oboe is a 
C++ library which makes it easy to build high-performance audio apps on 
Android"*. PJMEDIA support Oboe audio capture and playback device.

- Integration instructions: see https://github.com/pjsip/pjproject/pull/2707


.. _bdsound:

bdIMAD by BdSound
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

bdIMAD (BdSound IMproved Audio Device) is bdSound advanced audio device for 
PJSIP, supporting advanced speech processing features such as Full Duplex Acoustic Echo 
Cancellation, Noise Reduction, Automatic Level Control, Loudness Manager, 
Adaptive Comfort Noise)

This driver supports Windows, Mac OS X, Linux, Embedded Linux, Windows Embedded,
iOS, and Android. Please see http://www.bdsound.com/support/category/bdimad/ for most 
up to to date information and instructions on how to use it.

.. _coreaudio:

CoreAudio (Mac OS X and iPhone)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TBD.

.. _wmme:

WMME (Windows and Windows Mobile devices)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WMME is Windows Multimedia API that is available in every Windows operating systems.
PJMEDIA has native support for WMME audio device.

To enable WMME suport, add this to your ``config_site.h``:

.. code-block:: c

   #define PJMEDIA_AUDIO_DEV_HAS_WMME  1


And rebuild the Visual Studio project.


.. _wasapi:

WASAPI (Windows Audio Session API)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WASAPI will be used by following the instructions in
:any:`Getting started for Windows Phone</get-started/windows-phone/build_instructions>`.


No longer supported devices:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _portaudio:


PortAudio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PortAudio (PA) is a open source portable audio device abstraction by http://portaudio.com/.  
It supports Windows, Macintosh OS X, and Unix (OSS/ALSA). Since PJMEDIA already supports
native many audio devices in platforms that PA supports, we no longer actively
maintain PortAudio support.

Follow these guides below to enable PA support in PJMEDIA:

#. Download and build PortAudio for your platform
#. For Mac OS/Linux/Unix, run ``configure`` with ``--with-external-pa`` option. This should
   pick up PortAudio headers and libs in standard locations. If PA is not in
   standard locations, you need to set ``CFLAGS`` and ``LDFLAGS`` accordingly:

   .. code-block:: shell

     $ ./configure --with-external-pa
     $ make

#. For Windows:

   #. Make sure PA headers and libs are in standard location. If not, modify 
      ``pjmedia-audiodev`` Visual Studio project and set header and library directories
      as appropriate.
   #. Add this to your ``config_site.h``:

      .. code-block:: c

         #define PJMEDIA_AUDIO_DEV_HAS_PORTAUDIO 1


   #. Rebuild the workspace

Blackberry BB10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
See https://trac.pjsip.org/repos/wiki/Getting-Started/BB10


Nokia APS/VAS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
See https://trac.pjsip.org/repos/wiki/APS


Symbian MMF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
See https://trac.pjsip.org/repos/wiki/Getting-Started/Symbian


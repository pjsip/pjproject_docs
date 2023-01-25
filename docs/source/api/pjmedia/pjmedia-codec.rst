PJMEDIA-Codec
---------------------------------------------
.. _pjmedia-codec:

List of audio and video codecs supported by PJMEDIA-Codec.


.. include:: ../../common/common_codecs.rst



Detail information:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _amediacodec:

Android H.264, VP8, VP9 (native)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Android AMediaCodec provides native AMR-NB and AMR-WB audio codecs and AVC (H264), 
VP8, VP9 video codecs for Android.

- See :pr:`2552` for integration instructions

.. _bcg729:

BCG729 (a G.729 compliant codec)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Available on Windows, Posix (Mac OS X, Linux), iOS, Android.
- GPL license
- Build instructions: https://github.com/pjsip/pjproject/issues/2029
- Code documentation: :doc:`BCG729 </api/generated/pjmedia/group/group__PJMED__BCG729>`

.. _ffmpeg:

FFMPEG codecs (H.261, H.263, H.263P (H263-1998), H.264, MJPEG, VP8, VP9)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`guide_ffmpeg`.


See also:

- Code documentation: :doc:`FFMPEG </api/generated/pjmedia/group/group__PJMEDIA__CODEC__VID__FFMPEG>`
- VP8/VP9 support: https://github.com/pjsip/pjproject/pull/2863

.. _g711:

G.711
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ITU G.711 codec is built-in and enabled by default in PJMEDIA (controlled by
  ``PJMEDIA_HAS_G711_CODEC`` macro)
- Fast table vs compute-based implementation are available (controlled by
  ``PJMEDIA_HAS_ALAW_ULAW_TABLE`` macro)
- Code documentation: :doc:`G.711 </api/generated/pjmedia/group/group__PJMED__G711>`

.. _g722:

G.722
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ITU G.722 wideband codec is built-in and enabled by default in PJMEDIA-Codec (controlled
  by ``PJMEDIA_HAS_G722_CODEC`` macro)
- Code documentation: :doc:`G.722 </api/generated/pjmedia/group/group__PJMED__G722>`

.. _g7221:

G.722.1/C
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ITU G.722.1 (a.k.a Siren7/Siren14 codecs) is shipped with PJPROJECT.
- Beware of licensing requirement to use this codec. We have acquired a license from Polycom
  to distribute the codec with PJSIP, however you (the user of PJSIP software) MUST acquire 
  the license from Poly (previously Polycom) yourself to use the codec and/or distribute 
  software linked with the codec. 
- This codec is by default disabled, due to the licensing restriction above.
- To enable it, declare in ``config_site.h``:

  .. code-block:: c

     #define PJMEDIA_HAS_G7221_CODEC  1

- Code documentation: :doc:`G.722.1 </api/generated/pjmedia/group/group__PJMED__G7221__CODEC>`

.. _gsm:

GSM FR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- GSM codec is built-in and enabled by default in PJMEDIA-Codec (controlled
  by ``PJMEDIA_HAS_GSM_CODEC`` macro)
- Code documentation: :doc:`GSM FR </api/generated/pjmedia/group/group__PJMED__GSM>`

.. _ilbc:

ILBC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Software based ILBC codec is built-in and enabled by default in PJMEDIA-Codec 
  (controlled by ``PJMEDIA_HAS_ILBC_CODEC`` macro)
- Optimized implementation is available for Mac OS X and iOS. To enable it, 
  declare this in your ``config_site.h``:

  .. code-block:: c

     #define PJMEDIA_ILBC_CODEC_USE_COREAUDIO 1

- Code documentation: :doc:`ILBC </api/generated/pjmedia/group/group__PJMED__ILBC>`

.. _ipp:

Intel IPP codecs
=========================================

- Installation: :ref:`guide_ipp`
- Code documentation: :doc:`IPP Codecs </api/generated/pjmedia/group/group__PJMED__IPP__CODEC>`

.. _l16:

Linear/PCM 8/16bit mono/stereo
=========================================

- These are family of L8/L16 codecs shipped with PJMEDIA. It supports stereo codec.
- By default they are disabled because we're running out of static RTP payload types.
- To enable it, set the codec(s) you desire to use to 1 in ``config_site.h``:

  .. code-block:: c

     #define PJMEDIA_CODEC_L16_HAS_8KHZ_MONO     1
     #define PJMEDIA_CODEC_L16_HAS_8KHZ_STEREO   1
     #define PJMEDIA_CODEC_L16_HAS_16KHZ_MONO    1
     #define PJMEDIA_CODEC_L16_HAS_16KHZ_STEREO  1
     #define PJMEDIA_CODEC_L16_HAS_48KHZ_MONO    1
     #define PJMEDIA_CODEC_L16_HAS_48KHZ_STEREO  1

- Code documentation: :doc:`PCM/Linear 16bit </api/generated/pjmedia/group/group__PJMED__L16>`

.. _opencore_amr:

OpenCore AMR NB/WB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Installation: :ref:`guide_opencore_amr`
- Code documentation: :doc:`OpenCore AMR NB/WB</api/generated/pjmedia/group/group__PJMED__OC__AMR>`

.. _openh264:

OpenH264
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provides video codec H.264, alternatively you can use ffmpeg (together with 
libx264).

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- OpenH264 may be detected and enabled by the ``configure`` script, either 
  automatically or manually via ``--with-openh264`` option. It may be forcefully 
  disabled by defining ``PJMEDIA_HAS_OPENH264_CODEC`` to 0 in ``config_site.h``
- Detailed instructions: :issue:`1947`
- Code documentation: :doc:`OpenH264 </api/generated/pjmedia/group/group__PJMEDIA__CODEC__OPENH264>`


.. _opus:

Opus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Opus is a totally open, royalty-free, highly versatile audio codec.

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- Build instructions: https://github.com/pjsip/pjproject/issues/1904
- Code documentation: :doc:`OPUS </api/generated/pjmedia/group/group__PJMED__OPUS>`

.. _passthrough:

Passthrough codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passthrough codecs are not actual codecs, rather they just PACK and PARSE encoded audio 
data from/into RTP payload. They are used to accommodate ports that work with encoded audio 
data, e.g: encoded audio files, and sound device with codec support, to let the 
frames pass through PJMEDIA without being encoded and decoded.

- Supports AMR, G.729, ILBC, PCMU, PCMA.
- Code documentation: :doc:`Passthrough </api/generated/pjmedia/group/group__PJMED__PASSTHROUGH__CODEC>`

.. _silk:

SILK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- Build instructions: https://github.com/pjsip/pjproject/issues/1586
- Code documentation: :doc:`SILK </api/generated/pjmedia/group/group__PJMED__SILK>`

.. _speex:

Speex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Speex codecs are shipped and enabled by default in PJMEDIA-Codec (controlled
  by ``PJMEDIA_HAS_SPEEX_CODEC`` macro)
- Supports narrowband, wideband, and ultra-wideband
- Code documentation: :doc:`Speex </api/generated/pjmedia/group/group__PJMED__SPEEX>`


.. _libvpx:

VP8 and VP9 (libvpx)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Build instructions: :issue:`2253`
- Code documentation: :doc:`VP8 and VP9 </api/generated/pjmedia/group/group__PJMEDIA__CODEC__VPX>`


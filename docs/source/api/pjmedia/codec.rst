PJMEDIA-Codec
---------------------------------------------
.. _pjmedia-codec:

List of audio and video codecs supported by PJMEDIA-Codec.


.. include:: ../../common/pjmedia_codec.rst



Detail information:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _amediacodec:

Android AMediaCodec
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Android AMediaCodec provides native AMR-NB and AMR-WB audio codecs and AVC (H264), 
VP8, VP9 video codecs for Android.

- Build instructions: https://github.com/pjsip/pjproject/pull/2552


.. _bcg729:

BCG729 (a G.729 compliant codec)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Available on Windows, Posix (Mac OS X, Linux), iOS, Android.
- GPL license
- Build instructions: https://github.com/pjsip/pjproject/issues/2029
- Code documentation: :doc:`BCG729 </api/generated/pjmedia/group/group__PJMED__BCG729>`


.. _openh264:

OpenH264
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- Build instructions: https://github.com/pjsip/pjproject/issues/1947
- Code documentation: :doc:`OpenH264 </api/generated/pjmedia/group/group__PJMEDIA__CODEC__OPENH264>`

.. _opus:

Opus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Opus is a totally open, royalty-free, highly versatile audio codec.

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- Build instructions: https://github.com/pjsip/pjproject/issues/1904
- Code documentation: :doc:`OPUS </api/generated/pjmedia/group/group__PJMED__OPUS>`


.. _ffmpeg:

FFMPEG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- VP8/VP9 support: https://github.com/pjsip/pjproject/pull/2863
- Code documentation: :doc:`FFMPEG </api/generated/pjmedia/group/group__PJMEDIA__CODEC__VID__FFMPEG>`

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

.. _silk:

SILK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Supports Windows, Posix (Mac OS X, Linux), iOS, Android.
- Build instructions: https://github.com/pjsip/pjproject/issues/1586
- Code documentation: :doc:`SILK </api/generated/pjmedia/group/group__PJMED__SILK>`

.. _libpvx:

VP8 and VP9 (libpvx)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Build instructions: https://github.com/pjsip/pjproject/issues/2253
- Code documentation: :doc:`VP8 and VP9 </api/generated/pjmedia/group/group__PJMEDIA__CODEC__VPX>`



Audio device API
=========================================

See :doc:`PJMEDIA-AudioDev </api/pjmedia/pjmedia-audiodev>` API reference.

Audio device tuning
=========================================

AEC
=========================================
- WebRTC: https://github.com/pjsip/pjproject/pull/2775
- Hardware AEC/VPIO: https://github.com/pjsip/pjproject/issues/1778
- Speex AEC: https://github.com/pjsip/pjproject/issues/589

Audio latency benchmark
=========================================

Audio quality troubleshooting
=========================================

If you experience any problem with the audio quality, you may want to try the steps below:

1. Follow the guide: `Test the sound device using pjsystest`_.
2. Identify the sound problem and troubleshoot it using the steps described in: `Checking for sound problems`_.

.. _`Checking for sound problems`: http://trac.pjsip.org/repos/wiki/sound-problems
.. _`Test the sound device using pjsystest`: http://trac.pjsip.org/repos/wiki/Testing_Audio_Device_with_pjsystest

It is probably easier to do the testing using lower level API such as PJSUA since we already have a built-in pjsua sample app located in pjsip-apps/bin to do the testing. However, you can also do the testing in your application using PJSUA2 API such as local audio loopback, recording to WAV file as explained in the Media chapter previously.


Integrating 3rd party media
=========================================

.. _guide_ipp:

Intel IPP codecs integration
=========================================

- Trac: https://trac.pjsip.org/repos/wiki/Intel_IPP_Codecs


OPUS  codec
=========================================

- Integration instructions: https://github.com/pjsip/pjproject/issues/1904


Tone generator
=========================================

.. _guide_webrtc:

WebRTC integration
================================
See:

- Main webrtc integration: https://github.com/pjsip/pjproject/issues/1888
- WebRTC AEC3: https://github.com/pjsip/pjproject/pull/2722

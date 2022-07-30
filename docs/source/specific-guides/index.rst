Audio
*****************************************

Audio device API
=========================================

Audio device tuning
=========================================

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

Intel IPP codecs
=========================================

OpenCore AMR codecs
=========================================

OPUS  codec
=========================================

Tone generator
=========================================

WebRTC AEC
=========================================


Media
*****************************************

Media flow explained
=========================================

Media transport adapter
=========================================

Media benchmark (MIPS test)
=========================================



Development & Programming
*****************************************

Build and Installation
=========================================

Group lock
=========================================

MSys/Mingw
=========================================


Network & NAT
*****************************************

Blocked/filtered network
=========================================

Please refer to the wiki `Getting Around Blocked or Filtered VoIP Network`_.

.. _`Getting Around Blocked or Filtered VoIP Network`: https://trac.pjsip.org/repos/wiki/get-around-nat-blocked-traffic-filtering


IP address change
=========================================

Please see the wiki `Handling IP Address Change`_. Note that the guide is written using PJSUA API as a reference.

.. _`Handling IP Address Change`: https://trac.pjsip.org/repos/wiki/IPAddressChange


IPv6
=========================================

Need detailed guide.

Relevant links:
* https://trac.pjsip.org/repos/wiki/IPv6
* https://github.com/pjsip/pjproject/issues/422
* https://github.com/pjsip/pjproject/issues/1971
* https://github.com/pjsip/pjproject/issues/2032

QoS
=========================================

Standalone ICE
=========================================

TCP
=========================================

Trickle ICE
=========================================


Performance & Footprint
*****************************************

Performance Optimization
=========================================
A general guide on how to reduce CPU utilization can be found here: `FAQ-CPU utilization`_.

.. _`FAQ-CPU utilization`: http://trac.pjsip.org/repos/wiki/FAQ#cpu



Security
*****************************************

SRTP
=========================================

TLS
=========================================


SIP
*****************************************


Video
*****************************************

Video quality troubleshooting
=========================================
For video quality problems, the steps are as follows:

1. For lack of video, check account's AccountVideoConfig, especially the fields autoShowIncoming and autoTransmitOutgoing. More about the video API is explained in `Video Users Guide`_.
2. Check local video preview using PJSUA API as described in `Video Users Guide-Video Preview API`_.
3. Since video requires a larger bandwidth, we need to check for network impairments as described in `Checking Network Impairments`_. The document is for troubleshooting audio problem but it applies for video as well.
4. Check the CPU utilization. If the CPU utilization is too high, you can try a different (less CPU-intensive) video codec or reduce the resolution/fps. A general guide on how to reduce CPU utilization can be found here: `FAQ-CPU utilization`_.

.. _`Video Users Guide`: http://trac.pjsip.org/repos/wiki/Video_Users_Guide
.. _`Video Users Guide-Video Preview API`: http://trac.pjsip.org/repos/wiki/Video_Users_Guide#VideopreviewAPI
.. _`Checking Network Impairments`: http://trac.pjsip.org/repos/wiki/audio-check-packet-loss
.. _`FAQ-CPU utilization`: http://trac.pjsip.org/repos/wiki/FAQ#cpu


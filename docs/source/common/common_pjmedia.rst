
.. comment: 

   This file is shared by both the Features (Datasheet) page and PJMEDIA API
   reference page.


Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PJMEDIA was designed to be applicable in broad range of systems, from desktop to
mobile, embedded, and maybe even DSP. These are the core considerations for such 
design:

- any clockrates
- N-channels support
- zero thread capable


Audio Features
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some audio processing algorithms implemented in PJMEDIA.

- :doc:`Accoustic Echo Cancellation </specific-guides/audio/aec>` 
- :doc:`Adaptive Delay Buffer </api/generated/pjmedia/group/group__PJMED__DELAYBUF>`
- :doc:`Adaptive Jitter Buffer </api/generated/pjmedia/group/group__PJMED__JBUF>`
- :doc:`Adaptive Silence Detection </api/generated/pjmedia/group/group__PJMEDIA__SILENCEDET>`
- :doc:`Circular Buffer </api/generated/pjmedia/group/group__PJMED__CIRCBUF>`
- :doc:`Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`
- :doc:`Conference Bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`
- :doc:`Format converter </api/generated/pjmedia/group/group__PJMEDIA__CONVERTER>`
- :doc:`Mono/Stereo/Multichannel Converter </api/generated/pjmedia/group/group__PJMEDIA__STEREO>`
- :doc:`Packet Lost Concealment (PLC) </api/generated/pjmedia/group/group__PJMED__PLC>`
- :doc:`Resampling Algorithm </api/generated/pjmedia/group/group__PJMEDIA__RESAMPLE>`
- :doc:`Tone/DTMF Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`
- :doc:`WAV file playback </api/generated/pjmedia/group/group__PJMEDIA__FILE__PLAY>`,
  :doc:`playlist </api/generated/pjmedia/group/group__PJMEDIA__WAV__PLAYLIST>`, and
  :doc:`recorder </api/generated/pjmedia/group/group__PJMEDIA__FILE__REC>`
- :doc:`Waveform Similarity Based Overlap-Add (WSOLA) </api/generated/pjmedia/group/group__PJMED__WSOLA>`
- `WebRTC AEC3 support <https://github.com/pjsip/pjproject/pull/2722>`_


Video Features
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: /common/common_video_features.rst


Transports
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Media transport is responsible for packing/unpacking media frames to/from the network,
as well as getting involved in negotiation of suitable transport in SDP. Media transports
can also be chained in a pipeline (for example, SRTP+ICE).

- :doc:`Media Transport API </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
- :any:`SRTP - Secure RTP (SDES and DTLS) </specific-guides/security/srtp>`
- :doc:`ICE - Interactive Connectivity Establishment </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ICE>`
- :doc:`UDP </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__UDP>`
- :doc:`Loopback </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__LOOP>`
- :doc:`Sample Transport Adapter </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ADAPTER__SAMPLE>`

Media transports implemented by community:

- ZRTP: https://github.com/wernerd/ZRTP4PJ


Media components (Ports)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
:doc:`Port </api/generated/pjmedia/group/group__PJMEDIA__PORT>` is PJMEDIA component 
for processing media frames. Media ports can be linked in a pipeline to process 
audio/video frames end-to-end from audio device to the network/transport.

- :doc:`Conference Bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`
- :doc:`Bidirectional Port </api/generated/pjmedia/group/group__PJMEDIA__BIDIRECTIONAL__PORT>`
- :doc:`Echo Cancellation Port </api/generated/pjmedia/group/group__PJMEDIA__ECHO__PORT>`
- :doc:`Buffer Playback </api/generated/pjmedia/group/group__PJMEDIA__MEM__PLAYER>`
- :doc:`Capture to Buffer </api/generated/pjmedia/group/group__PJMEDIA__MEM__CAPTURE>`
- :doc:`Null Port </api/generated/pjmedia/group/group__PJMEDIA__NULL__PORT>`
- :doc:`Resampling Port </api/generated/pjmedia/group/group__PJMEDIA__RESAMPLE__PORT>`
- :doc:`Multi-frequency/DTMF Tone Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`
- :doc:`Audio Stream </api/generated/pjmedia/group/group__PJMED__STRM>`
- :doc:`Video Stream </api/generated/pjmedia/group/group__PJMED__VID__STRM>`
- :doc:`WAV File Playback </api/generated/pjmedia/group/group__PJMEDIA__FILE__PLAY>`
- :doc:`WAV Playlist </api/generated/pjmedia/group/group__PJMEDIA__WAV__PLAYLIST>`
- :doc:`WAV File Recorder </api/generated/pjmedia/group/group__PJMEDIA__FILE__REC>`
- :doc:`Media channel splitter/combiner </api/generated/pjmedia/group/group__PJMEDIA__SPLITCOMB>`
  
  
Clock provider
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Because PJMEDIA has no thread, a "clock" must be provided to make the media frames flow
inside the media pipeline in a timely manner.

- :doc:`Introduction to clock concept </api/generated/pjmedia/group/group__PJMEDIA__PORT__CLOCK>`
- :doc:`Master Port </api/generated/pjmedia/group/group__PJMEDIA__MASTER__PORT>`
- :doc:`Sound Device Port </api/generated/pjmedia/group/group__PJMED__SND__PORT>`
- :doc:`Sound Device (Deprecated) </api/generated/pjmedia/group/group__PJMED__SND>`
- :doc:`Video media port </api/generated/pjmedia/group/group__PJMEDIA__VIDEO__PORT>`
- :doc:`Clock Generator </api/generated/pjmedia/group/group__PJMEDIA__CLOCK>`


Codec Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`Codec Registration </api/generated/pjmedia/group/group__PJMEDIA__CODEC__REGISTER__ALL>`
- :doc:`Codec constants </api/generated/pjmedia/group/group__pjmedia__codec__types>`
- :doc:`Audio Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`
- :doc:`Video Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__VID__CODEC>`

  .. note::

     For list of supported codecs, see :doc:`Supported codecs </overview/features_codec>`.

SDP
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SDP Parsing and Data Structure </api/generated/pjmedia/group/group__PJMEDIA__SDP>`
- :doc:`SDP Negotiation State Machine (Offer/Answer Model) </api/generated/pjmedia/group/group__PJMEDIA__SDP__NEG>`
  (:rfc:`3264`)
- `SDP SSRC attribute <https://github.com/pjsip/pjproject/issues/2098>`__ 
  (:rfc:`5576`)
- `RTP and RTCP multiplexing <https://github.com/pjsip/pjproject/issues/2087>`_
  (:rfc:`5761`)

RTP and RTCP
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`RTP Session and Encapsulation </api/generated/pjmedia/group/group__PJMED__RTP>`
  (:rfc:`3350`)
- :doc:`RTCP Session and Encapsulation </api/generated/pjmedia/group/group__PJMED__RTCP>`
  (:rfc:`3350`)
- `RTP and RTCP multiplexing <https://github.com/pjsip/pjproject/issues/2087>`_
  (:rfc:`5761`)
- :doc:`RTCP Feedback mechanism </specific-guides/media/rtcp_fb>`
- :doc:`RTCP XR </api/generated/pjmedia/group/group__PJMED__RTCP__XR>`
  (:rfc:`3611`)
- `SSRC synchronization via SDP <https://github.com/pjsip/pjproject/issues/2098>`__ 
  (:rfc:`5576`)
- `RTCP CNAME guideline <https://github.com/pjsip/pjproject/issues/2098>`__ 
  (:rfc:`7022`)
  

Compile Time Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`PJMEDIA </api/generated/pjmedia/group/group__PJMEDIA__CONFIG>`
- :doc:`Audio device </api/generated/pjmedia/group/group__s1__audio__device__config>`
- :doc:`Video Device </api/generated/pjmedia/group/group__s1__video__device__config>`


Basic Types and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Basic Types </api/generated/pjmedia/group/group__PJMEDIA__TYPES>`
- :doc:`Error Codes </api/generated/pjmedia/group/group__PJMEDIA__ERRNO>`
- :doc:`Object Signatures </api/generated/pjmedia/group/group__PJMEDIA__SIG>`


Endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The endpoint is a singleton runtime "manager" for PJMEDIA framework.

- :doc:`Media Endpoint </api/generated/pjmedia/group/group__PJMED__ENDPT>`


Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`RIFF/WAVE </api/generated/pjmedia/group/group__PJMEDIA__WAVE>`
- :doc:`AVI </api/generated/pjmedia/group/group__PJMEDIA__AVI>`
- :doc:`Media format framework </api/generated/pjmedia/group/group__PJMEDIA__FORMAT>`
- :doc:`Format Converter </api/generated/pjmedia/group/group__PJMEDIA__CONVERTER>`

Media Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Frame </api/generated/pjmedia/group/group__PJMEDIA__FRAME>`
- :doc:`Media Session </api/generated/pjmedia/group/group__PJMEDIA__SESSION>`
- :doc:`Media Port Framework </api/generated/pjmedia/group/group__PJMEDIA__PORT>`


Events
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Event Framework </api/generated/pjmedia/group/group__PJMEDIA__EVENT>`



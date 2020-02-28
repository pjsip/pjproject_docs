PJMEDIA - Media Stack
============================================

PJMEDIA is a fully featured open source media stack, featuring small footprint and 
good extensibility and excellent portability.


API Reference
---------------

Compile Time Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`PJMEDIA <generated/pjmedia/group/group__PJMEDIA__CONFIG>`
- :doc:`Codecs <generated/pjmedia/group/>`
- :doc:`Audio device <generated/pjmedia/group/group__s1__audio__device__config>`
- :doc:`Video Device <generated/pjmedia/group/group__s1__video__device__config>`


Basic Types and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Basic Types <generated/pjmedia/group/group__PJMEDIA__TYPES>`
- :doc:`Error Codes <generated/pjmedia/group/group__PJMEDIA__ERRNO>`
- :doc:`Object Signatures <generated/pjmedia/group/group__PJMEDIA__SIG>`


Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Endpoint <generated/pjmedia/group/group__PJMED__ENDPT>`


Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Format <generated/pjmedia/group/group__PJMEDIA__FORMAT>`
- File formats:

  - :doc:`RIFF/WAVE <generated/pjmedia/group/group__PJMEDIA__WAVE>`
  - :doc:`AVI <generated/pjmedia/group/group__PJMEDIA__AVI>`


Codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Codec Registration <generated/pjmedia/group/group__PJMEDIA__CODEC__REGISTER__ALL>`
- :doc:`Codec constants <generated/pjmedia/group/group__pjmedia__codec__types>`

Audio Codecs
^^^^^^^^^^^^^
- :doc:`Audio Codec Framework <generated/pjmedia/group/group__PJMEDIA__CODEC>`
- :doc:`G.711 <generated/pjmedia/group/group__PJMED__G711>`
- :doc:`AMR NB/WB <generated/pjmedia/group/group__PJMED__AMR__CODEC__HELPER>`
- :doc:`BCG729 (a G.729 compliant codec) <generated/pjmedia/group/group__PJMED__BCG729>`
- :doc:`G.722 <generated/pjmedia/group/group__PJMED__G722>`
- :doc:`G.722.1 <generated/pjmedia/group/group__PJMED__G7221__CODEC>`
- :doc:`GSM FR <generated/pjmedia/group/group__PJMED__GSM>`
- :doc:`ILBC <generated/pjmedia/group/group__PJMED__ILBC>`
- :doc:`IPP Codecs Library <generated/pjmedia/group/group__PJMED__IPP__CODEC>`
- :doc:`OpenCore AMR <generated/pjmedia/group/group__PJMED__OC__AMR>`
- :doc:`OPUS <generated/pjmedia/group/group__PJMED__OPUS>`
- :doc:`PCM/Linear 16bit <generated/pjmedia/group/group__PJMED__L16>`
- :doc:`Passthrough <generated/pjmedia/group/group__PJMED__PASSTHROUGH__CODEC>`
- :doc:`SILK <generated/pjmedia/group/group__PJMED__SILK>`
- :doc:`Speex <generated/pjmedia/group/group__PJMED__SPEEX>`


Video Codecs
^^^^^^^^^^^^^
- :doc:`Video Codec Framework <generated/pjmedia/group/group__PJMEDIA__VID__CODEC>`
- :doc:`FFMPEG Codecs <generated/pjmedia/group/group__PJMEDIA__CODEC__VID__FFMPEG>`
- :doc:`OpenH264 <generated/pjmedia/group/group__PJMEDIA__CODEC__OPENH264>`
- :doc:`Video Toolbox Codec for iOS and Mac <generated/pjmedia/group/group__PJMEDIA__CODEC__VID__TOOLBOX>`
- :doc:`VPX Codec for iOS and Mac <generated/pjmedia/group/group__PJMEDIA__CODEC__VPX>`



Media Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Frame <generated/pjmedia/group/group__PJMEDIA__FRAME>`
- :doc:`Media Session <generated/pjmedia/group/group__PJMEDIA__SESSION>`
- :doc:`Media Port Framework <generated/pjmedia/group/group__PJMEDIA__PORT>`

Events
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Event Framework <generated/pjmedia/group/group__PJMEDIA__EVENT>`


Ports
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`File Playback <generated/pjmedia/group/group__PJMEDIA__FILE__PLAY>`
- :doc:`File Recorder <generated/pjmedia/group/group__PJMEDIA__FILE__REC>`
- :doc:`Bidirectional Port <generated/pjmedia/group/group__PJMEDIA__BIDIRECTIONAL__PORT>`
- :doc:`Conference Bridge <generated/pjmedia/group/group__PJMEDIA__CONF>`
- :doc:`Echo Cancellation Port <generated/pjmedia/group/group__PJMEDIA__ECHO__PORT>`
- :doc:`Buffer Playback <generated/pjmedia/group/group__PJMEDIA__MEM__PLAYER>`
- :doc:`Capture to Buffer <generated/pjmedia/group/group__PJMEDIA__MEM__CAPTURE>`
- :doc:`Null Port <generated/pjmedia/group/group__PJMEDIA__NULL__PORT>`
- :doc:`Resampling Port <generated/pjmedia/group/group__PJMEDIA__RESAMPLE__PORT>`
- :doc:`Multi-frequency/DTMF Tone Generator <generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`
- :doc:`Audio Stream <generated/pjmedia/group/group__PJMED__STRM>`
- :doc:`Video Stream <generated/pjmedia/group/group__PJMED__VID__STRM>`
- :doc:`WAV Playlist <generated/pjmedia/group/group__PJMEDIA__WAV__PLAYLIST>`
- :doc:`Media channel splitter/combiner <generated/pjmedia/group/group__PJMEDIA__SPLITCOMB>`
- :doc:`Video conference bridge <generated/pjmedia/group/group__PJMEDIA__VID__CONF>`
- :doc:`Video source duplicator <generated/pjmedia/group/group__PJMEDIA__VID__TEE>`
  
  
- Clock provider ports:

  - :doc:`Introduction <generated/pjmedia/group/group__PJMEDIA__PORT__CLOCK>`
  - :doc:`Master Port <generated/pjmedia/group/group__PJMEDIA__MASTER__PORT>`
  - :doc:`Sound Device Port <generated/pjmedia/group/group__PJMED__SND__PORT>`
  - :doc:`Sound Device (Deprecated) <generated/pjmedia/group/group__PJMED__SND>`
  - :doc:`Video media port <generated/pjmedia/group/group__PJMEDIA__VIDEO__PORT>`
  - :doc:`Clock Generator <generated/pjmedia/group/group__PJMEDIA__CLOCK>`


Other Audio Features
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Accoustic Echo Cancellation API <generated/pjmedia/group/group__PJMEDIA__Echo__Cancel>`
- :doc:`Adaptive Delay Buffer <generated/pjmedia/group/group__PJMED__DELAYBUF>`
- :doc:`Adaptive Jitter Buffer <generated/pjmedia/group/group__PJMED__JBUF>`
- :doc:`Adaptive Silence Detection <generated/pjmedia/group/group__PJMEDIA__SILENCEDET>`
- :doc:`Circular Buffer <generated/pjmedia/group/group__PJMED__CIRCBUF>`
- :doc:`Format converter <generated/pjmedia/group/group__PJMEDIA__CONVERTER>`
- :doc:`Mono/Stereo/Multichannel Converter <generated/pjmedia/group/group__PJMEDIA__STEREO>`
- :doc:`Packet Lost Concealment (PLC) <generated/pjmedia/group/group__PJMED__PLC>`
- :doc:`Resampling Algorithm <generated/pjmedia/group/group__PJMEDIA__RESAMPLE>`
- :doc:`Waveform Similarity Based Overlap-Add (WSOLA) <generated/pjmedia/group/group__PJMED__WSOLA>`


Transports
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Transport API <generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
- :doc:`UDP <generated/pjmedia/group/group__PJMEDIA__TRANSPORT__UDP>`
- :doc:`ICE - Interactive Connectivity Establishment <generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ICE>`
- :doc:`SRTP - Secure RTP (SDES and DTLS) <generated/pjmedia/group/group__PJMEDIA__TRANSPORT__SRTP>`
- :doc:`Loopback <generated/pjmedia/group/group__PJMEDIA__TRANSPORT__LOOP>`
- :doc:`Sample Transport Adapter <generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ADAPTER__SAMPLE>`

SDP
-------------
- :doc:`SDP Parsing and Data Structure <generated/pjmedia/group/group__PJMEDIA__SDP>`
- :doc:`SDP Negotiation State Machine (Offer/Answer Model, RFC 3264) <generated/pjmedia/group/group__PJMEDIA__SDP__NEG>`


RTP and RTCP
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`RTP Session and Encapsulation (RFC 3350) <generated/pjmedia/group/group__PJMED__RTP>`
- :doc:`RTCP Session and Encapsulation (RFC 3350) <generated/pjmedia/group/group__PJMED__RTCP>`
- :doc:`RTCP Feedback (RFC 4585) <generated/pjmedia/group/group__PJMED__RTCP__FB>`
- :doc:`RTCP XR (RFC 3611) <generated/pjmedia/group/group__PJMED__RTCP__XR>`


Portable Audio Device Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Portable Audio Device API <generated/pjmedia/group/group__s2__audio__device__reference>`
- :doc:`Implementor's API <generated/pjmedia/group/group__s8__audio__device__implementors__api>`
- :doc:`Audio Test/Benchmark Utility <generated/pjmedia/group/group__s30__audio__test__utility>`
- :doc:`Error Codes <generated/pjmedia/group/group__error__codes>`


Portable Video Device Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Portable Video Device API <generated/pjmedia/group/group__video__device__reference>`
- :doc:`Implementor's API <generated/pjmedia/group/group__s8__video__device__implementors__api>`
- :doc:`AVI Player Virtual Device <generated/pjmedia/group/group__avi__dev>`
- :doc:`Error Codes <generated/pjmedia/group/group__error__codes>`

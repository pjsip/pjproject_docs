
.. comment: 

   This file is shared by both the Features (Datasheet) page and PJMEDIA API
   reference page.


Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PJMEDIA was designed to be applicable in broad range of systems, including DSPs.
These are the core considerations for such design:

- any clockrates
- N-channels support
- zero thread capable


Media components (Ports)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
:doc:`Port </api/generated/pjmedia/group/group__PJMEDIA__PORT>` is PJMEDIA component 
for processing media frames. Media ports can be linked in a pipeline to process 
audio/video frames end-to-end from audio device to the network/transport.

- :doc:`File Playback </api/generated/pjmedia/group/group__PJMEDIA__FILE__PLAY>`
- :doc:`File Recorder </api/generated/pjmedia/group/group__PJMEDIA__FILE__REC>`
- :doc:`Bidirectional Port </api/generated/pjmedia/group/group__PJMEDIA__BIDIRECTIONAL__PORT>`
- :doc:`Conference Bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`
- :doc:`Echo Cancellation Port </api/generated/pjmedia/group/group__PJMEDIA__ECHO__PORT>`
- :doc:`Buffer Playback </api/generated/pjmedia/group/group__PJMEDIA__MEM__PLAYER>`
- :doc:`Capture to Buffer </api/generated/pjmedia/group/group__PJMEDIA__MEM__CAPTURE>`
- :doc:`Null Port </api/generated/pjmedia/group/group__PJMEDIA__NULL__PORT>`
- :doc:`Resampling Port </api/generated/pjmedia/group/group__PJMEDIA__RESAMPLE__PORT>`
- :doc:`Multi-frequency/DTMF Tone Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`
- :doc:`Audio Stream </api/generated/pjmedia/group/group__PJMED__STRM>`
- :doc:`Video Stream </api/generated/pjmedia/group/group__PJMED__VID__STRM>`
- :doc:`WAV Playlist </api/generated/pjmedia/group/group__PJMEDIA__WAV__PLAYLIST>`
- :doc:`Media channel splitter/combiner </api/generated/pjmedia/group/group__PJMEDIA__SPLITCOMB>`
- :doc:`Video conference bridge </api/generated/pjmedia/group/group__PJMEDIA__VID__CONF>`
- :doc:`Video source duplicator </api/generated/pjmedia/group/group__PJMEDIA__VID__TEE>`
  
  
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


Audio Features
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Base audio processing algorithms implemented in PJMEDIA.

- :doc:`Accoustic Echo Cancellation API </api/generated/pjmedia/group/group__PJMEDIA__Echo__Cancel>`
- :doc:`Adaptive Delay Buffer </api/generated/pjmedia/group/group__PJMED__DELAYBUF>`
- :doc:`Adaptive Jitter Buffer </api/generated/pjmedia/group/group__PJMED__JBUF>`
- :doc:`Adaptive Silence Detection </api/generated/pjmedia/group/group__PJMEDIA__SILENCEDET>`
- :doc:`Circular Buffer </api/generated/pjmedia/group/group__PJMED__CIRCBUF>`
- :doc:`Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`
- :doc:`Format converter </api/generated/pjmedia/group/group__PJMEDIA__CONVERTER>`
- :doc:`Mono/Stereo/Multichannel Converter </api/generated/pjmedia/group/group__PJMEDIA__STEREO>`
- :doc:`Packet Lost Concealment (PLC) </api/generated/pjmedia/group/group__PJMED__PLC>`
- :doc:`Resampling Algorithm </api/generated/pjmedia/group/group__PJMEDIA__RESAMPLE>`
- :doc:`Tone/DTMF Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`
- :doc:`Waveform Similarity Based Overlap-Add (WSOLA) </api/generated/pjmedia/group/group__PJMED__WSOLA>`


Transports
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Media transport is responsible for packing/unpacking media frames to/from the network,
as well as getting involved in negotiation of suitable transport in SDP. Media transports
can also be chained in a pipeline (for example, SRTP+ICE).

- :doc:`Media Transport API </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
- :doc:`SRTP - Secure RTP (SDES and DTLS) </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__SRTP>`
- :doc:`ICE - Interactive Connectivity Establishment </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ICE>`
- :doc:`UDP </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__UDP>`
- :doc:`Loopback </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__LOOP>`
- :doc:`Sample Transport Adapter </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__ADAPTER__SAMPLE>`

SDP
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`SDP Parsing and Data Structure </api/generated/pjmedia/group/group__PJMEDIA__SDP>`
- :doc:`SDP Negotiation State Machine (Offer/Answer Model, RFC 3264) </api/generated/pjmedia/group/group__PJMEDIA__SDP__NEG>`


RTP and RTCP
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`RTP Session and Encapsulation (RFC 3350) </api/generated/pjmedia/group/group__PJMED__RTP>`
- :doc:`RTCP Session and Encapsulation (RFC 3350) </api/generated/pjmedia/group/group__PJMED__RTCP>`
- :doc:`RTCP Feedback (RFC 4585) </api/generated/pjmedia/group/group__PJMED__RTCP__FB>`
- :doc:`RTCP XR (RFC 3611) </api/generated/pjmedia/group/group__PJMED__RTCP__XR>`

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


Codecs
^^^^^^^^^^^^^^^^^^^^^^^^^^^
PJMEDIA implements the codec framework and G.711 codec for reference. Other codecs
are implemented in :ref:`PJMEDIA-Codec <pjmedia-codec>` library. Please see 
the complete list of :ref:`supported_codecs`.

- :doc:`Codec Registration </api/generated/pjmedia/group/group__PJMEDIA__CODEC__REGISTER__ALL>`
- :doc:`Codec constants </api/generated/pjmedia/group/group__pjmedia__codec__types>`
- :doc:`Audio Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`
- :doc:`G.711 </api/generated/pjmedia/group/group__PJMED__G711>`
- :doc:`Video Codec Framework </api/generated/pjmedia/group/group__PJMEDIA__VID__CODEC>`


Media Flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Media Frame </api/generated/pjmedia/group/group__PJMEDIA__FRAME>`
- :doc:`Media Session </api/generated/pjmedia/group/group__PJMEDIA__SESSION>`
- :doc:`Media Port Framework </api/generated/pjmedia/group/group__PJMEDIA__PORT>`


Events
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Event Framework </api/generated/pjmedia/group/group__PJMEDIA__EVENT>`



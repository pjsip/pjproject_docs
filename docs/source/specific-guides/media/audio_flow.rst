Understanding Audio Media Flow
==============================

.. contents:: Table of Contents
   :depth: 3


Introduction
---------------------

During a call, media components are managed by :any:`PJSUA-LIB </api/pjsua-lib/index>`, when PJSUA-LIB
or :any:`PJSUA2 </api/pjsua2/index>` is used, or by the application if the application uses
low level PJSIP or PJMEDIA API directly. Typically the media components for a (PJSUA-LIB) call
are interconnected as follows:

.. figure:: audio-media-flow.jpg
   :alt: audio-media-flow.jpg


The main building blocks for above diagram are the following components:

- :any:`audio device stream </api/pjmedia/pjmedia-audiodev>` (:cpp:any:`pjmedia_aud_stream`),
  which represents a sound device,
- a :any:`Sound Device Port </api/generated/pjmedia/group/group__PJMED__SND__PORT>`
  (:cpp:any:`pjmedia_snd_port`),
  to translate sound device callbacks into calls to downstream media port's
  :cpp:any:`pjmedia_port_put_frame()`/:cpp:any:`pjmedia_port_get_frame()`.
- a :any:`Conference Bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`
  (:cpp:any:`pjmedia_conf`),
- a :any:`Media Stream </api/generated/pjmedia/group/group__PJMED__STRM>`
  (:cpp:any:`pjmedia_stream`) to convert between PCM audio to encoded
  RTP/RTCP packets,
- a :any:`Media Transport </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
  (:cpp:any:`pjmedia_transport`) to transmit and receive RTP/RTCP packets to/from network.


The media interconnection above would be set up as follows:

- PJSUA-LIB (or application) creates a :any:`conference bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`
  (:cpp:any:`pjmedia_conf`)
  during initialization, and normally would retain this throughout the life time of the
  application.
- when making outgoing call or receiving incoming call, PJSUA-LIB
  opens a :any:`audio device stream </api/pjmedia/pjmedia-audiodev>` (:cpp:any:`pjmedia_aud_stream`)
  and creates a :any:`sound device port </api/generated/pjmedia/group/group__PJMED__SND__PORT>`
  (:cpp:any:`pjmedia_snd_port`) and 
  a media transport instance
  such as :any:`UDP media transport </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__UDP>`.
  The listening address and port number of the transport are put in the local SDP 
  to be given to the INVITE session.
- once the offer/answer session in the call is established, 
  :cpp:any:`pjsip_inv_callback::on_media_update` callback is called and
  PJSUA-LIB creates a :cpp:any:`pjmedia_stream_info` from both local and remote SDP
  by using :cpp:any:`pjmedia_stream_info_from_sdp()`.
- PJSUA-LIB creates a :any:`media stream </api/generated/pjmedia/group/group__PJMED__STRM>`
  (:cpp:any:`pjmedia_stream`) with :cpp:any:`pjmedia_stream_create()`,
  specifying the :cpp:any:`pjmedia_stream_info` and the media transport created earlier. 
  This creates media stream according to the codec settings and other
  parameters in the media stream info, and also establish *connection*
  between the media stream and the media transport.
- application registers this media stream to the conference bridge with
  :cpp:any:`pjmedia_conf_add_port()`
- application connects the media stream slot in the bridge to other
  slots such as slot zero which normally is connected to the sound
  device, with :cpp:any:`pjmedia_conf_connect_port()`.



The whole media flow is driven by timing of the sound device, especially
the playback callback.

Audio playback flow (the main flow)
-------------------------------------------

#. when :cpp:any:`pjmedia_aud_stream` needs another frame to be played to the
   speaker, it calls :cpp:any:`play_cb <pjmedia_aud_play_cb>` callback that was
   specified in :cpp:any:`pjmedia_aud_stream_create()`
#. This callback belongs to :cpp:any:`pjmedia_snd_port`. In this callback,
   :cpp:any:`pjmedia_snd_port` calls :cpp:any:`pjmedia_port_get_frame()` of
   its downstream port, which in  this case is the conference bridge 
   (:cpp:any:`pjmedia_conf`).
#. The conference bridge calls :cpp:any:`pjmedia_port_get_frame()` for all ports
   in the conference bridge,
      
      a. then it mixes the signal together according to ports connection in the bridge,  and deliver the mixed 
         signal by calling :cpp:any:`pjmedia_port_put_frame()` for all ports in 
         the bridge according to their connection.
      b. A :cpp:any:`pjmedia_port_get_frame()` call by conference bridge to 
         :any:`media stream </api/generated/pjmedia/group/group__PJMED__STRM>`
         (:cpp:any:`pjmedia_stream`)
         will cause it to pick one frame from the 
         :any:`jitter buffer </api/generated/pjmedia/group/group__PJMED__JBUF>`,
         decode the frame using the configured
         :any:`codec </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`
         (or apply Packet Lost Concealment/PLC if frame is lost), and return
         the PCM frame to the caller. Note that the jitter buffer is filled-in
         by other flow (the flow that polls the network sockets), and will be
         described in later section below.
      c. A :cpp:any:`pjmedia_port_put_frame()` call by conference bridge to media
         stream will cause the media stream to encode the PCM frame with the
         chosen codec, pack it into RTP packet with its
         RTP session, update RTCP session, schedule RTCP transmission, and
         deliver the RTP/RTCP packets to the underlying media transport
         that was previously attached to the stream. The media transport then
         sends the RTP/RTCP packet to the network.
      d. Once these processes finishes, the conference bridge returns the mixed signal
         for slot zero back to  the original :cpp:any:`pjmedia_port_get_frame()` call.
#. The :cpp:any:`pjmedia_snd_port` got the audio frame and returned it back
   to the audio device stream to finish the :cpp:any:`play_cb <pjmedia_aud_play_cb>` callback.


Audio recording flow
-------------------------------------------

The above flow only describes the flow in one direction, i.e. to the
speaker device. But what about the audio flow coming from the
microphone?

#. When the input sound (microphone) device has finished capturing *one*
   audio frame, it will report this event by calling 
   :cpp:any:`rec_cb <pjmedia_aud_rec_cb>` callback that was
   specified in :cpp:any:`pjmedia_aud_stream_create()`.
#. This callback belongs to :cpp:any:`pjmedia_snd_port`. In this callback,
   :cpp:any:`pjmedia_snd_port` calls :cpp:any:`pjmedia_port_put_frame()` of
   its downstream port, which in  this case is the conference bridge 
   (:cpp:any:`pjmedia_conf`).   
#. When :cpp:any:`pjmedia_port_put_frame()` function is called to the
   conference bridge, the bridge will just store the PCM frame to an
   internal buffer, to be picked up by the main flow (the 
   :cpp:any:`pjmedia_port_get_frame()` call to
   the bridge above) when the bridge collects frames from all ports and
   mix the signal.

.. _snd_dev_burst:

Sound device timing problem
-------------------------------------------
Ideally, :cpp:any:`rec_cb <pjmedia_aud_rec_cb>` and :cpp:any:`play_cb <pjmedia_aud_play_cb>` should be
called one after another, in turn and consecutively, by the sound device. But
unfortunately this is not always the case; in many low-end sound cards,
it is quite common to have several consecutive/burst of :cpp:any:`rec_cb <pjmedia_aud_rec_cb>` callbacks
and then followed by burst of :cpp:any:`play_cb <pjmedia_aud_play_cb>` calls. 

The internal sound device queue buffer in the 
conference bridge is large enough to store about 150 ms worth of audio,
and this is controlled by :c:macro:`PJMEDIA_SOUND_BUFFER_COUNT` macro 
(see :source:`pjmedia/src/pjmedia/conference.c`).

It is possible that a very very bad sound device may overrun this buffer, which in this case it
would be necessary to enlarge the :c:macro:`PJMEDIA_SOUND_BUFFER_COUNT` number
in your :any:`config_site.h`.


Incoming RTP/RTCP Packets
-------------------------------------------
Incoming RTP/RTCP packets is not driven by any of the flow above, but
by different flow ("thread"), that is the flow/thread that polls
the socket descriptors (of the media transport).

The standard implementation of :any:`UDP media transport </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT__UDP>`
in PJMEDIA will register the RTP and RTCP sockets to an
:cpp:any:`pj_ioqueue_t` (see :any:`IOQUEUE documentation </api/generated/pjlib/group/group__PJ__IOQUEUE>`).
Application can choose different strategy with regard to placing the
ioqueue instance:

-  Application can instruct :any:`the Media Endpoint </api/generated/pjmedia/group/group__PJMED__ENDPT>`
   to instantiate an internal IOQueue and start one or more worker
   threads to poll this ioqueue. This probably is the recommended
   strategy so that polling to media sockets is done by separate thread
   (and this is the default settings in :any:`PJSUA-LIB </api/pjsua-lib/index>`).
-  Alternatively, application can use a single ioqueue for both SIP and
   media sockets, and *poll* the whole thing from a single thread,
   possibly the main thread. To use this, application will specify the
   ioqueue instance to be used when creating the media endpoint and
   disable worker thread. This strategy is probably preferable on a
   small-footprint devices to reduce (or eliminate) threads in the system.

The flow of incoming RTP packets are as follows:

#. an internal worker thread in :any:`the Media Endpoint </api/generated/pjmedia/group/group__PJMED__ENDPT>`
   polls the ioqueue.
#. an incoming packet will cause the ioqueue to call
   ``on_rx_rtp()`` callback of the UDP media transport.
   This callback was previously registered by the UDP media transport to
   the ioqueue.
#. the ``on_rx_rtp()`` callback reports the incoming RTP packet to the
   :any:`media stream </api/generated/pjmedia/group/group__PJMED__STRM>`.
   The media stream was *attached* to the UDP media transport with
   :cpp:any:`pjmedia_transport_attach()`.
#. the media stream unpacks the RTP packet using its internal RTP
   session, update RX statistics, de-frame the payload according to the
   codec being used (there can be multiple audio frames in a single RTP
   packet), and put the frames in the jitter buffer.
#. the processing of incoming packets stops here, as the frames in the
   jitter buffer will be picked up by the main flow (a call to
   :cpp:any:`pjmedia_port_get_frame()` to the media stream) above.

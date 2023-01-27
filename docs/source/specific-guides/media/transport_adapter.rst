Transport Adapter
=======================

.. contents:: Table of Contents
   :depth: 3



Introduction to media transport
----------------------------------
Media transport (:cpp:any:`pjmedia_transport`) is PJMEDIA object that connects :cpp:any:`pjmedia_stream` to the
network. The main tasks of the media transport are to
send and receive RTP and RTCP packets. But media transports can do more
than that.The ICE media transport, for example, also takes care of NAT
traversal, while the SRTP transport secures your media communication.
The media transport also has access to SDP during SDP negotiation; it
has access to both local and remote offer and answer, and may add or
modify local SDP offer or answer (but note that this feature is only
available if PJSUA-LIB is used). The media
transport API in PJMEDIA provides framework to
integrate transport feature into the rest of the media framework.

The diagram below depicts the interconnection between :cpp:any:`pjmedia_stream`
and :cpp:any:`pjmedia_transport`.

.. figure:: media-transport.png
   :alt: media-transport.png

See :any:`Media Transport reference </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
for more info.

Media transport adapter
-----------------------------------
Media transport adapter is a variant of media transport, where
instead of interfacing directly to the network, it uses another media
transport to do that. The adapter sits between the media stream
object and another transport, and have full access to RTP/RTCP packets
that are exchanged between them. The adapter may inject it's own packets
to either direction if it wants to, or even drop some of them. The main
use of the adapter is to add processing to the media packets while
reusing existing transport features (such as ICE).

One main example of transport adapter is the SRTP transport. It provides
encryption and decryption of RTP and RTCP packets, and it also fully
interacts with the SDP negotiation, using the media transport
framework.

From the media transport diagram above, here is the transport diagram
when SRTP is used:

.. figure:: media-srtp-transport.png
   :alt: media-srtp-transport.png

To stream, the SRTP transport behaves as if it is a media transport
(because it **is** a media transport), and to the media transport it
behaves as if it is a stream. The SRTP object forwards RTP/RTCP packets
back and forth between stream and the actual transport,
encrypting/decrypting the RTP/RTCP packets as necessary.


For more info about SRTP feature please see :any:`/specific-guides/security/srtp`.



Implementing a custom transport adapter
-------------------------------------------

The following steps provide rough guidance to implement transport adapter: 

- Refer to :any:`Media Transport reference </api/generated/pjmedia/group/group__PJMEDIA__TRANSPORT>`
  to see how the media transport operates.
- start with :source:`pjmedia/src/pjmedia/transport_adapter_sample.c`. Copy this to your application directory (you don't
  need to add the transport to pjmedia directory). 
- implement the media transport methods (i.e., :cpp:any:`pjmedia_transport_op`)
  as necessary. At the very minimum, you'd need to implement:

    - :cpp:any:`pjmedia_transport_op::get_info`
    - :cpp:any:`pjmedia_transport_op::attach`, 
    - :cpp:any:`pjmedia_transport_op::detach`,
    - :cpp:any:`pjmedia_transport_op::send_rtp`, 
    - :cpp:any:`pjmedia_transport_op::send_rtcp2`, and
    - :cpp:any:`pjmedia_transport_op::destroy`. 
    
  You'll need to implement more if the adapter needs to
  interact with SDP. Again, the info is provided in the reference
  documentation. 
- Apart from the transport methods above, you also most
  likely need to equip the adapter with additional APIs according to your
  application requirement. At the very least, you'd need an API to create
  the transport itself, as this API is not part of the framework.
- integrate your adapter to your PJSUA-LIB based
  application (see the next section)

.. note::

  :cpp:any:`pjmedia_transport_op::attach` and :cpp:any:`pjmedia_transport_op::detach`
  may be called more than once during a call, e.g. when the media is restarted
  e.g. due to call hold. 


Integrating custom transport adapter
---------------------------------------

Implement :cpp:any:`pjsua_callback::on_create_media_transport`
callback. This callback notifies application when media transport needs
to be created, and this is where the adapter is supplied to be used by
PJSUA-LIB. See the description in ticket :issue:`1173` for some more info. 

In the callback, create the adapter and return it to PJSUA-LIB. 

.. note::


  Be prepared that the transport adapter may be destroyed while the call
  is running, and/or the :cpp:any:`pjsua_callback::on_create_media_transport` callback is
  called again for the same call (thus this callback may be called more than once for a call).
  This happens when media is removed or added during a call.


The ``pjsua`` application contains sample code to create and integrate
the sample media transport adapter. Open :source:`pjsip-apps/src/pjsua/pjsua_app.c` and
look for ``TRANSPORT_ADAPTER_SAMPLE`` macro.

Reducing SIP message size
============================

.. note::

   PJSIP **automatically switches transport to TCP** when
   request size is larger than (default MTU) 1300  bytes, hence
   message size shouldn't be an issue. See ticket :issue:`831`
   for more info.

   See also :any:`Using SIP with TCP/TLS <sip_tcp_tls>`. TCP/TLS
   are probably better too in terms of NAT traversal and security
   issues.


This article provides several guidelines to reduce SIP message size.

#. Configure PJSIP to send compact form of SIP headers. This will 
   reduce SIP message size by approximately 50 bytes.
   
   .. code-block:: c
        
        extern pj_bool_t pjsip_use_compact_form;

        // enable compact form
        pjsip_use_compact_form = PJ_TRUE;
        
#. Suppress the inclusion of *Allow* header in outgoing requests, by setting
   :c:macro:`PJSIP_INCLUDE_ALLOW_HDR_IN_DLG` macro to 0 in :any:`config_site.h`.
   This will reduce SIP message size by approximately 86 bytes.
#. Suppress the inclusion of SDP ``rtpmap`` attribute for static payload types, by
   setting :c:macro:`PJMEDIA_ADD_RTPMAP_FOR_STATIC_PT` macro to 0 in
   :any:`config_site.h`. This should not cause bad effects since SDP ``rtpmap``
   attributes for static payload types are optional.
   This will reduce SIP message size by approximately 65 bytes.
#. Disable RTCP (advertisement) in SDP, by setting
   :c:macro:`PJMEDIA_ADVERTISE_RTCP` macro to 0 in :any:`config_site.h`. When RTCP is
   disabled, no RTCP packets will be sent or received, and this will cause
   some RTCP TX statistics (including RTT report) to be unavailable. Other
   RTCP statistics such as RX statistics, as well as number of TX packets,
   will still be available since these values are generated locally.
   Disabling RTCP will reduce SIP message size by approximately 235 bytes
   for ICE with three candidates.
#. Disable bandwidth modifier in SDP, by
   setting :c:macro:`PJMEDIA_ADD_BANDWIDTH_TIAS_IN_SDP` macro to 0 in
   :any:`config_site.h`. See the macro documentation for more info.
   This will reduce SIP message size by approximately 14 bytes.
#. If DTMF via RFC2833/``telephone-event`` is not needed, it can
   be disabled by setting :c:macro:`PJMEDIA_RTP_PT_TELEPHONE_EVENTS` macro to 0 in
   :any:`config_site.h`. This will reduce SIP message size by approximately 53 bytes.
#. Disable some unused network interfaces in the
   system to reduce the number of ICE candidates advertised in SDP. It's quite common
   to have some loopback network interfaces which probably are unused.
#. In pjsua, you can use ``--use-compact-form`` option to reduce the message
   size.

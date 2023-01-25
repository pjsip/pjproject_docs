.. _qos:

QoS Support
==============================================

.. contents:: Table of Contents
    :depth: 3

This article describes the QoS support in PJSIP and how to use it.

Introduction on QoS
---------------------------

QoS settings are available for both Layer 2 and Layer 3 of TCP/IP protocols:

Layer 2: IEEE 802.1p for Ethernet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


IEEE 802.1p tagging will mark frames sent by a host for prioritized delivery using a 3-bit Priority field in the virtual local area network (VLAN) header of the Ethernet frame. The VLAN header is placed inside the Ethernet header, between the Source Address field and either the Length field (for an IEEE 802.3 frame) or the !EtherType field (for an Ethernet II frame).

Layer 2: WMM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the Network Interface layer for IEEE 802.11 wireless, the Wi-Fi Alliance certification for Wi-Fi Multimedia (WMM) defines four access categories for prioritizing network traffic. These access categories are (in order of highest to lowest priority) voice, video, best-effort, and background. Host support for WMM prioritization requires that both wireless network adapters and their drivers support WMM. Wireless access points (APs) must have WMM enabled.

Layer 3: DSCP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the Internet layer, you can use Differentiated Services/Diffserv and set the value of the Differentiated Services Code Point (DSCP) in the IP header. As defined in RFC 2472, the DSCP value is the high-order 6 bits of the IP version 4 (IPv4) TOS field and the IP version 6 (IPv6) Traffic Class field.

Layer 3: Other
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other mechanisms exist (such as RSVP, IntServ) but this will not be implemented.


Availability
---------------------------

Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table summarizes the availability/accessability of various QoS settings on platforms that PJSIP supports. "XXX is supported" row shows whether the OS is able to set that QoS setting. Whether that setting can be controlled programmatically depends on "XXX is user settable" row. For example, on Windows Mobile 6 (WM6), both DSCP and WMM priority can be changed by the OS, but these settings are applied based on ``IP_DSCP_TRAFFIC_TYPE`` and user (i.e. PJLIB) cannot directly change the DSCP and WMM prio settings.

.. list-table:: QoS availability
   :header-rows: 1

   * - 
     - XP, Vista, WM2003, WM5
     - WM6
     - Linux
     - MacOS X
     - iPhone
     - Android
   * - High level API
     - No
     - Yes
     - Yes
     - Yes
     - Yes
     - Yes [1]
   * - API backend
     - qos_dummy.c
     - qos_wm.c
     - qos_bsd.c
     - qos_bsd.c
     - qos_bsd.c
     - qos_bsd.c
   * - DSCP is supported
     - No
     - Yes
     - Yes
     - Yes
     - Yes
     - Yes
   * - DSCP is user settable
     - No
     - no
     - Yes
     - Yes
     - Yes
     - Yes
   * - WMM prio is supported
     - No
     - Yes
     - No
     - No
     - No
     - No
   * - WMM prio is user settable
     - No
     - No
     - No
     - No
     - No
     - No
   * - SO_PRIORITY is supported
     - No
     - No
     - Yes
     - Yes
     - Yes
     - Yes
   * - SO_PRIORITY is settable
     - No
     - No
     - Yes
     - Yes
     - Yes
     - Yes [3]


Notes:
 1) Via PJSUA2 API :cpp:any:`pj::TransportConfig::qosType` and :cpp:any:`pj::TransportConfig::qosParams` fields.
 2) On win32, sock_qos_dummy.c is used by default. Set :cpp:any:`PJ_QOS_IMPLEMENTATION` to :cpp:any:`PJ_QOS_BSD` to enable the use of sock_qos_bsd.c.
 3) In our test, setting SO_PRIORITY showed no error, but wireshark traffic revealed that it's not set.

Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DSCP is available via IP TOS option. 

Ethernet 802.1p tagging is done by setting ``setsockopt(SO_PRIORITY)`` option of the socket, then with the ``set_egress_map option`` of the ``vconfig utility`` to convert this to set vlan-qos field of the packet. 

WMM is not known to be available.

MacOS X
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DSCP is available via IP TOS option. 

Windows and Windows Mobile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(It's a mess!)

DSCP is settable with ``setsockopt()`` on Windows 2000 or older, but Windows would silently ignore this call on WinXP or later, unless administrator modifies the registry. On Windows 2000, Windows XP, and Windows Server 2003, GQoS (Generic QoS) API is the standard API, but this API may not be supported in the future. On Vista and Windows 7, the is a new QoS2 API, also known as Quality Windows Audio-Video Experience (qWAVE).

IEEE 802.1p tagging is available via Traffic Control (TC) API, available on Windows XP SP2, but this needs administrator access. For Vista and later, it's in qWAVE. 

WMM is available for mobile platforms on Windows Mobile 6 platform and Windows Embedded CE 6, via ``setsockopt(IP_DSCP_TRAFFIC_TYPE)``. qWAVE supports this as well.


Update 2022: Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- TLDR; two ways to achieve QoS on Windows: with QoS2/qWAVE API or by using Policy-based. [1]
- QoS2/qWAVE API requires the app to be a member of Administrators or Network Configuration Operators group [2].
- Using Policy-based QoS, it works without any changes in the app, but it requires the user 
  (or network administrator) to set up the QoS Policy. A sample setup is `discussed here <https://community.cisco.com/t5/collaboration-knowledge-base/enable-dscp-marking-in-windows-os-7-8-10/tac-p/3849518/highlight/true#M9259>`__.
  DSCP tagging can be set per application/IP-port/protocol basis.

PJLIB currently does not support QoS2/qWAVE, and supporting it requires major modifications:

#. QoS needs to be set after the socket is connected, or if it is not connected yet, the remote 
   destination address needs to be specified [3]. While currently the PJLIB QoS interface does not 
   require that, so in many places in the library, the QoS is set up right after the socket is 
   instantiated and when the remote address may not be known yet.
#. The QoS2 API employs a QoS handle that needs to be closed after use. So the PJLIB socket mechanism will 
   need to be changed to be able to store and close a QoS handle.

References:

1. https://web.archive.org/web/20151208005603/http://blogs.msdn.com/b/wndp/archive/2006/07/05/657196.aspx
2. https://docs.microsoft.com/en-us/windows/win32/api/qos2/nf-qos2-qossetflow#parameters
3. https://docs.microsoft.com/en-us/windows/win32/api/qos2/nf-qos2-qosaddsockettoflow#parameters


Symbian S60 3rd Ed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both DSCP and WMM is supported via ``RSocket::SetOpt()`` with will set both Layer 2 and Layer 3 QoS settings accordingly.


Objective
---------------------------

The objective of this ticket is to add new API to PJLIB socket API to enable manipulation of the QoS parameters above in a uniform and portable manner.



Design
---------------------------

Based on the above, the following API is proposed.

Declare the following "standard" traffic types.

.. code-block:: c

    typedef enum pj_qos_type
    {
        PJ_QOS_TYPE_BEST_EFFORT,
        PJ_QOS_TYPE_BACKGROUND,
        PJ_QOS_TYPE_VIDEO,
        PJ_QOS_TYPE_VOICE,
        PJ_QOS_TYPE_CONTROL
    } pj_qos_type;
 
The traffic classes above will determine how the Layer 2 and 3 QoS settings will be used. The standard mapping between the classes above to the corresponding Layer 2 and 3 settings are as follows:

.. list-table:: Mapping between PJLIB QoS type and network settings
   :header-rows: 1

   * - PJLIB Traffic Type
     - IP DSCP
     - WMM
     - 802.1p
   * - :cpp:any:`PJ_QOS_TYPE_BEST_EFFORT`
     - 0x00
     - :cpp:any:`PJ_QOS_WMM_PRIO_BULK_EFFORT`
     - 0
   * - :cpp:any:`PJ_QOS_TYPE_BACKGROUND`
     - 0x08
     - :cpp:any:`PJ_QOS_WMM_PRIO_BULK`
     - 2
   * - :cpp:any:`PJ_QOS_TYPE_VIDEO`
     - 0x28
     - :cpp:any:`PJ_QOS_WMM_PRIO_VIDEO`
     - 5
   * - :cpp:any:`PJ_QOS_TYPE_VOICE`
     - 0x30
     - :cpp:any:`PJ_QOS_WMM_PRIO_VOICE`
     - 6
   * - :cpp:any:`PJ_QOS_TYPE_CONTROL`
     - 0x38
     - :cpp:any:`PJ_QOS_WMM_PRIO_VOICE`
     - 7
   * - :cpp:any:`PJ_QOS_TYPE_SIGNALLING`
     - 0x28
     - :cpp:any:`PJ_QOS_WMM_PRIO_VIDEO`
     - 5



There are two sets of API provided to manipulate the QoS parameters. 

Portable High Level API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first set of API is:

.. code-block:: c

        // Set QoS parameters
        PJ_DECL(pj_status_t) pj_sock_set_qos_type(pj_sock_t sock,
                                                pj_qos_type val);

        // Get QoS parameters
        PJ_DECL(pj_status_t) pj_sock_get_qos_type(pj_sock_t sock,
                                                pj_qos_type *p_val);


The API will set the traffic type according to the DSCP class, for '''both''' Layer 2 and Layer 3 QoS settings, where it's available. If any of the layer QoS setting is not settable, the API will silently ignore it. If '''both''' layers are not setable, the API will return error.

The API above is the recommended use of QoS, since it is the most portable across all platforms.

Fine Grained Control API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second set of API is intended for application that wants to fine tune the QoS parameters.

The Layer 2 and 3 QoS parameters are stored in :cpp:any:`pj_qos_params` structure:

.. code-block:: c

    typedef enum pj_qos_flag
    {
        PJ_QOS_PARAM_HAS_DSCP = 1,
        PJ_QOS_PARAM_HAS_802_1_P = 2,
        PJ_QOS_PARAM_HAS_WMM = 4
    } pj_qos_flag;

    typedef enum pj_qos_wmm_prio
    {
        PJ_QOS_WMM_TYPE_BULK_EFFORT_PRIO,
        PJ_QOS_WMM_TYPE_BULK_PRIO,
        PJ_QOS_WMM_TYPE_VIDEO_PRIO,
        PJ_QOS_WMM_TYPE_VOICE_PRIO
    } pj_qos_wmm_prio;

    typedef struct pj_qos_params
    {
        pj_uint8_t      flags;    // Determines which values to 
                                  // set, bitmask of pj_qos_flag
        pj_uint8_t      dscp_val; // DSCP value to set
        pj_uint8_t      so_prio;  // SO_PRIORITY value
        pj_qos_wmm_prio wmm_prio; // WMM priority value
    } pj_qos_params;
        

The second set of API with more fine-grained control over the parameters are:

.. code-block:: c

        // Retrieve QoS params for the specified traffic type
        PJ_DECL(pj_status_t) pj_qos_get_params(pj_qos_type type, 
                                               pj_qos_params *p);

        // Set QoS parameters to the socket
        PJ_DECL(pj_status_t) pj_sock_set_qos_params(pj_sock_t sock,
                                                    const pj_qos_params *p);

        // Get QoS parameters from the socket
        PJ_DECL(pj_status_t) pj_sock_get_qos_params(pj_sock_t sock,
                                                    pj_qos_params *p);

        

**Important:**
 
The :cpp:any:`pj_sock_get_qos_params()` and :cpp:any:`pj_sock_set_qos_params()` APIs are not portable, and it is probably only going to be implemented on Linux. Application should always try to use :cpp:any:`pj_sock_set_qos_type()` instead.


Limitations
---------------------------

Win32 currently is not be implemented.


Using QoS in PJSIP Applications
---------------------------------

PJSUA-LIB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On PJSUA-LIB, QoS parameters have been added to :cpp:any:`pjsua_transport_config`.

**Examples**

To set QoS of RTP/RTCP traffic to '''Voice''' type (this will activate the appropriate DSCP, WMM, and SO_PRIORITY settings, if the OS supports it):

.. code-block:: c

  // Media transport setting is configurable on per account basis
  pjsua_acc_config acc_cfg;

  pjsua_acc_config_default(&acc_cfg);
  // Set account settings
  ...
  // Set media transport settings (listening start port etc) according to app settings
  ...
  // Set media transport traffic type to Voice
  acc_cfg.rtp_cfg.qos_type = PJ_QOS_TYPE_VOICE;

  // Create account with this config
  pjsua_acc_add(&acc_cfg, ...);


To tag SIP transport traffic with a specific DSCP value (in this case, DSCP CS3 or value 24). Note that not all platforms allow this, see the table above:

.. code-block:: c

  pjsua_transport_config sip_tcfg;

  pjsua_transport_config_default(&sip_tcfg);
  // Set listening port etc according to app settings
  ...
  // Set QoS to DSCP CS3 (DSCP value 24)
  sip_tcfg.qos_params.flags = PJ_QOS_PARAM_HAS_DSCP;
  sip_tcfg.qos_params.dscp_val = 24;

  // Create SIP transport with this config
  pjsua_transport_create(..., &sip_tcfg, ...);



Low Level Transports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using the low level transports (such as SIP transports, media transports, or STUN/TURN/ICE transports) directly instead of from PJSUA-LIB, the QoS settings are available in one of its creation parameters. Hint: they are normally named as ``qos_type`` and ``qos_params``.



References
---------------------------

1. `QoS Support in Windows <http://technet.microsoft.com/en-gb/magazine/2007.02.cableguy.aspx>`__ - good intro for QoS on Windows and in general
2. `WMM (Wi-Fi Multimedia) <http://msdn.microsoft.com/en-us/library/aa916767.aspx>`__ (Windows Mobile 6)
3. `VoIP developer guidelines for S60 <http://wiki.forum.nokia.com/index.php/VoIP_developer_guidelines_for_S60>`_
4. `WiFi QoS Support in Windows Vista: WMM part 2 <http://blogs.msdn.com/wndp/archive/2006/06/30/WiFi_QoS_Support_in_Windows_Vista_part_2.aspx>`_
5. Apple SO_NET_SERVICE_TYPE: https://github.com/pjsip/pjproject/issues/1964
6. IPV6_TCLASS: https://github.com/pjsip/pjproject/issues/1963

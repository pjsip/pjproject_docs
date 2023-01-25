Getting Around Blocked, Filtered, or Mangled VoIP Network
=========================================================

.. contents:: Table of Contents
    :depth: 2


VoIP traffic may be blocked or filtered or mangled by a network element
in the middle (NEITM), which could be an edge router (e.g. your home
ADSL router), the network provider (e.g. on 3G network), or some other
entities. This document explains several settings that can be used to
help traversing this kind of network.

Use TCP/TLS for SIP Traffic
---------------------------

**Problems to solve** 

        SIP messages are blocked, filtered, or mangled by intermediate network entities.

**Solution**

        Sometimes it is possible to avoid the filtering simply by changing the SIP transport from UDP to TCP. Obviously using TLS will make it impossible to alter the traffic, so if TCP doesn’t solve it, TLS may be the answer.

        To use TCP, instantiate a TCP listener, then either add ``";transport=tcp"`` parameter to all destination URIs, or add a proxy/Route entry containing a destination with ``";transport=tcp"`` parameter. For example, with pjsua:

        .. code-block:: shell

                pjsua --proxy "sip:example.org;lr;transport=tcp"

        You will need to configure your proxy to record route so that the proxy is always reachable via TCP (otherwise if the UAS sends a Contact URI without ``";transport=tcp"`` parameter, we will send subsequent requests within the dialog via UDP).


Disable STUN
------------

**Problems to solve**

        Sometimes NEITM employs its own tricks to assist NAT traversal, often by mangling many SIP and SDP fields so that they are more Internet friendly (or so it thinks). Because the client is already doing its own NAT traversal tricks, the combination could create a SIP message that is even more confusing to route.

        In other cases, NEITM also mangles STUN responses, injecting mapped address that is invalid, or worse causing invalid STUN responses to be returned back to client.

        In the worst case scenario, STUN may be blocked altogether.

**Solution**

        For the problems above, you may consider disabling STUN altogether! This may sound like a silly approach but it does work especially if NEITM actively mangles SIP messages to assist NAT traversal (I assume it's because then it will be easier for it to spot the private IP addresses which need mangling in a SIP message).

        In the case where NEITM doesn't assist NAT traversal, your server (in public Internet) must terminate RTP traffic, because RTP traffic won't be able to go end to end between clients.


Relay RTP via TURN/TCP
----------------------

**Problems to solve**
        
        Use this when RTP traffic is blocked by what seems to be a packet inspection NEITM.

**Solution**

        #. You will need to install and provision a TURN relay server (e.g. from http://www.turnserver.org) 
        #. Enable TCP client connection in your TURN server
        #. In your PJSIP client, enable ICE and TURN and TURN TCP connection (i.e.-turn-tcp option). When TURN is used, the TURN address will be used as the default address in SDP, so this solution would still work even if remote doesn't support ICE.

Use Non-standard Ports for VoIP Services
----------------------------------------

**Problems to solve**

        Avoiding detection of SIP/STUN/TURN traffic.

**Solution**

        Change the port number of your SIP, STUN, and TURN servers to use non-standard port. Masquerading well known ports such as 80, 53, or 443 may be better.

        Note that for SIP, there is a problem with using non-standard port, as described below: 
        
        #. According to SIP spec (`RFC 3261 <http://tools.ietf.org/html/rfc3261>`__), port number is not allowed to appear in From and To headers. See Table 1 in Section 19.1.1 (`page 152 <http://tools.ietf.org/html/rfc3261#page-152>`__). 
        #. For example, your domain is **example.org** and you set your server to listen at port **5070**, all SIP requests will have the **From** header without the port number in its URI part, e.g. **From: sip:alice@example.org**. 
        #. The receiver of such message may want to save the sender address of a request, for example, to add a new buddy from an incoming MESSAGE request. 
        #. Problem arises when that client wants to send a request to the new buddy; in that case, the request will be sent to default port instead of to the non-standard port (because the original From header was missing port number).

        Provisioning DNS SRV entries for your SIP domain would avoid above problems.

        Alternatively, you could override PJSIP settings to allow using port number in To and From headers with the following code (but mind you this would inject a non-standard SIP messages in your network):

        .. code-block:: shell

                pjsip_cfg()->endpt.allow_port_in_fromto_hdr = PJ_TRUE;


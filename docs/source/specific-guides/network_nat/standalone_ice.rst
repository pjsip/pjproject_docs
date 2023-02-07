Using ICE in non-SIP Applications
=======================================================

.. contents:: Table of Contents
    :depth: 2


This article describes how to use the ICE stream transport of :doc:`PJNATH </api/pjnath/index>` in a standalone, probably non-SIP/SDP applications.

.. tip::

        See **icedemo.c** in the :doc:`/api/samples` page for a working demo

While reading this article, it's recommended to also open the :doc:`ICE stream transport </api/generated/pjnath/group/group__PJNATH__ICE__STREAM__TRANSPORT>` page for more detailed info for the API. This article will provide links to the API in that page for further reading about the detail specification of the API.

Introduction
----------------------

The :doc:`PJNATH </api/pjnath/index>` (PJSIP NAT Traversal Helper) library contains various objects to assist application with NAT traversal, using standard based protocols such as STUN, TURN, and ICE. The "ultimate" object in the library is the :doc:`ICE stream transport </api/generated/pjnath/group/group__PJNATH__ICE__STREAM__TRANSPORT>` (will be called *ice_strans* for short in this article), where it wraps the STUN, TURN, and ICE functionality in one object and provides applications with API to send and receive data, as well as to perform ICE session management.

From the library design point of view, all features in PJNATH are implemented in two layers, the transport independent/session layer, and the transport layer. The session layer contains only the logic to manage the corresponding session (for example, STUN, TURN, and ICE session). The transport layer wraps together the session object with socket(s) to make them ready to use transport objects.

This article assumes that the application wants to use ICE transport, and not the ICE session (layer).


Terminology
-----------

The following are some terms used throughout this article:

- **ICE stream transport (ice_strans)**

  This is the PJNATH *class* name for the transport that implement ICE negotiation, as explained above. The actual struct name is :cpp:any:`pj_ice_strans`.

- **ICE session**

  This represents one multimedia session (e.g. one *call* session) between two ICE endpoints, within the *ice_strans*. One *ice_strans* object may be reused to facilitate multiple ICE sessions (but not simultaneously).

- **ICE endpoint**

  The application that implements ICE. It is synonymous for ICE agent in the RFC.


Fitting ICE in the application
------------------------------

To use ICE, the application would need to replace it's send/receive socket(s) with :cpp:any:`pj_ice_strans` object (will be called *ice_strans* for short). Once the ICE session in *ice_strans* is up and running, application uses :cpp:any:`pj_ice_strans_sendto()` to send data, and registers :cpp:any:`pj_ice_strans_cb::on_rx_data` to receive incoming data.

For SIP/SDP usage, one *ice_strans* is good for one media stream, and one media stream may contain more than one media transports, or called component in ICE terms (e.g. one RTP and one RTCP). Each component typically will be provided with more than one candidates, e.g. local candidates, STUN candidate, and TURN candidate. It will be then ICE's job to work out which candidate pair to use for the session.

For non-SIP usage, it will be application's design decision whether to create one *ice_strans* with multiple components, or multiple *ice_strans* with one component, or combination of both. Using former would definitely be simpler since we only need to work with one session, but the later would have the advantage of faster negotiation (by tens to hundreds of msecs) since the two *ice_strans* objects can then do the negotiation in parallel.


Preparations
------------

Before using PJNATH's ICE, several steps need to be done.

The PJNATH library depends on the following libraries, hence they need to be built and added to the application's linking specifications: 

* :doc:`/api/pjlib/index`
* :doc:`/api/pjlib-util/index`

Several PJLIB objects need to be prepared by applications: 

* at least one :cpp:any:`pj_pool_factory` instance is required for all PJLIB's based application. The memory pool factory is used to manage memory allocations by the libraries.
* at least one :cpp:any:`pj_timer_heap_t` instance for managing the timers 
* at least one :cpp:any:`pj_ioqueue_t` instance for managing network I/O events.

One object of each typically is enough, although application may create more to fine tune the performance (by limiting the number of objects that each manages) or for other reasons.

Once these objects are created, there need to be something that polls the timer heap and the ioqueue (except on Symbian where polling is not used). Typically application would create at least one thread to do this polling.

These are pretty *basic* tasks that are required for all PJLIB network based applications, so please see the samples for some code snippets.


Basic lifecycle
---------------

The following are brief overview about the basic life cycle of
*ice_strans*. Each of the steps above will be explained in subsequent
sections: 

* create *ice_strans* 
* wait for initialization (a.k.a candidate gathering process) to complete 
* start ICE session: 

  - create ICE session 
  - exchange ICE info with remote (username, password, candidate list). 
  - start ICE negotiation 
  - wait for negotiation to complete 
  - exchange data between endpoints 
  - destroy the ICE session 
  - repeat above to start new ICE session 

* destroy *ice_strans*


Creating the ICE stream transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create the *ice_strans*: 

* initialize the :cpp:any:`pj_ice_strans_cfg`, calling :cpp:any:`pj_ice_strans_cfg_default()` beforehand. Among other things, this structure contains settings required to enable and use STUN and TURN, as well as instances of the memory pool  factory, timer heap and ioqueue (mentioned earlier) in the *stun_cfg* field.
* call :cpp:any:`pj_ice_strans_create()`
* wait for the :cpp:any:`pj_ice_strans_cb::on_ice_complete` callback to be called with *op* argument of :cpp:any:`PJ_ICE_STRANS_OP_INIT`, to indicate the status of the candidate gathering process (e.g. the result of STUN binding request and TURN allocation operations). The status of this candidate gathering process will be indicated in the *status* argument of the callback, with *PJ_SUCCESS* indicates succesful operation.

Once *ice_strans* is created, it can be used to create ICE sessions. One ICE session represents one multimedia session between endpoints (i.e. one call session). After one session completes, the same *ice_strans* can be used to facilitate further sessions. Only one session may be active in one *ice_strans* at the same time.


Working with session
~~~~~~~~~~~~~~~~~~~~

The steps to use the session are typically as follows.

Session creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the session by calling :cpp:any:`pj_ice_strans_init_ice()`, specifying the initial role of the (ICE) endpoint and optionally, the local username and password.

.. note::
        
   The role affects ICE's negotiation behavior, especially to determine which endpoint is the *controlling* side. While ICE provides *role conflict* resolution in its negotiation process, it's always recommended to supply this with correct initial value to avoid unnecessary round-trips for the *role conflict* resolution.

Exchanging ICE information with remote endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before ICE negotiation can start, each ICE endpoint would need to know the ICE information of the other endpoint. On SIP/SDP usage, this will happen when the application exchanges SDP's between each other. For non-SIP usage, this will be up to exchange this information (as well as how to encode it).

The following information needs to be sent to remote ICE endpoint: 

* the local ICE session's username and password (the so called *ufrag*/user fragment and password). 
* the candidate list for each and all ICE components. The :cpp:any:`pj_ice_strans_enum_cands()` function is used to list the candidates of the specified ICE component. For each candidate, the following information needs to be exchanged: 

  - component ID 
  - candidate type (i.e. host, srflx, or relay) 
  - foundation ID 
  - priority 
  - transport type (only UDP is supported for now) 
  - transport address (address family, IP address, and port) 
  - optional related address (e.g. for srflx/STUN candidate, the related address is the local address where STUN request is sent from). This would only be used for troubleshooting purposes and is not required by *ice_strans*.

* optionally the default candidate address for each ICE component. If remote doesn't support ICE, it can send data to this address. Application may also use this address to exchange data while ICE negotiation is in progress. The default candidate should be chosen from the candidate that is most likely to succeed, e.g. TURN, STUN, or one of the local candidate, in this order. Application may use :cpp:any:`pj_ice_strans_get_def_cand()` function to get the default candidate from the *ice_strans*.

How to encode/decode as well as to exchange the above information in non-SIP usage is up to the application/usage scenario. In PJSIP sample usage where ICE is integrated with media transport, the task to encode/decode the above information is done by the PJMEDIA's ICE transport (pjmedia/transport_ice.[hc]), and the information will be exchanged in SDP offer/answer. Below is a sample SDP generated by PJSIP which contains ICE information, with the relevant ICE attributes in **bold**:


.. raw:: html

        <pre>
        v=0
        o=- 3423381096 3423381096 IN IP4 81.178.x.y
        s=pjmedia
        c=IN IP4 <b>81.178.x.y</b>
        t=0 0
        a=X-nat:5
        m=audio <b>4808</b> RTP/AVP 103 102 104 117 3 0 8 9 101
        <b>a=rtcp:4809 IN IP4 81.178.x.y</b>
        a=rtpmap:103 speex/16000
        a=rtpmap:102 speex/8000
        a=rtpmap:104 speex/32000
        a=rtpmap:117 iLBC/8000
        a=fmtp:117 mode=30
        a=sendrecv
        a=rtpmap:101 telephone-event/8000
        a=fmtp:101 0-15
        <b>a=ice-ufrag:2b2c6196</b>
        <b>a=ice-pwd:06ea0fa8</b>
        <b>a=candidate:Sc0a80e 1 UDP 1698815 81.178.x.y 4808 typ srflx raddr 10.0.0.1 rport 4808</b>
        <b>a=candidate:Hc0a80e 1 UDP 2135151 192.168.0.14 4808 typ host</b>
        <b>a=candidate:Sc0a80e 2 UDP 1698814 81.178.x.y 4809 typ srflx raddr 10.0.0.1 rport 4809</b>
        <b>a=candidate:Hc0a80e 2 UDP 2135150 192.168.0.14 4809 typ host</b>
        </pre>

(Note: the c= and a=rtcp lines contain the default ICE candidate address for the RTP and RTCP components respectively. Public IP addresses have also been scrambled a bit in the SDP above to protect the innocence).

The *ice_strans* would also need to **receive** the above information before it can start ICE negotiation.


Starting ICE negotiation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once ICE endpoints have sent/received ICE information to/from remote, they can start ICE negotiation by calling :cpp:any:`pj_ice_strans_start_ice()`. This function would need the above ICE information as its arguments.
Each endpoint will need to call this in order for the negotiation to succeed.

ICE negotiation then will start.

.. note::

   The timing when each endpoint starts :cpp:any:`pj_ice_strans_start_ice()` doesn't have to be absolutely simultaneously, though the more synchronized the better of course to speed up negotiation, and there is also limit of approximately 7-8 seconds before ICE negotiation will complete with timeout status.


Getting ICE negotiation result
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Application will be notified about the result in the (again) in :cpp:any:`pj_ice_strans_cb::on_ice_complete` callback, although this time with *op* argument of :cpp:any:`PJ_ICE_STRANS_OP_NEGOTIATION`. The status of the operation will be indicated in the *status* argument of the callback, with PJ_SUCCESS indicates succesful negotiation.

.. note::

   * It is possible that the number of components between the two ICE endpoints are different, e.g. we support RTCP but remote doesn't. The :cpp:any:`pj_ice_strans_get_running_comp_cnt()` function can be used (after ICE negotiation completes) to find out how many components have been negotiated by ICE. Application can always deduce this information by comparing its local candidate list against remote's of course.
   * See also the remarks about negotiation time in the global **Notes** section at the end of this article.


Sending and Receiving Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use :cpp:any:`pj_ice_strans_sendto()` to send data to remote ICE endpoint. Incoming data will be reported in
 :cpp:any:`pj_ice_strans_cb::on_rx_data` callback.


Finishing with the session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the session is done (e.g. call has ended), call :cpp:any:`pj_ice_strans_stop_ice()` to clean up local resources allocated for the session.

Application may reuse this same *ice_strans* instance to start another session by repeating the steps from [#sess_create Session creation] above.


Destroying ICE stream transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use :cpp:any:`pj_ice_strans_destroy()` to destroy the ICE stream transport itself. This will initiate TURN deallocation procedure (if TURN in used), and ultimately will close down sockets as well as all resources allocated by this *ice_strans*
instance.

Note that *ice_strans* destruction will not complete immediately if TURN is used (since it needs to wait for deallocation procedure), hence it is important that polling to the timer heap and ioqueue continues to be done. Application will not be notified when *ice_strans* destruction completes, it just needs to assume that the *ice_strans* object is no longer usable as soon as :cpp:any:`pj_ice_strans_destroy()` is called.


Notes
---------------

Note that the information below applies to current PJSIP release (version 1.1 as of 2009/03/16). They may change (and definitely will be improved if we can) in subsequent releases.


Keep-alive
~~~~~~~~~~

Once the *ice_strans* is created, the STUN and TURN keep-alive will be done automatically and internally. The default STUN keep-alive period is 15 seconds (:c:macro:`PJ_STUN_KEEP_ALIVE_SEC`), and TURN is also 15 seconds (:c:macro:`PJ_TURN_KEEP_ALIVE_SEC`).


IP address change
~~~~~~~~~~~~~~~~~

Changes in STUN mapped address is handled automatically by *ice_strans* via the STUN keep-alive exchanges, although currently there is no callback to notify application about this event. Call to :cpp:any:`pj_ice_strans_enum_cands()` will get the updated address.

Changes in local interface's IP address are not detected.

If IP address change is of application's concern, currently we can only recommend the application to implement this detection, and restart the ICE session or destroy/recreate the *ice_strans* once it detects the IP address change.


Negotiation time
~~~~~~~~~~~~~~~~

.. tip::

        For quicker ICE negotiation, see :doc:`/specific-guides/network_nat/trickle_ice`

ICE negotiation may take tens to hundreds of milliseconds to complete. The time it takes to complete ICE negotiation depends on the number of candidates across all components in one single *ice_strans*, the round-trip time between the two ICE endpoints, as well as the signaling round-trip time since ICE information is exchanged using the signaling. In our brief (and strictly non-scientific!) test, it took about 100-150 msec to complete, in scenario where two (SIP) endpoints were behind different ADSL connections (both are in UK), with two components and 2-4 candidates per component. It is also worth mentioning that we used SIP proxy for the call (the SIP proxy was in US), hence the negotiation time depended on the SIP signaling round-trip as well.

But please also note that **it may take seconds** for ICE to report negotiation failure. ICE will wait until all STUN retransmissions have timed-out, and with the default setting, it will take 7-8 seconds before it will report ICE negotiation failure.


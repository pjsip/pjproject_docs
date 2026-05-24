Using SIP TCP Transport
=======================

.. contents:: Table of Contents
    :depth: 2


Enabling TCP support
-------------------------------

TCP support must be enabled in the build by setting :c:macro:`PJ_HAS_TCP` to non-zero. This is enabled by default, hence normally there's no specific step to do to enable this. You must then instantiate SIP TCP transport in your application, e.g.:

.. code-block:: c

   pjsua_transport_config tcfg;
   
   pjsua_transport_config_default(&tcfg); 
   status = pjsua_transport_create(PJSIP_TRANSPORT_TCP, &tcfg, &transport_id);


References:

- :cpp:any:`pjsua_transport_config`
- :cpp:any:`pjsua_transport_config_default()`
- :cpp:any:`pjsua_transport_create()`


Sending Initial Requests
------------------------------------

According to SIP spec, a request is sent to the address in the destination URI, which is the URI in the *Route* header if it is
present, or to the request URI if there is no Route header. PJSIP only sends the request with TCP if the destination URI contains ``“;transport=tcp"`` parameter. Hence to send request with TCP, the destination URI must contain this parameter. This can be accomplished in two ways:

1. The most convenient way is to add a route-set entry (with :cpp:any:`pjsua_acc_config::proxy` or :cpp:any:`pjsua_config::outbound_proxy` settings) containing URI with TCP transport. This way all **initial** requests will be sent with TCP via the proxy, and we don't need to change the URI for the registrar and all buddies in the buddy list. Sample code:

   .. code-block:: c
   
      pjsua_acc_config acc_cfg;
      
      ...
      acc_cfg.proxy[acc_cfg.proxy_cnt++] = pj_str("sip:proxy.example.com;transport=tcp");
   
   
   If the destination doesn't like the additional *Route* header, you can hide this Route header by adding ``“;hide"`` parameter to the route URI, for example:
   
   ::
   
      “sip:proxy.example.com;transport=tcp;hide"
   
   This way PJSIP will process the request as if the *Route* header is present, but the header itself will not actually put in the transmission.

2. If you don't want to configure route set entry, then you must add ``“;transport=tcp"`` parameter to all outgoing URIs (the registrar URI, the buddy URI, the target URI when making calls, the target URI when sending MESSAGE, etc.). For example, to make outgoing call with TCP: 

   ::
   
      pj_str_t dst = pj_str(“sip:alice@example.net;transport=tcp");
   
      status = pjsua_call_make_call(acc_id, &dst, NULL, NULL, NULL, NULL);


Contact Header
--------------------------

With PJSUA-LIB, when making or receiving calls with TCP, the local
Contact header will automatically be adjusted to use the TCP transport.

Subsequent Requests
-------------------------------

Subsequent requests means subsequent request that is sent within the
call (dialog), for example UPDATE, BYE, re-INVITE to hold the call, and
so on. Subsequent requests within a dialog will be sent to the URI that
is found in the top-most *Route* header which was built from the
*Record-Route* header in the response that established the dialog (it
could be the 18x or 200/OK response), or if there's no
*Route*/*Record-Route*, the URI in the *Contact* header of that
response.

It could be the case that the initial request is sent with TCP, but the
subsequent ones are with UDP. In this case, check the URI in the *Route*
or *Record-Route* or *Contact* header of the 18x or 2xx response that is
sent by the remote party. Chances are this header lacks the
``“;transport=tcp"`` parameter in the URI; in this case, you can take one
of the following measures:

 - Configure the other end to use TCP,
 - Configure your proxy to *record-route* (i.e. to force itself to be
   within the request path of the call).
 - Configure the transport of the accounts to have explicit control
   (:cpp:any:`AccountSipConfig::transportId`/:cpp:any:`Account::setTransport()`
   or :cpp:any:`pjsua_acc_config::transport_id`/:cpp:any:`pjsua_acc_set_transport()`).

Automatic Switch to TCP if Request is Larger than 1300 bytes
-----------------------------------------------------------------------
According to `RFC 3261 section 18.1.1 <http://tools.ietf.org/html/rfc3261#section-18.1.1>`__:

   “If a request is within 200 bytes of the path MTU, or if it is larger than 1300 bytes and the path MTU is unknown, the request MUST be sent using an RFC 2914 congestion controlled transport protocol, such as TCP."

By this rule, PJSIP will automatically send the request with TCP if the
request is larger than 1300 bytes. This feature was first implemented in
ticket :pr:`831`. The switching is done on request by request basis, i.e. if
an initial INVITE is originally meant to use UDP but end up being sent
with TCP because of this rule, then only that initial INVITE is sent
with TCP; subsequent requests will use UDP, unless of course if it's
larger than 1300 bytes. In particular, the Contact header stays the
same. Only the Via header is changed to TCP.

It could be the case that the initial INVITE is sent with UDP, and once
the request is challenged with 401 or 407, the size grows larger than
1300 bytes due to the addition of *Authorization* or
*Proxy-Authorization* header. In this case, the request retry will be
sent with TCP.

In case TCP transport is not instantiated, you will see error similar to
this:

   *"Temporary failure in sending Request msg INVITE/cseq=15228 (tdta02EB0530), will try next server. Err=171060 (Unsupported transport (PJSIP_EUNSUPTRANSPORT))*

As the error says, the error is not permanent, as PJSIP will send the
request anyway with UDP.

This TCP switching feature can be disabled as follows:

* at run-time by setting ``pjsip_cfg()->endpt.disable_tcp_switch`` to PJ_TRUE.
* at-compile time by setting ``PJSIP_DONT_SWITCH_TO_TCP`` to non-zero

You can also tweak the 1300 threshold by setting :c:macro:`PJSIP_UDP_SIZE_THRESHOLD` to the appropriate value.

Additional Info about Registration
------------------------------------------

The client registration session also will keep the TCP connection active
throughout the registration session, and server may send inbound
requests using this TCP connection if it wants to.

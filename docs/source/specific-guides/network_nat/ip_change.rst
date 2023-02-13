Handling IP address change
=========================================

.. contents:: Table of Contents
    :depth: 2


This article describes some issues and their corresponding solutions related to access point disconnection, reconnection, IP address change, and how to handle these events in your PJSIP applications, specifically 
for PJSIP version 2.7 or later. This wiki will focus on the new API :cpp:any:`pjsua_handle_ip_change()`.


Problem description
----------------------

IP address change and/or access point disconnection and reconnection are scenarios that need to be handled in mobile applications. Few issues or scenarios related to this for example are:

 - user moves outside the range of a Wi-Fi access point (AP) and lost the connection
 - user moves outside the range of one AP and reconnect to another
 - the handset may get new IP address if user reconnects to different AP


API: *pjsua_handle_ip_change()*
------------------------------------------------------------------
Since 2.7, pjsua API introduce a new API (:cpp:func:`pjsua_handle_ip_change()`) to handle IP address change. This way, application only needs to detect for IP address change event, and let the library
handle the IP address change based on the configuration. 



*pjsua_handle_ip_change()* flow
--------------------------------------------
When invoked, the stack will:

1. Restart the SIP transport listener

   This will restart TCP/TLS listener no matter whether they are enabled or not when the transport were created. If you don't have any use of the listener, you can disable this.
   However, if you do need this, then on some platform (e.g: on IOS), some delay is needed when restarting the the listener.

   ref: :cpp:any:`pjsua_ip_change_param::restart_listener` and :cpp:any:`pjsua_ip_change_param::restart_lis_delay`.

2. Shutdown the SIP transport used by account registration

   On some platform (e.g: iOS), it is necessary to shutdown the transport used by registration, since presumably the socket is already in a bad state.

   ref: ``ip_change_cfg.shutdown_tp`` in :cpp:class:`pjsua_acc_config`.

3. Update contact URI by sending re-Registration

   The server needs to be updated of the new Contact URI when the IP address changed. Set it to PJ_TRUE to allow the stack update contact URI to the server.

   ref: :cpp:member:`pjsua_acc_config::allow_contact_rewrite` and :cpp:member:`pjsua_acc_config::contact_rewrite_method`.

4. Hangup active calls or continue the call by sending re-INVITE

   You can either hangup or maintain the ongoing/active calls. If you intend to maintain the active calls, updating dialog's contact URI is required. This can be done by specifying :cpp:any:`pjsua_callback::PJSUA_CALL_UPDATE_CONTACT` to the reinvite flags. Note that, hanging up calls might be inevitable on some cases, please see
   **Network change to the same IP address type. (IPv4 to IPv4) or (IPv6 to IPv6)** section below.

   ref: :cpp:any:`pjsua_ip_change_acc_cfg::hangup_calls` and :cpp:any:`pjsua_ip_change_acc_cfg::reinvite_flags` in :cpp:class:`pjsua_acc_config::ip_change_cfg`


Notes and limitations
----------------------
To monitor the progress of IP change handling, application can use :cpp:member:`pjsua_callback::on_ip_change_progress` callback. The callback will notify application of these events:

- SIP transport listener restart,
- SIP transport shutdown,
- contact update (re-registration process), and
- calls hangup or retry (re-INVITE).

Related to maintaining a call during IP change, there are some scenarios that are currently not implemented by IP change mechanism, so application needs to handle manually: If IP change occurs during SDP negotiation (and it is not completed yet, so there cannot be another SDP offer), updating such call needs to be done in two steps:

#. Update Contact header, so remote endpoint can send its SDP answer to our new contact address, i.e: use UPDATE without SDP offer (:cpp:any:`PJSUA_CALL_NO_SDP_OFFER` :flag). Note that, not every endpoint supports UPDATE. Contact is used by remote to resolve target before sending new requests. If proxy is used, then you can probably skip this.
#. Update Contact header, so remote endpoint can send its SDP answer to our new contact address, i.e: use UPDATE without SDP offer (:cpp:any:`PJSUA_CALL_NO_SDP_OFFER` flag). Note that, not every endpoint supports UPDATE. Contact is used by remote to resolve target before sending new requests. If proxy is used, then you can probably skip this.
#. Update local media transport after SDP answer is received, by sending UPDATE/re-INVITE with :cpp:any:`PJSUA_CALL_REINIT_MEDIA` flag.

If IP change occurs before a call is confirmed, the call will be disconnected and reported to application via :cpp:any:`pjsua_callback::on_call_state`.


IP change scenarios
----------------------

Network change to the same IP address type. (IPv4 to IPv4) or (IPv6 to IPv6)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update contact process (re-Registration) and call handling (hang-up or continue the call) should be handled by the API (:cpp:func:`pjsua_handle_ip_change()`) without any special treatment from the application. 

Network change to a different IP address type. (IPv4 to IPv6) or (IPv6 to IPv4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you already know, IPv6 needs specific account configuration as described [wiki:IPv6 here].
On the case of IP address type change, then additional steps are required from application.

#. Once application detects a network with IP address type change, a new transport might need to be created.

#. Once the transport is available, app can bind the account to the new transport, change the account configuration needed for IPv6/IPv4, and call :cpp:func:`pjsua_handle_ip_change()`.

Notes: to maintain ongoing calls, update to RTP/RTCP address and update dialog's Contact is needed using re-INVITE. However sending re-INVITE might fail when route set is still using IPv4 (e.g: Record-route returned contains IPv4).
In this case, forcefully disconnect the call is recommended. 

.. code-block:: c

    static void ip_change_to_ip6()
    {
        ...
        //create new ipv6 transport, if it's not yet available. e.g: UDP6
        status = pjsua_transport_create(PJSIP_TRANSPORT_UDP6,
                                        &udp_cfg,
                                        &transport_id);
        ...

        // bind account to IPv6 transport
        pjsua_acc_set_transport(acc_id, transport_id);

        // modify specific IPv6 account configuration
        pjsua_acc_get_config(acc_id, app_config.pool, &acc_cfg);
        acc_cfg.ipv6_media_use = PJ_TRUE;
        acc_cfg.ip_change_cfg.hangup_calls = PJ_TRUE;	
        pjsua_acc_modify(acc_id, &acc_cfg);

        ...
        // handle ip change
        pjsua_ip_change_param_default(&param);
        pjsua_handle_ip_change(param);
    }



IP address change detection
----------------------------------

iOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Have a look at `Reachability API <https://developer.apple.com/library/content/samplecode/Reachability/Introduction/Intro.html>`__.

Android
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Have a look at `ConnectivityManager <https://developer.android.com/training/monitoring-device-state/connectivity-monitoring.html>`__.




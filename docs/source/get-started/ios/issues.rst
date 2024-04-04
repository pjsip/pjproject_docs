Common issues when developing iOS apps
===========================================

.. contents:: Table of Contents
    :depth: 2

Accepting calls in the background with PushKit
----------------------------------------------
Starting in iOS 9, 
`kCFStreamNetworkServiceTypeVoIP <https://developer.apple.com/library/ios/documentation/CoreFoundation/Reference/CFSocketStreamRef/index.html#//apple_ref/doc/constant_group/Stream_Service_Types>`__ is deprecated. 
Apple recommends that applications use VoIP Push Notifications 
(using **PushKit** framework) to avoid persistent connections as described in 
the `Apple's official doc <https://developer.apple.com/library/ios/documentation/Performance/Conceptual/EnergyGuide-iOS/OptimizeVoIP.html>`__.

This will require application to handle push notifications and integrate CallKit
in the application layer. Please check `Apple's doc
<https://developer.apple.com/documentation/pushkit/responding-to-voip-notifications-from-pushkit>`__ for more details.

For an example, you can check ipjsua sample app, and refer to :pr:`1941`.

CallKit integration and audio session (AVAudioSession) management
-----------------------------------------------------------------
**CallKit** requires application to configure audio session and start the call 
audio at specific times. Thus, to ensure a smooth integration, we disable the 
setup of audio session in our sound device wrapper to avoid conflict with 
application's audio session setting.
Starting from :pr:`1941`, application needs to set its own audio session 
category, mode, and activation/deactivation.

For an example of CallKit integration for incoming calls, please check
ipjsua sample app.

Crash after calling PJLIB APIs using Grand Central Dispatch (GCD)
----------------------------------------------------------------------
PJLIB API should be called from a registered thread, otherwise it will raise 
assertion such as   *"Calling pjlib from unknown/external thread..."*. 
With GCD, we cannot really be sure of which thread executing the PJLIB function. 

Registering that thread to PJLIB seems to be a simple and easy solution, 
however it potentially introduces a random crash which is harder to debug. 
Here are few possible crash scenarios:

  * PJLIB's :cpp:any:`pj_thread_desc` should remain valid until the registered thread 
    stopped, otherwise crash of invalid pointer access may occur, 
    e.g: in :cpp:any:`pj_thread_check_stack()`.
  * Some compatibility problems between GCD and PJLIB, see :pr:`1837` for more 
    info.

If you want to avoid any possibility of blocking operation by PJLIB (or any 
higher API layer such as PJMEDIA, PJNATH, PJSUA that usually calls PJLIB), 
instead of dispatching the task using GCD, the safest way is to create and 
manage your own thread pool and register that thread pool to PJLIB. 
Or alternatively, simply use PJSUA timer mechanism (with zero delay), 
see :cpp:any:`pjsua_schedule_timer()`/:cpp:any:`pjsua_schedule_timer2()` for more info.

Audio lost or other issues with interruption (by a phone call or an alarm), headset plug/unplug, or Bluetooth input
------------------------------------------------------------------------------------------------------------------------
It has been reported that any time an audio interruption happens, 
audio is lost until the application is killed/restarted.

Here is the reported working solution:

  * Application should be configured to receive interruption events, see 
    `Apple's AVAudioSession doc <https://developer.apple.com/reference/avfoundation/avaudiosession>`__.
  * Forcefully shutdown the sound device when interruption begins, 
    e.g: using :cpp:any:`pjsua_set_no_snd_dev()` for pjsua, or :cpp:any:`pj::AudDevManager::setNoDev()`
    for pjsua2
  * Restart the sound device after interruption ends, e.g: using :cpp:any:`pjsua_set_snd_dev()` 
    for pjsua, or :cpp:any:`pj::AudDevManager::setPlaybackDev()` and
    :cpp:any:`pj::AudDevManager::setCaptureDev()` for pjsua2.

Also note this is the recommended outline of the normal flow for audio interruption:

* on interruption begin
  
    #. hold the calls
    #. stop any other media if any (i.e. disconnect all connections in the bridge)
    #. by default, sound device will be stopped after some idle period after 
       there is no connection in the bridge, or alternatively just forcefully 
       shutdown the sound device.


* on interruption end

    #. unhold the calls
    #. resume any other media if any
    #. if sound device was not shutdown forcefully, first connection to the 
       bridge will cause sound device to be started, otherwise manual restarting 
       the sound device, by setting playback & capture device, is required.

.. _ios_bg:

SIP transport keepalive while in background
----------------------------------------------
As the process is normally suspended when application is in the background, 
the worker thread that handles TCP keepalive timer is also suspended. 
So basically application needs to schedule periodic wakeup to allow the 
library send TCP keep-alive. 

Sample code:

.. code-block::

     - (void)keepAlive {
        /* Register this thread if not yet */
        if (!pj_thread_is_registered()) {
            static pj_thread_desc   thread_desc;
            static pj_thread_t     *thread;
            pj_thread_register("mainthread", thread_desc, &thread);
        }

       /* Simply sleep for 5s, give the time for library to send transport
        * keepalive packet, and wait for server response if any. Don't sleep
        * too short, to avoid too many wakeups, because when there is any
        * response from server, app will be woken up again (see also #1482).
        */
        pj_thread_sleep(5000);
     }

     - (void)applicationDidEnterBackground:(UIApplication *)application
     {
        /* Send keep alive manually at the beginning of background */
        pjsip_endpt_send_raw*(...);

        /* iOS requires that the minimum keep alive interval is 600s */
        [application setKeepAliveTimeout:600 handler: ^{
          [self performSelectorOnMainThread:@selector(keepAlive)
                  withObject:nil waitUntilDone:YES];
        }];
     }

Make sure that keepalive feature of SIP transport is not disabled, see 
:c:macro:`PJSIP_TCP_KEEP_ALIVE_INTERVAL`  and :c:macro:`PJSIP_TLS_KEEP_ALIVE_INTERVAL`,
and the keepalive interval is set to less than 600s.

Alternatively, configuring server to send keepalive ping packet, if possible, 
and client responds back by sending keepalive pong to the server, 
so we have two-way traffic. As there is no way to detect incoming ping 
from server, currently application can just always send pong packet whenever 
it becomes active (application will be woken up when receiving TCP packet), 
e.g: send pong packet in ``UIApplication::applicationDidBecomeActive()``.

Unable to accept incoming call in background mode (iOS 8 or older)
-----------------------------------------------------------------------
Starting in iOS 9, this method to accept incoming call in bg is deprecated, 
please have a look at :ref:`this <ios_bg>`.

If while in the background, ipjsua (or your application) is unable to detect 
if there is an incoming call and display the local notification:

  #. Note that background feature only works with TCP.
  #. Make sure that voip is included in the required background modes 
     (UIBackgroundModes) in the application’s Info.plist file.
  #. Make sure that the TCP socket is successfully wrapped with CFReadStreamRef 
     (check if there is a message: "Failed to configure TCP transport for VoIP usage").
  #. Check whether you can accept the incoming call by bringing the app to the 
     foreground. If yes, make sure that the incoming call request comes from the 
     wrapped TCP socket (check the log for the INVITE request).

.. note:: 

     See also :any:`audio_troubleshooting_toc`.

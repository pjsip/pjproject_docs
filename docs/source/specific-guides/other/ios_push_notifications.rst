.. _guide_ios_push_notifications:

iOS Push Notifications
=========================

.. contents:: Table of Contents
    :depth: 2


This guide describes how to integrate PJSIP with iOS VoIP Push
Notifications (PushKit) and CallKit so an application can receive
incoming SIP calls while suspended or terminated, the way
production iOS softphones are expected to behave on modern iOS.

The reference implementation is the
:sourcedir:`pjsip-apps/src/pjsua/ios/ipjsua` sample, added by
:pr:`3913`. Code excerpts in this guide are extracted from
``ipjsuaAppDelegate.m`` in that sample. Apple-platform claims
(PushKit / CallKit / AVAudioSession behaviour) link out to Apple's
documentation rather than restate it here, since those policies
shift between iOS versions; this guide focuses on the **PJSIP side**
of the integration.


Why VoIP push is required
-------------------------

Historically PJSIP applications on iOS kept a long-lived TCP socket
to the SIP server, marked as a VoIP socket using
`kCFStreamNetworkServiceTypeVoIP <https://developer.apple.com/library/ios/documentation/CoreFoundation/Reference/CFSocketStreamRef/index.html#//apple_ref/doc/constant_group/Stream_Service_Types>`__,
so the OS could deliver inbound INVITEs to the suspended app.

That approach is no longer viable:

- iOS 9 deprecated the VoIP socket service type.
- iOS 16 actively **kills** apps that use it. PJSIP responded in
  :pr:`3253` by flipping the default of
  ``PJ_ACTIVESOCK_TCP_IPHONE_OS_BG`` to ``0`` — i.e. PJSIP no
  longer marks its TCP sockets as VoIP. Without that mark, the
  socket is suspended along with the app the moment it
  backgrounds.

The only sustainable pattern on modern iOS is therefore:

- The SIP server proxies / stores incoming INVITEs and sends a
  silent VoIP push (APNs) to the device.
- iOS wakes the app. The app drives PJSIP to send a fresh REGISTER
  to the SIP server, the server delivers the held INVITE, and the
  app accepts the call via CallKit.

This guide walks through both halves of that loop — the iOS-side
plumbing (PushKit registration, push handling, CallKit
integration) and the PJSIP-side configuration (re-registration,
audio session, IP-change handling, the thread-bridging idiom for
PJSIP calls).


Architecture overview
---------------------

The end-to-end flow for an incoming call::

    [Caller] ─INVITE→ [SIP server]
                            │
                            │ stores / suspends INVITE
                            │
                            └─VoIP push──→ [APNs] ──→ [Suspended app]
                                                          │
                                                          │ wakes; pushRegistry handler
                                                          │
                            ┌──REGISTER──────────────────┘
                            │
                            └──INVITE──→ [PJSIP] ──on_incoming_call→ [App]
                                                                       │
                                                                       │ reports to CallKit
                                                                       │
                                                          ←─CallKit answer
                                                                       │
                            ←──200 OK── [PJSIP] ←pjsua_call_answer←──┘
                                                  (via pjsua_schedule_timer2)

Key design points:

- The SIP server is the source of truth for "is there an inbound
  call". It must support holding an INVITE while the device is
  off-network and re-delivering once the device re-REGISTERs.
- The push payload itself is an opaque trigger; it doesn't carry
  the SIP INVITE. The app must re-REGISTER on every push.
- CallKit calls into the app on the main thread; PJSIP requires
  calls on a registered PJ thread. Crossing that boundary is the
  job of :cpp:any:`pjsua_schedule_timer2`.


App lifecycle
-------------

PJSIP needs different actions at each iOS app-lifecycle
transition. The reference behaviour from the sample, in order
of occurrence over an app's lifetime:

**App start** — ``application:didFinishLaunchingWithOptions:``

   Register the ``PKPushRegistry`` for VoIP push, request user
   notification + microphone permissions up-front (the prompts
   won't fire later from the background), set up the CallKit
   provider, attach a Reachability observer. PJSIP itself is not
   started yet — the app is awaiting the push token.

**Token received** — ``pushRegistry:didUpdatePushCredentials:``

   Format the token as a hex string. Start pjsua with
   :cpp:any:`pjsua_acc_config::reg_contact_uri_params` populated
   to embed the RFC 8599 push parameters in the REGISTER Contact
   URI. See the `PushKit token registration`_ subsection.

**Foreground operation**

   Normal PJSIP operation. Transport keep-alive runs at the
   configured interval (``PJSIP_TCP_KEEP_ALIVE_INTERVAL`` /
   ``PJSIP_TLS_KEEP_ALIVE_INTERVAL``); outgoing calls and
   presence work as usual.

**Entering background** — ``applicationDidEnterBackground:``

   Trigger one fresh REGISTER via the bridge dispatcher, then
   briefly sleep so it completes before iOS suspends:

   .. code-block:: objc

      - (void)applicationDidEnterBackground:(UIApplication *)application
      {
          SCHEDULE_TIMER(REREGISTER);
          /* Allow the re-registration to complete. */
          [NSThread sleepForTimeInterval:0.3];
      }

   After this, the TCP socket dies as iOS suspends the app's
   network access (with ``PJ_ACTIVESOCK_TCP_IPHONE_OS_BG=0``
   default). The device now relies on VoIP push for incoming
   calls until it returns to the foreground.

**VoIP push wake** — ``pushRegistry:didReceiveIncomingPushWithPayload:``

   Re-REGISTER (so the server delivers the held INVITE), activate
   the AVAudioSession, report the incoming call to CallKit. See
   the `Receiving an incoming VoIP push`_ subsection.

   .. note::

      The sample dispatches ``REREGISTER`` here. A safer
      alternative — particularly if the device may have switched
      networks while the app was suspended — is to dispatch
      ``HANDLE_IP_CHANGE`` instead.
      :cpp:any:`pjsua_handle_ip_change` is a superset of
      re-registration: it shuts down stale TCP/TLS transports,
      restarts the listener, and re-registers all accounts. The
      Reachability observer that normally fires
      ``HANDLE_IP_CHANGE`` may not run while the app is
      suspended, so an IP that changed during sleep can go
      undetected; calling it on push wake covers that gap at the
      cost of an extra transport restart in the no-change case.

**CallKit answer / end** — ``provider:performAnswerCallAction:``
/ ``provider:performEndCallAction:``

   Dispatch :cpp:any:`pjsua_call_answer` / :cpp:any:`pjsua_call_hangup`
   via the ``SCHEDULE_TIMER`` bridge. See `Bridging iOS handlers
   to PJSIP`_.

**IP change** — Reachability change observer

   Dispatch :cpp:any:`pjsua_handle_ip_change` via the bridge. See
   `IP-change handling`_ below.

**Returning to foreground** — ``applicationDidBecomeActive:``

   No PJSIP action required by default. The previously suspended
   TCP socket has either been replaced by a fresh registration on
   push wake, or will be re-established on the next user-initiated
   REGISTER / outgoing call.

**Termination** — ``applicationWillTerminate:``

   No special PJSIP action required. :cpp:any:`pjsua_destroy` for
   a clean shutdown is optional; most VoIP-push apps let iOS
   terminate the process without explicit teardown.

Subsequent sections expand on the entries that need PJSIP code
or configuration — token registration, push receive, the
thread-bridging idiom, audio session, and IP-change handling.


Application-side: PushKit and CallKit integration
--------------------------------------------------

PJSIP doesn't ship a PushKit / CallKit wrapper — the application
owns these layers. The patterns below summarise how the
:sourcedir:`ipjsua sample <pjsip-apps/src/pjsua/ios/ipjsua/ipjsuaAppDelegate.m>`
glues them to PJSIP.

PushKit token registration
~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``didFinishLaunchingWithOptions``, register a
``PKPushRegistry`` for VoIP push types and request user
notification permission:

.. code-block:: objc

   self.voipRegistry = [[PKPushRegistry alloc]
       initWithQueue:dispatch_get_main_queue()];
   self.voipRegistry.delegate = self;
   self.voipRegistry.desiredPushTypes = [NSSet setWithObject:PKPushTypeVoIP];

When the OS issues a push token, ``didUpdatePushCredentials``
fires. Stash the token, then start PJSIP:

.. code-block:: objc

   - (void)pushRegistry:(PKPushRegistry *)registry
       didUpdatePushCredentials:(PKPushCredentials *)credentials
       forType:(NSString *)type
   {
       /* Format the token as a hex string. */
       const char *data = [credentials.token bytes];
       self.token = [NSMutableString string];
       for (NSUInteger i = 0; i < [credentials.token length]; i++)
           [self.token appendFormat:@"%02.2hhx", data[i]];

       /* Now start pjsua. */
       [NSThread detachNewThreadSelector:@selector(pjsuaStart)
                              toTarget:self withObject:nil];
   }

The token reaches the SIP server inside the REGISTER request, as
:rfc:`8599` ("Push Notifications for SIP") Contact URI parameters.
PJSIP populates these from
:cpp:any:`pjsua_acc_config::reg_contact_uri_params` when sending
REGISTER:

.. code-block:: c

   /* During pjsua_acc_config setup, before pjsua_acc_add: */
   pj_ansi_snprintf(contact_uri_buf, sizeof(contact_uri_buf),
                    ";pn-provider=apns"
                    ";pn-param=%s.%s.voip"
                    ";pn-prid=%s",
                    team_id, bundle_id, token_hex);
   cfg.reg_contact_uri_params = pj_str(contact_uri_buf);

The three RFC 8599 parameters PJSIP appends to its Contact URI
on REGISTER:

- ``pn-provider`` — the push service. ``apns`` for Apple Push
  Notification Service.
- ``pn-param`` — service-specific payload. For APNs VoIP push the
  convention is ``<TeamID>.<BundleID>.voip``.
- ``pn-prid`` — the push token (hex-encoded).

The SIP server records this mapping on REGISTER and uses it to
issue an APNs push when an INVITE arrives for that AOR. See
:ref:`account-level-customization` for the broader account-level
field this builds on.

Receiving an incoming VoIP push
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When APNs delivers a VoIP push,
``pushRegistry:didReceiveIncomingPushWithPayload:`` fires. The
handler has a strict deadline — it must **initiate the CallKit
incoming-call report** (i.e. invoke
``reportNewIncomingCallWithUUID:update:completion:``) before
calling the push completion block. iOS may terminate the app if
the push completion fires without a CallKit report having been
issued. The report API itself is non-blocking: its inner
completion handler fires later, after CallKit processes the
report — that doesn't have to land before ``completion()``.

.. code-block:: objc

   - (void)pushRegistry:(PKPushRegistry *)registry
           didReceiveIncomingPushWithPayload:(PKPushPayload *)payload
           forType:(PKPushType)type
           withCompletionHandler:(void (^)(void))completion
   {
       NSUUID *uuid = [NSUUID UUID];

       /* Re-register, so the server will send us the suspended INVITE. */
       SCHEDULE_TIMER(REREGISTER);

       /* Activate audio session before CallKit grabs it. */
       AVAudioSession *audioSession = [AVAudioSession sharedInstance];
       [audioSession setCategory:AVAudioSessionCategoryPlayAndRecord
                            mode:AVAudioSessionModeVoiceChat
                         options:0
                           error:nil];
       [audioSession setActive:YES error:nil];

       /* Report the incoming call to CallKit. */
       CXCallUpdate *callUpdate = [[CXCallUpdate alloc] init];
       [self.provider reportNewIncomingCallWithUUID:uuid
                                             update:callUpdate
                                         completion:^(NSError *err) { /* ... */ }];

       completion();
   }

The crucial PJSIP step is the ``REREGISTER`` schedule. Calling
``pjsua_acc_set_registration`` directly from the iOS handler would
violate PJSIP's threading rules (see below); the
``SCHEDULE_TIMER`` macro defers the call onto a registered PJ
thread.

Bridging iOS handlers to PJSIP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP requires that any thread calling its APIs be registered
with :cpp:any:`pj_thread_register`. UIKit / GCD threads are not
registered by default, and PJLIB will assert on the first call
made from one. Worse, simply registering the GCD thread on the
fly is unsafe — the ``pj_thread_desc`` storage has to outlive the
thread, and GCD's thread pool churns.

The :sourcedir:`ipjsua sample <pjsip-apps/src/pjsua/ios/ipjsua/ipjsuaAppDelegate.m>`
solves this by piggy-backing on PJSUA's own timer thread:

.. code-block:: objc

   #define SCHEDULE_TIMER(action) \
   { \
       REGISTER_THREAD \
       pjsua_schedule_timer2(pjsip_funcs, (void *)action, 0); \
   }

   static void pjsip_funcs(void *user_data)
   {
       /* Runs on PJSUA's timer thread (already registered). */
       long code = (long)user_data & 0xF;
       if (code == REREGISTER) {
           for (unsigned i = 0; i < pjsua_acc_get_count(); ++i) {
               if (pjsua_acc_is_valid(i))
                   pjsua_acc_set_registration(i, PJ_TRUE);
           }
       } else if (code == ANSWER_CALL) {
           pjsua_call_id call_id = (pjsua_call_id)((long)user_data & 0xFF0) >> 4;
           pjsua_call_answer(call_id, PJSIP_SC_OK, NULL, NULL);
       }
       /* ... END_CALL, ACTIVATE_AUDIO, DEACTIVATE_AUDIO, HANDLE_IP_CHANGE ... */
   }

Every CallKit / PushKit / orientation / reachability handler that
needs to touch PJSIP encodes its intent in a small integer
``action`` and dispatches via ``SCHEDULE_TIMER``. The integer
encoding uses the low 4 bits for the action and the upper bits
for parameters such as the call ID.

.. caution::

   The ``REGISTER_THREAD`` step inside ``SCHEDULE_TIMER`` registers
   the *caller* with PJLIB just long enough to invoke
   ``pjsua_schedule_timer2``. That registration is safe only when
   the caller runs on a long-lived thread whose
   ``pj_thread_desc`` storage outlives the call — most commonly
   the main thread, which is why the sample initialises
   ``PKPushRegistry`` and ``CXProvider`` with
   ``dispatch_get_main_queue()``. If a handler fires on a
   different queue (some Reachability hookups, custom GCD
   queues), hop to the main queue or another dedicated long-
   lived PJ-registered thread before calling ``SCHEDULE_TIMER``.
   Don't drop the registration step into a transient GCD worker.

For a more complex application, the sample's header comment
recommends creating a dedicated PJ-registered worker thread
instead of leaning on the timer thread.

PJSUA2 (C++) applications have a native equivalent:
:cpp:func:`pj::Endpoint::utilTimerSchedule` schedules a timer
with a millisecond delay and a ``Token`` user-data, and the
virtual :cpp:func:`pj::Endpoint::onTimer` callback fires on a
PJ-registered thread. The Obj-C / Swift handler hands off via:

.. code-block:: c++

   /* From a CallKit / PushKit handler thread: */
   Endpoint::instance().utilTimerSchedule(0, (Token)(uintptr_t)REREGISTER);

   /* In your Endpoint subclass: */
   void MyEndpoint::onTimer(const OnTimerParam &prm) override
   {
       long action = (long)(uintptr_t)prm.userData;
       if (action == REREGISTER) {
           for (unsigned i = 0; i < Endpoint::instance().accGetCount(); ++i) {
               /* ... acc->setRegistration(true) ... */
           }
       }
       /* ... ANSWER_CALL, END_CALL, ACTIVATE_AUDIO, ... */
   }


PJSIP-side configuration
------------------------

The earlier sections cover the API needed to drive the push
wake-up: :cpp:any:`pjsua_acc_config::reg_contact_uri_params` to
inject the RFC 8599 push token into REGISTER, and
:cpp:any:`pjsua_acc_set_registration` to refresh the registration
when a push arrives (called from the ``REREGISTER`` branch of the
bridging dispatcher above). The remaining PJSIP-side concerns —
background socket policy, audio session, and IP-change handling
— are configuration knobs that don't fit inside the push-handler
code path.

Background socket policy
~~~~~~~~~~~~~~~~~~~~~~~~

A few PJLIB / PJSIP compile-time settings shape what PJSIP's
TCP/TLS sockets do when the app is backgrounded:

- **``PJ_ACTIVESOCK_TCP_IPHONE_OS_BG``** (default ``0`` since
  :pr:`3253`) — when non-zero, PJLIB marks active TCP sockets
  with ``kCFStreamNetworkServiceTypeVoIP`` so iOS keeps the
  socket alive in the background. Setting this back to ``1`` is
  **strongly discouraged on iOS 16+** — Apple actively kills
  apps that use the VoIP socket service type. Leave at the
  default and rely on VoIP push instead.
- **``PJSIP_TCP_TRANSPORT_DONT_CREATE_LISTENER``** /
  **``PJSIP_TLS_TRANSPORT_DONT_CREATE_LISTENER``** (default ``0``)
  — when set to ``1``, PJSIP skips creating a listening socket
  for that transport. VoIP-push-driven apps don't accept inbound
  TCP/TLS connections (the SIP server reaches them via push, not
  by dialling them), so the listener is dead weight and one less
  surface for iOS background-policy quirks. When enabling either,
  set :cpp:any:`pjsua_acc_config::contact_use_src_port` to
  ``PJ_TRUE`` so the Contact URI advertises the outbound socket's
  source port — otherwise the Contact ends up with a host:port
  pair that nothing is listening on.
- **``PJSIP_TCP_KEEP_ALIVE_INTERVAL``** /
  **``PJSIP_TLS_KEEP_ALIVE_INTERVAL``** — interval at which
  PJSIP sends TCP/TLS keep-alive packets while the app is in
  the foreground. Less relevant for VoIP-push-driven apps
  (where the connection is short-lived around each
  registration / call) but still controls foreground heartbeat
  behaviour.

For exhaustive background-keepalive handling on legacy iOS
versions, see :ref:`ios_bg`.

Audio session lifecycle
~~~~~~~~~~~~~~~~~~~~~~~

Since :pr:`1941`, PJSIP's ``coreaudio_dev`` no longer manages
``AVAudioSession`` itself, on the assumption that a CallKit-
integrated app needs full control of session category / mode /
activation. The application is now responsible for:

- Setting category to ``AVAudioSessionCategoryPlayAndRecord``
  with mode ``AVAudioSessionModeVoiceChat`` before CallKit
  reports the incoming call.
- Activating the session at the right point in the CallKit
  lifecycle — typically inside CallKit's
  ``provider:didActivateAudioSession:`` callback, which fires
  after CallKit has had a chance to wire up the audio routing.
- Deactivating it once the call ends, with
  ``AVAudioSessionSetActiveOptionNotifyOthersOnDeactivation``.

When CallKit's audio session activates, PJSIP's existing sound
device may not start producing audio until the device is forced
to reopen. The sample handles this with a forced sound-device
cycle:

.. code-block:: c

   /* In the ACTIVATE_AUDIO branch of pjsip_funcs() */
   pjsua_set_no_snd_dev();
   pjsua_set_snd_dev(PJSUA_SND_DEFAULT_CAPTURE_DEV,
                     PJSUA_SND_DEFAULT_PLAYBACK_DEV);

   /* Reconnect each active call's media to the conference bridge. */
   for (unsigned i = 0; i < count; i++) {
       /* ... pjsua_conf_connect for each PJMEDIA_TYPE_AUDIO call ... */
   }

For deactivation, gate on :cpp:any:`pjsua_snd_is_active` so a
call whose audio is still flowing isn't interrupted:

.. code-block:: c

   if (!pjsua_snd_is_active()) {
       [[AVAudioSession sharedInstance]
           setActive:NO
         withOptions:AVAudioSessionSetActiveOptionNotifyOthersOnDeactivation
               error:nil];
   }

IP-change handling
~~~~~~~~~~~~~~~~~~

Mobile devices switch networks frequently (Wi-Fi ↔ cellular,
roaming Wi-Fi). When the bound interface changes, ongoing TCP
flows die and registrations need to be refreshed. PJSIP exposes
a single entry point for this:

.. code-block:: c

   pjsua_ip_change_param param;
   pjsua_ip_change_param_default(&param);
   pjsua_handle_ip_change(&param);

Internally, this shuts down the stale TCP/TLS transports
(``shutdown_transport``, default ``PJ_TRUE``), restarts the
transport listener if one was created
(``restart_listener``, default ``PJ_TRUE`` — a no-op when the
listener was disabled via ``PJSIP_*_TRANSPORT_DONT_CREATE_LISTENER``,
see `Background socket policy`_), and then re-registers every
active account. It is therefore a superset of plain
re-registration — calling it always REGISTERs, plus rebuilds
transport state.

Trigger from a Reachability observer in the app. The same
schedule-timer bridge applies — call from a PJ-registered thread.

PJSUA2 applications use :cpp:func:`pj::Endpoint::handleIpChange`
with :cpp:any:`pj::IpChangeParam`.


Server-side checklist
---------------------

PJSIP does not own the server side, but a working integration
requires the SIP server to:

1. **Hold or proxy inbound INVITEs** while the target device is
   off-network, and **re-deliver** when a fresh REGISTER arrives.
2. **Parse the** :rfc:`8599` **push parameters from the REGISTER
   Contact URI** (``pn-provider``, ``pn-param``, ``pn-prid``) and
   store the token-to-AOR mapping. Servers without RFC 8599
   support typically accept the token via a separate provisioning
   API instead.
3. **Send a VoIP push to APNs** when a held INVITE is ready to
   deliver.

For the iOS side, follow Apple's documentation rather than
restating it here:

- `Responding to VoIP Notifications from PushKit
  <https://developer.apple.com/documentation/pushkit/responding-to-voip-notifications-from-pushkit>`__
- `Optimizing VoIP Apps
  <https://developer.apple.com/library/ios/documentation/Performance/Conceptual/EnergyGuide-iOS/OptimizeVoIP.html>`__
- `AVAudioSession
  <https://developer.apple.com/reference/avfoundation/avaudiosession>`__
- `Local Network Privacy
  <https://developer.apple.com/forums/thread/663858>`__ — required
  for media traffic from the background; the
  :sourcedir:`ipjsua sample <pjsip-apps/src/pjsua/ios/ipjsua/ipjsuaAppDelegate.m>`
  notes the implementation is left to the application.


Common pitfalls
---------------

The most-recurring iOS-specific gotchas, in roughly the order
applications hit them. See :doc:`/get-started/ios/issues` for the
broader iOS troubleshooting list.

- **Calling PJSIP from a GCD thread.** Triggers
  ``"Calling pjlib from unknown/external thread..."`` assertions.
  Use the :cpp:any:`pjsua_schedule_timer2` bridge above; do not
  register GCD threads directly with :cpp:any:`pj_thread_register`
  — the ``pj_thread_desc`` storage has to outlive the thread, and
  GCD pools churn. See :pr:`1837`.
- **Assuming PJSIP manages ``AVAudioSession``.** Since :pr:`1941`
  it doesn't. The app must set category, mode, and
  activate / deactivate explicitly.
- **Audio interruption killing audio for the rest of the call.**
  On interruption begin, hold the calls and forcibly stop the
  sound device with :cpp:any:`pjsua_set_no_snd_dev`; on end,
  unhold and restart via :cpp:any:`pjsua_set_snd_dev`. See the
  audio-interruption section of :doc:`/get-started/ios/issues`.
- **Missing ``voip`` background mode.** ``Info.plist`` must
  include ``voip`` under ``UIBackgroundModes`` for PushKit to
  deliver pushes.
- **Local Network Privacy not requested.** Required from iOS 14
  for media traffic from the background; without it the first
  RTP packet to a private-network peer fails silently. Sample
  doesn't include the request code; see the Apple forum link
  above.
- **Microphone permission requested late.** Opening the audio
  device while in the background does not trigger the permission
  prompt — the sample requests microphone access up front in
  ``didFinishLaunchingWithOptions``:

  .. code-block:: objc

     [[AVAudioSession sharedInstance]
       requestRecordPermission:^(BOOL granted) { /* ... */ }];

- **Push handler completion called before CallKit reports the
  call.** iOS terminates the app if the push completion handler
  returns without a ``reportNewIncomingCallWithUUID`` — invoke
  CallKit synchronously inside the handler.


Sample reference
----------------

The full integration is in
:sourcedir:`pjsip-apps/src/pjsua/ios/ipjsua/ipjsuaAppDelegate.m`
(:pr:`3913`). Build it from the ``ipjsua.xcworkspace`` and inspect:

- ``didFinishLaunchingWithOptions`` — PushKit + CallKit setup.
- ``pushRegistry:didUpdatePushCredentials:`` — token forwarding.
- ``pushRegistry:didReceiveIncomingPushWithPayload:`` — re-REGISTER
  + audio session + CallKit report.
- ``provider:perform*Action:`` (CallKit) — answer / end via
  ``SCHEDULE_TIMER``.
- ``pjsip_funcs`` — the action dispatcher running on PJSUA's
  timer thread.

The Swift sample at
:sourcedir:`pjsip-apps/src/pjsua/ios-swift/ipjsua-swift` does
**not** currently include push integration; the Obj-C sample is
the canonical reference.


PJSUA2 equivalents
------------------

Most of the API surface used here is PJSUA-LIB; PJSUA2 wraps the
same calls.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:func:`pj::Account::setRegistration`
     - :cpp:any:`pjsua_acc_set_registration`
   * - :cpp:func:`pj::Endpoint::handleIpChange` /
       :cpp:any:`pj::IpChangeParam`
     - :cpp:any:`pjsua_handle_ip_change` /
       :cpp:any:`pjsua_ip_change_param`
   * - :cpp:func:`pj::AudDevManager::setNoDev`
     - :cpp:any:`pjsua_set_no_snd_dev`
   * - :cpp:func:`pj::AudDevManager::setPlaybackDev` +
       :cpp:func:`pj::AudDevManager::setCaptureDev`
     - :cpp:any:`pjsua_set_snd_dev`
   * - :cpp:func:`pj::Endpoint::utilTimerSchedule` /
       :cpp:func:`pj::Endpoint::onTimer` (the timer-thread bridge
       — see the bridging section above)
     - :cpp:any:`pjsua_schedule_timer2`

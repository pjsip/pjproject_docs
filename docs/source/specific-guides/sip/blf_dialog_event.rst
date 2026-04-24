Busy Lamp Field (BLF) and Dialog Event
========================================

.. contents:: Table of Contents
    :depth: 3

Available since 2.15 (:pr:`3754`). Compile-time toggle added in 2.17
(:pr:`4810`).


Overview
------------------

The **Dialog Event** package (:rfc:`4235`) lets one SIP user agent
subscribe to another's dialog state and receive notifications as calls
are placed, answered, or hung up. The classic application is **Busy
Lamp Field (BLF)** on an IP-PBX system or desk phone — a lamp beside a
coworker's name that lights up while they're on a call.

The spec defines two roles:

- **Subscriber** (BLF watcher) — sends a ``SUBSCRIBE`` for
  ``Event: dialog`` and processes the ``dialog-info+xml`` bodies in
  each ``NOTIFY``.
- **Notifier** (the watched endpoint, typically a PBX or the watched
  UA itself) — accepts subscriptions and sends ``NOTIFY`` requests
  whenever its dialog state changes.

PJSIP implements the **subscriber** role at all layers (pjsip-simple,
PJSUA-LIB, PJSUA2), which is the common use case for a softphone or
attendant console watching another user. The notifier role is not
currently provided by the library — see :ref:`blf_limitations` below.


Enabling the package
------------------------

Dialog event support is gated by a compile-time flag in
``pjsip_config.h``/``config_site.h``:

.. code-block:: c

   /* Default: 1 (enabled). Set to 0 to omit client subscription code,
    * for example if you provide your own dialog-event server. */
   #define PJSUA_HAS_DLG_EVENT_PKG  1

The flag itself was added in 2.17 (:pr:`4810`); prior releases always
had the subscription support compiled in. When enabled, the ``dialog``
event package is automatically registered with the SIP endpoint
during ``pjsua_init()``.

Each buddy can independently choose between presence and dialog event.
Set one of the flags on the buddy config:

- :cpp:any:`pjsua_buddy_config::subscribe` — presence (RFC 3856)
- :cpp:any:`pjsua_buddy_config::subscribe_dlg_event` — dialog event (RFC 4235)

.. note::

   A single buddy can have **only one** active subscription at a time.
   If both flags are set on the same buddy config, PJSUA-LIB picks
   presence and silently ignores ``subscribe_dlg_event``. To watch the
   same target for both presence and dialog state, add two buddies
   with the same URI, one flag each.


PJSUA-LIB API
------------------

Wire callbacks to the endpoint, add buddies with
``subscribe_dlg_event = PJ_TRUE``, and read the parsed dialog-info
state from the callback via :cpp:any:`pjsua_buddy_get_dlg_event_info()`:

.. code-block:: c

   /* Called every time a NOTIFY arrives with updated dialog state. */
   static void on_buddy_dlg_event_state(pjsua_buddy_id buddy_id)
   {
       pjsua_buddy_dlg_event_info info;
       pjsua_buddy_get_dlg_event_info(buddy_id, &info);

       PJ_LOG(3, ("blf",
                  "%.*s: state=%.*s call-id=%.*s direction=%.*s",
                  (int)info.uri.slen,                  info.uri.ptr,
                  (int)info.dialog_state.slen,         info.dialog_state.ptr,
                  (int)info.dialog_call_id.slen,       info.dialog_call_id.ptr,
                  (int)info.dialog_direction.slen,     info.dialog_direction.ptr));
   }

   /* Called when the subscription itself changes state (e.g. the
    * server accepted or terminated the subscription). */
   static void on_buddy_evsub_dlg_event_state(pjsua_buddy_id buddy_id,
                                              pjsip_evsub *sub,
                                              pjsip_event *event)
   {
       PJ_UNUSED_ARG(event);
       PJ_LOG(4, ("blf", "Buddy %d: subscription state: %s",
                  buddy_id, pjsip_evsub_get_state_name(sub)));
   }

   /* Registration */
   pjsua_config ua_cfg;
   pjsua_config_default(&ua_cfg);
   ua_cfg.cb.on_buddy_dlg_event_state       = &on_buddy_dlg_event_state;
   ua_cfg.cb.on_buddy_evsub_dlg_event_state = &on_buddy_evsub_dlg_event_state;
   pjsua_init(&ua_cfg, /*log_cfg*/ NULL, /*media_cfg*/ NULL);

   /* Add a buddy watched for dialog events (BLF target). */
   pjsua_buddy_config bcfg;
   pjsua_buddy_config_default(&bcfg);
   bcfg.uri                 = pj_str("sip:alice@example.com");
   bcfg.subscribe_dlg_event = PJ_TRUE;
   pjsua_buddy_id bid;
   pjsua_buddy_add(&bcfg, &bid);

The library refreshes the subscription periodically. To force an
immediate refresh (e.g. after the user presses a "refresh" button),
call :cpp:any:`pjsua_buddy_update_dlg_event()`.

**Fields on `pjsua_buddy_dlg_event_info`**

Beyond the URI and subscription state, the structure surfaces the
top-level ``dialog-info`` element (``dialog_info_state``,
``dialog_info_entity``) and the details of one ``<dialog>`` child:
``dialog_id``, ``dialog_state``, ``dialog_call_id``,
``dialog_local_tag``, ``dialog_remote_tag``, ``dialog_direction``,
``dialog_duration``, plus the parsed ``<local>`` and ``<remote>``
identities (``local_identity``, ``local_identity_display``,
``local_target_uri`` and their ``remote_*`` counterparts). This is
what the pjsua CLI prints in its default BLF handler
(:source:`pjsip-apps/src/pjsua/pjsua_app.c`).

See :ref:`blf_limitations` for what is not surfaced (e.g. a NOTIFY
containing multiple ``<dialog>`` elements).


PJSUA2 API
------------------

Subclass :cpp:any:`pj::Buddy`, override
:cpp:any:`pj::Buddy::onBuddyDlgEventState()` and
:cpp:any:`pj::Buddy::onBuddyEvSubDlgEventState()`, and set
``subscribe_dlg_event`` on the ``BuddyConfig``:

.. code-block:: c++

   class BlfBuddy : public pj::Buddy {
   public:
       void onBuddyDlgEventState() override
       {
           /* Caveat: PJSUA2 does not yet expose the dialog-event info
            * structure. Drop to the C API to read the current state. */
           pjsua_buddy_dlg_event_info info;
           if (pjsua_buddy_get_dlg_event_info(getId(), &info) == PJ_SUCCESS)
           {
               std::cout << std::string(info.uri.ptr, info.uri.slen)
                         << " state="
                         << std::string(info.dialog_state.ptr,
                                        info.dialog_state.slen)
                         << "\n";
           }
       }

       void onBuddyEvSubDlgEventState(
           pj::OnBuddyEvSubStateParam &prm) override
       {
           PJ_UNUSED_ARG(prm);
           // ... subscription state change (active/terminated/etc.)
       }
   };

   // Setup
   pj::BuddyConfig bcfg;
   bcfg.uri                 = "sip:alice@example.com";
   bcfg.subscribe_dlg_event = true;

   BlfBuddy *b = new BlfBuddy();
   b->create(*account, bcfg);

To force an immediate refresh, call ``b->updateDlgEvent()``.

.. warning::

   As of 2.17, PJSUA2 has **no** ``BuddyDlgEventInfo`` struct and no
   ``Buddy::getDlgEventInfo()`` accessor — the callback fires but the
   state must be read via the C API
   (:cpp:any:`pjsua_buddy_get_dlg_event_info()`) as shown. The
   presence side has the symmetric ``BuddyInfo`` + ``getInfo()``;
   parity is a :ref:`known gap <blf_limitations>`.


Low-level PJSIP-Simple API
----------------------------

Applications that want full control — raw XML access, custom
subscription lifetime, managing their own dialog — can use the
pjsip-simple layer directly:

- :cpp:any:`pjsip_dlg_event_create_uac()` — create a client
  subscription on an existing dialog
- :cpp:any:`pjsip_dlg_event_initiate()` — build a ``SUBSCRIBE`` (or
  refresh / unsubscribe with ``expires`` = 0)
- :cpp:any:`pjsip_dlg_event_terminate()` — tear down locally (use
  ``expires = 0`` with ``_initiate()`` for a graceful unsubscribe)
- :cpp:any:`pjsip_dlg_event_get_status()` — read the parsed
  :cpp:any:`pjsip_dlg_event_status` for the latest NOTIFY
- :cpp:any:`pjsip_dlg_event_parse_dialog_info()` and
  :cpp:any:`pjsip_dlg_event_parse_dialog_info2()` — standalone XML
  parsing helpers, useful if the app obtains the body through another
  channel

The parsed status structure exposes the same fields as the PJSUA-LIB
wrapper **plus** a ``dialog_node`` of type ``pj_xml_node *`` for the
``<dialog>`` element, so the application can walk the XML for any
elements not pre-parsed (custom BroadWorks extensions, additional
``<target>`` parameters, etc.).


Dialog-info XML
-----------------

A ``NOTIFY`` body for this package looks like:

.. code-block:: xml

   <?xml version="1.0"?>
   <dialog-info xmlns="urn:ietf:params:xml:ns:dialog-info"
                version="3" state="partial"
                entity="sip:alice@example.com">
     <dialog id="as7d900as8" call-id="f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
             local-tag="1928301774" direction="initiator">
       <state>confirmed</state>
       <duration>274</duration>
       <local>
         <identity display="Alice">sip:alice@example.com</identity>
         <target uri="sip:desk@192.0.2.4"/>
       </local>
       <remote>
         <identity display="Bob">sip:bob@example.net</identity>
         <target uri="sip:bob@192.0.2.99"/>
       </remote>
     </dialog>
   </dialog-info>

The outer ``<dialog-info state="...">`` is captured as
``dialog_info_state`` (``full``, ``partial``) and the ``entity`` as
``dialog_info_entity``. The inner ``<dialog state="...">`` — the
actual call state — is captured as ``dialog_state``; RFC 4235
defines the states ``trying``, ``proceeding``, ``early``,
``confirmed``, and ``terminated``.


.. _blf_limitations:

Known limitations
--------------------

- **Notifier / server role.** PJSIP does not currently auto-generate
  ``dialog-info+xml`` bodies from the user's own dialogs or push
  ``NOTIFY`` requests when they change; there is no
  ``pjsip_dlg_event_create_uas()``. An application acting as a
  dialog-event source would have to construct the XML itself and use
  raw :cpp:any:`pjsip_evsub_create_uas()` / ``_notify()``.
- **PJSUA2 info getter is missing.** See the warning under the PJSUA2
  section — use the C API in the meantime.
- **Single-``<dialog>`` cap in the PJSUA-LIB struct.** The
  ``pjsua_buddy_dlg_event_info`` structure holds exactly one dialog
  (``PJSIP_DLG_EVENT_STATUS_MAX_INFO = 1``). RFC 4235 allows a watched
  party with several concurrent dialogs to report them all in one
  ``NOTIFY``; if that happens, only the first is visible via the
  PJSUA-LIB struct. At the pjsip-simple layer the full XML is
  reachable via ``dialog_node``.
- **One subscription slot per buddy.** A buddy carries a single
  subscription that is either presence **or** dialog event, never
  both. Which kind is active is "first-wins":

  - At ``pjsua_buddy_add()`` time, if both ``subscribe`` and
    ``subscribe_dlg_event`` are ``PJ_TRUE`` on the config, presence
    is chosen and the dialog-event flag is silently dropped.
  - Calls to :cpp:any:`pjsua_buddy_subscribe_pres()` or
    :cpp:any:`pjsua_buddy_subscribe_dlg_event()` while another
    subscription of either kind is already active are silent
    no-ops. To switch kinds, unsubscribe first, then subscribe with
    the other type.

  Model each feed as its own buddy when you genuinely need both
  presence *and* dialog-event for the same URI.


References
-----------

- :rfc:`4235` — An INVITE-Initiated Dialog Event Package for the SIP
- :rfc:`3856` — A Presence Event Package for SIP (for contrast)
- :pr:`3754` — Initial client subscription + BLF (2.15)
- :pr:`4214` — Parsing fix (2.16)
- :pr:`4810` — Compile-time toggle (2.17)
- Sample implementation:
  :source:`pjsip-apps/src/pjsua/pjsua_app.c` — see
  ``on_buddy_dlg_event_state`` and ``on_buddy_evsub_dlg_event_state``
  callbacks. The legacy menu UI (non-CLI) has a ``D`` / ``Du``
  toggle to subscribe / unsubscribe a buddy's dialog event
  (:source:`pjsip-apps/src/pjsua/pjsua_app_legacy.c`); the newer
  libcli-based UI (:source:`pjsip-apps/src/pjsua/pjsua_app_cli.c`)
  does not yet expose an equivalent command.

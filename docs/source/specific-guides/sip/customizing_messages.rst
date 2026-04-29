.. _guide_customizing_messages:

Customizing SIP Messages
=========================

.. contents:: Table of Contents
    :depth: 2

PJSIP generates the headers and body of outgoing SIP messages
automatically from the account configuration and dialog state.
This guide covers four ways to customize what gets sent, from
simplest to most flexible:

- **Account-level fields**, for values that apply to every message
  sent on behalf of an account: default From URI, default Contact,
  semicolon-separated parameters appended to every Contact,
  extra headers on REGISTER / SUBSCRIBE.
- **Per-message field overrides on the outgoing API call.** For
  per-call values (From URI, Contact URI, Call-ID) and the broader
  fields exposed by ``SipTxOption`` / ``pjsua_msg_data`` (target
  URI, body, multipart, custom headers), set the field on the
  parameter struct you pass to the API.
- **The** ``onCallSdpCreated`` **callback for locally generated
  SDP.** Fires every time PJSIP creates an SDP for the call —
  initial offer, answer, re-INVITE / UPDATE on either side.
  Receive the just-created SDP and mutate it in place before
  PJSIP sends it — for codec ordering, custom attributes, QoS /
  bandwidth lines.
- **A PJSIP module — a hook registered into PJSIP's message
  processing pipeline.** Modules are how PJSIP itself implements
  its transport, transaction, UA, and dialog layers; applications
  can register their own to intercept any message type (REGISTER
  / SUBSCRIBE / MESSAGE / OPTIONS / PUBLISH / INVITE / …) in
  either direction and patch headers or bodies arbitrarily.

Pick the simplest level that reaches what you need. The first
three cover the vast majority of cases; the module path is the
catch-all for everything the field- and callback-level options
can't touch.


.. _account-level-customization:

Account-level customization
---------------------------

Some customization happens once at account setup and then applies
to every outgoing message sent on behalf of that account, instead
of being re-passed per call. Configure these on
:cpp:any:`pj::AccountConfig` (``pjsua_acc_config`` for PJSUA-LIB):

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Effect
   * - ``idUri``
     - The default From URI for every outgoing message from this
       account. Per-message ``localUri`` overrides supersede it for
       a single call.
   * - ``sipConfig.contactForced``
     - Pin a Contact URI for every outgoing message from this
       account, instead of letting PJSIP auto-generate from the
       transport. Useful when the auto-generated Contact is wrong
       (e.g. behind a reverse proxy / odd NAT layout PJSIP can't
       infer).
   * - ``sipConfig.contactParams`` / ``contactUriParams``
     - Semicolon-separated parameters appended to every Contact
       header / Contact URI from this account — useful for
       ``;+sip.instance="<urn:uuid:...>"`` (RFC 5626), GRUU markers,
       custom device identifiers.
   * - ``regConfig.headers``
     - Custom SIP headers added to REGISTER requests only.
   * - ``regConfig.contactParams`` /
       ``regConfig.contactUriParams``
     - Same idea as the ``sipConfig`` variants, but appended only on
       the Contact of REGISTER requests.
   * - ``presConfig.headers``
     - Custom SIP headers added to outgoing presence SUBSCRIBE
       requests only.

These take effect when you create or modify the account; the per-
message paths below take precedence when both are set.


Customizing outgoing calls (From / Contact / Call-ID)
-----------------------------------------------------

Three common per-call fields can be overridden directly on the
``CallOpParam`` you pass to :cpp:func:`pj::Call::makeCall()`:

- **From** — override the account ID for this call's From header.
  Useful for multi-tenant systems, alias identities, B2BUA leg
  rewrites, caller-ID spoofing for legitimate use cases (CRM-driven
  outbound, click-to-call).
- **Contact** — override the auto-generated Contact. Useful for
  sending the call out one transport / NIC but advertising a
  different return path, hairpinning through a reverse proxy, etc.
- **Call-ID** — supply a predictable Call-ID instead of PJSIP's
  auto-generated unique value. Useful for correlating a
  PJSIP-originated call with an external system (CTI, dispatcher,
  SBC), or for testing.

Each is a separate field with its own scope, set independently on
``CallSetting`` or the call's ``SipTxOption``.

For the broader ``SipTxOption`` fields shared with other outgoing
APIs (target URI, body, multipart, custom headers) see
:ref:`other-siptxoption` below. To modify the SDP itself, see
:ref:`modifying-sdp-callback`.

Overriding the From URI
~~~~~~~~~~~~~~~~~~~~~~~

Set :cpp:any:`pj::SipTxOption::localUri` on the
``CallOpParam::txOption`` you pass to
:cpp:func:`pj::Call::makeCall()`:

.. code-block:: c++

   try {
       CallOpParam prm(true);
       prm.txOption.localUri = "sip:reception@example.com";
       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

Empty string falls back to the account's :cpp:any:`pj::AccountConfig::idUri`
(the default behaviour). The value is passed to ``pjsip_dlg_create_uac``
as the dialog's local URI, so it persists for the lifetime of the
dialog — every locally originated in-dialog request (re-INVITE,
BYE, etc.) uses the overridden From.

Available since PJSIP 2.14 (:pr:`3320`).


Overriding the Contact URI
~~~~~~~~~~~~~~~~~~~~~~~~~~

Set :cpp:any:`pj::SipTxOption::contactUri` on
``CallOpParam::txOption``:

.. code-block:: c++

   try {
       CallOpParam prm(true);
       prm.txOption.contactUri =
           "sip:agent@public.example.com:5061;transport=tls";
       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

Empty string falls back to the auto-generated contact (account
config + selected transport). Contact selection priority:

1. ``contactUri`` if provided and valid.
2. The account's stored Contact — either ``contactForced``
   (account-level override, see :ref:`above
   <account-level-customization>`) if set, otherwise the Contact
   advertised by the most recent successful REGISTER.
3. Auto-generated contact via PJSIP's transport selection.

Like the From override, the chosen Contact is passed to
``pjsip_dlg_create_uac`` and stored as the dialog's local Contact,
so it persists for the dialog's lifetime — used for every locally
originated in-dialog request. The override field itself is only
accepted on the initial ``makeCall``; you can't change it later via
``reinvite`` / ``update``.

Available since PJSIP 2.16 (:pr:`4647`).


Custom Call-ID
~~~~~~~~~~~~~~

Unlike From and Contact, Call-ID is a *dialog* identifier, not a
message header you can change per-message. Set it on
:cpp:any:`pj::CallSetting::customCallId` before issuing the
outgoing call:

.. code-block:: c++

   try {
       CallOpParam prm(true);
       prm.opt.customCallId = "campaign-2026-04-29-87654321@dispatcher";
       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

Empty string falls back to PJSIP's auto-generated unique Call-ID.
Note that **the application is responsible for uniqueness** — PJSIP
does no verification, and reusing a Call-ID across simultaneous
calls will cause dialog matching to break.

Available since PJSIP 2.15 (:pr:`4052`).


.. _other-siptxoption:

Other SipTxOption / pjsua_msg_data fields
-----------------------------------------

The ``localUri`` and ``contactUri`` shown above are two members of
the broader :cpp:any:`pj::SipTxOption` (PJSUA2) /
:cpp:any:`pjsua_msg_data` (PJSUA-LIB) struct that most outgoing-
message APIs accept. The remaining fields cover request-line and
body customization on the same channel — without a module:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field (PJSUA2)
     - Effect
   * - ``targetUri``
     - Override the request's target URI (the Request-URI). If empty,
       defaults to the remote URI (To header).
   * - ``localUri``
     - Override From URI (calls / IM only). See the call section above.
   * - ``contactUri``
     - Override Contact URI (calls only). See the call section above.
   * - ``headers``
     - Additional SIP headers to append to the message. See
       :ref:`guide_adding_custom_header` below for usage.
   * - ``contentType`` / ``msgBody``
     - Set a single message body. Only honoured when the message
       doesn't already carry one.
   * - ``multipartContentType`` / ``multipartParts``
     - Send a ``multipart/*`` body. If the message already has a body,
       it gets folded into the multipart envelope as one of the parts.

Which APIs accept the option varies per field. For example
``targetUri`` is honoured by :cpp:func:`pj::Call::makeCall`,
:cpp:func:`pj::Call::reinvite`, :cpp:func:`pj::Call::update`,
:cpp:func:`pj::Call::setHold`, and :cpp:func:`pj::Buddy::sendInstantMessage`;
``localUri`` and ``contactUri`` are call-and-IM specific. Check the
field documentation in :file:`pjsua.h` for the exact list per field.

**Example — outgoing INVITE whose Request-URI points to a specific
gateway while the To header still names the peer:**

.. code-block:: c++

   try {
       CallOpParam prm(true);
       prm.txOption.targetUri = "sip:gateway-east.example.com";
       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

The Request-URI is what intermediaries use to route the request;
the To header identifies the logical recipient.

.. note::

   ``msgBody`` is honoured **only when the message doesn't already
   carry a body** — so it does not replace the auto-generated SDP on
   INVITE / re-INVITE / 200 OK. Use ``msgBody`` for request types
   that PJSIP doesn't auto-populate a body for (e.g. SIP MESSAGE
   via :cpp:func:`pj::Buddy::sendInstantMessage`, OPTIONS).
   To attach a custom payload alongside an auto-generated SDP on
   an INVITE, use ``multipartContentType`` /
   ``multipartParts`` — PJSIP folds the existing body into the
   multipart envelope as one of the parts.


.. _guide_adding_custom_header:

Adding custom headers
~~~~~~~~~~~~~~~~~~~~~

Use the ``headers`` field to append arbitrary SIP headers to the
outgoing message — common use cases include vendor / proprietary
``X-...`` headers, ``P-Asserted-Identity``, ``P-Preferred-Identity``,
``Diversion``, and other private extensions PJSIP doesn't model
natively.

In PJSUA2, build a :cpp:any:`pj::SipHeader` for each header and
push it into ``txOption.headers``:

.. code-block:: c++

   try {
       CallOpParam prm(true);

       SipHeader h;
       h.hName = "X-Customer-Id";
       h.hValue = "42";
       prm.txOption.headers.push_back(h);

       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

In PJSUA-LIB, build each header as a ``pjsip_generic_string_hdr``
and link it into ``msg_data.hdr_list``:

.. code-block:: c

   pjsua_msg_data msg_data;
   pjsip_generic_string_hdr my_hdr;
   pj_str_t hname = pj_str("X-Customer-Id");
   pj_str_t hvalue = pj_str("42");

   pjsua_msg_data_init(&msg_data);
   pjsip_generic_string_hdr_init2(&my_hdr, &hname, &hvalue);
   pj_list_push_back(&msg_data.hdr_list, &my_hdr);

   /* Pass msg_data to the outgoing API, e.g. pjsua_im_send(): */
   pjsua_im_send(.., &msg_data, NULL);


.. _modifying-sdp-callback:

Modifying locally generated SDP
-------------------------------

For SDP-specific edits — adjusting codec ordering on a per-call
basis, injecting custom ``a=`` attributes, applying QoS / bandwidth
lines — use the dedicated callback rather than a module. The
callback fires every time PJSIP creates an SDP for the call:
initial offer, answer to an incoming offer, and any subsequent
re-INVITE / UPDATE generated by either side.
Override :cpp:func:`pj::Call::onCallSdpCreated`:

.. code-block:: c++

   void MyCall::onCallSdpCreated(OnCallSdpCreatedParam &prm) override
   {
       // prm.sdp    — the just-created local SDP
       // prm.remSdp — remote SDP if we're answering, empty if offering
       //
       // Modify prm.sdp.wholeSdp (an std::string) in place.
       // PJSUA2 re-parses it before sending.
   }

``remSdp`` distinguishes offerer from answerer roles (empty = local
is offering, populated = local is answering an incoming offer).

In PJSUA2 the application mutates the ``wholeSdp`` string on the
``SdpSession`` member; PJSUA2 re-parses it after the callback returns
and replaces the underlying ``pjmedia_sdp_session`` if the string
changed. PJSUA-LIB applications get a ``pjmedia_sdp_session *`` and
a pool argument and edit the parsed structure directly via
``pjmedia_sdp_*`` helpers.

This is cleaner than hooking ``on_tx_request`` in a module just to
rewrite outgoing SDP: the callback runs before serialization, gets
both local and remote SDPs in their parsed form, and avoids having
to identify INVITE / 200 OK by message inspection. Use the module
path only when you need to touch SDP on messages PJSUA doesn't
generate, or to rewrite SDP on *incoming* messages before PJSUA
parses them.


Patching messages with a PJSIP module
--------------------------------------

The customization options above cover specific outgoing fields. For
anything else — patching headers PJSIP would otherwise consume
verbatim, rewriting SDP (e.g. IPv4 ↔ IPv6 mapping, codec preference
juggling), normalising non-compliant remote messages, logging /
tracing every request and response, or implementing custom proxy
logic — the mechanism is the **PJSIP module**, registered on the
endpoint via :cpp:any:`pjsip_endpt_register_module()`.

A module is a :cpp:any:`pjsip_module` struct (``pjsip/sip_module.h``)
that hooks into the message processing chain. PJSIP itself implements
its core layers (transport, transaction, UA, dialog) as built-in
modules, so applications extending the chain are using exactly the
same machinery the library uses internally.

.. note::

   The module API is **C / C++ only**. ``pjsip_module`` is a C struct
   with C function pointers and is not exposed by the SWIG-based
   bindings (Java, Python, C#, Objective-C, …). Applications in
   those languages need to implement the module in C, build it into
   the native library, and add a SWIG wrapper to expose any
   registration / configuration entry point they want to call from
   the host language. The other three customization paths (account-
   level fields, per-message ``SipTxOption`` fields, and
   ``onCallSdpCreated``) are all available through the regular
   bindings.

Hook points
~~~~~~~~~~~

A module supplies any subset of these function pointers; ``NULL``
slots are simply skipped:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Hook
     - Fired when…
   * - ``on_rx_request``
     - An incoming SIP request arrives. Return ``PJ_TRUE`` to
       consume (stop dispatch), ``PJ_FALSE`` to let later modules
       continue.
   * - ``on_rx_response``
     - An incoming SIP response arrives. Same return semantics as
       ``on_rx_request``.
   * - ``on_tx_request``
     - An outgoing request is about to be sent on the wire. Return
       ``PJ_SUCCESS`` to proceed; any other ``pj_status_t`` (i.e.
       an error code) blocks the send.
   * - ``on_tx_response``
     - An outgoing response is about to be sent. Same semantics as
       ``on_tx_request``.
   * - ``on_tsx_state``
     - A transaction the module is the user of has changed state
       (calling, completed, terminated). Useful for transaction-
       level observers.

Plus lifecycle hooks ``load`` / ``start`` / ``stop`` / ``unload`` for
modules that need them.

In ``rx`` and ``tx`` handlers the application can mutate the message
in place — the rdata / tdata pool is available for any allocations.

Priority and ordering
~~~~~~~~~~~~~~~~~~~~~

The order in which modules see each message is governed by the
``priority`` field — note this is a numeric ranking, **not** a
"high priority = important" semantic. The smaller the number, the
closer to the transport layer; the larger the number, the closer
to the application. Order of dispatch depends on direction:

- **Incoming** (``on_rx_*``) — modules are called in **ascending**
  priority value (smallest number first). This matches the
  protocol stack going up: transport (8) → transaction (16) → UA
  (32) → dialog (48) → application (64).
- **Outgoing** (``on_tx_*``) — modules are called in **descending**
  priority value (largest number first). This matches the stack
  going down: application (64) → dialog (48) → UA (32) →
  transaction (16) → transport (8).

So a given priority value places your hook at the same spot in
the stack regardless of direction; only the call order along the
chain reverses. PJSIP defines five guideline values in
:cpp:any:`pjsip_module_priority`:

- ``PJSIP_MOD_PRIORITY_TRANSPORT_LAYER`` (8) — used by transport
  modules.
- ``PJSIP_MOD_PRIORITY_TSX_LAYER`` (16) — used by the transaction
  layer.
- ``PJSIP_MOD_PRIORITY_UA_PROXY_LAYER`` (32) — UA / proxy layer.
- ``PJSIP_MOD_PRIORITY_DIALOG_USAGE`` (48) — dialog usages.
- ``PJSIP_MOD_PRIORITY_APPLICATION`` (64) — recommended for
  applications that don't need to preempt anything.

Pick a priority that places your hook where you need it. To patch
**incoming responses before the dialog layer freezes state from
them**, use ``PJSIP_MOD_PRIORITY_TSX_LAYER + 1`` — after the
transaction layer has matched the response to its transaction, but
before any UA / dialog code reads the message. To **observe but
not interfere**, sit at ``APPLICATION`` priority — or use
``PJSIP_MOD_PRIORITY_TRANSPORT_LAYER - 1`` to sit closest to the
wire in either direction (first to see incoming messages, last to
see outgoing ones before they're serialized), the canonical
message-logger spot used by the samples below. To **block** a
class of message from reaching dialogs, return ``PJ_TRUE`` from
an ``on_rx_*`` hook at a priority value lower than the layer you
want to shield (e.g. anything below ``DIALOG_USAGE`` (48) to stop
a message before the dialog layer sees it).

Common use cases
~~~~~~~~~~~~~~~~

- **Header patching for interop** — fill in / strip / rewrite
  headers from non-compliant peers before the dialog layer reads
  them. The Contact-transport-parameter case below is one example;
  the same pattern handles Route / Record-Route quirks, custom
  P-headers, and so on.
- **SDP rewriting** — inspect and modify the SDP body in INVITE /
  re-INVITE / 200 OK. Common scenarios: NAT-aware address mapping
  (rewrite ``c=`` lines from internal IPv4 to public IPv6 or vice
  versa), forcing a specific codec ordering, stripping unsupported
  attributes, injecting bandwidth or QoS parameters.
- **Logging / tracing** — attach a module with a small priority
  value (close to transport) that hooks all four ``rx``/``tx``
  callbacks and dumps the message. PJSUA-LIB ships its own
  ``mod-pjsua-log`` (struct ``pjsua_msg_logger`` in
  ``pjsua_core.c``) registered at ``TRANSPORT_LAYER - 1``; a
  custom one lets you filter or redirect.
- **Custom proxy or B2BUA** — at higher priority than the UA layer,
  consume requests with ``PJ_TRUE`` and forward them yourself.

Sample implementations
~~~~~~~~~~~~~~~~~~~~~~

Working modules in the source tree, ordered by complexity:

- :sourcedir:`pjsip-apps/src/samples/sipecho.c` — minimal incoming-
  request handler; demonstrates the bare ``on_rx_request`` pattern at
  ``PJSIP_MOD_PRIORITY_APPLICATION``.
- :sourcedir:`pjsip-apps/src/samples/sipstateless.c` — bidirectional
  message logger plus a stateless UA. Shows the both-directions
  pattern (``on_rx_*`` + ``on_tx_*``) at the canonical
  ``TRANSPORT_LAYER - 1`` logger priority.
- :sourcedir:`pjsip/src/pjsua-lib/pjsua_core.c` — PJSUA-LIB's own
  built-in ``pjsua_msg_logger`` module (``mod-pjsua-log``). Same
  priority and shape as the ``sipstateless.c`` logger; this is the
  module behind the ``Request msg INVITE/cseq/...`` traces every
  PJSUA-based application emits, and a useful real-world reference.
- :sourcedir:`pjsip-apps/src/samples/proxy.h` — drop-in proxy module
  with full request / response / transaction-state handling,
  including how to consume requests and forward them.
- :sourcedir:`pjsip-apps/src/samples/invtester.c` — transaction-state
  observer using ``on_tsx_state`` for INVITE flow tracking.
- `mod_contact_tp_compat.c <../../_static/mod_contact_tp_compat.c>`__
  (linked from this guide; see the worked example below) — a header-
  patching module sitting at ``TSX_LAYER + 1`` so the patch lands
  before the dialog layer freezes the remote target.

The PJSIP Developer's Guide has a deeper treatment of the module
architecture (`Module chapter
<../../_static/PJSIP-Dev-Guide.pdf#page=15>`__) and the
authoritative API reference is
:doc:`Modules </api/generated/pjsip/group/group__PJSIP__MOD>`.

Worked example — non-compliant remote Contact transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A concrete interop pain: some PBXes and B2BUAs send a Contact in
2xx responses that doesn't match the transport the response
arrived on. Two flavours:

- **Missing transport parameter** — Contact lacks
  ``;transport=tcp`` even though the dialog was established over
  TCP. Per :rfc:`3263` the URI resolves to UDP for subsequent
  in-dialog requests (re-INVITE, re-SUBSCRIBE).
- **Mismatched transport parameter** — Contact has an explicit
  ``;transport=udp`` even though the dialog is over TCP (typical
  when a B2BUA rewrites the Contact from its outbound leg). Same
  resolution outcome on PRACK or in-dialog requests.

The failure mode depends on local UDP transport state:

- **No UDP transport configured** — outgoing request fails locally
  with ``PJSIP_ETPNOTSUITABLE`` because PJSIP can't find a matching
  transport for the resolved URI.
- **UDP transport configured** — request goes out over UDP, but the
  peer was only listening on TCP, so the message silently never
  reaches it.

Both are remote-side bugs; PJSIP's behaviour follows :rfc:`3261`
§12.1.2 and :rfc:`3263` correctly and won't be changed in the
library. A drop-in workaround module is available:
`mod_contact_tp_compat.c <../../_static/mod_contact_tp_compat.c>`__
— self-contained C with full doxygen. It hooks ``on_rx_response``
at ``PJSIP_MOD_PRIORITY_TSX_LAYER + 1`` and patches the Contact
URI's transport parameter before the dialog layer freezes the
remote target. Two modes:

- ``MOD_CONTACT_TP_COMPAT_ADD_ONLY`` (default, safer) — only adds
  ``;transport=`` when the Contact URI has none.
- ``MOD_CONTACT_TP_COMPAT_OVERRIDE`` (more aggressive) — also
  replaces an explicit-but-mismatched ``;transport=...``.

.. code-block:: c

   #include "mod_contact_tp_compat.c"

   /* After pjsua_init(), before pjsua_start(): */
   mod_contact_tp_compat_init(pjsua_get_pjsip_endpt(),
                              MOD_CONTACT_TP_COMPAT_ADD_ONLY);

PJSUA2 (C++) applications can include and call the module the same
way under an ``extern "C"`` block — see the file's header comment.
The module is also a useful template for any other header-patching
workaround in the same vein: replace the ``on_rx_response`` body,
keep the priority and registration plumbing.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - PJSUA2
     - PJSUA-LIB
   * - ``AccountConfig::idUri``
     - :cpp:any:`pjsua_acc_config::id`
   * - ``AccountConfig::sipConfig::contactForced``
     - :cpp:any:`pjsua_acc_config::force_contact`
   * - ``AccountConfig::sipConfig::contactParams`` / ``contactUriParams``
     - :cpp:any:`pjsua_acc_config::contact_params` / ``contact_uri_params``
   * - ``AccountConfig::regConfig::headers``
     - :cpp:any:`pjsua_acc_config::reg_hdr_list`
   * - ``AccountConfig::regConfig::contactParams`` / ``contactUriParams``
     - :cpp:any:`pjsua_acc_config::reg_contact_params` /
       ``reg_contact_uri_params``
   * - ``AccountConfig::presConfig::headers``
     - :cpp:any:`pjsua_acc_config::sub_hdr_list`
   * - ``CallOpParam::txOption.localUri``
     - :cpp:any:`pjsua_msg_data::local_uri` passed via the ``msg_data``
       argument to :cpp:any:`pjsua_call_make_call`
   * - ``CallOpParam::txOption.contactUri``
     - :cpp:any:`pjsua_msg_data::contact_uri`
   * - ``CallOpParam::txOption.targetUri``
     - :cpp:any:`pjsua_msg_data::target_uri`
   * - ``CallOpParam::txOption.headers``
     - :cpp:any:`pjsua_msg_data::hdr_list`
   * - ``CallOpParam::txOption.contentType`` / ``msgBody``
     - :cpp:any:`pjsua_msg_data::content_type` / ``msg_body``
   * - ``CallOpParam::txOption.multipartContentType`` / ``multipartParts``
     - :cpp:any:`pjsua_msg_data::multipart_ctype` / ``multipart_parts``
   * - ``CallOpParam::opt.customCallId``
     - :cpp:any:`pjsua_call_setting::custom_call_id`
   * - ``Call::onCallSdpCreated``
     - :cpp:any:`pjsua_callback::on_call_sdp_created`
   * - (workaround module is C only) — include
       ``mod_contact_tp_compat.c`` under ``extern "C"``
     - (same)

.. _guide_trickle_ice:

Using Trickle ICE
====================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

ICE establishes a media path by gathering local candidates (host,
STUN-derived server-reflexive, TURN-derived relayed) and probing them
pairwise against the peer's candidates. In the classic model
(:rfc:`8445`) each side must finish gathering before signalling
begins, so the call setup blocks for the slowest STUN/TURN response.

Trickle ICE (:rfc:`8838`) lets candidates be conveyed as soon as they
appear and connectivity checks start in parallel. The first
"initial offer" carries whatever is already known (typically just the
host candidates) and later candidates are trickled to the peer via
out-of-band signalling. In SIP that vehicle is SIP INFO messages with
``application/trickle-ice-sdpfrag`` payloads, per :rfc:`8840`.

The win is measurable for calls that include a relayed (TURN)
candidate, where the allocation handshake otherwise dominates setup
latency — call ringing can start before TURN has finished allocating.

For non-trickled ICE setup latency, see :doc:`standalone_ice` (the
*Negotiation time* section).


Half trickle vs full trickle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trickle ICE has two operating modes, defined in
:cpp:any:`pj_ice_sess_trickle`:

:cpp:any:`PJ_ICE_SESS_TRICKLE_HALF`
   Interoperable mode for when peer support is unknown at session
   start. As initiator, all local candidates are gathered before
   sending the initial offer (i.e. behaves like regular ICE on the
   wire) but the offer advertises trickle support so the answerer may
   trickle its side. As answerer, the agent trickles only when the
   offer indicates trickle support; otherwise it falls back to regular
   ICE.

:cpp:any:`PJ_ICE_SESS_TRICKLE_FULL`
   Use only when peer trickle support is known in advance. The
   initiator sends an offer with whatever candidates are gathered so
   far (commonly just host) and trickles the rest. PJSIP does not
   probe peer capability — discovering it is the application's
   responsibility.

When in doubt, use **half**. Both modes still satisfy the regular ICE
state machine.


Aggressive nomination is disabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trickle ICE and aggressive nomination are mutually exclusive
(:cpp:any:`pj_ice_sess_options::aggressive` doxygen). Enabling
``trickle`` automatically disables aggressive nomination —
regular (controlled) nomination is used instead. The pjsua CLI does
this for you when ``--ice-trickle`` is set; for PJSUA / PJSUA2
applications setting ``iceTrickle`` is sufficient and no extra step
is required.


Enabling Trickle ICE
--------------------

ICE itself must already be enabled — trickle is a mode of ICE, not a
standalone feature. The relevant switch lives on the account NAT
configuration.

PJSUA2
~~~~~~

Set :cpp:any:`pj::AccountNatConfig::iceTrickle` on the account
configuration before the account is created or modified:

.. code-block:: c++

   AccountConfig acfg;
   // ... existing config (id, server, credentials, etc.) ...
   acfg.natConfig.iceEnabled  = true;
   acfg.natConfig.iceTrickle  = PJ_ICE_SESS_TRICKLE_HALF;

   try {
       account.create(acfg);   // or account.modify(acfg);
   } catch(Error& err) {
   }

The field defaults to :cpp:any:`PJ_ICE_SESS_TRICKLE_DISABLED`.

PJSUA-LIB
~~~~~~~~~

Trickle can be configured globally (default for all accounts) or
overridden per account.

Globally — set the ``trickle`` field of
:cpp:any:`pjsua_media_config::ice_opt` (an instance of
:cpp:any:`pj_ice_sess_options`) on the media configuration passed
to :cpp:any:`pjsua_init()`:

.. code-block:: c

    pjsua_media_config med_cfg;
    pjsua_media_config_default(&med_cfg);
    med_cfg.enable_ice   = PJ_TRUE;
    med_cfg.ice_opt.trickle = PJ_ICE_SESS_TRICKLE_HALF;

    pjsua_init(NULL, NULL, &med_cfg);

Per account — opt out of the global ICE config and set the field
explicitly:

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);
    // ... id, registration URI, credentials, etc. ...
    acc_cfg.ice_cfg_use = PJSUA_ICE_CONFIG_USE_CUSTOM;
    acc_cfg.ice_cfg.enable_ice         = PJ_TRUE;
    acc_cfg.ice_cfg.ice_opt.trickle    = PJ_ICE_SESS_TRICKLE_FULL;

pjsua CLI
~~~~~~~~~

Add ``--ice-trickle=N`` where ``N`` is ``0`` (disabled), ``1`` (half),
or ``2`` (full):

.. code-block:: shell

    $ ./pjsua --use-ice --ice-trickle=1 \
              --stun-srv stun.example.org \
              --turn-srv turn.example.org \
              --turn-user [user] --turn-passwd ***

Aggressive nomination is automatically disabled when
``--ice-trickle`` is non-zero.


How candidates are conveyed
---------------------------

The initial offer
~~~~~~~~~~~~~~~~~

When trickle is enabled, the SDP carried in the initial offer/answer
contains:

- ``a=ice-options:trickle`` — signals trickle support to the peer
- ``a=ice-ufrag:`` / ``a=ice-pwd:`` — credentials
- whatever ``a=candidate:`` lines are already gathered (in full
  trickle mode this is often only the host candidates)
- ``a=end-of-candidates`` — present only when local gathering has
  already finished (half trickle initiator)
- ``a=mid:`` — media identifier; required by :rfc:`8840` because
  SDP fragments carried later in SIP INFO need to be associated
  with a specific m-line

PJSIP also adds ``trickle-ice`` to the ``Supported`` SIP header
(see :sourcedir:`pjsip/src/pjsua-lib/pjsua_call.c` — the
``str_trickle_ice`` literal).

Subsequent candidates: SIP INFO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Late-arriving candidates (STUN srflx after the STUN response, TURN
relay after the allocation completes) are encoded as an SDP fragment
and sent in a SIP INFO message:

.. code-block:: text

   INFO sip:peer@example.com SIP/2.0
   Content-Type: application/trickle-ice-sdpfrag
   ...
   <SDP fragment with new candidates, mid, ufrag, pwd>

The fragment contains only the candidates added since the last
conveyance (tracked internally via
:cpp:any:`pjmedia_ice_trickle_has_new_cand`) plus the ``a=mid``,
``a=ice-ufrag`` and ``a=ice-pwd`` lines and, when local gathering
completes, the ``a=end-of-candidates`` marker.

INFO messages are batched on a short timer
(:c:macro:`PJSUA_TRICKLE_ICE_NEW_CAND_CHECK_INTERVAL`, default
100 ms) so a burst of candidate-ready events produces one INFO, not
several.

Provisional responses (18x) before INFO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the dialog is not yet established (i.e. before the final
response) trickling on the answerer side rides 18x provisional
responses with SDP. PJSIP retransmits these provisional responses
(exponential backoff, capped at 6 attempts) until either the dialog
is established (so SIP INFO becomes available) or trickling
completes.


Detecting peer trickle support
------------------------------

PJSIP doesn't actively probe peer capability before negotiation.
Application-level discovery is done by inspecting the peer's:

- ``Supported: trickle-ice`` header in initial signalling, or
- ``a=ice-options:trickle`` attribute in a received SDP

For greenfield endpoint-to-endpoint setups where peer support is
guaranteed, full trickle is appropriate. For mixed fleets — or
anything reaching PSTN, gateways, or legacy PBXs — start with half
trickle.


Programmatic candidate notifications
------------------------------------

Applications that want to observe candidate gathering progress (for
UI feedback, logging, or custom signalling outside the PJSIP-managed
SDP flow) can hook
:cpp:any:`pjmedia_ice_cb::on_new_candidate` on the underlying
PJMEDIA ICE transport, which forwards
:cpp:any:`pj_ice_strans_cb::on_new_candidate` from PJNATH. The
callback fires for each newly resolved srflx/relayed candidate and
once more with ``end_of_cand=PJ_TRUE`` when gathering is complete.

Most PJSIP applications don't need this — the PJSIP-LIB / PJSUA2
SIP-side wiring delivers candidates automatically.


Debugging
---------

A few markers help when call setup with trickle isn't working as
expected:

- **Initial SDP lacks** ``a=ice-options:trickle`` — trickle is
  disabled or the global setting wasn't picked up. Verify
  ``ice_cfg_use`` is ``PJSUA_ICE_CONFIG_USE_CUSTOM`` if you set it
  per account.

- **Peer ignores trickled INFO** — check the peer accepts
  ``application/trickle-ice-sdpfrag`` and observes the
  ``trickle-ice`` ``Supported`` header. Some intermediaries strip
  unknown ``Supported`` values.

- **No** ``a=end-of-candidates`` **ever sent** — gathering is hanging
  on a STUN or TURN server. Check the server is reachable; the
  ICE log at level 4 prints per-candidate progress (look for
  ``Trickle`` and ``ice trickle`` lines in
  :sourcedir:`pjsip/src/pjsua-lib/pjsua_call.c`).

- **Aggressive nomination warnings** — harmless once trickle is on,
  but they indicate the previously-set aggressive flag was
  overridden by trickle (expected behaviour).


Interaction with other ICE features
-----------------------------------

- **TURN TCP/TLS** — orthogonal. Trickle controls *when* candidates
  are conveyed; the TURN connection type controls *what* relayed
  candidate is allocated. See :doc:`turn_tcp_tls`.

- **Manual host candidates** — manual candidates are added during
  ICE initialisation alongside auto-detected ones, so they appear in
  the initial offer with the auto-detected hosts. Trickle only
  affects the srflx/relayed candidates that arrive later. See
  :doc:`manual_ice_host_cand`.

- **Negotiation timeout** — even with trickle, ICE will report
  failure (with default settings) after roughly 7–8 seconds of no
  successful pair, the same as regular ICE.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::AccountNatConfig::iceTrickle`
     - ``acc_cfg.ice_cfg.ice_opt.trickle`` (per account, with
       ``ice_cfg_use = PJSUA_ICE_CONFIG_USE_CUSTOM``) or
       ``med_cfg.ice_opt.trickle`` (global). The field type is
       :cpp:any:`pj_ice_sess_options` and the relevant member is
       :cpp:any:`pj_ice_sess_options::trickle`.

Note: candidate trickling (SDP-fragment encoding, SIP INFO send/receive,
checklist updates) is handled by PJSUA-LIB itself in
:sourcedir:`pjsip/src/pjsua-lib/pjsua_call.c`; neither PJSUA-LIB nor
PJSUA2 surfaces a per-candidate event. Applications needing that
signal use the PJMEDIA-level callback
:cpp:any:`pjmedia_ice_cb::on_new_candidate` (which itself wraps
:cpp:any:`pj_ice_strans_cb::on_new_candidate` from PJNATH).
The underlying trickle helpers —
:cpp:any:`pjmedia_ice_trickle_update`,
:cpp:any:`pjmedia_ice_trickle_encode_sdp`,
:cpp:any:`pjmedia_ice_trickle_decode_sdp`,
:cpp:any:`pj_ice_strans_update_check_list` — are PJMEDIA / PJNATH
APIs intended for the SIP integration layer, not for direct
application use.


References
----------

- Trickle ICE: :rfc:`8838`
- SIP usage for Trickle ICE: :rfc:`8840`
- Base ICE (for context): :rfc:`8445`
- Initial implementation: :pr:`2588`; follow-up: :pr:`2667`

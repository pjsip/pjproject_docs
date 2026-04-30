DTMF
=========================================

.. contents:: Table of Contents
    :depth: 2


.. tip::

   This page is **PJSUA2-first**: prose, examples, and symbol names use the
   PJSUA2 (C++) API, with PJSUA-LIB equivalents in the
   :ref:`footer table <dtmf_pjsua_lib_equivalents>`.


Overview
------------------
PJSIP supports three DTMF transports for outgoing digits and two for
incoming digits:

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Method
     - Send
     - Receive
   * - RTP events (:rfc:`4733`, originally :rfc:`2833`)
     - Yes
     - Yes
   * - SIP INFO
     - Yes
     - Yes
   * - Inband audio tones
     - Yes
     - No (see :ref:`Inband detection <dtmf_inband_detection>` for a wiring sketch)

**RFC 4733 (telephone-event) is the recommended method.** It carries
events in-band with RTP, doesn't burden the signalling path, and is
the standards-based choice. PJSIP only sends RFC 4733 events when the
peer's SDP advertises the capability with a line like::

   a=rtpmap:101 telephone-event/8000

Without that line on the negotiated SDP, attempting to send via RFC 4733
returns ``PJMEDIA_RTP_EREMNORFC2833`` and the call falls back to whatever
fallback path the application implements (commonly: SIP INFO).

**SIP INFO** is non-standard (see :rfc:`6086#section-2`), expensive — every
keystroke becomes a SIP transaction — and the body format isn't
universally agreed (some PBXes use ``application/dtmf``,
some use ``application/dtmf-relay``; PJSIP sends and parses
``dtmf-relay``). Use only when RFC 4733 is unavailable. See :issue:`2036`
for background.

**Inband audio tones** are useful for codecs that don't preserve DTMF
through transcoding (e.g. some legacy gateways), but PJSIP does **not**
implement inband DTMF *detection* — only generation. See
:ref:`dtmf_inband_send` and :ref:`dtmf_inband_detection` for details.


Sending DTMF
------------

The modern API is :cpp:func:`pj::Call::sendDtmf`, which takes a
:cpp:any:`pj::CallSendDtmfParam` carrying the method, duration, and
digit string. It supersedes the legacy ``Call::dialDtmf()`` (the C
``pjsua_call_dial_dtmf*`` family), which was RFC 4733 only.

.. code-block:: c++

   try {
       CallSendDtmfParam prm;
       prm.method   = PJSUA_DTMF_METHOD_RFC2833;
       prm.duration = 200;       // milliseconds; 0 to use default
       prm.digits   = "12345";
       call.sendDtmf(prm);
   } catch (Error& err) {
       // PJMEDIA_RTP_EREMNORFC2833 if peer didn't advertise the
       // telephone-event rtpmap — fall back to SIP INFO here.
   }

The default ``duration`` is ``PJSUA_CALL_SEND_DTMF_DURATION_DEFAULT``,
in turn derived from ``PJMEDIA_DTMF_DURATION_MSEC`` (200 ms by default;
see :pr:`3540`). Passing ``0`` selects the default.

When ``method`` is ``PJSUA_DTMF_METHOD_RFC2833``, ``sendDtmf`` enqueues
the digits in the audio stream's DTMF send queue and returns immediately;
the digits go out one by one at the rate dictated by ``duration`` plus a
configured pause. When ``method`` is ``PJSUA_DTMF_METHOD_SIP_INFO``,
each digit produces one SIP INFO request immediately.

Method-selection trade-offs:

- **RFC 4733** — recommended. Cheap (in-band with RTP), standards-based,
  provides start / update / end semantics for the receiver. Requires
  peer-advertised capability in SDP.
- **SIP INFO** — fall-back when RFC 4733 is unavailable. Non-standard,
  expensive (one SIP transaction per digit), interop-fragile. Per the
  ``PJSUA_DTMF_METHOD_SIP_INFO`` doxygen: if the remote doesn't support
  SIP INFO and never replies, the sender treats it as a transaction
  timeout and **disconnects the call**.
- **Inband** — last-resort for paths that strip RFC 4733 / INFO. Plays
  audio tones over the existing media channel. See :ref:`dtmf_inband_send`.

Send-queue management
~~~~~~~~~~~~~~~~~~~~~

For RFC 4733, ``sendDtmf`` doesn't block: digits queue and play out at
the configured cadence. To inspect backpressure (e.g. before queuing
more digits from a dial-pad), PJSUA-LIB exposes
:cpp:any:`pjsua_call_get_queued_dtmf_digits` (:pr:`4645`):

.. code-block:: c

   unsigned queued = 0;
   pjsua_call_get_queued_dtmf_digits(call_id, &queued);

Returns the number of digits still pending transmission. Only
available in PJSUA-LIB; can be invoked directly from PJSUA2 C++
apps.


Tuning RFC 4733 transmission
----------------------------

.. note::

   The API in this section lives in PJMEDIA (no PJSUA2 wrapper).
   The ``pjmedia_stream *`` pointer is delivered to the application
   via :cpp:func:`pj::Call::onStreamCreated` (PJSUA2) /
   :cpp:any:`pjsua_callback::on_stream_created` (PJSUA-LIB); stash it
   when the callback fires and invoke the PJMEDIA functions against
   it.

For finer control over how RFC 4733 events are emitted on the wire,
:cpp:any:`pjmedia_stream_set_tx_dtmf_options` (:pr:`4663`) configures
the per-stream send parameters:

.. code-block:: c

   pjmedia_stream_set_tx_dtmf_options(
       stream,                     /* The audio stream */
       200,                        /* duration_ms (0..1000)              */
       50,                         /* pause_ms between events (0..1000)  */
       101,                        /* payload type                       */
       0,                          /* volume in dBm0 (-63..0; 0 = max)   */
       2                           /* extra end-bit repetitions (0..7)   */
   );

Knobs:

- **``duration_ms``** — single-event duration. Overrides the
  ``CallSendDtmfParam::duration`` and ``PJMEDIA_DTMF_DURATION_MSEC``
  defaults at the stream level.
- **``pause_ms``** — gap inserted between consecutive events when the
  send queue has more than one digit.
- **``pt``** — RTP payload type. Defaults to whatever the SDP
  negotiation produced (typically 101). Override only when the peer
  insists on a non-default PT.
- **``vol``** — RTP DTMF volume in dBm0; ``0`` is loudest, ``-63``
  quietest.
- **``ebit_rep_cnt``** — extra repetitions of the end-bit packet (the
  packet that signals "key released"). The total number of end-bit
  packets transmitted is ``1 + ebit_rep_cnt``. RFC 4733 §2.5.1.3
  recommends three total; PJSIP defaults to ``ebit_rep_cnt = 2``
  (i.e. three end-bit packets) — see ``DTMF_EBIT_RETRANSMIT_CNT`` in
  ``pjmedia/src/pjmedia/stream.c`` and :issue:`1582`. Bump on lossy
  UDP paths.

DTMF flash (event 16)
---------------------

RFC 4733 reserves event 16 for the on-hook flash signal. PJSIP encodes
flash with the literal character ``'R'`` in the digits string (per the
``pjsua_call_dial_dtmf`` doxygen and :rfc:`4730`). Compile-time toggle
``PJMEDIA_HAS_DTMF_FLASH`` (default on; :issue:`1734`) gates the
feature.

.. code-block:: c++

   CallSendDtmfParam prm;
   prm.method   = PJSUA_DTMF_METHOD_RFC2833;
   prm.duration = 200;
   prm.digits   = "R";          // single flash
   call.sendDtmf(prm);

Receivers see the flash as digit ASCII ``'R'`` (event code 16).


Receiving DTMF
--------------

PJSUA2 exposes two virtual callbacks on :cpp:class:`pj::Call`:

- :cpp:func:`pj::Call::onDtmfDigit` — fires for each digit; the
  :cpp:any:`pj::OnDtmfDigitParam` carries the method (RFC 4733 vs SIP
  INFO), digit, and total duration in milliseconds (or
  ``PJSUA_UNKNOWN_DTMF_DURATION``).
- :cpp:func:`pj::Call::onDtmfEvent` — fires for **every** RTP event
  packet (including update packets while a key is held), giving the
  application start / update / end semantics. Carries an extra
  ``flags`` field with ``PJMEDIA_STREAM_DTMF_IS_UPDATE`` /
  ``PJMEDIA_STREAM_DTMF_IS_END`` bits.

The most-specific implemented callback wins. ``onDtmfEvent`` —
when implemented — fully suppresses ``onDtmfDigit``, regardless of
method (verified at ``pjsua_aud.c:746-757``). Pick the callback that
matches what your dial-plan needs:

- **Single shot per digit** — implement ``onDtmfDigit``. Easiest for
  IVR-style dial-pads.
- **Progressive updates** (long-press, hold-to-flash, KPML-like UX) —
  implement ``onDtmfEvent`` and watch the flag bits.

.. code-block:: c++

   class MyCall : public Call {
   public:
       using Call::Call;

       void onDtmfDigit(OnDtmfDigitParam &prm) override
       {
           cout << "DTMF digit '" << (char)prm.digit << "'"
                << " via " << (prm.method == PJSUA_DTMF_METHOD_RFC2833
                               ? "RFC 4733" : "SIP INFO")
                << ", duration=" << prm.duration << " ms" << endl;
       }
   };

For the event-based callback, distinguish phases by inspecting
``prm.flags``:

.. code-block:: c++

   void onDtmfEvent(OnDtmfEventParam &prm) override
   {
       if (prm.flags & PJMEDIA_STREAM_DTMF_IS_END) {
           // Final indication; prm.duration is the total length (or
           // PJSUA_UNKNOWN_DTMF_DURATION). End indications can be
           // lost — applications should not require one for every
           // event.
       } else if (prm.flags & PJMEDIA_STREAM_DTMF_IS_UPDATE) {
           // Same digit, updated duration so far. The key is still
           // pressed.
       } else {
           // First indication for this digit.
       }
   }

For SIP INFO digits, ``onDtmfEvent`` fires once per digit with
``PJMEDIA_STREAM_DTMF_IS_END`` set (verified at ``pjsua_call.c:6749-6770``)
— SIP INFO has no incremental update mechanism.


SDP / capability negotiation
----------------------------

PJSIP advertises ``telephone-event`` in outgoing offers when
``PJMEDIA_RTP_PT_TELEPHONE_EVENTS`` is non-zero (default 120). A typical
offer looks like::

   m=audio 4000 RTP/AVP 0 8 120
   a=rtpmap:0 PCMU/8000
   a=rtpmap:8 PCMA/8000
   a=rtpmap:120 telephone-event/8000
   a=fmtp:120 0-15

The exact payload type negotiated may differ — many peers (Asterisk,
Cisco, FreeSWITCH defaults) use 101, and PJSIP picks whatever PT
survives negotiation. When the remote answers with a matching rtpmap,
RFC 4733 send is enabled. When the remote omits it, ``sendDtmf`` with
method ``PJSUA_DTMF_METHOD_RFC2833`` returns
``PJMEDIA_RTP_EREMNORFC2833``.

To detect the negotiated PT (e.g. when a peer uses something other
than the default), inspect ``pjmedia_stream_info::tx_event_pt`` after
the call goes active. Override the per-stream PT via
:cpp:any:`pjmedia_stream_set_tx_dtmf_options` if you need to match a
specific peer.

Two compile-time settings shape what PJSIP advertises:

- **``PJMEDIA_RTP_PT_TELEPHONE_EVENTS``** (default ``120``) — the
  starting payload type for telephone-event entries in outgoing SDP.
  Setting this to ``0`` disables telephone-event advertisement
  entirely (i.e. PJSIP will not offer or accept RFC 4733 events on
  any call).
- **``PJMEDIA_TELEPHONE_EVENT_ALL_CLOCKRATES``** (default ``1``;
  :issue:`2088`) — when enabled, PJSIP offers one
  ``telephone-event/<rate>`` rtpmap per audio-codec clock rate
  advertised in the offer (e.g. one for 8 kHz PCMU/PCMA, another
  for 16 kHz AMR-WB or Speex/16000, another for 48 kHz Opus). When
  disabled, only a single 8 kHz entry is offered (legacy behaviour
  before :issue:`2088`). The all-clockrates default is a safety belt
  for strict peers that insist on a matching telephone-event
  clockrate; in practice most endpoints accept RFC 4733 events even
  when only the 8 kHz entry is offered. Trade-offs of leaving it on:
  larger SDP, and more dynamic-PT slots (96-127) consumed by
  telephone-event entries — usually a non-issue, but worth knowing
  for footprint-constrained deployments offering many codecs.


.. _dtmf_inband_send:

Sending inband DTMF tones
--------------------------
Below are steps to send inband DTMF tones:

#. Once the call is established, create an instance of
   :doc:`Multi-frequency/DTMF Tone Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`.
#. Register this tone generator to pjsua's conference bridge with :cpp:any:`pjsua_conf_add_port()`.
#. *Connect* the tone generator to the call, with :cpp:any:`pjsua_conf_connect()`.
#. Now instruct the tone generator to *play* some DTMF digits with :cpp:any:`pjmedia_tonegen_play_digits()`.
   The digits then will be streamed to the call, and remote endpoint should receive the DTMF tone inband.

Below is the snippet to do it:

.. code-block:: c

   struct my_call_data
   {
        pj_pool_t          *pool;
        pjmedia_port       *tonegen;
        pjsua_conf_port_id  toneslot;
   };

   struct my_call_data *call_init_tonegen(pjsua_call_id call_id)
   {
        pj_pool_t *pool;
        struct my_call_data *cd;
        pjsua_call_info ci;

        pool = pjsua_pool_create("mycall", 512, 512);
        cd = PJ_POOL_ZALLOC_T(pool, struct my_call_data);
        cd->pool = pool;

        pjmedia_tonegen_create(cd->pool, 8000, 1, 160, 16, 0, &cd->tonegen);
        pjsua_conf_add_port(cd->pool, cd->tonegen, &cd->toneslot);

        pjsua_call_get_info(call_id, &ci);
        pjsua_conf_connect(cd->toneslot, ci.conf_slot);

        pjsua_call_set_user_data(call_id, (void*) cd);

        return cd;
   }

   void call_play_digit(pjsua_call_id call_id, const char *digits)
   {
        pjmedia_tone_digit d[16];
        unsigned i, count = strlen(digits);
        struct my_call_data *cd;

        cd = (struct my_call_data*) pjsua_call_get_user_data(call_id);
        if (!cd)
            cd = call_init_tonegen(call_id);

        if (count > PJ_ARRAY_SIZE(d))
            count = PJ_ARRAY_SIZE(d);

        pj_bzero(d, sizeof(d));
        for (i=0; i<count; ++i) {
           d[i].digit = digits[i];
           d[i].on_msec = 100;
           d[i].off_msec = 200;
           d[i].volume = 0;
        }

        pjmedia_tonegen_play_digits(cd->tonegen, count, d, 0);
   }

   void call_deinit_tonegen(pjsua_call_id call_id)
   {
        struct my_call_data *cd;

        cd = (struct my_call_data*) pjsua_call_get_user_data(call_id);
        if (!cd)
           return;

        pjsua_conf_remove_port(cd->toneslot);
        pjmedia_port_destroy(cd->tonegen);
        pj_pool_release(cd->pool);

        pjsua_call_set_user_data(call_id, NULL);
   }

The resources that were allocated above must be released once the call is disconnected,
by implementing this in :cpp:any:`pjsua_callback::on_call_state` callback:

.. code-block:: c

   static void on_call_state(pjsua_call_id call_id, pjsip_event *e)
   {
        pjsua_call_info call_info;

        pjsua_call_get_info(call_id, &call_info);

        if (call_info.state == PJSIP_INV_STATE_DISCONNECTED) {
           call_deinit_tonegen(call_id);
        }
   }

With the above snippet, calling ``call_play_digit()`` sends inband DTMF
digits to the remote party.


.. _dtmf_inband_detection:

Implementing an inband DTMF detector
-------------------------------------
Currently PJMEDIA lacks built-in tone detection routine. If a tone-detection
routine is available, integrating it into the framework is straightforward:

#. Wrap the routine as :doc:`PJMEDIA Port </api/generated/pjmedia/group/group__PJMEDIA__PORT>`
   so that it can be plugged into the media framework. The implementation would be similar to
   :doc:`WAV recorder </api/generated/pjmedia/group/group__PJMEDIA__FILE__REC>` media port
   (:source:`pjmedia/src/pjmedia/wav_writer.c`), but instead of writing to a WAV file, it would
   monitor the audio signal for tones and call some callback when a tone is detected.
#. Once the tone-detector media port is implemented, add this media port to the conference bridge
   with :cpp:any:`pjsua_conf_add_port()`, and connect the audio source to your tone detector
   with :cpp:any:`pjsua_conf_connect()`.


.. _dtmf_pjsua_lib_equivalents:

PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:func:`pj::Call::sendDtmf` /
       :cpp:any:`pj::CallSendDtmfParam`
     - :cpp:any:`pjsua_call_send_dtmf` /
       :cpp:any:`pjsua_call_send_dtmf_param`
   * - (no equivalent — PJSUA2 standardised on the param-struct form)
     - Legacy: :cpp:any:`pjsua_call_dial_dtmf` /
       :cpp:any:`pjsua_call_dial_dtmf2` (RFC 4733 only)
   * - :cpp:func:`pj::Call::onDtmfDigit` /
       :cpp:any:`pj::OnDtmfDigitParam`
     - :cpp:any:`pjsua_callback::on_dtmf_digit2` /
       :cpp:any:`pjsua_dtmf_info`. Legacy ASCII-only
       :cpp:any:`pjsua_callback::on_dtmf_digit` is suppressed when
       ``on_dtmf_digit2`` is set.
   * - :cpp:func:`pj::Call::onDtmfEvent` /
       :cpp:any:`pj::OnDtmfEventParam`
     - :cpp:any:`pjsua_callback::on_dtmf_event` /
       :cpp:any:`pjsua_dtmf_event`
   * - PJSUA-LIB only (invoke from C++)
     - :cpp:any:`pjsua_call_get_queued_dtmf_digits`
   * - PJMEDIA only (invoke from C++)
     - :cpp:any:`pjmedia_stream_set_tx_dtmf_options` (per-stream
       duration / pause / PT / volume / end-bit reps)

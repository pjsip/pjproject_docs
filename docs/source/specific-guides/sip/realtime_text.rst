.. _guide_realtime_text:

Real-Time Text (RFC 4103)
==========================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
------------------

Real-time text (RTT) is a media stream that carries text characters
character-by-character as the sender types, so the recipient sees
each keystroke as it is entered rather than waiting for a full
message. The transport is RTP, negotiated in SDP alongside the call's
audio and (optionally) video; the wire format is :rfc:`4103` (which
uses the T.140 character set wrapped in :rfc:`2198` redundancy).

Why it matters
~~~~~~~~~~~~~~

RTT is the standard accessibility-compliant text channel for SIP — the
modern equivalent of a TTY for hearing- or speech-impaired users. The
US FCC and EU accessibility directives mandate RTT support in
"advanced communication services", so applications that target those
markets need it.


RTT vs SIP MESSAGE / instant messaging
--------------------------------------

PJSIP supports two distinct mechanisms for text in a call. They solve
different problems and use entirely different transports — pick the
one that matches your use case.

+--------------------------------+--------------------------------------------------+
| Real-time text (this guide)    | SIP MESSAGE / instant messaging                  |
+================================+==================================================+
| RTP media stream — m=text line | SIP MESSAGE method — no media stream             |
| in SDP                         |                                                  |
+--------------------------------+--------------------------------------------------+
| Live, character-by-character   | Discrete, complete messages                      |
+--------------------------------+--------------------------------------------------+
| Always tied to a call          | Inside a call (in-dialog) **or** outside a call  |
|                                | (out-of-dialog)                                  |
+--------------------------------+--------------------------------------------------+
| Accessibility — TTY equivalent | "Chat in the call" or presence-style messaging   |
+--------------------------------+--------------------------------------------------+
| ``Call::sendText()`` /         | ``Call::sendInstantMessage()`` (in-dialog)       |
| ``Call::onCallRxText()``       | ``Buddy::sendInstantMessage()`` (out-of-dialog)  |
+--------------------------------+--------------------------------------------------+

For instant messaging (SIP MESSAGE), see the *Instant Messaging (IM)*
sections of :doc:`/pjsua2/using/call` and :doc:`/pjsua2/using/presence`.


Build prerequisites
-------------------

Real-time text is built unconditionally with the rest of PJMEDIA — no
per-feature build flag. Available in PJSIP 2.16 and later (:pr:`4344`).

The maximum RFC 2198 redundancy level used at runtime is capped at
:c:macro:`PJMEDIA_TXT_STREAM_MAX_RED_LEVELS` (default ``2``), set at
compile time in ``config_site.h``. The default of 2 covers RFC 4103's
recommendation; raise it only if your deployment has truly unusual
loss characteristics.


Negotiating a text stream
-------------------------

A call carries a text stream when the call setting includes one. Set
``CallSetting::textCount`` to ``1`` (or higher for multiple text
streams; rare) before issuing the offer or answer:

.. code-block:: c++

   try {
       CallOpParam prm(true);  // true = use default CallSetting
       prm.opt.audioCount = 1;
       prm.opt.videoCount = 0;
       prm.opt.textCount  = 1;

       call.makeCall("sip:peer@example.com", prm);
   } catch(Error& err) {
   }

The result is an additional ``m=text`` line in the offered SDP with
two ``rtpmap`` entries — ``red/1000`` for the RFC 2198 redundancy
codec and ``t140/1000`` for the underlying T.140 payload, as
specified in RFC 4103. If the peer accepts, the negotiated text
stream is created and the application can immediately send and
receive on it.

To accept incoming calls that offer a text stream, leave
``CallSetting::textCount`` at its default of ``1`` — the incoming
text stream is negotiated automatically and reported in
``onCallMediaState``. Set it to ``0`` to refuse text-stream offers.


Sending text
------------

Text is sent through :cpp:func:`pj::Call::sendText()` taking a
:cpp:any:`pj::CallSendTextParam`. The typical pattern is to call it
from the application's keystroke handler:

.. code-block:: c++

   void onKeyPressed(const std::string &ch)
   {
       try {
           CallSendTextParam param;
           param.text = ch;   // typically a single character or short run
           call.sendText(param);
       } catch(Error& err) {
       }
   }

The library handles RFC 4103 packetisation, the inter-keystroke
buffering window, and RFC 2198 redundancy transparently — pass each
character (or short run of characters) to ``sendText()`` as the user
types.

You can also call ``sendText()`` with a longer string when text
arrives in larger chunks (paste, autocomplete acceptance, voice-to-text
output). The library will fragment it into RFC 4103 packets.

The ``CallSendTextParam::medIdx`` field selects which text stream to
send to when the call has more than one. Default ``-1`` selects the
first text stream; in single-text-stream calls (the common case) you
can leave it alone.


Receiving text
--------------

Incoming text is delivered through :cpp:func:`pj::Call::onCallRxText`
on the application's ``Call`` subclass:

.. code-block:: c++

   class MyCall : public Call
   {
   public:
       using Call::Call;

       virtual void onCallRxText(OnCallRxTextParam &prm) override
       {
           // prm.seq — RTP sequence number for this text block
           // prm.ts  — RTP timestamp
           // prm.text — the decoded text (UTF-8); may be empty
           if (!prm.text.empty())
               appendToTranscript(prm.text);
       }
   };

The callback fires once per received text block, after the receive
buffer / jitter window has been drained. The library handles the
RFC 2198 redundancy decoding and discards duplicates by RTP sequence
number — the application sees each character at most once. Text may
legitimately be empty (the header explicitly notes
*"the text can be empty"*); guard for that.

T.140 control characters in the received bytes are passed through
verbatim — the application is responsible for any UI-level handling
(e.g. interpreting backspace).


Redundancy level (RFC 4103 / RFC 2198)
--------------------------------------

The RFC 2198 redundancy mechanism prepends each outgoing text packet
with copies of the previous N text blocks, so a packet loss of up to
N consecutive packets can be recovered by the receiver from a later
packet. Trade-off: each redundancy level adds packet bytes for every
text block sent.

The level is configured per account on
:cpp:any:`pj::AccountTextConfig::redundancyLevel`, accessed as
``AccountConfig::textConfig.redundancyLevel``:

.. code-block:: c++

   AccountConfig acc_cfg;
   // ... other configuration ...
   acc_cfg.textConfig.redundancyLevel = 2;   // default; 0 disables

   MyAccount *acc = new MyAccount;
   acc->create(acc_cfg);

Practical guidance:

- ``0`` — no redundancy. Lowest bandwidth; lowest tolerance to loss.
- ``1`` — adequate against an average packet loss of up to ~50 %.
- ``2`` — default; tolerates ~66.7 % loss. Recommended by RFC 4103.

The level actually used on the wire is the lower of the local and
remote levels after SDP negotiation, so configuring ``2`` locally is
safe even if the peer caps at ``1``.

The cap is :c:macro:`PJMEDIA_TXT_STREAM_MAX_RED_LEVELS` (default
``2``); raise it in ``config_site.h`` and rebuild if you genuinely
need higher.


Sample applications
-------------------

The pjsua console sample at :sourcedir:`pjsip-apps/src/pjsua` exposes
text-call commands; use it to verify a build supports RTT end-to-end
and as a reference for how the API is wired. The PJMEDIA-level
implementation lives in
:sourcedir:`pjmedia/src/pjmedia/txt_stream.c` and the PJSUA-LIB
integration in :sourcedir:`pjsip/src/pjsua-lib/pjsua_txt.c`.


PJSUA-LIB equivalents
---------------------

+----------------------------------------------------+--------------------------------------------------------+
| PJSUA2                                             | PJSUA-LIB                                              |
+====================================================+========================================================+
| ``CallSetting::textCount``                         | :cpp:any:`pjsua_call_setting::txt_cnt`                 |
+----------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Call::sendText()` /                 | :cpp:any:`pjsua_call_send_text()` /                    |
| ``CallSendTextParam{medIdx, text}``                | :cpp:any:`pjsua_call_send_text_param`                  |
+----------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Call::onCallRxText` /               | :cpp:any:`pjsua_callback::on_call_rx_text` /           |
| ``OnCallRxTextParam{seq, ts, text}``               | :cpp:any:`pjsua_txt_stream_data`                       |
+----------------------------------------------------+--------------------------------------------------------+
| ``AccountConfig::textConfig.redundancyLevel``      | :cpp:any:`pjsua_acc_config::txt_red_level`             |
+----------------------------------------------------+--------------------------------------------------------+

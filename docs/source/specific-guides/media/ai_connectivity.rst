AI Connectivity
====================

.. contents:: Table of Contents
    :depth: 3

Available since 2.17: WebSocket client (:pr:`4859`), PJMEDIA AI port
(:pr:`4866`), PJSUA2 wrapper (:pr:`4870`).

.. warning::

   This feature is **experimental**. The API may change in future releases.


Overview
------------------
PJMEDIA ships an AI media port that bridges the conference bridge to a
real-time AI service over WebSocket, letting call audio be routed to a
cloud model (speech-in, speech-out) the same way it is routed to any
other conference port.

At a glance:

- **Transport:** WebSocket (``ws://`` or ``wss://``), via the pjlib-util
  WebSocket client.
- **Media:** full-duplex PCM16 over the conference bridge; the port runs
  at the backend's native rate (24 kHz for OpenAI) and the conference
  bridge handles any resampling.
- **Backends:** pluggable. A built-in OpenAI Realtime API backend is
  provided; other vendors can be added by implementing
  :cpp:any:`pjmedia_ai_backend_op`.
- **Events:** connect/disconnect, transcripts, response start/done, and
  server VAD speech-started/stopped are delivered via an application
  callback.

The feature is available at two levels:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Layer
     - Entry point
   * - PJMEDIA
     - :cpp:any:`pjmedia_ai_port_create` + a backend factory
       (e.g. :cpp:any:`pjmedia_ai_openai_backend_create`)
   * - PJSUA2
     - :cpp:any:`pj::AudioMediaAiPort` (subclass of ``AudioMedia``),
       override ``onEvent()`` for notifications


PJSUA2 API
------------------

``AudioMediaAiPort`` wraps the PJMEDIA port as a standard ``AudioMedia``
subclass, so it can be connected to/from any other conference port
(call media, sound device, player, recorder, etc.) with the usual
``startTransmit()``/``stopTransmit()``.

.. code-block:: c++

   class MyAiPort : public AudioMediaAiPort
   {
       void onEvent(const AiMediaEvent &event) override
       {
           switch (event.type) {
           case PJMEDIA_AI_EVENT_CONNECTED:
               std::cout << "AI connected\n";
               break;
           case PJMEDIA_AI_EVENT_TRANSCRIPT:
               std::cout << "Transcript: " << event.text << "\n";
               break;
           case PJMEDIA_AI_EVENT_DISCONNECTED:
               std::cout << "AI disconnected, status=" << event.status << "\n";
               break;
           default:
               break;
           }
       }
   };

   MyAiPort ai;
   ai.createPort();    // Uses the OpenAI Realtime backend
   ai.connect("wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview",
              apiKey);

   // Bridge the call both ways
   callAudio.startTransmit(ai);
   ai.startTransmit(callAudio);

   // ... when done ...
   ai.disconnect();


Python (via SWIG) mirrors the same shape:

.. code-block:: python

   import pjsua2 as pj

   class MyAiPort(pj.AudioMediaAiPort):
       def onEvent(self, event):
           if event.type == pj.PJMEDIA_AI_EVENT_TRANSCRIPT:
               print("Transcript:", event.text)

   ai = MyAiPort()
   ai.createPort()
   ai.connect("wss://api.openai.com/v1/realtime?model=...", api_key)
   call_audio.startTransmit(ai)
   ai.startTransmit(call_audio)

.. note::

   ``onEvent()`` is invoked from the pjsua ioqueue worker thread. Keep
   the callback non-blocking; marshal work to an application thread if
   you need to do anything expensive (DB calls, UI updates, etc.).


PJMEDIA API
------------------

For applications that are not using PJSUA2, the underlying C API can be
used directly. The port needs an ioqueue, a timer heap, and a backend
instance. In a pjsua-based app you can reuse the SIP endpoint's ioqueue
and timer heap; in a standalone pjmedia app, create your own.

.. code-block:: c

   pjmedia_ai_backend *backend;
   pjmedia_ai_openai_backend_create(pool, &backend);

   pjmedia_ai_port_param prm;
   pjmedia_ai_port_param_default(&prm);
   prm.ioqueue       = pjsip_endpt_get_ioqueue(pjsua_get_pjsip_endpt());
   prm.timer_heap    = pjsip_endpt_get_timer_heap(pjsua_get_pjsip_endpt());
   prm.backend       = backend;          /* port takes ownership */
   prm.cb.on_event   = &on_ai_event;
   prm.user_data     = my_ctx;
   /* Optional: prm.vad_enabled, prm.ptime_msec, prm.ssl_param */

   pjmedia_ai_port *ai_port;
   pjmedia_ai_port_create(pool, &prm, &ai_port);

   pjmedia_port *port = pjmedia_ai_port_get_port(ai_port);
   pjmedia_conf_add_port(conf, pool, port, NULL, NULL);

   pj_str_t url   = pj_str("wss://api.openai.com/v1/realtime?model=...");
   pj_str_t token = pj_str(api_key);
   pjmedia_ai_port_connect(ai_port, &url, &token);

Destroy the port with :cpp:any:`pjmedia_port_destroy` when done; it
disconnects the WebSocket and destroys the backend it owns.


Events
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Event
     - Meaning
   * - ``PJMEDIA_AI_EVENT_CONNECTED``
     - WebSocket and backend session are ready; audio streaming starts.
   * - ``PJMEDIA_AI_EVENT_DISCONNECTED``
     - Connection lost or closed. ``event.status`` is ``PJ_SUCCESS`` for
       a clean close (code 1000) or an error otherwise.
   * - ``PJMEDIA_AI_EVENT_TRANSCRIPT``
     - Text transcript fragment from the AI service (``event.text``).
   * - ``PJMEDIA_AI_EVENT_RESPONSE_START`` / ``_DONE``
     - AI response generation started / finished.
   * - ``PJMEDIA_AI_EVENT_SPEECH_STARTED`` / ``_STOPPED``
     - Server-side VAD detected start / end of user speech.


Backends
------------------

The bundled OpenAI Realtime backend uses PCM16 at 24 kHz over a single
WebSocket, base64-encoded inside JSON events, with server-side VAD for
turn detection and barge-in. Other vendors can be added by implementing
:cpp:any:`pjmedia_ai_backend_op` (``prepare_connect``, ``on_ws_connected``,
``encode_audio``, ``on_rx_msg``, ``destroy``) and exposing a factory
similar to :cpp:any:`pjmedia_ai_openai_backend_create`.

Barge-in with the OpenAI backend is handled server-side: the AI port
keeps sending mic audio even while the AI is talking, so the server's
VAD can detect interruptions and truncate the response automatically.
To avoid false barge-ins from the AI's own playback leaking into the
mic, enable acoustic echo cancellation on the sound device
(:cpp:any:`pjmedia_snd_port_set_ec`) — the ``aidemo`` sample does this.


Limitations
------------------

The current PJSUA2 wrapper does not yet expose:

- SSL/TLS parameters (certificate verification, client certs, cipher
  suites). The C API accepts ``ssl_param``; TLS uses defaults in PJSUA2.
- OpenAI session customization (voice, instructions, modalities) — the
  backend defaults are used as-is.
- ``isConnected()`` / state query — connection state must be inferred
  from ``onEvent()``.
- JSON persistence for ``AiMediaPortParam``.


Sample app
------------------

:source:`pjsip-apps/src/samples/aidemo.c` is a minimal end-to-end demo:
local sound device ↔ OpenAI Realtime API. Build the samples, export
``OPENAI_API_KEY``, and run:

.. code-block:: sh

   export OPENAI_API_KEY="sk-..."
   ./pjsip-apps/bin/aidemo-x86_64-pc-linux-gnu

Useful options:

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Option
     - Description
   * - ``-m URL``
     - Override the WebSocket URL (default: OpenAI Realtime endpoint).
   * - ``-r N``
     - Sound device clock rate in Hz. Defaults to the backend native
       rate (24 kHz for OpenAI); set e.g. ``-r 48000`` if the sound
       device does not support 24 kHz — the demo resamples
       automatically.
   * - ``-n``
     - Null audio (no sound device); feeds silence. Useful for CI.
   * - ``-d N``
     - Duration in seconds for null-audio mode (default 10).
   * - ``-L N``
     - Log level 0–6 (default 4).

.. note::

   On Windows, log level 5+ can cause choppy audio because console
   output blocks the audio thread.

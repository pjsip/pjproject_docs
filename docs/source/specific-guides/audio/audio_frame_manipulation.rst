.. _guide_audio_frame_manipulation:

Audio Frame Manipulation
=========================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB and PJMEDIA-only readers — alternatives are listed at
   the bottom of this page.

Custom audio processing — applying a filter, feeding ML models,
muxing into another stream, recording to an unusual format, or just
inspecting the PCM passing through — needs application-level access
to raw audio frames. PJSIP exposes this access at three layers, with
different trade-offs in placement, capability, and ease of use.

If the underlying media-flow model (ports, ``get_frame()`` /
``put_frame()``, conference bridge) is unfamiliar, read
:doc:`/specific-guides/media/audio_flow` first.


PJSUA2 — ``AudioMediaPort``
----------------------------

The cleanest path for PJSUA2 (and SWIG-bound languages — Java, C#,
Python, Kotlin) is to subclass :cpp:any:`pj::AudioMediaPort` and
override its two callbacks:

- :cpp:func:`pj::AudioMediaPort::onFrameRequested` — invoked when
  the bridge needs an outbound frame from your port (you fill in
  the buffer to push data downstream).
- :cpp:func:`pj::AudioMediaPort::onFrameReceived` — invoked when
  the bridge delivers an inbound frame to your port (you read the
  buffer to consume data from upstream).

Both callbacks receive a :cpp:any:`pj::MediaFrame` carrying the
frame ``type`` (typically ``PJMEDIA_FRAME_TYPE_AUDIO``), a ``buf``
``ByteVector``, and a ``size``. The port participates in the
conference bridge like any other ``AudioMedia``: register it once,
then ``startTransmit`` / ``stopTransmit`` to wire it to your call's
audio media, the sound device, or any other source / sink.

Available since PJSIP 2.14 (:pr:`3569`).

Defining the port
~~~~~~~~~~~~~~~~~

.. code-block:: c++

   class MyAudioPort : public AudioMediaPort
   {
       virtual void onFrameRequested(MediaFrame &frame) override
       {
           // Fill frame.buf with up to frame.size bytes of audio.
           frame.type = PJMEDIA_FRAME_TYPE_AUDIO;
           // frame.buf.assign(frame.size, '\0');  // example: silence
       }

       virtual void onFrameReceived(MediaFrame &frame) override
       {
           // frame.buf and frame.size carry the inbound audio.
           // Inspect, copy into a queue for an ML model, write to a
           // file, etc. Keep the handler short — this runs on the
           // conference bridge clock thread.
       }
   };

Creating and wiring it
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++

   MyAudioPort *port = new MyAudioPort();

   MediaFormatAudio fmt;
   fmt.init(PJMEDIA_FORMAT_PCM,
            16000,    // clock rate
            1,        // channel count
            20000,    // frame time in microseconds (20 ms)
            16);      // bits per sample
   port->createPort("my_audio_port", fmt);

   // Wire to a call's audio media, in either or both directions:
   port->startTransmit(callAudio);   // we feed the call
   callAudio.startTransmit(*port);   // we receive the call's audio

The bridge handles clock-rate / channel-count / frame-size
conversion between connected ports, so the port's format only has
to be self-consistent — it doesn't have to match the call's codec.

Threading
~~~~~~~~~

The two callbacks run on the conference bridge's get-frame thread
(typically the sound device thread or a clock thread; see
:doc:`/specific-guides/media/audio_flow`). Keep them short and
non-blocking — long handlers stall the entire bridge tick. Pass
heavier work (file I/O, network calls, ML inference) to your own
thread via a queue.

Sample
~~~~~~

A working PJSUA2 example lives at
:sourcedir:`pjsip-apps/src/samples/pjsua2_demo.cpp` (search for
``MyAudioMediaPort``). The Python equivalent is in
:sourcedir:`pjsip-apps/src/swig/python/test.py`.


C / PJSUA-LIB / PJMEDIA alternatives
-------------------------------------

PJSUA2's ``AudioMediaPort`` was added in 2.14 and is the
recommended path. C-only applications, or apps that pre-date that
release, have three alternatives — listed by progressively more
setup but more capability.

PJSUA-LIB sound-device hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two callbacks on :cpp:any:`pjsua_media_config` give read access to
audio frames at the sound-device boundary:

- :cpp:any:`pjsua_media_config::on_aud_prev_rec_frame` — every
  microphone frame, **before** any media processing (echo
  canceller, AGC, noise suppression).
- :cpp:any:`pjsua_media_config::on_aud_prev_play_frame` — every
  playback frame, **right before** it's queued to the speaker.

Set them in the :cpp:any:`pjsua_media_config` you pass to
:cpp:any:`pjsua_init`:

.. code-block:: c

   static void on_rec(pjmedia_frame *frame)
   {
       /* frame->buf, frame->size — read-mostly. */
   }

   pjsua_media_config med_cfg;
   pjsua_media_config_default(&med_cfg);
   med_cfg.on_aud_prev_rec_frame = &on_rec;
   pjsua_init(&ua_cfg, &log_cfg, &med_cfg);

Caveats:

- The callbacks fire on the **sound-device thread**. No blocking,
  no PJSUA API calls that could lock, no audio-device switching,
  no ``pjsua_set_ec()``.
- They expose a single shared point in the audio pipeline — every
  call's audio mixes into the same playback stream you see here.
- Modifying the audio is **not safe** when software echo
  cancellation is active — the EC trains on the unmodified data,
  so changes would degrade or break it.

Use these when you need cheap, application-wide observation
(logging energy levels, dumping raw audio for debug, simple
metrics).

Custom ``pjmedia_port``
~~~~~~~~~~~~~~~~~~~~~~~

For full bidirectional access at the conference-bridge level
(equivalent to PJSUA2's ``AudioMediaPort``), implement a
:cpp:any:`pjmedia_port` with your own ``put_frame`` / ``get_frame``
function pointers, then register it with
:cpp:any:`pjsua_conf_add_port`:

.. code-block:: c

   static pj_status_t my_put_frame(pjmedia_port *this_port, pjmedia_frame *frame)
   {
       /* Inbound: bridge wrote a frame into us. */
       return PJ_SUCCESS;
   }

   static pj_status_t my_get_frame(pjmedia_port *this_port, pjmedia_frame *frame)
   {
       /* Outbound: bridge wants a frame from us. Fill frame->buf. */
       frame->type = PJMEDIA_FRAME_TYPE_AUDIO;
       return PJ_SUCCESS;
   }

   pjmedia_port *port = pj_pool_zalloc(pool, sizeof(pjmedia_port));
   pjmedia_port_info_init(&port->info, &name,
                          PJMEDIA_SIG_CLASS_PORT_AUD('m','p'),
                          16000, 1, 16, 320);
   port->put_frame = &my_put_frame;
   port->get_frame = &my_get_frame;

   pjsua_conf_port_id slot;
   pjsua_conf_add_port(pool, port, &slot);
   /* slot is now usable like any other bridge port. */

Same threading rules apply — the function pointers run on the
bridge clock thread.

Direct PJMEDIA audio device
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For applications that do not run a SIP stack at all — pure media
processing — use :cpp:any:`pjmedia_aud_stream_create` with
:cpp:any:`pjmedia_aud_rec_cb` and :cpp:any:`pjmedia_aud_play_cb`
callbacks. This bypasses both PJSUA-LIB and the conference bridge
and gives raw access to capture / playback frames at the audio
device level.

This is the lowest-level option and the most flexible (no
conference-bridge involvement at all), but you take on all
buffering, format conversion, and routing yourself.


Cross-cutting tools
-------------------

For interception at a *different* layer of the stack, see also:

- :doc:`/specific-guides/media/transport_adapter` — wraps the RTP
  transport so application code can intercept or rewrite packets
  *after* encoding (network-side). A different problem space:
  these are encoded RTP payloads, not raw PCM frames.


PJSUA-LIB / PJMEDIA equivalents
-------------------------------

+------------------------------------------------------+----------------------------------------------------+
| PJSUA2                                               | PJSUA-LIB / PJMEDIA                                |
+======================================================+====================================================+
| ``AudioMediaPort`` subclass with                     | custom ``pjmedia_port`` + ``pjsua_conf_add_port``  |
| ``onFrameRequested`` / ``onFrameReceived``           |                                                    |
+------------------------------------------------------+----------------------------------------------------+
| ``AudioMediaPort::createPort(name, fmt)``            | ``pjmedia_port_info_init`` + assign ``put_frame``  |
|                                                      | / ``get_frame`` function pointers                  |
+------------------------------------------------------+----------------------------------------------------+
| ``MediaFrame`` (``type`` / ``buf`` / ``size``)       | :cpp:any:`pjmedia_frame`                           |
+------------------------------------------------------+----------------------------------------------------+
| (no PJSUA2 equivalent)                               | ``pjsua_media_config::on_aud_prev_rec_frame`` /    |
|                                                      | ``on_aud_prev_play_frame``                         |
+------------------------------------------------------+----------------------------------------------------+
| (no PJSUA2 equivalent)                               | :cpp:any:`pjmedia_aud_stream_create` (no SIP)      |
+------------------------------------------------------+----------------------------------------------------+

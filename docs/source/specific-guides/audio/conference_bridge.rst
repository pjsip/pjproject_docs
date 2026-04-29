.. _guide_audio_conf:

Audio Conference Bridge
========================

.. contents:: Table of Contents
   :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

The audio conference bridge is the routing fabric that PJMEDIA uses to
move audio frames between sources (capture devices, call decoders,
file players, AI media ports) and sinks (speakers, call encoders, file
recorders). Every audio media object registers as a *port*; the
application connects sources to sinks to make audio flow. A single
bridge instance is created by the library at initialisation; the
application registers and connects ports through it.

In PJSUA2 each bridge port is wrapped as a :cpp:any:`pj::AudioMedia`
that knows its slot ID and exposes ``startTransmit()`` /
``stopTransmit()`` for connecting flows. Subclasses
(:cpp:any:`pj::AudioMediaPlayer`, :cpp:any:`pj::AudioMediaRecorder`,
:cpp:any:`pj::AudioMediaPort`, :cpp:any:`pj::AudioMediaAiPort`, etc.)
register their underlying ``pjmedia_port`` automatically.

If the underlying media-flow model (ports, ``get_frame()`` /
``put_frame()``, the master clock that drives the bridge) is
unfamiliar, read :doc:`/specific-guides/media/audio_flow` first —
the rest of this page assumes it.

For the lower-latency, encoded-frame, no-mixing alternative see
:doc:`switchboard`. For the video equivalent see
:doc:`/specific-guides/video/conference`.


Backend selection
-----------------

PJMEDIA ships **three** conference backend implementations, selected
at compile time via :c:macro:`PJMEDIA_CONF_BACKEND`:

+-----------------------------------------------+-------------------------------------------------------+
| Backend (``PJMEDIA_CONF_BACKEND`` value)      | When to use                                           |
+===============================================+=======================================================+
| :c:macro:`PJMEDIA_CONF_SERIAL_BRIDGE_BACKEND` | **Default.** Mixing bridge running on a single        |
| (``1``)                                       | clock thread. Comfortably covers typical SIP-client   |
|                                               | workloads on modern CPUs with common codecs (G.711,   |
|                                               | Opus) — multiple concurrent calls fit easily. The     |
|                                               | per-tick CPU only becomes a bottleneck at large       |
|                                               | participant counts (tens of ports). For benchmark     |
|                                               | numbers see                                           |
|                                               | :doc:`/specific-guides/perf_footprint/pjmedia_mips`.  |
+-----------------------------------------------+-------------------------------------------------------+
| :c:macro:`PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND`| Mixing bridge with multiple worker threads. Intended  |
| (``2``)                                       | for **server-type endpoints** (conference servers,    |
|                                               | SFU/MCU, IVR farms) where a single bridge hosts many  |
|                                               | concurrent participants and the per-tick mixing CPU   |
|                                               | exceeds one core. Typical SIP client apps do not      |
|                                               | need this. Auto-selected when ``PJMEDIA_CONF_THREADS``|
|                                               | is defined.                                           |
+-----------------------------------------------+-------------------------------------------------------+
| :c:macro:`PJMEDIA_CONF_SWITCH_BOARD_BACKEND`  | Drop-in replacement for the bridge that **handles     |
| (``0``)                                       | encoded audio frames** end-to-end (no decode-mix-     |
|                                               | encode cycle), at lower latency and lower footprint.  |
|                                               | The trade-off is no mixing — one source per sink only |
|                                               | — so it doesn't do conferencing. Useful for           |
|                                               | endpoints that need encoded-frame routing (e.g. when  |
|                                               | the audio device emits/consumes encoded frames        |
|                                               | directly) or care about low-latency 1:1 paths.        |
|                                               | Auto-selected when ``PJMEDIA_CONF_USE_SWITCH_BOARD``  |
|                                               | is defined. See :doc:`switchboard` for the full       |
|                                               | feature list.                                         |
+-----------------------------------------------+-------------------------------------------------------+

Default is serial. To pick a different backend, define one input
macro in your ``config_site.h`` — the auto-selection in
``pjmedia/include/pjmedia/config.h`` does the rest:

.. code-block:: c

   #ifndef PJMEDIA_CONF_BACKEND
   #   if defined(PJMEDIA_CONF_USE_SWITCH_BOARD) && PJMEDIA_CONF_USE_SWITCH_BOARD != 0
   #       define PJMEDIA_CONF_BACKEND  PJMEDIA_CONF_SWITCH_BOARD_BACKEND
   #   elif defined(PJMEDIA_CONF_THREADS)
   #       define PJMEDIA_CONF_BACKEND  PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND
   #   else
   #       define PJMEDIA_CONF_BACKEND  PJMEDIA_CONF_SERIAL_BRIDGE_BACKEND
   #   endif
   #endif

Switchboard wins over parallel if both inputs happen to be defined.

.. _enable_parallel_conf_bridge:

For the **parallel** backend, the recommended pattern is to set
``PJMEDIA_CONF_BACKEND`` *explicitly* alongside ``PJMEDIA_CONF_THREADS``,
so the intent is visible at the top of ``config_site.h`` and doesn't
depend on the auto-selection precedence:

.. code-block:: c

   #define PJMEDIA_CONF_BACKEND   PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND
   #define PJMEDIA_CONF_THREADS   4


Worker threads (parallel backend)
---------------------------------

The parallel backend's thread count is set at compile time via
:c:macro:`PJMEDIA_CONF_THREADS` — the **total** number of conference
threads including the get-frame thread. At runtime this maps to
``pjmedia_conf_param::worker_threads`` (= ``PJMEDIA_CONF_THREADS - 1``).
Default ``1`` is the serial bridge; ``2`` or more enables
parallelism. Available since PJSIP 2.16 (:pr:`4241`).

Two simple rules: **don't exceed the host's physical core count**
(mixing is compute-bound; oversubscribing cores burns context
switches), and **don't count hyper-threads as full cores** (the
realistic uplift is smaller than the logical-thread count suggests).

The only published reference point from PR :pr:`4241` is **8 threads
serving 240 concurrent ports without audio-quality degradation** on
the author's test bench; lower values were not measured. For a
concrete sizing procedure see the next section.


Measuring bridge capacity with the MIPS test
--------------------------------------------

The MIPS test is included in the unit-test app ``pjmedia-test`` (see
:doc:`/specific-guides/perf_footprint/pjmedia_mips`), and ships with
ready-made conference-bridge cases. The methodology works for sizing
either backend — choosing ``PJMEDIA_CONF_THREADS`` for parallel, or
answering "how many calls fit on this CPU?" for serial.

Each row reports **Time** in microseconds spent processing **one
second** of audio for that case, giving a simple real-time threshold:

   **If a row's Time exceeds 1 000 000 µs, that workload is already
   over budget for the current backend / thread count.**

(The CPU% column is just ``Time / 10 000`` per the test source, so 1 s
and 100 % are the same threshold.)

Pre-built conference cases:

- ``conference bridge with {1, 2, 4, 8, 16} ports`` — pure mixing,
  no codec / SRTP / resampling.
- ``conf bridge 100 calls - PCMU`` — full G.711 encode/decode at
  whatever ``PJMEDIA_CONF_THREADS`` the binary was built with.
- ``conf bridge 100 calls - PCMU, no parallel`` — same workload on
  the serial path; the diff shows what parallel buys you.
- ``conf bridge 100 calls - Speex`` and SRTP / resample variants.

.. important::

   The canned cases each cover **one** extra cost on top of mixing
   (codec, or SRTP, or resampling). A real call in a real conference
   is rarely just one of these — it commonly stacks *several*:
   codec encode/decode + resampling between port clock rates + SRTP
   encrypt/auth + VAD / silence detection + PLC + any per-stream
   effects. Sizing from the bare PCMU number will under-count.

   Adding a test case that varies **codec, number of participants,
   SRTP, and the parallel/no-parallel toggle** is straightforward —
   each is already a parameter to ``init_conf_call()`` in
   ``mips_test.c``; copy one of the existing ``conf100_*_test_init``
   wrappers and change the arguments. Resampling rides along
   automatically when the bridge clock rate differs from the
   codec's. Switching VAD / silence detection / PLC / per-stream
   effects on or off is **not** exposed through ``init_conf_call``
   and needs deeper modifications to the function or to the
   endpoint defaults — pick the canned case closest to your worst
   per-call cost when those features dominate.

Procedure:

1. Tune ``mips_test.c`` for your conditions — codec, call count, etc.
2. Build ``pjmedia-test`` with the backend you want to size
   (``PJMEDIA_CONF_THREADS`` undefined for serial, set to a candidate
   value for parallel) and run.
3. Read the **Time** column. Time well under 1 s = headroom; crossing
   1 s = either reduce the load or, for parallel, raise
   ``PJMEDIA_CONF_THREADS`` (up to the physical-core ceiling).
4. The configuration that keeps the worst-case Time under 1 s with
   margin is your sizing target.


Asynchronous operations
-----------------------

The audio conference bridge has been **asynchronous since PJSIP 2.15.1**
(:pr:`3928`). The change is the core source of behavioural surprises
when migrating from older versions, so it is worth being explicit
about what changed. (The :doc:`video conference bridge
</specific-guides/video/conference>` made the same transition earlier,
in PJSIP 2.13 via :pr:`3183` — the same async semantics described
below apply there.)

**Queued** (return when the work is queued; mutation runs later on
the clock thread inside ``get_frame()``):
``startTransmit`` / ``stopTransmit``, ``AudioMedia*`` registration /
unregistration through subclass constructors and destructors, and
since :pr:`4916` also :cpp:any:`pjsua_conf_adjust_conn_level`
(routed as ``PJMEDIA_CONF_OP_ADJUST_CONN_LEVEL``).

**Not queued:** the per-port level adjusters
``adjustTxLevel`` / ``adjustRxLevel``
(:cpp:any:`pjsua_conf_adjust_tx_level`,
:cpp:any:`pjsua_conf_adjust_rx_level`) take the bridge mutex briefly
and apply immediately.

Three concrete classes of bug appear when application code assumes
the queued ops are synchronous:

- **Resource deallocation ordering.** The ``pjmedia_port`` object
  itself is safe — the bridge holds a group-lock reference on each
  added port, so the port stays valid until the clock thread is done
  with it. The race is over **application-side resources attached
  to the port** (buffers, file handles, AI session state): freeing
  them right after ``stopTransmit()`` or ``remove_port`` can run
  ahead of the clock thread that still uses them. See :issue:`4526`.
  The cleanest fix is to register a destroy handler on the port via
  :cpp:any:`pjmedia_port_add_destroy_handler` (:pr:`4244`); the
  handler fires when the bridge's last reference drops, which is the
  correct point to free the attached resources.
- **Fast remove-after-add (no-clock case).** When a port is added
  then removed before the clock thread has serviced either op,
  ``remove_port`` runs **synchronously** and frees the slot
  immediately (:pr:`4253`, since 2.16, in response to :issue:`4706`).
  This is the path that lets a bridge with no clock (e.g. when no
  sound device is attached, so no one is pumping ``get_frame()``)
  still drain its slots — without it, slots would fill up and never
  be freed. On older versions (pre-2.16) the slot ID could be reused
  unexpectedly in this scenario; if you target those, wait for the
  add op-completion before queuing the remove.
- **Reading state while ops are pending.** Several read-side
  functions —
  :cpp:any:`pjmedia_conf_get_port_count`,
  :cpp:any:`pjmedia_conf_enum_ports`,
  :cpp:any:`pjmedia_conf_get_port_info`,
  :cpp:any:`pjmedia_conf_get_ports_info` —
  do not synchronise against the op queue. The values they return
  are accurate as of the calling moment, but a concurrent op could
  change them right after. Avoid using them as a barrier; use the
  op-completion callback instead. See :issue:`4496`.

Op-completion callback
----------------------

To know when a queued op has actually taken effect, implement
:cpp:func:`pj::Endpoint::onAudioMediaOpCompleted`:

.. code-block:: c++

   class MyEndpoint : public Endpoint
   {
   public:
       void onAudioMediaOpCompleted(OnAudioMediaOpCompletedParam &prm) override
       {
           if (prm.status != PJ_SUCCESS) {
               // Op failed; log and recover.
               return;
           }
           switch (prm.opType) {
               case PJMEDIA_CONF_OP_ADD_PORT:
                   onPortAdded(prm.opParam.addInfo.mediaId);
                   break;
               case PJMEDIA_CONF_OP_REMOVE_PORT:
                   onPortRemoved(prm.opParam.removeInfo.mediaId);
                   break;
               case PJMEDIA_CONF_OP_CONNECT_PORTS:
                   onConnected(prm.opParam.connectInfo.mediaId,
                               prm.opParam.connectInfo.targetMediaId);
                   break;
               case PJMEDIA_CONF_OP_DISCONNECT_PORTS:
                   onDisconnected(prm.opParam.disconnectInfo.mediaId,
                                  prm.opParam.disconnectInfo.targetMediaId);
                   break;
               default:
                   break;
           }
       }
   };

**Threading.** Callback invocations are serialised by the library —
two never run concurrently. The thread varies, though: the clock
thread for async-path completions, but the **application thread that
called ``remove_port``** for the synchronous fast-path. So the
callback can race against the rest of your code; anything shared
with other threads (e.g. the ``mediaId → AudioMedia*`` map below)
still needs your own mutex. Keep handlers short — post any long or
blocking work to your own thread.

**No clock = no callback.** Op processing runs inside ``get_frame()``,
so a bridge that no one is pumping (no sound device, no master
port) never fires async-path completions. For that topology, rely on
the synchronous fast-path above instead of waiting on a callback.

Available since PJSIP 2.16 (:pr:`4446`).

Mapping ``mediaId`` back to your ``AudioMedia``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The callback only carries the bridge slot ID
(``opParam.addInfo.mediaId`` etc.). Note that not every slot
corresponds to an app-created object — call stream ports, the sound
device, and other library-internal ports also live in the bridge,
and the app never explicitly created an ``AudioMedia`` for them. The
three options below cover both cases.

1. **Application-owned ``mediaId → AudioMedia*`` map** *(app-owned
   ports only)*. Cleanest when you already keep long-lived references
   to your registered media. Doesn't help for library-internal ports
   — the app never has an instance to put into the map for those.
   Guard with a mutex — the op-completion callback can race against
   the application thread:

   .. code-block:: c++

      std::mutex                          mediaMu;
      std::unordered_map<int, AudioMedia*> mediaById;

      // After registering each AudioMedia:
      {
          std::lock_guard<std::mutex> g(mediaMu);
          mediaById[player->getPortId()] = player;
      }

      // In onAudioMediaOpCompleted:
      std::lock_guard<std::mutex> g(mediaMu);
      auto it = mediaById.find(prm.opParam.addInfo.mediaId);
      if (it != mediaById.end()) { /* use it->second */ }

2. **Wrap the slot ID with a thin ``AudioMedia`` subclass** *(works
   for any slot, including library-internal ones)*. The ``id`` field
   of ``AudioMedia`` is protected, so subclasses can set it directly.
   This is the same trick PJSUA2 uses internally (the in-tree
   ``AudioMediaHelper`` in ``pjsip/src/pjsua2/util.hpp`` is *not*
   exposed in public headers — define your own):

   .. code-block:: c++

      class AudioMediaHelper : public AudioMedia {
      public:
          void setPortId(int port_id) { id = port_id; }
      };

      AudioMediaHelper am;
      am.setPortId(prm.opParam.addInfo.mediaId);
      am.startTransmit(...);   // or adjustTxLevel, getPortInfo, etc.

   Useful when you don't already hold the ``AudioMedia`` instance
   for that slot. Caveat: the helper only exposes the **base**
   ``AudioMedia`` interface (``startTransmit``, ``stopTransmit``,
   ``adjustTxLevel`` / ``RxLevel``, ``getPortInfo``, ``getPortId``,
   etc.). It does not give you the originating derived instance, so
   subclass-only methods like ``AudioMediaPlayer::setPos()``,
   ``AudioMediaRecorder::getOption()``, or
   ``AudioMediaPort::onFrameRequested()`` remain out of reach — for
   those you still need a typed pointer via Option 1 or other
   app-side bookkeeping.

3. **Read-only port info via the static lookup** *(any slot)*. If
   you only need the port's name, format, levels, or listener list,
   :cpp:func:`pj::AudioMedia::getPortInfoFromId` returns a
   ``ConfPortInfo`` directly from the slot ID — no map and no
   subclass needed.

A note on multiple bridges
~~~~~~~~~~~~~~~~~~~~~~~~~~

PJSUA-LIB and PJSUA2 are designed around a **single, library-owned
conference bridge**. Creating additional ``pjmedia_conf`` instances
through the PJMEDIA API is generally not recommended — several
PJSUA / PJSUA2 helpers assume the primary bridge and don't behave
correctly against secondary ones. ``onAudioMediaOpCompleted`` is one
such case (see :issue:`4697`); it is wired only to the primary
bridge, so ops on a secondary bridge must use the lower-level
:cpp:any:`pjmedia_conf_op_cb` directly.

If the goal is serving **many concurrent calls or participants**, use
the parallel backend on the single primary bridge (see
:ref:`how to enable the parallel backend <enable_parallel_conf_bridge>`) rather than spinning up multiple
bridges.


Per-port TX / RX state
----------------------

:cpp:any:`pjsua_conf_configure_port` (added in :pr:`4437`) lets
applications change a port's *transmit* and *receive* state at
runtime, without removing it from the bridge:

- ``PJMEDIA_PORT_NO_CHANGE`` — leave the direction untouched.
- ``PJMEDIA_PORT_DISABLE`` — fully disable the direction
  (``get_frame()`` / ``put_frame()`` will not be called for this
  port).
- ``PJMEDIA_PORT_MUTE`` — keep calling the port but discard the
  frame.
- ``PJMEDIA_PORT_ENABLE`` — restore normal operation.

Useful for fine-grained TX/RX gating without re-creating connections.

There is currently **no PJSUA2 wrapper**. C++ PJSUA2 apps can drop to
the PJSUA-LIB call directly:

.. code-block:: c++

   // Get the slot id from your AudioMedia subclass:
   int slot = my_port.getPortId();

   // Mute TX (bridge → port) but leave RX as-is:
   pjsua_conf_configure_port(slot, PJMEDIA_PORT_MUTE, PJMEDIA_PORT_NO_CHANGE);

Apps using PJSUA2 from a SWIG-bound language (Java, C#, Python,
Kotlin, …) have no path to this API at the moment — the SWIG
bindings expose only PJSUA2, not the underlying PJSUA-LIB C API.
Until a PJSUA2 wrapper exists, removing and re-adding the port (or
not transmitting to/from it) is the only application-level
workaround.


Port direction and signature
----------------------------

:pr:`4556` added ``direction`` and ``signature`` fields to
:cpp:any:`pjmedia_conf_port_info` — useful for telling sources from
sinks and identifying which backend a port belongs to. They are
**not surfaced** through ``pjsua_conf_port_info`` or ``ConfPortInfo``;
reading them needs a direct PJMEDIA-level call against the underlying
``pjmedia_conf``, which PJSUA does not expose. Most apps won't need
them.


Common pitfalls
---------------

- **"My port is gone but its resources are still in use."** App freed
  buffers right after ``stopTransmit`` / port removal; the clock
  thread hadn't processed the op yet. Wait for
  ``onAudioMediaOpCompleted`` (or use ``pjmedia_port_add_destroy_handler``)
  before freeing.
- **"`getPortInfo()` shows a port I just removed."** Read-side port-
  info APIs don't synchronise against the op queue; use the
  op-completion callback as the barrier.
- **"I added then removed a player and got a different port back at
  the same slot."** Pre-2.16 issue; resolved on 2.16+ by :pr:`4253`'s
  synchronous fast-path (including the no-clock case).
- **"My op-completion callback never fires."** Op processing runs
  inside ``get_frame()``. If nothing is pumping the bridge (no sound
  device, no master port), async ops sit forever. Use the
  synchronous fast-path above.
- **"`onAudioMediaOpCompleted` doesn't fire for my second bridge."**
  Multiple bridges aren't a supported PJSUA-LIB / PJSUA2 pattern;
  only the primary bridge is wired. For scaling to many concurrent
  calls, use the parallel backend instead
  (:ref:`how to enable the parallel backend <enable_parallel_conf_bridge>`).
- **"My conference server is bottlenecked on one CPU."** Serial
  backend hitting its single-tick budget. Switch to the parallel
  backend (:ref:`how to enable the parallel backend <enable_parallel_conf_bridge>`). Client apps almost
  never need this.


PJSUA-LIB equivalents
---------------------

+------------------------------------------------------+--------------------------------------------------------+
| PJSUA2                                               | PJSUA-LIB                                              |
+======================================================+========================================================+
| ``AudioMedia`` (slot wrapper)                        | :cpp:any:`pjsua_conf_port_id` (raw slot ID)            |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::AudioMedia::getPortId()`              | (the slot ID is the value itself)                      |
+------------------------------------------------------+--------------------------------------------------------+
| ``AudioMedia::startTransmit(sink)``                  | :cpp:any:`pjsua_conf_connect()` /                      |
|                                                      | :cpp:any:`pjsua_conf_connect2()`                       |
+------------------------------------------------------+--------------------------------------------------------+
| ``AudioMedia::stopTransmit(sink)``                   | :cpp:any:`pjsua_conf_disconnect()`                     |
+------------------------------------------------------+--------------------------------------------------------+
| ``AudioMedia::adjustTxLevel()`` /                    | :cpp:any:`pjsua_conf_adjust_tx_level()` /              |
| ``adjustRxLevel()``                                  | :cpp:any:`pjsua_conf_adjust_rx_level()`                |
+------------------------------------------------------+--------------------------------------------------------+
| no PJSUA2 wrapper — C++ apps can call PJSUA-LIB      | :cpp:any:`pjsua_conf_adjust_conn_level()`              |
| directly; SWIG-bound languages (Java/C#/Python/…)    |                                                        |
| have no path                                         |                                                        |
+------------------------------------------------------+--------------------------------------------------------+
| no PJSUA2 wrapper — C++ apps can call PJSUA-LIB      | :cpp:any:`pjsua_conf_configure_port()`                 |
| directly; SWIG-bound languages (Java/C#/Python/…)    |                                                        |
| have no path                                         |                                                        |
+------------------------------------------------------+--------------------------------------------------------+
| ``ConfPortInfo`` from                                | :cpp:any:`pjsua_conf_port_info` from                   |
| ``AudioMedia::getPortInfo()``                        | :cpp:any:`pjsua_conf_get_port_info()`                  |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Endpoint::onAudioMediaOpCompleted()`  | :cpp:any:`pjsua_callback::on_conf_op_completed`        |
+------------------------------------------------------+--------------------------------------------------------+

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

The terms **clock thread** and **get-frame thread** are used
interchangeably below. Both refer to the upstream thread that pumps
the bridge by calling ``get_frame()`` on it — typically the master
port (slot 0), e.g. the sound device port driving the bridge.

For the lower-latency, encoded-frame, no-mixing alternative see
:doc:`switchboard`. For the video equivalent see
:doc:`/specific-guides/video/conference`.


Backend selection
-----------------

PJMEDIA ships **three** conference backend implementations, selected
at compile time via :c:macro:`PJMEDIA_CONF_BACKEND`:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Backend (``PJMEDIA_CONF_BACKEND`` value)
     - When to use
   * - :c:macro:`PJMEDIA_CONF_SERIAL_BRIDGE_BACKEND` (``1``)
     - **Default.** Mixing bridge running on a single clock
       thread. Comfortably covers typical SIP-client workloads on
       modern CPUs with common codecs (G.711, Opus) — multiple
       concurrent calls fit easily. The per-tick CPU only becomes
       a bottleneck at large participant counts (tens of ports).
       For benchmark numbers see
       :doc:`/specific-guides/perf_footprint/pjmedia_mips`.
   * - :c:macro:`PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND` (``2``)
     - Mixing bridge with multiple worker threads. Intended for
       **server-type endpoints** (conference servers, SFU/MCU,
       IVR farms) where a single bridge hosts many concurrent
       participants and the per-tick mixing CPU exceeds one core.
       Typical SIP client apps do not need this. Auto-selected
       when ``PJMEDIA_CONF_THREADS`` is defined.
   * - :c:macro:`PJMEDIA_CONF_SWITCH_BOARD_BACKEND` (``0``)
     - Drop-in replacement for the bridge that **handles encoded
       audio frames** end-to-end (no decode-mix-encode cycle), at
       lower latency and lower footprint. The trade-off is no
       mixing — one source per sink only — so it doesn't do
       conferencing. Useful for endpoints that need encoded-frame
       routing (e.g. when the audio device emits/consumes encoded
       frames directly) or care about low-latency 1:1 paths.
       Auto-selected when ``PJMEDIA_CONF_USE_SWITCH_BOARD`` is
       defined. See :doc:`switchboard` for the full feature list.

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
``PJMEDIA_CONF_BACKEND`` *explicitly* alongside ``PJMEDIA_CONF_THREADS``
in ``config_site.h``, so the intent is visible at the top of the
file and doesn't depend on the auto-selection precedence:

.. code-block:: c

   #define PJMEDIA_CONF_BACKEND   PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND
   #define PJMEDIA_CONF_THREADS   4

The *backend* choice is compile-time only, but the *thread count*
can also be overridden at runtime — at any API level (PJSUA2,
PJSUA-LIB, or PJMEDIA). See *Worker threads* below for the
field names.


Worker threads (parallel backend)
---------------------------------

The parallel backend's thread count is the **total** number of
conference threads including the get-frame thread, set in two places:

- **Compile time** — :c:macro:`PJMEDIA_CONF_THREADS` in
  ``config_site.h`` is the default value baked into the binary.
- **Runtime** — three equivalent fields, one per API level. Each
  forwards into the next, and each defaults to the compile-time
  ``PJMEDIA_CONF_THREADS`` value if not set:

  - PJSUA2 — :cpp:any:`pj::MediaConfig::confThreads` inside
    :cpp:any:`pj::EpConfig::medConfig`.
  - PJSUA-LIB — :cpp:any:`pjsua_media_config::conf_threads` in the
    ``pjsua_media_config`` passed to :cpp:any:`pjsua_init`.
  - PJMEDIA — :cpp:any:`pjmedia_conf_param::worker_threads` passed
    to :cpp:any:`pjmedia_conf_create2()`. Apps that drive PJMEDIA
    directly (no PJSUA-LIB / PJSUA2) use this. Note this field is
    *worker* threads, i.e. ``conf_threads - 1`` (excludes the
    get-frame thread).

  The runtime field is only honoured when the parallel backend has
  been compiled in
  (``PJMEDIA_CONF_BACKEND == PJMEDIA_CONF_PARALLEL_BRIDGE_BACKEND``)
  — backend choice itself remains compile-time.

Note that the *serial backend* is selected only when
``PJMEDIA_CONF_THREADS`` is **undefined** at compile time; defining
it (even as ``1``) selects the *parallel* backend per the
auto-selection logic above — ``1`` then means "parallel backend
with no extra workers" rather than the serial backend. Available
since PJSIP 2.16 (:pr:`4241`).

Two simple rules: **don't exceed the host's physical core count**
(mixing is compute-bound; oversubscribing cores burns context
switches), and **don't count hyper-threads as full cores** (the
realistic uplift is smaller than the logical-thread count suggests).

**Thread priority asymmetry.** Only the get-frame thread *attempts*
to run at elevated priority — ``pjmedia_clock`` calls
``pj_thread_set_prio`` to the OS maximum, and sound-device threads
typically get OS-level audio priority. The parallel-backend pool
workers, by contrast, are created with default priority and no
priority bump.

The bump itself can silently fail. On Linux, raising thread
priority beyond default requires ``CAP_SYS_NICE`` (effectively root
or a matching rlimit configuration); without it,
``pj_thread_set_prio`` returns an error that PJMEDIA logs at debug
level but otherwise ignores — the clock thread keeps running at
default priority. Comparable restrictions apply on other OSes.

The bump can be disabled at the PJMEDIA level via the
``PJMEDIA_CLOCK_NO_HIGHEST_PRIO`` flag on
:cpp:any:`pjmedia_clock_create2()`, but **PJSUA-LIB / PJSUA2 do not
expose this flag** for the bridge's clock — both the real
``pjmedia_snd_port`` and the null-sound-device master port set up
their internal clock with ``options = 0``. Disabling it from a
PJSUA app would require either patching the library or driving
PJMEDIA directly.

Net effect on a typical non-root server deployment: nothing runs at
elevated priority anyway. On a heavily loaded host the pool workers
(and the clock thread when its bump didn't take) can be preempted
by other application threads. Size with margin if the deployment is
CPU-tight.

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
   ``init_conf_call()`` calls :cpp:any:`pjmedia_conf_create2()` with
   an explicit ``worker_threads`` value, so changing the thread
   count is just a one-line edit there; no rebuild against a
   different ``PJMEDIA_CONF_THREADS`` is needed (the parallel
   backend itself does still need to be compiled in).
2. Build ``pjmedia-test`` (with parallel compiled in if you want to
   measure parallel) and run.
3. Read the **Time** column. Time well under 1 s = headroom; crossing
   1 s = either reduce the load or raise ``worker_threads`` (up to
   the physical-core ceiling).
4. The configuration that keeps the worst-case Time under 1 s with
   margin is your sizing target. In your real PJSUA-LIB / PJSUA2 app,
   apply that count via the runtime ``confThreads`` /
   ``conf_threads`` field — same underlying ``worker_threads`` knob,
   just one API level up.


.. _asynchronous_operations:

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
  them right after ``stopTransmit()`` or
  :cpp:any:`pjmedia_conf_remove_port` can run ahead of the clock
  thread that still uses them. See :issue:`4526`.
  The cleanest fix is to register a destroy handler on the port via
  :cpp:any:`pjmedia_port_add_destroy_handler` (:pr:`4244`); the
  handler fires when the bridge's last reference drops, which is the
  correct point to free the attached resources. For ports the
  application creates itself, the full pool / group-lock contract
  is in :ref:`custom_port_lifecycle` below.
- **Fast remove-after-add (no-clock case).** When a port is added
  then removed before the clock thread has serviced either op,
  :cpp:any:`pjmedia_conf_remove_port` runs **synchronously** and
  frees the slot
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
called the remove API** (:cpp:any:`pjmedia_conf_remove_port` or its
PJSUA-LIB / PJSUA2 wrappers) for the synchronous fast-path. So the
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
   ``adjustTxLevel`` / ``adjustRxLevel``, ``getPortInfo``, ``getPortId``,
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


.. _custom_port_lifecycle:

Custom port lifecycle
---------------------

.. important::

   **Backward-compatibility considerations when upgrading from
   PJSIP < 2.15.1.** Before :pr:`3928`, bridge port operations
   were synchronous: freeing a custom port's pool right after
   ``pjmedia_conf_remove_port`` was safe because the removal had
   already completed when the call returned. From 2.15.1 onwards
   removals are queued in the common case (with a synchronous
   fast-path exception covered in :ref:`asynchronous_operations`
   above), so any custom port that doesn't already follow one of
   the patterns below is at risk of an access-after-free crash on
   the clock thread. If you maintain a custom ``pjmedia_port``,
   audit it against this section.

For most existing ports the migration fix is small: have the
port create and own its own pool inside the port-creation
function (using the application-supplied pool's factory), and
release that pool from ``on_destroy``:

.. code-block:: c

   /* In the port-creation function: */
   pj_pool_t *own_pool = pj_pool_create(app_pool->factory,
                                        "myport", 1000, 1000, NULL);
   /* ... allocate the port struct in own_pool, stash own_pool
    * inside it, set on_destroy ... */

   /* And release the pool from on_destroy: */
   static pj_status_t my_port_on_destroy(pjmedia_port *this_port)
   {
       struct my_port *p = (struct my_port *)this_port;
       pj_pool_safe_release(&p->pool);
       return PJ_SUCCESS;
   }

That's the whole change for most ports — the bridge auto-creates
the group lock and the destroy chain handles the timing. The
patterns below cover when this minimum is enough, when a port
also needs to manage its own group lock, and the alternative
when the port doesn't own a pool at all.

Applications that supply their own ``pjmedia_port`` (rather than
the bundled file player / recorder, AI port, or tone generator)
need to respect the same async-removal contract as the
library-side ports. The bridge holds a group-lock reference on
every added port and only drops it when the queued remove op
runs on the clock thread (typical case) — so the port struct,
the pool it lives in, and any attached resources must outlive
that reference, even though the calling thread sees
``pjmedia_conf_remove_port`` return immediately.

Two main shapes:

**Pattern 1 — port has its own pool.** The port struct lives in
a pool the port itself owns, and the pool must be released from
inside the group-lock destroy chain (so it survives the bridge's
queued remove). Two sub-cases depending on who creates the group
lock:

*Pattern 1a — port also owns a group lock.* The port creator
calls :cpp:any:`pjmedia_port_init_grp_lock`, which populates
``port->grp_lock``, registers an internal handler that will
invoke ``port->on_destroy`` when the lock destroys, and takes
an implicit reference on the lock (so the port itself holds
one). The pool is released from ``on_destroy``, or equivalently
from a handler added via
:cpp:any:`pjmedia_port_add_destroy_handler` — both run from the
same destroy chain. The port-creation function:

.. code-block:: c

   /* Internal: the port struct, allocated inside its own pool. */
   struct my_port {
       pjmedia_port  base;
       pj_pool_t    *pool;
       /* ... attached resources (buffers, file handles, etc.) ... */
   };

   static pj_status_t my_port_on_destroy(pjmedia_port *this_port)
   {
       struct my_port *p = (struct my_port *)this_port;
       /* tear down attached resources first... */
       pj_pool_safe_release(&p->pool);
       return PJ_SUCCESS;
   }

   /* Public: create a new port and return it to the caller. */
   pj_status_t my_port_create(pjmedia_endpt *endpt,
                              /* ... */,
                              pjmedia_port **p_port)
   {
       pj_pool_t *pool = pjmedia_endpt_create_pool(endpt, "myport",
                                                   1000, 1000);
       struct my_port *p = PJ_POOL_ZALLOC_T(pool, struct my_port);
       p->pool = pool;

       pjmedia_port_info_init(&p->base.info, /* ... */);
       p->base.get_frame  = &my_get_frame;
       p->base.put_frame  = &my_put_frame;
       p->base.on_destroy = &my_port_on_destroy;

       /* Populates p->base.grp_lock; registers the destroy chain
        * that will invoke on_destroy when the lock destroys;
        * implicit add_ref — the port now holds one reference. */
       pjmedia_port_init_grp_lock(&p->base, pool, NULL);

       *p_port = &p->base;
       return PJ_SUCCESS;
   }

The application then creates the port and adds it to the bridge.
The bridge takes its own reference on the same group lock:

.. code-block:: c

   pjmedia_port *port;
   my_port_create(endpt, /* ... */, &port);

   /* `parent_pool` is any long-lived pool the app already has;
    * the bridge uses it only to allocate its own conf_port slot
    * data. The port's *own* pool (created inside
    * my_port_create) is separate and lives until the destroy
    * chain releases it. */
   pjmedia_conf_add_port(conf, parent_pool, port, NULL, &slot);

To remove and destroy, queue the bridge removal *and* drop the
port's own reference. Order doesn't matter — whichever
``dec_ref`` runs last triggers the destroy chain:

.. code-block:: c

   pjmedia_conf_remove_port(conf, slot);  /* queues bridge dec_ref */
   pjmedia_port_destroy(port);            /* drops the port's own ref */
   /* DO NOT touch port or its pool from here on. */

:cpp:any:`pjmedia_port_destroy` routes to ``dec_ref`` when a
group lock is present, so calling it is safe even with the
bridge's queued op still outstanding. Pool release happens
later, on whichever thread drops the final reference (usually
the clock thread when the bridge services its queued remove).
This is the shape :source:`pjmedia/src/pjmedia/ai_port.c`
follows.

*Pattern 1b — port has no group lock.* The port doesn't call
``init_grp_lock`` itself; the bridge sees ``port->grp_lock ==
NULL`` at add time and creates one internally (verified at
``pjmedia/src/pjmedia/conference.c``, the add-port path:
``pjmedia_port_init_grp_lock(port, conf_pool, NULL)`` followed by
``pj_grp_lock_add_ref``). The same internal handler that invokes
``port->on_destroy`` is registered as part of that
``init_grp_lock`` call, so the destroy chain still runs through
the port's own cleanup. A port that just sets
``on_destroy = ...`` and leaves the group-lock setup to the
bridge is also crash-safe — provided the application doesn't
free the port's pool from outside ``on_destroy``. This is the
shape :source:`pjmedia/src/pjmedia/wav_player.c` follows.

The reference math is the same as Pattern 1a: the bridge's
``init_grp_lock`` takes one implicit reference and its
``add_ref`` adds another, leaving two outstanding. The bridge
drops one when the queued remove runs; the application must
call :cpp:any:`pjmedia_port_destroy` (or
:cpp:any:`pjmedia_port_dec_ref`) after
``pjmedia_conf_remove_port`` to drop the second, otherwise the
destroy chain never fires and the pool leaks. PJSUA-LIB's
own port teardown follows this pairing — see
``pjsua_aud.c:522`` (remove) / ``:562`` (destroy) for the
reference pattern.

.. note::

   ``pjmedia_port_init_grp_lock`` logs a level-2 warning when a
   port is registered without an ``on_destroy`` callback (see
   :source:`pjmedia/src/pjmedia/port.c`) — a useful tripwire for
   ports that own a pool but forgot the cleanup hook.

**Pattern 2 — port has no own pool.** The port struct lives in
a pool owned by a wider scope (a dialog pool, an account pool,
the application's main pool). The constraint is simpler but
strict: **the pool's lifetime must extend beyond the port's
lifetime in the bridge.** Concretely, don't tear down the parent
scope until the bridge has finished servicing its queued
remove for the port — otherwise the bridge dereferences memory
inside an already-released pool.

If the parent scope is naturally long-lived (an account that
outlives all its calls, a dialog that outlives its media
streams), this is automatic. If the parent scope might be torn
down close to the port's removal, gate the parent teardown on a
:cpp:any:`pjmedia_port_add_destroy_handler` callback so you
know the bridge has released the port before you release the
pool.

The risk in any pattern is the same: if the port's pool (or the
parent pool in Pattern 2) is released before the bridge has
finished servicing its queued remove, the clock thread reads
freed memory — typically crashing inside ``conference.c``,
``stream.c``, or ``port.c``. The canonical built-in ports
(``ai_port.c`` for Pattern 1a, ``wav_player.c`` for Pattern 1b)
are crash-safe out of the box; custom variants that strip out
the group lock, no-op the ``on_destroy``, or free the pool from
the application thread lose that safety net.

PJSUA-LIB applications that substitute or wrap the default
audio stream port for a call (via
:cpp:any:`pjsua_callback::on_stream_created` /
:cpp:any:`pjsua_callback::on_stream_created2`) face an extra
constraint when the substituted port keeps a reference to the
precreated audio stream port. The contract above still applies,
plus the inner stream port must be pinned through its group
lock — see :ref:`guide_audio_custom_audio_stream_port`.


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

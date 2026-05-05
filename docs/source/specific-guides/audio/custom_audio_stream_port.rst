.. _guide_audio_custom_audio_stream_port:

Customizing the Audio Stream Port
=================================

.. contents:: Table of Contents
   :depth: 2

Introduction
------------

When PJSUA-LIB sets up the audio media for a call, it creates
an :any:`audio stream </api/generated/pjmedia/group/group__PJMED__STRM>`
(:cpp:any:`pjmedia_stream`, which carries RTP/RTCP and the
codec) and adds the **audio stream port** — the
:cpp:any:`pjmedia_port` returned by
:cpp:any:`pjmedia_stream_get_port` — to the conference bridge
so that the call can be mixed with other ports (sound device,
file players, recorders, other calls).

Applications can intercept that wiring through the
:cpp:any:`pjsua_callback::on_stream_created` /
:cpp:any:`pjsua_callback::on_stream_created2` callback and
return a different :cpp:any:`pjmedia_port` to be registered to
the bridge instead of the default audio stream port. Typical
reasons to do this:

- insert a DSP / processing port (AEC variant, AGC, custom
  resampler) between the bridge and the stream,
- bridge to a non-PJMEDIA media source/sink (for example a
  hardware codec, file system, or custom capture),
- inject a tap (recorder/forker) on the call media path,
- substitute a fully synthetic source (test tone, AI port,
  prerecorded prompt) for a leg.

The substituted port falls into one of two shapes:

- **Pattern A — wraps the precreated stream port.** The
  application's port keeps a pointer to the original stream port
  as its downstream and forwards (or transforms) frames to/from
  it. Conference ↔ wrapper ↔ stream ↔ network.
- **Pattern B — does not use the precreated stream port.** The
  application's port is a self-contained source / sink (or
  bridges to its own media stack). The pjsua-created stream
  still exists and is still destroyed by pjsua at call
  teardown, but no conference frames flow through it via this
  slot.

Both patterns share the bridge-side custom-port lifecycle
contract documented in :ref:`custom_port_lifecycle` (own pool,
``on_destroy``, group-lock-aware teardown). The key extra
consideration in Pattern A is keeping the inner stream port
alive for as long as the wrapper references it.

The PJSUA call-teardown sequence
--------------------------------

The audio media is torn down in :source:`pjsip/src/pjsua-lib/pjsua_aud.c`,
in ``stop_media_session`` (around line 520). The relevant
sequence (with the substituted custom port called
``media_port`` and the precreated stream called ``strm``):

.. code-block:: c

   /* Step 1: queue bridge removal of media_port. */
   pjsua_conf_remove_port(call_med->strm.a.conf_slot);   /* ~:522 */

   /* Step 2: notify the application. */
   pjsua_var.ua_cfg.cb.on_stream_destroyed(...);         /* ~:550 */

   /* Step 3: if the application asked PJSUA to own the
    *         substituted port and it differs from the
    *         stream's own port, pjmedia_port_destroy() it.
    */
   pjmedia_port *stream_port;
   pjmedia_stream_get_port(call_med->strm.a.stream, &stream_port);
   if (call_med->strm.a.destroy_port &&
       call_med->strm.a.media_port != stream_port)
   {
       pjmedia_port_destroy(call_med->strm.a.media_port);  /* ~:562 */
   }

   /* Step 4: always destroy the stream. */
   pjmedia_stream_destroy(strm);                          /* ~:567 */

Two non-obvious facts about this sequence shape the rest of
the document:

- **Step 1 is asynchronous in the common case.** The bridge
  queues the remove for its clock thread (see
  :ref:`asynchronous_operations`); ``pjsua_conf_remove_port``
  returns immediately, *before* the bridge has actually
  released its reference on the port.
- **Step 4 is unconditional and may free the stream's port
  immediately.** PJSUA does not destroy the stream's port
  directly — the port shares the stream's group lock (set
  during ``pjmedia_stream_create``), and
  :cpp:any:`pjmedia_stream_destroy` simply drops the stream's
  group-lock reference. If nothing else holds a reference,
  the stream's port is freed there and then, on the calling
  thread, while step 1's bridge remove is still queued.

Pattern A — wrapping the precreated stream port
-----------------------------------------------

When the substituted port keeps the original stream port as its
downstream, the wrapper holds a raw ``pjmedia_port*`` pointer
across the call lifetime. The bridge's queued remove and the
unconditional ``pjmedia_stream_destroy`` together create a
window in which the wrapper can outlive the inner port — that
is the bug to design against.

The bug pattern
~~~~~~~~~~~~~~~

Without explicit pinning, the teardown sequence above unwinds
like this:

1. **Step 1** queues the bridge remove. The wrapper is still
   in the bridge.
2. **Step 4** runs ``pjmedia_stream_destroy`` on the calling
   thread. Nothing else references the stream's group lock,
   so the refcount drops to zero, the stream's destroy chain
   fires, and the inner stream port is freed.
3. **One or more clock ticks later**, the bridge processes
   the queued remove. Before it does, it makes another pass
   of ``get_frame()`` / ``put_frame()`` on the ports it still
   holds — including the wrapper. The wrapper dereferences
   its (now freed) ``downstream`` pointer.

Symptoms in the log: a "Stream destroyed" line interleaved
between bridge-side ``read_port`` / ``get_frame`` traces, and
use-after-free reports inside ``conference.c`` or inside the
wrapper's ``get_frame``. The bridge's own removal state
machine cannot prevent this — by the time the
``conf_port->removing`` flag is checked, the inner port may
already be gone.

The fix: pin the inner stream port via group lock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The stream's port has a group lock (the stream sets
``port.grp_lock = stream->grp_lock`` during creation), so the
wrapper can use the standard PJLIB session-management primitive
to keep it alive:

- Take a reference at wrapper construction:
  :cpp:any:`pj_grp_lock_add_ref` ``(downstream->grp_lock)``.
- Drop that reference from the wrapper's ``on_destroy``:
  :cpp:any:`pj_grp_lock_dec_ref` ``(downstream->grp_lock)``.

The wrapper itself follows :ref:`custom_port_lifecycle`
Pattern 1 — has its own pool, sets ``on_destroy``, and either
calls :cpp:any:`pjmedia_port_init_grp_lock` itself
(Pattern 1a) or lets the bridge auto-create the group lock at
add-port time (Pattern 1b).

Reference math
~~~~~~~~~~~~~~

Two group locks are involved — the wrapper's and the stream's
— and three actors take references on them:

- the **stream itself**, when ``pjmedia_stream_create`` runs
  (released by ``pjmedia_stream_destroy``);
- the **wrapper itself**, when ``pjmedia_port_init_grp_lock``
  runs in the wrapper's create function (released by
  ``pjmedia_port_destroy`` on the wrapper);
- the **bridge**, when ``pjmedia_conf_add_port`` runs (released
  asynchronously when the bridge services the queued remove);

plus, in Pattern A, the **wrapper's pin on the stream** added
explicitly at construction (released from the wrapper's
``on_destroy``).

For Pattern A with a Pattern-1a-style wrapper:

.. list-table::
   :header-rows: 1
   :widths: 50 25 25

   * - Step
     - wrapper ref
     - stream ref
   * - stream is created (pjsua)
     - —
     - 1 (stream itself)
   * - wrapper is constructed; pins stream
     - 1 (wrapper itself)
     - 2 (+pin)
   * - bridge add-port (``pjmedia_conf_add_port``)
     - 2 (+bridge)
     - 2
   * - app calls ``pjsua_conf_remove_port`` (queued)
     - 2
     - 2
   * - PJSUA calls ``pjmedia_port_destroy(wrapper)``
     - 1 (–wrapper itself)
     - 2
   * - PJSUA calls ``pjmedia_stream_destroy(strm)``
     - 1
     - 1 (–stream itself)
   * - clock tick: bridge services the queued remove
     - 0 → wrapper destroy chain → ``on_destroy`` → ``dec_ref`` on stream
     - 0 → stream destroy chain runs

At no point is the wrapper accessed after the inner stream port
has been freed.

For Pattern A with a Pattern-1b-style wrapper (no group lock of
its own), the picture is the same — the bridge auto-creates a
group lock at add-port time, takes the same two references, and
the destroy chain still routes through the wrapper's
``on_destroy``.

Worked example
~~~~~~~~~~~~~~

Skeleton of a wrapping port that adds a DSP step on each frame.
This shows only the parts that differ from a vanilla custom
port — the pool / group lock / ``init_grp_lock`` boilerplate is
exactly as in :ref:`custom_port_lifecycle` Pattern 1.

.. code-block:: c

   struct dsp_wrapper {
       pjmedia_port    base;
       pj_pool_t      *pool;        /* wrapper's own pool */
       pjmedia_port   *downstream;  /* pjsua's stream port */
       /* ... DSP state ... */
   };

   static pj_status_t dsp_get_frame(pjmedia_port *this_port,
                                    pjmedia_frame *frame)
   {
       struct dsp_wrapper *w = (struct dsp_wrapper *)this_port;
       pj_status_t status = pjmedia_port_get_frame(w->downstream, frame);
       if (status == PJ_SUCCESS && frame->type == PJMEDIA_FRAME_TYPE_AUDIO)
           dsp_process(w, frame);   /* in-place transform */
       return status;
   }

   static pj_status_t dsp_put_frame(pjmedia_port *this_port,
                                    pjmedia_frame *frame)
   {
       struct dsp_wrapper *w = (struct dsp_wrapper *)this_port;
       /* dsp_process(w, frame); -- if also processing playback */
       return pjmedia_port_put_frame(w->downstream, frame);
   }

   static pj_status_t dsp_on_destroy(pjmedia_port *this_port)
   {
       struct dsp_wrapper *w = (struct dsp_wrapper *)this_port;
       /* Drop the reference we took on the inner stream port. */
       if (w->downstream && w->downstream->grp_lock)
           pj_grp_lock_dec_ref(w->downstream->grp_lock);
       /* ... tear down DSP state ... */
       pj_pool_safe_release(&w->pool);
       return PJ_SUCCESS;
   }

   pj_status_t dsp_wrapper_create(pjmedia_endpt *endpt,
                                  pjmedia_port *downstream,
                                  pjmedia_port **p_port)
   {
       pj_pool_t *pool = pjmedia_endpt_create_pool(endpt, "dspwrap",
                                                   1000, 1000);
       struct dsp_wrapper *w = PJ_POOL_ZALLOC_T(pool, struct dsp_wrapper);
       w->pool = pool;
       w->downstream = downstream;

       pjmedia_port_info_init(&w->base.info, /* ... copy from downstream ... */);
       w->base.get_frame  = &dsp_get_frame;
       w->base.put_frame  = &dsp_put_frame;
       w->base.on_destroy = &dsp_on_destroy;

       /* Pin the inner stream port for as long as the wrapper exists. */
       if (downstream && downstream->grp_lock)
           pj_grp_lock_add_ref(downstream->grp_lock);

       /* Pattern 1a: register a group lock on the wrapper.
        * Omit this for Pattern 1b — the bridge will auto-create one.
        */
       pjmedia_port_init_grp_lock(&w->base, pool, NULL);

       *p_port = &w->base;
       return PJ_SUCCESS;
   }

Hooked up from the callback:

.. code-block:: c

   static void on_stream_created2(pjsua_call_id call_id,
                                  pjsua_on_stream_created_param *param)
   {
       pjmedia_port *wrapper;
       dsp_wrapper_create(pjsua_var.med_endpt, param->port, &wrapper);

       /* Replace the port being added to the bridge. */
       param->port         = wrapper;
       /* Ask PJSUA to call pjmedia_port_destroy(wrapper) at
        * teardown — this drops the wrapper's own ref so the
        * destroy chain can complete.
        */
       param->destroy_port = PJ_TRUE;
   }

Pattern B — replacing the precreated stream port
-------------------------------------------------

When the substituted port doesn't reference the precreated
stream port, lifecycle is simpler: there is no cross-object
reference to manage, so the standard custom-port lifecycle
(:ref:`custom_port_lifecycle`) is sufficient.

What still happens behind the scenes:

- pjsua's stream is still created. RTP/RTCP socket handling,
  codec instance, jitter buffer — all live as usual.
- The bridge is wired to your custom port instead of the
  stream port. Frames flow:
  ``conference ↔ your custom port ↔ wherever you decide``.
- At call teardown pjsua still calls
  ``pjmedia_stream_destroy(strm)`` (step 4 above). Because
  nothing else references the stream's group lock, it is
  destroyed cleanly at that point.

Common reasons to use Pattern B:

- The media is supplied by another stack (third-party codec
  library, hardware DSP) and the pjsua-created stream is
  redundant — your custom port pumps frames in/out through that
  stack. The pjsua stream and its RTP transport may still be
  useful for negotiation, RTCP, ICE, SRTP; keep an eye on
  duplicated network paths if your stack also speaks RTP.
- The leg is fully synthetic for the duration: a recorded
  prompt port, an AI port (:cpp:any:`pjmedia_ai_port_create`),
  a tone generator, a test source.

Worked example: dropping in an AI port. ``pjmedia_ai_port_create``
returns a :cpp:any:`pjmedia_ai_port`; obtain the underlying
:cpp:any:`pjmedia_port` with
:cpp:any:`pjmedia_ai_port_get_port` and substitute that into
``param->port``:

.. code-block:: c

   static void on_stream_created2(pjsua_call_id call_id,
                                  pjsua_on_stream_created_param *param)
   {
       pjmedia_ai_port *ai_port;
       pjmedia_port *port;

       pjmedia_ai_port_create(pjsua_var.pool, /* cfg */ ..., &ai_port);
       port = pjmedia_ai_port_get_port(ai_port);

       param->port         = port;
       param->destroy_port = PJ_TRUE;
   }

The AI port manages its own pool and group lock, while pjsua owns
the substituted ``pjmedia_port`` in ``param->port``. At call
teardown, with ``destroy_port = PJ_TRUE``, pjsua calls
:cpp:any:`pjmedia_port_destroy` on that substituted port, which
releases the AI-port wrapper through its normal destroy chain;
the precreated stream port remains unreferenced, and pjsua tears
down the stream independently when the call ends.

Checklist
---------

Regardless of which pattern the substituted port follows:

- **Set** ``destroy_port = PJ_TRUE`` **in
  ``pjsua_on_stream_created_param``** — unless the application
  already arranges to call :cpp:any:`pjmedia_port_destroy` on
  the substituted port itself. With ``destroy_port = PJ_TRUE``,
  PJSUA performs that call at step 3 of the teardown sequence
  (only when the substituted port differs from the stream's
  own port — see ``pjsua_aud.c`` near line 559). If neither the
  application nor PJSUA calls ``port_destroy``, the wrapper's
  own reference is never released, the destroy chain never
  fires, and the wrapper's pool leaks — and in Pattern A, the
  pin on the stream's group lock keeps the stream port alive
  past its useful life too.

- **Never call** :cpp:any:`pjmedia_stream_destroy` **on the
  precreated stream from the application.** PJSUA owns that
  stream's lifecycle and calls it at step 4. A second call from
  the application is at best a redundant ``dec_ref`` on a freed
  lock and at worst crashes inside the second invocation.

- **Don't free the substituted port's pool from the application
  thread.** Bridge removal is asynchronous; pool release must
  happen from inside the destroy chain (i.e. from the wrapper's
  ``on_destroy``). The wrapper struct allocated in the
  application's main pool — and a parent pool destroyed too
  eagerly — is the same use-after-free under a different
  guise. ``pjmedia_port_init_grp_lock`` emits a level-2 warning
  when ``on_destroy`` is missing
  (:source:`pjmedia/src/pjmedia/port.c`); take it seriously.
  See :ref:`custom_port_lifecycle` for the full bridge-side
  contract.

- **Don't share the precreated stream's group lock with the
  wrapper.** Hand the wrapper its own group lock (Pattern 1a)
  or let the bridge auto-create one (Pattern 1b). Sharing
  collapses two distinct lifetimes into one counter — the
  wrapper's own reference and the stream's own reference end
  up on the same lock — and one ``pjmedia_port_destroy``
  releases both.

- **Pattern A only: pin the inner stream port at construction.**
  Without ``pj_grp_lock_add_ref(downstream->grp_lock)`` and a
  matching ``dec_ref`` in ``on_destroy``, the
  use-after-free described in `The bug pattern`_ is
  unavoidable. The bridge's ``conf_port->removing`` flag does
  *not* prevent this — it only narrows the window between flag
  check and the next ``read_port`` call.

- **``on_stream_destroyed`` is informational only.** The
  callback fires at step 2; the application does not need to
  release anything from there. Wrapper teardown is driven by
  ``destroy_port`` + the bridge remove, not by this callback.

See also
--------

- :ref:`custom_port_lifecycle` — bridge-side contract that
  every custom port must honour, including the substituted
  ports described here.
- :ref:`asynchronous_operations` — why
  ``pjmedia_conf_remove_port`` returns before the port is
  actually unregistered.
- :doc:`/specific-guides/develop/group_lock` — group lock
  semantics and the :cpp:any:`pj_grp_lock_add_ref` /
  :cpp:any:`pj_grp_lock_dec_ref` primitives used here.
- :doc:`/specific-guides/media/audio_flow` — the broader
  picture of how the conference bridge, stream, and transport
  fit together.
- :cpp:any:`pjsua_callback::on_stream_created2`,
  :cpp:any:`pjsua_callback::on_stream_created`,
  :cpp:any:`pjsua_callback::on_stream_destroyed`,
  :cpp:any:`pjsua_on_stream_created_param`.

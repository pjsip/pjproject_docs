.. _guide_vidconf:

Video Conference
=================

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.

The video conference bridge is the routing fabric that PJMEDIA uses to
move video frames between sources (capture devices, call decoders,
file players) and sinks (renderers, call encoders, file writers). It
plays the same role for video that the audio conference bridge plays
for audio: every video media object is registered with the bridge as a
*port* (identified by a slot ID), and the application connects sources
to sinks to make video flow.

In PJSUA2 each bridge port is wrapped as a :cpp:any:`pj::VideoMedia`
that knows its slot ID and exposes ``startTransmit()`` /
``stopTransmit()`` for connecting flows.

Available since PJSIP 2.9. The original design discussion lives in
ticket :issue:`2181`.


How the bridge works
--------------------

- Each video media object — a call's encoding stream, a call's decoding
  stream, a capture device, a renderer, an AVI player, an arbitrary
  ``pjmedia_port`` — registers as a port in the bridge and is
  identified by a slot ID. In PJSUA2 the slot is encapsulated in a
  ``VideoMedia`` instance; the raw integer ID is available via
  :cpp:func:`pj::VideoMedia::getPortId()` if needed.
- Connections are **unidirectional**: a source's frames are copied to
  zero or more sinks. To make video flow both ways between two
  endpoints, the application must establish two separate connections.
- **One source → many sinks** — frames are duplicated and delivered to
  each sink. This is how the local capture is shown both in a preview
  window and on the wire to a remote peer.
- **Many sources → one sink** — frames are *mixed* into a tile layout;
  each source is currently resized down so all sources occupy equal
  area in the sink frame. This is how a multi-party conference renders
  every other participant into one window.
- The bridge handles frame-rate and format mismatches between
  connected ports (see :cpp:any:`pjsua_vid_conf_update_port()` for
  picking up format changes mid-session).


Bridge configuration and limits
-------------------------------

PJSUA-LIB creates a single video conference bridge during
initialization with default settings (see
:cpp:any:`pjmedia_vid_conf_setting`). The defaults that matter:

- **Frame rate**: 60 fps. The bridge runs at one rate and resamples
  port frames to it. For smooth playback, the bridge rate should be a
  common multiple of the port frame rates in use. With the default 60,
  ports running at 10, 15, 20, or 30 fps align cleanly; a port at e.g.
  24 fps will jitter against the 60 fps grid. If your application has
  unusual frame-rate combinations, you'd need to raise the bridge rate
  accordingly — but neither PJSUA-LIB nor PJSUA2 exposes a setter for
  this, so changing it requires either using the lower-level
  :cpp:any:`pjmedia_vid_conf_create()` API directly or modifying
  ``pjsua_vid.c``.
- **Maximum slot count**: 32. This is the absolute ceiling on the
  number of ports (calls × 2 for encoder + decoder, plus preview, plus
  any custom ports) that can be registered with the bridge at once.
- **Layout mode**: :cpp:any:`PJMEDIA_VID_CONF_LAYOUT_DEFAULT
  <pjmedia_vid_conf_layout::PJMEDIA_VID_CONF_LAYOUT_DEFAULT>`
  (the equal-tiles behaviour described in the next section). The
  :cpp:any:`pjmedia_vid_conf_layout` enum also defines
  ``SELECTIVE_FOCUS``, ``INTERVAL_FOCUS``, and ``CUSTOM`` values, but
  these are reserved and **not implemented** in the current bridge.
  Applications that need active-speaker, round-robin, or custom
  layouts implement them via a custom intermediate port (see
  :ref:`Custom intermediate ports for advanced layouts
  <vid_conf_custom_port>` below) rather than by setting one of these
  layout modes.


Mixing layout
-------------

When multiple sources transmit to the same sink, the bridge tiles them
into the sink frame. The layout depends on the **number of sources**
(1, 2, 3, or 4) and the **aspect** of the sink frame
(*landscape* if ``width ≥ height``, otherwise *portrait*). Each tile is
filled by center-cropping the source to match the tile's aspect ratio
— sources are never stretched, only cropped.

**1 source** — fills the whole sink frame (no mixing). If the format
and size also match, the bridge skips conversion entirely and just
copies the frame.

**2 sources**:

.. code-block:: text

   landscape sink:           portrait sink:
   +---------+---------+     +-----------+
   |         |         |     |   src 0   |
   |  src 0  |  src 1  |     +-----------+
   |         |         |     |   src 1   |
   +---------+---------+     +-----------+

**3 sources**:

.. code-block:: text

   landscape sink:           portrait sink:
   +---------+---------+     +-----------+
   |         |  src 1  |     |   src 0   |
   |  src 0  +---------+     +-----------+
   |         |  src 2  |     |   src 1   |
   +---------+---------+     +-----------+
                             |   src 2   |
                             +-----------+

**4 sources**:

.. code-block:: text

   landscape sink:           portrait sink:
   +---------+---------+     +-----------+
   |  src 0  |  src 1  |     |   src 0   |
   +---------+---------+     +-----------+
   |  src 2  |  src 3  |     |   src 1   |
   +---------+---------+     +-----------+
                             |   src 2   |
                             +-----------+
                             |   src 3   |

The slot order in the layout follows the order in which sources were
connected to the sink (the ``transmitters`` array in
:cpp:any:`pjsua_vid_conf_port_info`).

**5 or more sources** — the connect call does not enforce a 4-source
limit, so additional connections succeed and the sources are tracked
in the sink's transmitter list. However, the rendering layout switch
only handles 1–4, so only the **first 4 connected sources** are tiled
into the sink frame. Frames from sources connected beyond the fourth
are silently dropped at render time without an error — they simply
don't appear in the mixed output.

.. _vid_conf_custom_port:

Custom intermediate ports for advanced layouts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The bridge's built-in tile mixing covers the common
"everyone equal, up to four" case. Any other layout or selection
behaviour is implemented by inserting a custom intermediate
``pjmedia_port`` — application code that consumes incoming frames
from one or more upstream sources and emits a single composed
frame for downstream sinks. In PJSUA2, derive from ``VideoMedia``,
register the underlying port via
:cpp:func:`pj::VideoMedia::registerMediaPort2()`, then connect
upstream sources into it and it into the eventual sink like any other
``VideoMedia``.

This pattern handles, among others:

- **More than 4 participants in one sink** — compose more sources into
  a single image yourself (e.g. a 3×3 grid for nine participants), or
  do nested mixing where several intermediate ports each mix four and
  feed a final port that mixes those four mixes.
- **Active-speaker / focus view** — render whichever source is
  currently flagged as "speaking" (typically driven by audio-level
  detection on the corresponding audio stream) into the full sink
  frame, with the other participants either hidden or shown as small
  thumbnails. Update the selection on the fly without touching the
  bridge connections.
- **Round-robin / cycling source** — cycle through sources over time,
  showing one (or N) at a time on a timer.
- **Picture-in-picture / non-uniform layouts** — one large region for
  the main source plus smaller regions for the rest, custom borders or
  labels, fixed positions per participant slot, etc.
- **Per-feed video/image filters** — a single-input single-output port
  that applies a filter to its source frames before forwarding them.
  Common uses: background blur or replacement, brightness/contrast/
  saturation adjustment, sharpening, watermarking, privacy redaction,
  ML-based segmentation, etc. Insert one filter port between the
  capture device (or call decoder) and the eventual sink to process
  just that feed; chain several to compose effects.

Because the intermediate port presents itself to the rest of the
bridge as an ordinary single-source port, downstream sinks (call
encoders, renderers) don't need to know any of this is happening — the
selection/composition logic stays local to the custom port. If your
selection state changes mid-call (e.g. a different participant becomes
the active speaker), update inside the port's ``put_frame`` /
``get_frame`` implementation; you don't need to ``startTransmit()`` /
``stopTransmit()`` on every change.


Default wiring
--------------

When a video stream is negotiated on a call, the library adds the
call's encoder and decoder as separate ports and wires them
automatically:

- The default capture device is connected to the call's encoding slot,
  so the camera reaches the encoder without manual setup.
- The call's decoding slot is connected to a renderer that the library
  creates for the incoming video.

Most apps don't need to touch the bridge for normal one-to-one calls.
The bridge becomes interesting when:

- the app wants the same camera feed in a local preview *and* on a
  call (multi-sink fan-out is automatic; nothing to do for the
  preview-while-calling case),
- the app wants to bridge two or more calls into a single video
  conference (cross-connect their encoder/decoder slots),
- the app wants to feed an AVI player or other custom
  ``pjmedia_port`` into a call (register the port, then connect it to
  the call's encoder slot).


Looking up VideoMedia handles
-----------------------------

PJSUA2 exposes per-stream VideoMedia objects directly on the call:

.. code-block:: c++

   // Per-stream VideoMedia — each wraps a bridge slot.
   VideoMedia enc = call.getEncodingVideoMedia(med_idx);
   VideoMedia dec = call.getDecodingVideoMedia(med_idx);

   // The underlying slot IDs, if you need them:
   int enc_slot = enc.getPortId();
   int dec_slot = dec.getPortId();

For a local capture preview started with
:cpp:func:`pj::VideoPreview::start()`, the corresponding VideoMedia is
returned by :cpp:func:`pj::VideoPreview::getVideoMedia()`. For
arbitrary ports added via ``registerMediaPort2()``, the slot is
available as ``getPortId()`` on the wrapping VideoMedia subclass.

To inspect the bridge as a whole, use
:cpp:any:`pjsua_vid_conf_get_active_ports()`,
:cpp:any:`pjsua_vid_conf_enum_ports()`, and
:cpp:any:`pjsua_vid_conf_get_port_info()`. The port info also lists
each port's current transmitters and listeners, which is useful for
debugging connection state.


Connecting and disconnecting flows
----------------------------------

VideoMedia exposes start / stop transmit between any two slots:

.. code-block:: c++

   source_vm.startTransmit(sink_vm, VideoMediaTransmitParam());
   source_vm.stopTransmit(sink_vm);

Both are unidirectional and both run **asynchronously** — see
:ref:`async notification <vid_conf_async>` below.


Three-party video conference
----------------------------

Adding a third leg means cross-connecting two existing calls so their
remote videos flow to each other in addition to the local participant.

.. code-block:: c++

   VideoMedia enc1 = call1.getEncodingVideoMedia(med_idx);
   VideoMedia dec1 = call1.getDecodingVideoMedia(med_idx);
   VideoMedia enc2 = call2.getEncodingVideoMedia(med_idx);
   VideoMedia dec2 = call2.getDecodingVideoMedia(med_idx);

   // Show call2's video to call1, and call1's video to call2:
   dec2.startTransmit(enc1, VideoMediaTransmitParam());
   dec1.startTransmit(enc2, VideoMediaTransmitParam());

Now both remote parties see each other in addition to the local
participant. Because mixing happens on the *sink* side, neither remote
needs special support — they each just receive a single mixed frame
that combines the local participant and the other remote.

Tear it down by reversing the connects:

.. code-block:: c++

   dec2.stopTransmit(enc1);
   dec1.stopTransmit(enc2);


Adding a custom port
--------------------

Any ``pjmedia_port`` (for example, the AVI player from
:cpp:any:`pjmedia_avi_player_create_streams()`) can be registered with
the bridge so it participates in the routing. PJSUA2's ``VideoMedia``
exposes the registration helpers as protected, so the application
derives a wrapper class that calls them and takes ownership of the
underlying port:

.. code-block:: c++

   class CustomVideoPort : public VideoMedia
   {
   public:
       void init(pjmedia_port *port, pj_pool_t *pool) {
           // Calls into the protected VideoMedia helper.
           registerMediaPort(port, pool);
       }
       ~CustomVideoPort() override {
           if (id != PJSUA_INVALID_ID)
               unregisterMediaPort();
       }
   };

   CustomVideoPort avi_src;
   avi_src.init(avi_port, pool);

   // Forward into call1's encoder and a local renderer:
   avi_src.startTransmit(call1.getEncodingVideoMedia(0),
                         VideoMediaTransmitParam());
   avi_src.startTransmit(my_renderer_vm, VideoMediaTransmitParam());

The destructor calls ``unregisterMediaPort()`` so the port is removed
from the bridge when the wrapper goes out of scope.

If the port's media format changes mid-session (for example, a video
decoder learns new dimensions from incoming RTP), call
:cpp:any:`pjsua_vid_conf_update_port()` to make the bridge re-read the
port info and rewire any conversions. The bridge does this
automatically for the call streams it owns; only manually-added ports
need this call.


.. _vid_conf_async:

Asynchronous operations and completion callback
-----------------------------------------------

``startTransmit``, ``stopTransmit``, ``registerMediaPort2``,
``unregisterMediaPort``, and the underlying
``pjsua_vid_conf_update_port`` all return as soon as the operation is
*queued*. The actual work happens on a media thread.

Apps that need to know when an operation has fully taken effect should
implement :cpp:func:`pj::Endpoint::onVideoMediaOpCompleted()`. The
callback receives info identifying which operation completed and the
operation's result code (``PJ_SUCCESS`` on success, or an error code if
the operation failed). The callback fires from a media thread, so keep
the handler short — defer any long or blocking work to your own thread.

A common pattern: kick off a connect, mark the call/UI state as
"pending", and let the completion callback transition it to "active".
Don't assume the connection is ready right after ``startTransmit()``
returns.


PJSUA-LIB equivalents
---------------------

+------------------------------------------------------+--------------------------------------------------------+
| PJSUA2                                               | PJSUA-LIB                                              |
+======================================================+========================================================+
| ``VideoMedia`` (slot wrapper)                        | :cpp:any:`pjsua_conf_port_id` (raw slot ID)            |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::VideoMedia::getPortId()`              | (the slot ID is the value itself)                      |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Call::getEncodingVideoMedia()` /      | :cpp:any:`pjsua_call_get_vid_conf_port()` with         |
| :cpp:func:`pj::Call::getDecodingVideoMedia()`        | ``PJMEDIA_DIR_ENCODING`` / ``PJMEDIA_DIR_DECODING``    |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::VideoPreview::getVideoMedia()`        | :cpp:any:`pjsua_vid_preview_get_vid_conf_port()`       |
+------------------------------------------------------+--------------------------------------------------------+
| ``VideoMedia::startTransmit(sink, param)``           | :cpp:any:`pjsua_vid_conf_connect()`                    |
+------------------------------------------------------+--------------------------------------------------------+
| ``VideoMedia::stopTransmit(sink)``                   | :cpp:any:`pjsua_vid_conf_disconnect()`                 |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::VideoMedia::registerMediaPort2()`     | :cpp:any:`pjsua_vid_conf_add_port()`                   |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::VideoMedia::unregisterMediaPort()`    | :cpp:any:`pjsua_vid_conf_remove_port()`                |
+------------------------------------------------------+--------------------------------------------------------+
| :cpp:func:`pj::Endpoint::onVideoMediaOpCompleted()`  | :cpp:any:`pjsua_callback::on_vid_conf_op_completed`    |
+------------------------------------------------------+--------------------------------------------------------+

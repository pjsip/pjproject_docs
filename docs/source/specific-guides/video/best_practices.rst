Video Best Practices
=====================

Cross-cutting "do this, watch out for that" notes for video
applications.

.. contents::
   :local:
   :depth: 2


Threading and GUI frameworks
----------------------------

Don't call PJSIP from the GUI thread
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP API calls can take time to complete or block on a lock. Calling
them directly from the GUI / main thread freezes the UI; on some
platforms it deadlocks outright. Always post PJSIP work to a worker
thread, or schedule it via
:cpp:func:`pj::Endpoint::utilTimerSchedule()` (PJSUA2) so the library
worker thread runs it.

Media event callbacks (``onCallMediaEvent``,
``onVideoMediaOpCompleted``) themselves run on a media thread —
keep the handlers short and post any heavy work elsewhere.


macOS Cocoa main-thread requirement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On macOS, the video implementation uses Cocoa frameworks, which
require user-event handling and window drawing to happen on the main
thread. To avoid deadlock, the application **must not** call any
potentially-blocking PJSIP API from the main thread.

PJLIB provides :cpp:any:`pj_run_app()` as a convenience: it sets up an
event-loop manager in the main thread and creates a worker thread for
your real ``main_func``, so PJSIP calls can run from the worker
without blocking the GUI. The pjsua sample app at
:sourcedir:`pjsip-apps/src/pjsua` uses this pattern.

.. code-block:: c

   int main_func(int argc, char *argv[])
   {
       // This is your real main function
   }

   int main(int argc, char *argv[])
   {
       // pj_run_app() will call your main function from another thread
       // (if necessary) — this frees the main thread to handle GUI
       // events and drawing.
       return pj_run_app(&main_func, argc, argv, 0);
   }

For a PJSUA2-flavoured equivalent on Windows / SDL where the same
"don't call from the GUI thread" rule applies, see *Important note
about threading* on the :any:`/pjsua2/using/media_video` page, which
shows scheduling preview start via ``Endpoint::onTimer()``.


.. _vid_ug_show_window:

Video window UX
---------------

Hide the renderer until the first FMT_CHANGED event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a video call the application typically cannot know the remote
video format — width, height, frame rate — until after some video RTP
packets arrive and decode successfully. If the renderer window is
shown before that, users see green frames or a stretched black box
until the first decoded frame arrives.

Recommended pattern:

#. Leave ``AccountVideoConfig::autoShowIncoming`` (PJSUA-LIB:
   :cpp:any:`pjsua_acc_config::vid_in_auto_show`) at ``false`` so the
   library does not show the window for you.
#. In your :cpp:func:`pj::Call::onCallMediaEvent` handler, watch for
   :cpp:any:`PJMEDIA_EVENT_FMT_CHANGED <pjmedia_event_type::PJMEDIA_EVENT_FMT_CHANGED>`
   on the incoming video stream's media index.
#. On the first ``FMT_CHANGED`` for that stream, read the new size
   from the event payload, size your UI container accordingly, then
   show the renderer window — embed the native window handle (for
   native windows) into your UI hierarchy, or call ``Show(true)``
   (for non-native windows like SDL on desktop).
#. Subsequent ``FMT_CHANGED`` events on the same stream indicate that
   the peer changed resolution mid-call; resize the container in
   place.

A worked PJSUA2 handler is in *Video event* on the
:any:`/pjsua2/using/media_video` walkthrough.

The same anti-pattern bites when the call is reconnecting from
mobile background or after a network change: keep the renderer
hidden until ``FMT_CHANGED`` fires again, otherwise the user sees a
flash of stale or empty frames.

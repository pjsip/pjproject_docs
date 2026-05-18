.. _guide_logging:

Logging and Diagnostics for Issue Reports
==========================================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Goal
----

When something misbehaves in the library, two artifacts are
usually needed to investigate:

1. A **log** showing what happened, ideally at level 4 or higher
   (so internal flow is visible).
2. For crashes / hangs, a **stack trace** of where the process was
   when it failed.

This guide covers how to capture both in two common scenarios —
*development* (you're actively reproducing) and *production*
(the issue happened in the field, often on someone else's device)
— and how to package them for a useful bug report.


Two scenarios
-------------

Development / debugging
~~~~~~~~~~~~~~~~~~~~~~~

You can reproduce the issue at will, you have the source, you can
run a debugger.

- Build the library with **debug symbols** (``-g`` for GCC/Clang;
  ``/Zi`` for MSVC; Debug configuration in Xcode/Android Studio).
- Set log level to **5 or 6** for full trace.
- Run under a debugger (``gdb``, ``lldb``, Visual Studio / Xcode
  attached) so crashes drop you into a live backtrace.

Production / field
~~~~~~~~~~~~~~~~~~

The issue happened on an end user's deployment. You can't attach a
debugger; you have to **persist** diagnostic state and ship it back.

- Build with debug symbols (yes, even for release) and keep the
  unstripped binaries (``.so`` / ``.pdb`` / ``.dSYM``) on your
  build server. Ship stripped binaries to users. Symbolicate
  later.
- Configure the library to log to a **file** so messages survive
  process exit and can be uploaded.
- Use **at least level 4** for the file log (see *Choosing a log
  level* below).
- Install a **crash handler** that captures backtraces and
  uploads them.


Capturing logs
--------------

Choosing a log level
~~~~~~~~~~~~~~~~~~~~

The :cpp:any:`PJ_LOG` macro takes a level 0–6 (:sourcedir:`pjlib/src/pj/log.c`):

+-------+--------+--------------------------------------+
| Level | Name   | What you see                         |
+=======+========+======================================+
| 0     | FATAL  | fatal-only — nothing else            |
+-------+--------+--------------------------------------+
| 1     | ERROR  | unrecoverable errors                 |
+-------+--------+--------------------------------------+
| 2     | WARN   | non-fatal anomalies                  |
+-------+--------+--------------------------------------+
| 3     | INFO   | major events (start, REGISTER OK,    |
|       |        | call connected, …)                   |
+-------+--------+--------------------------------------+
| 4     | DEBUG  | level-3 plus internal flow, SDP      |
|       |        | exchange details, callbacks fired    |
+-------+--------+--------------------------------------+
| 5     | TRACE  | level-4 plus per-packet, per-timer,  |
|       |        | per-callback                         |
+-------+--------+--------------------------------------+
| 6     | DETRC  | exhaustive detail trace              |
+-------+--------+--------------------------------------+

**Recommendations**

- **Production**: at least **level 4**. Level 4 carries enough
  context (state transitions, errors, key callbacks) to triage
  most issues. Going lower (3 or 2) is acceptable only when
  resources are genuinely tight (footprint, log volume) **and**
  nobody is on duty to investigate issues — at lower levels, most
  bug reports become unactionable.
- **Development**: **level 5** is the sweet spot for active
  debugging. Level 6 is useful for nasty races / timing bugs but
  produces a lot of noise.
- **Compile-time cap**: :c:macro:`PJ_LOG_MAX_LEVEL` (default 5 in
  ``pjlib/include/pj/config.h``) is the hard ceiling. Bumping it
  to 6 in ``config_site.h`` enables ``DETRC`` log macros; lowering
  it strips higher-level calls entirely at compile time.

Module-specific tracing
~~~~~~~~~~~~~~~~~~~~~~~

Beyond the runtime log level, some modules carry extra tracing
that's gated by a compile-time switch and needs a library rebuild
to enable. It's not normally on because the output is voluminous
or expensive — but a deeper investigation of a specific module
may need it.

Three patterns to be aware of:

- **``config_site.h`` macros** — e.g.,
  :c:macro:`PJMEDIA_STREAM_TRACE_JB` enables the jitter-buffer
  CSV trace in :sourcedir:`pjmedia/src/pjmedia/stream.c`. Set in
  ``pjlib/include/pj/config_site.h`` and rebuild.
- **In-source ``#define X 0`` knobs** — e.g., ``DTLS_DEBUG`` at
  the top of :sourcedir:`pjmedia/src/pjmedia/transport_srtp_dtls.c`,
  ``ENABLE_LOG`` in :sourcedir:`pjnath/src/pjnath/upnp.c`. Edit the
  ``.c`` file to flip them to ``1`` and rebuild.
- **Local ``TRACE_(...)`` macros** at high log level — e.g.,
  the per-frame trace in
  :sourcedir:`pjmedia/src/pjmedia/vid_conf.c` emits at level 5 by
  default; raising your runtime level to 5 or 6 surfaces it
  without a rebuild.

You don't need to enable these speculatively. If you know which
module is involved (jitter buffer, DTLS handshake, video
conference, etc.) and you've already filed an issue, mention what
you know about the module — you may then be asked whether a
specific trace is worth enabling.

Configuring the log via PJSUA2 / PJSUA-LIB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PJSUA2 (set on :cpp:any:`pj::EpConfig::logConfig`):

.. code-block:: c++

   EpConfig epcfg;
   epcfg.logConfig.level        = 5;
   epcfg.logConfig.consoleLevel = 4;
   epcfg.logConfig.msgLogging   = true;          // include SIP message traffic
   epcfg.logConfig.filename     = "/var/log/myapp/pjsip.log";
   epcfg.logConfig.fileFlags    = PJ_O_APPEND;   // append on restart

   endpoint.libCreate();
   endpoint.libInit(epcfg);
   endpoint.libStart();

PJSUA-LIB equivalent:

.. code-block:: c

   pjsua_logging_config log_cfg;
   pjsua_logging_config_default(&log_cfg);
   log_cfg.level         = 5;
   log_cfg.console_level = 4;
   log_cfg.msg_logging   = PJ_TRUE;
   log_cfg.log_filename  = pj_str("/var/log/myapp/pjsip.log");
   log_cfg.log_file_flags = PJ_O_APPEND;

   pjsua_init(NULL, &log_cfg, NULL);

Defaults from :cpp:any:`pjsua_logging_config_default`: ``level=5``,
``console_level=4``, ``msg_logging=PJ_TRUE``, decor as below.

Log decor
^^^^^^^^^

*Decor* is the bitmask that controls what each log line includes
beyond the message itself — timestamp, source filename, thread
markers, etc. The default produces lines like:

.. code-block:: text

   10:24:33.451   pjsua_core.c  Start handling IP address change

Each ``PJ_LOG_HAS_*`` flag toggles one column
(:sourcedir:`pjlib/include/pj/log.h`). Defaults
(:sourcedir:`pjlib/src/pj/log.c`) enable: ``PJ_LOG_HAS_TIME``,
``PJ_LOG_HAS_MICRO_SEC``, ``PJ_LOG_HAS_SENDER``,
``PJ_LOG_HAS_NEWLINE``, ``PJ_LOG_HAS_SPACE``,
``PJ_LOG_HAS_THREAD_SWC`` (a marker on thread changes),
``PJ_LOG_HAS_INDENT``, and on Windows ``PJ_LOG_HAS_COLOR`` (ANSI
colour by level).

For threading visibility, the default decor already enables
``PJ_LOG_HAS_THREAD_SWC`` — a one-line marker emitted only when
the logging thread *changes*, which is the lightweight default and
usually enough. For a richer view, add ``PJ_LOG_HAS_THREAD_ID``,
which appends the thread name to every line (more readable in
heavy-concurrency bugs at the cost of wider lines).

Other flags useful for issue reports that aren't on by default:

- ``PJ_LOG_HAS_LEVEL_TEXT`` — prefixes each line with
  ``ERROR:`` / ``WARN:`` / ``INFO:`` etc., useful when piping the
  log into ``grep`` or a viewer that doesn't know the pjsip
  format.
- ``PJ_LOG_HAS_DAY_OF_MON`` / ``PJ_LOG_HAS_YEAR`` /
  ``PJ_LOG_HAS_MONTH`` — date
  components. Useful for long-running deployments where a
  timestamp alone (which wraps at 24 hours) is ambiguous.

To customise, OR the flags you want with the existing decor:

.. code-block:: c++

   epcfg.logConfig.decor |= PJ_LOG_HAS_THREAD_ID | PJ_LOG_HAS_LEVEL_TEXT;

Or take full control by setting decor to exactly what you want.

Thread-safety / dropped lines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Worth knowing for diagnostic work:

- With the default ``PJ_LOG_USE_STACK_BUFFER=1``
  (:sourcedir:`pjlib/include/pj/config.h`), each ``PJ_LOG`` call
  uses its own stack buffer — concurrent logs from different
  threads are safe and don't corrupt each other. If you've set
  ``PJ_LOG_USE_STACK_BUFFER=0`` for footprint, the writer becomes
  non-reentrant — concurrent calls from multiple threads can
  interleave or lose data.
- PJLIB suppresses logging *recursively* on the same thread — if
  a log call's internal formatting triggers another log (e.g.
  via a PJLIB API the formatter calls), the nested log is
  **silently dropped**. This also applies inside a custom
  ``LogWriter`` / ``cb``: any ``PJ_LOG`` you emit from within the
  writer is dropped, not recursed. The mechanism prevents
  infinite recursion but can confuse "where did my log line go?"
  debugging.

pjsua CLI
~~~~~~~~~

.. code-block:: shell

   $ ./pjsua --log-file=/tmp/pjsip.log --log-level=5 --app-log-level=4 --log-append

- ``--log-file=path`` — write to file (otherwise stderr only).
- ``--log-level=N`` — file/callback level (default 5).
- ``--app-log-level=N`` — console level (default 4).
- ``--log-append`` — append on each run instead of overwriting.


Custom log writer
-----------------

Sometimes you need the library's log to land somewhere other than
stdout or a file — for example a platform logger (logcat,
``os_log``, ``OutputDebugString``, syslog), an in-app log viewer,
or your own crash/diagnostic uploader. Install a custom writer
and the library delegates every log line to it.

PJSUA2 — subclass :cpp:any:`pj::LogWriter` and override ``write()``:

.. code-block:: c++

   class MyLogWriter : public LogWriter {
   public:
       void write(const LogEntry &entry) override {
           // entry.msg, entry.level, entry.threadId, entry.time, ...
           // Forward to your sink:
           //   - syslog():            POSIX system log
           //   - os_log():            Apple unified logging
           //   - __android_log_print: Android logcat
           //   - OutputDebugStringA:  Windows debug stream
           //   - your own uploader
       }
   };

   MyLogWriter writer;        // must outlive the Endpoint
   epcfg.logConfig.writer = &writer;

PJSUA-LIB — set the C callback on :cpp:any:`pjsua_logging_config::cb`:

.. code-block:: c

   static void my_log_callback(int level, const char *data, int len) {
       /* level: pjlib log level 0–6
        * data:  full formatted line, may include trailing newline
        * len:   length of `data`
        * Forward to your sink.
        */
   }

   pjsua_logging_config_default(&log_cfg);
   log_cfg.cb = &my_log_callback;
   pjsua_init(NULL, &log_cfg, NULL);

Raw PJLIB — :cpp:any:`pj_log_set_log_func` (signature is the same
``pj_log_func``):

.. code-block:: c

   pj_log_set_log_func(&my_log_callback);

Java (PJSUA2 via SWIG) — subclass ``LogWriter`` and override
``write``. The Android sample does this to push into logcat via
``System.out`` (see :sourcedir:`pjsip-apps/src/swig/java/android/`):

.. code-block:: java

   class MyLogWriter extends LogWriter {
       @Override
       public void write(LogEntry entry) {
           System.out.println(entry.getMsg());
           // Or, for a custom logcat tag:
           // android.util.Log.d("pjsip", entry.getMsg());
       }
   }

   MyLogWriter lw = new MyLogWriter();   // keep this reference alive!
   epCfg.getLogConfig().setWriter(lw);
   endpoint.libInit(epCfg);

Python (PJSUA2 via SWIG) — subclass ``pj.LogWriter`` (the bundled
``pjsip-apps/src/swig/python/test.py`` has a working example):

.. code-block:: python

   import pjsua2 as pj
   import sys

   class MyLogWriter(pj.LogWriter):
       def write(self, entry):
           sys.stdout.write("pjsip: " + entry.msg + "\n")

   ep_cfg = pj.EpConfig()
   lw = MyLogWriter()              # keep this reference alive!
   ep_cfg.logConfig.writer = lw
   ep_cfg.logConfig.decor &= ~(pj.PJ_LOG_HAS_CR | pj.PJ_LOG_HAS_NEWLINE)

   ep = pj.Endpoint()
   ep.libCreate()
   ep.libInit(ep_cfg)

.. warning::

   The callback may be invoked from **any thread** — including
   pjsip worker threads and timer callbacks. Keep the writer
   thread-safe and **non-blocking**. Avoid calling pjsip APIs
   from within it (re-entrancy risk). Don't allocate or take
   locks that other pjsip code might hold.

   **Java / Python: keep the writer object referenced** for the
   lifetime of the Endpoint. If the only reference is the SWIG
   wrapper's, the garbage collector may free the writer while
   the library still holds a pointer to it — leading to a
   use-after-free crash. Store it as an instance / module variable.

For applications that link pjnath / pjlib without PJSUA-LIB, the
same callback is set via the raw PJLIB API
:cpp:any:`pj_log_set_log_func`:

.. code-block:: c

   static void my_log_writer(int level, const char *data, int len) {
       /* write to file, syslog, etc. */
   }

   pj_log_set_level(5);
   pj_log_set_decor(PJ_LOG_HAS_SENDER | PJ_LOG_HAS_TIME |
                    PJ_LOG_HAS_MICRO_SEC | PJ_LOG_HAS_NEWLINE);
   pj_log_set_log_func(&my_log_writer);


Per-platform fetching
---------------------

Where the default log ends up, and how to capture it, varies by
platform. The default writer
(:sourcedir:`pjlib/src/pj/log_writer_stdout.c`) is just
``printf()`` — so behaviour depends on where stdout goes on each
platform.

Linux / macOS / \*nix
~~~~~~~~~~~~~~~~~~~~~

Default goes to stdout. Capture by redirecting or using the
``--log-file`` flag (or :cpp:any:`pjsua_logging_config::log_filename`):

.. code-block:: shell

   ./myapp 2>&1 | tee pjsip.log
   ./myapp >pjsip.log 2>&1

Or set ``log_filename`` directly so the library writes the file
itself (preferable for daemons).

Windows
~~~~~~~

Default writer uses ``printf()`` with ANSI colour codes. On modern
Windows the console renders them natively. For redirection:

.. code-block:: shell

   myapp.exe > pjsip.log 2>&1

For GUI / service apps without a console, the simplest path is to
use ``log_filename`` so the library writes a file directly. If you
need ``OutputDebugString`` (visible in DebugView /
``WinDbg``), install a custom writer and call ``OutputDebugStringA``
from it.

Android
~~~~~~~

The library does **not** ship a logcat-aware writer. What the
default ``printf()`` does depends on which side of the JNI boundary
the message originates:

- **PJSUA2 from Java / Kotlin** (the typical app pattern): override
  :cpp:any:`pj::LogWriter` and call
  ``System.out.println(entry.getMsg())``. Android's runtime
  forwards ``System.out`` to logcat under the ``System.out`` tag,
  so logs show up in logcat automatically. This is what the
  bundled ``pjsua2`` Java / Kotlin Android samples do
  (see :sourcedir:`pjsip-apps/src/swig/java/android/`). For a
  custom tag, call ``android.util.Log.d("pjsip", entry.getMsg())``
  instead of ``println``.
- **Native NDK code linking the library directly**: ``printf()`` /
  stdout from the native side is not forwarded to logcat. Set
  ``log_filename`` to write to a file, or install a custom writer
  in C that calls ``__android_log_print(ANDROID_LOG_INFO, "pjsip",
  "%.*s", len, data);``.

**Recommended file location**: the app's **internal files**
directory, ``context.getFilesDir()``. Always available, app-
private, requires no permission. Path looks like
``/data/data/<package>/files/pjsip.log``.

.. code-block:: java

   // Java / Kotlin — pass to pjsip as the log_filename
   File logFile = new File(context.getFilesDir(), "pjsip.log");

The trade-off is that internal storage isn't directly accessible
to the user. **Pair this with a "Share log" UI affordance** in
your app that surfaces the file via a Share Intent (``ACTION_SEND``
with a ``FileProvider`` URI) — the user picks email / drive / chat
to send it. This is the production pattern.

``getExternalFilesDir(null)`` (``/sdcard/Android/data/<pkg>/files/``)
is the alternative when you want the file *visible to the user*
via a file manager without an in-app affordance — but it can return
``null`` when external storage isn't mounted, so it's not always
available. Don't rely on it as the only location in production.

For development builds, ``adb pull`` works against internal storage
via ``run-as`` (debuggable build only):

.. code-block:: shell

   # External files dir (any build):
   adb pull /sdcard/Android/data/com.example.myapp/files/pjsip.log

   # Internal files dir (debuggable build only):
   adb exec-out run-as com.example.myapp cat files/pjsip.log > pjsip.log

Forwarding to logcat (custom writer):

.. code-block:: c

   __android_log_print(ANDROID_LOG_INFO, "pjsip", "%.*s", len, data);

Watch live: ``adb logcat -s pjsip``.

iOS / macOS apps
~~~~~~~~~~~~~~~~

Same situation as Android — the default ``printf()`` goes to
stdout, which on iOS isn't user-accessible.

**Recommended file location**: the app's Documents directory
(``NSDocumentDirectory``), which becomes user-visible if the app's
``Info.plist`` sets:

.. code-block:: xml

   <key>UIFileSharingEnabled</key>           <true/>
   <key>LSSupportsOpeningDocumentsInPlace</key>  <true/>

With both keys set, the log file shows up under the app in the
iOS **Files** app, so the user can email / AirDrop / upload it to
your support endpoint without needing a developer's help. From a
Mac with a connected device, the file is also accessible via
**Finder → Files** when the device is connected.

For background apps without a UI, install a custom writer that
calls ``os_log`` / ``os_log_with_type`` — messages then appear in
Console.app and the device's unified logging stream. ``os_log`` is
preferred over ``NSLog`` for non-debug logging.


.. _capturing_media:

Capturing media (for audio / video issues)
------------------------------------------

For issues that show up as bad audio (silence, distortion, echo,
dropouts, one-way audio) or bad video (frozen, flipped, garbled,
lag), the actual audio / video symptom is often more useful for
investigation than the log alone. The simplest way to capture it
is to **record what flows through the conference bridge**:
attach a recorder port on the same slot the call is connected to,
and the library writes a ``.wav`` (audio) or ``.avi`` (video) you
can attach to the issue.

PJSUA2:

.. code-block:: c++

   // Audio — record the call leg as it sounds locally.
   AudioMediaRecorder rec;
   rec.createRecorder("/path/to/writable/call.wav");
   // On Android, pass the path from context.getFilesDir() (or
   // context.getExternalFilesDir(null)) through JNI; on iOS, the
   // Documents directory; on desktop, any writable path.

   // Hook to the call's audio leg (after the call connects).
   AudioMedia callAudio = call.getAudioMedia(/*med_idx*/ -1);
   callAudio.startTransmit(rec);   // record incoming audio

   // To also capture what you sent, transmit the local mic into rec too:
   AudDevManager &mgr = ep.audDevManager();
   mgr.getCaptureDevMedia().startTransmit(rec);

   // ... call runs ...

   // Stop & close — the WAV header is finalised on destruction.
   // `rec` going out of scope is enough; explicit cleanup not required.

Video (PJSUA2) — :cpp:any:`pj::VideoRecorder` works analogously
against the video conference bridge; see the AVI writer reference
in :sourcedir:`pjmedia/include/pjmedia/avi_stream.h`.

PJSUA-LIB equivalents:
:cpp:any:`pjsua_recorder_create` for audio (and the underlying
:cpp:any:`pjmedia_wav_writer_port_create` if you need raw PJMEDIA
control). Then :cpp:any:`pjsua_conf_connect` to wire the
recorder's slot to the call leg's slot.

Where to put the file: same recommendation as for log files — on
Android use ``getExternalFilesDir(null)``, on iOS use the
Documents directory with file-sharing enabled, on desktop a
writable path the user knows.

For diagnostic needs beyond a plain WAV recording — inspecting
raw PCM frames, feeding them into a custom format or an ML
pipeline, or otherwise tapping the audio path programmatically —
see :doc:`/specific-guides/audio/audio_frame_manipulation`, which
covers :cpp:any:`pj::AudioMediaPort` and the PJSUA-LIB /
PJMEDIA-level alternatives.

.. note::

   Recording captures media as it appears **inside** the library's
   conference bridge — i.e. after RTP receive and decoding, before
   playback. That's the right perspective for most issues
   ("the library thinks the audio is X"). When the problem is in
   how the OS audio device renders sound, or how it captured it
   in the first place, the bridge recording won't see it — see
   *External observers* below.

External observers
~~~~~~~~~~~~~~~~~~

Some classes of issue are only visible from *outside* the library:

- **On-wire SIP / RTP problems** (packets dropped by a NAT,
  malformed packets from a peer, codec mismatches that survive
  SDP negotiation but break decoding): capture with **Wireshark**
  / ``tshark`` / ``tcpdump`` on the same network the call is on.
  Wireshark's *Telephony → VoIP Calls* view stitches SIP +
  RTP together and can play back the captured RTP stream as
  audio.
- **OS audio device behaviour** (mic muted by the OS, AGC over-
  aggressive, sample-rate conversion artefacts): capture the
  device-level audio with the platform's tools — Audio MIDI Setup
  on macOS, ``adb shell dumpsys audio`` on Android, Windows
  Sound control panel, etc.
- **Echo from acoustic coupling**: indistinguishable from
  software echo in logs; a separate microphone recording of the
  room is what's needed.

Mention any external captures in the bug report — they're useful
to know about even if you don't attach them upfront.


Capturing stack traces
----------------------

Build with debug symbols
~~~~~~~~~~~~~~~~~~~~~~~~

In all cases, the library must be built with debug info, or
backtraces will be unsymbolised addresses you can't act on.

- **GCC / Clang** (autotools, CMake, Makefile builds): add ``-g``
  to ``CFLAGS`` / ``CXXFLAGS``. For production, you typically
  want ``-O2 -g`` (full optimisation, full symbols), then strip
  symbols out of the shipping binary while keeping an unstripped
  copy on the build server.

  .. code-block:: shell

     ./configure CFLAGS="-O2 -g" && make
     # On the build server, keep libpjproject.so.unstripped
     cp libpjproject.so libpjproject.so.unstripped
     strip libpjproject.so

- **MSVC**: build with ``/Zi`` and link with ``/DEBUG`` to produce
  a ``.pdb`` file alongside the ``.exe`` / ``.dll``. Ship the
  binary, keep the ``.pdb`` on the symbol server.

- **Xcode (iOS / macOS)**: Debug configuration produces full
  symbols. For Release, set ``Generate Debug Symbols = Yes`` and
  ``Strip Debug Symbols During Copy = No`` — the build emits a
  ``.dSYM`` bundle alongside the app. Archive the ``.dSYM`` for
  post-hoc symbolication.

- **Android NDK**: ``APP_OPTIM=release`` doesn't strip by default
  — symbols are in the unstripped ``.so`` under
  ``obj/local/<abi>/``. Gradle's release build strips automatically;
  keep the unstripped ``.so`` for ``ndk-stack``.

Development: under a debugger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest path. Run your app under the debugger from the start;
on crash, dump the backtrace.

Linux:

.. code-block:: shell

   gdb --args ./myapp
   (gdb) run
   ... (crash) ...
   (gdb) thread apply all bt    # backtraces of every thread

macOS:

.. code-block:: shell

   lldb -- ./myapp
   (lldb) run
   ... (crash) ...
   (lldb) thread backtrace all

Windows: F5 in Visual Studio; on crash, **Debug → Windows → Call
Stack**, then **Threads** for other threads' stacks.

iOS / macOS app: launch from Xcode; crash drops into the debugger
with the backtrace visible in the navigator.

Android: launch from Android Studio with the native debugger
enabled, or attach ``ndk-gdb`` / ``lldb`` to a running process.

Production: crashes after the fact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can't be in the debugger when the user hits the crash. Two
strategies:

**Coredumps + post-mortem (Linux / macOS servers)**:

.. code-block:: shell

   ulimit -c unlimited
   # ... crash produces a 'core' file ...
   gdb /path/to/myapp /path/to/core
   (gdb) thread apply all bt

For systemd services, configure ``LimitCORE`` and
``CoreDumpFilter`` so cores actually get written.

**Crash reporter integration**:

- **Sentry / Crashlytics / Bugsnag**: link their SDK and your app
  uploads crashes (with backtraces) automatically. They handle
  symbolication if you upload your ``.dSYM`` / unstripped ``.so``
  / ``.pdb``.
- **Custom**: install a signal handler (``SIGSEGV``, ``SIGABRT``)
  that captures **raw frame addresses** via ``backtrace()`` (glibc
  / macOS — async-signal-safe), writes them with ``write(2)`` to
  a pre-opened file descriptor, and re-raises. Resolve the
  addresses to symbols *offline* with ``addr2line`` against the
  unstripped binary. Do **not** call ``backtrace_symbols()``,
  ``malloc``, ``printf``, or PJ_LOG from the handler — they
  aren't async-signal-safe and can deadlock or corrupt state.
  For anything beyond this minimal pattern, prefer a dedicated
  crash-reporter library.

**Android tombstones**: native crashes produce tombstones in
``/data/tombstones/`` (system-owned, not app-readable). The
portable way to retrieve them is via the bug report:

.. code-block:: shell

   adb bugreport bugreport.zip
   # tombstone files are inside, under FS/data/tombstones/

Direct access via ``adb shell ls /data/tombstones`` works only
when the ``shell`` user has access (typically rooted devices /
``userdebug`` builds); on stock release builds root is required.

Symbolicate with ``ndk-stack``:

.. code-block:: shell

   ndk-stack -sym path/to/obj/local/arm64-v8a -dump tombstone.txt

**iOS crash logs**: Xcode → **Window → Devices and Simulators →
View Device Logs**. ``.ips`` files can be symbolicated via
``symbolicatecrash`` (in Xcode's tools) using the archived
``.dSYM``.

**Windows minidumps**: a custom ``SetUnhandledExceptionFilter`` +
``MiniDumpWriteDump`` writes a ``.dmp`` file. Analyze with
WinDbg:

.. code-block:: text

   windbg -z crash.dmp
   > !analyze -v
   > ~*kn               # backtraces of every thread


Hangs (live backtrace, no crash)
--------------------------------

When the process is **stuck** rather than crashed — deadlock,
spinning, blocked on a syscall — capture a live backtrace of every
thread:

- Linux: ``gstack <pid>`` (one-shot, no debugger setup), or
  ``gdb -p <pid>`` then ``thread apply all bt``.
- macOS: ``sample <pid> 5`` samples for 5 seconds and prints a
  full per-thread trace.
- Windows: attach Visual Studio's debugger and break, then look
  at all threads' call stacks.
- Android: ``adb shell debuggerd -b <pid>`` writes a tombstone for
  the running process without crashing it.

A live backtrace from a hung process is often more useful than a
log, because it shows exactly where each thread is parked.


Reporting checklist
-------------------

For an issue report that can be acted on, attach:

- **PJSIP version**: usually already in the log — pjsua's
  initialisation prints a line like ``pjsua version 2.17 for
  Linux-x86_64 initialized`` at level 3, which is enough. For
  ``git`` builds, also include the commit SHA so the exact source
  tree can be identified.
- **Platform**: OS / OS version, CPU architecture, SSL backend
  (OpenSSL, GnuTLS, Mbed TLS, Schannel), SRTP source (bundled vs
  external).
- **Build flags**: ``./configure`` line and any ``config_site.h``
  overrides.
- **A log at level 5** whenever possible (level 4 is acceptable
  fallback when level 5 isn't feasible — e.g. production
  footprint), covering the relevant time window — full session
  preferred, not just the failing moment.
- **For crashes**: backtrace from the debugger / tombstone /
  ``.dSYM``-symbolicated ``.ips`` / minidump analysis. Including
  *all threads* matters when the crash involves locking.
- **For hangs**: live backtrace of every thread (see *Hangs*
  above).
- **For audio / video issues**: a media recording captured at the
  conference bridge — see :ref:`capturing_media` for the recipe.
- **For network / RTP / NAT-flavoured issues**: a **packet
  capture** taken concurrently with the log, on the network
  interface the call ran over. Wireshark's *Telephony → VoIP
  Calls* view stitches SIP + RTP together and lets you confirm
  whether packets were actually delivered, what SDP was on the
  wire, whether RTP was flowing in both directions, and so on.
  ``tcpdump -i any -w call.pcap`` from a server, or Wireshark
  capture filtered to the SIP port plus the negotiated RTP range
  on a desktop, is usually enough.

  A common diagnostic blindspot: an **ALG** (Application Layer
  Gateway) or other SIP-aware middlebox (some routers, firewalls,
  carrier-grade NAT, SBCs) can rewrite SIP messages in flight —
  Contact header, SDP ``c=`` line, RTP ports — without your or
  the peer's knowledge. The log shows what pjsip *sent*, but the
  capture shows what's actually on the wire.
- **Reproduction steps**: what you did to trigger it.
- **Custom code paths** that change how the library runs. The
  bug itself may or may not be in the custom code, but custom
  extensions shape the runtime environment — message flow, media
  flow, thread scheduling — and the actual runtime needs to be
  known to reason about the issue. Call out anything that isn't
  stock PJSIP:

  - **Patches on top of a release** — if it's "PJSIP X.Y plus a
    few PRs", list the PR numbers; for local changes not yet
    upstream, attach the diff.
  - **Custom PJSIP modules** (:cpp:any:`pjsip_module`) — hook the
    SIP message pipeline.
  - **Custom PJMEDIA ports** (:cpp:any:`pjmedia_port`) — inserted
    into the conference bridge or stream. See
    :doc:`/specific-guides/audio/custom_audio_stream_port` and
    :ref:`custom_port_lifecycle` for the contract.
  - **Custom transport adapter**
    (:cpp:any:`pjmedia_transport_adapter_create`) — wraps the
    underlying media transport; see
    :doc:`/specific-guides/media/transport_adapter`.
  - **Third-party media** — custom codecs, custom audio / video
    devices; see
    :doc:`/specific-guides/media/3rd_party_media`.
  - **Custom PJSUA-LIB callback handlers** doing significant work
    (synchronous I/O, blocking calls) on a pjsip thread.

  If none of these apply, say so explicitly ("stock PJSIP
  X.Y.Z, no patches, no custom modules / ports") — it saves a
  round-trip asking.

.. note::

   Check if there is sensitive info in the log before sharing.
   Most of what pjsip logs is not — SIP signalling, SDP
   negotiation, RTP stats — so don't over-redact.


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::LogConfig::level`
     - :cpp:any:`pjsua_logging_config::level`
   * - :cpp:any:`pj::LogConfig::consoleLevel`
     - :cpp:any:`pjsua_logging_config::console_level`
   * - :cpp:any:`pj::LogConfig::msgLogging`
     - :cpp:any:`pjsua_logging_config::msg_logging`
   * - :cpp:any:`pj::LogConfig::filename`
     - :cpp:any:`pjsua_logging_config::log_filename`
   * - :cpp:any:`pj::LogConfig::fileFlags`
     - :cpp:any:`pjsua_logging_config::log_file_flags`
   * - :cpp:any:`pj::LogConfig::decor`
     - :cpp:any:`pjsua_logging_config::decor`
   * - :cpp:any:`pj::LogConfig::writer`
       (:cpp:any:`pj::LogWriter`)
     - :cpp:any:`pjsua_logging_config::cb`
       (function-pointer callback)
   * - (not exposed)
     - :cpp:any:`pj_log_set_level`,
       :cpp:any:`pj_log_set_decor`,
       :cpp:any:`pj_log_set_log_func`
       (raw PJLIB API)


References
----------

- :cpp:any:`PJ_LOG` macro and level conventions:
  :sourcedir:`pjlib/include/pj/log.h`
- :cpp:any:`pjsua_logging_config`:
  :sourcedir:`pjsip/include/pjsua-lib/pjsua.h`
- :cpp:any:`pj::LogConfig` / :cpp:any:`pj::LogWriter`:
  :sourcedir:`pjsip/include/pjsua2/endpoint.hpp`

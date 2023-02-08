Performance Optimization
=========================================

.. contents:: Table of Contents
   :depth: 3


Maximising performance
---------------------------
There are few configuration settings to tweak to reduce the CPU usage of
the application or to produce the best performance out of pjsip: 

Echo canceller
~~~~~~~~~~~~~~~~~~
The software AEC probably is the most CPU intensive
module in PJSIP. To reduce the CPU usage, shorten the EC tail length to
lower value (the :cpp:any:`pjsua_media_config::ec_tail_len` setting), or even
disable it altogether by setting it to zero. 

Float vs fixed point
~~~~~~~~~~~~~~~~~~~~~~~
If the platform does not support
floating point, disable floating point in PJSIP build, by declaring
:c:macro:`PJ_HAS_FLOATING_POINT` to 0 in :any:`config_site.h`. 

Codec
~~~~~~~~~~~~~~
Use low complexity codecs such as *pcmu* or *pcma*. When using
*pcmu* or *pcma*, make sure pjmedia chooses the table based
implementation, by setting :c:macro:`PJMEDIA_HAS_ALAW_ULAW_TABLE` macro to 1
(this is default).

Avoid resampling
~~~~~~~~~~~~~~~~~~~
Resampling is a CPU intensive process, thus it
should be avoided, by choosing uniform clock rate for all
media components (sound device, conference bridge, codecs, WAV files, etc.). 

Choose effective sampling rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Make sure that PJSUA-LIB selects the most effective sampling rate/clock rate for the
application. For example, if the application only supports narrowband
codecs (G.711, GSM, iLBC, G.723, or G.729), then the best sampling rate
to choose would be 8KHz. Choosing higher sampling rate will only just
waste CPU power due to resampling and more processing in general.
With *pjsua*, sampling rate can be forced with ``--clock-rate``
option. In the application, this can be achieved by setting
:cpp:any:`pjsua_media_config::clock_rate` field.

Conference bridge vs audio switchboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If conferencing feature is not needed, replace the conference bridge with the 
:any:`Audio Switchboard </specific-guides/audio/switchboard>`
that is lighter and has less latency. To use the audio switchboard, 
declare :c:macro:`PJMEDIA_CONF_USE_SWITCH_BOARD` to non-zero in :any:`config_site.h`.
See :any:`Audio Switchboard </specific-guides/audio/switchboard>` for more
information.

Logging
~~~~~~~~~~~~~~~~
Speeding up logging can be achieved in two ways. 

First is to make sure that the log writer callback function that is registered to PJLIB logging
writes the log as quick as possible. The default log writer callback is to print the log
to stdout, hence the performance depends on the performance of the terminal.
Application can supply its own log writer callback by calling
:cpp:any:`pj_log_set_log_func()` function. The callback can control what gets
written by filtering the log level of the message.

The second way is to control what gets written to the log in the first place, by setting
the logging (verbosity) level, which ranges from 1 (fatal error) to 5 (verbose debug).
The default logging level is 5 to provide verbose information to assist
debugging. Logging level can be changed at run-time with :cpp:any:`pj_log_set_level()`.

When absolute performance is needed, application can disable, at compile time, all logging calls 
with verbosity greater than certain limit by setting
:c:macro:`PJ_LOG_MAX_LEVEL` macro to the desired level in :any:`config_site.h`. 

Threads
~~~~~~~~~~~~~~~~
Use the optimum number of SIP worker threads in the application. The optimum
number would be equal to the number of processors (or processor cores)
in the system.

Run-time checks
~~~~~~~~~~~~~~~~~~
The libraries are equipped with run-time checks to prevent bad parameters from crashing the
software. This feature can be disabled by setting
:c:macro:`PJ_ENABLE_EXTRA_CHECK` to 0. 

Stack checks
~~~~~~~~~~~~~~~~~~~
PJLIB is equipped with stack overflow detection. This feature can be disabled by
setting :c:macro:`PJ_OS_HAS_CHECK_STACK` to 0. 

Safe module
~~~~~~~~~~~~~~~~~~~
PJSIP is equipped with mutex protection to protect PJSIP modules from being
unregistered while they are still being accessed by PJSIP. If the
application doesn't add/remove modules dynamically during run-time, you
can disable this protection by setting :c:macro:`PJSIP_SAFE_MODULE` to 0. 

Unescape in-place
~~~~~~~~~~~~~~~~~~~~~~~~~
By default, PJSIP will make a copy of escaped
message sequence before unescaping it. You can configure PJSIP to
unescape *in-place* by setting :c:macro:`PJSIP_UNESCAPE_IN_PLACE` to 1. Note
that unescaping in place will modify the original message, so don't do
this if the application needs to access the original message after it
has been parsed (pjsip does not need this access). 

Hash tolower Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By setting :c:macro:`PJ_HASH_USE_OWN_TOLOWER` to one, the hash
function will convert the key to lower case and calculate the hash value
in one loop. 

Release mode
~~~~~~~~~~~~~~~~~~
Don't forget to set the appropriate compiler optimization flag, and disable 
assertion with ``-DNDEBUG``.


How to configure pjsip to serve thousands of calls
-------------------------------------------------------

There are few settings to tweak: 

#. First apply the CPU reduction techniques above to maximize the performance. 
#. Do not use PJSUA-LIB. PJSUA-LIB is designed for building client application.
#. By default, PJSIP is configured to handle only 16384 simultaneous SIP transactions and
   dialogs. This can be enlarged according to the requirement, by
   setting both :c:macro:`PJSIP_MAX_TSX_COUNT` and :c:macro:`PJSIP_MAX_DIALOG_COUNT` to
   the appropriate values (for example, ``640*1024-1``). 
#. If large number of TCP/TLS connections are needed, increase :c:macro:`PJ_IOQUEUE_MAX_HANDLES`
   to some large number (the default is only 64). 
#. We've found that the simple GUID generator (used by GNU build system for \*nix and MacOS X)
   will produce duplicate Id after approximately 2^14 generations.
   This would cause things like transactions to have duplicated branch as
   previous transactions! On Linux, the ``./configure`` script will detect
   the presence of ``libuuid`` (part of
   `e2fsprogs <http://e2fsprogs.sourceforge.net/>`__) and use it if
   available, to avoid this problem. If you encounter this problem, please
   check if ``libuuid`` is available for ``./configure`` on your system.

If you are using PJUS-LIB, then the maximum number of calls supported is
configurable from :cpp:any:`pjsua_config::max_calls` (default is 4). When
increasing the limit, compile time options :c:macro:`PJSUA_MAX_CALLS` and
:c:macro:`PJ_IOQUEUE_MAX_HANDLES` also needs to be changed accordingly (set the
later to approximately 3 times :c:macro:`PJSUA_MAX_CALLS`).

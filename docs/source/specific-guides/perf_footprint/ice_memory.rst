ICE Heap Usage
===============================================

.. note::

   Although this article is very old (last updated 2010), the result may still be useful
   to get a general idea about the heap size.

.. contents:: Table of Contents
   :depth: 3

This page explains how to analyze the heap usage requirement of PJNATH
and how to set various settings to reduce its consumption.

Scope
-----

This test uses **pjsua** application from the :any:`Samples </api/samples>`, with
all NAT traversal features enabled (STUN, ICE, and TURN).  Memory usage of non-PJNATH components
will not be shown nor calculated.

The tests were run on a Linux x86_64 machine. The default 64bit
alignment may have grown the memory usage slightly. The executable were
built with optimizations turned off (because some
debugging were at the same time), but this shouldn't matter for the heap usage.

PJSIP version 1.6-trunk was used. Version prior to
this didn't have configurable TURN pool memory size.

How the memory usage is calculated
-------------------------------------

Enter “**dd**” in *pjsua* menu to print all the pools being allocated by
the application. For this test though, the application has been instrumented
to dump the memory usage at certain points during execution (with
:cpp:any:`pjsip_endpt_dump()`) to make the results more consistent.

Call Setup
----------

Calculations were all done in caller side.

Caller:

::

    $ ./pjsua-x86_64-unknown-linux-gnu --null-audio --max-calls=1 \
                                       --stun-srv=stun.pjsip.org --use-ice \
                                       --dis-codec \* --add-codec pcmu \
                                       --log-file mem.log \
                                       --use-turn --turn-srv=turn.pjsip.org:33478 \
                                       --turn-user xxx --turn-passwd xxx

-  has two components (RTP and RTCP) and three candidates (host, STUN,
   and TURN) for each component in the SDP offer, making a total of six
   candidates in the offer.

Callee:

::

    $ /pjsua-x86_64-unknown-linux-gnu --null-audio --local-port 5080 \
                                      --max-calls 1 --use-ice \
                                      --stun-srv=stun.pjsip.org

-  has two components (RTP and RTCP) and one host candidate in the SDP
   answer, making a total of two candidates in the answer.

Checkpoints
-----------

Memory usage calculations were taken at the following checkpoints:

1. Startup, after TURN allocation:

   -  this will show the initial ICE objects, along with some transmit
      data buffers for TURN allocation. This checkpoint is not really
      important.

2. After :cpp:any:`pjsua_start()`:

   -  this will show additional objects created by NAT type checker.
      This would be a good indication on how much peak memory is used
      during startup.

3. Idle after initialization:

   -  memory usage should have decreased because NAT type checker and
      initial transmit data buffers would have been cleared. This shows
      the idle memory usage.

4. Right after making outgoing call:

   -  this will show the additional objects created for the session.
      There is no special significance of this checkpoint.

5. ICE negotiation is complete:

   -  this would *probably* show the peak memory usage during a call
      (and at all times), as many ICE connectivity checks are still kept
      in memory.
   -  Warning though: that might not be true. If connectivity checks
      have been running for a long time (say more than 7 seconds), some
      objects may have been cleaned.

6. 1 minute into call:

   -  memory usage should decrease as ICE connectivity checks are done.
      This shows stable memory usage in a call.
   -  Warning though: TURN was not selected by ICE on this test. When
      TURN is selected, memory usage will be greater.

Running with Default Settings
-----------------------------

Here are the heap usage (of PJNATH objects only) of pjsua, built with
default settings, at the above checkpoints:

::

   =================================== ====== ========= =============
                                       Used   Allocated Utilization %
   =================================== ====== ========= =============
   1) Startup, after TURN allocation   41,968 58,672    72
   2) After pjsua_start()              46,728 66,792    70
   3) Idle after initialization        33,744 46,528    73
   4) Right after making outgoing call 43,936 61,280    72
   5) ICE negotiation is complete      55,008 75,960    72
   6) 1 minute into call               44,568 61,792    72
   =================================== ====== ========= =============


Optimizing the Memory Usage
---------------------------

These methods below only discuss the optimization for PJNATH. For more
general memory usage optimization methods, please see :ref:`perf_footprint_guide_toc`.

These are the methods that can be used to reduce memory usage.

Reduce the size of the packet buffers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each STUN and TURN sockets/sessions would allocate memory buffer, and by
default the buffer size is quite big to accommodate wide uses of the
library. The savings from reducing these would be significant.

Sample optimized value for the affected settings (and their previous
default values in comment):

.. code-block:: c

   #define PJ_STUN_SOCK_PKT_LEN        (160+200)               /* 2000 */
   #define PJ_STUN_MAX_PKT_LEN         PJ_STUN_SOCK_PKT_LEN    /*  800 */
   #define PJ_TURN_MAX_PKT_LEN         PJ_STUN_MAX_PKT_LEN     /* 3000 */

.. note::

  (160+200): 160 is for 20ms PCMA/PCMU frame, and 200 is for
  additional STUN/TURN headers in case the frame needs to be transported
  encapsulated inside STUN/TURN frame (the actual STUN/TURN overhead most
  likely would be much lower, but I haven't checked the exact size).

.. warning::

  reducing the buffer size will limit how much you can
  send/receive of course.

Limit the number of ICE candidates, checks, components, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These would affect the ICE's *struct* size. It probably wouldn't reduce
it by much, but still, every bytes count! Sample optimized value for the
affected settings (and their default value):

.. code-block:: c

    #define PJ_ICE_ST_MAX_CAND     4           /* 8 */
    #define PJ_ICE_COMP_BITS       0           /* 1 */
    #define PJ_ICE_MAX_CAND        (PJ_ICE_ST_MAX_CAND*2)  /* 16 */
    #define PJ_ICE_MAX_CHECKS      (PJ_ICE_ST_MAX_CAND*PJ_ICE_ST_MAX_CAND) /* 32 */

.. warning::

  - reducing these constants may cause inability to run on
    particular hosts (e.g. when there are too many interfaces in the host) 
  - or to talk to certain peers (when they have too many candidates in
    their SDPs).

Reduce Log Verbosity
~~~~~~~~~~~~~~~~~~~~

Turning off level 5 logging will turn off message tracing in the STUN
session, which frees up memory by 1000 bytes per STUN session!

Suggested setting:

.. code-block:: c

    #define PJ_LOG_MAX_LEVEL       4   /* 5 */

Optimize the Pool Size
~~~~~~~~~~~~~~~~~~~~~~

Using smaller pool sizes would reduce the memory wasted by the pool, at
the expense of more calls to *malloc()*. Each memory pool used by the
libraries are tunable, but you would need to experiment with your use
case to find out the best size settings for them.

For a very lazy optimization though, just set all pool sizes to 128 (or
lower!).

.. warning::

   your app would run slower if you set the pool sizes to smaller values


All Settings
~~~~~~~~~~~~

These are the combined settings based on above methods. You can copy and
paste these to your :any:`config_site.h`:

.. code-block:: c

   /* To reduce socket buffers */
   #define PJ_STUN_SOCK_PKT_LEN        (160+200)               /* 2000 */
   #define PJ_STUN_MAX_PKT_LEN         PJ_STUN_SOCK_PKT_LEN    /*  800 */
   #define PJ_TURN_MAX_PKT_LEN         PJ_STUN_MAX_PKT_LEN     /* 3000 */

   /* Reduce the size of the respective sessions */
   #define PJ_ICE_ST_MAX_CAND          4                       /* 8 */
   #define PJ_ICE_COMP_BITS            0                       /* 1 */
   #define PJ_ICE_MAX_CAND             (PJ_ICE_ST_MAX_CAND*2)  /* 16 */
   #define PJ_ICE_MAX_CHECKS           (PJ_ICE_ST_MAX_CAND*PJ_ICE_ST_MAX_CAND) /* 32 */

   /* Log level < 5 frees up 1000 bytes of buffer in the STUN session! */
   #define PJ_LOG_MAX_LEVEL            4                       /* 5 */

   /* A lazy pool memory usage optimization.. */
   #   define PJNATH_POOL_LEN_ICE_SESS         128
   #   define PJNATH_POOL_INC_ICE_SESS         128
   #   define PJNATH_POOL_LEN_ICE_STRANS       128
   #   define PJNATH_POOL_INC_ICE_STRANS       128
   #   define PJNATH_POOL_LEN_NATCK            128
   #   define PJNATH_POOL_INC_NATCK            128
   #   define PJNATH_POOL_LEN_STUN_SESS        128
   #   define PJNATH_POOL_INC_STUN_SESS        128
   #   define PJNATH_POOL_LEN_STUN_TDATA       128
   #   define PJNATH_POOL_INC_STUN_TDATA       128

   #   define PJNATH_POOL_LEN_TURN_SESS        128
   #   define PJNATH_POOL_INC_TURN_SESS        128
   #   define PJNATH_POOL_LEN_TURN_SOCK        128
   #   define PJNATH_POOL_INC_TURN_SOCK        128

More Optimized Results
----------------------

The result, after using the :any:`config_site.h` settings above:

::

   +----------------------------------------------+--------+-----------+---------------+
   |                                              | Used   | Allocated | Utilization % |
   +==============================================+========+===========+===============+
   | 1) App initialization, after TURN allocation | 21,488 | 25,216    | 85            |
   | 2) After pjsua_start()                       | 24,440 | 28,800    | 85            |
   | 3) Idle after initialization                 | 15,568 | 18,048    | 86            |
   | 4) Right after making outgoing call          | 21,032 | 24,064    | 87            |
   | 5) After ICE negotiation is complete         | 25,368 | 29,312    | 87            |
   | 6) 1 minute into call                        | 21,464 | 24,320    | 88            |
   +----------------------------------------------+--------+-----------+---------------+


Wait, There's More!
-------------------

If memory constraint is really really tight, there is one more final
optimization that we can do, i.e. **disabling RTCP**, by declaring this
macro in :any:`config_site.h`:

.. code-block:: c

   #define PJMEDIA_ADVERTISE_RTCP          0


Since many ICE objects are duplicated across ICE components (RTCP is an ICE component), this could potentially lower the heap usage by half!

While the library currently only provides RTCP for media statistics to assist troubleshooting, still it's quite useful sometimes. You will loose RTT and TX statistics if you disable RTCP (for TX stats, you could get it in the remote endpoint of course). The system designer would need to decide whether this is a feasible optimization.



Final Result
--------------

With RTCP **turned off**, here are the final result:

::

   |                                               |   Used  |  Allocated | Utilization% |
   |-----------------------------------------------|---------|------------|--------------|
   |1) App initialization, after TURN allocation   |  11,264 |   13,184   |        85    |
   |2) After pjsua_start()                         |  14,216 |   16,768   |        85    |
   |3) Idle after initialization                   |   8,304 |    9,600   |        87    |
   |4) Right after making outgoing call            |  12,800 |   14,464   |        88    |
   |5) After ICE negotiation is complete           |  18,544 |   20,992   |        88    |
   |6) 1 minute into call                          |  13,136 |   14,720   |        89    |

It does reduce the heap consumption by close to half in some checkpoints (e.g. when idling after initialization), and significantly reduce the usages on other checkpoints.


Conclusion
-------------

We've shown that with the default settings, the **peak** heap usage per call was around **76 KB**, then we reduced it to around **29 KB**, then after the final tweak, it's down to around **21 KB** only.



.. warning::

   - please see all other warnings above
   - the number of candidates will vary on each host, hence the memory usages will vary.
   - these are just crude experimentations, just to give an idea on how to experiment further
   - once again, please bear in mind that we're only optimizing PJNATH here, other settings are left to their default values.



Appendix
--------------

This section explains briefly how ICE in PJNATH works, in order to understand where the memory is used. More information can be found in :doc:`/api/pjnath/index`. For each object mentioned below, the memory pool name format will be shown to recognize them in the memory dump output later, in square brackets. For example, "STUN session ``[stuntp%p]``" means the STUN session is using memory pool which name is formatted with printf like ``"stuntp%p"`` format, e.g. ``"stuntp0x12345678"``. The value given to the "%p" argument actually is the memory location of the object.


Objects Created During Startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ICE Media Transports**

These objects are created during PJSUA-LIB initialization, and will be kept alive throughout.

If ICE is enabled, each call will require one *PJMEDIA ICE media transport* ``[icetp%d]``, which in turn creates one *ICE stream transport* ``[icetp%d]``. Each of these will have two ICE components by default (i.e. RTP and RTCP components). For each component, one *STUN socket transport* ``[stuntp%p]`` and one *TURN socket transport* ``[udprel%p]`` will be created.

The *STUN socket transport* in turn will create one *STUN session*. which each will create another pool for incoming packet buffer. All of these use ``[stuntp%p]`` pool name format.

Each *TURN socket transport* creates one *TURN session*, which in turn create one one *STUN session*, along with its incoming packet buffer. All of these use ``[udprel%p]`` pool name format.

Sample dump output:

::

   ..
   19:04:16.888       cachpool              icetp00:      344 of      512 (67%) used
   19:04:16.888       cachpool              icetp00:     1848 of     1920 (96%) used
   19:04:16.888       cachpool      stuntp0x8218e88:     1248 of     1792 (69%) used
   19:04:16.889       cachpool      stuntp0x8218e88:      784 of      896 (87%) used
   19:04:16.889       cachpool      stuntp0x8218e88:      416 of      512 (81%) used
   19:04:16.889       cachpool      udprel0x822de60:     1184 of     1408 (84%) used
   19:04:16.889       cachpool      udprel0x822de60:     1816 of     1920 (94%) used
   19:04:16.889       cachpool      udprel0x822de60:      872 of      896 (97%) used
   19:04:16.889       cachpool      udprel0x822de60:      368 of      384 (95%) used
   19:04:16.889       cachpool      stuntp0x822f800:     1248 of     1792 (69%) used
   19:04:16.889       cachpool      stuntp0x822f800:      784 of      896 (87%) used
   19:04:16.889       cachpool      stuntp0x822f800:      416 of      512 (81%) used
   19:04:16.889       cachpool      udprel0x82308e8:     1184 of     1408 (84%) used
   19:04:16.889       cachpool      udprel0x82308e8:     1816 of     1920 (94%) used
   19:04:16.889       cachpool      udprel0x82308e8:      872 of      896 (97%) used
   19:04:16.889       cachpool      udprel0x82308e8:      368 of      384 (95%) used
   ..

Note that all the above objects are the memory dump of just a single ICE
media transport!

NAT Type Checker
~~~~~~~~~~~~~~~~~~~~~~~~~

The library will also perform NAT type detection to assist NAT related
troubleshooting. This test will run briefly (approximately ten seconds),
and will be cleaned after that. The NAT type detector's pool format is
``[natck%p]``.

Transmit Data Buffers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each outgoing STUN packet allocates one ``[tdata%p]`` pool. Normally
these buffers will be kept for few seconds due to retransmissions.

.. note::

  the SIP transmit buffer is named rather similarly: ``[tdta%p]``.
  Did you notice the difference?*

Sample dump of objects related to NAT type checker:

::

   ..
    19:04:05.499       cachpool       natck0x8233c80:     1200 of     1280 (93%) used
    19:04:05.499       cachpool       natck0x8233c80:      784 of      896 (87%) used
    19:04:05.499       cachpool       natck0x8233c80:      416 of      512 (81%) used
    19:04:05.499       cachpool       tdata0x8234ad0:      888 of     1152 (77%) used
    19:04:05.499       cachpool       tdata0x8234f70:      888 of     1152 (77%) used
    19:04:05.499       cachpool       tdata0x822da48:      888 of     1152 (77%) used
   ..


Objects Created During Call
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each call, an *ICE session* ``[tdta%p]`` will be created. Then
several individual *STUN sessions* ``[stuse%p]`` will be created, one
for each route. Recall that ICE works by *pairing* every *local
candidates* with each *remote candidates*, creating N x M possible
routes. A mechanism is defined in ICE spec to optimize the number of
possible routes, but still, each will need to be checked and each check
will require sending a request and waiting for response.

Sample memory dump with three local candidates and two remote
candidates:

::

   ..
    19:04:33.681       cachpool              icetp00:     3928 of     3968 (98%) used
    19:04:33.681       cachpool       stuse0x8231bd8:      784 of      896 (87%) used
    19:04:33.681       cachpool       stuse0x82303c0:      376 of      384 (97%) used
    19:04:33.687       cachpool       stuse0x82304c8:      784 of      896 (87%) used
    19:04:33.687       cachpool       stuse0x82326b8:      104 of      256 (40%) used
    19:04:33.687       cachpool       tdata0x822da48:      912 of     1024 (89%) used
    19:04:33.687       cachpool       tdata0x823f658:     1144 of     1280 (89%) used
    19:04:33.687       cachpool       tdata0x823fc08:     1144 of     1280 (89%) used
    19:04:33.687       cachpool       tdata0x82401b8:     1080 of     1280 (84%) used
   ..

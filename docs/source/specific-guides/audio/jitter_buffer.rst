Jitter buffer features and operations
=======================================

.. contents:: Table of Contents
    :depth: 3

The main function of a jitter buffer is to ensure that it's user receive
continuous flow of incoming frames regardless of the
jitter in the incoming packet arrival time. 

Features
----------------
Some of the features of PJMEDIA's jitter buffer are as follows.


Adaptive to jitter change
~~~~~~~~~~~~~~~~~~~~~~~~~
The jitter buffer adapts to change in network jitter,
increasing or decreasing the prefetch value and the buffering latency as
necessary.

Handle network and device jitters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The sound device's jitter/bursts, as explained in :any:`snd_dev_burst`, may
ultimately cause jitter in frame retrieval from the jitter buffer. The jitter
buffer accommodates this (device) jitter as well as jitter from
the network.

Low latency
~~~~~~~~~~~
The jitter buffer provides the minimum latency possible without sacrificing
the continuous flow requirement.

Duplicate/old frame
~~~~~~~~~~~~~~~~~~~
The jitter buffer handles the receipt of duplicate or old
frames.

A duplicate frame is a frame which has the same frame number of an
existing frame in it's buffer. In this case, the handling depends on the
value of *discarded* argument in :cpp:any:`pjmedia_jbuf_put_frame2()` function:

- PJ_TRUE, jitter buffer will ignore the duplicate frame and
  set the *discarded* argument of :cpp:any:`pjmedia_jbuf_put_frame2()` to non-zero. 
- PJ_FALSE, the jitter buffer will override the old frame with this newer
  frame, and set the *discarded* argument of :cpp:any:`pjmedia_jbuf_put_frame2()`
  to FALSE.
- if NULL, then PJ_FALSE is assumed.

An old frame (which sequence number is older than what has been played)
is always discarded, and *discarded* argument of
:cpp:any:`pjmedia_jbuf_put_frame2()` function will be set.

Non octet-aligned
~~~~~~~~~~~~~~~~~

The jitter buffer is able to store frames that are not octet/byte
aligned.

Sequence number jump/restart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The jitter buffer detects and handles large jump in frame's sequence number.

DTX
~~~
The jitter buffer handles discontinuous transmission
(DTX) without triggering restart. Note that user MAY use RTP timestamp
or sequence number as jbuf's frame sequence number,
hence DTX MAY or MAY NOT be reflected with a jump in the frame sequence
number.

Minimum prefetching
~~~~~~~~~~~~~~~~~~~
The jitter buffer can be configured with a minimum latency (prefetching).

Fixed mode operation
~~~~~~~~~~~~~~~~~~~~
The jitter buffer can be set to to operate in fixed/non-adaptive mode.
This can be done by calling :cpp:any:`pjmedia_jbuf_set_fixed()` function.

Return frame type/status
~~~~~~~~~~~~~~~~~~~~~~~~~~
The jitter buffer returns frame status in :cpp:any:`pjmedia_jbuf_get_frame()`.
See :cpp:any:`pjmedia_jb_frame_type` for possible values.



Operations
----------------
Some of the jitter buffer's operational terms will be described below.

Progressive discard
~~~~~~~~~~~~~~~~~~~~~~~
The optimal latency of the jitter buffer is defined as the minimum buffering
needed to handle current jitters (both from network and sound device).

When the latency in the jitter buffer is longer than the optimal latency, 
the jitter buffer begins to discard some frames. The progressive discard drops frames
at various rates depending on the difference between the actual latency and
the optimal/target latency.

There are some configurable macro settings that affects the discard
rate:

- :c:macro:`PJMEDIA_JBUF_PRO_DISC_MIN_BURST` and :c:macro:`PJMEDIA_JBUF_PRO_DISC_MAX_BURST`,
- :c:macro:`PJMEDIA_JBUF_PRO_DISC_T1` and :c:macro:`PJMEDIA_JBUF_PRO_DISC_T2`,
- :c:macro:`PJMEDIA_JBUF_DISC_MIN_GAP`

For example, when the optimal latency is 3 frames and
current latency is 10 frames, the jitter buffer will schedule to discard
a frame with calculations as follow: 

- Difference between actual and target latencies (we call this *overflow*) is set as ``10-3 = 7`` frames. 
- Use the following formula for calculating the target time for adjusting the
  latency (i.e: by discarding the overflow of 7 frames above): 
  
  .. code-block::
  
     T = PJMEDIA_JBUF_PRO_DISC_T1 + (PJMEDIA_JBUF_PRO_DISC_T2 -
         PJMEDIA_JBUF_PRO_DISC_T1) \* (burst_level -
         PJMEDIA_JBUF_PRO_DISC_MIN_BURST) /
         (PJMEDIA_JBUF_PRO_DISC_MAX_BURST-PJMEDIA_JBUF_PRO_DISC_MIN_BURST);

     /*
        Default settings:
        PJMEDIA_JBUF_PRO_DISC_T1 = 2000ms
        PJMEDIA_JBUF_PRO_DISC_T2 = 10000ms
        PJMEDIA_JBUF_PRO_DISC_MIN_BURST = 1
        PJMEDIA_JBUF_PRO_DISC_MIN_BURST = 100
      */

  At this point, the target time is ``2000 + (8000 * 3/99) = 2242`` msec
  or discard rate is
  ``target_time / overflow = 2242 / 7 = 320`` ms per frame. So the jitter
  buffer will discard a frame with timestamp 320ms (or frame to be played
  320ms later). There are also few notes: 
  
  - If the frame with that timestamp is not available in the jitter buffer yet, the calculation
    will be done again later. If the burst level is changed when the
    calculation is redone, the frame to discard may be changed too (no
    longer frame with timestamp 320ms).
  - If the scheduled frame timestamp
    is lower than :c:macro:`PJMEDIA_JBUF_DISC_MIN_GAP` (i.e: 200ms), the jitter
    buffer will use :c:macro:`PJMEDIA_JBUF_DISC_MIN_GAP` instead, so the discard
    rate will not be faster than :c:macro:`PJMEDIA_JBUF_DISC_MIN_GAP`.


Static discard
~~~~~~~~~~~~~~~~~~~~~~~
With this setting, the jitter buffer's latency is set as twice the
optimal level. This algorithm discard rate is fixed to :c:macro:`PJMEDIA_JBUF_DISC_MIN_GAP`, so it
will discard a frame every 200ms (the default value) until the
target latency is reached.


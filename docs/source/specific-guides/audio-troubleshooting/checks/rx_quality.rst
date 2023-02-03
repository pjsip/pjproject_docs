Check for network impairments of incoming RTP packets
========================================================

.. contents:: Table of Contents
    :depth: 2

The pjsua's ``dq`` (dump quality of current call) command from
pjsua's menu provides excellent tool for troubleshooting network
impairments of incoming RTP packets.

::

   >>> dq
    14:54:37.008        pjsua.c
     [CONFIRMED ] To: sip:user@localhost;tag=1857bde149264e2986c4aac1a26f5866
       Call time: 00h:00m:53s, 1st res in 1071 ms, conn in 1191ms
       #0 speex @16KHz, sendrecv, peer=192.168.0.66:4000
          RX pt=103, stat last update: 00h:00m:01.753s ago
             total 1.7Kpkt 72.2KB (127.2KB +IP hdr) @avg=10.6Kbps
             pkt loss=0 (0.0%), dup=0 (0.0%), reorder=0 (0.0%)
                   (msec)    min     avg     max     last
             loss period:   0.000   0.000   0.000   0.000
             jitter     :   0.000   5.506 227.000   9.812
          TX pt=103, ptime=20ms, stat last update: 00h:00m:07.871s ago
             total 0pkt 0B (0B +IP hdr) @avg 0bps
             pkt loss=0 (-1.$%), dup=0 (-1.$%), reorder=0 (-1.$%)
                   (msec)    min     avg     max     last
             loss period:   0.000   0.000   0.000   0.000
             jitter     :   0.000   0.000   0.000   0.000
         RTT msec       :   0.274   0.616   1.233   1.233

The following information is provided by the above output.

Call Identification
-------------------

The following line provides identification of the call:

::

     [CONFIRMED ] To: sip:user@localhost;tag=1857bde149264e2986c4aac1a26f5866

SIP Signaling Statistic
-----------------------

::

       Call time: 00h:00m:53s, 1st res in 1071 ms, conn in 1191ms

The line above tells us the duration of the call, the delay before the
first non-100 response is received, and the delay before the call is
confirmed.

Stream Identification
---------------------

::

       #0 speex @16KHz, sendrecv, peer=192.168.0.66:4000

The line above identifies the first stream in the session (in the
future, a session may have more than one streams, e.g. one audio stream
and one video stream), the codec being used, the direction of the
stream, and the address where RTP packets will be transmitted to.

RX Statistics
-------------

::

          RX pt=103, stat last update: 00h:00m:01.753s ago

The line above shows the expected RTP payload to be received from remote
(103) and the time when the last RTCP SR/RR packet is **sent**.

::

             total 1.7Kpkt 72.2KB (127.2KB +IP hdr) @avg=10.6Kbps

The line above shows the total number of RTP packets and total number of
RTP payload size that has been received since the media is established.

::

             pkt loss=0 (0.0%), dup=0 (0.0%), reorder=0 (0.0%)

The line above shows total number of packet loss, duplicate packets, and
out-of-order packets respectively, along with their percentage against
total received packets.

::

                   (msec)    min     avg     max     last
             loss period:   0.000   0.000   0.000   0.000

The line above shows the minimum, average, maximum, and last duration of
the loss packet, to see the maximum duration of a packet loss burst.

::

             jitter     :   0.000   5.506 227.000   9.812

The line above shows the minimum, average, maximum, and last jitter
value of incoming RTP packets.

TX Statistics
-------------

The TX statistics are calculated from the RTCP SR/RR packet received
from remote, so if remote doesn't support RTCP, the TX statistic values
will be all zero.

The following line shows whether incoming RTCP SR/RR packet has been
received from remote:

::

          TX pt=103, ptime=20ms, stat last update: 00h:00m:07.871s ago

The stat last update time above shows when the last time RTCP SR/RR was
received from remote.

RTT Estimates
-------------

The RTT estimates is calculated from the RTCP RR received from remote.
If no RTCP RR is received, the RTT would be displayed as zero.

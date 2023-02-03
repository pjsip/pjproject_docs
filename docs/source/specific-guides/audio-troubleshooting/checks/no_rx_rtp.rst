Check if RTP packets are received
====================================

Use pjsua’s **dq** (dump quality of current call) command from
pjsua’s menu to check that RTP packets are indeed received by pjsua. Use
this command after the media is established, of course.

Also make sure that current call selected is the call that you want. You
can change current call with **]** and **[** command.

Once correct call is selected and media is established, you can invoke
**dq** command like below:

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

Pay attention to this part of the report:

::

          RX pt=103, stat last update: 00h:00m:01.753s ago
             total 1.7Kpkt 72.2KB (127.2KB +IP hdr) @avg=10.6Kbps

as it shows the number of RTP packets received since the media is
established.

Make sure that the number makes sense for the duration of the call
(without VAD, normally we’ll have about 50 packets received per second).

If the number is zero, then we’re not receiving any RTP packets. There
could be problems with the network, or NAT, or firewall, or something
else, which is not related to the sound device.

If the number is too low, it’s possible that remote is transmitting
silence frames, which of course will be rendered as silence in the
speaker.

What to do if no RTP packet is received
-------------------------------------------

If no RTP packet is received, first thing to check is the log file, see
if there are any warnings or errors, especially related to media transport
and SDP negotiation.

Another very common problem is NAT and/or firewall. The
:any:`/specific-guides/network_nat/nat_guide` page describes some
solutions to make the application works behind NAT.

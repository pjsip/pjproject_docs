Check that audio is transmitting and to correct remote address
====================================================================

Use pjsua's ``dq`` (dump quality) command to see the address where RTP packets are transmitted to:

::

        >>> dq
        19:01:38.878        pjsua.c
        [CONFIRMED ] To: sip:localhost;tag=213e15bcf98b4c0394a402881e885431
        Call time: 00h:01m:44s, 1st res in 1452 ms, conn in 1682ms
        #0 iLBC @8KHz, sendrecv, peer=192.168.0.66:4000
        RX pt=117, stat last update: 00h:00m:01.943s ago
                total 4.3Kpkt 164.0KB (302.2KB +IP hdr) @avg=12.5Kbps
                pkt loss=0 (0.0%), dup=0 (0.0%), reorder=0 (0.0%)
                        (msec)    min     avg     max     last
                loss period:   0.000   0.000   0.000   0.000
                jitter     :   0.125  15.779 1695.000   1.250
        TX pt=117, ptime=20ms, stat last update: 00h:00m:09.304s ago
                total 5.1Kpkt 197.2KB (363.4KB +IP hdr) @avg 15.0Kbps
                pkt loss=0 (0.0%), dup=0 (0.0%), reorder=0 (0.0%)
                        (msec)    min     avg     max     last
                loss period:   0.000   0.000   0.000   0.000
                jitter     :  14.750  15.570  18.875  18.875
        RTT msec       :   0.854  24.516 125.000  18.783


The **first important** check is the number of packets transmitted (by us):

::

        TX pt=117, ptime=20ms, stat last update: 00h:00m:09.304s ago
                total 5.1Kpkt 197.2KB (363.4KB +IP hdr) @avg 15.0Kbps

The above output shows that we've transmitted 5.1K packets for a total of
197.2KB. Check both the number of packets and the total size (it is possible
that many packets are transmitted, but they are all silence packets).

If the number of packets transmitted is low, possible causes include:

- call is not connected to the microphone
- microphone level is too low and transmission is cut by VAD

The **next important** part is this line:

::

    #0 iLBC @8KHz, sendrecv, peer=192.168.0.66:4000


which tells us that RTP packet is transmitting to IP address 192.168.0.66 and to port 4000.

Verify that this is indeed the correct address where remote is expecting incoming RTP packets.
Especially when remote party is on the other side of Internet, make sure the
address is not private as above.

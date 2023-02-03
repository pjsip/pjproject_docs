Checking that codec is negotiated properly by both parties
==========================================================

Normally both parties should agree on same codec to be used for the
session (call), but sometimes one or both party/parties get it wrong and the call
ends up using different codec to encode/decode the packets.

Potential Problems with Codec Negotiation
-----------------------------------------------

Different iLBC mode used by either party
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

iLBC has two framing modes: 20ms or 30ms. Each party specifies which
framing mode it wants to **receive** by specifying the following line in
the SDP:

::

   a=fmtp:117 mode=20

PJMEDIA SHOULD allow different modes to be used for TX and RX, and
it obeys the fmtp mode that the remote party wants to receive and
that it indicates in the SDP that it sends. However, some user agents
might not be able to do this.

To verify whether this is or isn’t the case, experiment with
changing the iLBC mode that is used by pjsua with using
``--ilbc-mode=20`` or ``--ilbc-mode=30`` command line argument.
This will change the mode preference that is advertised by PJSIP in the
outgoing SDP.

Wrong codec negotiation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a worse case, it is also possible that codec negotiation has gone totally wrong
in either party, and both parties end up with completely different
codec for the call. If PCMA/PCMU codec negotiation mismatches, both may
end up with a noisy audio.

More than one codecs are active in remote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
While it is okay, according to the standard, to answer an SDP offer with
more than one active codecs in a single media (m=) line, currently PJMEDIA
does not support having two codecs active in the same stream. Thus when it
sees such SDP answer, it will create an updated offer with just one codec
from the answer.

While we don't anticipate this to create the noisy problem, just be aware
of this mechanism and keep an eye on potential side effects.

Checking which codec is being used by pjsua
-------------------------------------------

Use pjsua’s ``dq`` (dump quality) command from pjsua menu to check
which codec is being used for the call:

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

The important bit of above output is this line:

::

       #0 iLBC @8KHz, sendrecv, peer=192.168.0.66:4000

which tells us that iLBC is being used for the call (although unfortunately
it doesn’t tell the mode).

Try to use other codec
----------------------

If you know what codec is likely to be used by remote party, you can
force pjsua to *prefer* certain codec to be used, by using
``--add-codec NAME`` command. The NAME is the shortest string that uniquely
identifies the codec, such as:

* pcma 
* pcmu 
* speex/8000 
* speex/16000 
* speex/32000 
* ilbc 
* etc.

For iLBC, you can change the RX mode used by pjsua with using
``--ilbc-mode=20`` or ``--ilbc-mode=30`` command line argument.


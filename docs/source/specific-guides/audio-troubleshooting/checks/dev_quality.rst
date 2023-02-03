Checking the quality of the sound device
========================================

.. contents:: Table of Contents
   :depth: 3


In some cases, some of the audio problems may come from the sound
device itself, causing problems such as:

- :any:`/specific-guides/audio-troubleshooting/problems/audio_dropouts`, 
- :any:`/specific-guides/audio-troubleshooting/problems/audio_breaking_up`

It may not be the sound device itself that is causing the problem, but
could be the operating system driver for the device. For example, on
Linux, the ALSA driver tends to have a very good quality while using OSS
driver for the same device would give a less satisfactory result.

It is also observed from the mailing list discussions that many embedded
Linux device with on-board sound adapter give a bad audio quality with
OSS driver, although normally it would play a WAV file fine. We conclude
that these sound adapter (or the driver) is not really designed for
streaming, bidirectional communication like audio call, but rather for
trivial tasks like playing a file to the speaker.

Sound Device Problems
---------------------

Some problems with sound device are as follows.

Jitter
~~~~~~

Common problem with most sound device is the jitter. Where for example
PJMEDIA expects audio frames to be delivered at exactly 20ms interval,
the sound device (or driver) may deliver it at 10ms, 10ms, 30ms, 30ms,
etc. Normally the total number of frames delivered will match the clock
rate (i.e. there's no lost frames), but it's just that these frames are
not delivered in timely manner.

Audio jitter in the capture direction will cause outgoing RTP packet
to be delivered in uneven time. This shouldn't cause too much problem
because remote should be able to accomodate the jitter.

Audio jitter in the playback direction should be okay too. Much worse
problem is audio burst (see below).

Burst
~~~~~

A worsening problem with the jitter is bursting, where the sound device
(or driver) delivers the audio frames in burst and then followed by
silent period, and burst again. If the sound device is open in
full-duplex mode, this would normally cause the recorder callback to be
called in burst of several calls, then followed by burst call to the
playback callback, and back to burst call to the recorder callback, and
so on.

PJMEDIA should be capable of handling audio burst to some level, 
as explained in :ref:`snd_dev_burst` in  :any:`/specific-guides/media/audio_flow`. 


Underflows Overflows
~~~~~~~~~~~~~~~~~~~~

Another problem with audio application is underflows and overflows,
where application is not processing the audio frames quickly enough.
When underflow or overflow occurs in the playback direction, you would
hear a click sound in the speaker.

The PortAudio audio abstraction in PJMEDIA prints the number of
underflow/overflow when the sound device is closed. With pjsua, you need
to set the log level to 5 (``--app-log-level 5``), and when the
application exits the underflow/overflow statistic will be printed to
console/log.

Clock drifting
~~~~~~~~~~~~~~

A not so common problem with some sound device is clock drifting, where
the sound device is not delivering audio samples at the exact clock
rate. For example, when the sound device is opened at 8KHz, the sound
device may deliver a little less or more than 8000 samples per second.

Testing the Sound Device
------------------------
Use **pjsystest** to test the performance of the sound device. See
:any:`/specific-guides/audio-troubleshooting/checks/pjsystest` for more information.

Specifically, run *pjsystest* **Device Test** (menu **01**) to test
the audio device's burst and clock drifts problem. Below is a sample 
output of *Device Test*:

::

    Audio Device Test
    Here are the audio statistics:
    Rec : interval (min/max/avg/dev)=
            0/31/20/11 (ms)
        max burst=2
    Play: interval (min/max/avg/dev)=
            10/26/20/1 (ms)
        burst=2
    There could be 1 problem(s) with the sound device:
    1: Clock drifts detected. Capture is 16 samples/sec faster than the playback device


From the results above, the burst is good, and there is a little clock
drifts, both should be able to be handled by PJMEDIA.
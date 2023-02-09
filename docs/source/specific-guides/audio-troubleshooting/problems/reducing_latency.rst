Reducing audio latency
=========================
.. contents:: Table of Contents
    :depth: 2

Overview
----------------
The end to end audio latency consists of the following components: 

#. The latency of the sound capture. 
#. Codec latency on both sender and receiver. 
#. Other algorithmic latency (such as AEC or sample rate conversion). 
#. Network latency. 
#. Jitter buffering on the receiver end.
#. The latency of the sound playback.


Optimizing sound device latency
-------------------------------------
Sound device adds latency in two ways. First is the latency due to the
use of audio playback and recording buffers, and second is latency due
to buffering by pjmedia components (such as the conference bridge) to
accommodate sound device's jitter/bursts characteristic (see :any:`snd_dev_burst`).

Both the latency and jitter/bursts characteristics of the sound device
can be analyzed with :any:`/specific-guides/audio-troubleshooting/checks/pjsystest`.

The sound device buffer sizes can be set by using the following settings:

- PJSUA-LIB:
  
  - :cpp:any:`pjsua_media_config::snd_rec_latency`, which default value
    is :c:macro:`PJMEDIA_SND_DEFAULT_REC_LATENCY`
  - :cpp:any:`pjsua_media_config::snd_play_latency` , which default value
    is :c:macro:`PJMEDIA_SND_DEFAULT_PLAY_LATENCY`
  - :cpp:any:`pjsua_snd_set_setting()` with :cpp:any:`PJMEDIA_AUD_DEV_CAP_INPUT_LATENCY`
    and :cpp:any:`PJMEDIA_AUD_DEV_CAP_OUTPUT_LATENCY` capabilities.

- PJSUA2:

  - :cpp:any:`pj::MediaConfig::sndRecLatency` and 
    :cpp:any:`pj::MediaConfig::sndPlayLatency` (similar to PJSUA-LIB settings
    above)
  - :cpp:any:`pj::AudDevManager::setInputLatency()` and 
    :cpp:any:`pj::AudDevManager::setOutputLatency()`

The default buffer size settings have proven to be good to get the balance between
stability and latency, but you can experiment with changing the values to improve
latency.

In our experience, the performance (latency and burst/jitter characteristics)
of the sound device is pretty much given and the only way to change it is
to change the *driver* type. If the platform offers more than one sound device
implementations, for example, :ref:`jnisound`, :ref:`opensl`, and :ref:`oboe`
implementations are available for :doc:`Android </get-started/android/index>`
platform, experiment with each and use one with performance most suitable for your
application.


Codec latency
--------------------
Codec latency is determined by the codec algorithm and its ``ptime``, but
usually it shouldn't add too much latency, around 10 to 30 ms. 


Use audio switchboard
-------------------------
The :doc:`conference bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>` 
adds significant buffering to accommodate jitter/bursts
from the sound device. See :any:`snd_dev_burst` for more information.

If conferencing is not needed, consider replacing it with the
:any:`/specific-guides/audio/switchboard`.

Choosing lower audio frame length
------------------------------------
.. warning::

        This method is now deprecated.

PJSIP now uses :doc:`Adaptive Delay Buffer </api/generated/pjmedia/group/group__PJMED__DELAYBUF>` to
automatically learn the amount of buffers required to handle the burst.
The semantic of :c:macro:`PJMEDIA_SOUND_BUFFER_COUNT` has been changed, and rather
now it means the maximum amount of buffering that will be handled by the
delay buffer. Lowering the value will not affect latency, and may cause
unnecessary :doc:`WSOLA </api/generated/pjmedia/group/group__PJMED__WSOLA>`
processing (to discard the excessive frames because
the buffer is full) and may even produce audio impairments, hence it is
no longer recommended.


Optimizing Jitter Buffer Latency
----------------------------------
The jitter buffer algorithm is constantly trying to get the best latency for
the current jitter conditions, hence usually there is no tuning needed to get
better latency.

For reference, jitter buffer settings are in :cpp:any:`pjsua_media_config`
and :cpp:any:`pj::MediaConfig` (look for settings with ``jb`` prefix).


Other sources of latency
-------------------------
Other sources of latency include:

- The default resampling algorithm in PJMEDIA adds about 5 ms latency.
- The AEC may introduce some latency, but we don't know exactly by 
  how much. 
- The network latency itself.

Audio drop-outs or "stutters"
=================================
The symptom is audio is sounding like it's skipping some frames.

For a sample audio, play this `stutter.wav <../../../_static/stutter.wav>`__ file [1]_. 
Hear the stutters at 2.5, 3.8, and 8.8 second.


Checklists:

#. :any:`/specific-guides/audio-troubleshooting/checks/loopback`: check whether the symptom is observable
   when looping the microphone to the speaker locally.
#. :any:`/specific-guides/audio-troubleshooting/checks/dangling_pbx_call`. A dangling call is call that 
   is left active in the PBX because previous (*pjsua*) application has terminated
   abruptly.
#. :any:`Check for high network jitter, packet loss, etc. </specific-guides/audio-troubleshooting/checks/rx_quality>`
#. :any:`/specific-guides/audio-troubleshooting/checks/cpu`
#. Try to enlarge :c:macro:`PJMEDIA_SOUND_BUFFER_COUNT` value by setting it in your 
   :any:`config_site.h`. Increase it to, say, 16, and see if it fixes the problem. But be 
   aware that enlarging this buffer will increase the audio latency, so find a minimum value
   where the sound quality doesn't break.
#. :doc:`/specific-guides/audio-troubleshooting/checks/dev_under_overflow`


.. [1] audio file courtesy of Chen Huan <chenhuan at sict.ac.cn> who managed to convince his 
       girlfriend to record the audio for testing :)

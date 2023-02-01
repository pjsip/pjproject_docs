Audio is breaking up
===========================

The symptom is the audio from remote party is breaking up or audio from playing a file 
locally is breaking up.

Checklists:

#. It's always recommended to check whether the problem exists with the 
   latest git version of the libraries.
#. Check that no other application is using the devices. It is common to not 
   be able to use sound device when the device is being used by other 
   applications.
#. :any:`/specific-guides/audio/checks/cpu`
#. :any:`/specific-guides/audio/checks/dangling_pbx_call`. A dangling call is call that 
   is left active in the PBX because previous (*pjsua*) application has terminated
   abruptly.
#. :any:`Check for high network jitter, packet loss, etc. </specific-guides/audio/checks/rx_quality>`. 
#. Check if audio is breaking up when playing file locally:
   :any:`/specific-guides/audio/checks/play_wav`
#. Check if the breakup is coming from the sound device:
   :any:`/specific-guides/audio/checks/dev_quality`
#. Check if local audio is breaking up by looping back microphone signal to the speaker:
   :any:`/specific-guides/audio/checks/loopback`

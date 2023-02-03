Loud static noise
================================================================
Checklists:

#. Check that audio device is functioning properly and noise is not heard when looping microphone to the speaker,
   by following: :any:`/specific-guides/audio-troubleshooting/checks/loopback`
#. :any:`Check that codec is negotiated properly by both parties </specific-guides/audio-troubleshooting/checks/codec_nego>`.
#. Be mindful with combination of sampling rate and ptime that causes non-whole number of samples,
   such as:

   - 10ms of 22050 Hz (220.5 samples), 
   - 20ms of 11025 Hz (also 220.5 samples).



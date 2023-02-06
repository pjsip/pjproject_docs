Soft/quiet noise
================================================================
Checklists:

#. Check that you're using the latest (git) version of the libraries.
#. :any:`Check whether you have this noise when looping the microphone to the speaker locally </specific-guides/audio-troubleshooting/checks/loopback>`: 
   If yes, then the noise is
   probably introduced by your sound device (it's quite common with onboard sound 
   adapters).
#. Be mindful with combination of sampling rate and ptime that causes non-whole number of samples.
   See :any:`/specific-guides/audio-troubleshooting/checks/problematic_clock_rate`.

Check for audio underflows/overflows
==========================================

.. note::

        This only applies when PortAudio is chosen for the audio
        device backend.

Check for audio underflows/overflows, by looking at the log (at log level 5) 
when the sound device is closed. 

Look for line similar to this in the log:

::

   23:33:43.391 pasound.c Closing /dev/dsp: 0 underflow, 0 overflow


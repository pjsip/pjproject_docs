How to record audio with pjsua
==============================
Follow this guide to record any audio coming into the conference bridge to a WAV file.

#. Run pjsua with additional ``--rec-file`` argument:

   .. code-block:: shell

       $ ./pjsua --rec-file OUTPUT.WAV

   .. note::

      Make sure *pjsua* quits properly before reading the WAV file,
      otherwise the WAV file may be detected as corrupt because
      the header does not contain the correct information.

#. See that the file has been registered to the conference
   bridge with ``cl`` command:

   ::

      >>> cl
      Conference ports:
      Port #00[16KHz/10ms] Primary Sound Capture Driver  transmitting to:
      Port #01[16KHz/10ms]           OUTPUT.WAV  transmitting to:

#. Make a call and establish media as usual.
#. When the call is established, normally it is
   "connected" to the sound device in the bridge. This can be confirmed
   with the ``cl`` command below:

   ::

      >>> cl
      Conference ports:
      Port #00[16KHz/10ms] Primary Sound Capture Driver  transmitting to: #2
      Port #01[16KHz/10ms]           OUTPUT.WAV  transmitting to:
      Port #02[16KHz/20ms]   sip:user@localhost  transmitting to: #0

#. Now connect whatever port(s) to record to
   the OUTPUT.WAV port. For example, this command would record the audio
   from remote call to the WAV:

   ::

      >>> cc 2 1
       09:40:08.969   conference.c Port 2 (sip:user@localhost) transmitting to port 1
      (OUTPUT.WAV)
      Success

#. You can also, for example, record the audio from the microphone to
   the WAV file at the same time:

   ::

      >>> cc 0 1
       09:40:47.894   conference.c Port 0 (Primary Sound Capture Driver) transmitting
      to port 1 (OUTPUT.WAV)
      Success

   In this case, the audio from both the call and the microphone will be
   first mixed in the conference bridge before it is recorded to the WAV
   file. 
   
#. Now both the audio from the remote call and the audio from the
   microphone will be recorded to the WAV file, as can be seen with
   ``cl`` command:

   ::

      >>> cl
      Conference ports:
      Port #00[16KHz/10ms] Primary Sound Capture Driver  transmitting to: #2 #1
      Port #01[16KHz/10ms]           OUTPUT.WAV  transmitting to:
      Port #02[16KHz/20ms]   sip:user@localhost  transmitting to: #0 #1

   As can be seen from above output, both the sound device (port 0) and the
   call (port 2) are both transmitting to the WAV file, thus output from
   both will be mixed and recorded to the WAV file.

#. Note that when debugging audio problem, it's probably best **not** to mix the audio
   from the problematic source with other sources so that we can be clear
   about the source of the problem.

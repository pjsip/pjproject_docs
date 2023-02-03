Checking by playing a WAV file
===========================================================

Play WAV file with pjsua
----------------------------------------

An easy way to check if speaker is functioning properly is by using
**pjsua** to play a WAV file to the speaker, with these easy steps:

#. Find any WAV file with the following specification:

   -  any clock rate
   -  **mono** (not stereo)
   -  16bit, PCM sample
#. Run pjsua with the file:

   .. code-block:: shell

       $ ./pjsua --play-file THEFILE.WAV

#. Check that the file is registered to the bridge:

   ::

     >>> cl
     Conference ports:
     Port #00[16KHz/10ms] Primary Sound Capture Driver  transmitting to:
     Port #01[16KHz/10ms]          THEFILE.WAV  transmitting to:

#. Play the file to the speaker:

   ::

     >>> cc 1 0
     Success
     
#. Done. You should hear the file played to the speaker.

If you couldn’t hear the file played properly to the speaker, then
follow the next step.

If first check fails, try playing the WAV file with playfile sample
-------------------------------------------------------------------

If the file is **not** playing properly with pjsua, then try playing the
file with :source:`pjsip-apps/src/samples/playfile.c` sample. The *playfile* sample binary should
be put in ``pjsip-apps/bin/samples`` directory after the samples project
is successfully built.

To play a WAV file with *playfile* sample:

.. code-block:: shell

    $ ./playfile THEFILE.WAV

The difference between pjsua and playfile program is the lack of
conference bridge in playfile.

If no audio is heard with both pjsua and playfile
-----------------------------------------------------

Chances are other apps are unable to play to that sound device either. Please follow
general sound device troubleshooting for your operating system. Some of the
problems may include:

- the speaker is not working properly
- the level is set too low
- the WAV file contains blank recording


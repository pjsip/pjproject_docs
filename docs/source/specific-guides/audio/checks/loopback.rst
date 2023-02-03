Check by looping back microphone to speaker
=================================================================
The easiest way to check if both microphone and speaker are functioning properly is 
by using **pjsua** and looping the microphone to the speaker in the conference bridge: 

#. run *pjsua*, e.g:
    - for desktop, *pjsua* sample app is automatically built, so simply run it from console:

      .. code-block:: shell

         $ ./pjsua

    - for mobile platforms, *pjsua CLI* sample app usually needs to be built manually 
      (check :any:`get_started_toc` wiki of the platform, e.g: 
      :doc:`/get-started/android/index`,  or :doc:`/get-started/ios/index`, 
      run it on the device and start a telnet session to *pjsua CLI* app running on the device 
      from desktop console, e.g:

      .. code-block:: shell

          $ telnet 192.168.1.101 2323

      Wait until telnet session is established. Check 
      :any:`/specific-guides/other/cli_cmd` for more info about pjsua CLI.

#. loopback microphone to the speaker:

   .. code-block:: shell
        
      >>> cc 0 0



Now whatever captured in your microphone will be played-back locally to your speaker. 

.. note::

   This step is not recommended for PDA application since on PDA, the echo suppressor 
   will cut the microphone signal once it detects that something is playing in the 
   speaker.



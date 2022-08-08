PJMEDIA Samples
---------------------
Below are PJMEDIA samples. Open the source file for more information.

.. list-table::
   :header-rows: 1

   * - Sample
     - Library(s)
     - Description
   * - `aectest.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/aectest.c>`_
     - PJMEDIA
     - Tests the effectiveness of :doc:`the AEC </api/generated/pjmedia/group/group__PJMEDIA__Echo__Cancel>`
       in PJMEDIA by feeding it with playback and (simulated) captured WAV files from the microphone, 
       and outputs the results of AEC processing as another WAV file.
   * - `auddemo.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/auddemo.c>`_
     - PJMEDIA-(core, audiodev)
     - Interactively demonstrates operations to the sound devices, such as listing, refreshing,
       recording, playback, getting/setting latencies, and performing timing tests.
   * - `aviplay.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/aviplay.c>`_
     - PJMEDIA-(core, codec, audiodev, videodev)
     - AVI media player.
   * - `confbench.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/confbench.c>`_
     - PJMEDIA
     - Internal utility to benchmark the conference bridge
   * - `confsample.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/confsample.c>`_
     - PJMEDIA
     - Interactive demo of the :doc:`conference bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`, 
       allowing mixing, audio level setting, and audio level meter.
   * - `encdec.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/encdec.c>`_
     - PJMEDIA-(core, codec)
     - Encoding and decoding WAV file to demonstrate how to use the
       :doc:`codec framework </api/generated/pjmedia/group/group__PJMEDIA__CODEC>`.


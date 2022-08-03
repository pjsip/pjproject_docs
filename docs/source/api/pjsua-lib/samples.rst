PJSUA-LIB Samples
------------------
.. list-table::
   :header-rows: 1

   * - Sample
     - Library(s)
     - Description
   * - `simple_pjsua.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/simple_pjsua.c>`_
     - PJSUA-LIB
     - This small app (~200 LoC) is a fully functional SIP user agent, supporting 
       registration and audio call (P.S. you need to modify credentials in the source code to
       register). Use this sample to study the general pattern and flow of PJSUA-LIB.
   * - `pjsua <https://github.com/pjsip/pjproject/tree/master/pjsip-apps/src/pjsua/>`_
     - PJSUA-LIB
     - This is the reference implementation of PJSIP, demonstrating everything that PJSIP
       has to offer. We use this for any testing and for actual communications as well.
   * - `pjsystest <https://github.com/pjsip/pjproject/tree/master/pjsip-apps/src/pjsystest/>`_
     - PJSUA-LIB
     - Perform series of tests to detect problems and measure the performance of the system,
       especially the audio subsystem, such as playback test, recording test, measuring audio 
       device performance such as bursts, latency, and drifts, AEC performance, as well as
       displaying basic audio system information.
   * - `vidgui <https://github.com/pjsip/pjproject/tree/master/pjsip-apps/src/vidgui/>`_
     - PJSUA-LIB
     - GUI user agent supporting video. Requires Qt toolkit.





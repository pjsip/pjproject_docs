PJSIP Samples
---------------------
.. list-table::
   :header-rows: 1

   * - Sample
     - Library(s)
     - Description
   * - `sipstateless.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/sipstateless.c>`_
     - PJSIP (core)
     - This is the simplest SIP application if using the low level PJSIP (core) library.
       It demonstrate the core concept of PJSIP handling of SIP messages using 
       :doc:`PJSIP module </api/generated/pjsip/group/group__PJSIP__MOD>`.

       This simple program responds any incoming requests (except ACK, of course!)
       with 501/Not Implemented. It supports UDP and TCP.
   * - `stateless_proxy.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/stateless_proxy.c>`_,
       `proxy.h <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/proxy.h>`_
     - PJSIP (core)
     - Simple implementation of pure stateless proxy as spec-ed by RFC 3261. 
   * - `stateful_proxy.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/stateful_proxy.c>`_,
       `proxy.h <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/proxy.h>`_
     - PJSIP (core)
     - Simple implementation of stateful proxy as spec-ed by RFC 3261. 
   * - `sipecho.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/sipecho.c>`_
     - PJSIP-UA
     - Accepts all incoming calls with SDP to make caller send media to itself. Useful for
       auto-responding test server. Supports UDP, TCP, IPv6.
   * - `invtester.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/invtester.c>`_
     - PJSIP-UA
     - Utility to send INVITE or re-INVITE without SDP, for testing.
   * - `pjsip-perf.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/pjsip-perf.c>`_
     - PJSIP-UA
     - SIP call generator/load testing/performance measurement, can be used as both server and client. 
       Only performs signaling (SIP and SDP negotiation) and does not do RTP.
   * - `simpleua.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/simpleua.c>`_,
       `util.h <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/util.h>`_
     - PJSIP-UA, PJMEDIA (Codec, AudioDev, VideoDev)
     - Full implementation of a SIP user agent, supporting SIP, SDP, RTP, audio, and video, with
       actual sound device and camera, using the low level PJSIP and PJMEDIA libraries.
   * - `siprtp.c <https://github.com/pjsip/pjproject/blob/master/pjsip-apps/src/samples/siprtp.c>`_
     - PJSIP-UA, PJMEDIA
     - A specialized program to measure audio quality under load by using RTCP feedback. Can be used to
       generate/handle load testing with many calls.

       This program establishes SIP INVITE session and media, and calculate
       the media quality (packet lost, jitter, rtt, etc.). Unlike normal
       pjmedia applications, this program bypasses all pjmedia stream
       framework and transmit encoded RTP packets manually using own thread.



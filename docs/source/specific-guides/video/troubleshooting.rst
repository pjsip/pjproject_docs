Video quality troubleshooting
=========================================
For video quality problems, the steps are as follows:

#. For lack of video, check the account's :cpp:any:`pj::AccountVideoConfig`,
   especially the fields :cpp:any:`pj::AccountVideoConfig::autoShowIncoming`
   and :cpp:any:`pj::AccountVideoConfig::autoTransmitOutgoing`.

   More about the call-side video API is explained in
   :any:`/specific-guides/video/users_guide/call_video` (for PJSUA-LIB)
   or :any:`/pjsua2/using/media_video` (for PJSUA2).
#. Check local video preview using PJSUA API as described under
   :any:`/specific-guides/video/users_guide/call_video`.
#. Since video requires a larger bandwidth, we need to check for network
   impairments as described in
   :any:`/specific-guides/audio-troubleshooting/checks/rx_quality`. The
   document is for troubleshooting audio problems but it applies to video
   as well.
#. :any:`/specific-guides/audio-troubleshooting/checks/cpu`. If the CPU
   utilization is too high, you can try a different (less CPU-intensive)
   video codec or reduce the resolution/fps.

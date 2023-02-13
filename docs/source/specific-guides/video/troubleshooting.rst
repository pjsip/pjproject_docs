Video quality troubleshooting
=========================================
For video quality problems, the steps are as follows:

#. For lack of video, check account's :cpp:any:`pj::AccountVideoConfig`, especially the
   fields :cpp:any:`pj::AccountVideoConfig::autoShowIncoming` and
   :cpp:any:`pj::AccountVideoConfig::autoTransmitOutgoing`. 
   
   More about the video API is  explained in :any:`/specific-guides/video/users_guide`
   (for PJSUA-LIB) or :any:`/pjsua2/using/media_video` (for PJSUA2).
#. Check local video preview using PJSUA API as described in :any:`/specific-guides/video/users_guide`.
#. Since video requires a larger bandwidth, we need to check for network impairments as described in
   :any:`/specific-guides/audio-troubleshooting/checks/rx_quality`.
   The document is for troubleshooting audio problem but it applies for video as well.
#. :any:`/specific-guides/audio-troubleshooting/checks/cpu`.
   If the CPU utilization is too high, you can try a different 
   (less CPU-intensive) video codec or reduce the resolution/fps..

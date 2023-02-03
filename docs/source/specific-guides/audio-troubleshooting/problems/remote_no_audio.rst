No audio is heard by remote party
===========================================

Checklists:

#. :any:`/specific-guides/audio-troubleshooting/checks/device`
#. :any:`Check that microphone is functioning properly</specific-guides/audio-troubleshooting/checks/loopback>`
   by looping-back microphone to speaker device.
#. Check that no other application is using the sound devices. It is common to not be 
   able to use sound device when other application is using the device.
#. :any:`Check that the microphone is connected to the call in the conference bridge </specific-guides/audio-troubleshooting/checks/conf_connections>` 
#. :any:`/specific-guides/audio-troubleshooting/checks/tx_addr`.
#. Use *pjsua* on the remote side to check that packets are received. Follow 
   :any:`/specific-guides/audio-troubleshooting/checks/no_rx_rtp` on how to use *pjsua* to verify 
   receipt of incoming RTP packets.
#. :any:`/specific-guides/audio-troubleshooting/checks/cpu`


No audio is heard by remote party
===========================================

Checklists:

#. :any:`/specific-guides/audio/checks/device`
#. :any:`/specific-guides/audio/checks/loopback`. Check that microphone is functioning 
   properly by looping-back microphone to speaker device.
#. Check that no other application is using the sound devices. It is common to not be 
   able to use sound device when other application is using the device.
#. :any:`/specific-guides/audio/checks/conf_connections`. Check that the microphone is
   connected to the call in the conference bridge.
#. :any:`/specific-guides/audio/checks/tx_addr`.
#. Use *pjsua* on the remote side to check that packets are received. Follow 
   :any:`/specific-guides/audio/checks/no_rx_rtp` on how to use *pjsua* to verify 
   receipt of incoming RTP packets.
#. :any:`/specific-guides/audio/checks/cpu`


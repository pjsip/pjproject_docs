Check for dangling call in PBX
==================================
Sometimes, when a call party is terminated for some reason, the call is 
still left active in the PBX. When subsequent call (*pjsua*) is started, this new application 
instance will receive two RTP streams simultaneously from the PBX: once from current call, and 
one from the dangling call. This would definitely cause audio breakup problem in pjsua.

This happens because *pjsua* by default will use UDP port 4000 for the RTP port, so both calls 
(the dangling and active call in the PBX) will send to the same port 4000 of *pjsua*.

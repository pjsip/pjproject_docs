Network / IP change leaves video black
========================================

When the host's IP address changes (Wi-Fi ↔ cellular, VPN
connect, docking, …), media transports bound to the old address
need to be moved to the new one. Audio usually recovers cleanly
via PJSIP's IP-change handler, but video sometimes ends up black
on one or both sides — typically because the remote decoder lost
its decoder state when the link broke.

Recovery flow:

#. **Trigger PJSIP's IP-change handling** with
   :cpp:any:`pjsua_handle_ip_change()`, configured via
   :cpp:any:`pjsua_ip_change_param` (use
   :cpp:any:`pjsua_ip_change_param_default()` to populate
   defaults). This restarts the listener (if requested) and
   shuttles existing calls onto the new address through
   re-INVITE/UPDATE.

#. **If video still doesn't auto-recover after the IP change
   completes**, send an explicit re-INVITE with the current call
   setting:
   :cpp:any:`pjsua_call_reinvite2()` /
   :cpp:any:`pjsua_call_update2()`. This forces a fresh SDP
   negotiation that includes the new transport addresses.

#. **Once the stream is live again, force a keyframe**. The
   peer's previous decoder context is invalid after the break.
   Either:

   - request a keyframe from the peer (the library does this
     automatically via PLI/FIR if the decoder reports missing
     keyframes), or
   - force our outgoing keyframe so the peer can re-anchor:
     :cpp:any:`pjsua_call_set_vid_strm()` with
     :cpp:any:`PJSUA_CALL_VID_STRM_SEND_KEYFRAME <pjsua_call_vid_strm_op::PJSUA_CALL_VID_STRM_SEND_KEYFRAME>`.

#. **Verify the new RTP path actually delivers packets.** If a
   firewall or NAT on the new network blocks the negotiated UDP
   port, you'll see no RTP at all on the new path. Apply the same
   checks as for the audio side:
   :doc:`/specific-guides/audio-troubleshooting/checks/no_rx_rtp`.

For mid-call stream changes after a network event, see
*Modifying video during a call* in
:any:`/pjsua2/using/media_video`.

Related: :doc:`mobile_bg_fg`.

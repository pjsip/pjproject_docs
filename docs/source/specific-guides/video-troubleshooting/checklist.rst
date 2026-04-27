Video troubleshooting checklists
##################################

Video-specific checks
=====================

.. toctree::
   :maxdepth: 1
   :glob:

   checks/*


Shared with audio troubleshooting
==================================

The following checks under :ref:`Audio Troubleshooting
<audio_troubleshooting_toc>` are equally applicable to video calls
and are referenced from the symptom-based pages above:

- :doc:`/specific-guides/audio-troubleshooting/checks/no_rx_rtp` —
  is RTP being received at all?
- :doc:`/specific-guides/audio-troubleshooting/checks/rx_quality` —
  network impairments (loss / jitter / late) on the receive path.
- :doc:`/specific-guides/audio-troubleshooting/checks/tx_addr` —
  is the local RTP send address something the peer can actually
  reach?
- :doc:`/specific-guides/audio-troubleshooting/checks/cpu` — is
  the host CPU a bottleneck?
- :doc:`/specific-guides/audio-troubleshooting/checks/loopback` —
  send to self to narrow down sender vs receiver. The audio
  technique applies to video by analogy (capture device →
  conference → renderer).

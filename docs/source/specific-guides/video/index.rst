FFMPEG
=======================
See :ref:`guide_ffmpeg`.


.. _guide_libyuv:

Integrating libyuv
====================
See https://github.com/pjsip/pjproject/issues/1937


Video quality troubleshooting
=========================================
For video quality problems, the steps are as follows:

1. For lack of video, check account's AccountVideoConfig, especially the fields autoShowIncoming and autoTransmitOutgoing. More about the video API is explained in `Video Users Guide`_.
2. Check local video preview using PJSUA API as described in `Video Users Guide-Video Preview API`_.
3. Since video requires a larger bandwidth, we need to check for network impairments as described in `Checking Network Impairments`_. The document is for troubleshooting audio problem but it applies for video as well.
4. Check the CPU utilization. If the CPU utilization is too high, you can try a different (less CPU-intensive) video codec or reduce the resolution/fps. A general guide on how to reduce CPU utilization can be found here: `FAQ-CPU utilization`_.

.. _`Video Users Guide`: http://trac.pjsip.org/repos/wiki/Video_Users_Guide
.. _`Video Users Guide-Video Preview API`: http://trac.pjsip.org/repos/wiki/Video_Users_Guide#VideopreviewAPI
.. _`Checking Network Impairments`: http://trac.pjsip.org/repos/wiki/audio-check-packet-loss
.. _`FAQ-CPU utilization`: http://trac.pjsip.org/repos/wiki/FAQ#cpu


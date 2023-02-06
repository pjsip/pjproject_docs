High jitter value observed by remote party 
================================================

Checklists:

#. Check if this is a network condition rather than problem with transmission.
#. Since the transmission of the RTP packet is driven by the sound device clock
   (see :any:`/specific-guides/media/audio_flow` page for the complete explanation),
   the performance of the transmission is affected by the performance of the sound
   device. If the sound device doesn't deliver the captured frame in timely manner,
   the outgoing RTP transmission will have jitter in it. See
   :any:`/specific-guides/audio-troubleshooting/checks/dev_quality`
   for more information.

Note that normally a jitter in the transmission shouldn't cause problems, since 
the jitter is not very big and the receiving party should be able to accomodate this
with a de-jitter buffer.

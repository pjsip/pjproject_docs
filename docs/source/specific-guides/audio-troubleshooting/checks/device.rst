Check that correct device is used
==========================================
Some audio problems occur simply because the wrong device is being used by the application. 
One way to inspect which sound device is used is by setting the log level to 5 
(``--app-log-level=5`` argument with *pjsua*). Then when the the sound device is opened, 
for example when a call is established, it should display something like this:

::

 15:05:37.978      pasound.c Opened device Primary Sound Capture Driver(Windows 
 DirectSound)/Primary Sound Driver(Windows DirectSound) for recording and playback, 
 sample rate=16000, ch=1, bits=16, 160 samples per frame, input latency=0 ms,
 output latency=120 ms

Check that the correct device is being used from the log above.



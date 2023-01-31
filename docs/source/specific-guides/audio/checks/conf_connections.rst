Check audio interconnection in the conference bridge
=======================================================

Use pjsua's ``cl`` (conference list) command from the *pjsua*'s menu
to check if the connection is made between the call and the sound device
in the conference bridge. 

As an example, consider the following output:

::

   >>> cl
   Conference ports:
   Port #00[16KHz/10ms]         Master/sound  transmitting to: #1
   Port #01[16KHz/20ms]   sip:user@localhost  transmitting to: #0

then the call **does** have bidirectional media flow with the sound
device (the ``cl`` command output above shows that the audio device is
transmitting to the call (port 1) and the call is transmitting to the sound
device (port 0), thus bidirectional media flow between sound device and call is
established).

If you don't see the bidirectional media flow between sound device and
the call, you can *connect* them using pjsua's ``cc`` (conference
connect) command as shown in the command sequence below:

::

   >>> cl
   Conference ports:
   Port #00[16KHz/10ms]         Master/sound  transmitting to:
   Port #01[16KHz/20ms]   sip:user@localhost  transmitting to:

The above output shows **no** media flow between call and sound device. The
command below will establish **unidirectional** media flow from the
sound device to the call:

::

   >>> cc 0 1
   Success

And the command below will establish another unidirectional media flow
from the **reverse** direction, from the call to the sound device:

::

   >>> cc 1 0
   Success

Now if we check again the connection status in the conference bridge,
you should see this output:

::

   >>> cl
   Conference ports:
   Port #00[16KHz/10ms]         Master/sound  transmitting to: #1
   Port #01[16KHz/20ms]   sip:user@localhost  transmitting to: #0

   >>>

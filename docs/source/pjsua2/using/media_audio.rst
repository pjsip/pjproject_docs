
Working with audio media
==========================
Media objects are objects that are capable of producing or reading media.
PJSUA2 media objects are derived from :cpp:class:`pj::Media` class.

An important subclass of ``Media`` is :cpp:class:`pj::AudioMedia` which represents 
audio media. There are several types of audio media objects supported in PJSUA2:

- Capture device's AudioMedia, to capture audio from the sound device.
- Playback device's AudioMedia, to play audio to the sound device.
- Call's AudioMedia, to transmit and receive audio to/from remote person.
- :cpp:class:`pj::AudioMediaPlayer`, to play WAV file(s).
- :cpp:class:`pj::AudioMediaRecorder`, to record audio to a WAV file.


The conference bridge
----------------------------
The conference bridge provides a simple but yet powerful concept to manage audio flow 
between the audio medias. The principle is very simple; application connects audio source 
to audio destination, and the bridge makes the audio flows from that source to the specified
destination, and that's it. If more than one sources are transmitting to the same destination, 
then the audio from the sources will be mixed. If one source is transmitting to more than one 
destinations, the bridge will take care of duplicating the audio from the source to the 
multiple destinations. The bridge will even take care of mixing medias with different clock 
rates and ptime.

In PJSUA2, all audio media objects are registered to the central conference bridge for easier 
manipulation. At first, a registered audio media will not be connected to anything, so media 
will not flow from/to any objects. An audio media source can start/stop the transmission to 
a destination by using the API :cpp:func:`pj::AudioMedia::startTransmit()` and 
:cpp:func:`pj::AudioMedia::stopTransmit()`.

.. note::

    An audio media object registered to the conference bridge will be given a port ID number that 
    identifies the object in the bridge. Application can use the API :cpp:func:`pj::AudioMedia::getPortId()` 
    to retrieve the port ID. Normally, application should not need to worry about the conference 
    bridge and its port ID (as all will be taken care of by the ``Media`` class) unless application 
    wants to create its own custom audio media.

    As a convention in PJSUA-LIB API, port zero of the conference bridge is denoted for
    the sound device. Hence connecting a media to port zero will play that media to speaker,
    and connecting port zero to a media will capture audio from the microphone.


Playing a WAV file
----------------------------
To playback the WAV file to the sound device, create a WAV playback and call
:cpp:func:`pj::AudioMedia::startTransmit()` sound device's playback media:

.. code-block:: c++

    AudioMediaPlayer player;
    AudioMedia& speaker_media = Endpoint::instance().audDevManager().getPlaybackDevMedia();
    try {
        player.createPlayer("file.wav");
        player.startTransmit(speaker_media);
    } catch(Error& err) {
    }

See :cpp:class:`pj::AudioMediaPlayer` and :cpp:func:`pj::Endpoint::audDevManager()`
for reference.

By default, the WAV file will be played in a loop. To disable the loop, specify 
``PJMEDIA_FILE_NO_LOOP`` when creating the player:

.. code-block:: c++

        player.createPlayer("file.wav", PJMEDIA_FILE_NO_LOOP);

Without looping, silence will be played once the playback has reached the end of the WAV file.

If application wants to be notified on playback EOF event, it can subclass 
``AudioMediaPlayer`` and implement :cpp:func:`pj::AudioMediaPlayer::onEof2()` callback.

Once application is done with the playback, just call :cpp:func:`pj::AudioMedia::stopTransmit()` 
to stop the playback:

.. code-block:: c++

    try {
        player.stopTransmit(speaker_media);
    } catch(Error& err) {
    }

Resuming the transmission (by calling ``startTransmit()``) after the playback is stopped will 
resume playback from the last play position. Use :cpp:func:`pj::AudioMediaPlayer::setPos()` to 
set playback position to a desired location.


Recording to WAV file
----------------------------
The example below starts recording audio from the microphone to a WAV file, by using
:cpp:class:`pj::AudioMediaRecorder` class:

.. code-block:: c++

    AudioMediaRecorder wav_writer;
    AudioMedia& mic_media = Endpoint::instance().audDevManager().getCaptureDevMedia();
    try {
        wav_writer.createRecorder("file.wav");
        mic_media.startTransmit(wav_writer);
    } catch(Error& err) {
    }

See :cpp:class:`pj::AudioMediaRecorder` and :cpp:func:`pj::Endpoint::audDevManager()`
for reference.

Media will flow from the sound device to the WAV recorder as soon as ``startTransmit()``
is called. As usual, to stop or pause recording, just call :cpp:func:`pj::AudioMedia::stopTransmit()`:

.. code-block:: c++

    try {
       mic_media.stopTransmit(wav_writer);
    } catch(Error& err) {
    }

Note that stopping the transmission to the WAV recorder as above does not close the WAV file, 
and you can resume recording by connecting a source (any source, doesn't have to be the same source) 
to the WAV recorder again. You cannot playback the recorded WAV file until you close it. To close 
the WAV recorder, simply delete it:

.. code-block:: c++

    delete wav_writer;


Local audio loopback
----------------------------
A useful test to check whether the local sound device (capture and playback device) is working 
properly is by transmitting the audio from the capture device directly to the playback device 
(i.e. local loopback). Application can do this by:

.. code-block:: c++

    mic_media.startTransmit(speaker_media);


Looping audio
----------------------------
Application can loop the audio of an audio media object to itself (i.e. the audio received from 
the object will be transmitted to itself). You can loop-back audio from any objects, as long as 
the object has bidirectional media. That means you can loop the call's audio media, so that audio 
received from the remote person will be transmitted back to her/him. But you can't loop the WAV 
player or recorder since these objects can only play or record and not both.


Call's media
----------------------------

A single call can have more than one media (for example, audio and video). Application can retrieve 
the audio media by utilizing :cpp:func:`pj::Call::getInfo()` and :cpp:func:`pj::Call::getMedia()`. 
Usually for a normal call, bidirectional audio is established with the remote person, which can be 
done by connecting the sound device to the call's audio media:

.. code-block:: c++

    CallInfo ci = call.getInfo();
    AudioMedia *aud_med = NULL;

    for (unsigned i=0; i<ci.media.size(); ++i) {
        if (ci.media[i].type == PJMEDIA_TYPE_AUDIO) {
            aud_med = (AudioMedia *)call.getMedia(i);
            break;
        }
    }

    if (aud_med) {
        mic_media.startTransmit(*aud_med);
        aud_med->startTransmit(speaker_media);
    }



Second call
----------------------------
PJSUA2 supports more than one simultaneous calls. Suppose we want to talk with two remote parties 
at the same time. Since we already have bidirectional media connection with one party, we just need to 
add bidirectional connection with the other party by repeating the same procedure for the second
call:

.. code-block:: c++

    CallInfo ci2 = call2.getInfo();
    AudioMedia *aud_med2 = NULL;

    for (unsigned i=0; i<ci2.media.size(); ++i) {
        if (ci2.media[i].type == PJMEDIA_TYPE_AUDIO) {
            aud_med2 = (AudioMedia *)call2.getMedia(i);
            break;
        }
    }

    if (aud_med2) {
        mic_media->startTransmit(*aud_med2);
        aud_med2->startTransmit(speaker_media);
    }

Now we can talk to both parties at the same time, and we will hear audio from either party. 
But at this stage, the remote parties can't talk or hear each other (i.e. we're not in full conference 
mode yet).


Conference call
----------------------------
To enable both parties talk to each other, just establish bidirectional media between them:

.. code-block:: c++

    aud_med->startTransmit(*aud_med2);
    aud_med2->startTransmit(*aud_med);

Now the three parties (us and both remote parties) will be able to talk to each other.

Recording the Conference
----------------------------

While doing the conference, application can record the conference to a WAV file, 
by connecting the microphone and both calls to the WAV recorder:

.. code-block:: c++

    mic_media.startTransmit(wav_writer);
    aud_med->startTransmit(wav_writer);
    aud_med2->startTransmit(wav_writer);



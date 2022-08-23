
Working with video media
==========================
Video media is similar to audio media in many ways. The class :cpp:class:`pj::VideoMedia` is
also derived from :cpp:class:`pj::Media` class. Its object types also consist of capture &
playback devices, and call stream. The video conference bridge shares the same
principles as the audio conference bridge; application connects video source to video
destination to allow video flow from that source to the specified destination, which
in turn may also induce video mixing and duplicating operations.

There are several types of video media objects supported in PJSUA2:

- Capture device's VideoMedia, to capture video frames from the camera.
- Render device's VideoMedia, to render video frames on the screen.
- Call's VideoMedia, to transmit and receive video to/from the remote party.


The video conference bridge
----------------------------
As mentioned before, the video conference is actually similar to the audio conference
bridge. Application connects video source to video destination, and the bridge makes the video
flows from that source to the specified destination. If more than one sources are transmitting
to the same destination, then the video frames from the sources will be combined into one
video frame in specific tile configuration. If one source is transmitting to more than one 
destinations, the bridge will take care of duplicating the video frame from the source to the 
multiple destinations. The bridge will even take care of mixing video with different frame
rates.

In PJSUA2, all video media objects, of class :cpp:class:`pj::VideoMedia`, are registered to
the central conference bridge for easier manipulation. At first, a registered video media will
not be connected to anything, so media will not flow from/to any objects. A video media source
can start/stop the transmission to a destination by using the API
:cpp:func:`pj::VideoMedia::startTransmit()` and :cpp:func:`pj::VideoMedia::stopTransmit()`.

.. note::

    A video media object registered to the conference bridge will be given a port ID number that
    identifies the object in the bridge. Application can use the API :cpp:func:`pj::VideoMedia::getPortId()` 
    to retrieve the port ID. Normally, application should not need to worry about the conference 
    bridge and its port ID (as all will be taken care of by the ``Media`` class) unless application 
    wants to create its own custom video media.

    In the video conference bridge, the port zero is not special like in audio, which is designated
    for the main audio device. In video, port zero can be assigned to any type of video object.


Starting camera preview
----------------------------
Application can start the camera (or any capture device in general) preview using video object
:cpp:class:`pj::VideoPreview`.

.. note::
    Application does not need to start a camera preview manually to setup a video call.
    The camera preview will be started automatically once the video call is established,
    it is just that by default the video preview window is hidden. The capture device
    to be used in a video call is configurable in account setting.

.. code-block:: c++

    void StartPreview(int device_id, void* hwnd, int width, int height, int fps)
    {
        try {
            // Set the video capture device format.
	    VidDevManager &mgr = Endpoint::instance().vidDevManager();
            MediaFormatVideo format = mgr.getFormat(device_id);
	    format.width    = width;
	    format.height   = height;
	    format.fpsNum   = fps;
	    format.fpsDenum = 1;
            mgr.setFormat(device_id, format, true);
        
	    // Start the preview on a panel with window handle 'hwnd'.
	    // Note that if hwnd is set to NULL, library will automatically create
	    // a new floating window for the rendering.
	    VideoPreviewOpParam param;
	    param.window.handle.window = (void*) hwnd;
	    
	    VideoPreview preview(device_id);
	    preview.start(param);
        } catch(Error& err) {
        }
    }

See :cpp:class:`pj::VideoPreview`, :cpp:class:`VideoPreviewOpParam`, :cpp:class:`MediaFormatVideo`,
and :cpp:func:`pj::Endpoint::vidDevManager()` for reference.


Important note about threading
----------------------------
On some GUI frameworks, for example SDL on Windows, calling :cpp:func:`pj::VideoPreview::start()`
from the GUI thread, such as from window event callback, may cause GUI to gets stuck (e.g:
unresponsive GUI window). This can be avoided by calling :cpp:func:`pj::VideoPreview::start()`
from non-GUI thread, for example via PJSUA2 timer so it will be invoked from the library worker thread.

Note that some other operations that indirectly involve video rendering may need to be done in
non-GUI thread too, for example we found :cpp:func:`pj::Endpoint::libDestroy()` in C# desktop
will cause stuck when initiated from GUI thread.

Generally it is a good practice to keep the GUI thread free from non-UI work to improve application
responsiveness. So it is also recommended to avoid calling PJSIP API from GUI thread since:
- it may take some time to complete, or
- it may block while trying to acquire a lock.
    
Here is a sample code to post a job via schedule timer, in this sample, it is for scheduling
a video capture device preview start.

.. code-block:: c++
    // Timer type ID
    enum {
        TIMER_START_PREVIEW = 1,
	...
    };
    
    // Generic timer parameter
    struct MyTimerParam {
	int type;
	union {
	    struct {
	        int   dev_id;
		void *hwnd;
		int   w, h, fps;
	    } start_preview;
	    ...
	} data;
    };
    
    
    // PJSUA2 Endpoint::onTimer() implementation
    void Endpoint::onTimer(const OnTimerParam &prm)
    {
        MyTimerParam *param = (MyTimerParam*) prm.userData;
	if (param->type == TIMER_START_PREVIEW) {
	    int dev_id = param->data.start_preview.dev_id;
            void *hwnd = param->data.start_preview.hwnd;
	    int w      = param->data.start_preview.w;
	    int h      = param->data.start_preview.h;
	    int fps    = param->data.start_preview.fps;
	    StartPreview(device_id, hwnd, w, h, fps);
	}
	...
	
	// Finally delete the timer parameter.
	delete param;
    }
    
    ...
    
    MyTimerParam *tp = new MyTimerParam();
    tp->type = TIMER_START_PREVIEW;
    tp->data.start_preview.dev_id = 1; // colorbar virtual device
    tp->data.start_preview.hwnd   = (void*)some_hwnd;
    tp->data.start_preview.w      = 320;
    tp->data.start_preview.h      = 240;
    tp->data.start_preview.fps    = 15;
    
    // Schedule the preview start to be executed immediately (zero milisecond delay).
    Endpoint::instance().utilTimerSchedule(0, tp);


Call's video media
----------------------------
Unlike in audio, call video media is separated between encoding and decoding, this is because
the video formats (e.g: width, height, frame rate) of both directions can be different.
Application can retrieve the video media objects using 
:cpp:func:`pj::Call::getEncodingVideoMedia()` for the encoding direction and
:cpp:func:`pj::Call::getDecodingVideoMedia()` for the decoding direction, both will return
instance of class :cpp:class:`pj::VideoMedia`.
    
Also unlike in audio call where port connections between audio device and call audio media needs
to be set up manually by application, in video, the port connections in the conference bridge
are set up automatically by the library, so the video capture device (configured via account settings)
will be connected to the encoding video media and the decoding video media will be connected
to a renderer video window.

.. note::

    In a video call scenario, actually the video capture device is transmitting to
    two destinations, one is to the preview window, by default the window is hidden
    if preview is started automatically by the library, and the other is to the encoding
    call media. And if there are two or more concurrent video calls sharing the same
    capture device, the device will be transmitting to three or more destinations.
    Thanks to the video conference bridge for its duplicating feature.


Configuring a video window
----------------------------
Video window is represented by class :cpp:class:`VideoWindow`, it manages video presentation
window. Application can query the native window handle, show/hide, resize, reposition, or
rotate the video window.

On some platforms, e.g: iOS, the video preview comes with a native video window,
so the video window for that preview is not created by the library. In this case,
application can query the native window handle using :cpp:func:`pj::VideoWindow::getInfo()`
and should use platform's native window API to manage (show/hide, resize,
reposition, rotate) the video window.

For example here is the code to show the video window for a video preview:

.. code-block:: c++
    
    try {
        VideoPreview preview(device_id);
        VideoWindow window = preview.getVideoWindow();
        VideoWindowInfo window_info = window.getInfo();
        if (!window_info.isNative()) {
	    window.Show(true);  // show the window
	}
    } catch(Error& err) {
    }

If you are using PJSUA2 via SWIG, currently available for Python, C#, and Java,
application cannot query the native window handle info of a video window. This is because
a native window handle created by the library is usually not very useful (or not easy to
manage) for the app written in high level languages. So application should create
a GUI window/panel whose native window handle can be queried, e.g: ``ANativeWindow``
in Android, and assign the native window handle to the library to be used by
the video render engine via :cpp:func:`pj::WindowHandle::setWindow()`.

Here is a C# sample code to assign/change the video window of a video preview.

.. code-block:: c#

    // Create a panel
    Panel panel = new Panel();
    panel.Size = new Size(350, 250);
    panel.Location = new Point(20, 20);
    Controls.Add(panel);
    
    try {
        // Assuming a preview for colorbar has been started,
	// we just instantiate a VideoPreview to refer to it.
        const int DEV_ID_COLORBAR = 1;
        VideoPreview vp = new VideoPreview(DEV_ID_COLORBAR);
    
        // Set the window of the preview to the just created panel
	VideoWindow window = vp.getVideoWindow();
        window.setWindow(panel.Handle.ToInt64());
    } catch(Error& err) {
    }

    
Video event
----------------------------
Application can listen to video events delivered via media event callbacks:
- :cpp:func:`pj::Call::onCallMediaEvent()` for media events in a video call session, or
- :cpp:func:`pj::Endpoint::onMediaEvent()` for global media events.

One of the most important video event types is video format changed
(``PJMEDIA_EVENT_FMT_CHANGED``). In a video call, usually we cannot know the video format
(especially size and frame rate) sent by remote until we receive some video RTP packets
and decode them successfully. Once the video format is known, the library will notify
application via format change event, so application can start showing the video window
and/or adjust the window size accordingly. This event may also be invoked anytime whenever
the video format is changed.

.. code-block:: c++
    
    void MyCall::onCallMediaEvent(OnCallMediaEventParam &prm)
    {
        if (prm.ev.type == PJMEDIA_EVENT_FMT_CHANGED) {
            try {
		MediaSize new_size;
		new_size.x = prm.ev.data.fmtChanged.newWidth;
		new_size.y = prm.ev.data.fmtChanged.newHeight;
		
		// Scale down the size if necessary
		if (new_size.x > 500 || new_size.y > 500) {
		    new_size.x /= 2;
		    new_size.y /= 2;
		}

	        // Show and adjust the size of the video window
	        CallInfo info = getInfo();
	        VideoWindow window = info.media[prm.medIdx].videoWindow;
		window.show(true);
                window.setSize(new_size);
            } catch(Error& err) {
            }
        }
    }


Video conference call
----------------------------
Just like in the audio, to enable three or more parties video conference,
we need to establish bidirectional video media between them:

.. code-block:: c++

    VideoMedia vid_enc_med1 = call1.getEncodingVideoMedia(-1);
    VideoMedia vid_dec_med1 = call1.getDecodingVideoMedia(-1);
    
    VideoMedia vid_enc_med2 = call2.getEncodingVideoMedia(-1);
    VideoMedia vid_dec_med2 = call2.getDecodingVideoMedia(-1);
    
    vid_dec_med1.startTransmit(vid_enc_med2);
    vid_dec_med2.startTransmit(vid_enc_med1);

Now the three parties (us and both remote parties) will be able to see each other.

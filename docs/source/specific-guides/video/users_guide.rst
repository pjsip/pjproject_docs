Video User's Guide
========================

.. contents:: Table of Contents
   :depth: 4

Video is available on PJSIP version 2.0 and later (2.3 support video for
iOS, 2.4 support video for Android). This document describes how to use
the video feature with PJSIP.

Building with Video Support
---------------------------

Follow :any:`get_started_toc` for your platform
on building pjsip with video support.

Building the GUI Sample Application
----------------------------------------------

We have a GUI sample application with video support. The project is
located under :sourcedir:`pjsip-apps/src/vidgui`. It is not built by default, and
you need `Qt SDK <http://qt.nokia.com/downloads/>`__ to build it.

GNU Build System (Mac OS X, Linux, etc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to build vidgui sample: 

#. Go to vidgui source directory: 

   .. code-block:: shell

    $ cd pjsip-apps/src/vidgui

#. Generate Makefile. For Linux: 

   .. code-block:: shell

      $ qmake
      
   and for Mac OS X:
   
   .. code-block:: shell
       
      $ qmake -spec macx-g++

#. Build the app:

   .. code-block::
      
      $ make


Visual Studio
~~~~~~~~~~~~~

Follow these steps to build vidgui sample with Visual Studio:

#. Open command prompt, and 

   .. code-block:: shell
      
      cd pjsip-apps\src\vidgui

#. Generate project files:

   .. code-block:: shell
      
      qmake -tp vc

#. Open *vidgui.vcproj* project.
#. Save the solution, and build the project


Using Video API (pjsua-lib)
---------------------------

This section provides several sample scenarios of using video in your
application. Please see :any:`vid_ug_api_ref` section below for a more
complete documentation about the Video API.

Enabling Video
~~~~~~~~~~~~~~

By default, video is enabled in :cpp:any:`pjsua_call_setting::vid_cnt` setting.

Incoming Video Call
~~~~~~~~~~~~~~~~~~~

Incoming video will be accepted/rejected depending on whether video is
enabled in the call setting (see above). You can pass the call setting
using the API :cpp:any:`pjsua_call_answer2()` (so for example, to reject the
video, set ``vid_cnt`` to 0 and call :cpp:any:`pjsua_call_answer2()`). If
video is enabled, incoming video will be accepted as long as we have
matching codec for it. However, this does not necessarily mean that the
video will be displayed automatically to the screen, nor that outgoing
video will be transmitted automatically, as there will be separate
settings for these. Outgoing video behavior will be explained in the
next section.

Display Incoming Video Automatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, incoming video **is not** displayed automatically, since the
app may want to seek user approval first. Use the following code to
change this behavior on per account basis:

.. code-block:: c

   pjsua_acc_config cfg;

   pjsua_acc_config_default(&cfg); 
   cfg.vid_in_auto_show = PJ_TRUE;



Show or Hide Incoming Video
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regardless of the setting above, you can use the following steps to show or hide the display incoming video:

1. Use :cpp:any:`pjsua_call_get_vid_stream_idx()` or enumerate the call's media stream to find the media index of the default video. If there are multiple video streams in a call, the default video is the first active video media in the call.
2. Locate the media information of the specified stream index in the :cpp:any:`pjsua_call_info`, and acquire the window ID associated with the remote video. Sample code:

.. code-block:: c

   int vid_idx; pjsua_vid_win_id wid;

   vid_idx = pjsua_call_get_vid_stream_idx(call_id); 
   if (vid_idx >= 0) {
      pjsua_call_info ci;

      pjsua_call_get_info(call_id, &ci);
      wid = ci.media[vid_idx].stream.vid.win_in;

   }

3. Using the video window ID, you may retrieve the associated
   native video handle with :cpp:any:`pjsua_vid_win_get_info()` and then show or
   hide the video window using native API, or use
   :cpp:any:`pjsua_vid_win_set_show()` to show/hide the window using PJSUA API.
   See :any:`vid_ug_wvw` section below for information on
   manipulating video windows.


.. _vid_ug_civs:

Controlling Incoming Video Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Controlling the video window above will not cause any re-INVITE or
UPDATE to be sent to remote, since the operation occurs locally.
However, if you wish, you may alter the incoming video stream with
:cpp:any:`pjsua_call_set_vid_strm()` API, and this **will** cause re-INVITE or
UPDATE to be sent to negotiate the new SDP. The relevant operation to
control incoming video with :cpp:any:`pjsua_call_set_vid_strm()` are: 

- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_DIR`: change the media direction (e.g. to
  "sendonly", or even "inactive") 
- :cpp:any:`PJSUA_CALL_VID_STRM_REMOVE`: remove
   the media stream altogether by settings its port to zero 
- :cpp:any:`PJSUA_CALL_VID_STRM_ADD`: add new video media stream

Since :cpp:any:`pjsua_call_set_vid_strm()` will result in renegotiation of the
SDP in a re-INVITE or UPDATE transaction, the result of this operation
will not be available immediately. Application can monitor the status by
implementing :cpp:any:`pjsua_callback::on_call_media_state()` callback and enumerate the media
stream status with pjsua_call_info.

Incoming Re-offer
^^^^^^^^^^^^^^^^^

If the re-offer contains video, incoming re-offer will be automatically
answered with current video setting in the call setting. Currently there
is no callback for this, however application can always watch for media
update via :cpp:any:`pjsua_callback::on_call_media_state()` callback.

Outgoing Video Call
~~~~~~~~~~~~~~~~~~~

Outgoing video is enabled/disabled depending on the call setting. To
initiate a call with video in the SDP as inactive, you can disable the
video in the call setting and set :cpp:any:`pjsua_call_setting::flag` with
:cpp:any:`PJSUA_CALL_INCLUDE_DISABLED_MEDIA`.

Outgoing Video Transmission
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Outgoing video transmission is independent from the incoming video
transmission; each can be operated separately. Note that outgoing video
transmission **is not started by default**, not even when incoming offer
contains video support. This behavior is controlled by
:cpp:any:`pjsua_acc_config::vid_out_auto_transmit` setting, which default to
*PJ_FALSE*. Setting this to *PJ_TRUE* will cause video transmission to
be started automatically on each outgoing calls and on incoming calls
that indicates video support in its offer. However, it is more flexible
and appropriate to leave this setting at PJ_FALSE, and add video later
during the call by using :cpp:any:`pjsua_call_set_vid_strm()` API, as will be
explained shortly.

Default Capture Device
^^^^^^^^^^^^^^^^^^^^^^

The default capture device that is used by an account is configured in
:cpp:any:`pjsua_acc_config::vid_cap_dev` setting. It is more convenient to set
the "correct" device here rather than having to set it in every other
API calls later.

.. _vid_ug_cvs:

Controlling Video Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Application uses :cpp:any:`pjsua_call_set_vid_strm()` API to control video
stream on a call.

- :cpp:any:`PJSUA_CALL_VID_STRM_ADD`: add a new video
  stream 
- :cpp:any:`PJSUA_CALL_VID_STRM_REMOVE`: remove video stream (set port to
  zero) 
- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_DIR`: change direction or deactivate
  (i.e. set direction to "inactive") 
- :cpp:any:`PJSUA_CALL_VID_STRM_CHANGE_CAP_DEV`: change capture device 
- :cpp:any:`PJSUA_CALL_VID_STRM_START_TRANSMIT`: start previously stopped
  transmission 
- :cpp:any:`PJSUA_CALL_VID_STRM_STOP_TRANSMIT`: stop transmission

See :cpp:any:`pjsua_call_vid_strm_op` for more information.

Some of the video operations above require re-INVITE or UPDATE to be
sent, hence the result will not be available immediately. In that case,
application can implement :cpp:any:`pjsua_callback::on_call_media_state()` callback and inspect
the resulting negotiation by looking at the :cpp:any:`pjsua_call_info`. Please
see :any:`vid_ug_vcm` in the API reference section below
for more information about the operations above.

Add or Remove Video
~~~~~~~~~~~~~~~~~~~

You can set :cpp:any:`pjsua_call_setting::vid_cnt` to
the desired video count to add/remove video, then send the
reinvite/update. Alternatively, you can use
:cpp:any:`pjsua_call_set_vid_strm()` API to control the video stream on a call
:any:`vid_ug_civs` or :any:`vid_ug_cvs` above.


.. _vid_ug_wvw:

Working with Video Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video Window represents all window objects on the screen that the
library creates. The video window can display incoming video, preview,
and/or other video playbacks.

Application may retrieve video windows from the following places: 

- for calls, the video window of incoming video stream is contained in the
  media stream inside :cpp:any:`pjsua_call_info::media` structure. 
- preview window associated with a capture device can be queried with
  :cpp:any:`pjsua_vid_preview_get_win()`. 
- for all other purposes, application
  may enumerate all video windows with :cpp:any:`pjsua_vid_enum_wins()`.

Application retrieves :cpp:any:`pjsua_vid_win_info` with
:cpp:any:`pjsua_vid_win_get_info()`. The one window property that most
applications will be interested with is the native window handle of the
video. The native video handle is contained by :cpp:any:`pjmedia_vid_dev_hwnd`
structure inside :cpp:any:`pjsua_vid_win_info`. Application can use the native
handle to embed the video window into application's GUI structure.
Alternatively, the library also provides few simple and most commonly
used API to operate the window, such as :cpp:any:`pjsua_vid_win_set_show()`,
:cpp:any:`pjsua_vid_win_set_size()`, etc., however the availability of these
APIs are not guaranteed since it depends on the underlying backend
device.

Modifying video codec parameters for video call
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video codec parameters are specified in :cpp:any:`pjmedia_vid_codec_param`. The
codec parameters provide separate settings for each direction, encoding
and decoding. Any modifications on video codec parameters can be applied
using :cpp:any:`pjsua_vid_codec_set_param()`, here is a sample code for
reference: 

.. code-block:: c

   const pj_str_t codec_id = {"H264", 4};
   pjmedia_vid_codec_param param;

   pjsua_vid_codec_get_param(&codec_id, &param);

   /* Modify param here */
   ...

   pjsua_vid_codec_set_param(&codec_id, &param);


Size or resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify video picture dimension.

a. For encoding direction, configured via ``det.vid.size`` field of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

   .. code-block:: c

      /* Sending 1280 x 720 */
      param.enc_fmt.det.vid.size.w = 1280;
      param.enc_fmt.det.vid.size.h = 720;

   .. note::

       - Both width and height must be even numbers. 
       - There is a possibility that the value will be adjusted to follow remote capability. For example, if remote signals  that maximum resolution supported is 640 x 480 and locally the encoding direction size is set to 1280 x 720, then 640 x 480 will be used.
       -  The library will find the closest size/ratio that the capture device supports. Application should choose the size ratio that the capture device supports, otherwise the video might get stretched. For example, if the device capture supports 640x480 and 1280x720 and the size is set to 500x500. The device camera will be opened at 640x480 and later converted to 500x500 and get the image stretched. 

b. For decoding direction, two steps are needed:

   1. The ``det.vid.size`` field of :cpp:any:`pjmedia_vid_codec_param::dec_fmt` should be set to the highest value expected for incoming video size.
   2. signalling to remote, configured via codec specific SDP format parameter (fmtp): :cpp:any:`pjmedia_vid_codec_param::dec_fmtp`.

       - H263-1998, e.g:

         .. code-block:: c

            /* 1st preference: 352 x 288 (CIF) */
            param.dec_fmtp.param[n].name = pj_str("CIF");
            /* The value actually specifies framerate, see framerate section below */
            param.dec_fmtp.param[n].val = pj_str("1");
            /* 2nd preference: 176 x 144 (QCIF) */
            param.dec_fmtp.param[n+1].name = pj_str("QCIF");
            /* The value actually specifies framerate, see framerate section below */
            param.dec_fmtp.param[n+1].val = pj_str("1");

       - H264, the size is implicitly specified in H264 level (check the standard specification or `this Wikipedia page <http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels>`__) and on SDP, the H264 level is signalled via H264 SDP fmtp `profile-level-id <http://tools.ietf.org/html/rfc6184#section-8.1>`__, e.g:

         .. code-block:: c

            /* Can receive up to 1280×720 @30fps */
            param.dec_fmtp.param[n].name = pj_str("profile-level-id");
            /* Set the profile level to "1f", which means level 3.1 */
            param.dec_fmtp.param[n].val = pj_str("xxxx1f");

Framerate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify number of frames processed per second.

a. For encoding direction, configured via ``det.vid.fps`` of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

   .. code-block:: c

      /* Sending @30fps */
      param.enc_fmt.det.vid.fps.num   = 30;
      param.enc_fmt.det.vid.fps.denum = 1;

   .. note::

        - that there is a possibility that the value will be adjusted to follow remote capability. For example, if remote signals that maximum framerate supported is 10fps and locally the encoding direction framerate is set to 30fps, then 10fps will be used.
        - **limitation:** if preview is enabled before call is established, capture device will opened using default framerate of the device, and subsequent calls that use that device will use this framerate regardless of the configured encoding framerate that is set above. Currently the only solution is to disable preview before establishing media and re-enable it once the video media is established.

b. For decoding direction, two steps are needed:

   1. The ``det.vid.fps`` of :cpp:any:`pjmedia_vid_codec_param::dec_fmt` should be set to the highest value expected for incoming video framerate.
   2. signalling to remote, configured via codec specific SDP format parameter (fmtp): :cpp:any:`pjmedia_vid_codec_param::dec_fmtp`.

      - H263-1998, maximum framerate is specified per size/resolution basis, check `RFC 4629 Section 8.1.1 <http://tools.ietf.org/html/rfc4629#section-8.1.1>`__ for more info.

         .. code-block:: c

            /* 3000/(1.001*2) fps for CIF */
            param.dec_fmtp.param[m].name = pj_str("CIF");
            param.dec_fmtp.param[m].val = pj_str("2");
            /* 3000/(1.001*1) fps for QCIF */
            param.dec_fmtp.param[n].name = pj_str("QCIF");
            param.dec_fmtp.param[n].val = pj_str("1");

      - H264, similar to size/resolution, the framerate is implicitly specified in H264 level (check the standard specification or `MPEG-4 AVC levels <http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels>`__) and the H264 level is signalled via H264 SDP fmtp ``profile-level-id``, e.g:

         .. code-block:: c

            /* Can receive up to 1280×720 @30fps */
            param.dec_fmtp.param[n].name = pj_str("profile-level-id");
            param.dec_fmtp.param[n].val = pj_str("xxxx1f");

Bitrate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify bandwidth requirement for video payloads stream delivery.

This is configurable via ``det.vid.avg_bps`` and ``det.vid.max_bps`` fields of :cpp:any:`pjmedia_vid_codec_param::enc_fmt`, e.g:

.. code-block:: c

   /* Bitrate range preferred: 512-1024kbps */
   param.enc_fmt.det.vid.avg_bps = 512000;
   param.enc_fmt.det.vid.max_bps = 1024000;

.. note::

   - This setting is applicable for encoding and decoding direction,
     currently there is no way to set asymmetric bitrate. By decoding
     direction, actually it just means that this setting will be queried when
     generating bandwidth info for local SDP (see next point). 
   - The bitrate
     setting of all codecs will be enumerated and the highest value will be
     signalled in bandwidth info in local SDP (see ticket :issue:`1244`). 
   - There is
     a possibility that the encoding bitrate will be adjusted to follow
     remote bitrate setting, i.e: read from SDP bandwidth info (b=TIAS line)
     in remote SDP. For example, if remote signals that maximum bitrate is
     128kbps and locally the bitrate is set to 512kbps, then 128kbps will be
     used. 
   - If codec specific bitrate setting signalling (via SDP fmtp) is
     desired, e.g: *MaxBR* for H263, application should put the SDP fmtp
     manually, for example: 
  
     .. code-block:: c
  
        /* H263 specific maximum bitrate 512kbps */
        param.dec_fmtp.param[n].name = pj_str("MaxBR");
        param.dec_fmtp.param[n].val = pj_str("5120"); /* = max_bps / 100 \*/

Setting video capture orientation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On mobile platforms, in order to send video in the proper orientation
(i.e. head always up regardless of the device orientation), application
needs to do the following:

1. Setup the device to get orientation change notification.
2. Inside the callback, call PJSUA API :cpp:any:`pjsua_vid_dev_set_setting()`, e.g.:

   .. code-block:: c

      pjsua_vid_dev_set_setting(dev_id, PJMEDIA_VID_DEV_CAP_ORIENTATION,
                                &new_orientation, PJ_TRUE)
   
   or PJSUA2 API :cpp:any:`pj::VidDevManager::setCaptureOrient()`, e.g.:

   .. code-block:: c++

      Endpoint.instance().vidDevManager()
                         .setCaptureOrient(dev_id, new_orient, true)
   
   to tell the video device about the new
   orientation.

For sample usage, please refer to our sample apps, ipjsua for iOS, and
pjsua2 for Android. Ticket :issue:`1861` explains this feature in detail.

When video orientation signaling is available
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case application has the capability to signal remote about video
orientation (e.g: via SIP INFO or RTP header extension), instead of
telling video device capturer (via :cpp:any:`pjsua_vid_dev_set_setting()` or
:cpp:any:`pj::VidDevManager::setCaptureOrient()`), it may signal remote directly about the new
orientation. This way the video sent to remote will always in full frame
(no black bands in left+right sides due to forcing landscape video in
portrait frame or vice versa), but it may not be in "proper"
orientation, this should not be problem though as remote could get the
orientation info from out of band signaling, so it should be able to
render the incoming video frames in "proper" orientation.

However note that if **portrait** mode is prefered as the initial
orientation in a video call session (default settings are set for
landscape video orientation), the encoding part of video codec param
should be configured as portrait too, i.e: width < height, e.g: 

.. code-block:: c

   /* Sending 240 x 320 */ 
   param.enc_fmt.det.vid.size.w = 240;
   param.enc_fmt.det.vid.size.h = 320;


and the initial video device orientation should be set as portrait too, e.g:

.. code-block:: c

   /* After the capturer device is opened, e.g: using pjsua_vid_preview_start() 
    * or opened automatically by video call, tell the capture device about 
    * current orientation. Note this need to be done once only, so when orientation 
    * is changed, never update the device about the new orientation. 
    */

   /* On Android, portrait mode is defined as PJMEDIA_ORIENT_ROTATE_270DEG */ 
   current_orient = PJMEDIA_ORIENT_ROTATE_270DEG;

   /* On iOS, portrait mode is defined as PJMEDIA_ORIENT_ROTATE_90DEG*/
   current_orient = PJMEDIA_ORIENT_ROTATE_90DEG;

   pjsua_vid_dev_set_setting(dev_id, PJMEDIA_VID_DEV_CAP_ORIENTATION,
                             &current_orient, PJ_TRUE);

   ...



then when device orientation is changed, application **must not** update the video device orientation, instead, it should just signal remote about device orientation. Updating orientation info to video capture device will cause device to rotate (and perhaps downsize the image) to make sure that the image always has "proper" orientation (head upside).



.. _guide_vidconf:


Video Conference
-------------------

Available since 2.9.

Please check ticket :issue:`2181` for more info.



Additional Info
-------------------

Using OpenGL with SDL
~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP supports OpenGL video rendering with SDL. Follow these steps to enable and use the OpenGL backend.

1. Install OpenGL development libraries for your system. The instructions vary, and some platforms may have OpenGL development libraries installed by default.

   - For Ubuntu 12.04, you can run the following:
   
     .. code-block:: shell

        $ sudo apt-get install freeglut3 freeglut3-dev
        $ sudo apt-get install binutils-gold

   - Alternatively, you can use libgl-dev which is smaller. Please note that since Ubuntu 14.04 LTS, libsdl2-dev is available which comes with libgl-dev automatically, so it might not be needed anymore.
      
      .. code-block:: shell

         $ sudo apt-get install libgl-dev

2. Enable SDL OpenGL support in PJSIP, by declaring this in your :any:`config_site.h`:
   
   .. code-block:: c

      #define PJMEDIA_VIDEO_DEV_SDL_HAS_OPENGL    1

3. If you're not using Visual Studio, add OpenGL library in your application's input library list. If you're using GNU tools, you can add this in **user.mak** file in root PJSIP directory:


   .. code-block::

      export LDFLAGS += -lGL

4. Rebuild PJSIP
5. Now **"SDL openGL renderer"** device should show up in video device list. Simply just use this device.


Mac OS X Video Threading Issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On Mac OS X, our video implementation uses Cocoa frameworks, which require handling user events and drawing window content to be done in the main thread. Hence, to avoid deadlock, application should not call any PJSIP API which can potentially block from the main thread. We provide an API :cpp:any:`pj_run_app()` to simplify creating a GUI app on Mac OS X, please refer to *pjsua* app located in :sourcedir:`pjsip-apps/src/pjsua` for sample usage. Basically, :cpp:any:`pj_run_app()` will setup an event loop management in the main thread and create a multi-threading environment, allowing PJSIP to be called from another thread.

.. code-block:: c

   int main_func(int argc, char *argv[])
   {
       // This is your real main function
   }

   int main(int argc, char *argv[])
   {
       // pj_run_app() will call your main function from another thread (if necessary)
       // this will free the main thread to handle GUI events and drawing
       return pj_run_app(&main_func, argc, argv, 0);
   }


.. _vid_key:

Video key frame transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Sending/receiving missing video keyframe indication using the following techniques:

  * SIP INFO with XML Schema for Media Control (:rfc:`5168#section-7.1`), using:

     - Full Intra Request (:rfc:`5104#section-3.5.1`)
     - Picture Loss Indication feedback (:rfc:`4585#section-6.3.1`)
     - See issue :issue:`1234` for more info

  * RTCP Picture Loss Indication feedback (:rfc:`4585#section-6.3.1`):

     - See issue :issue:`1437` for more info

- Key frame at the start of the call (see issue :issue:`1910`)
- See also RTCP key frame request


.. _vid_ug_api_ref:

Video API Reference (pjsua-lib)
------------------------------------------

This section explains and lists the Video API as it was available when
this document is written. For a richer and more up to date list, please
see :doc:`Video API reference </api/generated/pjsip/group/group__PJSUA__LIB__VIDEO>`

The Video API is classified into the following categories.

Device enumeration API
~~~~~~~~~~~~~~~~~~~~~~

- :cpp:any:`pjsua_vid_dev_count()`
- :cpp:any:`pjsua_vid_dev_get_info()`
- :cpp:any:`pjsua_vid_enum_devs()`

In addition, the :any:`PJMEDIA videodev </api/generated/pjmedia/group/group__video__device__reference>`
also provides this API to detect change in device availability:

- - :cpp:any:`pjmedia_vid_dev_refresh()`

Video preview API
~~~~~~~~~~~~~~~~~

The video preview API can be used to show the output of capture device
to a video window:

- struct :cpp:any:`pjsua_vid_preview_param`
- :cpp:any:`pjsua_vid_preview_start()`
- :cpp:any:`pjsua_vid_preview_get_win()`
- :cpp:any:`pjsua_vid_preview_stop()`

Video Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video is enabled/disabled on :cpp:any:`pjsua_call_setting`.

Video settings are mostly configured on the :cpp:any:`pjsua_acc_config` with the
following fields:

- :cpp:any:`pjsua_acc_config::vid_in_auto_show`
- :cpp:any:`pjsua_acc_config::vid_out_auto_transmit`
- :cpp:any:`pjsua_acc_config::vid_cap_dev`
- :cpp:any:`pjsua_acc_config::vid_rend_dev`


.. _vid_ug_vcm:

Video Call Manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default video behavior for a call is controlled by the account
settings above. On top of that, the application can manipulate video of
an already-going call by using :cpp:any:`pjsua_call_set_vid_strm()` API.

Use :cpp:any:`pjsua_call_get_vid_stream_idx()` to get the media stream index of 
the default video stream in the call.


Video Call Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Video media information are available in :cpp:any:`pjsua_call_info`.


Video Call Stream Information and Statistic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use the following API to query call's stream information and statistic.


- :cpp:any:`pjsua_call_get_stream_info()`
- :cpp:any:`pjsua_call_get_stream_stat()`
- :cpp:any:`pjsua_call_get_med_transport_info()`

.. note::

   The :cpp:any:`pjsua_call_get_media_session()` has been deprecated since its use is unsafe.


Video Window API
~~~~~~~~~~~~~~~~~~~~~~~~

A video window is a rectangular area in your monitor to display video
content. The video content may come from remote stream, local camera (in
case of preview), AVI playback, or any other video playback. Application
mostly will be interested in the native handle of the video window so
that it can embed it in its application window, however we also provide
simple and commonly used API for manipulating the window.

See:

- :cpp:any:`pjsua_vid_enum_wins()`
- :cpp:any:`pjsua_vid_win_get_info()`
- :cpp:any:`pjsua_vid_win_set_show()`
- :cpp:any:`pjsua_vid_win_set_pos()`
- :cpp:any:`pjsua_vid_win_set_size()`


Video Codec API
~~~~~~~~~~~~~~~~~~~~~~~

API for managing video codecs:

- :cpp:any:`pjsua_vid_enum_codecs()`
- :cpp:any:`pjsua_vid_codec_set_priority()`
- :cpp:any:`pjsua_vid_codec_get_param()`
- :cpp:any:`pjsua_vid_codec_set_param()`

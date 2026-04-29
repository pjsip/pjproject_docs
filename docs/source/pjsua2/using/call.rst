
Calls
====================

.. contents:: Table of Contents
    :depth: 2


Calls are represented by :cpp:class:`pj::Call` class.

Subclassing the Call class
------------------------------------
To use the ``Call`` class, application SHOULD subclass it, such as:

.. code-block:: c++

    class MyCall : public Call
    {
    public:
        MyCall(Account &acc, int call_id = PJSUA_INVALID_ID)
        : Call(acc, call_id)
        { }

        ~MyCall()
        { }

        // Notification when call's state has changed.
        virtual void onCallState(OnCallStateParam &prm);

        // Notification when call's media state has changed.
        virtual void onCallMediaState(OnCallMediaStateParam &prm);
    };

Application implement Call's callbacks to process events related to the call, such as 
:cpp:func:`pj::Call::onCallState()`, and many more. See :cpp:class:`pj::Call` class
for more info.


Making outgoing calls
--------------------------------------
Make outgoing call is by invoking :cpp:func:`pj::Call::makeCall()` with the destination URI
string (something like ``"sip:alice@example.com"``). The URI can also be enclosed in ``name-addr``
form (``[ display-name ] <SIP/SIPS URI>``) (such as ``"Alice <sip:alice@example.com;transport=tcp>"``).
Note that an account instance is required to create a call instance:

.. code-block:: c++

    Call *call = new MyCall(*acc);
    CallOpParam prm(true); // Use default call settings
    try {
        call->makeCall(dest_uri, prm);
    } catch(Error& err) {
        cout << err.info() << endl;
    }


Receiving Incoming Calls
--------------------------------------
Incoming calls are reported as :cpp:func:`pj::Account::onIncomingCall()` callback. Note that
this is the callback of the :cpp:any:`pj::Account` class (not :cpp:any:`pj::Call`). You must derive a class from the 
:cpp:any:`pj::Account` class to handle incoming calls.

Below is a sample code of the callback implementation:

.. code-block:: c++

    void MyAccount::onIncomingCall(OnIncomingCallParam &iprm)
    {
        Call *call = new MyCall(*this, iprm.callId);
        CallOpParam prm;
        prm.statusCode = PJSIP_SC_OK;
        call->answer(prm);
    }

For incoming calls, the call instance is created in the callback function as shown above. 
Application should make sure to store the call instance during the lifetime of the call (that is 
until the call is disconnected (see :ref:`pjsua2_call_disconnection` below)).


Call Properties
----------------
All call properties such as state, media state, remote peer information, etc. are stored in 
:cpp:class:`pj::CallInfo` class, which can be retrieved from the call object with using 
:cpp:func:`pj::Call::getInfo()` method.


.. _pjsua2_call_disconnection:

Call Disconnection
-------------------
Call disconnection event is a special event since once the callback that reports this event returns, 
the call is no longer valid and any operations invoked to the call object will raise error exception. 
Thus, it is recommended to delete the call object inside the callback.

The call disconnection is reported in :cpp:func:`pj::Call::onCallState()` callback. Below is
a sample implementation:

.. code-block:: c++

    void MyCall::onCallState(OnCallStateParam &prm)
    {
        CallInfo ci = getInfo();
        if (ci.state == PJSIP_INV_STATE_DISCONNECTED) {
            /* Delete the call */
            delete this;
        }
    }

Working with Call's Audio Media
-------------------------------------------------
Application can only operate the call's audio media when the call's audio media state is ready (or active).
Usually this happens once the call has been established, although media can active before that (it is
called early media), and established call can have no media (such as when it is being put on-hold).

The changes to the call's media state is reported in :cpp:func:`pj::Call::onCallMediaState()` callback. 
Only when the call's audio media state is ready (or active) the function :cpp:func:`pj::Call::getAudioMedia()` 
will return a valid audio media.

Below is a sample code to connect the call to the sound device when the media is active:

.. code-block:: c++

    void MyCall::onCallMediaState(OnCallMediaStateParam &prm)
    {
        CallInfo ci = getInfo();

        for (unsigned i = 0; i < ci.media.size(); i++) {
            if (ci.media[i].type==PJMEDIA_TYPE_AUDIO) {
                try {
                    AudioMedia aud_med = getAudioMedia(i);

                    // Connect the call audio media to sound device
                    AudDevManager& mgr = Endpoint::instance().audDevManager();
                    aud_med.startTransmit(mgr.getPlaybackDevMedia());
                    mgr.getCaptureDevMedia().startTransmit(aud_med);
                }
                catch(const Error &e) {
                  // Handle invalid or not audio media error here
                }
            }
        }
    }

When the audio media becomes inactive (for example when the call is put on hold), there is no need to
stop the call's audio media transmission since they will be removed automatically from the conference
bridge, and this will automatically remove all connections to/from the call.


Setting media direction
------------------------
By default each media stream is negotiated as ``sendrecv``. To
configure a different direction (sendonly, recvonly, or inactive)
for one or more streams in a call, set the ``PJSUA_CALL_SET_MEDIA_DIR``
flag on :cpp:any:`pj::CallSetting::flag` and populate
:cpp:any:`pj::CallSetting::mediaDir` with the per-stream direction.

The direction is honoured wherever ``CallSetting`` is accepted —
:cpp:func:`pj::Call::makeCall()`, :cpp:func:`pj::Call::answer()`,
:cpp:func:`pj::Call::reinvite()`, :cpp:func:`pj::Call::update()`, and
the :cpp:func:`pj::Call::onCallRxOffer()` /
:cpp:func:`pj::Call::onCallRxReinvite()` callbacks. It then persists for
subsequent offers and answers on the same call. Note that the direction
can only be **narrowed**
once set: a stream that was set to ``PJMEDIA_DIR_ENCODING`` can
become inactive on a later re-INVITE but will not flip back to
``sendrecv`` from the local side.

The index of each ``mediaDir`` entry corresponds to the provisional
media slot in :cpp:any:`pj::CallInfo::provMedia`. For offers that
add new media (initial offer, or a re-INVITE that adds streams),
the index orders all new **audio** media first, then **video**.
So a new call with two audio streams and one video stream uses
``mediaDir[0]`` and ``mediaDir[1]`` for the audios and ``mediaDir[2]``
for the video.

**Example — make an outgoing call as receive-only:**

.. code-block:: c++

    CallOpParam prm(true);
    prm.opt.flag |= PJSUA_CALL_SET_MEDIA_DIR;
    prm.opt.mediaDir.push_back(PJMEDIA_DIR_DECODING);  // audio: recvonly

    try {
        call->makeCall(dest_uri, prm);
    } catch(Error& err) {
    }

**Example — answer with a one-way (send-only) audio path:**

.. code-block:: c++

    void MyAccount::onIncomingCall(OnIncomingCallParam &iprm) override
    {
        Call *call = new MyCall(*this, iprm.callId);
        CallOpParam prm;
        prm.statusCode = PJSIP_SC_OK;
        prm.opt.flag |= PJSUA_CALL_SET_MEDIA_DIR;
        prm.opt.mediaDir.push_back(PJMEDIA_DIR_ENCODING);
        call->answer(prm);
    }

**Example — narrow an existing stream via re-INVITE** (e.g. mute
the outgoing audio mid-call):

.. code-block:: c++

    CallOpParam prm(true);
    prm.opt.flag |= PJSUA_CALL_SET_MEDIA_DIR;
    prm.opt.mediaDir.push_back(PJMEDIA_DIR_DECODING);  // recvonly

    try {
        call->reinvite(prm);
    } catch(Error& err) {
    }

For per-video-stream direction changes that don't go through a
re-INVITE — e.g. flipping a video stream's direction locally
without renegotiation — see :cpp:func:`pj::Call::vidSetStream` with
the ``PJSUA_CALL_VID_STRM_CHANGE_DIR`` operation in
:any:`/pjsua2/using/media_video`. Putting a call on hold is the
more common case and is handled by :cpp:func:`pj::Call::setHold` /
:cpp:func:`pj::Call::reinvite` directly; you don't need to drive
``mediaDir`` manually for hold.

.. note::

   *Inactive* and *disabled* are different SDP concepts.
   **Inactive** (``PJMEDIA_DIR_NONE`` here, ``a=inactive`` on the
   wire) keeps the stream negotiated — real port, codec list,
   RTCP still flowing (Sender / Receiver Reports keep updating).
   RTP is the part that's suppressed by ``a=inactive``; if
   PJMEDIA's media keep-alive is enabled
   (``PJMEDIA_STREAM_ENABLE_KA``, off by default) the stream still
   emits keep-alive packets every few seconds — those are also
   RTP packets (empty RTP frame in the default ``KA_EMPTY_RTP``
   mode, or a user-defined payload in ``KA_USER`` mode). This is
   what you set via ``mediaDir``.
   **Disabled** is a stream rejected with ``port=0`` on the m-line
   per RFC 3264: no resources allocated, no codec negotiation, no
   RTP, no RTCP, no keep-alive — the m-line is preserved only for
   index alignment with the original offer. ``mediaDir`` does not
   express disabled — for that, lower ``audioCount`` /
   ``videoCount`` / ``textCount`` to drop the streams you don't
   want, optionally combined with the
   ``PJSUA_CALL_INCLUDE_DISABLED_MEDIA`` flag to keep the
   placeholder m-line in the offer.

PJSUA-LIB applications use the same flag plus the
:cpp:any:`pjsua_call_setting::media_dir` array
(``PJMEDIA_MAX_SDP_MEDIA`` entries instead of a vector).


Call Operations
-------------------
Call have many other operations, such as hanging up, putting the call on hold, sending re-INVITE, etc. 
See :cpp:class:`pj::Call` reference for more info.


Instant Messaging(IM)
---------------------
.. note::

    Usually it is more appropriate to do instant messaging outside the context of a
    call. Application can send IM and typing indication outside a call by using 
    :cpp:func:`pj::Buddy::sendInstantMessage()` and :cpp:func:`pj::Buddy::sendTypingIndication()`.
    More will be explained in the next section.

Application can send IM within a call using :cpp:func:`pj::Call::sendInstantMessage()`. The transmission status 
of outgoing instant messages is reported in :cpp:func:`pj::Call::onInstantMessageStatus()` callback.

In addition, you can also send typing indication using 
:cpp:func:`pj::Call::sendTypingIndication()`.

Incoming IM and typing indication received within a call will be reported in 
:cpp:func:`pj::Call::onInstantMessage()` and :cpp:func:`pj::Call::onTypingIndication()`
callbacks.

While it is recommended to send IM outside call context, application should handle incoming
IM **inside** call context for robustness.

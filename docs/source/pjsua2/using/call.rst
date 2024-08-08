
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

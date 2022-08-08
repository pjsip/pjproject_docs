Presence and Instant Messaging
====================================
Presence feature in PJSUA2 centers around :cpp:class:`pj::Buddy` class. This class represents 
a remote buddy (a person, or a SIP endpoint).

Subclassing the Buddy class
----------------------------
To use the :cpp:class:`pj::Buddy` class, normally application SHOULD create its own subclass, such as:

.. code-block:: c++

    class MyBuddy : public Buddy
    {
    public:
        MyBuddy() {}
        ~MyBuddy() {}

        virtual void onBuddyState();
    };

In its subclass, application can implement the buddy callback to get the notifications on buddy state change.

Subscribing to Buddy's Presence Status
---------------------------------------
To subscribe to buddy's :cpp:class:`presence status <pj::PresenceStatus>`, you need to add a buddy object 
and subscribe to buddy's presence status. Below is a sample code:

.. code-block:: c++

    BuddyConfig cfg;
    cfg.uri = "sip:alice@example.com";
    MyBuddy buddy;
    try {
        buddy.create(*acc, cfg);
        buddy.subscribePresence(true);
    } catch(Error& err) {
    }

Then you can get the buddy's presence state change inside the :cpp:func:`pj::Buddy::onBuddyState()` callback:

.. code-block:: c++

    void MyBuddy::onBuddyState()
    {
        BuddyInfo bi = getInfo();
        cout << "Buddy " << bi.uri << " is " << bi.presStatus.statusText << endl;
    }

For more information, please see :cpp:class:`pj::Buddy` and :cpp:class:`pj::PresenceStatus`.


Responding to Presence Subscription Request
-------------------------------------------
By default, incoming presence subscription to an account will be accepted automatically. Application probably 
wants to change this behavior, for example only to automatically accept subscription if it comes from one of 
the buddy in the buddy list, and for anything else prompt the user if he/she wants to accept the request.

This can be done by overriding the :cpp:func:`pj::Account::onIncomingSubscribe()` callback. 


Changing Account's Presence Status
----------------------------------
To change account's presence status, app can call :cpp:func:`pj::Account::setOnlineStatus()` 
to set basic account's presence status (i.e. available or not available) and optionally, some extended 
information (e.g. busy, away, on the phone, etc). Sample code:

.. code-block:: c++

    try {
        PresenceStatus ps;
        ps.status = PJSUA_BUDDY_STATUS_ONLINE;
        // Optional, set the activity and some note
        ps.activity = PJRPID_ACTIVITY_BUSY;
        ps.note = "On the phone";
        acc->setOnlineStatus(ps);
    } catch(Error& err) {
    }

When the presence status is changed, the account will publish the new status to all of its presence 
subscribers, either with SIP **PUBLISH** or **NOTIFY** request, or both, depending on account configuration.


Instant Messaging(IM)
---------------------
You can send IM using :cpp:func:`pj::Buddy::sendInstantMessage()`. The transmission status of outgoing 
IM is reported in :cpp:func:`pj::Account::onInstantMessageStatus()` callback.

In addition to sending instant messages, you can also send typing indication to remote buddy using 
:cpp:func:`pj::Buddy::sendTypingIndication()`.

Incoming IM and typing indication received outside the scope of a call will be reported in 
:cpp:func:`pj::Account::onInstantMessage()` and :cpp:func:`pj::Account::onTypingIndication()` callbacks.

.. tip::

    Use :cpp:func:`pj::Account::findBuddy()` and :cpp:func:`pj::Account::findBuddy2()` to match
    incoming IM and typing indication to a buddy in the account's buddy list.




Accounts
====================
Accounts provide identity (or identities) of the user who is currently using the application. 
An account has one SIP Uniform Resource Identifier (URI) associated with it. In SIP terms, 
this URI acts as Address of Record (AOR) of the person and is used as the From header in 
outgoing requests.

Account may or may not have client registration associated with it. An account is also 
associated with route set and some authentication credentials, which are used when sending 
SIP request messages using the account. An account also has presence status, which will be 
reported to remote peer when they subscribe to the account's presence, or which is published 
to a presence server if presence publication is enabled for the account.

At least one account MUST be created in the application, since any outgoing requests require 
an account context. If no user association is required, application can create a userless 
account by calling Account.create(). A userless account identifies local endpoint instead 
of a particular user, and it corresponds to a particular transport ID.

Also one account must be set as the default account, which will be used as the account 
identity when pjsua fails to match incoming request with any accounts using the stricter 
matching rules.

Subclassing the Account class
---------------------------------
To use the :cpp:class:`pj::Account` class, normally application SHOULD create its own subclass, 
in order to  receive notifications for the account. For example:

.. code-block:: c++

    class MyAccount : public Account
    {
    public:
        MyAccount() {}
        ~MyAccount() {}

        virtual void onRegState(OnRegStateParam &prm)
        {
            AccountInfo ai = getInfo();
            cout << (ai.regIsActive? "*** Register: code=" : "*** Unregister: code=")
                 << prm.code << endl;
        }
    
        virtual void onIncomingCall(OnIncomingCallParam &iprm)
        {
            Call *call = new MyCall(*this, iprm.callId);

            // Just hangup for now
            CallOpParam op;
            op.statusCode = PJSIP_SC_DECLINE;
            call->hangup(op);
            
            // And delete the call
            delete call;
        }
    };

In its subclass, application can implement the account callbacks, which is basically used to 
process events related to the account, such as:

- the status of SIP registration
- incoming calls
- incoming presence subscription requests
- incoming instant message not from buddy

Application needs to override the relevant callback methods in the derived class to handle 
these particular events.

If the events are not handled, default actions will be invoked:

- incoming calls will not be handled
- incoming presence subscription requests will be accepted
- incoming instant messages from non-buddy will be ignored

Creating Userless Accounts
--------------------------
A userless account identifies a particular SIP endpoint rather than a particular user. Some 
other SIP softphones may call this peer-to-peer mode, which means that we are calling another 
computer via its address rather than calling a particular user ID. For example, we might 
identify ourselves as "sip:192.168.0.15" (a userless account) rather than, say, 
"sip:alice@pjsip.org".

In the lower layer PJSUA-LIB API, a userless account is associated with a SIP transport, and 
is created with ``pjsua_acc_add_local()`` API. This concept has been deprecated in PJSUA2, 
and rather, a userless account is a "normal" account with a userless ID URI (e.g. 
"sip:192.168.0.15") and without registration. Thus creating a userless account is exactly 
the same as creating "normal" account.


Creating Account
----------------
We need to configure :cpp:class:`pj::AccountConfig` and call :cpp:class:`Account.create() <pj::Account>` 
to create the account. At the very minimum, pjsua only requires the account's ID, which is 
an URI to identify the account (or in SIP terms, it's called Address of Record/AOR). 
Here's a snippet:


.. code-block:: c++

    AccountConfig acc_cfg;
    acc_cfg.idUri = "sip:test1@pjsip.org";

    MyAccount *acc = new MyAccount;
    try {
        acc->create(acc_cfg);
    } catch(Error& err) {
        cout << "Account creation error: " << err.info() << endl;
    }

The account created above doesn't do anything except to provide identity in the "From:" header 
for outgoing requests. The account will not register to SIP server or anything.

Typically you will want the account to authenticate and register to your SIP server so that 
you can receive incoming calls. To do that you will need to configure some more settings in 
your :cpp:class:`pj::AccountConfig`, something like this:

.. code-block:: c++

    AccountConfig acc_cfg;
    acc_cfg.idUri = "sip:test1@pjsip.org";
    acc_cfg.regConfig.registrarUri = "sip:pjsip.org";
    acc_cfg.sipConfig.authCreds.push_back( AuthCredInfo("digest", "*", "test1", 0, "secret1") );

    MyAccount *acc = new MyAccount;
    try {
        acc->create(acc_cfg);
    } catch(Error& err) {
        cout << "Account creation error: " << err.info() << endl;
    }

Account Configurations
-----------------------
There are more settings that can be specified in :cpp:class:`pj::AccountConfig`, like:

- :cpp:class:`pj::AccountRegConfig`, the registration settings, such as registrar server and retry interval.
- :cpp:class:`pj::AccountSipConfig`, the SIP settings, such as credential information and proxy server.
- :cpp:class:`pj::AccountCallConfig`, the call settings, such as whether reliable provisional response (SIP 100rel) is required.
- :cpp:class:`pj::AccountPresConfig`, the presence settings, such as whether presence publication (PUBLISH) is enabled.
- :cpp:class:`pj::AccountMwiConfig`, the MWI (Message Waiting Indication) settings.
- :cpp:class:`pj::AccountNatConfig`, the NAT settings, such as whether STUN or ICE is used.
- :cpp:class:`pj::AccountMediaConfig`, the media settings, such as Secure RTP (SRTP) related settings.
- :cpp:class:`pj::AccountVideoConfig`, the video settings, such as default capture and render device.
- :cpp:class:`pj::AccountIpChangeConfig`, the settings during IP change.


Account Operations
--------------------------------------
Some of the operations to the :cpp:class:`pj::Account` object:

- manage registration
- manage buddies/contacts
- manage presence online status

Please see the reference documentation for :cpp:class:`pj::Account` for more info. 
Calls, presence, and buddy will be explained in later chapters.



The Endpoint
====================

.. contents:: Table of Contents
    :depth: 2


The :cpp:class:`pj::Endpoint` class is a singleton class, and application MUST create
this class instance before it can do anything else, and similarly, once this class is destroyed, 
application must NOT call any library API. This class is the core class of PJSUA2, and it 
provides the following functions:

- Starting up and shutting down
- Customization of configurations, such as core UA (User Agent) SIP configuration, media configuration, 
  and logging configuration

This chapter will describe the functions above.


Instantiating the endpoint
--------------------------
Before anything else, you must instantiate the Endpoint class:

.. code-block:: c++

    Endpoint *ep = new Endpoint;

Once the endpoint is instantiated, you can retrieve the Endpoint instance using
:cpp:func:`pj::Endpoint::instance()` static method.

Creating the library
----------------------
Create the library by calling its :cpp:func:`pj::Endpoint::libCreate()` method:

.. code-block:: c++

    try {
        ep->libCreate();
    } catch(Error& err) {
        cout << "Startup error: " << err.info() << endl;
    }

The ``libCreate()`` method will raise exception if error occurs, so we need to trap the exception using 
try/catch clause as above. See :cpp:class:`pj::Error` for reference.

Initializing and configuring the library
----------------------------------------------------------------------------

The :cpp:class:`pj::EpConfig` class provides endpoint configuration which allows the customization of 
the following settings:

- :cpp:class:`pj::UAConfig`, to specify core SIP user agent settings.
- :cpp:class:`pj::MediaConfig`, to specify various media *global* settings
- :cpp:class:`pj::LogConfig`, to customize logging settings.

.. tip::

    Some settings can be specified on per account basis, in the 
    :cpp:class:`pj::AccountConfig`, when creating an :cpp:class:`pj::Account`. Creating accounts
    will be explained in :doc:`next section <account>`.

To customize the settings, create instance of ``EpConfig`` class and specify them during the endpoint 
initialization (will be explained more later), for example:

.. code-block:: c++

    EpConfig ep_cfg;
    ep_cfg.logConfig.level = 5;
    ep_cfg.uaConfig.maxCalls = 4;
    ep_cfg.mediaConfig.sndClockRate = 16000;

Next, you can initialize the library by calling :cpp:func:`pj::Endpoint::libInit()`:

.. code-block:: c++

    try {
        EpConfig ep_cfg;
        // Specify customization of settings in ep_cfg
        ep->libInit(ep_cfg);
    } catch(Error& err) {
        cout << "Initialization error: " << err.info() << endl;
    }

The snippet above initializes the library with the default settings.

Creating one or more transports
--------------------------------------------------
Application needs to create one or more transports before it can send or receive SIP messages:

.. code-block:: c++

    try {
        TransportConfig tcfg;
        tcfg.port = 5060;
        TransportId tid = ep->transportCreate(PJSIP_TRANSPORT_UDP, tcfg);
    } catch(Error& err) {
        cout << "Transport creation error: " << err.info() << endl;
    }

The :cpp:func:`pj::Endpoint::transportCreate()` method returns the newly created Transport ID and 
it takes the transport type and :cpp:class:`pj::TransportConfig` object to customize the transport 
settings like bound address and listening port number. Without this, by default the transport will be 
bound to ``INADDR_ANY`` and any available port.

There is no real use of the Transport ID, except to create userless account (with 
:cpp:func:`pj::Account::create()`, as will be explained later), and perhaps to display the list of transports to user if the application wants it.

Starting the library
--------------------
Now we're ready to start the library. We need to start the library to finalize the initialization phase,
e.g. to complete the initial STUN address resolution, initialize/start the sound device, etc. To start 
the library, call :cpp:func:`pj::Endpoint::libStart()` method:

.. code-block:: c++

    try {
        ep->libStart();
    } catch(Error& err) {
        cout << "Startup error: " << err.info() << endl;
    }

Shutting down the library
--------------------------------------
Once the application exits, the library needs to be shutdown so that resources can be released back to 
the operating system. Although this can be done by deleting the Endpoint instance, which will internally 
call :cpp:func:`pj::Endpoint::libDestroy()`, it is better to call it manually because on Java or Python 
there are problems with garbage collection as explained earlier:

.. code-block:: c++

    ep->libDestroy();
    delete ep;



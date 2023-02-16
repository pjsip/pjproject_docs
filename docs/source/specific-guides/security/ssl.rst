.. _guide_ssl:

SSL/TLS
=========================================

.. contents:: Table of Contents
    :depth: 2


Requirements
------------

The TLS support in PJSIP requires one of the following:

- OpenSSL
- BoringSSL: :pr:`2856`
- GnuTLS: :issue:`2082`
- Mac/iOS native backend: :issue:`2482` and :issue:`2185`

This page mostly describes TLS usage with OpenSSL. For other backends, please refer to the GitHub issues/PR above.


Installing  OpenSSL
----------------------------------------

For OpenSSL installation, refer to the following guides:

- :any:`windows_openssl` (for Windows)
- :any:`ios_openssl` (for iOS/iPhone)
- :any:`android_openssl` (for Android)
- For Debian/Ubuntu:

  .. code-block:: shell

     $ sudo apt-get install libssl-dev

- Note that native SSL backend is available for Mac/iOS, see :pr:`2482`.
- (deprecated) *BB10: using bundled OpenSSL*
- (deprecated) TLS support on Symbian is implemented natively using CSecureSocket,
  hence it doesn’t require OpenSSL development kit. Please see *Configuring TLS on Symbian* for the
  detailed information.


Build PJSIP with TLS Support
----------------------------

SIP TLS transport is implemented based on PJLIB's 
:doc:`SSL Socket API </api/generated/pjlib/group/group__PJ__SSL__SOCK>`,
and its availability is based on :c:macro:`PJ_HAS_SSL_SOCK` macro value. For
*autoconf* build system, the value is automatically detected based on
OpenSSL availability. For other platforms such as Windows and Symbian,
please declare this in your :ref:`config_site.h`:

.. code-block:: c

   #define PJ_HAS_SSL_SOCK 1

Note: 

- The :c:macro:`PJSIP_HAS_TLS_TRANSPORT` default value will be set to
  :c:macro:`PJ_HAS_SSL_SOCK` setting. 


Configuring SIP TLS transport
-------------------------------
Once TLS support has been built, configure the TLS settings as follows.

For PJSUA2 based applications:

- Configure the :cpp:any:`pj::TlsConfig` in the :cpp:any:`pj::TransportConfig`
- Create the TLS transport by following :any:`pjsua2_create_transport`


For PJSUA-LIB based applications:

- Configure the TLS certificates in :cpp:any:`pjsua_transport_config::tls_setting`.
- Create TLS transport with :cpp:any:`pjsua_transport_create()` and so on. See
  :doc:`PJSUA-LIB Transport </api/generated/pjsip/group/group__PJSUA__LIB__TRANSPORT>`.

For PJSIP based applications:

- See  :doc:`PJSIP TLS Transport </api/generated/pjsip/group/group__PJSIP__TRANSPORT__TLS>`.


Using SIP TLS transport
-------------------------------
Once SIP transport has been configured, it will be used to send requests to remote endpoint
that requires TLS transport, i.e. either the URL contains ``;transport=tls`` parameter
or the URI is ``sips:``.

The instructions are similar to :any:`/specific-guides/network_nat/sip_tcp`; just replace
``"tcp"`` with ``"tls"``.


Running pjsua as TLS Server
------------------------------------------------

1. You will need specify a TLS certificate, represented by three PEM
   files:

   a. The root certificate
   b. The server certificate
   c. The private key

2. Run pjsua:

   .. code-block:: shell

      $ ./pjsua --use-tls --tls-ca-file root.pem --tls-cert-file server-cert.pem --tls-privkey-file privkey.pem


3. To see more TLS options, run `./pjsua --help`.


Running pjsua as TLS Client
------------------------------------------------
To make call to SERVER using TLS:


.. code-block:: shell

   $ ./pjsua --use-tls <sip:SERVER;transport=tls>

To see more TLS options, run ``./pjsua --help``.


Enable TLS mutual authentication
-------------------------------------------

Basically, it is done by two ways certificate verification, so both
sides must provide TLS certificate (as described in [#pjsua-tls-server
Running pjsua as TLS Server] above) and enable verification: 

- as TLS server: append pjsua option ``--tls-verify-client``, 
- as TLS client: append pjsua option ``--tls-verify-server``.

To see about TLS in library level, check the TLS docs in the links
section below.

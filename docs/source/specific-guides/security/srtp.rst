SRTP
=====================

.. contents:: Table of Contents
    :depth: 2



Introduction
----------------
Secure Real-time Transport Protocol (SRTP) is a profile of the 
Real-time Transport Protocol (RTP) to provide confidentiality, message authentication, 
and replay protection to the RTP/RTCP traffic. SRTP is an IETF Standard, 
defined in :rfc:`3711`.

In PJSIP, SRTP support is included in version 0.9 (see ticket :issue:`61`). SRTP is
implemented by means of :any:`/specific-guides/media/transport_adapter`.


Features
--------
The SRTP functionality in PJSIP has the following features: 

- SRTP (:rfc:`3711`), using the Open Source
  `libsrtp <https://github.com/cisco/libsrtp>`__ library. 
- Keys exchange using Security Descriptions for Media Streams (SDESC, :rfc:`4568`) 
- Supported cryptos:

  - AES_CM_128_HMAC_SHA1_80 
  - AES_CM_128_HMAC_SHA1_32 
- Secure RTCP (SRTCP) is supported.

Negotiation of crypto session parameters in SDP is currently not
supported.


Requirements
------------

SRTP feature in PJSIP uses the Open Source `libsrtp <https://github.com/cisco/libsrtp>`__ 
library from Cisco Systems, Inc. Copy of
`libsrtp <https://github.com/cisco/libsrtp>`__ is included in PJSIP
source tree in :sourcedir:`third_party/srtp` directory. There is no other
software to download.

`libsrtp <https://github.com/cisco/libsrtp>`__ is distributed under
BSD-like license, you must satisfy the license requirements if you
incorporate SRTP in your application. Please see :ref:`3rd Party Licensing <licensing_3rd_party>` 
page for more information.



How to integrate
-----------------

There is a new third party library in the distribution, namely
**libsrtp**, you will need to add this library into your
application's input libraries specification.

For GNU build systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. You will need to re-run ``./configure``, ``make dep`` and ``make`` to update ``build.mak`` 
   and rebuild the project dependencies. 
#. If **your** Makefile includes ``build.mak`` , you just need to 
   rebuild your application as the input libraries will be updated automatically (by ``build.mak``). 
#. If you maintain your own independent Makefile, please add ``libsrtp-$(TARGET)``
   from ``third_party/lib`` directory to your input libraries.


For Visual Studio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. New ``libsrtp`` project has been
   added into pjproject Visual Studio workspaces.
#. If you maintain your own application workspace, you need to add ``libsrtp``
   project into your application. The ``libsrtp`` project files are in
   ``third_party/build/srtp`` directory.



Building PJSIP with SRTP Support
--------------------------------

Availability
~~~~~~~~~~~~

SRTP feature is currently available in: 

- Visual Studio for Windows targets
- GNU based build system (for Linux, including uC-Linux for embedded systems, Mingw,
  MacOS X, and \*nix based platforms)
- Windows Mobile targets (deprecated)
- Symbian targets (deprecated)


Building
~~~~~~~~

libsrtp is always built by default, from ``third_party/build/srtp``
directory.

Support for SRTP is enabled by default in PJMEDIA and PJSUA-LIB. To
**disable** this feature, declare :cpp:any:`PJMEDIA_HAS_SRTP` as zero in your :any:`config_site.h`:

.. code-block:: c

   #define PJMEDIA_HAS_SRTP  0



Using SRTP
----------

SRTP is implemented as media transport in PJMEDIA. In the high level
:doc:`/api/pjsua-lib/index`, the
use of SRTP is controlled by couple of settings as explained below.

Using SRTP in PJSUA-LIB
~~~~~~~~~~~~~~~~~~~~~~~

In :doc:`/api/pjsua-lib/index`, the use of SRTP is controlled by settings in 
both :cpp:any:`pjsua_config` and :cpp:any:`pjsua_acc_config`. The settings in
:cpp:any:`pjsua_config` specify the default settings for all accounts, and the settings in
:cpp:any:`pjsua_acc_config` can be used to further set the behavior for that specific account.

In both :cpp:any:`pjsua_config` and :cpp:any:`pjsua_acc_config`, there are two
configuration items related to SRTP:

use_srtp
```````````````

The :cpp:any:`pjsua_config::use_srtp` and :cpp:any:`pjsua_acc_config::use_srtp` options control whether secure media transport (SRTP) should be used for this account. Valid values are: 

- :cpp:any:`PJMEDIA_SRTP_DISABLED` (0): SRTP is disabled, and incoming call with
  RTP/SAVP transport will be rejected with 488/Not Acceptable Here
  response. 
- :cpp:any:`PJMEDIA_SRTP_OPTIONAL` (1): SRTP will be advertised and
  SRTP will be used if remote supports it, but the call may fall back to
  unsecure media. Incoming call with RTP/SAVP is accepted and responded
  with RTP/SAVP too. 
- :cpp:any:`PJMEDIA_SRTP_MANDATORY` (2): secure media is
  mandatory, and the call can only proceed if secure media can be
  established. 
     
The default value for this option is :cpp:any:`PJSUA_DEFAULT_USE_SRTP`, which is zero (disabled).

srtp_secure_signaling
```````````````````````````

The :cpp:any:`pjsua_config::srtp_secure_signaling` and :cpp:any:`pjsua_acc_config::srtp_secure_signaling` options controls whether SRTP requires secure signaling to be used. This option is only used when ``use_srtp`` option above is non-zero. Valid values are: 

- 0: SRTP does not require secure signaling (not recommended) 
- 1: SRTP requires secure transport such as TLS to be used. 
- 2: SRTP requires secure end-to-end transport (``sips:`` URI scheme) to be used. 

The default value for this option is :cpp:any:`PJSUA_DEFAULT_SRTP_SECURE_SIGNALING`, 
which is 1 (require TLS transport).

pjsua
~~~~~

Two new options were added to *pjsua*:

- ``--use-srtp=N`` This corresponds to ``use_srtp`` setting above.
  Valid values are 0, 1, or 2. Default value is 0.
- ``--srtp-secure=N`` This corresponds to ``srtp_secure_signaling``
  setting above. Valid values are 0, 1, or 2. Default value is 1.

Sample usage:

.. code-block:: shell

    $ ./pjsua --use-tls --use-srtp=1 sip:alice@example.com;transport=tls


Using SRTP Transport Directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SRTP transport may also be used directly without having to involve
SDP negotiations (for example, to use SRTP without SIP). Please see
``streamutil`` from the :doc:`/api/samples` collection for a sample application. 
For this to work, you will need to have a different mechanism to exchange keys between
endpoints.

To use SRTP transport directly: 

- Call :cpp:any:`pjmedia_transport_srtp_create()` to create the SRTP adapter, giving it the actual media transport
  instance (such as UDP transport). 
- Call :cpp:any:`pjmedia_transport_srtp_start()` to active SRTP session, giving it both local and remote crypto settings
  and keys. 
- Call :cpp:any:`pjmedia_transport_attach()` to configure the remote RTP/RTCP addresses and attach your RTP and RTCP
  callbacks. 
- Call :cpp:any:`pjmedia_transport_send_rtp()` and  :cpp:any:`pjmedia_transport_send_rtcp()` to send RTP/RTCP packets. 
- Once you done with your session, call :cpp:any:`pjmedia_transport_close()` 
  to destroy the SRTP adapter (and optionally the actual transport which
  is attached to the SRTP adapter, depending on whether *close_member_tp*
  flag is set in the :cpp:any:`pjmedia_srtp_setting`  when creating the SRTP adapter).



AES-GCM support
-----------------

PJSIP 2.6 enabled the support for AES-GCM (:issue:`1943`), however the bundled
libSRTP (1.5.4) at that time has compatibility issue with OpenSSL 1.1.0.
Updating the libSRTP was done in :issue:`1993`, included in 2.7.

As an alternative to the bundled libSRTP, users are also allowed to use
external libSRTP by specifying ``--with-external-srtp``. Using :issue:`2050`,
it's been tested to work with external libSRTP 1.5.4 and 2.1.0. Note
about this option, using libSRTP with AES-GCM would also require the
user to enable building pjsip with ssl.

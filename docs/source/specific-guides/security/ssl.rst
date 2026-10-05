.. _guide_ssl:

Using SSL/TLS with PJSIP
=========================================

.. contents:: Table of Contents
    :depth: 2


Overview
--------

PJSIP uses TLS to secure the **SIP signalling transport**: SIP messages
on port 5061 (the standard) or any other TLS listening port, selected
when the SIP URI carries ``;transport=tls`` or uses the ``sips:``
scheme.

Two related mechanisms have their own guides:

- **Media security** (SDES-SRTP and DTLS-SRTP) is described in
  :doc:`/specific-guides/security/srtp`. It is not fully independent of
  the TLS library, though: the SRTP crypto attribute in SDP (the SDES
  key material) is generated with the secure random bytes generator of
  the TLS backend, and DTLS-SRTP needs OpenSSL. See
  :ref:`tls_capabilities` and :ref:`tls_openssl_features`.
- **SIP digest authentication** (MD5, SHA-256, SHA-512-256 and AKA) is
  described in :ref:`guide_digest_auth`. Its SHA-256 variants also need
  OpenSSL.

This page is organised as follows:

1. :ref:`tls_backends`: the TLS libraries PJSIP can use, and what each
   one supports.
2. :ref:`tls_building`: selecting the backend when building PJSIP.
3. :ref:`tls_configuring`: setting up the SIP TLS transport in the
   application: credentials, protocol versions, verification policy.
4. :ref:`tls_runtime`: custom verification, renegotiation and
   certificate rotation.
5. :ref:`tls_examples` with pjsua, and :ref:`tls_troubleshooting`.


.. _tls_backends:

TLS backends
------------

PJSIP's TLS support is implemented through PJLIB's
:doc:`SSL Socket API </api/generated/pjlib/group/group__PJ__SSL__SOCK>`,
which has one implementation, or *backend*, per TLS library. The
backend is selected at build time by the :c:macro:`PJ_SSL_SOCK_IMP`
macro (see :ref:`tls_building`), with one of these values:

.. list-table::
   :header-rows: 1

   * - Value
     - Code
     - Backend
     - Typical use
   * - :c:macro:`PJ_SSL_SOCK_IMP_OPENSSL`
     - 1
     - :ref:`OpenSSL <tls_backend_openssl>` (or BoringSSL as a drop-in
       replacement)
     - Default; widest support
   * - :c:macro:`PJ_SSL_SOCK_IMP_GNUTLS`
     - 2
     - :ref:`GnuTLS <tls_backend_gnutls>`
     - LGPL-only deployments
   * - :c:macro:`PJ_SSL_SOCK_IMP_DARWIN`
     - 3
     - :ref:`Apple Secure Transport <tls_backend_darwin>` (deprecated)
     - Legacy macOS / iOS
   * - :c:macro:`PJ_SSL_SOCK_IMP_APPLE`
     - 4
     - :ref:`Apple Network framework <tls_backend_apple>`
     - macOS 10.15+ / iOS 13+
   * - :c:macro:`PJ_SSL_SOCK_IMP_SCHANNEL`
     - 5
     - :ref:`Windows SChannel <tls_backend_schannel>`
     - Windows native
   * - :c:macro:`PJ_SSL_SOCK_IMP_MBEDTLS`
     - 6
     - :ref:`Mbed TLS <tls_backend_mbedtls>`
     - Embedded / constrained
   * - :c:macro:`PJ_SSL_SOCK_IMP_NONE`
     - 0
     - :ref:`TLS disabled <tls_backend_none>`
     - Build without TLS

The rest of this page refers to the backends by the names in the
*Backend* column.

.. _tls_backend_openssl:

OpenSSL
~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_OPENSSL` is the default and the most
thoroughly exercised backend. It supports the full PJSIP TLS feature
set, including the handshake-time verification callback (see
:ref:`tls_custom_verification`), credentials given as pre-loaded
OpenSSL objects (``cert_direct``), and the ``curves`` and ``sigalgs``
settings. Several PJSIP features outside the TLS transport also depend
on OpenSSL; see :ref:`tls_openssl_features`.

**BoringSSL** and **LibreSSL** are API-compatible with OpenSSL and work
as link-time substitutes; there is no separate
``PJ_SSL_SOCK_IMP_BORINGSSL``.

OpenSSL trusts only the CA certificates the application supplies; it
does not use a system trust store.

**FIPS:** only OpenSSL in FIPS mode has been exercised. In a strict-FIPS
OpenSSL configuration, MD5 may be unavailable; PJSIP detects this at
run time and falls back to its internal MD5 for digest authentication
(see :ref:`guide_digest_auth`).

.. _tls_backend_gnutls:

GnuTLS
~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_GNUTLS` is an LGPL alternative for projects
whose licensing precludes OpenSSL. It is functionally close to OpenSSL,
with these differences:

- cipher names are mapped internally to GnuTLS priority-string syntax;
- the handshake-time verification callback is not implemented;
- the ``curves`` and ``sigalgs`` settings are not used;
- in addition to the CA certificates the application supplies, GnuTLS
  trusts the system trust store.

Before pjproject 2.17, the GnuTLS backend skipped chain verification
when PJSIP-level verification was disabled; see the warning in
:ref:`tls_post_handshake`.

.. _tls_backend_apple:

Apple Network framework
~~~~~~~~~~~~~~~~~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_APPLE` is the recommended backend on macOS
10.15+ and iOS 13+. It requires the ``select`` I/O queue
(``PJ_IOQUEUE_IMP_SELECT``). ``configure`` never selects it; set it in
:ref:`config_site.h` or use CMake (see :ref:`tls_building`).

Credentials differ from the other backends:

- the certificate comes from ``cert_file`` or ``cert_buf``: a PKCS#12
  bundle on iOS; PKCS#12, PEM or DER on macOS;
- ``privkey_file`` and ``privkey_buf`` are not used: the private key
  must be inside the PKCS#12 bundle (iOS) or in the keychain (macOS);
- a CA in ``ca_list_file`` or ``ca_buf`` must be a single DER
  certificate, and becomes the only trust anchor; without one, the
  system trust store is used. ``ca_list_path`` only serves as the
  directory of ``ca_list_file``;
- ``cert_lookup`` is not consumed.

The handshake-time verification callback and the ``curves`` and
``sigalgs`` settings are not supported.

.. _tls_backend_darwin:

Apple Secure Transport
~~~~~~~~~~~~~~~~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_DARWIN` is the legacy Apple backend. It is
**deprecated** in macOS 10.15 and iOS 13, and has no TLS 1.3: it
rejects a protocol set with TLS 1.3 only. New code should use the
:ref:`tls_backend_apple` backend instead.

Credentials follow the same rules as for the Apple Network framework,
and the same settings are unsupported.

On macOS and iOS targets, ``configure`` selects this backend only if
the SDK does not report it as deprecated, which current SDKs do.

.. _tls_backend_schannel:

Windows SChannel
~~~~~~~~~~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_SCHANNEL` uses the Windows SSPI/SChannel
stack and the Windows certificate store. It is selected in
:ref:`config_site.h` for Visual Studio builds; ``configure`` never
selects it, and the CMake build does not implement it yet.

The only credential source it consumes is ``cert_lookup``:
``cert_file``, ``cert_buf``, ``privkey_*``, ``ca_list_*`` and
``ca_buf`` are ignored, and peers are verified against the Windows
certificate store. A server with no ``cert_lookup``, including one
given only ``cert_file`` or ``cert_buf``, falls back to a self-signed
certificate, with a warning; a server whose ``cert_lookup`` matches
nothing has no certificate.

The ``ciphers`` and ``curves`` settings are ignored, ``sigalgs`` and
the handshake-time verification callback are not supported, and TLS
1.3 is available on recent Windows versions. SChannel requests a
client certificate when asked to, but PJLIB does not itself reject a
client that sends none (see ``require_client_cert`` in
:ref:`tls_verification`).

.. _tls_backend_mbedtls:

Mbed TLS
~~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_MBEDTLS` is a small TLS stack typical for
embedded and resource-constrained targets. Mbed TLS 3.6 and 4.x are
supported, both with TLS 1.3; some distributions still package 2.28
(e.g. Ubuntu 24.04), which is not supported.

The handshake-time verification callback and the ``curves`` and
``sigalgs`` settings are not supported. Mbed TLS has no access to a
system trust store, so it trusts only the CA certificates the
application supplies.

Building Mbed TLS and PJSIP with it, and configuring Mbed TLS for a
small footprint, are covered in :ref:`guide_mbedtls`.

.. _tls_backend_none:

TLS disabled
~~~~~~~~~~~~

:c:macro:`PJ_SSL_SOCK_IMP_NONE` disables TLS entirely. Useful for
builds where signalling goes through a TLS-terminating proxy, or for
footprint-constrained builds.

.. _tls_capabilities:

Capability comparison
~~~~~~~~~~~~~~~~~~~~~

+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Capability                               | OpenSSL  | GnuTLS  | Apple NW  | Apple Darwin | SChannel | Mbed TLS |
+==========================================+==========+=========+===========+==============+==========+==========+
| Certificate from file (``cert_file``)    | yes      | yes     | yes ¹     | yes ¹        | —        | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Certificate from memory (``cert_buf``)   | yes      | yes     | yes ¹     | yes ¹        | —        | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| CA file or buffer (``ca_list_file``,     | yes      | yes     | DER ¹     | DER ¹        | —        | yes      |
| ``ca_buf``)                              |          |         |           |              |          |          |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| CA directory (``ca_list_path``)          | yes      | yes     | —         | —            | —        | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| System trust store                       | —        | yes     | yes ²     | yes ²        | yes      | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| OS-store ``cert_lookup``                 | —        | —       | —         | —            | yes      | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Backend-object ``cert_direct``           | yes      | —       | —         | —            | —        | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Handshake-time verify hook               | yes      | —       | —         | —            | —        | —        |
| (``on_verify_cb``)                       |          |         |           |              |          |          |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| TLS 1.3                                  | yes      | yes     | yes       | —            | yes ³    | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| ``curves`` and ``sigalgs``               | yes      | —       | —         | —            | —        | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Secure SDES-SRTP keys                    | yes      | —       | yes       | —            | —        | yes      |
| (``pj_ssl_rand_bytes()``)                |          |         |           |              |          |          |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+

| ¹ The private key must be in the PKCS#12 bundle or the keychain, and
  the CA must be a single DER certificate; see :ref:`tls_backend_apple`.
| ² Unless a CA is given, which then becomes the only trust anchor.
| ³ On recent Windows versions.

Without a system trust store, a client must be given the CA
certificates to verify servers. Without ``pj_ssl_rand_bytes()``,
PJMEDIA generates SDES-SRTP keys with a weak generator, and logs a
warning.

Renegotiation support also differs per backend; see
:ref:`tls_renegotiation`.

.. note::

   Custom verification is still possible on every backend, with the
   post-handshake inspection described in :ref:`tls_post_handshake`.
   The *Handshake-time verify hook* row only covers the callback that
   runs during the handshake. Before ruling out a non-OpenSSL backend
   for a custom verification policy, read :ref:`tls_custom_verification`.

.. _tls_openssl_features:

Features that require OpenSSL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Beyond the TLS transport itself, a few PJSIP features couple to OpenSSL,
with different rules:

+------------------------------------+-----------------------+----------------------------------+
| Feature                            | Couples to            | How to enable                    |
|                                    | ``PJ_SSL_SOCK_IMP``?  |                                  |
+====================================+=======================+==================================+
| SHA-256 / SHA-512-256 SIP digest   | **Yes**: must be      | Set ``algorithm_type`` on        |
| authentication                     | ``PJ_SSL_SOCK_IMP_    | :cpp:any:`pjsip_cred_info`; see  |
|                                    | OPENSSL``             | :ref:`guide_digest_auth`         |
+------------------------------------+-----------------------+----------------------------------+
| DTLS-SRTP                          | **Yes**: must be      | ``PJMEDIA_SRTP_HAS_DTLS=1`` in   |
|                                    | ``PJ_SSL_SOCK_IMP_    | :ref:`config_site.h` (default    |
|                                    | OPENSSL``             | ``0``)                           |
+------------------------------------+-----------------------+----------------------------------+
| AEAD-GCM SRTP suites               | Not directly: needs   | ``PJMEDIA_SRTP_HAS_AES_GCM_128`` |
| (``AEAD_AES_128_GCM``,             | libsrtp with OpenSSL  | / ``_GCM_256`` in                |
| ``AEAD_AES_256_GCM``)              | crypto (see below)    | :ref:`config_site.h`             |
+------------------------------------+-----------------------+----------------------------------+
| AES-CM-192 SRTP suite              | No: same as           | ``PJMEDIA_SRTP_HAS_AES_CM_192``  |
|                                    | AEAD-GCM              | in :ref:`config_site.h`          |
+------------------------------------+-----------------------+----------------------------------+

**SHA-256 digest authentication** requires ``PJ_SSL_SOCK_IMP =
PJ_SSL_SOCK_IMP_OPENSSL``. The digest algorithms are also checked at
run time, so OpenSSL must provide them (SHA-512-256 needs OpenSSL 1.1.1
or later).

**DTLS-SRTP** has a hard source-level gate in ``transport_srtp.c`` that
force-disables :c:macro:`PJMEDIA_SRTP_HAS_DTLS` whenever
``PJ_SSL_SOCK_IMP != PJ_SSL_SOCK_IMP_OPENSSL``, even though the DTLS
handshake code in ``transport_srtp_dtls.c`` calls OpenSSL APIs directly
rather than going through ``pj_ssl_sock``. Combining DTLS-SRTP with a
non-OpenSSL TLS backend therefore requires a local patch to remove that
gate.

**The AEAD-GCM and AES-CM-192 SRTP suites** are not tied to the TLS
backend in the code; they need libsrtp built with OpenSSL crypto. You
can run e.g. GnuTLS for SIP TLS and still enable these suites by
setting the matching ``PJMEDIA_SRTP_HAS_*`` flag, provided libsrtp has
OpenSSL crypto, which the build systems decide differently:

- with ``configure``, the bundled libsrtp uses OpenSSL crypto only when
  ``configure`` detects OpenSSL, which it does not with
  ``--with-gnutls`` or ``--with-mbedtls``;
- with CMake, the bundled libsrtp uses OpenSSL crypto whenever OpenSSL
  is found and ``SRTP_WITH_OPENSSL`` is ``ON`` (the default), whatever
  ``PJLIB_WITH_SSL`` is;
- an external libsrtp may be built with OpenSSL or NSS crypto.

See :doc:`/specific-guides/security/srtp` for the SRTP-side
configuration.


.. _tls_building:

Building PJSIP with TLS support
-------------------------------

Two macros gate TLS in any PJSIP build:

- :c:macro:`PJ_HAS_SSL_SOCK` turns on TLS support (default ``0``).
- :c:macro:`PJ_SSL_SOCK_IMP` selects the backend (defaults to
  :c:macro:`PJ_SSL_SOCK_IMP_OPENSSL` when ``PJ_HAS_SSL_SOCK = 1``).

:c:macro:`PJSIP_HAS_TLS_TRANSPORT` follows :c:macro:`PJ_HAS_SSL_SOCK`
automatically.

autoconf
~~~~~~~~

.. code-block:: shell

   ./configure                       # auto-detect, OpenSSL first
   ./configure --with-ssl=DIR        # OpenSSL installed in DIR
   ./configure --with-gnutls=DIR     # GnuTLS
   ./configure --with-mbedtls=DIR    # Mbed TLS
   ./configure --disable-ssl         # no TLS

Without an option, ``configure`` looks for OpenSSL, then GnuTLS, then
Mbed TLS, and uses the first one found. On macOS and iOS targets it
first tries :ref:`tls_backend_darwin`, and uses it only if the SDK does
not report it as deprecated, which current SDKs do;
``--disable-darwin-ssl`` skips that check. ``--with-gnutls`` and
``--with-mbedtls`` select that library instead of OpenSSL. When cross
compiling, no TLS library is detected unless one of the ``--with-*``
options is given.

``configure`` never selects :ref:`tls_backend_apple` or
:ref:`tls_backend_schannel`. Set them in :ref:`config_site.h` (the
Apple Network framework also needs ``PJ_IOQUEUE_IMP_SELECT``), or use
CMake for the Apple Network framework.

For Debian/Ubuntu systems, the development headers are typically:

.. code-block:: shell

   sudo apt-get install libssl-dev      # OpenSSL
   sudo apt-get install libgnutls28-dev # GnuTLS
   sudo apt-get install libmbedtls-dev  # Mbed TLS

Check the packaged Mbed TLS version: PJSIP needs 3.6 or later, and some
distributions still ship 2.28 (e.g. Ubuntu 24.04).

See also the platform-specific OpenSSL install pages:

- :any:`windows_openssl` (Windows)
- :any:`ios_openssl` (iOS / iPhone)
- :any:`android_openssl` (Android)

For building Mbed TLS and PJSIP with it, see :ref:`guide_mbedtls`.

CMake
~~~~~

.. code-block:: shell

   cmake -DPJLIB_WITH_SSL=openssl   ...   # default
   cmake -DPJLIB_WITH_SSL=gnutls    ...
   cmake -DPJLIB_WITH_SSL=mbedtls   ...
   cmake -DPJLIB_WITH_SSL=darwin    ...   # Apple Secure Transport (legacy)
   cmake -DPJLIB_WITH_SSL=apple -DPJLIB_WITH_IOQUEUE=select ...
                                          # Apple Network framework
   cmake -DPJLIB_WITH_SSL=          ...   # disable

``schannel`` is accepted as a value but not implemented yet in the
CMake build; use Visual Studio for SChannel. With the default
``openssl``, a build where OpenSSL is not found continues without TLS;
check the CMake output.

Visual Studio and config_site.h
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your build system doesn't auto-detect (e.g. a raw MSVC project), set
both macros explicitly in :ref:`config_site.h`:

.. code-block:: c

   #define PJ_HAS_SSL_SOCK     1
   #define PJ_SSL_SOCK_IMP     PJ_SSL_SOCK_IMP_OPENSSL   /* or another */

Checking the build
~~~~~~~~~~~~~~~~~~

To verify at run time that the build picked the backend you expected,
call :cpp:any:`pj_dump_config()` early in your initialisation. It logs
every notable PJLIB build-time macro at level 3, including the two
TLS-related ones:

.. code-block:: text

    PJ_HAS_SSL_SOCK           : 1
    PJ_SSL_SOCK_IMP           : 1

Match the printed ``PJ_SSL_SOCK_IMP`` value against the codes in the
table in :ref:`tls_backends` (1 = OpenSSL, 2 = GnuTLS, …).


.. _tls_configuring:

Configuring the TLS transport
-----------------------------

Transport setup
~~~~~~~~~~~~~~~

Three layers of API are available:

- **PJSUA-LIB**: configure
  :cpp:any:`pjsua_transport_config::tls_setting` (a
  :cpp:any:`pjsip_tls_setting`) and call
  :cpp:any:`pjsua_transport_create()` with
  :cpp:any:`PJSIP_TRANSPORT_TLS`. See
  :doc:`PJSUA-LIB Transport </api/generated/pjsip/group/group__PJSUA__LIB__TRANSPORT>`.
- **PJSUA2**: configure :cpp:any:`pj::TlsConfig` inside
  :cpp:any:`pj::TransportConfig`, then create the transport via
  :any:`pjsua2_create_transport`.
- **Bare PJSIP**: call :cpp:any:`pjsip_tls_transport_start()` (or
  :cpp:any:`pjsip_tls_transport_start2()`) with a
  :cpp:any:`pjsip_tls_setting`. See
  :doc:`PJSIP TLS Transport </api/generated/pjsip/group/group__PJSIP__TRANSPORT__TLS>`.

The :cpp:any:`pjsip_tls_setting` structure is the central configuration
object. Initialise it with :cpp:any:`pjsip_tls_setting_default()`. The
rest of this section goes through its fields.

.. _tls_credentials:

Credentials
~~~~~~~~~~~

PJSIP supports four ways to supply a TLS credential, through
mutually-exclusive groups of fields on :cpp:any:`pjsip_tls_setting`:

- **Files**: set :cpp:any:`pjsip_tls_setting::ca_list_file`,
  :cpp:any:`pjsip_tls_setting::cert_file` and
  :cpp:any:`pjsip_tls_setting::privkey_file` to PEM (or DER) paths. As
  an alternative to ``ca_list_file``,
  :cpp:any:`pjsip_tls_setting::ca_list_path` accepts a directory of CA
  files (OpenSSL, GnuTLS and Mbed TLS only). Supported on every backend
  except SChannel; the Apple backends have their own format rules (see
  :ref:`tls_backend_apple`).
- **In-memory buffers**: set ``ca_buf``, ``cert_buf`` and
  ``privkey_buf`` instead. Useful when the credential is fetched at run
  time (e.g. from a vault) and must not touch the filesystem. Supported
  on every backend except SChannel.
- **OS certificate-store lookup**: set ``cert_lookup`` (a
  :cpp:any:`pj_ssl_cert_lookup_criteria`) to identify a credential by
  subject, SHA-1 thumbprint, etc. inside the platform's certificate
  store. Consumed only by :ref:`tls_backend_schannel`; the Apple
  backends ignore it and require file or buffer credentials.
- **Backend objects**: set ``cert_direct`` to inject pre-loaded backend
  objects (e.g. an OpenSSL ``X509`` plus ``EVP_PKEY``). OpenSSL only.

If the private key is encrypted, set
:cpp:any:`pjsip_tls_setting::password`. The companion
:cpp:any:`pjsip_tls_setting_wipe_keys()` zero-fills the key fields when
you no longer need them.

Populate exactly one kind of source. The TLS transport loads every
populated field into one credential, and when several are set, the
backend decides which one is used (OpenSSL, for example, prefers the
files, then the buffers, then ``cert_direct``; SChannel uses only
``cert_lookup``). Set only the source that matches the chosen backend;
:ref:`tls_capabilities` has the per-backend summary.

.. _tls_protocols:

Protocol versions, ciphers and curves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :cpp:any:`pjsip_tls_setting::proto` is a bitmask of
  :cpp:any:`pj_ssl_sock_proto` values; combine them with bitwise OR to
  enable several TLS versions (e.g. ``PJ_SSL_SOCK_PROTO_TLS1_2 |
  PJ_SSL_SOCK_PROTO_TLS1_3``). This is the field to use for explicit
  version selection, for example to allow TLS 1.3 only or to drop TLS
  1.0/1.1. The default (``PJSIP_SSL_DEFAULT_PROTO``) is
  ``TLS1 | TLS1_1 | TLS1_2``: **TLS 1.3 is not enabled by default** and
  must be added explicitly, per transport or for the whole application
  by redefining ``PJSIP_SSL_DEFAULT_PROTO`` in :ref:`config_site.h`.
  TLS 1.3 is supported by every backend except
  :ref:`tls_backend_darwin`, which rejects a protocol set with TLS 1.3
  only; on SChannel it depends on the Windows version.
- :cpp:any:`pjsip_tls_setting::method` is a legacy field carrying a
  :cpp:any:`pjsip_ssl_method` value (e.g. ``PJSIP_TLSV1_METHOD``,
  ``PJSIP_TLSV1_2_METHOD``). Its default
  ``PJSIP_SSL_UNSPECIFIED_METHOD`` (0) maps to
  ``PJSIP_SSL_DEFAULT_METHOD``, currently ``PJSIP_TLSV1_METHOD``. It is
  used only when ``proto`` is zero, which it is not by default.
- :cpp:any:`pjsip_tls_setting::ciphers` and ``ciphers_num`` give the
  allowed :cpp:any:`pj_ssl_cipher` IDs. Empty (the default) means the
  backend's default cipher list. Enumerate what is available on the
  running system with :cpp:any:`pj_ssl_cipher_get_availables()`.
  Ignored by SChannel.
- :cpp:any:`pjsip_tls_setting::curves` and ``curves_num`` do the same
  for elliptic curves; enumerate with
  :cpp:any:`pj_ssl_curve_get_availables()`. OpenSSL only.
- :cpp:any:`pjsip_tls_setting::sigalgs` is a colon-separated string of
  signature algorithms in the form
  ``"<DIGEST>+<ALGORITHM>:<DIGEST>+<ALGORITHM>"``, e.g.
  ``"SHA256+RSA:SHA256+ECDSA"``. OpenSSL only.

Cipher and curve identifiers map to backend-specific names internally
(e.g. ``"AES256-SHA"`` in OpenSSL vs the GnuTLS priority-string
syntax), and :cpp:any:`pj_ssl_cipher_get_availables()` returns whatever
the linked backend supports, so the same call gives different results
on an OpenSSL build and on a Mbed TLS build. The available set is what
you compiled in; these settings only constrain it.

.. _tls_hostname:

Hostname matching and SNI
~~~~~~~~~~~~~~~~~~~~~~~~~

When the local end acts as a TLS client, PJSIP sends SNI with, and
matches the peer's certificate (subjectAltName, or CN) against, the
host name of the **next hop**, before DNS SRV/A resolution: the host of
the top ``Route`` header or outbound proxy if there is one, otherwise
the host (or ``maddr``) of the Request-URI. With an outbound proxy, the
certificate must therefore match the proxy's name. PJSIP does this
matching itself, with every backend.

There is no per-transport override field on
:cpp:any:`pjsip_tls_setting`; to reach an SBC at a different host than
the URI's host (e.g. dial by IP but expect a specific certificate
subject or SAN), route the request through a SIP URI whose host matches
the certificate.

.. _tls_verification:

Verification policy
~~~~~~~~~~~~~~~~~~~

Two flags on :cpp:any:`pjsip_tls_setting` control what the transport
does when the peer certificate fails to verify:

- :cpp:any:`pjsip_tls_setting::verify_server`: client-side check of the
  server certificate. Default ``PJ_FALSE``.
- :cpp:any:`pjsip_tls_setting::verify_client`: server-side check of the
  client certificate. Default ``PJ_FALSE``.

The flag primarily controls the *consequence* of a verification
failure:

- ``PJ_FALSE``: the connection completes regardless of the verification
  outcome. The application receives ``PJSIP_TP_STATE_CONNECTED`` via
  the transport-state callback and can inspect the
  :cpp:any:`pjsip_tls_state_info` for the verification result. This is
  "notify only".
- ``PJ_TRUE``: a verification failure shuts the transport down; the
  application receives ``PJSIP_TP_STATE_DISCONNECTED``.

The SIP transport applies both flags itself, after the handshake,
rather than passing them to the SSL socket underneath. On the OpenSSL,
GnuTLS, Apple Network framework and SChannel backends the chain is
verified regardless of the flag, so ``verify_status`` in
:cpp:any:`pjsip_tls_state_info` is populated either way. **On GnuTLS
before pjproject 2.17, chain verification is skipped when the flag is
PJ_FALSE and verify_status comes back empty**; see the warning in
:ref:`tls_post_handshake`.

Which certificates are trusted depends on the backend: OpenSSL and
Mbed TLS trust only the CA certificates you supply, GnuTLS adds the
system trust store, the Apple backends use the system trust store unless
a CA is supplied, and SChannel uses the Windows certificate store (see
:ref:`tls_capabilities`).

A separate flag, :cpp:any:`pjsip_tls_setting::require_client_cert`
(server side, default ``PJ_FALSE``), tells the transport to **reject the
connection** when the client did not present a certificate at all. This
corresponds to OpenSSL's ``SSL_VERIFY_FAIL_IF_NO_PEER_CERT``. SChannel
requests a client certificate, but PJLIB does not itself reject a
client that sends none.

For most production deployments, you want ``verify_server = PJ_TRUE``
on the client side, to prevent man-in-the-middle attacks, and on the
server side either ``verify_client = PJ_TRUE`` plus
``require_client_cert = PJ_TRUE`` (true mutual TLS, see
:ref:`tls_mtls`) or both left ``PJ_FALSE`` if SIP digest
authentication is the actual authentication mechanism.

Policies that the standard verification doesn't cover, such as
certificate pinning, are the subject of :ref:`tls_custom_verification`.

.. _tls_mtls:

Mutual TLS
~~~~~~~~~~

Mutual TLS combines verification on both sides:

- *Client side*: ``verify_server = PJ_TRUE``, plus a CA list
  (``ca_list_file`` or ``ca_buf``) that trusts the server's signing
  chain.
- *Server side*: ``verify_client = PJ_TRUE`` and
  ``require_client_cert = PJ_TRUE``, plus a CA list that trusts the
  client certificate's issuer.

Each side then presents its own ``cert_file`` and ``privkey_file`` (or
the equivalent for the chosen credential source).

Mutual TLS authenticates the **transport peer**, not the SIP user. It
can **replace** SIP digest authentication (the server trusts whoever
holds a valid client certificate) or **complement** it (certificate
plus digest). Choose based on your trust model: digest authenticates
the user identity claimed in ``From``, mutual TLS authenticates the TCP
endpoint. See :ref:`tls_examples` for the pjsua command lines.


.. _tls_runtime:

Operating TLS at runtime
------------------------

.. _tls_custom_verification:

Custom verification
~~~~~~~~~~~~~~~~~~~

For policies that the standard verification doesn't cover (certificate
pinning, additional CRL/OCSP checks, custom subject matching), PJSIP
offers two approaches:

.. list-table::
   :header-rows: 1

   * - Requirement
     - Use
     - Backends
   * - Block the handshake **before** any bytes flow
     - :ref:`tls_handshake_hook`
     - OpenSSL only
   * - Cross-backend custom policy; tolerate the TLS session reaching
       CONNECTED momentarily before being torn down
     - :ref:`tls_post_handshake`
     - All (GnuTLS needs pjproject 2.17 or later)

.. _tls_handshake_hook:

Handshake-time hook
^^^^^^^^^^^^^^^^^^^

Set :cpp:any:`pjsip_tls_setting::on_verify_cb`. The callback receives a
:cpp:any:`pjsip_tls_on_verify_param` and returns a ``pj_bool_t``: a
``PJ_FALSE`` return drops the connection immediately, regardless of
how the standard verification went. The callback fires **regardless**
of ``verify_server`` and ``verify_client``: even when those flags are
``PJ_FALSE``, the hook still runs.

.. warning::

   ``on_verify_cb`` is currently implemented for the OpenSSL backend
   only. On other backends the field is ignored. If your application
   relies on the policy decision happening before the handshake
   completes, pin your build to OpenSSL.

.. _tls_post_handshake:

Post-handshake inspection
^^^^^^^^^^^^^^^^^^^^^^^^^

Disable PJSIP-level verification on the relevant side, let the
handshake complete, and apply your custom policy from the
transport-state callback once
:cpp:any:`PJSIP_TP_STATE_CONNECTED <pjsip_transport_state::PJSIP_TP_STATE_CONNECTED>`
fires. The recipe:

1. Set ``verify_server = PJ_FALSE`` (client) or
   ``verify_client = PJ_FALSE`` (server), so that the handshake doesn't
   tear itself down on verification failure.
2. In your :cpp:any:`pjsua_callback::on_transport_state` (PJSUA-LIB) or
   :cpp:func:`pj::Endpoint::onTransportState()` (PJSUA2) handler, watch
   for ``PJSIP_TP_STATE_CONNECTED`` on a TLS transport.
3. Read the :cpp:any:`pjsip_tls_state_info` from the state info (it
   carries a :cpp:any:`pj_ssl_sock_info` with the chain-trust flags in
   its ``verify_status`` field). Apply your custom policy on top of
   those flags.
4. If the policy fails, shut the transport down with
   :cpp:any:`pjsip_transport_shutdown()`. In-flight requests on that
   transport will fail.

The trade-off versus the handshake-time hook: **the TLS connection
reaches the CONNECTED state on both ends before your policy runs**, and
your shutdown happens after the fact. The peer (and any monitoring or
audit log watching the TLS layer) sees a fully established session,
even if briefly, before you tear it down. For deployments that require
"no completed TLS session with an unverified peer, ever", the
handshake-time hook is the only option. Also:

- Encrypted bytes, including SIP messages, can already be flowing on
  the connection between handshake completion and your
  ``pjsip_transport_shutdown()`` call. Applications that care can also
  drop unauthenticated requests at the SIP layer, but that is extra
  work.
- Tearing the transport down after the fact is more cleanup than
  rejecting in-handshake.
- On the upside, this approach works on **every** PJLIB SSL backend,
  not just OpenSSL.

.. warning::

   On the GnuTLS backend, post-handshake inspection requires pjproject
   **2.17 or later**. Earlier versions had a bug, fixed under security
   advisory `GHSA-x2fv-6j6c-pxmx
   <https://github.com/pjsip/pjproject/security/advisories/GHSA-x2fv-6j6c-pxmx>`__,
   where the GnuTLS backend skipped chain verification entirely when
   ``verify_peer`` was false at the SSL-socket level, which is exactly
   what this approach sets. ``verify_status`` then came back empty, so
   applications relying on it for policy decisions silently accepted
   *every* peer. If you must use GnuTLS this way, upgrade to 2.17+ or
   backport the fix.

Server-side accept failures (TLS handshake errors before the verify
stage) are reported via the companion
:cpp:any:`pjsip_tls_setting::on_accept_fail_cb`; this is informational
only.

.. _tls_renegotiation:

Renegotiation
~~~~~~~~~~~~~

TLS renegotiation lets a connected TLS session re-do the handshake
mid-session, typically to rekey or update the authentication context.
It only exists in **TLS 1.2 and earlier**: TLS 1.3 removed it and
replaced it with the on-the-wire key-update message, which is invisible
to the application. On a TLS 1.3-only deployment, none of the controls
below have any effect.

**Accepting incoming renegotiation requests** is controlled by
:cpp:any:`pjsip_tls_setting::enable_renegotiation` (default
``PJ_TRUE``). Setting it to ``PJ_FALSE`` is a defence against
renegotiation-flood denial-of-service attacks (and similar abuse) at
the cost of forfeiting any rekey before the session ends; it is worth
doing on a public-facing TLS endpoint whose peers don't need to
renegotiate. Only OpenSSL and the Apple Network framework honour the
flag, though; see the table below.

**Triggering a renegotiation** is not exposed by the SIP TLS transport
at all: neither :cpp:any:`pjsip_tls_setting` nor the PJSUA-LIB and
PJSUA2 transport APIs offer a way to initiate one. At the lower PJLIB
SSL-socket level there is :cpp:any:`pj_ssl_sock_renegotiate()`,
operating on a raw ``pj_ssl_sock_t``, so it can only be called from
code that works directly against PJLIB sockets.

.. list-table::
   :header-rows: 1

   * - Backend
     - ``enable_renegotiation``
     - ``pj_ssl_sock_renegotiate()``
   * - :ref:`tls_backend_openssl`
     - honoured
     - works, with ``SSL_renegotiate()`` (TLS 1.2 and earlier)
   * - :ref:`tls_backend_gnutls`
     - ignored: always accepts
     - server side only. As a client, returns ``PJ_ENOTSUP``:
       ``gnutls_rehandshake()`` only sends the server's HelloRequest
   * - :ref:`tls_backend_apple`
     - honoured
     - returns ``PJ_ENOTSUP``: the Network framework API has no way to
       trigger renegotiation
   * - :ref:`tls_backend_darwin`
     - ignored: always accepts
     - works, with ``SSLReHandshake()``
   * - :ref:`tls_backend_schannel`
     - ignored: always accepts
     - works: restarts the handshake on the existing context
   * - :ref:`tls_backend_mbedtls`
     - ignored: always refuses
     - returns ``PJ_SUCCESS`` but does nothing: no re-handshake is
       triggered and the connection's keys are not refreshed

.. _tls_listener_restart:

Listener restart and certificate rotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updating TLS certificates without restarting the whole library is done
by restarting the **listener** with a fresh
:cpp:any:`pjsip_tls_setting`:

- **PJSUA-LIB**: :cpp:any:`pjsua_transport_lis_restart()` (added in
  2.16, :pr:`4631`) takes a transport ID and a new
  :cpp:any:`pjsua_transport_config`. The listener socket is closed, the
  new ``tls_setting`` is applied, and the listener is recreated on the
  same address and port.
- **Bare PJSIP**: :cpp:any:`pjsip_tls_transport_restart2()` is the
  TLS-specific equivalent that takes a new ``pjsip_tls_setting``;
  :cpp:any:`pjsip_udp_transport_restart2()` is the UDP variant.
- **PJSUA2** has no equivalent yet.

These restart the **listener**; existing connections are not torn down
by the restart itself. Plan rotation around your application's
reconnection cadence: rotate the certificate, then let connections
refresh on the next register or renegotiate event.

A typical rotation flow with PJSUA-LIB:

.. code-block:: c

   pjsua_transport_config cfg;

   pjsua_transport_config_default(&cfg);
   cfg.port = 5061;
   cfg.tls_setting.ca_list_file  = pj_str("ca.pem");
   cfg.tls_setting.cert_file     = pj_str("server-NEW.pem");
   cfg.tls_setting.privkey_file  = pj_str("privkey-NEW.pem");
   cfg.tls_setting.verify_server = PJ_TRUE;
   /* ...other tls_setting fields you previously used... */

   pjsua_transport_lis_restart(tls_transport_id, &cfg);


.. _tls_examples:

Examples with pjsua
-------------------

Running pjsua as a TLS server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Provide a server certificate as three PEM files: a CA / root
   certificate, the server certificate, and the server private key.

2. Run pjsua with ``--use-tls`` plus the certificate paths:

   .. code-block:: shell

      ./pjsua \
          --use-tls \
          --tls-ca-file root.pem \
          --tls-cert-file server-cert.pem \
          --tls-privkey-file privkey.pem

3. ``./pjsua --help`` lists all TLS-related options, including
   ``--tls-password``, ``--tls-neg-timeout`` and ``--tls-cipher``.

Running pjsua as a TLS client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To call a SIP server over TLS:

.. code-block:: shell

   ./pjsua --use-tls "<sip:SERVER;transport=tls>"

Mutual TLS with pjsua
~~~~~~~~~~~~~~~~~~~~~

Add the corresponding verify flag on each side (see :ref:`tls_mtls`):

.. code-block:: shell

   # Server: require and verify the client cert
   ./pjsua \
       --use-tls --tls-verify-client \
       --tls-ca-file ca.pem \
       --tls-cert-file server-cert.pem \
       --tls-privkey-file privkey.pem

   # Client: present a cert and verify the server's
   ./pjsua \
       --use-tls --tls-verify-server \
       --tls-ca-file ca.pem \
       --tls-cert-file client-cert.pem \
       --tls-privkey-file client-privkey.pem


.. _tls_troubleshooting:

Troubleshooting
---------------

**"verification failed: certificate expired / not trusted".**
Inspect the per-connection :cpp:any:`pjsip_tls_state_info` from the
transport-state callback for the OpenSSL-style error code. Common
causes: clock skew, missing intermediate certificates, wrong CA in
``ca_list_file``, or no CA at all with a backend that has no system
trust store (OpenSSL, Mbed TLS; see :ref:`tls_capabilities`).

**"name mismatch".**
The server certificate's CN or SAN doesn't match the next-hop host (the
outbound proxy or ``Route`` host if there is one, otherwise the
Request-URI host). Either fix the certificate, or route the request
through a URI whose host matches the certificate; there is no
per-transport override (see :ref:`tls_hostname`).

**Cipher or signature-algorithm mismatch.**
The two ends share no common cipher or signature algorithm. Enumerate
what your build offers with :cpp:any:`pj_ssl_cipher_get_availables()`
and :cpp:any:`pj_ssl_curve_get_availables()`. Backend defaults vary;
setting ``ciphers``, ``curves`` and ``sigalgs`` makes the policy
explicit (see :ref:`tls_protocols`).

**TLS version mismatch.**
Older peers may insist on TLS 1.0/1.1, which modern backends often
disable by default. Set ``proto`` explicitly to enable older versions,
only when you must.

**OpenSSL FIPS-mode MD5 failures.**
Strict-FIPS OpenSSL builds disable MD5; PJSIP detects this and falls
back to its internal MD5 for digest authentication. TLS does not use
MD5 in modern cipher suites; if a TLS handshake fails under FIPS, it is
usually because of a legacy-only cipher choice. Relax the cipher list.

**SChannel: certificate-store ACL.**
On Windows, the user that PJSIP runs as needs read access to the
private key in the certificate store. Use ``certutil -repairstore`` or
the Certificates MMC to grant access.

**SChannel server presents a self-signed certificate.**
``cert_lookup`` was not set; ``cert_file`` and ``cert_buf`` are
ignored by SChannel (see :ref:`tls_backend_schannel`).

**Mbed TLS: "Unsupported TLS protocol".**
The protocol set asks only for versions the Mbed TLS build lacks, e.g.
TLS 1.3 alone from a TLS 1.2-only configuration. Add a version the
build has to ``proto``, or rebuild Mbed TLS with it. More in
:ref:`guide_mbedtls`.

**Apple Secure Transport deprecation warnings.**
On macOS 10.15+ and iOS 13+, use :ref:`tls_backend_apple` instead.


See also
--------

- :ref:`guide_mbedtls`: building Mbed TLS and PJSIP with it, and
  configuring Mbed TLS for a small footprint.
- :ref:`guide_digest_auth`: what TLS protects vs what SIP digest
  authentication protects, and the shared OpenSSL dependency.
- :doc:`/specific-guides/security/srtp`: media-layer security.
- :any:`/specific-guides/sip/async_auth`: token-based or user-prompted
  authentication flows that complement TLS.

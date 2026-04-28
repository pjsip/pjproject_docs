.. _guide_ssl:

SSL/TLS
=========================================

.. contents:: Table of Contents
    :depth: 2


Overview
--------

PJSIP uses TLS to secure the **SIP signalling transport** — i.e. SIP
messages on port 5061 (the standard) or any other TLS-listening port,
selected when the SIP URI carries ``;transport=tls`` or uses the
``sips:`` scheme.

Media-layer security (SRTP/SDES, DTLS-SRTP) is a separate mechanism;
see :doc:`/specific-guides/security/srtp`.

Application-layer authentication (SIP digest with MD5 / SHA-256 /
SHA-512-256 / AKA) is also separate; see :ref:`guide_digest_auth`.

Enabling TLS in a PJSIP build is a three-phase task:

1. **Build-time decisions** — pick a TLS backend, configure the build.
2. **Configure** the SIP TLS transport in the application (certificates,
   ciphers, verification policy, hostname matching).
3. **Operate** at runtime — verification callbacks, mutual TLS, listener
   restart for certificate rotation.

The rest of this page is organized along those three phases, followed
by ready-to-run pjsua examples and a troubleshooting checklist.


Build-time decisions
--------------------

Choosing a backend
~~~~~~~~~~~~~~~~~~

PJSIP's TLS support is implemented through PJLIB's
:doc:`SSL Socket API </api/generated/pjlib/group/group__PJ__SSL__SOCK>`.
The backend is selected at build time via the
:c:macro:`PJ_SSL_SOCK_IMP` macro, with one of these values:

+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``PJ_SSL_SOCK_IMP_*``                  | Code | Backend                                          | Typical use              |
+========================================+======+==================================================+==========================+
| ``OPENSSL``                            | 1    | OpenSSL (or BoringSSL as a drop-in replacement)  | Default; widest support  |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``GNUTLS``                             | 2    | GnuTLS                                           | LGPL-only deployments    |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``DARWIN``                             | 3    | Apple Secure Transport (deprecated)              | Legacy macOS / iOS       |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``APPLE``                              | 4    | Apple Network framework                          | macOS 10.15+ / iOS 13+   |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``SCHANNEL``                           | 5    | Windows SChannel SSP                             | Windows native           |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``MBEDTLS``                            | 6    | Mbed TLS                                         | Embedded / constrained   |
+----------------------------------------+------+--------------------------------------------------+--------------------------+
| ``NONE``                               | 0    | TLS disabled                                     | Build without TLS        |
+----------------------------------------+------+--------------------------------------------------+--------------------------+

A short profile of each, with the trade-offs that usually drive the
choice:

- **OpenSSL** is the default and the most thoroughly exercised backend.
  It supports the full PJSIP TLS feature set, including handshake-time
  custom verification callbacks (see below) and direct backend-object
  credential loading. **BoringSSL** is API-compatible with OpenSSL and
  works as a link-time substitute — there is no separate
  ``PJ_SSL_SOCK_IMP_BORINGSSL``. Several PJSIP features outside the
  TLS transport itself also depend on OpenSSL — see the *Features
  that require OpenSSL* note below the capability table.
- **GnuTLS** is an LGPL alternative for projects whose licensing
  precludes OpenSSL. Functionally close to OpenSSL but cipher-suite
  syntax differs and the custom-verify callback is not implemented.
- **Apple Network framework** is the recommended Apple-side backend
  on macOS 10.15+ and iOS 13+. Certificate material is supplied as
  PEM/DER via ``cert_file`` / ``cert_buf`` (and the matching
  ``ca_list_*`` / ``privkey_*`` fields); ``cert_lookup`` is not
  currently consumed by this backend.
- **Apple Secure Transport** (``DARWIN``) is the legacy Apple backend.
  It is **deprecated** in macOS 10.15 and iOS 13; new code should use
  the Network framework backend (``APPLE``) above. Like Apple NW it
  consumes file/buffer credentials, not ``cert_lookup``.
- **Windows SChannel** uses the OS SSPI/SChannel stack and the
  Windows certificate store. The only credential source it consumes
  is ``cert_lookup`` — ``cert_file`` / ``cert_buf`` are silently
  ignored, and a server with no matching store entry falls back to a
  self-signed certificate.
- **Mbed TLS** is a small TLS stack typical for embedded and
  resource-constrained targets. The feature set is a subset (e.g.
  TLS 1.3 support depends on the Mbed TLS version) and the custom
  verify callback is not exposed.
- **NONE** disables TLS entirely. Useful for builds where signalling
  goes through a TLS-terminating proxy or for footprint-constrained
  builds.

Capability differences worth noting:

+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Capability                               | OpenSSL  | GnuTLS  | Apple NW  | Apple Darwin | SChannel | Mbed TLS |
+==========================================+==========+=========+===========+==============+==========+==========+
| File-based PEM/DER certs                 | yes      | yes     | yes       | yes          | —        | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| In-memory ``cert_buf`` / ``ca_list_buf`` | yes      | yes     | yes       | yes          | —        | yes      |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| OS-store ``cert_lookup``                 | —        | —       | —         | —            | yes      | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Backend-object ``cert_direct``           | yes      | —       | —         | —            | —        | —        |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+
| Handshake-time verify hook               | yes      | —       | —         | —            | —        | —        |
| (``on_verify_cb``)                       |          |         |           |              |          |          |
+------------------------------------------+----------+---------+-----------+--------------+----------+----------+

.. note::

   *Custom verification* is still possible on every backend via the
   post-handshake inspection pattern (Pattern B in *Operating TLS at
   runtime* below). The capability row above only covers the
   handshake-time hook; readers chasing custom verification on a
   non-OpenSSL backend should read that section before deciding the
   backend can't fit.

Features that require OpenSSL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beyond the TLS transport itself, a few PJSIP features couple to
OpenSSL with different rules. The matrix:

+------------------------------------+-----------------------+----------------------------------+
| Feature                            | Couples to            | How to enable                    |
|                                    | ``PJ_SSL_SOCK_IMP``?  |                                  |
+====================================+=======================+==================================+
| SHA-256 / SHA-512-256 SIP digest   | **Yes** — must be     | Set ``algorithm_type`` on        |
| authentication                     | ``PJ_SSL_SOCK_IMP_    | :cpp:any:`pjsip_cred_info`; see  |
|                                    | OPENSSL``             | :ref:`guide_digest_auth`         |
+------------------------------------+-----------------------+----------------------------------+
| DTLS-SRTP                          | **Yes** — must be     | ``PJMEDIA_SRTP_HAS_DTLS=1`` in   |
|                                    | ``PJ_SSL_SOCK_IMP_    | :ref:`config_site.h`             |
|                                    | OPENSSL``             |                                  |
+------------------------------------+-----------------------+----------------------------------+
| AEAD-GCM SRTP suites               | No — needs libsrtp    | ``PJMEDIA_SRTP_HAS_AES_GCM_128`` |
| (``AEAD_AES_128_GCM``,             | built with OpenSSL    | / ``_GCM_256`` in                |
| ``AEAD_AES_256_GCM``)              | (or NSS), independent | :ref:`config_site.h`             |
|                                    | of TLS backend        |                                  |
+------------------------------------+-----------------------+----------------------------------+
| AES-CM-192 SRTP suite              | No — same as          | ``PJMEDIA_SRTP_HAS_AES_CM_192``  |
|                                    | AEAD-GCM              | in :ref:`config_site.h`          |
+------------------------------------+-----------------------+----------------------------------+

In short: digest SHA-256 and DTLS-SRTP require ``PJ_SSL_SOCK_IMP =
PJ_SSL_SOCK_IMP_OPENSSL``; the AEAD/GCM and AES-CM-192 SRTP suites
work with any TLS backend as long as libsrtp itself is built against
OpenSSL or NSS. The reasoning and a workaround for combining DTLS-SRTP
with a non-OpenSSL TLS backend are in *Build-time security
considerations* below.

Building with TLS support
~~~~~~~~~~~~~~~~~~~~~~~~~

Two macros gate TLS in any PJSIP build:

- :c:macro:`PJ_HAS_SSL_SOCK` — turns on TLS support (default ``0``).
- :c:macro:`PJ_SSL_SOCK_IMP` — selects the backend (defaults to
  :c:macro:`PJ_SSL_SOCK_IMP_OPENSSL` when ``PJ_HAS_SSL_SOCK = 1``).

:c:macro:`PJSIP_HAS_TLS_TRANSPORT` follows :c:macro:`PJ_HAS_SSL_SOCK`
automatically.

**autoconf**

.. code-block:: shell

   ./configure --with-ssl=DIR        # OpenSSL (default)
   ./configure --with-gnutls=DIR     # GnuTLS
   ./configure --with-mbedtls=DIR    # Mbed TLS

OpenSSL detection runs by default. ``--with-gnutls`` disables OpenSSL
detection and selects GnuTLS instead. SChannel and the Apple backends
are auto-selected on their respective platforms.

For Debian/Ubuntu systems, the development headers are typically:

.. code-block:: shell

   sudo apt-get install libssl-dev      # OpenSSL
   sudo apt-get install libgnutls28-dev # GnuTLS
   sudo apt-get install libmbedtls-dev  # Mbed TLS

See also the platform-specific OpenSSL install pages:

- :any:`windows_openssl` (Windows)
- :any:`ios_openssl` (iOS / iPhone)
- :any:`android_openssl` (Android)

**CMake**

.. code-block:: shell

   cmake -DPJLIB_WITH_SSL=openssl   ...   # default
   cmake -DPJLIB_WITH_SSL=gnutls    ...
   cmake -DPJLIB_WITH_SSL=mbedtls   ...
   cmake -DPJLIB_WITH_SSL=darwin    ...   # Apple Secure Transport (legacy)
   cmake -DPJLIB_WITH_SSL=apple     ...   # Apple Network framework
   cmake -DPJLIB_WITH_SSL=schannel  ...
   cmake -DPJLIB_WITH_SSL=          ...   # disable

**Visual Studio / config_site.h**

If your build system doesn't auto-detect (e.g. raw MSVC project), set
both macros explicitly in :ref:`config_site.h`:

.. code-block:: c

   #define PJ_HAS_SSL_SOCK     1
   #define PJ_SSL_SOCK_IMP     PJ_SSL_SOCK_IMP_OPENSSL   /* or another */

To verify at runtime that the build picked the backend you expected,
call :cpp:any:`pj_dump_config()` early in your initialisation. It
logs every notable PJLIB build-time macro at level 3, including the
two TLS-related ones:

.. code-block:: text

    PJ_HAS_SSL_SOCK           : 1
    PJ_SSL_SOCK_IMP           : 1

Match the printed ``PJ_SSL_SOCK_IMP`` value against the codes in the
backend table above (1 = OpenSSL, 2 = GnuTLS, …).

Build-time security considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **OpenSSL-coupled features** — see the matrix in *Features that
  require OpenSSL* above. The two notable cases are:

  - **AEAD-GCM and AES-CM-192 SRTP suites** are *not* coupled to
    :c:macro:`PJ_SSL_SOCK_IMP`; they only require libsrtp to be
    built with OpenSSL (or NSS). You can run e.g.
    ``PJ_SSL_SOCK_IMP_GNUTLS`` for SIP TLS and still enable these
    SRTP suites by flipping the matching ``PJMEDIA_SRTP_HAS_*`` flag.
  - **DTLS-SRTP** has a hard source-level gate in
    ``transport_srtp.c`` that force-disables
    :c:macro:`PJMEDIA_SRTP_HAS_DTLS` whenever ``PJ_SSL_SOCK_IMP !=
    PJ_SSL_SOCK_IMP_OPENSSL`` — even though the DTLS handshake code
    in ``transport_srtp_dtls.c`` calls OpenSSL APIs directly rather
    than going through ``pj_ssl_sock``. Combining DTLS-SRTP with a
    non-OpenSSL TLS backend therefore requires a local patch to
    remove that gate.

  See :doc:`/specific-guides/security/srtp` for the SRTP-side
  configuration.
- **FIPS** — only OpenSSL backends in FIPS mode have been exercised.
  In a strict-FIPS OpenSSL configuration, MD5 may be unavailable;
  PJSIP detects this at runtime and falls back to its internal MD5
  for digest authentication (see :ref:`guide_digest_auth`).
- **TLS 1.3** is supported in OpenSSL, GnuTLS, Mbed TLS (recent
  versions), the Apple Network framework, and SChannel on recent
  Windows. The legacy Apple Secure Transport (``DARWIN``) does not.
- **Cipher / curve / signature-algorithm policy** — the *available* set
  comes from the backend; PJSIP lets you constrain it at runtime
  (see *Configuring TLS in your application* below). The available
  set itself is what you compiled in.


Configuring TLS in your application
-----------------------------------

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
object. Initialise it with :cpp:any:`pjsip_tls_setting_default()`.

Certificate sources
~~~~~~~~~~~~~~~~~~~

PJSIP supports four ways to supply a TLS credential, enabled by
mutually-exclusive fields on :cpp:any:`pjsip_tls_setting`:

- **File-based** — set
  :cpp:any:`pjsip_tls_setting::ca_list_file`,
  :cpp:any:`pjsip_tls_setting::cert_file`, and
  :cpp:any:`pjsip_tls_setting::privkey_file` to PEM (or DER) paths.
  Supported on every backend except SChannel.
- **In-memory buffer** — set ``ca_list_buf``, ``cert_buf``,
  ``privkey_buf`` instead. Useful when the credential is fetched at
  runtime (e.g. from a vault) and you don't want it touching the
  filesystem. Supported on every backend except SChannel.
- **OS certificate-store lookup** — set ``cert_lookup`` (a
  :cpp:any:`pj_ssl_cert_lookup_criteria`) to identify a credential by
  subject / SHA-1 thumbprint / etc. inside the platform's cert store.
  Currently consumed only by the **Windows SChannel** backend; the
  Apple backends ignore ``cert_lookup`` and require file or buffer
  credentials.
- **Backend-direct objects** — set ``cert_direct`` to inject
  pre-loaded backend objects (e.g. an OpenSSL ``X509`` plus
  ``EVP_PKEY``). **OpenSSL only**.

If the private key is encrypted, set
:cpp:any:`pjsip_tls_setting::password`. The companion
:cpp:any:`pjsip_tls_setting_wipe_keys()` zero-fills the key fields when
you no longer need them.

On OpenSSL, where the same context can accept multiple source kinds,
file-based fields take precedence over in-memory buffers, which take
precedence over ``cert_direct``. On every other backend each source
kind is consumed in isolation, so this ordering does not apply —
populate only the source the backend actually supports.

TLS protocol versions and primitives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :cpp:any:`pjsip_tls_setting::method` — legacy field carrying a
  :cpp:any:`pjsip_ssl_method` value (e.g. ``PJSIP_TLSV1_METHOD``,
  ``PJSIP_TLSV1_2_METHOD``). Default
  ``PJSIP_SSL_UNSPECIFIED_METHOD`` (0) maps to
  ``PJSIP_SSL_DEFAULT_METHOD``, currently
  ``PJSIP_TLSV1_METHOD``. Used only when ``proto`` is zero.
- :cpp:any:`pjsip_tls_setting::proto` — bitmask of
  :cpp:any:`pj_ssl_sock_proto` values; combine with bitwise OR to
  enable multiple TLS versions (e.g. ``PJ_SSL_SOCK_PROTO_TLS1_2 |
  PJ_SSL_SOCK_PROTO_TLS1_3``). Prefer this over ``method`` when you
  need explicit version selection — for example, to force TLS 1.3
  only or to drop TLS 1.0/1.1.
- :cpp:any:`pjsip_tls_setting::ciphers` and ``ciphers_num`` — array of
  allowed :cpp:any:`pj_ssl_cipher` IDs. Empty (default) means "use the
  backend's default cipher list". Enumerate what's actually available
  on the running system with :cpp:any:`pj_ssl_cipher_get_availables()`.
- :cpp:any:`pjsip_tls_setting::curves` and ``curves_num`` — same
  pattern for elliptic curves; enumerate with
  :cpp:any:`pj_ssl_curve_get_availables()`.
- :cpp:any:`pjsip_tls_setting::sigalgs` — colon-separated string of
  signature algorithms in the form
  ``"<DIGEST>+<ALGORITHM>:<DIGEST>+<ALGORITHM>"``, e.g.
  ``"SHA256+RSA:SHA256+ECDSA"``.

Cipher and curve identifiers map to backend-specific names internally
(e.g. ``"SSL_RSA_WITH_AES_256_CBC_SHA"`` in OpenSSL vs the GnuTLS
priority-string syntax). The
:cpp:any:`pj_ssl_cipher_get_availables()` enumerator returns whatever
the linked backend supports — so the same call gives different
results on an OpenSSL build vs a Mbed TLS build.

Hostname matching and SNI
~~~~~~~~~~~~~~~~~~~~~~~~~

When the local end acts as a TLS client, the peer's certificate is
matched against the **server name** in the URI by default. PJSIP
sends SNI based on the same name. If you need to override (e.g.
connecting to an SBC by IP but expecting a specific cert subject /
SAN), set :cpp:any:`pjsip_tls_setting::server_name`.


Operating TLS at runtime
------------------------

Verification policy
~~~~~~~~~~~~~~~~~~~

Two flags on :cpp:any:`pjsip_tls_setting` control what the transport
does when the peer certificate fails to verify:

- :cpp:any:`pjsip_tls_setting::verify_server` — client-side check of
  the server certificate. Default ``PJ_FALSE``.
- :cpp:any:`pjsip_tls_setting::verify_client` — server-side check of
  the client certificate. Default ``PJ_FALSE``.

The flag primarily controls the *consequence* of a verification
failure:

- ``PJ_FALSE`` — the connection completes regardless of verification
  outcome. The application receives ``PJSIP_TP_STATE_CONNECTED`` via
  the transport-state callback and can inspect the
  :cpp:any:`pjsip_tls_state_info` for the verification result. This
  is "notify only".
- ``PJ_TRUE`` — verification failure causes the transport to be shut
  down; the application receives ``PJSIP_TP_STATE_DISCONNECTED``.

On the OpenSSL, Apple, SChannel, and Mbed TLS backends the chain is
verified regardless of the flag, so :cpp:any:`pjsip_tls_state_info`'s
``verify_status`` is populated either way. **On GnuTLS prior to
pjproject 2.17, chain verification is skipped when the flag is
``PJ_FALSE`` and ``verify_status`` comes back empty** — see the
Pattern B warning below for context.

A separate flag :cpp:any:`pjsip_tls_setting::require_client_cert`
(server-side, default ``PJ_FALSE``) tells the transport to **reject
the connection** when the client did not present a certificate at
all. This corresponds to OpenSSL's ``SSL_VERIFY_FAIL_IF_NO_PEER_CERT``.

For most production deployments, you want
``verify_server = PJ_TRUE`` on the client side to prevent
man-in-the-middle, and either ``verify_client = PJ_TRUE`` plus
``require_client_cert = PJ_TRUE`` on the server side (true mTLS) or
both left ``PJ_FALSE`` if SIP digest auth is the actual auth
mechanism.

Custom verification
~~~~~~~~~~~~~~~~~~~

For policies that the standard verification doesn't cover (certificate
pinning, additional CRL/OCSP checks, custom subject matching), PJSIP
offers two patterns. Pick one based on these questions:

+------------------------------------------+-------------+-------------------+
| Requirement                              | Use         | Backends          |
+==========================================+=============+===================+
| Block the handshake **before** any       | Pattern A   | OpenSSL only      |
| bytes flow                               |             |                   |
+------------------------------------------+-------------+-------------------+
| Cross-backend custom policy; tolerate    | Pattern B   | All (GnuTLS       |
| the TLS session reaching CONNECTED       |             | needs ≥ 2.17)     |
| momentarily before being torn down       |             |                   |
+------------------------------------------+-------------+-------------------+

Pattern A — handshake-time hook (OpenSSL only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set :cpp:any:`pjsip_tls_setting::on_verify_cb`. The callback receives
a :cpp:any:`pjsip_tls_on_verify_param` and returns a ``pj_bool_t``: a
``PJ_FALSE`` return causes the connection to be dropped immediately,
regardless of how the standard verification went. The callback fires
**regardless** of ``verify_server`` / ``verify_client`` — even when
those flags are ``PJ_FALSE``, your custom hook still runs.

.. warning::

   ``on_verify_cb`` is currently implemented for the OpenSSL backend
   only. On other backends the field is ignored. If your application
   relies on the policy decision happening before the handshake
   completes, pin your build to OpenSSL.

Pattern B — post-handshake inspection (all backends)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Disable PJSIP-level verification on the relevant side, let the
handshake complete, and apply your custom policy from the
transport-state callback once
:cpp:any:`PJSIP_TP_STATE_CONNECTED <pjsip_transport_state::PJSIP_TP_STATE_CONNECTED>`
fires. The recipe:

1. Set ``verify_server = PJ_FALSE`` (client) or ``verify_client =
   PJ_FALSE`` (server) so the handshake doesn't tear itself down on
   verification failure.
2. In your :cpp:any:`pjsua_callback::on_transport_state` (PJSUA-LIB)
   or :cpp:func:`pj::Endpoint::onTransportState()` (PJSUA2)
   handler, watch for ``PJSIP_TP_STATE_CONNECTED`` on a TLS
   transport.
3. Read the :cpp:any:`pjsip_tls_state_info` from the state info
   (it carries a :cpp:any:`pj_ssl_sock_info` with the chain-trust
   flags in its ``verify_status`` field). Apply your custom policy
   on top of those flags.
4. If the policy fails, shut the transport down with
   :cpp:any:`pjsip_transport_shutdown()`. Existing in-flight requests
   on that transport will fail.

The big trade-off versus Pattern A: **the TLS connection reaches the
CONNECTED state on both ends before your policy runs**, and your
shutdown happens after the fact. The peer (and any monitoring or
audit log watching the TLS layer) sees a fully-established session,
even if briefly, before you tear it down. For deployments that
require "no completed TLS session with an unverified peer, ever",
Pattern A is the only option.

Other considerations versus Pattern A:

- Encrypted bytes — including SIP messages — can already be flowing
  on the connection between handshake completion and your
  ``pjsip_transport_shutdown()`` call. Apps that care can also drop
  unauthenticated requests at the SIP layer, but that's extra work.
- Tearing the transport down after the fact is more cleanup than
  rejecting in-handshake.
- On the upside, this pattern works on **every** PJLIB SSL backend,
  not just OpenSSL.

.. warning::

   On the GnuTLS backend, Pattern B requires pjproject **2.17 or
   later**. Earlier versions had a bug — fixed under security
   advisory `GHSA-x2fv-6j6c-pxmx
   <https://github.com/pjsip/pjproject/security/advisories/GHSA-x2fv-6j6c-pxmx>`__
   — where the GnuTLS backend skipped chain verification entirely
   when ``verify_peer`` was false at the SSL-socket level (which is
   exactly what Pattern B sets). The result was that
   ``verify_status`` came back empty, so applications relying on it
   for policy decisions silently accepted *every* peer. If you must
   use GnuTLS with Pattern B, upgrade to 2.17+ or backport the fix.

Server-side accept failures (TLS handshake errors before the verify
stage) are reported via the companion
:cpp:any:`pjsip_tls_setting::on_accept_fail_cb`; this is informational
only.

Mutual TLS
~~~~~~~~~~

Mutual TLS combines verification on both sides:

- *Client side*: ``verify_server = PJ_TRUE``, plus a CA list
  (``ca_list_file`` or ``ca_list_buf``) that trusts the server's
  signing chain.
- *Server side*: ``verify_client = PJ_TRUE``, ``require_client_cert =
  PJ_TRUE``, plus a CA list that trusts the client certificate's
  issuer.

Each side then presents its own ``cert_file``/``privkey_file`` (or
equivalent for the chosen credential source).

mTLS authenticates the **transport peer**, not the SIP user. It can
**replace** SIP digest authentication (the server trusts whoever
holds a valid client cert) or **complement** it (cert + digest
together). Choose based on your trust model — digest authenticates
the user identity claimed in ``From``, mTLS authenticates the TCP
endpoint.

Renegotiation
~~~~~~~~~~~~~

TLS renegotiation is the mechanism that lets a connected TLS session
re-do the handshake mid-session — typically to rekey or update the
authentication context. It only exists in **TLS 1.2 and earlier**.
TLS 1.3 removed it entirely and replaced it with the on-the-wire
key-update message, which is invisible to the application; on a
TLS-1.3-only deployment, none of the controls below have any effect.

There are two distinct sides to renegotiation:

**Accepting incoming renegotiation requests** is controlled by
:cpp:any:`pjsip_tls_setting::enable_renegotiation` (default
``PJ_TRUE``). The default is appropriate for most applications.
Setting it to ``PJ_FALSE`` is a defence against renegotiation-flood
denial-of-service attacks (and similar abuse patterns) at the cost
of forfeiting any rekey before the session ends; it's worth doing if
you're running a public-facing TLS endpoint and your peers don't
genuinely need to renegotiate.

**Triggering a renegotiation** is not exposed by the SIP TLS
transport at all — neither :cpp:any:`pjsip_tls_setting` nor the
PJSUA-LIB / PJSUA2 transport APIs offer a way to initiate one. At
the lower PJLIB SSL-socket level there is
:cpp:any:`pj_ssl_sock_renegotiate()` operating on a raw
``pj_ssl_sock_t``, so the only place this can be called from is code
that works directly against PJLIB sockets.

Even at PJLIB level, two backends fall short of doing a real
re-handshake:

- The **Apple Network framework** backend (the modern macOS 10.15+ /
  iOS 13+ ``APPLE`` backend) returns ``PJ_ENOTSUP`` — the underlying
  Network framework API doesn't expose a way to trigger renegotiation
  manually. The legacy Apple **Secure Transport** (``DARWIN``)
  backend, by contrast, does implement it via ``SSLReHandshake()``.
- **Mbed TLS** currently returns ``PJ_SUCCESS`` but the call is a
  silent no-op — no re-handshake is actually triggered, so the
  function appears to succeed while the connection's keys are not
  refreshed.

Listener restart and certificate rotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updating TLS certificates without restarting the whole library is
done by restarting the **listener** with a fresh
:cpp:any:`pjsip_tls_setting`:

- **PJSUA-LIB**: :cpp:any:`pjsua_transport_lis_restart()` (added in
  2.17, :pr:`4631`) takes a transport ID and a new
  :cpp:any:`pjsua_transport_config`. The listener socket is closed,
  the new ``tls_setting`` is applied, and the listener is recreated
  on the same address/port.
- **Bare PJSIP**: :cpp:any:`pjsip_tls_transport_restart2()` is the
  TLS-specific equivalent that takes a new ``pjsip_tls_setting``;
  :cpp:any:`pjsip_udp_transport_restart2()` provides the UDP variant
  for non-TLS settings.

These restart the **listener**; existing in-flight connections are
not torn down by the restart itself. Plan rotation around your
application's reconnection cadence: rotate the certificate, then
let connections refresh on the next register / renegotiate event.

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


Operational examples
--------------------

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

3. ``./pjsua --help`` lists all TLS-related options.

Running pjsua as a TLS client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To call a SIP server over TLS:

.. code-block:: shell

   ./pjsua --use-tls "<sip:SERVER;transport=tls>"

Mutual TLS with pjsua
~~~~~~~~~~~~~~~~~~~~~

Append the corresponding verify flag on each side:

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


Troubleshooting
---------------

- **"verification failed: certificate expired / not trusted"** —
  Inspect the per-connection :cpp:any:`pjsip_tls_state_info` from the
  transport-state callback for the OpenSSL-style error code. Common
  causes: clock skew, missing intermediate certificates, wrong CA in
  ``ca_list_file``.
- **"name mismatch"** — The server's certificate ``CN`` / SAN doesn't
  match the URI host. Either fix the certificate or set
  :cpp:any:`pjsip_tls_setting::server_name` to override the default.
- **Cipher / signature-algorithm mismatch** — The two ends share no
  common cipher or sigalg. Enumerate what your build offers with
  :cpp:any:`pj_ssl_cipher_get_availables()` /
  :cpp:any:`pj_ssl_curve_get_availables()`. Note that backend defaults
  vary; explicitly setting ``ciphers`` /``curves``/``sigalgs`` makes
  the policy explicit.
- **TLS version mismatch** — Older peers may insist on TLS 1.0/1.1,
  which modern backends often disable by default. Set ``proto``
  explicitly to enable older versions only when you must.
- **OpenSSL FIPS-mode MD5 failures** — Strict-FIPS OpenSSL builds
  disable MD5; PJSIP detects this and falls back to its internal MD5
  for digest auth. TLS does not use MD5 in modern cipher suites; if a
  TLS handshake fails due to FIPS, it is usually because of a
  legacy-only cipher choice — relax the cipher list.
- **SChannel: certificate-store ACL** — On Windows, the user that
  PJSIP runs as needs read access to the private key in the cert
  store. Use ``certutil -repairstore`` or the Certificates MMC to
  grant access.
- **Mbed TLS: TLS 1.3 missing** — Older Mbed TLS releases lack TLS 1.3
  altogether. Upgrade Mbed TLS or set ``proto`` to TLS 1.2 only.
- **Apple Secure Transport (Darwin) deprecation** — On macOS 10.15+
  and iOS 13+, prefer the ``APPLE`` (Network framework) backend.


See also
--------

- :ref:`guide_digest_auth` — what TLS protects vs what SIP digest
  auth protects, and the shared OpenSSL dependency.
- :doc:`/specific-guides/security/srtp` — media-layer security.
- :any:`/specific-guides/sip/async_auth` — for token-based or
  user-prompted auth flows that complement TLS.

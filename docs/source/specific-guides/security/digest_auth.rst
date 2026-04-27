.. _guide_digest_auth:

SIP Digest Authentication
============================

.. contents:: Table of Contents
    :depth: 2


Overview
--------

PJSIP implements HTTP digest authentication for SIP per :rfc:`3261`,
:rfc:`7616`, and :rfc:`8760`, with the following digest algorithms:

+-------------------+----------------------+-------------------------+
| Algorithm enum    | IANA name            | Reference               |
+===================+======================+=========================+
| ``MD5``           | ``MD5``              | :rfc:`3261`,            |
|                   |                      | :rfc:`7616`             |
+-------------------+----------------------+-------------------------+
| ``SHA256``        | ``SHA-256``          | :rfc:`7616`             |
+-------------------+----------------------+-------------------------+
| ``SHA512_256``    | ``SHA-512-256``      | :rfc:`7616`,            |
|                   |                      | :rfc:`8760`             |
+-------------------+----------------------+-------------------------+
| ``AKAV1_MD5``     | ``AKAv1-MD5``        | :rfc:`3310`             |
+-------------------+----------------------+-------------------------+
| ``AKAV2_MD5``     | ``AKAv2-MD5``        | :rfc:`4169`,            |
|                   |                      | 3GPP TS 33.203          |
+-------------------+----------------------+-------------------------+

The full enum is :cpp:any:`pjsip_auth_algorithm_type` in
``pjsip/sip_auth.h``. The IANA name is the value that appears in the
``algorithm`` parameter of SIP ``WWW-Authenticate`` /
``Proxy-Authenticate`` / ``Authorization`` / ``Proxy-Authorization``
headers.

MD5 has been the historical default and remains widely supported,
but it is cryptographically weak and many modern SIP servers now
mandate SHA-256 (or stronger) for compliance reasons. SHA-256 and
SHA-512/256 support landed in PJSIP 2.15
(:pr:`4118`).

This page covers how to select the digest algorithm on both the
client (UA) and server (UAS / proxy) side, build prerequisites, and
backward-compat / migration notes. For asynchronous handling of
incoming 401/407 challenges (e.g. when credentials must be fetched
from an external service before responding), see
:any:`/specific-guides/sip/async_auth`.


Build prerequisites
-------------------

Algorithm availability depends on what the build links against:

- **MD5** is always available. With OpenSSL it goes through
  ``EVP_get_digestbyname("MD5")``; in strict-FIPS OpenSSL builds where
  MD5 is unavailable, PJSIP detects this at runtime and transparently
  falls back to its internal MD5 implementation.
- **SHA-256** and **SHA-512/256** require **OpenSSL** as the SSL
  socket implementation, i.e. the library must be built with
  ``PJ_HAS_SSL_SOCK = 1`` and ``PJ_SSL_SOCK_IMP =
  PJ_SSL_SOCK_IMP_OPENSSL``. Without OpenSSL, the SHA digests are not
  computed; only MD5 works.
- **AKA-MD5** (v1 and v2) is gated separately by the compile-time
  flag :c:macro:`PJSIP_HAS_DIGEST_AKA_AUTH`, which defaults to ``0``.
  Set it to ``1`` in :any:`config_site.h` when building for IMS / VoLTE
  deployments. AKA additionally needs the application to compute the
  AKA response in a callback (see below) and is independent of the
  OpenSSL requirement above.

To check at runtime whether a given algorithm is supported in the
current build, use:

.. code-block:: c

   if (pjsip_auth_is_digest_algorithm_supported(PJSIP_AUTH_ALGORITHM_SHA256)) {
       /* SHA-256 is available */
   }

There is no separate *PJSIP_HAS_DIGEST_SHA256_AUTH* flag — SHA-256
support follows OpenSSL availability automatically.


Selecting the digest algorithm (client side)
---------------------------------------------

When acting as a UA, the application advertises its credentials via
:cpp:any:`pjsip_cred_info`. Two fields together determine which
algorithm is used in the ``Authorization`` header:

- :cpp:any:`pjsip_cred_info::data_type` — ``PJSIP_CRED_DATA_PLAIN_PASSWD``
  (plaintext password; the framework computes the H(A1) hash when
  responding to a challenge) or ``PJSIP_CRED_DATA_DIGEST`` (the
  ``data`` field already contains the pre-hashed H(A1) for the
  selected algorithm).
- :cpp:any:`pjsip_cred_info::algorithm_type` — the
  :cpp:any:`pjsip_auth_algorithm_type` to use. If left at
  :cpp:any:`PJSIP_AUTH_ALGORITHM_NOT_SET` (the default after
  ``pj_bzero()`` / ``PJ_POOL_ZALLOC_T()``), the framework treats the
  credential as MD5 — this preserves backward compatibility for
  existing apps.

When the credential's algorithm matches what the server's challenge
asked for, the framework uses that credential to compute the
response. If the server's challenge is for a different algorithm,
the framework looks for another credential on the account with a
matching ``algorithm_type``.

PJSUA-LIB
^^^^^^^^^

Each :cpp:any:`pjsua_acc_config::cred_info` array entry is a
:cpp:any:`pjsip_cred_info`. Set ``algorithm_type`` per credential.
The most common pattern: the application advertises both an MD5 and
a SHA-256 credential for the same realm/username, and the framework
picks whichever the server challenges with.

.. code-block:: c

   pjsua_acc_config cfg;

   pjsua_acc_config_default(&cfg);
   /* ...id, reg URI, etc... */

   /* Credential #0: SHA-256 */
   cfg.cred_info[0].realm    = pj_str("*");        /* match any realm */
   cfg.cred_info[0].scheme   = pj_str("digest");
   cfg.cred_info[0].username = pj_str("alice");
   cfg.cred_info[0].data_type = PJSIP_CRED_DATA_PLAIN_PASSWD;
   cfg.cred_info[0].data     = pj_str("s3cret");
   cfg.cred_info[0].algorithm_type = PJSIP_AUTH_ALGORITHM_SHA256;

   /* Credential #1: MD5 fallback for older servers */
   cfg.cred_info[1].realm    = pj_str("*");
   cfg.cred_info[1].scheme   = pj_str("digest");
   cfg.cred_info[1].username = pj_str("alice");
   cfg.cred_info[1].data_type = PJSIP_CRED_DATA_PLAIN_PASSWD;
   cfg.cred_info[1].data     = pj_str("s3cret");
   cfg.cred_info[1].algorithm_type = PJSIP_AUTH_ALGORITHM_MD5;

   cfg.cred_count = 2;

PJSUA2
^^^^^^

The PJSUA2 wrapper :cpp:any:`pj::AuthCredInfo` exposes the same field
in camelCase as :cpp:any:`pj::AuthCredInfo::algoType`:

.. code-block:: c++

   AccountConfig cfg;
   /* ...idUri, regConfig.registrarUri, etc... */

   AuthCredInfo sha;
   sha.scheme   = "digest";
   sha.realm    = "*";
   sha.username = "alice";
   sha.dataType = PJSIP_CRED_DATA_PLAIN_PASSWD;
   sha.data     = "s3cret";
   sha.algoType = PJSIP_AUTH_ALGORITHM_SHA256;
   cfg.sipConfig.authCreds.push_back(sha);

   AuthCredInfo md5;
   md5.scheme   = "digest";
   md5.realm    = "*";
   md5.username = "alice";
   md5.dataType = PJSIP_CRED_DATA_PLAIN_PASSWD;
   md5.data     = "s3cret";
   md5.algoType = PJSIP_AUTH_ALGORITHM_MD5;
   cfg.sipConfig.authCreds.push_back(md5);

Pre-hashed credentials
^^^^^^^^^^^^^^^^^^^^^^

If you don't want the plaintext password in your binary, set
``data_type`` to :cpp:any:`PJSIP_CRED_DATA_DIGEST` and put the H(A1)
hash directly in ``data``. The hash must be computed with the
algorithm declared in ``algorithm_type``:

- For MD5: ``H(A1) = MD5(username:realm:password)``, hex string.
- For SHA-256: ``H(A1) = SHA256(username:realm:password)``, hex
  string.
- For SHA-512/256: ``H(A1) = SHA-512/256(username:realm:password)``,
  hex string.

In this mode, ``algorithm_type`` MUST match the algorithm used to
compute the hash; the framework will not re-hash a digest credential.


Issuing challenges (server side)
---------------------------------

When acting as a UAS or proxy that authenticates incoming requests,
use :cpp:any:`pjsip_auth_srv_challenge2()` to attach a
``WWW-Authenticate`` (or ``Proxy-Authenticate``) header to a 401/407
response with a specific algorithm:

.. code-block:: c

   /* qop, nonce, opaque can be NULL — the framework fills them in */
   pjsip_auth_srv_challenge2(&auth_srv,
                             NULL, NULL, NULL,
                             PJ_FALSE,                  /* not stale */
                             tdata,
                             PJSIP_AUTH_ALGORITHM_SHA256);

The legacy :cpp:any:`pjsip_auth_srv_challenge()` exists for backward
compatibility but always issues an MD5 challenge — new server-side
code should call ``_challenge2()``.

To advertise multiple algorithms in one response (so a client can
pick the strongest it supports), call :cpp:any:`pjsip_auth_srv_challenge2()`
multiple times on the same ``tdata`` with different
``algorithm_type`` values. Per :rfc:`7616` the strongest algorithm
should appear first.


Helper APIs
-----------

- :cpp:any:`pjsip_auth_get_algorithm_by_type()` — returns the
  :cpp:any:`pjsip_auth_algorithm` describing an enum value (IANA
  name, OpenSSL name, digest length, hex length).
- :cpp:any:`pjsip_auth_get_algorithm_by_iana_name()` — same lookup
  by header value (e.g. ``"SHA-256"``).
- :cpp:any:`pjsip_auth_is_digest_algorithm_supported()` —
  runtime check; returns ``PJ_FALSE`` for SHA-256 / SHA-512-256
  if the build has no OpenSSL.

These are useful when the application needs to negotiate per-realm
algorithm preference dynamically, or when bridging credentials
between PJSIP and an external auth backend.


AKA authentication
------------------

Digest AKA (Authentication and Key Agreement, used in IMS / VoLTE)
is structurally similar to MD5 digest but the H(A1) hash is computed
by the application using the SIM key material rather than from a
plaintext password. To use it:

1. Build with :c:macro:`PJSIP_HAS_DIGEST_AKA_AUTH` set to ``1`` in
   :any:`config_site.h`.
2. Set ``algorithm_type`` on the credential to either
   :cpp:any:`PJSIP_AUTH_ALGORITHM_AKAV1_MD5` or
   :cpp:any:`PJSIP_AUTH_ALGORITHM_AKAV2_MD5`.
3. Set ``data_type`` to ``PJSIP_CRED_DATA_PLAIN_PASSWD |
   PJSIP_CRED_DATA_EXT_AKA``.
4. Provide the AKA inputs in the ``ext.aka`` sub-struct: ``k``
   (permanent subscriber key), ``op`` (operator variant), ``amf``
   (authentication management field), and ``cb`` — a callback that
   computes the AKA response from the challenge.
5. The PJSUA2 equivalent fields are :cpp:any:`pj::AuthCredInfo::akaK`,
   :cpp:any:`pj::AuthCredInfo::akaOp`, and
   :cpp:any:`pj::AuthCredInfo::akaAmf`.

The full AKA programming model is its own topic and not covered
further here; see ``pjsip/sip_auth_aka.h`` and
``PJSIP_AUTH_AKA_API`` for the callback contract and helper
functions.


Backward compatibility and deprecations
----------------------------------------

- Code written before SHA-256 support landed continues to work
  unchanged. Credentials with ``algorithm_type == 0``
  (``NOT_SET``) are treated as MD5.
- :cpp:any:`pjsip_auth_create_digestSHA256()` is deprecated; new
  code should use :cpp:any:`pjsip_auth_create_digest2()` with
  ``algorithm_type = PJSIP_AUTH_ALGORITHM_SHA256``. The deprecated
  helper still works but the explicit form composes more cleanly
  with the rest of the algorithm-aware API.
- :cpp:any:`pjsip_auth_create_digest()` (MD5-only) is similarly
  deprecated in favour of :cpp:any:`pjsip_auth_create_digest2()`.
- The legacy server-side :cpp:any:`pjsip_auth_srv_challenge()` keeps
  working for MD5-only deployments; use :cpp:any:`pjsip_auth_srv_challenge2()`
  to issue challenges for any other algorithm.


See also
--------

- :any:`/specific-guides/sip/async_auth` — asynchronous handling of
  401/407 challenges, plus ``pjsua_acc_config::use_shared_auth`` for
  reusing the auth session across modules (REGISTER / SUBSCRIBE /
  PUBLISH / etc.).

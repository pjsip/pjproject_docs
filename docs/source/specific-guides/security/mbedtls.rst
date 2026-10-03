.. _guide_mbedtls:

Using Mbed TLS with PJSIP
=========================================

.. contents:: Table of Contents
    :depth: 2


`Mbed TLS <https://github.com/Mbed-TLS/mbedtls>`__ is a TLS library designed for
embedded systems. PJSIP can use it as its SSL/TLS backend, for SIP over TLS, TURN
over TLS and any other ``pj_ssl_sock`` user. Its random number generator also
provides ``pj_ssl_rand_bytes()``, which PJMEDIA uses for SDES-SRTP keys.

This guide covers building Mbed TLS, building PJSIP against it, and configuring
Mbed TLS for a small footprint. It applies to both supported major versions.

See also: :any:`/specific-guides/security/ssl`.


Supported versions
------------------

- **Mbed TLS 3.6** (the long-term support branch), tested with 3.6.7.
- **Mbed TLS 4.x**, tested with 4.2.0.

Earlier versions are not supported.


Footprint
---------

Code and constant data of the TLS library linked into a PJLIB TLS client (ROM), with
the default configurations and, for Mbed TLS, with the minimal TLS 1.2 client
configurations given later, in the examples for :ref:`3.6 <mbedtls_example_36>`
and :ref:`4.x <mbedtls_example_4x>`:

.. list-table::
   :header-rows: 1

   * - Configuration
     - Mbed TLS 3.6.7
     - Mbed TLS 4.2.0
     - OpenSSL 3.6.1
   * - Default, with ``MBEDTLS_THREADING_C``
     - 410 KB
     - 377 KB
     - 3.8 MB
   * - Minimal TLS 1.2 client
     - 85 KB
     - 99 KB, or 100 KB with ``MBEDTLS_THREADING_C``
     - not measured

- Trimming the configuration saves about 75–80% of Mbed TLS's code with either
  version; see :ref:`mbedtls_small_footprint`.
- With the default configurations, 4.2 is about 8% smaller than 3.6, mostly in the
  crypto library, and both are about a tenth of OpenSSL's default build.
- With the minimal configurations, 4.2 is about 13 KB larger, mostly in the crypto
  library. A TLS 1.2 client with 3.6 can leave PSA Crypto out entirely, as the 3.6
  example does, while 4.x always includes the PSA core: its key store and the
  dispatch to the algorithms.

Static RAM (``.data`` and ``.bss``) is small: about 11 KB (3.6) and 10 KB (4.2) by
default, mostly AES tables generated at run time, and under 3 KB for the minimal
configurations. OpenSSL's is about 35 KB. Most of the RAM is allocated per TLS
connection, and is dominated by the record buffers, ``MBEDTLS_SSL_IN_CONTENT_LEN``
plus ``MBEDTLS_SSL_OUT_CONTENT_LEN``: 16 KB each by default, 16 KB and 4 KB in the
minimal configurations.

How these were measured: on x86-64 with GCC 13.3, Mbed TLS built with CMake
``MinSizeRel`` (``-Os``) and ``-ffunction-sections -fdata-sections``, then linked
with ``-Wl,--gc-sections`` into a small program that creates a PJLIB TLS socket and
calls ``pj_ssl_rand_bytes()``, which pulls in the whole PJLIB backend. OpenSSL was
built the same way, as static libraries with its default options
(``./Configure no-shared -Os -ffunction-sections -fdata-sections``), and linked
through PJLIB's OpenSSL backend. The sizes are the ``.text``, ``.rodata`` and
``.data`` taken from the TLS library's archives, from the linker map; PJSIP's own
code is not included. Absolute sizes are smaller on 32-bit microcontrollers, but the
differences between the configurations should be similar in proportion.


What changed in Mbed TLS 4
--------------------------

Mbed TLS 4 moved all cryptography into a separate project, TF-PSA-Crypto, which is
bundled in the Mbed TLS release, and exposes it only through the PSA Crypto API.
For PJSIP users the differences are:

.. list-table::
   :header-rows: 1

   * -
     - Mbed TLS 3.6
     - Mbed TLS 4.x
   * - Build system
     - CMake or make
     - CMake only
   * - Libraries
     - ``libmbedtls``, ``libmbedx509``, ``libmbedcrypto``
     - ``libmbedtls``, ``libmbedx509``, ``libtfpsacrypto``; ``libmbedcrypto`` is
       installed as a compatibility alias
   * - Configuration files
     - ``include/mbedtls/mbedtls_config.h``
     - ``include/mbedtls/mbedtls_config.h`` for TLS and X.509, plus
       ``tf-psa-crypto/include/psa/crypto_config.h`` for cryptography
   * - Selecting algorithms
     - ``MBEDTLS_xxx_C`` options
     - ``PSA_WANT_xxx`` options
   * - Random numbers used by PJSIP
     - one CTR_DRBG per TLS socket and per ``pj_ssl_rand_bytes()`` call
     - the global PSA random generator
   * - DES, 3DES and PKCS#12
     - available
     - removed: private keys encrypted with them cannot be loaded
   * - CMake package targets
     - ``MbedTLS::mbedtls``, ``MbedTLS::mbedx509``, ``MbedTLS::mbedcrypto``
     - ``MbedTLS::mbedtls``, ``MbedTLS::mbedx509``, ``MbedTLS::tfpsacrypto``

PJSIP handles these differences itself. The ones that need attention from you are
the configuration files (see :ref:`mbedtls_small_footprint`), thread safety (see
:ref:`mbedtls_thread_safety`), and encrypted private keys (see
:ref:`mbedtls_troubleshooting`).


Building Mbed TLS
-----------------

Download the release archive, e.g. ``mbedtls-4.2.0.tar.bz2``, from the
`Mbed TLS release page <https://github.com/Mbed-TLS/mbedtls/releases>`__. Do not use
the "Source code" archives that GitHub generates: they lack the ``framework``
submodule (and, for 4.x, ``tf-psa-crypto``), without which the build files and the
configuration script do not work.

With CMake (3.6 and 4.x)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ tar xjf mbedtls-4.2.0.tar.bz2
   $ cd mbedtls-4.2.0
   $ cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
           -DENABLE_TESTING=OFF -DENABLE_PROGRAMS=OFF \
           -DCMAKE_INSTALL_PREFIX=$HOME/opt/mbedtls
   $ cmake --build build -j
   $ cmake --install build

This installs the headers under ``include/`` and static libraries under ``lib/``
(``lib64/`` on some distributions), together with pkg-config files (``lib/pkgconfig``) and CMake package files
(``lib/cmake``). PJSIP's ``configure`` uses the former, and PJSIP's CMake build
needs the latter.

Useful options:

- **Shared libraries:** ``-DUSE_SHARED_MBEDTLS_LIBRARY=ON``, and with 4.x also
  ``-DUSE_SHARED_TF_PSA_CRYPTO_LIBRARY=ON``.
- **Static libraries for a shared PJSIP** (``./configure --enable-shared``): add
  ``-DCMAKE_POSITION_INDEPENDENT_CODE=ON``.
- **Smaller code:** ``-DCMAKE_BUILD_TYPE=MinSizeRel``, see :ref:`mbedtls_compiler_flags`.
- **Cross compiling:** the usual ``-DCMAKE_TOOLCHAIN_FILE=...``.

With make (3.6 only)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   $ tar xjf mbedtls-3.6.7.tar.bz2
   $ cd mbedtls-3.6.7
   $ make no_test -j
   $ make install DESTDIR=$HOME/opt/mbedtls

This also builds and installs Mbed TLS's sample programs, under ``bin/``. The make
build installs neither pkg-config nor CMake package files. PJSIP's ``configure``
does not need them, but PJSIP's CMake build does, so use CMake if you build PJSIP
with CMake.

.. _mbedtls_thread_safety:

Thread safety
~~~~~~~~~~~~~

If PJSIP is built with threads, which is the default, build Mbed TLS with its
threading layer: enable ``MBEDTLS_THREADING_C`` and ``MBEDTLS_THREADING_PTHREAD``
(or ``MBEDTLS_THREADING_ALT`` with your own mutex implementation on an RTOS).

- With **4.x** this is required. All TLS sockets and ``pj_ssl_rand_bytes()`` (SRTP
  keys) share PSA's random generator and key store, and PSA Crypto is not
  thread-safe without these options.
- With **3.6** it is recommended whenever ``MBEDTLS_PSA_CRYPTO_C`` is enabled, which
  it is by default and which TLS 1.3 needs.

In both cases, PJSIP's Mbed TLS backend warns at compile time when PJSIP has threads
and Mbed TLS has ``MBEDTLS_PSA_CRYPTO_C`` without ``MBEDTLS_THREADING_C``.

Enable the options before building, with the configuration script that comes with
the release:

.. code-block:: shell

   # Mbed TLS 3.6
   $ python3 scripts/config.py set MBEDTLS_THREADING_C
   $ python3 scripts/config.py set MBEDTLS_THREADING_PTHREAD

   # Mbed TLS 4.x (the options are in the crypto configuration)
   $ python3 tf-psa-crypto/scripts/config.py set MBEDTLS_THREADING_C
   $ python3 tf-psa-crypto/scripts/config.py set MBEDTLS_THREADING_PTHREAD


Building PJSIP with Mbed TLS
----------------------------

With configure
~~~~~~~~~~~~~~

.. code-block:: shell

   $ ./configure --with-mbedtls=$HOME/opt/mbedtls
   $ make clean
   $ make

Check the ``configure`` output for these lines:

.. code-block:: text

   Using MbedTLS prefix... /home/user/opt/mbedtls
   checking for mbedtls/version.h... yes
   MbedTLS library found, SSL support enabled

When ``--with-mbedtls`` is given, ``configure`` uses Mbed TLS instead of OpenSSL. It
may also print ``** No GnuTLS libraries found, disabling SSL support **``, which can
be ignored.

``--with-mbedtls`` takes the directory Mbed TLS is installed in. If it has
pkg-config files (``<prefix>/lib/pkgconfig`` or ``<prefix>/lib64/pkgconfig``, as a
CMake install does), the flags come from them, and pkg-config looks nowhere else, so
another Mbed TLS on the system cannot be mixed in. Otherwise ``configure`` uses
``<prefix>/include`` and links ``-lmbedtls -lmbedx509 -lmbedcrypto`` from
``<prefix>/lib`` (and ``<prefix>/lib64``, if it exists). Both work with 3.6 and 4.x,
with static or shared libraries.

Without ``--with-mbedtls``, ``configure`` prefers OpenSSL, and uses Mbed TLS only
when no other TLS library is found, from pkg-config (``PKG_CONFIG_PATH``) or the
compiler's default paths.

Run ``make clean`` whenever you switch to Mbed TLS from another backend, or between
Mbed TLS builds with a different configuration.

With CMake
~~~~~~~~~~

.. code-block:: shell

   $ cmake -S . -B build -DPJLIB_WITH_SSL=mbedtls \
           -DCMAKE_PREFIX_PATH=$HOME/opt/mbedtls \
           -DSRTP_WITH_OPENSSL=OFF
   $ cmake --build build -j

``CMAKE_PREFIX_PATH`` points at the Mbed TLS installation, which must have been
installed with CMake (it needs ``lib/cmake/MbedTLS``).

``-DSRTP_WITH_OPENSSL=OFF`` keeps the bundled libsrtp from using OpenSSL's crypto
when OpenSSL happens to be installed. Without it, a build that uses Mbed TLS for TLS
still links OpenSSL's ``libcrypto`` for SRTP.

Visual Studio
~~~~~~~~~~~~~

The Visual Studio projects do not include the Mbed TLS backend. On Windows, build
PJSIP with CMake.

Checking the result
~~~~~~~~~~~~~~~~~~~

At log level 4 or higher, PJSIP logs the Mbed TLS version when it creates its first
TLS socket:

.. code-block:: text

   ssl_sock_mbedtls.c  Mbed TLS version : Mbed TLS 4.2.0

PJLIB's test application exercises the backend, including TLS 1.2 and 1.3, client
and server certificates, and certificate name verification. Run it from
``pjlib/bin``, where it finds its test certificates:

.. code-block:: shell

   $ cd pjlib/bin
   $ ./pjlib-test-<target> ssl_sock_test

The test needs a TLS server and the default set of algorithms, so it fails with a
client-only or otherwise reduced Mbed TLS configuration.


.. _mbedtls_tls13:

Using TLS 1.3
-------------

The default configurations of both Mbed TLS versions include TLS 1.3, and the PJLIB
backend supports it. PJSIP's SIP TLS transport, however, asks for TLS 1.0 to 1.2 by
default (``PJSIP_SSL_DEFAULT_PROTO``), whatever the backend. To allow TLS 1.3 for
SIP, add ``PJ_SSL_SOCK_PROTO_TLS1_3`` to the protocol set:

- per transport, in ``pjsip_tls_setting.proto`` (in PJSUA,
  ``pjsua_transport_config.tls_setting.proto``; in PJSUA2, ``TlsConfig::proto``),
  e.g. ``PJ_SSL_SOCK_PROTO_TLS1_2 | PJ_SSL_SOCK_PROTO_TLS1_3``;
- or for the whole application, in :ref:`config_site.h`:

  .. code-block:: c

     #define PJSIP_SSL_DEFAULT_PROTO (PJ_SSL_SOCK_PROTO_TLS1_2 | \
                                      PJ_SSL_SOCK_PROTO_TLS1_3)

The backend only asks Mbed TLS for the versions it was built with, so the same
setting also works with an Mbed TLS that lacks one of them.


What PJSIP needs from Mbed TLS
------------------------------

Whatever the configuration, the PJLIB backend needs:

- a TLS client (``MBEDTLS_SSL_CLI_C``), with TLS 1.2 (``MBEDTLS_SSL_PROTO_TLS1_2``),
  TLS 1.3 (``MBEDTLS_SSL_PROTO_TLS1_3``) or both;
- X.509 certificate parsing (``MBEDTLS_X509_CRT_PARSE_C``), with the certificate
  information functions, i.e. ``MBEDTLS_X509_REMOVE_INFO`` not defined;
- private and public key parsing (``MBEDTLS_PK_PARSE_C``);
- ``MBEDTLS_VERSION_C``;
- random numbers: with 3.6, ``MBEDTLS_ENTROPY_C`` and ``MBEDTLS_CTR_DRBG_C``; with
  4.x, the PSA random generator (``MBEDTLS_PSA_CRYPTO_C`` with ``MBEDTLS_CTR_DRBG_C``
  or ``MBEDTLS_HMAC_DRBG_C``).

Optional:

.. list-table::
   :header-rows: 1

   * - Option
     - Needed for
   * - ``MBEDTLS_SSL_SRV_C``
     - accepting incoming TLS connections, e.g. a SIP TLS listener with a certificate
   * - ``MBEDTLS_FS_IO``
     - loading certificates, keys and CA lists from files or a directory; without
       it, only buffers can be used
   * - ``MBEDTLS_PEM_PARSE_C``, ``MBEDTLS_BASE64_C``
     - PEM-encoded certificates and keys; without them, DER only
   * - ``MBEDTLS_HAVE_TIME``, ``MBEDTLS_HAVE_TIME_DATE``
     - checking certificate validity dates, which needs a real-time clock
   * - ``MBEDTLS_DEBUG_C``
     - Mbed TLS debug messages, which PJSIP logs at level 3

Mbed TLS has no access to a system trust store. To verify servers
(``verify_server``), give PJSIP the CA certificates, as a file, directory or buffer.
Mbed TLS 3.6.3 and later also need the name to verify the server against, in
``server_name``; PJSIP's SIP TLS transport sets it to the remote host.


.. _mbedtls_small_footprint:

Configuring Mbed TLS for a small footprint
------------------------------------------

The default Mbed TLS configuration includes nearly every algorithm, protocol version
and feature. A device that talks to one known server needs a small part of that, and
building only that part saves most of the library's code and some of its RAM.

Principles
~~~~~~~~~~

- **One protocol version.** TLS 1.2 alone is smaller: TLS 1.3 needs HKDF and, with
  RSA certificates, RSA-PSS. Both are still in common use, so pick what your server
  supports.
- **One cipher suite, one curve.** ``TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`` over
  P-256 is supported by practically every TLS 1.2 server. Pin it with
  ``MBEDTLS_SSL_CIPHERSUITES`` so the ciphersuite table and the ClientHello carry
  only that entry.
- **Client only**, unless the device must accept TLS connections.
- **Only the certificate types your servers use**, e.g. RSA with PKCS#1 v1.5
  signatures. Add ECDSA if a server has an ECDSA certificate.
- **Smaller buffers.** ``MBEDTLS_SSL_OUT_CONTENT_LEN`` can be reduced to what the
  application sends: SIP messages are well under 4 KB. ``MBEDTLS_SSL_IN_CONTENT_LEN``
  must stay at 16384, because a server may send full-size records unless the Max
  Fragment Length extension is negotiated, which PJSIP does not do.
- **Size over speed.** A handful of options trade speed or flexibility for code
  size; see below.

.. _mbedtls_install_config:

Build the configuration into the installed headers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Structure layouts in the Mbed TLS headers depend on the configuration, so PJSIP must
be compiled against the same configuration as the library. The reliable way is to
replace the default configuration files in the source tree before building, so that
``cmake --install`` installs your configuration:

.. code-block:: shell

   # Mbed TLS 3.6
   $ cp my_mbedtls_config.h include/mbedtls/mbedtls_config.h

   # Mbed TLS 4.x
   $ cp my_mbedtls_config.h include/mbedtls/mbedtls_config.h
   $ cp my_crypto_config.h  tf-psa-crypto/include/psa/crypto_config.h

Then build and install as above, and rebuild PJSIP from clean against it.

Mbed TLS also accepts the configuration through the CMake options
``MBEDTLS_CONFIG_FILE`` and ``TF_PSA_CRYPTO_CONFIG_FILE``. Note that this does not
change the installed configuration headers: only CMake projects importing the Mbed
TLS package receive the setting, as a compile definition pointing at the original
file. PJSIP's ``configure`` build would compile against the default configuration,
so do not use these options with it.

Size options
~~~~~~~~~~~~

These options keep their names in both versions. In 4.x they are in the crypto
configuration file.

.. list-table::
   :header-rows: 1

   * - Option
     - Effect
   * - ``MBEDTLS_AES_ROM_TABLES``
     - AES tables in flash rather than generated in RAM
   * - ``MBEDTLS_AES_FEWER_TABLES``
     - one AES table instead of four, about a quarter of the table size, a little
       slower
   * - ``MBEDTLS_AES_ONLY_128_BIT_KEY_LENGTH``
     - no AES-192/256; with 3.6 needs ``MBEDTLS_CTR_DRBG_USE_128_BIT_KEY``, with 4.x
       ``MBEDTLS_PSA_CRYPTO_RNG_STRENGTH 128``
   * - ``MBEDTLS_BLOCK_CIPHER_NO_DECRYPT``
     - no AES decryption, which GCM does not use; rejected if CBC or another mode
       that needs it is enabled
   * - ``MBEDTLS_SHA256_SMALLER``
     - smaller, slower SHA-256
   * - ``MBEDTLS_MPI_WINDOW_SIZE 1``
     - smallest bignum exponentiation table; little cost for RSA signature
       verification
   * - ``MBEDTLS_MPI_MAX_SIZE 512``
     - bignums up to 4096 bits instead of 8192, shrinking stack buffers
   * - ``MBEDTLS_ECP_WINDOW_SIZE 2``
     - smallest table for elliptic curve multiplication
   * - ``MBEDTLS_ECP_FIXED_POINT_OPTIM 0``
     - no precomputed base-point table in flash; slower key generation
   * - ``MBEDTLS_ECP_NIST_OPTIM``
     - worth keeping: fast NIST curve reduction for about a kilobyte of code
   * - ``MBEDTLS_SSL_KEEP_PEER_CERTIFICATE``
     - leave undefined to free the server's certificate chain after the handshake;
       PJSIP then reports no remote certificate information

.. _mbedtls_compiler_flags:

Compiler flags
~~~~~~~~~~~~~~

Build Mbed TLS, and PJSIP, for size with ``-Os``, and add
``-ffunction-sections -fdata-sections`` to the compiler flags and
``-Wl,--gc-sections`` to the link flags of the application, so that unused functions
are dropped. With CMake:

.. code-block:: shell

   $ cmake -S . -B build -DCMAKE_BUILD_TYPE=MinSizeRel \
           -DCMAKE_C_FLAGS="-ffunction-sections -fdata-sections" ...

.. _mbedtls_example_36:

Example: minimal TLS 1.2 client, Mbed TLS 3.6
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A TLS 1.2 client with one cipher suite, ``TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256``,
over P-256, verifying RSA PKCS#1 v1.5 signatures with SHA-256. It also provides the
random generator behind ``pj_ssl_rand_bytes()``, which PJMEDIA uses for SDES-SRTP
keys. This replaces the whole ``include/mbedtls/mbedtls_config.h``:

.. code-block:: c

   /* System support */
   #define MBEDTLS_HAVE_ASM
   #define MBEDTLS_PLATFORM_C
   #define MBEDTLS_PLATFORM_MEMORY
   #define MBEDTLS_DEPRECATED_REMOVED

   /* TLS */
   #define MBEDTLS_SSL_TLS_C
   #define MBEDTLS_SSL_CLI_C
   #define MBEDTLS_SSL_PROTO_TLS1_2
   #define MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED
   #define MBEDTLS_SSL_SERVER_NAME_INDICATION
   #define MBEDTLS_SSL_EXTENDED_MASTER_SECRET
   #define MBEDTLS_SSL_CIPHERSUITES MBEDTLS_TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
   #define MBEDTLS_SSL_IN_CONTENT_LEN  16384
   #define MBEDTLS_SSL_OUT_CONTENT_LEN 4096

   /* X.509 */
   #define MBEDTLS_X509_USE_C
   #define MBEDTLS_X509_CRT_PARSE_C
   #define MBEDTLS_PK_C
   #define MBEDTLS_PK_PARSE_C
   #define MBEDTLS_ASN1_PARSE_C
   #define MBEDTLS_OID_C

   /* Public key */
   #define MBEDTLS_BIGNUM_C
   #define MBEDTLS_MPI_WINDOW_SIZE 1
   #define MBEDTLS_MPI_MAX_SIZE    512
   #define MBEDTLS_RSA_C
   #define MBEDTLS_PKCS1_V15
   #define MBEDTLS_ECP_C
   #define MBEDTLS_ECP_DP_SECP256R1_ENABLED
   #define MBEDTLS_ECP_NIST_OPTIM
   #define MBEDTLS_ECP_WINDOW_SIZE        2
   #define MBEDTLS_ECP_FIXED_POINT_OPTIM  0
   #define MBEDTLS_ECDH_C

   /* Symmetric */
   #define MBEDTLS_CIPHER_C
   #define MBEDTLS_AES_C
   #define MBEDTLS_AES_ROM_TABLES
   #define MBEDTLS_AES_FEWER_TABLES
   #define MBEDTLS_AES_ONLY_128_BIT_KEY_LENGTH
   #define MBEDTLS_BLOCK_CIPHER_NO_DECRYPT
   #define MBEDTLS_GCM_C

   /* Hash */
   #define MBEDTLS_MD_C
   #define MBEDTLS_SHA256_C
   #define MBEDTLS_SHA256_SMALLER

   /* Random numbers */
   #define MBEDTLS_ENTROPY_C
   #define MBEDTLS_ENTROPY_FORCE_SHA256
   #define MBEDTLS_CTR_DRBG_C
   #define MBEDTLS_CTR_DRBG_USE_128_BIT_KEY

   #define MBEDTLS_VERSION_C

This configuration leaves out PSA Crypto, which TLS 1.2 does not need with 3.6, so
the threading layer is not needed either.

.. _mbedtls_example_4x:

Example: minimal TLS 1.2 client, Mbed TLS 4.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same profile for Mbed TLS 4.x, as a pair of files.
``include/mbedtls/mbedtls_config.h``:

.. code-block:: c

   #define MBEDTLS_SSL_TLS_C
   #define MBEDTLS_SSL_CLI_C
   #define MBEDTLS_SSL_PROTO_TLS1_2
   #define MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED
   #define MBEDTLS_SSL_SERVER_NAME_INDICATION
   #define MBEDTLS_SSL_EXTENDED_MASTER_SECRET
   #define MBEDTLS_SSL_CIPHERSUITES MBEDTLS_TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
   #define MBEDTLS_SSL_IN_CONTENT_LEN  16384
   #define MBEDTLS_SSL_OUT_CONTENT_LEN 4096

   #define MBEDTLS_X509_USE_C
   #define MBEDTLS_X509_CRT_PARSE_C

   #define MBEDTLS_VERSION_C

``tf-psa-crypto/include/psa/crypto_config.h``:

.. code-block:: c

   #ifndef PSA_CRYPTO_CONFIG_H
   #define PSA_CRYPTO_CONFIG_H

   /* Algorithms and key types */
   #define PSA_WANT_ALG_ECDH                        1
   #define PSA_WANT_ECC_SECP_R1_256                 1
   #define PSA_WANT_KEY_TYPE_ECC_PUBLIC_KEY         1
   #define PSA_WANT_KEY_TYPE_ECC_KEY_PAIR_BASIC     1
   #define PSA_WANT_KEY_TYPE_ECC_KEY_PAIR_IMPORT    1
   #define PSA_WANT_KEY_TYPE_ECC_KEY_PAIR_GENERATE  1
   #define PSA_WANT_ALG_RSA_PKCS1V15_SIGN           1
   #define PSA_WANT_KEY_TYPE_RSA_PUBLIC_KEY         1
   /* Required by MBEDTLS_KEY_EXCHANGE_ECDHE_RSA_ENABLED, even for a client */
   #define PSA_WANT_KEY_TYPE_RSA_KEY_PAIR_BASIC     1
   #define PSA_WANT_ALG_GCM                         1
   #define PSA_WANT_KEY_TYPE_AES                    1
   #define PSA_WANT_ALG_SHA_256                     1
   #define PSA_WANT_ALG_HMAC                        1
   #define PSA_WANT_KEY_TYPE_HMAC                   1
   #define PSA_WANT_ALG_TLS12_PRF                   1

   /* Core and random numbers */
   #define MBEDTLS_PSA_CRYPTO_C
   #define MBEDTLS_PSA_BUILTIN_GET_ENTROPY
   #define MBEDTLS_CTR_DRBG_C
   #define MBEDTLS_PSA_CRYPTO_RNG_STRENGTH          128
   #define MBEDTLS_HAVE_ASM
   #define MBEDTLS_PLATFORM_C
   #define MBEDTLS_PLATFORM_MEMORY

   /* Certificates and keys */
   #define MBEDTLS_ASN1_PARSE_C
   #define MBEDTLS_PK_C
   #define MBEDTLS_PK_PARSE_C

   /* Size over speed */
   #define MBEDTLS_AES_ROM_TABLES
   #define MBEDTLS_AES_FEWER_TABLES
   #define MBEDTLS_AES_ONLY_128_BIT_KEY_LENGTH
   #define MBEDTLS_BLOCK_CIPHER_NO_DECRYPT
   #define MBEDTLS_SHA256_SMALLER
   #define MBEDTLS_MPI_WINDOW_SIZE                  1
   #define MBEDTLS_MPI_MAX_SIZE                     512
   #define MBEDTLS_ECP_NIST_OPTIM
   #define MBEDTLS_ECP_WINDOW_SIZE                  2
   #define MBEDTLS_ECP_FIXED_POINT_OPTIM            0

   #endif /* PSA_CRYPTO_CONFIG_H */

If PJSIP is built with threads, also define ``MBEDTLS_THREADING_C`` and
``MBEDTLS_THREADING_PTHREAD`` in the crypto file; PJSIP warns at compile time if they
are missing.

Adapting the examples
~~~~~~~~~~~~~~~~~~~~~

Mbed TLS checks the configuration when it is compiled and names any missing
prerequisite in an ``#error`` from ``check_config.h`` (4.x:
``mbedtls_check_config.h``), which is the quickest guide when adding features.
Common additions:

.. list-table::
   :header-rows: 1

   * - Need
     - 3.6
     - 4.x
   * - Server with an ECDSA certificate
     - ``MBEDTLS_ECDSA_C``, ``MBEDTLS_ASN1_WRITE_C``,
       ``MBEDTLS_KEY_EXCHANGE_ECDHE_ECDSA_ENABLED``, and its suite in
       ``MBEDTLS_SSL_CIPHERSUITES``
     - ``PSA_WANT_ALG_ECDSA``, ``MBEDTLS_KEY_EXCHANGE_ECDHE_ECDSA_ENABLED``, and its
       suite
   * - Server that only offers AES-256-GCM
     - drop the AES-128-only options, add ``MBEDTLS_SHA512_C`` and
       ``MBEDTLS_SHA384_C``, and the ``..._AES_256_GCM_SHA384`` suite
     - drop the AES-128-only options, add ``PSA_WANT_ALG_SHA_384``, and the suite
   * - TLS 1.3
     - ``MBEDTLS_SSL_PROTO_TLS1_3``,
       ``MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_EPHEMERAL_ENABLED``,
       ``MBEDTLS_PSA_CRYPTO_C``, ``MBEDTLS_HKDF_C``, ``MBEDTLS_PKCS1_V21``
     - ``MBEDTLS_SSL_PROTO_TLS1_3``,
       ``MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_EPHEMERAL_ENABLED``,
       ``PSA_WANT_ALG_HKDF_EXTRACT``, ``PSA_WANT_ALG_HKDF_EXPAND``,
       ``PSA_WANT_ALG_RSA_PSS``
   * - Accepting TLS connections
     - ``MBEDTLS_SSL_SRV_C`` and the server's key type
     - ``MBEDTLS_SSL_SRV_C`` and the server's key type
   * - PEM certificates or CA lists
     - ``MBEDTLS_PEM_PARSE_C``, ``MBEDTLS_BASE64_C``
     - ``MBEDTLS_PEM_PARSE_C``, ``MBEDTLS_BASE64_C``
   * - Certificate validity dates
     - ``MBEDTLS_HAVE_TIME``, ``MBEDTLS_HAVE_TIME_DATE``
     - ``MBEDTLS_HAVE_TIME``, ``MBEDTLS_HAVE_TIME_DATE``
   * - Troubleshooting
     - ``MBEDTLS_DEBUG_C``, ``MBEDTLS_ERROR_C``
     - ``MBEDTLS_DEBUG_C``, ``MBEDTLS_ERROR_C``

With TLS 1.3, remember to :ref:`enable it in PJSIP <mbedtls_tls13>` as well.

Entropy on embedded targets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both examples take their entropy from the operating system (``getrandom()`` or
``/dev/urandom`` on Linux). On a target without one, give Mbed TLS a hardware
source:

- **3.6:** define ``MBEDTLS_NO_PLATFORM_ENTROPY``, and either register a source with
  ``mbedtls_entropy_add_source()`` or implement ``mbedtls_hardware_poll()`` with
  ``MBEDTLS_ENTROPY_HARDWARE_ALT``.
- **4.x:** replace ``MBEDTLS_PSA_BUILTIN_GET_ENTROPY`` with
  ``MBEDTLS_PSA_DRIVER_GET_ENTROPY`` and implement ``mbedtls_platform_get_entropy()``
  (declared in ``mbedtls/platform.h``), or provide a complete random generator with
  ``MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG``. A device with no entropy source at all can use
  a seed provisioned in non-volatile memory, with ``MBEDTLS_ENTROPY_NV_SEED``.


.. _mbedtls_troubleshooting:

Troubleshooting
---------------

**Failed to mbedtls_pk_parse_keyfile, ret = -0x2E80 with Mbed TLS 4.x.**
The private key is encrypted with an algorithm Mbed TLS 4 no longer has, typically
3DES (``MBEDTLS_ERR_PKCS5_FEATURE_UNAVAILABLE``), as older OpenSSL versions produce
for ``-des3``. Re-encrypt it with AES, keeping the password:

.. code-block:: shell

   $ openssl pkcs8 -topk8 -v2 aes-256-cbc -v2prf hmacWithSHA256 \
             -in old_key.pem -out new_key.pem

**Random crashes or failed handshakes after changing the Mbed TLS configuration.**
PJSIP was compiled against a different configuration than the library: rebuild PJSIP
from clean against the installed headers, and make sure the installed configuration
files are the ones the library was built with (see :ref:`mbedtls_install_config`).

**Unsupported TLS protocol.**
The application asked only for protocol versions that this Mbed TLS build does not
have, e.g. TLS 1.3 alone from a TLS 1.2-only build.

**Handshake fails when verifying the server.**
Mbed TLS has no system trust store: supply the CA certificates. With PEM files, the
configuration needs ``MBEDTLS_PEM_PARSE_C``; to load files at all, ``MBEDTLS_FS_IO``.
With Mbed TLS 3.6.3 and later, ``Failed to mbedtls_ssl_handshake, ret -0x5D80``
(``MBEDTLS_ERR_SSL_CERTIFICATE_VERIFICATION_WITHOUT_HOSTNAME``) means the client
verifies the server but has no name to verify it against: set ``server_name`` in
``pj_ssl_sock_param``.

**More detail.**
Build Mbed TLS with ``MBEDTLS_DEBUG_C``; its messages then appear in the PJSIP log at
level 3.

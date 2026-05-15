.. _guide_srtp:

SRTP — Secure RTP (SDES and DTLS-SRTP)
==========================================

.. contents:: Table of Contents
    :depth: 2

.. tip::

   PJSUA-LIB readers — symbol equivalents are listed at the bottom of
   this page.


Overview
--------

Secure RTP (SRTP, :rfc:`3711`) provides confidentiality, message
authentication, and replay protection for RTP/RTCP media streams.
What SRTP doesn't do is *exchange the keys* — that's a separate
problem solved by a **keying method**. PJSIP supports two:

- **SDES** (:rfc:`4568`) — keys are carried in the SDP offer/answer.
  Simple, but only secure if the signalling path itself is
  encrypted (TLS, S/MIME, etc.) — otherwise anyone who can read the
  SDP can decrypt the media.
- **DTLS-SRTP** (:rfc:`5763` / :rfc:`5764`) — a DTLS handshake on
  the media socket derives SRTP keys via the TLS-Exporter
  (:rfc:`5705`). Keys never traverse the signalling path; SDP only
  carries the peer's certificate fingerprint for authentication.

Default usage on a PJSUA / PJSUA2 account is **DISABLED**
(:c:macro:`PJSUA_DEFAULT_USE_SRTP`). When SRTP is enabled, both
keying methods are available with the default priority **SDES then
DTLS-SRTP**.

**As offerer**, the outgoing SDP carries the *first* keying from
the priority list. The m-line transport reflects that keying:

- SDES → ``RTP/AVP`` (OPTIONAL mode) or ``RTP/SAVP`` (MANDATORY)
- DTLS-SRTP → ``UDP/TLS/RTP/SAVP`` (any mode)

With the default priority (SDES first), outgoing offers use SDES.
To send DTLS-SRTP offers instead, reorder ``srtpOpt.keyings`` to
put ``PJMEDIA_SRTP_KEYING_DTLS_SRTP`` first.

**As answerer**, the keying used is whichever matches the actual
offer received:

- An SDES-style offer (``RTP/AVP`` or ``RTP/SAVP`` m-line with
  ``a=crypto``) → answered with SDES.
- A DTLS-SRTP offer (``UDP/TLS/RTP/SAVP`` m-line with
  ``a=fingerprint``) → answered with DTLS-SRTP.
- An offer with both styles (some non-standard peers do this) →
  priority list breaks the tie.

If the offer matches no enabled keying, the SRTP transport reports
an error and the call is rejected (or falls back to non-secure
media, depending on the ``use_srtp`` mode).

SRTP is implemented as a :doc:`media transport adapter
</specific-guides/media/transport_adapter>` wrapping the underlying
UDP/ICE transport.


Choosing SDES vs DTLS-SRTP
--------------------------

+---------------------------------+----------------------------------+
| SDES (:rfc:`4568`)              | DTLS-SRTP (:rfc:`5763`/`5764`)   |
+=================================+==================================+
| Keys in SDP offer/answer        | Keys derived from DTLS handshake |
|                                 | (TLS-Exporter, :rfc:`5705`)      |
+---------------------------------+----------------------------------+
| Requires confidential signalling| Signalling carries fingerprint   |
| (TLS / SIPS) to be safe         | only; safe over plaintext SIP    |
+---------------------------------+----------------------------------+
| Built-in, always available      | Requires                         |
|                                 | ``PJMEDIA_SRTP_HAS_DTLS=1`` and  |
|                                 | the **OpenSSL** SSL backend      |
+---------------------------------+----------------------------------+
| One round-trip (in SDP)         | DTLS handshake on media path     |
|                                 | adds ~1 RTT before media flows   |
+---------------------------------+----------------------------------+
| Wide cipher choice              | Cipher suite limited to four     |
|                                 | (see below)                      |
+---------------------------------+----------------------------------+
| Wide interop (legacy SIP fleets)| WebRTC-aligned; required for     |
|                                 | WebRTC interop                   |
+---------------------------------+----------------------------------+

If you control both endpoints and they're modern, prefer DTLS-SRTP
— it removes the "signalling must also be encrypted" caveat that
trips up SDES deployments. For interop with legacy SIP equipment,
keep SDES enabled (it's the default-preferred keying anyway).


Build prerequisites
-------------------

SRTP itself (SDES)
~~~~~~~~~~~~~~~~~~

Enabled by default. The bundled libsrtp library
(:sourcedir:`third_party/srtp`) is built unconditionally; the SRTP
transport is gated by :c:macro:`PJMEDIA_HAS_SRTP` (default ``1``).
To disable entirely:

.. code-block:: c

   #define PJMEDIA_HAS_SRTP  0

External libsrtp can be used instead via the autotools option
``--with-external-srtp`` (see :issue:`2050`).

DTLS-SRTP
~~~~~~~~~

Disabled by default. Two preconditions:

1. **Build with OpenSSL.** DTLS-SRTP is OpenSSL-only as of
   :pr:`4239` — GnuTLS and Mbed TLS backends do not implement the
   required ``SSL_export_keying_material()`` path. Build with
   ``--with-ssl`` (the autotools default if OpenSSL is found) or
   the equivalent CMake setting.
2. **Enable the macro.** Set
   :c:macro:`PJMEDIA_SRTP_HAS_DTLS` to ``1`` in
   :any:`config_site.h`:

   .. code-block:: c

      #define PJMEDIA_SRTP_HAS_DTLS  1

Optional tuning macros:

- :c:macro:`PJMEDIA_SRTP_DTLS_OSSL_CIPHERS` — OpenSSL cipher list
  for the DTLS handshake (default ``"DEFAULT"``).
- :c:macro:`PJMEDIA_SRTP_DTLS_CHECK_HELLO_ADDR` — gate the
  ClientHello source-address check (default ``0``, see *ClientHello
  source-address validation* under DTLS-SRTP below).


Enabling SRTP
-------------

Two account-level settings drive SRTP behaviour:

**Use policy** (:cpp:any:`pj::AccountMediaConfig::srtpUse` /
:cpp:any:`pjsua_acc_config::use_srtp`) — picks one of three values.
The behaviour depends on whether the account is the offerer or the
answerer (summary from
:sourcedir:`pjmedia/src/pjmedia/transport_srtp.c`):

:c:macro:`PJMEDIA_SRTP_DISABLED`
   - **Offerer**: SRTP is skipped entirely; the offer is plain
     ``RTP/AVP`` with no SRTP attributes.
   - **Answerer**: accepts only non-secure offers. A remote offer
     that *requires* SRTP (``RTP/SAVP``, or ``UDP/TLS/RTP/SAVP``
     for DTLS-SRTP) is rejected with 488 / Not Acceptable Here.

:c:macro:`PJMEDIA_SRTP_OPTIONAL`
   - **Offerer**: SRTP is offered. For SDES the m-line is
     ``RTP/AVP`` with ``a=crypto``, which the peer may answer either
     securely (echo back a chosen crypto) or non-securely (omit
     crypto). For DTLS-SRTP the m-line is ``UDP/TLS/RTP/SAVP``,
     which the peer must accept as DTLS-SRTP or reject (the same
     m-line cannot answer ``RTP/AVP``); OPTIONAL adds nothing
     special on the offerer side for DTLS-SRTP.
   - **Answerer**: accept whatever the remote offered. Non-secure
     offers are answered non-secure; SRTP offers are answered with
     SRTP. This is where OPTIONAL really matters — it lets the
     local side join non-secure calls when the remote initiated
     them.

:c:macro:`PJMEDIA_SRTP_MANDATORY`
   - **Offerer**: the offer requires SRTP — ``RTP/SAVP`` for SDES
     or ``UDP/TLS/RTP/SAVP`` for DTLS-SRTP. No non-secure fallback.
   - **Answerer**: per :rfc:`3711` / :rfc:`4568`, SRTP requires the
     m-line transport profile to be an SRTP profile. PJSIP
     enforces this — anything else is rejected, including
     non-compliant offers that put ``a=crypto`` on a plain
     ``RTP/AVP`` m-line. The call is rejected with 488 / Not
     Acceptable Here.

Default on a fresh :cpp:any:`pjsua_acc_config` is
:c:macro:`PJSUA_DEFAULT_USE_SRTP` (compile-time, ``DISABLED`` in
the default build).

**Signalling requirement**
(:cpp:any:`pj::AccountMediaConfig::srtpSecureSignaling` /
:cpp:any:`pjsua_acc_config::srtp_secure_signaling`):

- ``0`` — no requirement on signalling transport. Only safe for
  DTLS-SRTP, where the keys aren't on the SIP path. **Not safe for
  SDES**, which carries plaintext keys in SDP.
- ``1`` — SIP transport must be TLS. Default
  (:c:macro:`PJSUA_DEFAULT_SRTP_SECURE_SIGNALING`).
- ``2`` — end-to-end SIPS URI required.

Plus an optional per-account override for cryptos and keying-method
priority via
:cpp:any:`pj::AccountMediaConfig::srtpOpt` /
:cpp:any:`pjsua_acc_config::srtp_opt`. Both ``srtpUse`` and
``srtpOpt`` also have global defaults on :cpp:any:`pj::UaConfig`
and :cpp:any:`pjsua_config`.

PJSUA2
~~~~~~

.. code-block:: c++

   AccountConfig acc_cfg;
   // ... existing config ...
   acc_cfg.mediaConfig.srtpUse              = PJMEDIA_SRTP_MANDATORY;
   acc_cfg.mediaConfig.srtpSecureSignaling  = 1;   // TLS required

   // Optional: prefer DTLS-SRTP over SDES on this account.
   // The keyings vector is in priority order.
   acc_cfg.mediaConfig.srtpOpt.keyings.clear();
   acc_cfg.mediaConfig.srtpOpt.keyings.push_back(PJMEDIA_SRTP_KEYING_DTLS_SRTP);
   acc_cfg.mediaConfig.srtpOpt.keyings.push_back(PJMEDIA_SRTP_KEYING_SDES);

   try {
       account.create(acc_cfg);   // or account.modify(acc_cfg)
   } catch(Error& err) {
   }

Leaving ``srtpOpt.keyings`` empty (the default) enables both with
the built-in default order (SDES first, DTLS-SRTP second).

PJSUA-LIB
~~~~~~~~~

.. code-block:: c

    pjsua_acc_config acc_cfg;
    pjsua_acc_config_default(&acc_cfg);
    acc_cfg.use_srtp              = PJMEDIA_SRTP_MANDATORY;
    acc_cfg.srtp_secure_signaling = 1;

    /* Optional: prefer DTLS-SRTP over SDES. */
    acc_cfg.srtp_opt.keying_count = 2;
    acc_cfg.srtp_opt.keying[0]    = PJMEDIA_SRTP_KEYING_DTLS_SRTP;
    acc_cfg.srtp_opt.keying[1]    = PJMEDIA_SRTP_KEYING_SDES;

    pjsua_acc_add(&acc_cfg, PJ_TRUE, NULL);

The :cpp:any:`pjsua_srtp_opt` struct mirrors
:cpp:any:`pjmedia_srtp_setting` minus the ROC fields (which are
per-call, not per-account).

pjsua CLI
~~~~~~~~~

.. code-block:: shell

   # Mandatory SRTP, SDES priority (default), over TLS:
   $ ./pjsua --use-tls --use-srtp=2 --srtp-secure=1 sip:peer@example.com;transport=tls

   # Mandatory SRTP, DTLS-SRTP priority:
   $ ./pjsua --use-tls --use-srtp=2 --srtp-keying=1 sip:peer@example.com;transport=tls

Flags:

- ``--use-srtp=N`` — ``use_srtp`` (0 disabled / 1 optional / 2
  mandatory).
- ``--srtp-secure=N`` — ``srtp_secure_signaling`` (0/1/2).
- ``--srtp-keying=N`` — keying-method priority. ``0`` = SDES first
  (default), ``1`` = DTLS-SRTP first.


SDES (RFC 4568)
---------------

Keys travel in the SDP offer/answer as ``a=crypto:`` lines. PJSIP
generates one ``a=crypto`` per supported cipher in the offer, in
priority order; the answerer picks one and echoes it back. The
selected keys are installed on the SRTP transport before the first
RTP packet flows.

Supported cipher suites (priority order, :issue:`1943` for
AES-GCM details):

- ``AES_CM_128_HMAC_SHA1_80``
- ``AES_CM_128_HMAC_SHA1_32``
- ``AES_256_CM_HMAC_SHA1_80``
- ``AES_256_CM_HMAC_SHA1_32``
- ``AES_192_CM_HMAC_SHA1_80`` [#aes192]_
- ``AES_192_CM_HMAC_SHA1_32`` [#aes192]_
- ``AEAD_AES_256_GCM`` [#gcm]_
- ``AEAD_AES_256_GCM_8`` [#gcm]_
- ``AEAD_AES_128_GCM`` [#gcm]_
- ``AEAD_AES_128_GCM_8`` [#gcm]_

.. [#aes192] Works on some libSRTP versions only and needs OpenSSL.
   See :issue:`1943`.
.. [#gcm] Requires OpenSSL. See :issue:`1943` and
   :ref:`srtp_aes_gcm` below.

Negotiation of crypto session parameters in SDP is not yet
supported.

Customising the cipher list — set
``mediaConfig.srtpOpt.cryptos`` (PJSUA2) /
``srtp_opt.crypto[]`` (PJSUA-LIB). Leaving it empty enables all
available cryptos in default order.

**Security note.** SDES is only as secure as the channel that
carries the SDP. Use ``srtpSecureSignaling = 1`` to require a TLS
transport for SIP signalling, or ``= 2`` to require end-to-end
``sips:`` URIs.


DTLS-SRTP (RFC 5763 / 5764)
---------------------------

Introduced in PJSIP 2.7 (:issue:`2018`). Separate DTLS handshakes
for RTP and RTCP arrived in 2.14 (:pr:`3571`); the optional
ClientHello source-address check in 2.16 (:pr:`4261`).

The SDP offer/answer carries only the local certificate
*fingerprint* via the ``a=fingerprint:`` attribute (:rfc:`5763`
§5). After offer/answer completes, each side runs a DTLS handshake
directly on the media socket; the master SRTP key and salt are
derived from the negotiated DTLS keying material via
:rfc:`5705` TLS-Exporter with label
``"EXTRACTOR-dtls_srtp"`` (:rfc:`5764` §4.2). The actual SRTP keys
never appear in SIP signalling.

.. note::

   The use-policy enum (``DISABLED`` / ``OPTIONAL`` /
   ``MANDATORY``) is shared with SDES, but the m-line transport
   for DTLS-SRTP does **not** vary by mode — when DTLS-SRTP is
   the selected keying, the offerer always uses
   ``UDP/TLS/RTP/SAVP``. The mode at the SRTP-transport level
   still controls whether a *non-SRTP* offer is acceptable
   (OPTIONAL falls back to plain RTP/AVP if no enabled keying
   matches; MANDATORY rejects). Switching between SDES and
   DTLS-SRTP is automatic based on what's in the SDP and what
   keyings are enabled.

Cipher suites
~~~~~~~~~~~~~

Per :rfc:`5764`, only four SRTP cipher suites are valid with
DTLS-SRTP, regardless of what SDES would allow:

- ``AES_CM_128_HMAC_SHA1_80``
- ``AES_CM_128_HMAC_SHA1_32``
- ``AEAD_AES_256_GCM``
- ``AEAD_AES_128_GCM``

The SRTP key itself is not user-configurable — DTLS-SRTP derives it
from the handshake.

RTP and RTCP run separate handshakes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PJSIP runs two independent DTLS state machines, one for the RTP
socket and one for the RTCP socket, with separate
``SSL_export_keying_material()`` calls per channel. This was added
in :pr:`3571`. Practical implications:

- RTCP-MUX (where both share a port) collapses the two into one
  handshake.
- Without RTCP-MUX, expect two ClientHello exchanges and roughly
  twice the handshake bandwidth.
- A mid-session RTCP-address change (e.g. after IP-change handling)
  is handled by :pr:`3732` — the RTCP DTLS state is reset and the
  handshake restarts on the new address.

ClientHello source-address validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, PJSIP forwards incoming DTLS ClientHello packets to
OpenSSL regardless of source address. An attacker who can spoof UDP
source addresses could trigger early-stage handshake processing
before SDP-level peer commitment. To require that the ClientHello's
source IP/port match the SDP-advertised remote, set:

.. code-block:: c

   #define PJMEDIA_SRTP_DTLS_CHECK_HELLO_ADDR  1

When enabled, packets from unexpected sources are dropped at the
SRTP layer before reaching OpenSSL (:pr:`4261`). Disabled by
default because it adds a hard ordering requirement (SDP
offer/answer must complete before the peer's ClientHello arrives —
not always true on lossy mobile networks).

When NAT is in play (notably with ICE), the validation is deferred
to ICE — ICE already validates the source via STUN connectivity
checks, so the SRTP-layer check is skipped to avoid double-checking
the same property.

Certificates
~~~~~~~~~~~~

The DTLS certificate is taken from the global SSL context, the
same one used for the SIP TLS transport. There is no per-account
DTLS certificate configuration today — if you need different certs
per account, you'd have to manage multiple endpoints or extend the
SRTP setup at the PJMEDIA layer directly. The fingerprint that
appears in ``a=fingerprint:`` is computed from this global cert and
is retrievable via
:cpp:any:`pjmedia_transport_srtp_dtls_get_fingerprint`.

Interaction with ICE
~~~~~~~~~~~~~~~~~~~~

DTLS handshake packets flow over the ICE transport once a
candidate pair is selected. The DTLS handshake won't start until
ICE has produced a working pair — adding ~1 RTT on top of ICE
negotiation. The handshake survives ICE candidate-pair changes
because the DTLS state is per-stream, not per-candidate.

Interaction with re-INVITE / IP change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:pr:`4639` made re-INVITE DTLS handling idempotent — a re-INVITE
that doesn't actually change addresses won't trigger a new
handshake. For IP-change scenarios (see
:doc:`/specific-guides/network_nat/ip_change`), the
media transport is reinitialised and DTLS runs a fresh handshake
on the new path; ROC state is preserved via
:cpp:any:`pjmedia_srtp_setting::rx_roc` / ``tx_roc`` to avoid SRTP
replay-window resets.


Using SRTP transport directly (advanced)
----------------------------------------

The SRTP transport can be used outside the PJSUA / PJSUA2 flow —
for example, in a non-SIP application or to bridge custom media.
See :sourcedir:`pjsip-apps/src/samples/streamutil.c` for a worked
example. Briefly:

1. Create the underlying media transport (UDP, ICE, etc.).
2. :cpp:any:`pjmedia_transport_srtp_create` to wrap it, passing a
   :cpp:any:`pjmedia_srtp_setting`.
3. For SDES — :cpp:any:`pjmedia_transport_srtp_start` with the
   negotiated tx/rx cryptos (you supply both sides' keys; key
   exchange is your problem).
4. For DTLS-SRTP — call
   :cpp:any:`pjmedia_transport_srtp_dtls_start_nego` with a
   :cpp:any:`pjmedia_srtp_dtls_nego_param` containing the peer's
   fingerprint, remote RTP / RTCP addresses, and the role
   (``is_role_active`` true = initiator).
5. :cpp:any:`pjmedia_transport_attach` to wire up RTP/RTCP
   callbacks and start I/O.
6. :cpp:any:`pjmedia_transport_close` when done. If
   :cpp:any:`pjmedia_srtp_setting::close_member_tp` is true the
   underlying transport is closed too.

The setup callback
(:cpp:any:`pjmedia_srtp_cb::on_srtp_nego_complete`) fires once
DTLS-SRTP keys are installed.


.. _srtp_aes_gcm:

AES-GCM support
---------------

PJSIP 2.6 enabled AES-GCM (:issue:`1943`), but the bundled libSRTP
(1.5.4 at that time) had a compatibility issue with OpenSSL 1.1.0.
The libSRTP update in :issue:`1993` (included in 2.7) resolved
that.

External libSRTP can be used instead via ``--with-external-srtp``
(:issue:`2050`); tested with libSRTP 1.5.4 and 2.1.0. Note that
AES-GCM requires building PJSIP with SSL enabled.


Diagnostics
-----------

What the SDP looks like
~~~~~~~~~~~~~~~~~~~~~~~

**SDES, OPTIONAL mode** — ``RTP/AVP`` m-line (i.e. non-secure
profile) plus one or more ``a=crypto`` lines. The peer can choose
to use SRTP or not:

.. code-block:: text

   m=audio 4000 RTP/AVP 0 8
   a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:WVNfX19zZW1jdGwgKGNyeXB0bykgaXMgY29
   a=crypto:2 AES_CM_128_HMAC_SHA1_32 inline:WVNfX19zZW1jdGwgKGNyeXB0bykgaXMgY29

**SDES, MANDATORY mode** — ``RTP/SAVP`` m-line, no fallback:

.. code-block:: text

   m=audio 4000 RTP/SAVP 0 8
   a=crypto:1 AES_CM_128_HMAC_SHA1_80 inline:WVNfX19zZW1jdGwgKGNyeXB0bykgaXMgY29

The answerer echoes back one ``a=crypto`` with the chosen suite
and its own keying material.

**DTLS-SRTP offer** — ``UDP/TLS/RTP/SAVP`` m-line (:rfc:`5764`
§8) plus ``a=fingerprint:`` and ``a=setup:``:

.. code-block:: text

   m=audio 4000 UDP/TLS/RTP/SAVP 0 8
   a=fingerprint:SHA-256 6B:8B:F0:65:5F:78:E2:51:3B:AC:6F:F3:3F:46:1B:35:DC:B8:5F:64:1A:24:C2:43:F0:A1:58:D0:A1:2C:19:08
   a=setup:actpass

The ``a=fingerprint`` line uses the algorithm name from
:cpp:any:`pjmedia_transport_srtp_dtls_get_fingerprint`; the
``a=setup`` value follows :rfc:`5763` (``actpass`` in offers,
``active`` / ``passive`` in answers).

Note: only the highest-priority enabled keying's attributes appear
in the offer — the offerer doesn't advertise both SDES and DTLS-SRTP
in the same m-line.

Log lines
~~~~~~~~~

At log level 2:

.. code-block:: text

   DTLS-SRTP negotiation for RTP completed!
   DTLS-SRTP negotiation for RTCP completed!

At log level 4 (per
:sourcedir:`pjmedia/src/pjmedia/transport_srtp.c` and
:sourcedir:`pjmedia/src/pjmedia/transport_srtp_dtls.c`):

.. code-block:: text

   SRTP transport created
   SRTP uses keying method <SDES|DTLS-SRTP>
   DTLS-SRTP <client|server> negotiation initiated as <active|passive>
   <profile-name> profile is supported

Level 5 prints per-direction key installation
(``TX: <crypto> key=<base64>``, ``RX: <crypto> key=<base64>``) and
per-packet trace.

If SRTP fails, look for level-4 ``"SRTP not active"`` and the
specific error codes:

- ``PJMEDIA_SRTP_ESDPREQCRYPTO`` — mandatory SRTP, peer didn't
  provide ``a=crypto``.
- ``PJMEDIA_SRTP_ECRYPTONOTMATCH`` — peer picked a crypto suite
  not in the local offer.
- ``PJMEDIA_SDP_EINPROTO`` — m-line protocol mismatch (e.g.
  MANDATORY locally, peer offered ``RTP/AVP``).

Call dump (PJSUA-LIB)
~~~~~~~~~~~~~~~~~~~~~

:cpp:any:`pjsua_call_dump` emits one line per call with SRTP
status, populated from :cpp:any:`pjmedia_srtp_info`:

.. code-block:: text

      SRTP status: Active Crypto-suite: AES_CM_128_HMAC_SHA1_80

When SRTP is disabled / failed: ``SRTP status: Not active`` with
empty crypto-suite.

Programmatic checks
~~~~~~~~~~~~~~~~~~~

For application-level UI / logging:

- :cpp:any:`pjmedia_srtp_cb::on_srtp_nego_complete` fires when the
  keying handshake finishes (either SDES offer/answer or DTLS-SRTP
  handshake).
- :cpp:any:`pjmedia_transport_get_info` populates a
  :cpp:any:`pjmedia_transport_info` whose ``spc_info[]`` array
  holds one entry per stacked transport type (SRTP, ICE, ...).
  Find the SRTP entry by ``type == PJMEDIA_TRANSPORT_TYPE_SRTP``
  and cast its ``buffer`` to :cpp:any:`pjmedia_srtp_info`:

  .. code-block:: c

      pjmedia_transport_info tp_info;
      pjmedia_srtp_info     *srtp_info = NULL;
      unsigned j;

      pjmedia_transport_info_init(&tp_info);
      pjmedia_transport_get_info(media_tp, &tp_info);

      for (j = 0; j < tp_info.specific_info_cnt; ++j) {
          if (tp_info.spc_info[j].type == PJMEDIA_TRANSPORT_TYPE_SRTP) {
              srtp_info = (pjmedia_srtp_info*) tp_info.spc_info[j].buffer;
              break;
          }
      }

      if (srtp_info && srtp_info->active) {
          /* srtp_info->tx_policy.name is the negotiated crypto-suite. */
          /* srtp_info->use / peer_use show the policy and what the
           * peer asked for. */
      }

  (The same iteration is what PJSUA-LIB's own dump uses —
  :sourcedir:`pjsip/src/pjsua-lib/pjsua_dump.c`.)


PJSUA-LIB equivalents
---------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - PJSUA2
     - PJSUA-LIB
   * - :cpp:any:`pj::AccountMediaConfig::srtpUse`
     - :cpp:any:`pjsua_acc_config::use_srtp`
   * - :cpp:any:`pj::AccountMediaConfig::srtpSecureSignaling`
     - :cpp:any:`pjsua_acc_config::srtp_secure_signaling`
   * - :cpp:any:`pj::AccountMediaConfig::srtpOpt`
       (:cpp:any:`pj::SrtpOpt`)
     - :cpp:any:`pjsua_acc_config::srtp_opt`
       (:cpp:any:`pjsua_srtp_opt`)
   * - ``SrtpOpt::keyings`` (``IntVector``)
     - ``pjsua_srtp_opt::keying[]`` / ``keying_count``
   * - ``SrtpOpt::cryptos`` (:cpp:any:`pj::SrtpCryptoVector`)
     - ``pjsua_srtp_opt::crypto[]`` / ``crypto_count``
   * - (not exposed)
     - :cpp:any:`pjmedia_transport_srtp_create`,
       :cpp:any:`pjmedia_transport_srtp_dtls_start_nego`,
       :cpp:any:`pjmedia_transport_srtp_dtls_get_fingerprint`
       (PJMEDIA direct API)


References
----------

- SRTP: :rfc:`3711`
- SDES keying: :rfc:`4568`
- DTLS-SRTP framework: :rfc:`5763`
- DTLS-SRTP extension: :rfc:`5764`
- TLS-Exporter: :rfc:`5705`
- DTLS-SRTP enabled (initial): :pr:`2096`
- DTLS-SRTP for RTCP: :pr:`3571`
- DTLS-SRTP restricted to OpenSSL: :pr:`4239`
- ClientHello source-address check: :pr:`4261`
- libsrtp: https://github.com/cisco/libsrtp

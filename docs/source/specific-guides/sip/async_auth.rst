Asynchronous SIP Authentication
=========================================

.. contents:: Table of Contents
    :depth: 3

Available since 2.17 (:pr:`4816`).


Overview
------------------
By default, PJSIP handles 401/407 authentication challenges synchronously:
when a challenge arrives, the library looks up pre-configured credentials,
builds the Authorization header, and resends the request — all within the
transaction callback.

The **asynchronous authentication** API lets applications intercept the
challenge and supply credentials later. This is useful when credentials are
not available immediately, for example:

- Prompting the user for a password
- Fetching credentials from a vault or keychain
- Performing an OAuth token exchange
- Applying rate-limiting or policy checks before retrying

The feature is available at three API levels:

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Layer
     - Entry Point
     - Async Mechanism
   * - PJSIP
     - :cpp:any:`pjsip_auth_clt_async_configure()`
     - Token-based callback; call :cpp:any:`pjsip_auth_clt_async_send_req()`
       or :cpp:any:`pjsip_auth_clt_async_abandon()`
   * - PJSUA-LIB
     - ``pjsua_callback.on_auth_challenge``
     - Set ``param->handled = PJ_TRUE``, then call PJSIP async APIs
   * - PJSUA2
     - ``Account::onAuthChallenge()``
     - Call ``challenge.defer()`` to get a heap-allocated handle, then
       ``respond()`` or ``abandon()`` later

The feature is **fully backward-compatible**. If the callback is not set or
does not handle the challenge, the library falls back to the existing
synchronous credential-based authentication.


PJSUA2 API
------------------

Implement the virtual method :cpp:any:`pj::Account::onAuthChallenge()`.
Inside the callback you can:

1. **Respond immediately** with the account's current credentials.
2. **Respond with new credentials** supplied at challenge time.
3. **Defer** the decision and respond (or abandon) asynchronously.

Responding immediately
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c++

   void onAuthChallenge(OnAuthChallengeParam &prm) override
   {
       // Respond using credentials already configured on the account
       prm.challenge.respond();
   }

Responding with new credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c++

   void onAuthChallenge(OnAuthChallengeParam &prm) override
   {
       AuthCredInfoVector creds;
       creds.push_back(AuthCredInfo("digest", "*",
                                    "alice", 0, "secret123"));
       prm.challenge.respond(creds);
   }

.. warning::

   ``respond(creds)`` sets the credentials on the account's shared auth
   session, **permanently replacing** the account's credentials. All
   subsequent authentication for the account will use these new credentials.
   If you only want to authenticate a single request, prefer the PJSIP-level
   API where you can set credentials on a non-shared session.

Deferring the response
^^^^^^^^^^^^^^^^^^^^^^

``defer()`` returns a heap-allocated ``AuthChallenge*`` that you own.
Pass it to another thread, a timer, or any asynchronous workflow, then call
``respond()`` or ``abandon()`` when ready.

.. code-block:: c++

   void onAuthChallenge(OnAuthChallengeParam &prm) override
   {
       AuthChallenge *deferred = prm.challenge.defer();

       // Hand off to async credential-fetching logic.
       // When credentials are available:
       AuthCredInfoVector creds;
       creds.push_back(AuthCredInfo("digest", "*",
                                    "alice", 0, "secret123"));
       deferred->respond(creds);
       delete deferred;
   }

.. note::

   On a deferred ``AuthChallenge``, ``respond()``, ``abandon()``, and
   destruction all call into PJSIP and therefore **must be invoked from a
   pjlib-registered thread**. If a worker thread fetches credentials,
   register it with :cpp:any:`pj_thread_register()` (or hand the result
   back to a registered thread) before calling ``respond()``/``abandon()``.

.. warning::

   If ``respond()`` or ``abandon()`` is never called, the destructor will
   auto-abandon the challenge — but in garbage-collected languages (Java,
   Python) the destructor/finalizer typically runs on an unregistered GC
   thread, which will trip PJLIB thread-registration assertions. Always
   explicitly call ``respond()``, ``abandon()``, or ``delete`` on the
   deferred object from a pjlib-registered thread. Do **not** rely on GC
   to clean it up. See :ref:`gc_problems`.


Python example
^^^^^^^^^^^^^^

.. code-block:: python

   import pjsua2 as pj

   class MyAccount(pj.Account):
       def onAuthChallenge(self, prm):
           deferred = prm.challenge.defer()

           # ... fetch credentials asynchronously (from a pjlib-registered
           # thread, or marshal the result back to one) ...

           creds = pj.AuthCredInfoVector()
           creds.append(pj.AuthCredInfo("digest", "*",
                                        "alice", 0, "secret123"))
           deferred.respond(creds)
           # Must explicitly consume the deferred object — do not rely on
           # Python GC to abandon it (finalizer runs on an unregistered
           # thread). See the GC warning above.


PJSUA-LIB API
------------------

Set the ``on_auth_challenge`` callback in :cpp:any:`pjsua_callback`:

.. code-block:: c

   pjsua_config cfg;
   pjsua_config_default(&cfg);
   cfg.cb.on_auth_challenge = &on_auth_challenge;

The callback receives a ``pjsua_on_auth_challenge_param`` with the
auth session, opaque token, original request (``tdata``), and the
challenge response (``rdata``). To handle asynchronously:

1. Clone ``rdata`` and add a reference to ``tdata`` (they become invalid
   after the callback returns).
2. Set ``param->handled = PJ_TRUE``.
3. Later, call :cpp:any:`pjsip_auth_clt_reinit_req()` to build the
   authenticated request, then :cpp:any:`pjsip_auth_clt_async_send_req()`
   to send it (or :cpp:any:`pjsip_auth_clt_async_abandon()` to give up).

.. code-block:: c

   struct auth_ctx {
       pjsip_auth_clt_sess *auth_sess;
       void                *token;
       pjsip_tx_data       *tdata;
       pjsip_rx_data       *rdata_clone;
       pjsua_acc_id         acc_id;
   };

   /* Timer callback — runs after credentials are available */
   static void on_creds_ready(pj_timer_heap_t *th, pj_timer_entry *te)
   {
       struct auth_ctx *ctx = (struct auth_ctx *)te->user_data;
       pjsip_cred_info cred;
       pjsip_tx_data *new_req = NULL;
       pj_status_t status;

       PJ_UNUSED_ARG(th);

       /* Set credentials on the auth session */
       pj_bzero(&cred, sizeof(cred));
       cred.scheme    = pj_str("digest");
       cred.realm     = pj_str("*");
       cred.username  = pj_str("alice");
       cred.data      = pj_str("secret123");
       cred.data_type = PJSIP_CRED_DATA_PLAIN_PASSWD;
       pjsip_auth_clt_set_credentials(ctx->auth_sess, 1, &cred);

       /* Build and send the authenticated request */
       status = pjsip_auth_clt_reinit_req(ctx->auth_sess,
                                          ctx->rdata_clone,
                                          ctx->tdata, &new_req);
       if (status == PJ_SUCCESS && new_req) {
           pjsip_auth_clt_async_send_req(ctx->auth_sess,
                                         ctx->token, new_req);
       } else {
           pjsip_auth_clt_async_abandon(ctx->auth_sess, ctx->token);
       }

       pjsip_rx_data_free_cloned(ctx->rdata_clone);
       pjsip_tx_data_dec_ref(ctx->tdata);
       free(ctx);
   }

   static void on_auth_challenge(pjsua_on_auth_challenge_param *prm)
   {
       struct auth_ctx *ctx;
       pj_timer_entry *te;
       pj_time_val delay = {1, 0};

       ctx = (struct auth_ctx *)malloc(sizeof(*ctx));
       ctx->auth_sess = prm->auth_sess;
       ctx->token     = prm->token;
       ctx->tdata     = prm->tdata;
       ctx->acc_id    = prm->acc_id;
       pjsip_rx_data_clone(prm->rdata, 0, &ctx->rdata_clone);
       pjsip_tx_data_add_ref(ctx->tdata);

       prm->handled = PJ_TRUE;

       te = (pj_timer_entry *)malloc(sizeof(*te));
       pj_timer_entry_init(te, 0, ctx, &on_creds_ready);
       pjsip_endpt_schedule_timer(pjsua_get_pjsip_endpt(), te, &delay);
   }


PJSIP API
------------------

At the lowest level, configure async auth on any
:cpp:any:`pjsip_auth_clt_sess`:

.. code-block:: c

   pjsip_auth_clt_async_setting async_opt;
   pj_bzero(&async_opt, sizeof(async_opt));
   async_opt.cb        = &my_on_challenge;
   async_opt.user_data = my_context;
   pjsip_auth_clt_async_configure(&auth_sess, &async_opt);

The callback signature:

.. code-block:: c

   static pj_bool_t my_on_challenge(
       pjsip_auth_clt_sess *sess,
       void *token,
       const pjsip_auth_clt_async_on_chal_param *param)
   {
       /* Return PJ_TRUE to handle the challenge asynchronously.
        * Later call pjsip_auth_clt_async_send_req() or
        * pjsip_auth_clt_async_abandon().
        *
        * Return PJ_FALSE to fall back to synchronous auth.
        */
   }

The opaque ``token`` carries per-challenge state (allocated from the
transaction pool with a group-lock reference to keep the transaction alive).
After calling ``async_send_req()`` or ``async_abandon()``, the token is
invalidated and must not be reused.


Design Notes
------------------

Token lifetime
^^^^^^^^^^^^^^
Each challenge allocates a token from the transaction's pool and takes a
group-lock reference on the transaction. This keeps the transaction alive
until the application calls ``async_send_req()`` or ``async_abandon()``,
at which point the reference is released and the token is invalidated.

Sync fallback
^^^^^^^^^^^^^
If the callback returns ``PJ_FALSE`` (or is not set), the library falls
through to the existing synchronous ``pjsip_auth_clt_reinit_req()`` path.
This makes the feature fully backward-compatible.

Shared auth session
^^^^^^^^^^^^^^^^^^^
``pjsua_acc_config.use_shared_auth`` is **disabled by default**. When
enabled, all modules for an account (REGISTER, SUBSCRIBE, PUBLISH, etc.)
share a single auth session, so credentials set on it are available to all
modules and redundant challenge round-trips are avoided.

Regardless of this setting, when ``on_auth_challenge`` is configured the
account's shared auth session is still used as the session handed to the
callback — the async challenge hook works with or without
``use_shared_auth``. The flag only controls whether the other modules
(registration, presence, IM, etc.) reuse that same session for their
outgoing requests.

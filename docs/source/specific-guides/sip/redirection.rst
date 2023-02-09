Processing redirection (3xx) response
===================================================

.. note::

   This article is about processing SIP redirect (3xx)
   response in outgoing calls, and not about sending redirection/3xx
   response. Sending 3xx response in PJSUA-LIB can be accomplished by calling
   :cpp:any:`pjsua_call_hangup()` and with the new targets in Contact header in
   :cpp:any:`pjsua_msg_data` parameter.


.. contents:: Table of Contents
    :depth: 3


Features
----------

- It is implemented all the way from PJSIP to PJSUA2 API level, 
  to allow the usage on non-PJSUA-LIB based applications.
- Handles multiple targets in the 3xx response (and targets that are 
  returned in 3xx response of subsequent INVITE).
- Allows application to accept or reject the redirection request on a per-target basis.
- Allows application to defer the decision to accept or reject the
  redirection request, for example, to ask for user confirmation in the UI.
- Remembers which targets have been sent INVITE and not retry the INVITE 
  to these targets 
- Prioritize targets based on the q-value
- Allows keeping or replacing the To URI in the subsequent INVITE requests,
  while keeping the same From, and Call-ID as the original INVITE. 


Redirection with PJSIP API
--------------------------------
Application **MUST** implement :cpp:any:`pjsip_inv_callback::on_redirected` callback 
to handle redirection. If this callback is not implemented, the invite session will be
disconnected upon receipt of 3xx response.

Redirection handling is controlled by the return value of this callback. See
:cpp:any:`pjsip_redirect_op` for possible actions.

If application wishes to defer the redirection decision, it must return from the
callback with :cpp:any:`PJSIP_REDIRECT_PENDING` and call 
:cpp:any:`pjsip_inv_process_redirect()` once it has decided
how to process the redirection.

The redirection usage scenarios will be explained below.

Accept redirection to this target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return :cpp:any:`PJSIP_REDIRECT_ACCEPT` from the callback to accept the
redirection to this target. And INVITE session will be sent immediately
to the target.

Alternatively :cpp:any:`PJSIP_REDIRECT_ACCEPT_REPLACE` can be returned
to accept the redirection to the current target and 
replace the To header in the INVITE request with the current target.

Reject redirection to this target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return :cpp:any:`PJSIP_REDIRECT_REJECT` from the callback to reject the
redirection to this target. If there is another target to try, then the
callback will be called again with this next target, otherwise the
invite session will be disconnected immediately.

Stop redirection
^^^^^^^^^^^^^^^^

Return :cpp:any:`PJSIP_REDIRECT_STOP` from the callback to stop the redirection
process and disconnect the call immediately, regardless of whether there
are more targets to try.

Defer the Decision
^^^^^^^^^^^^^^^^^^

Return :cpp:any:`PJSIP_REDIRECT_PENDING` from the callback to tell the invite
session that a decision cannot be made that this time (for example to
ask for user approval), and the application will notify the invite
session about the decision later.

Once the application gets the user approval (or disapproval), it
**MUST** call :cpp:any:`pjsip_inv_process_redirect()` function to notify the
session about the decision. It may accept or reject the target, or stop
the redirection altogether by setting the appropriate value to the *cmd*
argument. It must not set :cpp:any:`PJSIP_REDIRECT_PENDING` to this argument.

Failure to call :cpp:any:`pjsip_inv_process_redirect()` will cause the invite
session to be kept alive indefinitely until the library is shutdown.

When the :cpp:any:`pjsip_inv_process_redirect()` function is called for the
next target in the context of this function (that is when this function
is called with reject command and next target is selected, hence the
callback is called), the event (*e*) argument passed to this function
will be passed down to the callback. And similarly when the disconnect
callback is called. If NULL is given to the event argument of this
function, this function will create a :cpp:any:`PJSIP_EVENT_USER` event with
NULL values, to be passed to the callbacks.

Because of this, application MUST be prepared to handle these type of
events in both the :cpp:any:`pjsip_inv_callback::on_redirected` and 
:cpp:any:`pjsip_inv_callback::on_state_changed`
callbacks. Traditionally only :cpp:any:`PJSIP_EVENT_TSX_STATE` event is passed
to :cpp:any:`pjsip_inv_callback::on_state_changed` callback.

Redirection with PJSUA-LIB API
--------------------------------------------
Use the :cpp:any:`pjsua_callback::on_call_redirected` callback and
:cpp:any:`pjsua_call_process_redirect()` API to handle redirection.

See the PJSIP section above on how to use this feature.

Redirection with PJSUA2 API
--------------------------------------------
Use the :cpp:any:`pj::Call::onCallRedirected` and
:cpp:any:`pj::Call::processRedirect()` methods to handle redirection.

See the PJSIP section above on how to use this feature.

Redirection in *pjsua* application
-----------------------------------

Call redirection handling in *pjsua* is as follows:

-  Use command line argument ``--accept-redirect``, with valid
   values:

   -  ``0``: reject/stop,
   -  ``1``: follow automatically (default),
   -  ``2``: ask

-  the default behavior is to follow redirection automatically
-  when ``--accept-redirect`` is set to 2 (ask), user can enter ``Ra``,
   ``Rr``, or ``Rd`` to accept, reject, or stop/disconnect the redirection.

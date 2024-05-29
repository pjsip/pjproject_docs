DTMF
=========================================

.. contents:: Table of Contents
    :depth: 2


Overview
------------------
:doc:`PJSUA2 </api/pjsua2/index>` and :doc:`PJSUA-LIB </api/pjsua-lib/index>` 
support sending DTMF digits as inband tone, RTP events (:rfc:`4733`/:rfc:`2833`), 
or SIP INFO. On the receiving side, the libraries support reporting DTMF digits sent as
RTP events (:rfc:`4733`/:rfc:`2833`) and SIP INFO. Note that detection of inband DTMF tone
is currently not implemented.

PJSUA-LIB (and inherently PJSUA2) will only send RFC 2833 DTMF if remote party
has indicated its capability to accept RFC 2833 events in its SDP. This is done by putting 
this line in the SDP:

::

   a=rtpmap:101 telephone-event/8000

Without receiving this capability indication, PJSIP will refuse to send RFC 2833 event, 
and :cpp:any:`pj::Call::sendDtmf()`, :cpp:any:`pjsua_call_send_dtmf()`,
:cpp:any:`pjsua_call_dial_dtmf()` or :cpp:any:`pjmedia_session_dial_dtmf()` or 
:cpp:any:`pjmedia_stream_dial_dtmf()` will return error code :c:macro:`PJMEDIA_RTP_EREMNORFC2833`.

Communicating DTMF using SIP INFO is considered as proprietary and have not 
been standardized (see :rfc:`6086#section-2`). This mechanism is also very expensive
in terms of network resources used. Use this mechanism with care. Please see
ticket :issue:`2036` for more information.


PJSUA2 API
------------------
Send DTMF with :cpp:any:`pj::Call::sendDtmf()` method, specifying the method
in :cpp:any:`pj::CallSendDtmfParam::method` field.

Incoming DTMF will be reported in :cpp:any:`pj::Call::onDtmfDigit` callback.

PJSUA API
----------------
Send DTMF with :cpp:any:`pjsua_call_send_dtmf()` function, specifying the method
in :cpp:any:`pjsua_call_send_dtmf_param::method` field.

Incoming DTMF digits will be reported in :cpp:any:`pjsua_callback::on_dtmf_digit2` callback.

Sending inband DTMF tones
--------------------------
Below are steps to send inband DTMF tones:

#. Once the call is established, create an instance of 
   :doc:`Multi-frequency/DTMF Tone Generator </api/generated/pjmedia/group/group__PJMEDIA__MF__DTMF__TONE__GENERATOR>`.
#. Register this tone generator to pjsua's conference bridge with :cpp:any:`pjsua_conf_add_port()`.
#. *Connect* the tone generator to the call, with :cpp:any:`pjsua_conf_connect()`.
#. Now instruct the tone generator to *play* some DTMF digits with :cpp:any:`pjmedia_tonegen_play_digits()`. 
   The digits then will be streamed to the call, and remote endpoint should receive the DTMF tone inband.

Below is the snippet to do it:

.. code-block:: c

   struct my_call_data
   {
        pj_pool_t          *pool;
        pjmedia_port       *tonegen;
        pjsua_conf_port_id  toneslot;
   };

   struct my_call_data *call_init_tonegen(pjsua_call_id call_id)
   {
        pj_pool_t *pool;
        struct my_call_data *cd;
        pjsua_call_info ci;

        pool = pjsua_pool_create("mycall", 512, 512);
        cd = PJ_POOL_ZALLOC_T(pool, struct my_call_data);
        cd->pool = pool;

        pjmedia_tonegen_create(cd->pool, 8000, 1, 160, 16, 0, &cd->tonegen);
        pjsua_conf_add_port(cd->pool, cd->tonegen, &cd->toneslot);

        pjsua_call_get_info(call_id, &ci);
        pjsua_conf_connect(cd->toneslot, ci.conf_slot);

        pjsua_call_set_user_data(call_id, (void*) cd);

        return cd;
   }

   void call_play_digit(pjsua_call_id call_id, const char *digits)
   {
        pjmedia_tone_digit d[16];
        unsigned i, count = strlen(digits);
        struct my_call_data *cd;

        cd = (struct my_call_data*) pjsua_call_get_user_data(call_id);
        if (!cd)
            cd = call_init_tonegen(call_id);

        if (count > PJ_ARRAY_SIZE(d))
            count = PJ_ARRAY_SIZE(d);

        pj_bzero(d, sizeof(d));
        for (i=0; i<count; ++i) {
           d[i].digit = digits[i];
           d[i].on_msec = 100;
           d[i].off_msec = 200;
           d[i].volume = 0;
        }

        pjmedia_tonegen_play_digits(cd->tonegen, count, d, 0);
   }

   void call_deinit_tonegen(pjsua_call_id call_id)
   {
        struct my_call_data *cd;

        cd = (struct my_call_data*) pjsua_call_get_user_data(call_id);
        if (!cd)
           return;

        pjsua_conf_remove_port(cd->toneslot);
        pjmedia_port_destroy(cd->tonegen);
        pj_pool_release(cd->pool);

        pjsua_call_set_user_data(call_id, NULL);
   }

The resources that were allocated above must be released once the call is disconnected,
by implementing this in :cpp:any:`pjsua_callback::on_call_state` callback:

.. code-block:: c

   static void on_call_state(pjsua_call_id call_id, pjsip_event *e)
   {
        pjsua_call_info call_info;

        pjsua_call_get_info(call_id, &call_info);

        if (call_info.state == PJSIP_INV_STATE_DISCONNECTED) {
           call_deinit_tonegen(call_id);
        }
   }

With the above snippet, call ``call_play_digit()`` send inband DTMF digit to remote party.

Implementing inband DTMF detector
-------------------------------------
Currently PJMEDIA lacks built-in tone detection routine. If tone detection routine is available,
it should be straightforward to integrate it to the framework:

#. Wrap the routine as :doc:`PJMEDIA Port </api/generated/pjmedia/group/group__PJMEDIA__PORT>`
   so that it can be plugged to the media framework. The implementation would be similar to
   :doc:`WAV recorder </api/generated/pjmedia/group/group__PJMEDIA__FILE__REC>` media port
   (:source:`pjmedia/src/pjmedia/wav_writer.c`), but instead of writing to WAV file, it would
   monitor the audio signal for tone and call some callback when a tone is detected.
#. Once the tone detector media port is implementation, add this media port to the conference bridge 
   with :cpp:any:`pjsua_conf_add_port()`, and connect the audio source to your tone detector
   with :cpp:any:`pjsua_conf_connect()`.

/*
 * Copyright (C) 2008-2026 Teluu Inc. (http://www.teluu.com)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

/**
 * @file mod_contact_tp_compat.c
 * @brief Application-level SIP module for transport parameter
 *        compatibility in remote Contact header.
 *
 * Problem:
 *   Some PBXes/UAs omit the ";transport=tcp" parameter from the
 *   Contact header in SIP responses, even when the dialog was
 *   established over TCP. When PJSIP's dialog layer freezes the
 *   remote target from this Contact, subsequent in-dialog requests
 *   (re-INVITE, re-SUBSCRIBE, etc.) resolve to UDP and fail with
 *   PJSIP_ETPNOTSUITABLE.
 *
 *   A related scenario occurs when a B2BUA/carrier returns a Contact
 *   with an explicit ";transport=udp" even though the dialog was
 *   established over TCP (e.g. the B2BUA rewrites the Contact from
 *   its outbound leg). This also causes PJSIP_ETPNOTSUITABLE when
 *   sending PRACK or subsequent in-dialog requests.
 *
 * Standard behavior:
 *   PJSIP's dialog layer follows RFC 3261 Section 12.1.2: the remote
 *   target is set from the Contact header in the response, and the
 *   transport is resolved from that URI per RFC 3263. A Contact
 *   without ";transport=tcp" correctly resolves to UDP per the
 *   standard. This is the intended library behavior and will not be
 *   changed.
 *
 * Workaround:
 *   This application-level module works around non-compliant remote
 *   implementations by patching the Contact URI before the dialog
 *   layer processes it. It runs at a priority between the transaction
 *   layer and the dialog/UA layer, inspecting incoming 1xx/2xx SIP
 *   responses. If the response arrived over a reliable transport
 *   (TCP/TLS), it patches the Contact URI's transport parameter before
 *   the dialog layer freezes it.
 *
 *   Two modes are supported:
 *
 *   - MOD_CONTACT_TP_COMPAT_ADD_ONLY (default):
 *     Only adds the transport parameter when the Contact URI has none.
 *     This is the safer option — it does not override an explicit
 *     transport parameter set by the remote party.
 *
 *   - MOD_CONTACT_TP_COMPAT_OVERRIDE:
 *     Also overrides a mismatched transport parameter (e.g. replaces
 *     ";transport=udp" with ";transport=tcp" when the response arrived
 *     over TCP). Use this when a B2BUA or carrier is known to send
 *     incorrect transport parameters in the Contact. This is more
 *     aggressive and may not be appropriate for all deployments.
 *
 * Risks:
 *   This module modifies the Contact URI in incoming responses before
 *   any other dialog-level processing. Potential side effects include:
 *
 *   - Legitimate multi-transport topologies may break. If the remote
 *     party intentionally uses a different transport for the Contact
 *     (e.g. signaling arrives over TCP but the Contact points to a
 *     UDP-only endpoint for subsequent requests), this module will
 *     incorrectly force TCP.
 *
 *   - In OVERRIDE mode, the module silently discards the remote
 *     party's explicit transport preference. This can mask network
 *     configuration issues and make debugging harder.
 *
 *   - The module applies globally to all responses on the endpoint.
 *     There is no per-account or per-dialog granularity. If only
 *     certain peers are non-compliant, the module will still patch
 *     responses from compliant peers (though this is harmless when
 *     the Contact already matches the transport).
 *
 *   Use this module only when interoperability with a specific
 *   non-compliant implementation requires it.
 *
 * Usage — PJSUA-LIB (C):
 * @code
 *   #include "mod_contact_tp_compat.c"
 *
 *   // After pjsua_init(), before pjsua_start():
 *
 *   // Default mode: only add missing transport parameter
 *   mod_contact_tp_compat_init(pjsua_get_pjsip_endpt(),
 *                           MOD_CONTACT_TP_COMPAT_ADD_ONLY);
 *
 *   // Or: also override mismatched transport parameter
 *   mod_contact_tp_compat_init(pjsua_get_pjsip_endpt(),
 *                           MOD_CONTACT_TP_COMPAT_OVERRIDE);
 * @endcode
 *
 * Usage — PJSUA2 (C++):
 * @code
 *   extern "C" {
 *   #include "mod_contact_tp_compat.c"
 *   }
 *
 *   // After Endpoint::libInit(), before Endpoint::libStart():
 *   mod_contact_tp_compat_init(pjsua_get_pjsip_endpt(),
 *                           MOD_CONTACT_TP_COMPAT_ADD_ONLY);
 * @endcode
 */

#include <pjsip.h>
#include <pj/log.h>

#define THIS_FILE   "mod_contact_tp_compat.c"


/**
 * Module operation mode.
 */
typedef enum mod_contact_tp_compat_mode
{
    /**
     * Only add transport parameter when the Contact URI has none.
     * A Contact with an explicit ";transport=udp" will NOT be changed.
     * This is the safe default.
     */
    MOD_CONTACT_TP_COMPAT_ADD_ONLY,

    /**
     * Also override a mismatched transport parameter. For example,
     * if the response arrived over TCP but the Contact has
     * ";transport=udp", replace it with ";transport=tcp".
     *
     * Use this when a B2BUA or carrier is known to send incorrect
     * transport parameters in the Contact.
     */
    MOD_CONTACT_TP_COMPAT_OVERRIDE

} mod_contact_tp_compat_mode;


/* Module state */
static mod_contact_tp_compat_mode fix_mode = MOD_CONTACT_TP_COMPAT_ADD_ONLY;

static pj_bool_t on_rx_response(pjsip_rx_data *rdata);

static pjsip_module mod_contact_tp_compat =
{
    NULL, NULL,                         /* prev, next                   */
    { "mod-contact-tp-compat", 21 },    /* Name                         */
    -1,                                 /* Id                           */
    PJSIP_MOD_PRIORITY_TSX_LAYER + 1,  /* Priority: after tsx,         */
                                        /*   before dialog/UA layer     */
    NULL,                               /* load()                       */
    NULL,                               /* start()                      */
    NULL,                               /* stop()                       */
    NULL,                               /* unload()                     */
    NULL,                               /* on_rx_request()              */
    &on_rx_response,                    /* on_rx_response()             */
    NULL,                               /* on_tx_request()              */
    NULL,                               /* on_tx_response()             */
    NULL,                               /* on_tsx_state()               */
};


/* Get the transport parameter string for the given transport type.
 * Returns NULL if no patching is needed (e.g. UDP or unknown type).
 */
static const char* get_tp_param(pjsip_transport_type_e tp_type)
{
    /* Strip IPv6 flag to get the base type. */
    pjsip_transport_type_e base;
    base = (pjsip_transport_type_e)(tp_type & ~PJSIP_TRANSPORT_IPV6);

    switch (base) {
    case PJSIP_TRANSPORT_TCP:
        return "tcp";
    case PJSIP_TRANSPORT_TLS:
        return "tls";
    default:
        return NULL;
    }
}


static pj_bool_t on_rx_response(pjsip_rx_data *rdata)
{
    pjsip_contact_hdr *contact;
    pjsip_sip_uri *uri;
    const char *tp_param;
    pjsip_transport_type_e tp_type;

    /* Only process 1xx/2xx responses. The dialog layer updates
     * dlg->target from Contact on:
     *  - 1xx (101-199): provisional, used as PRACK target
     *  - 2xx: freezes route set and remote target
     *  - target-refresh in established dialogs
     * Failure responses (>= 300) never update dlg->target.
     */
    if (rdata->msg_info.msg->type != PJSIP_RESPONSE_MSG ||
        rdata->msg_info.msg->line.status.code >= 300)
    {
        return PJ_FALSE;
    }

    /* Check the transport type the response arrived on. */
    tp_type = rdata->tp_info.transport->key.type;
    tp_param = get_tp_param(tp_type);
    if (!tp_param) {
        /* Response arrived on UDP or other non-reliable transport,
         * no patching needed.
         */
        return PJ_FALSE;
    }

    /* Find Contact header. */
    contact = (pjsip_contact_hdr*)
              pjsip_msg_find_hdr(rdata->msg_info.msg,
                                 PJSIP_H_CONTACT, NULL);
    if (!contact || !contact->uri)
        return PJ_FALSE;

    /* Only patch sip: URIs (sips: already implies secure transport). */
    if (!PJSIP_URI_SCHEME_IS_SIP(contact->uri))
        return PJ_FALSE;

    uri = (pjsip_sip_uri*)pjsip_uri_get_uri(contact->uri);

    if (uri->transport_param.slen == 0) {
        /* No transport parameter — add one. */
        pj_strdup2(rdata->tp_info.pool, &uri->transport_param, tp_param);

        PJ_LOG(4, (THIS_FILE,
                   "Added missing Contact ;transport=%s "
                   "(response %d %.*s)",
                   tp_param,
                   rdata->msg_info.msg->line.status.code,
                   (int)rdata->msg_info.msg->line.status.reason.slen,
                   rdata->msg_info.msg->line.status.reason.ptr));

    } else if (fix_mode == MOD_CONTACT_TP_COMPAT_OVERRIDE &&
               pj_stricmp2(&uri->transport_param, tp_param) != 0)
    {
        /* Transport parameter present but mismatched, and override
         * mode is enabled — replace it.
         */
        PJ_LOG(4, (THIS_FILE,
                   "Overriding Contact ;transport=%.*s -> %s "
                   "(response %d %.*s)",
                   (int)uri->transport_param.slen,
                   uri->transport_param.ptr,
                   tp_param,
                   rdata->msg_info.msg->line.status.code,
                   (int)rdata->msg_info.msg->line.status.reason.slen,
                   rdata->msg_info.msg->line.status.reason.ptr));

        pj_strdup2(rdata->tp_info.pool, &uri->transport_param, tp_param);

    } else {
        /* Transport parameter already matches, or override is
         * disabled — nothing to do.
         */
        return PJ_FALSE;
    }

    /* Don't consume -- let dialog layer process the patched response. */
    return PJ_FALSE;
}


/**
 * Initialize and register the Contact transport compatibility module.
 *
 * Call this after the SIP endpoint is created (e.g. after pjsua_init())
 * and before making or receiving calls.
 *
 * @param endpt     The SIP endpoint instance.
 * @param mode      Operation mode:
 *                  - MOD_CONTACT_TP_COMPAT_ADD_ONLY: only add transport
 *                    parameter when the Contact URI has none.
 *                  - MOD_CONTACT_TP_COMPAT_OVERRIDE: also replace a
 *                    mismatched transport parameter.
 *
 * @return          PJ_SUCCESS on success.
 */
static pj_status_t mod_contact_tp_compat_init(pjsip_endpoint *endpt,
                                           mod_contact_tp_compat_mode mode)
{
    fix_mode = mode;
    return pjsip_endpt_register_module(endpt, &mod_contact_tp_compat);
}

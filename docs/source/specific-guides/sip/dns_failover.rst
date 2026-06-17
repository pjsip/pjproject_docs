Implement DNS SRV failover
=========================================
Our DNS SRV failover support is only limited to TCP (or TLS)
:cpp:any:`connect()` failure, which in this case pjsip will automatically
retries the next server. But even then, there is no mechanism to flag that
a server has been failing, which means that the next request may try
the same server again and triggering the failover again.

What we've been suggesting is to implement the failover mechanism in the
application layer. In this case, the application queries the list of available
servers either with :cpp:any:`gethostbyname()`, DNS SRV, or by other means.
It then specifies which server to use by putting the IP address as
proxy parameter (i.e. Route header) in the account config. The mechanism to
test the wellness of a server and when to initiate the failover is totally
controlled by the application. The application can change which server to
use by changing the account proxy setting with :cpp:any:`pjsua_acc_modify()`.

.. warning::

   **This IP-in-Route approach does not work for TLS.** When an IP address is
   put in the proxy/Route URI, PJSIP uses that same value both as the TLS
   ClientHello SNI and as the name matched against the server certificate
   (CN/subjectAltName). Sending an IP literal as SNI is invalid per RFC 6066,
   and the certificate name check typically fails because certificates usually
   carry the server *hostname*, not its IP (unless the cert includes an iPAddress
   subjectAltName entry). The result is a failed handshake or a rejected certificate.

   The underlying reason is that the TLS transport derives the SNI and the
   certificate-validation name from a single field (the next-hop URI host),
   so overriding the connect address with an IP also overrides the TLS name.
   For UDP and TCP there is no such name check, so the IP-in-Route approach
   above works as-is.

Failover with TLS
-----------------------------------------
To do application-controlled failover over TLS, keep the **hostname** in the
proxy/Route URI (so SNI and certificate validation use the correct name) and
select the actual server *address* separately. A PJSUA application can do this
with an external resolver (current releases) or with server affinity (the
release after 2.17); an application working directly at the PJSIP layer can use
the transport API.

Using an external resolver (PJSUA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Register an external resolver with :cpp:any:`pjsip_endpt_set_ext_resolver()`.
Because the next-hop hostname is recorded before resolution runs, ``dest_info.name``
stays the hostname — so SNI and certificate validation remain correct — while
your resolver callback decides which address(es) to return for that hostname,
in what order, and which failing server to exclude. PJSIP then uses the
returned addresses (and retries the next one on connect failure). This works
with PJSUA on current releases and keeps all failover policy in the application.

The resolver is just a single ``resolve`` callback — typically a thin wrapper
over ``pj_getaddrinfo()`` (or your own server table) that returns the addresses
in the order your failover logic prefers::

    /* Turn the next-hop hostname into an address list, in your preferred
     * order. dest_info.name already holds the hostname, so SNI/cert are
     * unaffected by what is returned here.
     */
    static void my_resolve(pjsip_resolver_t *res, pj_pool_t *pool,
                           const pjsip_host_info *target, void *token,
                           pjsip_resolver_callback *cb)
    {
        pjsip_server_addresses svr;
        pj_addrinfo ai[8];
        unsigned i, cnt = PJ_ARRAY_SIZE(ai);
        pj_status_t status;

        pj_bzero(&svr, sizeof(svr));

        /* Resolve the hostname (getaddrinfo/DNS SRV), or consult your own
         * server table here and drop/reorder the servers you think are down.
         */
        status = pj_getaddrinfo(pj_AF_UNSPEC(), &target->addr.host, &cnt, ai);

        for (i = 0; i < cnt; ++i) {
            pj_sockaddr_cp(&svr.entry[i].addr, &ai[i].ai_addr);
            pj_sockaddr_set_port(&svr.entry[i].addr,
                                 (pj_uint16_t)(target->addr.port ?
                                               target->addr.port : 5061));
            svr.entry[i].addr_len = pj_sockaddr_get_len(&svr.entry[i].addr);
            svr.entry[i].type     = target->type;   /* preserve transport (TLS) */
            svr.entry[i].name     = target->addr.host;
        }
        svr.count = cnt;

        cb(status, token, &svr);   /* hand the ordered list back to PJSIP */
    }

    /* Install once, e.g. right after pjsua_init(). */
    pjsip_ext_resolver ext;
    pj_bzero(&ext, sizeof(ext));
    ext.resolve = &my_resolve;
    pjsip_endpt_set_ext_resolver(pjsua_get_pjsip_endpt(), &ext);

.. note::

   The callback does not have to do the lookup itself with ``pj_getaddrinfo()``.
   It can instead drive PJSIP's built-in DNS resolver — obtained via
   :cpp:any:`pjsip_endpt_get_resolver()` (a :cpp:any:`pj_dns_resolver`) — to
   perform the actual SRV/A resolution, then reorder or filter the results
   before calling ``cb``. That keeps PJSIP's DNS handling (SRV priority/weight,
   caching) while still letting the application control failover order. Note the
   resolution is asynchronous in that case: call ``cb`` from the DNS query
   completion, not inline.

Using server affinity (PJSUA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. note::

   Server affinity is **not yet part of a released PJSIP version**; it will ship
   in the next release after 2.17. On current releases use the external resolver
   above. See :ref:`guide_server_affinity` for the full feature guide.

Enable :cpp:any:`pjsua_acc_config::server_affinity` on the account and pin the
chosen server address with :cpp:any:`pjsua_acc_set_affinity_addr()`. The
hostname in ``proxy[0]`` (or ``reg_uri``) is used for SNI and certificate
validation, while the address you pass is used as the actual connect target::

    pjsua_acc_config cfg;
    pjsua_acc_config_default(&cfg);

    /* Hostname here drives SNI + cert validation, NOT the connect target. */
    cfg.proxy_cnt = 1;
    cfg.proxy[0]  = pj_str("sip:sip.example.com;transport=tls;lr");
    cfg.reg_uri   = pj_str("sip:example.com");

    /* Enable affinity so the pinned transport is reused across requests.
     * Leave cfg.transport_id == PJSUA_INVALID_ID: a fixed transport_id
     * bypasses affinity. */
    cfg.server_affinity = PJSUA_SERVER_AFFINITY_ENABLED;

    pjsua_acc_add(&cfg, PJ_TRUE, &acc_id);

    /* Pick the server IP yourself (your failover decision) and pin it.
     * Connects to 198.51.100.10:5061 but presents/validates the TLS name
     * as "sip.example.com". */
    pj_sockaddr addr;
    pj_sockaddr_init(pj_AF_INET(), &addr, NULL, 5061);
    pj_inet_pton(pj_AF_INET(), &pj_str("198.51.100.10"),
                 &addr.ipv4.sin_addr);

    pjsua_acc_set_affinity_addr(acc_id, &addr);

On failover, call :cpp:any:`pjsua_acc_set_affinity_addr()` again with the next
server's address; the hostname (and therefore SNI and certificate validation)
stays correct. Note that on transport *reuse* the per-request hostname recheck
is skipped (trust is asserted at handshake), which is safe here because the
handshake used the correct hostname.

.. note::

   Server affinity is not TLS-specific: it pins the chosen address for UDP and
   TCP as well (TCP/TLS via the transport selector, UDP via a hidden Route
   header). It is the recommended way to do application-controlled failover for
   any transport; for TLS it additionally keeps the SNI and certificate name
   correct.

Using the transport API directly (PJSIP layer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At the PJSIP level the connect address and the TLS name are independent inputs
to :cpp:any:`pjsip_endpt_acquire_transport2()`: the ``addr`` argument is the
socket connect target, while ``tdata->dest_info.name`` is the name used for SNI
and certificate validation. Acquire the transport with the IP as ``addr`` and
the hostname in ``dest_info.name``. The call only *reads* ``dest_info`` from
the tdata (to learn the connect target and the TLS name) and does not retain
or reference-count it, so a throwaway zero-initialized ``pjsip_tx_data`` is
sufficient here — this mirrors the pattern PJSIP uses internally::

    pjsip_tx_data dummy;
    pj_bzero(&dummy, sizeof(dummy));
    pj_strdup2(pool, &dummy.dest_info.name, "sip.example.com");

    pjsip_endpt_acquire_transport2(endpt, PJSIP_TRANSPORT_TLS,
                                   &ip_addr, addr_len,  /* connect target */
                                   tp_sel, &dummy, &tp);

To actually send on that connection, set a transport selector of type
``PJSIP_TPSELECTOR_TRANSPORT`` (``sel->u.transport`` = the acquired transport)
on the outgoing :cpp:any:`pjsip_tx_data` before sending.

.. note::

   This is a PJSIP-layer technique and is **not reachable from a plain PJSUA
   application**. PJSUA's per-account transport binding
   (:cpp:any:`pjsua_acc_config::transport_id` / :cpp:any:`pjsua_acc_set_transport()`)
   selects only the local *listener* for connection-oriented transports
   (TCP/TLS), not a specific connected transport, so it cannot pin the
   destination. Use this approach when your application manages its own dialogs
   and transactions and can set ``tdata->tp_sel`` directly. PJSUA applications
   should use the external resolver (current releases) or server affinity (the
   release after 2.17) above instead.

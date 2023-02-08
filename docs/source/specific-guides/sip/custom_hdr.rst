.. _guide_adding_custom_header:

Adding custom header
=========================================
Custom headers can be specified when sending SIP requests, for example, 
when sending INVITE, IM message, etc. by specifying
the headers in :cpp:any:`pjsua_msg_data` structure, as shown in 
an example below:

.. code-block:: c

    pjsua_msg_data msg_data;
    pjsip_generic_string_hdr my_hdr;
    pj_str_t hname = pj_str("My-Header");
    pj_str_t hvalue = pj_str("This is the content of My-Header");

    pjsua_msg_data_init(&msg_data);
    pjsip_generic_string_hdr_init2(&my_hdr, &hname, &hvalue);
    pj_list_push_back(&msg_data.hdr_list, &my_hdr);

    // Specify the msg_data in pjsua_im_send(), for example
    pjsua_im_send(.., &msg_data, NULL);


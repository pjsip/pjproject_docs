URI Escaping
===================

The general rules about escaping and unescaping reserved characters in SIP message elements in PJSIP are as follows:

#. For incoming message, escaped strings will be unescaped by the parser before they are placed in the corresponding elements. For example, an element containing this URI:

   .. code-block::
      
      sip:good%20user@example.com

   will result in the following values to be placed in the :cpp:any:`pjsip_sip_uri` structure:
 
   .. code-block:: c

      pjsip_sip_uri.user = pj_str("good user");
      pjsip_sip_uri.host = pj_str("example.com");
 
   Notice the value of the ``user`` field in the example above.

#. A :cpp:any:`pjsip_sip_uri` that is passed around within the application MUST contain unescaped values. Keep this in mind especially when constructing a :cpp:any:`pjsip_sip_uri` structure manually. The library will take care about escaping them when needed, i.e. before transmitting the message to the wire. Hence using the example above, when setting the ``user`` field, put ``"good user"`` instead of ``"good%20user"`` as the value.
#. URI that is passed around within the application as a string MUST be escaped. Keep this in mind when constructing any URI strings. If you can't control the characters that go into an URI (for example, the username character set is not strictly enforced), then you need to construct a :cpp:any:`pjsip_sip_uri` and ``print`` it in order to get a properly escaped URI. For example:

    .. code-block:: c

       pjsip_sip_uri sip_uri;
       char buf[PJSIP_MAX_URL_SIZE];

       pjsip_sip_uri_init(&sip_uri, PJ_FALSE);
       sip_uri.user = pj_str("good user");
       sip_uri.host = pj_str("example.com");

       len = pjsip_uri_print(PJSIP_URI_IN_FROMTO_HDR, 
                             &sip_uri, buf, sizeof(buf));
       buf[len] = '\0';

       // buf now contains "sip:good%20user@example.com"

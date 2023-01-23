List of links
****************

How to link to various elements of the documentation from .rst file.

Overview
==========

- :ref:`3rd Party Licensing <licensing_3rd_party>`


API Reference
==============
- :doc:`/api/pjsua-lib/index`

Samples
===========
- :doc:`/api/samples`

Doxygen Objects
=================

TLDR: I think :cpp:any:`PJSUA_CALL_NO_SDP_OFFER` construct would work for all kinds of doxygen objects.
Other examples:

- a field: :cpp:any:`pjsua_callback::on_call_state`

Limitations: I don't know how to resolve nested struct. Example: :cpp:any:`pjsua_acc_config::ip_change_cfg::hangup_calls`

For full reference see https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain

Alternatively choose the correct way to link an object:

- C++ class: :cpp:class:`pj::AccountConfig`
- C++ method: :cpp:func:`pj::Account::create()`
- C API: :cpp:func:`pjsua_handle_ip_change()`
- C struct: :cpp:class:`pjsua_ip_change_param`
- Macro: :cpp:any:`PJSUA_CALL_NO_SDP_OFFER`

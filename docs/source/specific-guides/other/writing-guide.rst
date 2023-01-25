Writing guide
============================

.. contents:: Table of Contents
   :depth: 2

Note: see this document online in https://docs.pjsip.org/en/latest/specific-guides/other/writing-guide.html


Heading convention
----------------------------------------------

::

        ====================
        H0 (for site title)
        ====================
        
        H1 (prefer this for document title)
        ===================================


        We also use this for document title:

        Also H1 and document title
        *********************************

        (Historically, *** is higher level than === in this site, but then the layer
        with *** was deleted, so === becomes H1)


        H2
        ------------------------

        H3
        ~~~~~~~~~~~~~~~~~~~~~~~~~

        Also H3
        ^^^^^^^^^^^^^^^^^^^^^^^^^

        (I prefer ~~~ for H3 since it's less conspicuous)

        It's not recommended to have H4 and beyond; just use bold font.


Typography conventions
----------------------------------------------

- For PJSIP symbols, use breathe-apidoc constructs, e.g.:
   - macro: :cpp:any:`PJ_HAS_TCP`
   - C API: :cpp:any:`pjsua_handle_ip_change()`
   - C struct: :cpp:any:`pjsua_ip_change_param`
   - C field: :cpp:any:`pjsua_callback::on_call_state`
   - PJSUA2 class: :cpp:any:`pj::AccountConfig`
   - PJSUA2 method: :cpp:any:`pj::Account::create()`
- For other identifier: ``identifier``
- ``command``
- ``file name``
- Bold for **UI items** like **OK** button, **File -> Open** menu, and for normal emphasis like **this** is important.
- Italics for quoted info, e.g. according to RFC 123 Section 1.2: *Open source software is good*.


.. note::

   - Sometomes macros wouldn't resolve (sometimes it resolves in my local machine, but not in RTD site, or the other way around). Don't know why yet.
   - nested struct member wouldn't resolve, not sure why yet, e.g.: :cpp:any:`pjsua_acc_config::ip_change_cfg::hangup_calls`
   - For full reference see https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain


Cross referencing
----------------------------------------------

Linking to a page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``:doc:`` to link to a page.

Sample linking to getting started pages:

- :doc:`/get-started/android/index`
- :doc:`/get-started/ios/index`
- :doc:`/get-started/ios/index`
- :doc:`/get-started/posix/index`
- :doc:`/get-started/windows/index`
- :doc:`/get-started/windows-phone/index`

Sample linking to root API reference pages and samples:

- :doc:`/api/pjsua2/index`
- :doc:`/api/pjsua-lib/index`
- :doc:`/api/pjsip/index`
- :doc:`/api/pjmedia/index`
- :doc:`/api/pjnath/index`
- :doc:`/api/pjlib-util/index`
- :doc:`/api/pjlib/index`
- :doc:`/api/samples`

Linking to doxygen group/topic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To link to specific doxygen group/topic:

- Open the relevant API reference page (e.g. :doc:`/api/pjnath/ref`)
- View the source to get the link, e.g. 
  
  ::

        `:doc:`uPnP </api/generated/pjnath/group/group__PJNATH__UPNP>`

  which will be rendered as :doc:`uPnP </api/generated/pjnath/group/group__PJNATH__UPNP>`


Creating own cross reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is if you want to create and cross reference a specific location in a page (rather than the whole page).

First create the link target (analogous to ``<A name>``). Don't forget the underscore before the id:

.. _my_secret_target:

::

        .. _my_secret_target:

Then to reference the target, use `my_secret_target`_ or :ref:`With a text <my_secret_target>` (note: there's no underscore).



Linking to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Issue :issue:`1234`
- PR :pr:`3291` 
- source :source:`pjmedia/include/pjmedia/config.h`
- source directory :sourcedir:`pjmedia/include`

.. note::

   In practice ``:issue:`` or ``:pr:`` can be used interchangeably since GitHub will redirect to correct URL, but it's best to use the correct construct to avoid unnecessary redirect.


External links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

E.g. `PJSIP website <https://pjsip.org>`__

Note: use double instead of single underscore.



Linking from external website
----------------------------------------------

Find the target link from the front page: https://docs.pjsip.org/en/latest/index.html



Notes, Warnings, and Blocks
----------------------------------------------

.. note:: 

   This is a note


.. tip::

   This is a tip


.. warning::

   This is a warning


.. code-block:: c

   /* Sample C code */
   puts("Hello world");


.. code-block:: shell

   $ echo Hello world


References:

- https://sublime-and-sphinx-guide.readthedocs.io/en/latest/notes_warnings.html
- https://sublime-and-sphinx-guide.readthedocs.io/en/latest/code_blocks.html


Local TOC
----------------------------------------------
It's recommended to have TOC at the start of the document:

::

        .. contents:: Table of Contents
            :depth: 2


Converting from Trac wiki
----------------------------------------------

This is what I found to get the best conversion result, although bear in mind that the best result still requires a lot of manual editing afterwards. It requires Pandoc though (https://pandoc.org/).

#. Download Trac wiki page to a temporary file
#. Convert:

.. code-block:: shell

        $ trac2down tracwikifile.trac | pandoc -f markdown -t rst > output.rst

Note: ``trac2down.py`` is in the root dir of ``pjproject_docs``

Note: there should be other tools to convert from markdown to rst. I happen to have Pandoc installed.




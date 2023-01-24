Writing guide
****************

Heading convention
=====================

::

        ====================
        H0 (for site title)
        ====================

        H1
        ***

        H2
        ===

        H3
        ---

        H4
        ^^^

        or this (used by some converter):

        H4
        ~~~~~~~~~~~~


Typography convention
========================

* ``identifier``
* ``command``
* ``file name``
* **UI item**


Writing links From within the doc (from other .rst file)
============================================================


Linking to a page
-------------------------------------------
::

    Getting started pages:

        - :doc:`/get-started/android/index`
        - :doc:`/get-started/ios/index`
        - :doc:`/get-started/ios/index`
        - :doc:`/get-started/posix/index`
        - :doc:`/get-started/windows/index`
        - :doc:`/get-started/windows-phone/index`

    Root API reference pages and samples:

        - :doc:`/api/pjsua2/index`
        - :doc:`/api/pjsua-lib/index`
        - :doc:`/api/pjsip/index`
        - :doc:`/api/pjmedia/index`
        - :doc:`/api/pjnath/index`
        - :doc:`/api/pjlib-util/index`
        - :doc:`/api/pjlib/index`
        - :doc:`/api/samples`

    For links to specific Doxygen group, see group's Doxygen ID in the index page
    of the corresponding library:

        - api/pjlib/index.rst
        - api/pjlib-util/index.rst
        - etc
  

Creating/linking to user defined point
-------------------------------------------
Create the link target (analogous to ``<A name>``). Don't forget the underscore before the id:

::

        .. _android_pjsua2:

Then create the link (without underscore):

::

        :ref:`android_pjsua2`

        or 

        :ref:`With a text <android_pjsua2>`


Linking to Doxygen Objects
-------------------------------------------

::

        - macro: :cpp:any:`PJSUA_CALL_NO_SDP_OFFER`
        - C API: :cpp:any:`pjsua_handle_ip_change()`
        - C struct: :cpp:any:`pjsua_ip_change_param`
        - C field: :cpp:any:`pjsua_callback::on_call_state`
        - C++ class: :cpp:any:`pj::AccountConfig`
        - C++ method: :cpp:any:`pj::Account::create()`

Limitations: I don't know how to link nested struct member. Example: :cpp:any:`pjsua_acc_config::ip_change_cfg::hangup_calls` would not resolve.

For full reference see https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain



Linking to issues/PR in PJPROJECT GitHub
-------------------------------------------
::

        :pr:`2797`


Linking from external website
============================================================

Find the target link from the front page: https://docs.pjsip.org/en/latest/index.html



Notes, Warnings, and Blocks
==============================

.. code-block::

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
============
::
        .. contents:: Table of Contents
            :depth: 2


Converting from Trac wiki
===========================

This is what I found to get the best conversion result, although bear in mind that the best result still requires a lot of manual editing afterwards. It requires Pandoc though (https://pandoc.org/).

#. Download Trac wiki page to a temporary file
#. Convert:

.. code-block:: shell

        $ trac2down tracwikifile.trac | pandoc -f markdown -t rst > output.rst

Note: ``trac2down.py`` is in the root dir of ``pjproject_docs``

Note: there should be other tools to convert from markdown to rst. I happen to have Pandoc installed.




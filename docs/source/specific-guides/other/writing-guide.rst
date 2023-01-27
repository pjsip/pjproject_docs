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

        H4
        ``````````````
        


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

   - Sometomes macros wouldn't resolve (sometimes it resolves in development machine, but not in RTD site, or the other way around). Not sure why yet.
   - nested struct member wouldn't resolve, e.g.: :cpp:any:`pjsua_acc_config::ip_change_cfg::hangup_calls`, so you need to break it down into separate parts, e.g. :cpp:any:`hangup_calls <pjsua_ip_change_acc_cfg::hangup_calls>` of :cpp:any:`pjsua_acc_config::ip_change_cfg`
   - For full reference see https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain


Cross referencing
----------------------------------------------

.. tip::

   Rather than explicitly specifying the role in the link (with ``:doc:`` or
   ``:ref:``), you can use ``:any:`` to make Sphinx automatically detect the best
   role to use for the specified target.


Linking to documentation section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Links to sections in the menu:

- :any:`overview_toc`
- :any:`get_started_toc`
- :any:`pjsua2_toc`
- :any:`specific_guides_toc`

  - :any:`spec_guide_audio_toc`
  - :any:`build_int_guide_toc`
  - :any:`dev_prog_guide_toc`
  - :any:`media_guide_toc`
  - :any:`network_nat_guide_toc`
  - :any:`perf_footprint_guide_toc`
  - :any:`security_guide_toc`
  - :any:`sip_guide_toc`
  - :any:`video_guide_toc`
  - :any:`other_guide_toc`


- API Reference & Samples: :any:`api_ref_samples_toc`



Linking to a page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``:any:`` or ``:doc:`` to link to a page.

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


Available cross-references:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currenty available cross-references:

.. code-block:: shell


   $ egrep -r '^.. _' * | grep rst
   api/pjlib/index.rst:.. _pjlib_pool:
   api/pjlib/index.rst:.. _pjlib_string:
   api/pjnath/ref.rst:.. _ice:
   api/pjnath/ref.rst:.. _stun:
   api/pjnath/ref.rst:.. _turn:
   api/pjnath/ref.rst:.. _upnp:
   api/pjnath/ref.rst:.. _nat_detect:
   api/pjmedia/pjmedia-audiodev.rst:.. _audiodev_supported_devs:
   api/pjmedia/pjmedia-audiodev.rst:.. _alsa:
   api/pjmedia/pjmedia-audiodev.rst:.. _opensl:
   api/pjmedia/pjmedia-audiodev.rst:.. _jnisound:
   api/pjmedia/pjmedia-audiodev.rst:.. _oboe:
   api/pjmedia/pjmedia-audiodev.rst:.. _bdsound:
   api/pjmedia/pjmedia-audiodev.rst:.. _coreaudio:
   api/pjmedia/pjmedia-audiodev.rst:.. _wmme:
   api/pjmedia/pjmedia-audiodev.rst:.. _wasapi:
   api/pjmedia/pjmedia-audiodev.rst:.. _portaudio:
   api/pjmedia/pjmedia-videodev.rst:.. _android_cam:
   api/pjmedia/pjmedia-videodev.rst:.. _avi_device:
   api/pjmedia/pjmedia-videodev.rst:.. _avfoundation:
   api/pjmedia/pjmedia-videodev.rst:.. _colorbar:
   api/pjmedia/pjmedia-videodev.rst:.. _dshow:
   api/pjmedia/pjmedia-videodev.rst:.. _ffmpeg_capture:
   api/pjmedia/pjmedia-videodev.rst:.. _opengl:
   api/pjmedia/pjmedia-videodev.rst:.. _qtdev:
   api/pjmedia/pjmedia-videodev.rst:.. _sdl:
   api/pjmedia/pjmedia-videodev.rst:.. _guide_sdl:
   api/pjmedia/pjmedia-videodev.rst:.. _video4linux:
   api/pjmedia/pjmedia-videodev.rst:.. _guide_video4linux:
   api/pjmedia/pjmedia-codec.rst:.. _pjmedia-codec:
   api/pjmedia/pjmedia-codec.rst:.. _amediacodec:
   api/pjmedia/pjmedia-codec.rst:.. _bcg729:
   api/pjmedia/pjmedia-codec.rst:.. _ffmpeg:
   api/pjmedia/pjmedia-codec.rst:.. _g711:
   api/pjmedia/pjmedia-codec.rst:.. _g722:
   api/pjmedia/pjmedia-codec.rst:.. _g7221:
   api/pjmedia/pjmedia-codec.rst:.. _gsm:
   api/pjmedia/pjmedia-codec.rst:.. _ilbc:
   api/pjmedia/pjmedia-codec.rst:.. _ipp:
   api/pjmedia/pjmedia-codec.rst:.. _l16:
   api/pjmedia/pjmedia-codec.rst:.. _opencore_amr:
   api/pjmedia/pjmedia-codec.rst:.. _openh264:
   api/pjmedia/pjmedia-codec.rst:.. _opus:
   api/pjmedia/pjmedia-codec.rst:.. _passthrough:
   api/pjmedia/pjmedia-codec.rst:.. _silk:
   api/pjmedia/pjmedia-codec.rst:.. _speex:
   api/pjmedia/pjmedia-codec.rst:.. _libvpx:
   get-started/android/build_instructions.rst:.. _android_pjsua2:
   get-started/android/build_instructions.rst:.. _android_create_app:
   get-started/ios/issues.rst:.. _ios_bg:
   get-started/guidelines-development.rst:.. _dev_start:
   get-started/guidelines-development.rst:.. _config_site.h:
   get-started/guidelines-api.rst:.. _which_api_to_use:
   overview/license_3rd_party.rst:.. _licensing_3rd_party:
   pjsua2/using/call.rst:.. _pjsua2_call_disconnection:
   pjsua2/using/account.rst:.. _pjsua2_creating_userless_account:
   specific-guides/sip/index.rst:.. _guide_adding_custom_header:
   specific-guides/build_int/ffmpeg.rst:.. _guide_ffmpeg:
   specific-guides/audio/webrtc.rst:.. _guide_webrtc:
   specific-guides/audio/opencore-amr.rst:.. _guide_opencore_amr:
   specific-guides/audio/index.rst:.. _guide_ipp:
   specific-guides/perf_footprint/index.rst:.. _guide_performance:
   specific-guides/perf_footprint/index.rst:.. _guide_footprint:
   specific-guides/security/ssl.rst:.. _guide_ssl:
   specific-guides/network_nat/qos.rst:.. _qos:
   specific-guides/other/writing-guide.rst:.. _my_secret_target:
   specific-guides/video/index.rst:.. _guide_libyuv:
   specific-guides/video/index.rst:.. _guide_vidconf:


Creating own cross reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is if you want to create and cross reference a specific location in a page (rather than the whole page).

First create the link target (analogous to ``<A name>``). Don't forget the underscore before the id:

.. _my_secret_target:

::

        .. _my_secret_target:

Then to reference the target, use `my_secret_target`_ or :ref:`With a text <my_secret_target>` (note: there's no underscore).

See https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role for more info.


Linking to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Issue :issue:`1234`
- PR :pr:`3291` 
- source :source:`pjmedia/include/pjmedia/config.h`
- source directory :sourcedir:`pjmedia/include`

.. note::

   In practice ``:issue:`` or ``:pr:`` can be used interchangeably since GitHub will redirect to correct URL, but it's best to use the correct construct to avoid unnecessary redirect.


RFC link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``:rfc:\`3711\``` which will be rendered as :rfc:`3711`.


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




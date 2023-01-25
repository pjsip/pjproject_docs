Development guidelines
======================

Preparation
------------
* **Essential:** Familiarise yourself with SIP. While there is no need to be an expert, 
  some SIP knowledge is essential. 
* Check out the features in :doc:`Features/Datasheet </overview/features>`.
* Familiarize with the structure of https://docs.pjsip.org. All documentations
  are hosted here.

.. _dev_start:

Development
-------------
* **Essential:** Follow the :doc:`Getting Started </get-started/getting>`
  instructions to build PJSIP for your platform.
* **Essential:** Interactive debugging capability is essential during development


Coding Style
-------------
Below is the PJSIP coding style. You need to follow it if you are submitting 
patches to PJSIP:

* Indent by 4 characters and use spaces only.
* All public API in header file must be documented in Doxygen format.
* Use `K & R style <http://en.wikipedia.org/wiki/1_true_brace_style#K.26R_style>`__, 
  which is the only correct style anyway.

.. note::

   PJSIP indentation scheme was changed to use spaces only since version 2.13.


Deployment
-----------
* **Essential:** Logging is essential when troubleshooting any problems. The application MUST be 
  equipped with logging capability. Enable PJSIP log at level 5.


.. _config_site.h:

config_site.h
---------------------
You need to create ``pjlib/include/pj/config_site.h`` file. This file contains compile-time
customizations for your application.

It is recommended to start with default settings in :source:`pjlib/include/pj/config_site_sample.h`,
by including this file in your ``config_site.h``, i.e.:

  .. code-block:: c

        #include <pj/config_site_sample.h>

The default settings should be good to get you started. You can always optimize later after 
things are running okay.


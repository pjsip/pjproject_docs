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
Our coding style will be discussed in the :doc:`next section <coding-style>`.


Deployment
-----------
* **Essential:** Logging is essential when troubleshooting any problems. The application MUST be 
  equipped with logging capability. Enable PJSIP log at level 5.


.. _config_site.h:

config_site.h
---------------------
Depending on the platform, you may need to create ``pjlib/include/pj/config_site.h`` file. 
This file contains compile-time customizations that are specific for your application, hence this
file is not included in PJSIP distribution.

If you're using GNU make build system, the ``./configure`` script will create an empty
``config_site.h`` if it doesn't exist. 

It is recommended to start with default settings in :source:`pjlib/include/pj/config_site_sample.h`,
by including this file in your ``config_site.h``, i.e.:

  .. code-block:: c

        #include <pj/config_site_sample.h>

The default settings should be good to get you started. You can always optimize later after 
things are running okay.


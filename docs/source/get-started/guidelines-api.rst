.. _which_api_to_use:

Which API to use
================
Let's have a look at the libraries architecture again:

.. raw:: html
    :file: ../overview/architecture.svg

PJSIP, PJMEDIA, and PJNATH Level
--------------------------------
At the lowest level we have the individual **C** libraries, which 
consist of :doc:`PJSIP </api/pjsip/index>`, :doc:`PJMEDIA </api/pjmedia/index>`, and 
:doc:`PJNATH </api/pjnath/index>`, with :doc:`PJLIB-UTIL </api/pjlib-util/index>` and 
:doc:`PJLIB </api/pjlib/index>` as support libraries. This level provides the most flexibility, but 
it's also the hardest to use. The only reason you'd want to use this level is if:

#. You only need the individual library (say, PJNATH)
#. You need to be very very tight in footprint (say when things need to be measured in Kilobytes instead 
   of Megabytes)
#. You are **not** developing a SIP client

Use the corresponding :doc:`PJSIP </api/pjsip/index>`, :doc:`PJMEDIA </api/pjmedia/index>`, and 
:doc:`PJNATH </api/pjnath/index>` manuals and :doc:`samples </api/samples>` for information on how
to use the libraries. 


PJSUA-LIB API
-------------
Next up is :doc:`PJSUA-LIB API </api/pjsua-lib/index>` that combines all those libraries into a 
high level, integrated client user agent library written in **C**. This is the library that most 
PJSIP users use, and the highest level abstraction before PJSUA2 was created. 

Motivations for using PJSUA-LIB library include:

#. Developing client application (PJSUA-LIB is optimized for developing client app)
#. Better efficiency than higher level API


PJSUA2 C++ API
--------------
:doc:`PJSUA2 API </api/pjsua2/index>` is an objected oriented, C++ API created on top of PJSUA-LIB. 
The API is different than PJSUA-LIB, but it should be even easier to use and it should have better 
documentation too (see :any:`PJSUA2 Guide <pjsua2_toc>`). The PJSUA2 API removes most cruxes 
typically associated with PJSIP, such as :ref:`the pool <pjlib_pool>` and :ref:`pj_str_t <pjlib_string>`, 
and adds new features such as object persistence so you can save your configs to JSON file, for example. 
All data structures are rewritten for more clarity. 

A C++ application can use PJSUA2 natively, while at the same time still has access to the lower level 
**C** objects if it needs to. This means that the C++ application should not lose any information from 
using the C++ abstraction, compared to if it is using PJSUA-LIB directly. The C++ application also 
should not lose the ability to extend the library. It would still be able to register a custom PJSIP module, 
pjmedia_port, pjmedia_transport, and so on.

Benefits of using PJSUA2 C++ API include:

#. Cleaner object oriented API
#. Uniform API for higher level language such as Java, Python, and C#
#. Persistence API
#. The ability to access PJSUA-LIB and lower level libraries when needed (including the ability to extend 
   the libraries, for example creating custom PJSIP module, pjmedia_port, pjmedia_transport, etc.)


Some considerations on using PJSUA2 C++ API are:

#. Instead of returning error, the API uses exception for error reporting
#. It uses standard C++ library (STL)
#. The performance penalty due to the API abstraction should be negligible on typical modern device



PJSUA2 API for Java, Python, C#, and Others
------------------------------------------------
The PJSUA2 API is also available for non-native code via SWIG binding. Configurations for Java, Python, and 
C# are provided with the distribution. See :doc:`Building PJSUA2 </pjsua2/building>` section for more
information. Thanks to SWIG, other language bindings may be generated relatively easily in the future.
 
The PJSUA2 API for non-native code is effectively the same as PJSUA2 C++ API. You can peek at the 
:doc:`Hello world </pjsua2/hello_world>` section to see how these look like. However, unlike C++, 
you cannot access PJSUA-LIB and the underlying C libraries from the scripting language, hence you are 
limited to what pjsua2 provides. 

You can use this API if native application development is not available in target platform (such as Android), 
or if you prefer to develop with non-native code instead of C/C++.

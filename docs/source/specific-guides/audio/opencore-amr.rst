.. _guide_opencore_amr:

OpenCore AMR codecs integration
=========================================


This page describes how to add OpenCORE AMR-NB and AMR-WB support into PJSIP.

Building and Installing OpenCORE AMR Library
---------------------------------------------------

This instruction applies for **all platforms** that OpenCORE supports, **including Windows**. For Windows, you need to use MinGW to build the OpenCORE library.

We tested building the OpenCORE libraries for Linux, MacOS X, Windows (MinGW), and BlackBerry 10 (BB10).

Building and installing OpenCORE AMR library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 #. Download the latest `opencore-amr <http://sourceforge.net/projects/opencore-amr/files/opencore-amr/>`__ tarball. We tested with version 0.1.3.
 #. Unpack the tarballs to a directory:
 
    .. code-block:: shell
        
        $ cd my_build_directory
        $ tar xzf opencore-amr-0.1.3.tar.gz
        $
 
 #. Run configure. Add ``--prefix`` to install the library to an alternate directory (such as your home folder) instead of to the system wide ``/usr`` directory:
 
    .. code-block:: shell
     
        $ ./configure --prefix=/home/foo
 
 #. **Obsolete:** Or if you're building for BB10, then download ``generic-configure-bb10`` script in the attachment in the bottom of this page, copy it to the opencore-amr directory, and use it instead. Make sure BB10 environment variables have been set as per BB10 instructions.
 
     .. code-block:: shell
    
        $ chmod +x generic-configure-bb10
        $ ./generic-configure-bb10 --prefix=/home/foo
 
 #. Build and install:
 
    .. code-block:: shell
    
       make && make install
 

Adding AMR-WB Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The OpenCORE AMR tarball contains AMR-NB encoder and decoder, but only AMR-WB decoder. We have to install AMR-WB encoder separately:

#. Download the latest `vo-amrwbenc <http://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/>`__ tarball. We tested with version 0.1.3
#. Unpack the tarballs to a directory:

   .. code-block:: shell

      $ cd my_build_directory
      $ tar xzf vo-amrwbenc-0.1.3.tar.gz
      $
 
#. Run configure. If you use ``--prefix``, make sure it has the same prefix as the one you used when configuring opencore-amr library:

   .. code-block:: shell

      $ ./configure --prefix=/home/foo
 
#. **Obsolete**: Again if you're building for BB10, then download ``generic-configure-bb10`` script in the attachment in the bottom of this page, copy it to the opencore-amr directory, and use it instead:

   .. code-block:: shell
   
      $ chmod +x generic-configure-bb10
      $ ./generic-configure-bb10 --prefix=/home/foo
 
#. Build and install:

   .. code-block:: shell
   
      $ make && make install


Testing The Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To verify, make sure **include** directory in the installation directory contains these files. Suppose you use ``--prefix=/home/foo``, then:

   .. code-block:: shell
   
      $ ls /home/foo/include
        opencore-amrnb  opencore-amrwb  vo-amrwbenc


Adding AMR Support in PJSIP
----------------------------------
Make Build System (MacOS X, Linux, BB10, etc.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. In the pjproject directory, run ``configure`` script, specifying the installation directory of OpenCORE codec to the ``--with-opencore-amr`` option:

   .. code-block:: shell

      $ ./configure --with-opencore-amr=/home/foo

#. **Obsolete**: Or if you're building for BB10, then use ``configure-bb10`` instead. See Getting Started for BB10 instructions for the complete instructions on how to build PJSIP for BB10:

   .. code-block:: shell

      $ ./configure-bb10 --with-opencore-amr=/home/foo

#. Check the output of ``configure`` command, make sure that the codecs are detected:

   .. code-block:: shell

      checking for OpenCORE AMR installations..
      Using OpenCORE AMR prefix... /home/foo
      ...
      ...
      OpenCORE AMR-NB library found, AMR-NB support enabled
      ...
      ...
      OpenCORE AMR-WB library found, AMR-WB support enabled

#. If the codecs are not enabled, that means the ``configure`` script were unable to find some files in the specified directory. Check the screen output again to see what were missing, and rebuild or reinstall the OpenCORE libraries if necessary.
#. Build PJSIP:

   .. code-block:: shell

      $ make dep && make clean && make

#. PJSIP is now built with OpenCORE AMR support

Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Add your installed OpenCORE directories to Visual Studio include and lib paths. You should know how to do this.
#. Configure and build pjsip with Visual Studio:

   #. Download the latest pjproject
   #. Add this to your ``config_site.h``:

      .. code-block:: c

        #define PJMEDIA_HAS_OPENCORE_AMRNB_CODEC 1
        /* And if you want to have AMR-WB support: */
        #define PJMEDIA_HAS_OPENCORE_AMRWB_CODEC 1

   #. Build the pjproject solution.
   #. The AMR-NB (and AMR-WB) codecs are now available ready to be used.

   .. note:: 

      On MSVC, there may be linking error such as:

      .. code-block:: shell

         unresolved external symbol ___chkstk referenced in function _coder

      A possible solution is by manually appending ``_chkstk.o`` to ``libvo-amrwbenc.a``:

      .. code-block:: shell

         $ cd <path-to-libvo-amrwbenc.a>
         $ ar x <path-to>/libgcc.a _chkstk.o
         $ ar q libvo-amrwbenc.a _chkstk.o



Testing PJSIP For OpenCORE AMR Support
---------------------------------------------

#. Run ``pjsua``
#. List the codecs with ``Cp`` command from pjsua console:

   .. code-block:: shell
   
      >>> Cp
      List of audio codecs:
        ...
        127	AMR/8000/1
        128	AMR-WB/8000/1
        ...

      List of video codecs:
        ...

      Enter codec id and its new priority (e.g. "speex/16000 200", "H263 200"),
      or empty to cancel.
      Codec name ("*" for all) and priority: 
      Done
      >>>
 


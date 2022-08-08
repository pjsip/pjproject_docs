Building PJSUA2
******************************
The PJSUA2 C++ library is built by default by PJSIP build system. 
Standard C++ library is required.

The following sections applies to building SWIG Python, Java, or C# modules.

Common Requirements
======================================

#. On Linux/MacOS X/Unix, you need to build PJPROJECT with ``-fPIC`` option. 
   You can either put it in ``user.mak`` file in root pjproject directory like 
   this:

   .. code-block::

      CFLAGS += -fPIC

   or you can specify it when calling ``configure``:

   .. code-block:: shell

      ./configure CFLAGS="-fPIC"

   Then rebuild pjproject.

#. Install `SWIG <http://www.swig.org>`_

   For Debian based distributions (such as Ubuntu):

   .. code-block:: shell

      sudo apt-get install swig

   For Windows and other platforms please see https://www.swig.org/download.html


Building Python SWIG Module
======================================
1. Install SWIG as shown above.
2. Install Python development package:

   For Debian based distributions (such as Ubuntu):

   .. code-block:: shell

      sudo apt-get install python3-dev
   
   For other platforms, TBD.

3. Build:

   .. code-block:: shell

      cd pjsip-apps/src/swig/python
      make
      make install

   .. note::

      The above will install the module to user's ``site-packages`` directory.

      If you're currently on a **virtualenv**, run ``python setup.py install`` instead.

   

4. Test the installation:

   .. code-block:: shell

      $ python3
      > import pjsua2
      > ^Z



Building Java SWIG Module
======================================
1. Install SWIG as shown above.
2. Install JDK.
3. Build:

   .. code-block:: shell

      cd pjsip-apps/src/swig/java
      make
      make install

   TBD.


Building C# SWIG Module
======================================
1. Install SWIG as shown above.
2. Install .. (TBD)
3. Build:

   .. code-block:: shell

      cd pjsip-apps/src/swig/csharp
      make
      make install

   TBD.

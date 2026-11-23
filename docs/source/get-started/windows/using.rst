Using PJSIP in Windows applications
=====================================================

These steps use the libraries built with :doc:`build_vs`. For the libraries built with
:doc:`build_cmake`, see :doc:`/get-started/cmake/using`.

#. Put these include directories in the include search path of your project:

   * pjlib/include
   * pjlib-util/include
   * pjnath/include
   * pjmedia/include
   * pjsip/include

#. Put the combined library directory **lib** (located in the root directory of 
   pjproject source code) in the library search path
#. Include the relevant PJ header files in the application source file. 
   For example, using these would include ALL APIs exported by PJ:

   .. code-block:: c

      #include <pjlib.h>
      #include <pjlib-util.h>
      #include <pjnath.h>
      #include <pjsip.h>
      #include <pjsip_ua.h>
      #include <pjsip_simple.h>
      #include <pjsua-lib/pjsua.h>
      #include <pjmedia.h>
      #include <pjmedia-codec.h>

   .. note::

      The documentation of the relevant libraries should say which header files 
      should be included to get the declaration of the APIs).

#. Link with the main pjproject library ``libpjproject``. It includes all the 
   libraries provided. 

   .. note::

      The actual library names will be appended with the target name and the 
      build configuration. For example: The actual library names will look 
      like ``libpjproject-x86_64-x64-vc14-Release.lib`` depending on whether
      we are building the Debug or Release version of the library.

#. Build the application with the same C run-time option as the libraries, e.g. Multithreaded
   Debug (/MTd) for the ``Debug`` configuration; see the build configurations in
   :doc:`build_vs`.

#. Link with system specific libraries, as the ``pjsua`` project does: ws2_32.lib, mswsock.lib,
   iphlpapi.lib, netapi32.lib, ole32.lib, user32.lib, gdi32.lib, advapi32.lib, dsound.lib,
   dxguid.lib

#. If you want to use video API see :any:`/pjsua2/using/media_video` and the deep-dive pages under :ref:`video_guide_toc`.


Using PJSIP in Windows applications
=====================================================

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

#. Declare PJ_WIN32=1 macro in the project settings (declaring the macro in the 
   source file may not be sufficient).

#. Link with the main pjproject library ``libpjproject``. It includes all the 
   libraries provided. 

   .. note::

      The actual library names will be appended with the target name and the 
      build configuration. For example: The actual library names will look 
      like ``libpjproject-i386-win32-vc6-debug.lib`` depending on whether 
      we are building the Debug or Release version of the library.

#. Link with system specific libraries such as: wsock32.lib, ws2_32.lib, ole32.lib, 
   dsound.lib

#. If you want to use video API see :any:`/specific-guides/video/users_guide`


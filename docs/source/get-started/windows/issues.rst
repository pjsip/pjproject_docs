Issue(s) when Developing Windows Apps
**************************************

*  **Troubleshooting Crash Problem on Win32**
  
   **Building Application with Debugging Info**

   The best way to find the crash is to equip your program with debugging info 
   (for the Release mode) so that we can know exactly where the crash location is. 
   A debugging info will not slow down your application, although it will 
   add size to it, so it shouldn't be a problem.
   Building Application with Debugging Info

   The instructions here applies for Visual Studio use:

   * For all libraries, open Project Settings, then go to C/C++ General Tab, 
     set Debug Info to Program Database.
   * Then in the application project, open Project Settings, go to Link tab, 
     enable Generate debug info.
   * Rebuild all libraries and application 

   Now a .PDB (Program Database) file will be generated for the application.

   **Distributing Application**

   When distributing the application executable, the .PDB file (for the application) 
   needs to be distributed alongside the application. 
   Put the .PDB file on the same directory as the application.

   .. note::

     whenever the application is rebuilt, don't forget to update the .PDB file 
     as well or otherwise the debugging information will not contain the correct 
     information.

   **Testing if Crash Reporting Works**

   Before running the application with real usage, it's probably better to test 
   if the error reporting works correctly.

   Add a code somewhere to simulate a crash, something like:

   .. code-block:: c

      int *p = (int *)0;
      *p = 0;

   It's probably best to place this crash generator code somewhere deep in the 
   libraries to make sure that crash in the library is properly reported.
   
   **Checking the Crash Report**

   If Visual Studio is installed in the target machine, it will be executed when 
   the application crashes.

   Otherwise the crash info will be saved in Dr. Watson log. Open Dr. Watson 
   application by executing drwtsn32.exe from Start Menu --> Run.. menu. 
   The crash info should show where exactly the crash happens along with other 
   useful information.

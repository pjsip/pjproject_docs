Common issues when developing on Windows
===============================================

.. contents:: Table of Contents
    :depth: 2


Troubleshooting crash problem on Win32
-----------------------------------------------
  
Building Application with Debugging Info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The best way to find the crash is to equip your program with debugging info 
(for the Release mode) so that we can know exactly where the crash location is. 
A debugging info will not slow down your application, although it will 
add size to it, so it shouldn't be a problem.

The instructions here applies for Visual Studio use:

   * For all libraries, open the project's Properties, then go to
     *C/C++ > General*, set *Debug Information Format* to *Program Database (/Zi)*.
   * Then in the application project, open the Properties, go to *Linker > Debugging*,
     set *Generate Debug Info* to *Yes*.
   * Rebuild all libraries and application 

   Now a .PDB (Program Database) file will be generated for the application.

With :doc:`build_cmake`, build the ``RelWithDebInfo`` configuration instead, which is optimized
and generates the .PDB files.

Distributing Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Keep the .PDB file (for the application) of every build you distribute; it is needed to read the
crash dumps below. For a debugger on the target machine to show the crash location, also
distribute the .PDB file alongside the application, in the same directory.

.. note::

     whenever the application is rebuilt, don't forget to update the .PDB file 
     as well or otherwise the debugging information will not contain the correct 
     information.

Testing if Crash Reporting Works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Before running the application with real usage, it's probably better to test 
if the error reporting works correctly.

Add a code somewhere to simulate a crash, something like:

.. code-block:: c

      int *p = (int *)0;
      *p = 0;

It's probably best to place this crash generator code somewhere deep in the 
libraries to make sure that crash in the library is properly reported.

Checking the Crash Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If Visual Studio is installed in the target machine, it will be executed when 
the application crashes.

Otherwise, have Windows Error Reporting save a crash dump: create the registry key
``HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps``. The dumps
are then saved in ``%LOCALAPPDATA%\CrashDumps``. Open the dump file in Visual Studio or WinDbg,
with the application's .PDB file, to see where exactly the crash happens along with other
useful information.

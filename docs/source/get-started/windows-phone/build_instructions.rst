Build Instructions
===================

.. contents:: Table of Contents
    :depth: 3


Requirements
------------------

Tools and SDKs
^^^^^^^^^^^^^^^

* Microsoft Visual Studio 2015 Update 3
* `UWP SDK <https://dev.windows.com/en-us/downloads/windows-10-sdk>`__ 
  for UWP/Windows 10 target.
* `Windows Phone 8 SDK <http://dev.windowsphone.com/en-us/downloadsdk>`__ 
  for Windows Phone 8 target. 
* Configuring device for development:

  * for Windows 10, follow the instructions 
    `here <https://msdn.microsoft.com/en-us/windows/uwp/get-started/enable-your-device-for-development>`__
  * for Windows Phone 8.x, follow the instructions 
    `here <http://msdn.microsoft.com/en-us/library/windowsphone/develop/ff769508(v=vs.105).aspx>`__

Host requirements
^^^^^^^^^^^^^^^^^^

For the host, the following are required:

* Operating System type : 64-bit Windows 8 Professional or higher.

Build Preparation
------------------

#. :doc:`Getting the source code </get-started/getting>` if you haven't already.
#. Set your :ref:`config_site.h <dev_start>` to the following:

.. code-block:: c

   #define PJMEDIA_AUDIO_DEV_HAS_PORTAUDIO   0
   #define PJMEDIA_AUDIO_DEV_HAS_WMME        0
   #define PJMEDIA_AUDIO_DEV_HAS_WASAPI      1

Building and running the Projects
---------------------------------

UWP
^^^

Follow the steps below to build the libraries and sample application using 
Visual Studio 2015:

#. Using any text editor, open :source:`build\vs\pjproject-vs14-api-def.props` 
   and set ``API_Family`` to **UWP**, i.e:

   .. code-block:: 

      ...
      <API_Family>UWP</API_Family>
      ...
      
   .. note:: 

      If ``pjproject-vs14.sln`` solution is opened, you need to close and reopen 
      the solution after changing API family.

#. Open ``pjproject-vs14.sln`` solution file.
#. Set solution platform to:

   * **ARM** to build for UWP/Windows 10 device
   * **Win32** to build for emulator

#. Set **Voip** as Startup Project.
#. Build the project. This will build **Voip** application and all libraries 
   needed by **Voip**.
#. Run

Windows Phone 8.x
^^^^^^^^^^^^^^^^^^

Follow the steps below to build the libraries and sample application using 
Visual Studio 2015:

#. Using any text editor, open ``build\vs\pjproject-vs14-api-def.props`` 
   and set ``API_Family`` to **Winphone8**, i.e:

   .. code-block:: 
   
      ...
      <API_Family>Winphone8</API_Family>
      ...

   .. note:: 

      If ``pjproject-vs14.sln`` solution is opened, you need to close and reopen 
      the solution after changing API family.

#. Open ``pjproject-vs14.sln`` solution file.
#. Set **ARM** as the solution platform.
#. Set **pjsua_cli_wp** as Startup Project.
#. Build the project. This will build **pjsua_cli_wp** application and 
   all libraries needed by **pjsua_cli_wp**.
#. Run/deploy the **pjsua_cli_wp** application on a registered Windows phone device.
#. You will see telnet instructions on the device's screen. Telnet to this address 
   to operate the application. 
   See :doc:`CLI Manual </specific-guides/other/cli_cmd>` for command reference.

Debugging Application
----------------------

To Debug native(C/C++) part of the application:

* Set the **Debugger type** of project properties [Debug menu] to **Native Only**.

To Debug managed(C#) part of the application:

* Set the **Debugger type** of project properties [Debug menu] to **Managed Only**.

Assert Problem on Debugging Native Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As described `<here http://blogs.msdn.com/b/andypennell/archive/2013/06/17/native-code-on-windows-phone-8-the-assert-problem.aspx>`, 
assertion will cause process exiting (instead of just stopping). 
Adding the following code in the application would make process stopping on 
assertion:

.. code-block:: 

   #ifndef NDEBUG   
   signal(SIGABRT, [](int)
   {
      __debugbreak();  
   }); 
   #endif

Other References
-----------------

 * `VoIP apps for Windows Phone 8 <http://msdn.microsoft.com/en-us/library/windowsphone/develop/jj206983%28v=vs.105%29.aspx>`__ 
 * Ticket :pr:`1900` about porting to Windows 10/UWP
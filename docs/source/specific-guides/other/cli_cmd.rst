PJSUA Command Line Interface (CLI) Manual
==========================================

Introduction
-------------

CLI is a feature of pjsua that enables user to execute commands from telnet/console interface.

Features:

* Command completion, the system will detect if a fraction of a word makes up a unique command.
* Arguments/command-params completion.
* Command history (the use of up and down arrow).

CLI mode is enabled/disabled by running pjsua with these options:

.. list-table:: 
   :header-rows: 0

   * - **--use-cli**
     - Enables CLI mode
   * - **--cli-telnet-port=PORT**
     - elnet port, set 0 to disable telnet (default=0)
   * - **--no-cli-console**
     - Disable console interface

.. note:: 

   for mobile pjsua (iOS, BB10, Symbian) CLI (telnet) will be enabled by default.

Commands
---------

Commands are specified using tree structure (commands/sub-commands).

  e.g : to make new call use ("**call new sip:localhost**")

Command shortcuts are executed on the root command without the need to specify the full command path.

  e.g : to hangup call use ("**g**") and not ("**call g**")

Some commands might need parameters/arguments to be entered. There are 3 types of arguments:

* Choice. User needs to pick the option from the option list (by typing “tab” or “?” key).
  
  e.g : select next account ("**acc next**") + tab
   
  .. code-block:: shell

     [0]   <sip:192.168.1.6:5060>
     [1]   *<sip:192.168.1.6:5060;transport=TCP>
     [2]   <sip:192.168.1.6:5061;transport=TLS>
   
  Expected input : 0/1/2. ("**acc next 1**")

* Input. User needs to specify the input required by the commands.

  e.g : answer call ("**call answer**") + tab
  
  .. code-block:: shell

     <code> Answer code
   
  Expected input : answer code ("**call answer 200**")

* Mixed. User is presented by Choice type and input type.

  e.g : make new call ("call new") + tab
  
  .. code-block:: shell

     [-1]   All buddies
     [0]    Current dialog
     [URL]  An URL

  Expected input : -1/0/destination ("**call new 0**" or "**call new sip:localhost**")

The following commands can be specified when invoking pjsua in CLI mode.

Root commands
^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **log**
     - 
     - Change log level
   * - **exit**
     - 
     - Exit session
   * - **call**
     - 
     - Call and related commands
   * - **im**
     - 
     - IM and presence commands
   * - **acc**
     - 
     - Account commands
   * - **audio**
     - 
     - Conference and media commands
   * - **stat**
     - 
     - Status and config commands
   * - **sleep**
     - 
     - Suspend keyboard input
   * - **network**
     - 
     - Detect network type
   * - **shutdown**
     - 
     - Shutdown application
   * - **restart**
     - 
     - Restart application

Call and related commands [**call**]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **new**
     - 
     - Make a new call/INVITE
   * - **multi**
     -
     -  Make multiple calls
   * - **answer**
     - 
     - Answer call
   * - **hangup**
     - **g**
     - Hangup call
   * - **hangup_all**
     - **hA**
     - Hangup all call
   * - **hold**
     - **H**
     - Hold call
   * - **reinvite**
     - **v**
     - Re-invite (release hold)
   * - **update**
     - **U**
     - Send update request
   * - **next**
     - **]**
     - Select next call
   * - **previous**
     - **[**
     - Select previous call
   * - **transfer**
     - **x**
     - Transfer call
   * - **transfer_replaces**
     - **X**
     - Transfer replace call
   * - **redirect**
     - **R**
     - Redirect call
   * - **d_2833**
     - **#**
     - Send DTMF (RFC 2833)
   * - **d_info**
     - **\***
     - Send DTMF with SIP INFO
   * - **dump_q**
     - **dq**
     - Dump (call) quality
   * - **send_arb**
     - **S**
     - Send arbitrary request
   * - **list**
     -
     - Show current call

IM and Presence commands [**im**]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **add_b**
     - **+b**
     - Add buddy
   * - **del_b**
     - **-b**
     - Delete buddy
   * - **send_im**
     - **i**
     - Send IM
   * - **sub_pre**
     - 
     -  Subscribe presence
   * - **unsub_pre**
     - 
     - Unsubscribe presence
   * - **tog_state**
     - 
     - Toggle online state
   * - **pre_text**
     - **T**
     - Specify custom presence text
   * - **bud_list**
     - **b**
     - Show buddy list

Account commands [**acc**]
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **add**
     - **+a**
     - Add new account
   * - **del**
     - **-a**
     - Delete account
   * - **mod**
     - **!a**
     - Modify account
   * - **reg**
     - **rr**
     - Send (Refresh) register request to register
   * - **unreg**
     - **ru**
     - Send Register request to unregister
   * - **next**
     - **<**
     - Select the next account for sending outgoing requests
   * - **previous**
     - **>**
     - Select the previous account for sending outgoing requests
   * - **show**
     - **l**
     - Show account list

Conference and Media commands [**audio**]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **list**
     - **cl**
     - Show conference list
   * - **conf_con**
     - **cc**
     - Conference connect
   * - **conf_dis**
     - **cd**
     - Conference disconnect
   * - **adjust_vol**
     - **V**
     - Adjust volume
   * - **codec_prio**
     - **Cp**
     - Arrange codec priorities

Status and config commands[**stat**]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **dump_stat**
     - **ds**
     - Dump status
   * - **dump_detail**
     - **dd**
     -  Dump detail status
   * - **dump_conf**
     - **dc**
     - Dump configuration to screen
   * - **write_setting**
     - **f**
     - Write current configuration file

Video commands [**video**]
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **enable**
     - 
     - Enable video
   * - **disable**
     - 
     - Disable video
   * - **acc**
     - 
     - Video setting for current account
   * - **call**
     - **vcl**
     - Video call commands/settings
   * - **device**
     - **vv**
     - Video device commands
   * - **codec**
     - 
     - Video codec commands
   * - **win**
     - 
     - Video windows settings/commands

Video setting for current account [**video acc**]
``````````````````````````````````````````````````

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **rx**
     -
     - Enable/disable video RX for stream in curr call
   * - **tx**
     -
     - Enable/disable video TX for stream in curr call
   * - **add**
     -
     - Add video stream for current call
   * - **enable**
     -
     - Enable stream #N in current call
   * - **disable**
     -
     - Disable stream #N in current call
   * - **cap**
     -
     - Set capture dev ID for stream #N in current call

Video call commands/settings [**video call**]
`````````````````````````````````````````````

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **rx**
     - 
     - Enable/disable video RX for stream in curr call
   * - **tx**
     - 
     - Enable/disable video TX for stream in curr call
   * - **add**
     - 
     - Add video stream for current call
   * - **enable**
     - 
     - Enable stream #N in current call
   * - **disable**
     - 
     - Disable stream #N in current call
   * - **cap**
     - 
     - Set capture dev ID for stream #N in current call

Video device commands [**video device**]
````````````````````````````````````````

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **list**
     - 
     - Show all video devices
   * - **refresh**
     - 
     - Refresh video device list
   * - **prev**
     - 
     - Enable/disable preview for specified device ID

Video codec commands [**video codec**]
````````````````````````````````````````

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **list**
     -
     - Show video codec list
   * - **prio**
     -
     - Set video codec priority
   * - **fps**
     -
     - Set video codec framerate
   * - **bitrate**
     -
     - Set video codec bitrate
   * - **size**
     -
     - Set codec ID size/resolution

Video windows settings/commands [**video win**]
```````````````````````````````````````````````

.. list-table:: 
   :header-rows: 1

   * - Commands
     - Shortcut
     - Description
   * - **list**
     - 
     - List all active video windows
   * - **arrange**
     - 
     - Auto arrange windows
   * - **show**
     - 
     - Show specific windows
   * - **hide**
     - 
     - Hide specific windows
   * - **move**
     - 
     - Move window position
   * - **resize**
     - 
     - Resize window to specific width/height

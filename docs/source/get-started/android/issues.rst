Common issues when developing Android SIP client
==================================================

.. contents:: Common issues:
   :local:
   :depth: 2


Pjsua2 keeps stopping during startup
------------------------------------------------------------------


Failed to load native library pjsua2
------------------------------------------------------------------

::

  W  Failed to load native library pjsua2
  W  java.lang.UnsatisfiedLinkError: dlopen failed: library "libpjsua2.so" not found

There can be several reasons for that, below are some that are quite common:

* If it is your own application, check that you have copied the native libraries to directory
  **<YOUR-APP>/src/main/jniLibs/<ARCH>**. At the very minimum, you need to copy:

  * **libpjsua2.so**
  * **libc++_shared.so**

* If you have enabled additional/optional features when building PJSIP, you need to copy the relevant
  shared libraries to the directory above, or otherwise ``libpjsua2.so`` will fail to load.
  For example:

  * **libcrypto.so** and **libssl.so** for OpenSSL, 
  * **liboboe.so** for OBOE sound device, 
  * **libopenh264.so** for OpenH264 codecs.

* On Linux, you can check what libraries ``libpjsua2.so`` depends on by executing this command:

  ::

      $ readelf --dynamic libpjsua2.so | grep NEEDED

* Of course you need to build PJSIP for the correct architecture, otherwise ``libpjsua2.so``
  will fail to load (rather misleadingly with *"not found"* exception). For example, it might
  worth mentioning that the Android Studio emulator's architecture is ``x86_64``, not ``arm64-v8a``.
* You can check that the correct libraries are packaged correctly by opening the **.apk** file
  with an archiver and look at the libraries in the **lib** directory, under the correct
  architecture. If it is not there, check the Gradle script or other packaging script that you
  use.


Failed to load native library libssl.so
------------------------------------------------------------------
Follow the instructions in :ref:`android_copy_3rd_party_libs`.


Failed to load native library libcrypto.so
------------------------------------------------------------------
Follow the instructions in :ref:`android_copy_3rd_party_libs`.


Failed to load native library liboboe.so
------------------------------------------------------------------
Follow the instructions in :ref:`android_copy_3rd_party_libs`.


Failed to load native library openh264
------------------------------------------------------------------

::

  W  Failed to load native library openh264
  W  java.lang.UnsatisfiedLinkError: dlopen failed: library "libopenh264.so" not found
  I  This could be safely ignored if you don't use OpenH264 video codec.


As the message says, you can ignore it if you're not using OpenH264. Otherwise follow the OpenH264
installation instructions to install it properly.


No implementation found for void org.pjsip.pjsua2.pjsua2JNI.swig_module_init()
-------------------------------------------------------------------------------
This usually is the follow up error of *Failed to load native library pjsua2* error above.


Find library dependencies
------------------------------------------------------------------
Command to see what shared libraries are needed by **libpjsua.so**:

::

  $ readelf --dynamic libpjsua.so | grep NEEDED


Unable to make or receive call due to large message size
------------------------------------------------------------------
Problem with sending and receiving large (INVITE) requests over TCP.
The issue is documented in :issue:`1488`. The solution is to try using port other 
than 5060 in **both** client and server, and/or reducing the SIP message size,
as explained in :any:`/specific-guides/sip/reducing_size`.

Garbage Collector May Crash Your App (Pjsua2 API)
------------------------------------------------------
Please check this PJSUA2 section: :any:`gc_problems`.

OpenSLES audio device deadlock upon shutdown
----------------------------------------------------
As reported in `Android NDK forum <https://groups.google.com/forum/#!topic/android-ndk/G7dLKAGGL28>`__, 
when shutting down OpenSLES sound device backend, it may block forever:

.. code-block:: 

      W/libOpenSLES(6434): frameworks/wilhelm/src/itf/IBufferQueue.c:57: pthread 0x5fce71c0 (tid 6670) sees object 0x5fcd0080 was locked by pthread 0x5f3a2cb0 (tid 6497) at frameworks/wilhelm/src/itf/IObject.c:411

Currently, the only workaround is to use PJSIP's Android JNI sound device instead 
(one way to do this is by defining 
:c:macro:`PJMEDIA_AUDIO_DEV_HAS_ANDROID_JNI` to 1 and :c:macro:`PJMEDIA_AUDIO_DEV_HAS_OPENSL` to 0).

Bad audio recording quality on some devices
--------------------------------------------------
Reported that audio quality recorded on the microphone is bad and the speed is 
twice what it should be, it only happens on some devices. It could be fixed 
by setting audio mode via ``AudioManager`` to ``MODE_IN_COMMUNICATION`` in the 
application, e.g:

.. code-block:: java

      AudioManager am = (AudioManager) getSystemService(Context.AUDIO_SERVICE);
      int original_mode = am.getMode();

      /* Set audio mode before using audio device, for example before making/answering a SIP call */
      am.setMode(AudioManager.MODE_IN_COMMUNICATION);
      ...
      /* Restore back to the original mode after finished with audio device */
      am.setMode(original_mode);

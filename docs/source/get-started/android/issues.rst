Important Issue(s) when Developing Android Apps
***********************************************

*  **Unable to Make or Receive Call (Problem with sending and receiving large (INVITE) requests over TCP)**

   The issue is documented in :pr:`1488`. The solution is to try using port other 
   than 5060 in **both** client and server, and/or reducing the SIP message size.

*  **Garbage Collector May Crash Your App (Pjsua2 API)**

   Please check this pjsua2 book page about 
   `problems with GC <http://www.pjsip.org/docs/book-latest/html/intro_pjsua2.html#problems-with-garbage-collection>`__.

*  **OpenSLES audio device deadlock upon shutdown**

   As reported in `Android NDK forum <https://groups.google.com/forum/#!topic/android-ndk/G7dLKAGGL28>`__, 
   when shutting down OpenSLES sound device backend, it may block forever:

   .. code-block:: 

      W/libOpenSLES(6434): frameworks/wilhelm/src/itf/IBufferQueue.c:57: pthread 0x5fce71c0 (tid 6670) sees object 0x5fcd0080 was locked by pthread 0x5f3a2cb0 (tid 6497) at frameworks/wilhelm/src/itf/IObject.c:411

   Currently, the only workaround is to use PJSIP's Android JNI sound device instead 
   (one way to do this is by defining 
   ``PJMEDIA_AUDIO_DEV_HAS_ANDROID_JNI`` to 1 and ``PJMEDIA_AUDIO_DEV_HAS_OPENSL`` to 0).

*  **Bad audio recording quality on some devices**

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

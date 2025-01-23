Adding optional features
=======================================

.. contents:: In this page:
   :depth: 2
   :local:



Installing OpenH264 (optional)
----------------------------------
#. For general information on OpenH264 integration see :ref:`openh264`
#. Copy all library .so files into your Android application project directory, 
   for example:

   .. code-block:: shell

     cp /Users/me/openh264/android/*.so /Users/me/pjproject-2.0/pjsip-apps/src/swig/java/android/libs/armeabi


Installing libvpx (optional)
-----------------------------------
See :ref:`libvpx`


Installing ffmpeg (optional)
------------------------------------
See :doc:`/specific-guides/build_int/ffmpeg`


Installing AMediaCodec, native Android codecs (experimental)
-----------------------------------------------------------------
See :ref:`amediacodec`



Video Support
-------------------


Configuring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specify third-party video libraries when invoking ``./configure-android``, e.g:

.. code-block:: shell

   $ ./configure-android --with-openh264=/Users/me/openh264/android

Make sure openh264 is detected by ``./configure-android``:

.. code-block:: shell

   ...
   Using OpenH264 prefix... /Users/me/openh264/android
   checking OpenH264 availability... ok
   ...

.. note:: 

   If you use PJSIP before version 2.6, you need to specify external libyuv via 
   the configure script param ``--with-libyuv``, check :pr:`1776` for more info.

Adding Video Capture Device to Your Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Copy the java part of PJSIP Android capture device to the application's source 
directory:

.. code-block:: shell

   cp pjmedia/src/pjmedia-videodev/android/PjCamera*.java [your_app]/src/org/pjsip/


Since 2.12, the capture device uses ``Camera2`` API (see also :pr:`2797` for 
more info), application need to configure the ``CameraManager`` instance 
in ``PjCameraInfo2`` before using the camera, e.g:

.. code-block:: java

   @Override protected void onCreate(Bundle savedInstanceState)
   {
      //..
      CameraManager cm = (CameraManager)getSystemService(Context.CAMERA_SERVICE);
      PjCameraInfo2.SetCameraManager(cm);
      //..
   }

Using Video API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please check :doc:`Working with Video </pjsua2/using/media_video>` (PJSUA2 Guide).

Video capture orientation support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To send video in the proper orientation (i.e. head always up regardless of the 
device orientation), application needs to do the following:

#. Setup the application to get orientation change notification 
   (by adding ``android:configChanges="orientation|keyboardHidden|screenSize"`` 
   in the application manifest file and override the callback ``onConfigurationChanged()``).
#. Inside the callback, call PJSUA2 API ``VidDevManager::setCaptureOrient()`` 
   to set the video device to the correct orientation.

For sample usage, please refer to pjsua2 sample app. Ticket :pr:`1861` explains 
this feature in detail.

.. _android_openssl:

OpenSSL Support
-------------------
#. Build OpenSSL (tested with OpenSSL 1.0.2s) for Android.
   The instruction provided here is specifically for arm64. 
   For other architectures, modify accordingly. 

   Please visit `this page <https://github.com/openssl/openssl/blob/master/NOTES-ANDROID.md>`__ 
   for reference and some examples. 

   .. note:: 

      You need to change the NDK path and the API platform level below.

   .. code-block:: shell

      cd openssl-3.0.4

      export ANDROID_NDK_ROOT=[your_android_ndk_path]

      # Change the host as required (e.g: linux -> darwin)
      PATH=$ANDROID_NDK_ROOT/toolchains/llvm/prebuilt/linux-x86_64/bin:$ANDROID_NDK_ROOT/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin:$PATH

      ./Configure android-arm64 -D__ANDROID_API__=29

      make

   Then copy the libraries into lib folder:

   .. code-block:: shell

      mkdir lib
      cp lib*.a lib/

#. Specify OpenSSL location when running ``configure-android``, for example 
   (with Bash): (change the openssl path folder)

   .. code-block:: shell

      TARGET_ABI=arm64-v8a ./configure-android --use-ndk-cflags --with-ssl=[your_openssl_path]

   And check that OpenSSL is detected by the configure script:

   .. code-block::

      ...
      checking for OpenSSL installations..
      checking openssl/ssl.h usability... yes
      checking openssl/ssl.h presence... no
      aconfigure: WARNING: openssl/ssl.h: accepted by the compiler, rejected by the preprocessor!
      aconfigure: WARNING: openssl/ssl.h: proceeding with the compiler's result
      checking for openssl/ssl.h... yes
      checking for ERR_load_BIO_strings in -lcrypto... yes
      checking for SSL_library_init in -lssl... yes
      OpenSSL library found, SSL support enabled
      ...

#. Build the libraries:

   .. code-block:: shell

      make dep && make

   If you encounter linking errors, you need to add this in ``user.mak``:

   .. code-block:: shell

      export LIBS += "-ldl -lz"


Low latency audio device
------------------------
Oboe offers low latency audio and some other benefits, please check `here <https://developer.android.com/games/sdk/oboe>`__ for more info.
Oboe is supported since PJSIP version 2.12. To enable Oboe, please follow steps described in :pr:`2707`.


Trying our sample application and creating your own
---------------------------------------------------------

Setting up the target device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run or debug application (such as the sample applications below), 
first we need to setup the target device: 

* using virtual device: http://developer.android.com/tools/devices/index.html
* using real device: http://developer.android.com/tools/device.html

.. _android_pjsua2:

Building and running pjsua2 sample applications (Java & Kotlin)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sample applications using :doc:`pjsua2 API </api/pjsua2/ref>` with SWIG Java binding 
is located under :source:`pjsip-apps/src/swig/java/android`. It is not built by 
default, and you need `SWIG <http://www.swig.org/download.html>`__ to build it.

Follow these steps to build pjsua2 sample applications:

#. Make sure SWIG is in the build environment PATH.
#. Run ``make`` from directory :source:`pjsip-apps/src/swig` (note that the 
   Android NDK root should be in the PATH), e.g:

   .. code-block:: shell

      $ cd /path/to/your/pjsip/dir
      $ cd pjsip-apps/src/swig
      $ make

   This step should produce:

   * native library ``libpjsua2.so`` in ``pjsip-apps/src/swig/java/android/pjsua2/src/main/jniLibs/arm64-v8a``

     .. note::
 
        If you are building for other target ABI, you'll need to manually move ``libpjsua2.so`` 
        to the appropriate target ABI directory, e.g: ``jniLibs/armeabi-v7a``, 
        please check `here <https://developer.android.com/ndk/guides/abis.html#am>`__ 
        for target ABI directory names.

   * pjsua2 Java interface (a lot of ``.java`` files) in 
     `pjsip-apps/src/swig/java/android/pjsua2/src/main/java/org/pjsip/pjsua2`

#. Make sure any library dependencies are copied to 
   ``pjsip-apps/src/swig/java/android/pjsua2/src/main/jniLibs/arm64-v8a``
   (or the appropriate target ABI directory), e.g: ``libopenh264.so`` for video 
   support.
#. Open pjsua2 project in Android Studio, it is located in 
   :source:`pjsip-apps/src/swig/java/android`.
   It will contain three modules:
   - pjsua2 Java interface: :source:`pjsip-apps/src/swig/java/android/pjsua2`
   - Java sample app: :source:`pjsip-apps/src/swig/java/android/app`
   - Kotlin sample app: :source:`pjsip-apps/src/swig/java/android/app-kotlin`
#. Run sample app.

**Log output**

The pjsua2 sample applications will write log messages to **LogCat** window.

.. _android_create_app:

Creating your own application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For developing Android application, you should use :doc:`pjsua2 API </api/pjsua2/ref>` 
whose Java interface available via SWIG Java binding.

#. First, build ``pjproject`` libraries as described above.
#. Also build ``pjsua2 sample application`` as described above, this step is 
   required to generate the pjsua2 Java interface and the native library.
#. Create Android application outside the PJSIP sources for your project.
#. Get pjsua2 Java interface and native library from pjsua2 sample application:

   #. Copy pjsua2 Java interface files from 
      ```pjsip-apps/src/swig/java/android/app/src/main/java`` to your 
      project's ``app/src/main/java`` folder, e.g:

      .. code-block:: shell

         $ cd $YOUR_PROJECT_DIR/app/src/main/java
         $ cp -r $PJSIP_DIR/pjsip-apps/src/swig/java/android/app/src/main/java .

         # Cleanup excess pjsua2 application sources.
         $ rm -r org/pjsip/pjsua2/app

   #. Copy native library ``libpjsua2.so`` from 
      ``pjsip-apps/src/swig/java/android/app/src/main/jniLibs`` to your 
      project's ``app/src/main/jniLibs`` folder:

      .. code-block:: shell

         $ cd $YOUR_PROJECT_DIR/app/src/main/jniLibs
         $ cp -r $PJSIP_DIR/{pjsip-apps/src/swig/java/android/app/src/main/jniLibs .

#. Start writing your application, please check 
   `pjsua2 docs <http://www.pjsip.org/docs/book-latest/html/index.html>`__ for 
   reference.

Pjsua sample application with telnet interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is also the usual `pjsua <http://www.pjsip.org/pjsua.htm>`__ with telnet 
command line user interface, which is located under :source:`pjsip-apps/src/pjsua/android`. 
It is not built by default and you need `SWIG <http://www.swig.org/download.html>`__ 
to build it. Application flow and user interface are handled mainly in the native 
level, so it doesn't use pjsua2 API with Java interface.

Follow these steps to build pjsua:

#. Make sure that pjsua app is included on the build.
   
   Call this before calling ``configure-android``

   .. code-block:: shell

      EXPORT EXCLUDE_APP=0

#. Proceed to normal build by calling ``configure-android``, ``make dep``, ``make``
#. Make sure SWIG is in the build environment PATH.
   Alternatively, update SWIG path in :source:`pjsip-apps/src/pjsua/android/jni/Makefile` 
   file.
#. Run ``make`` from directory :source:`pjsip-apps/src/pjsua/android/jni`. 
   The Android NDK root should be in the PATH, e.g:
   
   .. code-block:: shell

      $ cd /path/to/your/pjsip/dir
      $ cd pjsip-apps/src/pjsua/android/jni
      $ make

#. Open pjsua2 app project in Android Studio, it is located in 
   :source:`pjsip-apps/src/pjsua/android`.
#. Run it.
#. You will see telnet instructions on the device's screen. Telnet to this 
   address to operate the application. See 
   :doc:`CLI Manual </specific-guides/other/cli_cmd>`.


Kotlin Support
^^^^^^^^^^^^^^
To develop PJSIP app using Kotlin, please take a look at :pr:`2648`

Creating your own application
=======================================

.. contents:: In this page:
   :depth: 2
   :local:



.. _android_create_app:

Creating your own application
------------------------------------------

Creating your own Android SIP application based on PJSIP typically involves the following steps.

#. We assume that PJSIP native libraries have been built by following the previous guide in
   :doc:`/get-started/android/build_instructions`, including the JNI (SWIG) interface.
#. Create Android application outside the PJSIP sources for your project.
#. Copy ``libpjsua2.so`` and ``libc++_shared.so`` to your **jniLibs/$ARCH** directory:

   .. code-block:: shell

      $ cd $YOUR_PROJECT_DIR/app/src/main/jniLibs
      $ cp -r $PJSIP_DIR/pjsip-apps/src/swig/java/android/pjsua2/src/main/jniLibs/* .
      $ ls -R
      arm64-v8a

      ./arm64-v8a:
      libcrypto.so  libc++_shared.so  liboboe.so  libpjsua2.so  libssl.so

#. You will see the third party libs (OpenSSL, Oboe) in the ``ls`` output above if you have followed the
   previous tutorial to develop the sample Java application. If you only see ``libpjsua2.so`` and
   ``libc++_shared.so``, follow the guide in :ref:`android_copy_3rd_party_libs`. After
   that, you should see the **jniLibs** contents like above.
#. Copy pjsua2 Java interface files from ``pjsip-apps/src/swig/java/android/app/src/main/java`` to your 
   project's ``app/src/main/java`` folder, e.g:

   .. code-block:: shell

      $ cd $YOUR_PROJECT_DIR/app/src/main/java
      $ cp -r $PJSIP_DIR/pjsip-apps/src/swig/java/android/app/src/main/java/* .

      # check
      $ ls
      org

      # Cleanup excess pjsua2 application sources.
      $ rm -r org/pjsip/pjsua2/app

#. Start writing your application, by following these guides:

   - :doc:`pjsua2 Guide </pjsua2/intro>`
   - :doc:`pjsua2 API reference and samples </api/pjsua2/index>`



Adding Video Capture Device to Your Application
-------------------------------------------------------

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
-----------------------------------
Please check :doc:`Working with Video </pjsua2/using/media_video>` (PJSUA2 Guide).


Video capture orientation support
-------------------------------------------

To send video in the proper orientation (i.e. head always up regardless of the 
device orientation), application needs to do the following:

#. Setup the application to get orientation change notification 
   (by adding ``android:configChanges="orientation|keyboardHidden|screenSize"`` 
   in the application manifest file and override the callback ``onConfigurationChanged()``).
#. Inside the callback, call PJSUA2 API ``VidDevManager::setCaptureOrient()`` 
   to set the video device to the correct orientation.

For sample usage, please refer to pjsua2 sample app. Ticket :pr:`1861` explains 
this feature in detail.



Installing additional components
-----------------------------------

.. _android_openh264:

Installing OpenH264 (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note that OpenH264 is optional because native H.264 codec is already provided by :ref:`amediacodec`.

#. Build OpenH264 for Android. See :ref:`openh264` for more information.
#. Run **configure-android** with specifying OpenH264 directory, e.g.:

   .. code-block:: shell

      $ ./configure-android --with-openh264=/Users/me/openh264/android

#. Make sure openh264 is detected:

   .. code-block:: shell

      ...
      Using OpenH264 prefix... /Users/me/openh264/android
      checking OpenH264 availability... ok
      ...

   .. note:: 

      If you use PJSIP before version 2.6, you need to specify external libyuv via 
      the configure script param ``--with-libyuv``, check :pr:`1776` for more info.

#. Copy all library's **.so** files into your Android application's **jniLibs/$ARCH** directory,
   as explained in :ref:`android_copy_3rd_party_libs`. For example:

   .. code-block:: shell

     $ cd pjsip-apps/src/swig/java/android/pjsua2/src/main/jniLibs/arm64-v8a
     $ cp /Users/me/openh264/android/*.so .




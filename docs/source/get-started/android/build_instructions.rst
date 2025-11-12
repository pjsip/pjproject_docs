Configure and build PJSIP for Android
=======================================

In this section, we will configure and build PJSIP as a native library for Android, and
:doc:`PJSUA2 API </api/pjsua2/index>` Java/JNI interface that can be used by Android Java and
Kotlin applications.


.. contents:: Configuration and build steps:
   :depth: 2
   :local:


Create *config_site.h*
-----------------------------------

Create :ref:`pjlib/include/pj/config_site.h <dev_start>` file with a text editor and set the
contents to the following:

.. code-block:: c

   /* Activate Android specific settings in the 'config_site_sample.h' */
   #define PJ_CONFIG_ANDROID 1
   #include <pj/config_site_sample.h>

   #define PJMEDIA_HAS_VIDEO 1


The rest of the configurations will be set by the configure script below.

  
Configuring PJSIP
---------------------------------
Using ``OPENSSL_DIR`` and ``OBOE_DIR`` environment variables that we set earlier in the previous
page, run the configure commands below, replacing the Android NDK path with the correct path:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ export ANDROID_NDK_ROOT=/home/whoever/Android/android-sdk/ndk/28.0.12916984
   $ ./configure-android -with-ssl=$OPENSSL_DIR --with-oboe=$OBOE_DIR

Using the default setting will build NDK's default target architecture (currently **arm64-v8a**). See next
section for building other targets.

.. tip:: 

   On MinGW32/MSys, use absolute path format ``D:/path/to/android/ndk`` 
   instead of ``/D/path/to/android/ndk`` for ``ANDROID_NDK_ROOT``.

.. tip:: 

   * The ``./configure-android`` is a wrapper that calls the standard ``./configure`` 
     script with settings suitable for Android target. Standard ``./configure`` 
     options should be applicable to this script too.
   * Please check ``./configure-android --help`` for more info.
   * Other customizations are similar to what is explained in 
     :doc:`Building with GNU Tools/Autoconf </get-started/posix/build_instructions>` 
     page.

Specifying Android API level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify the Android API level target in ``APP_PLATFORM``. For example:

.. code-block:: shell

   APP_PLATFORM=23 ./configure-android --with-ssl=$OPENSSL_DIR --with-oboe=$OBOE_DIR

.. note::

   Some features may require a specific minimum API level. For example:

   * Third party libraries that use ``stdout`` and ``stderr`` (e.g: OpenSSL, OpenH264) may not
     be detected properly by the configure on API level below 23.
   * Native Android audio & video codecs require API level 28 or higher.

.. note::

   * If you build third party libraries from the source (such as OpenSSL), you need to rebuild them
     for the same API level as well.

   * If you have built PJSIP for other API level, it's recommended to clean it up first before running
     configure above:

     .. code-block:: shell

        $ cd /path/to/pjproject
        $ make distclean

Configuring for other architectures (including emulator)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specify the target arch in ``TARGET_ABI`` and run it with ``--use-ndk-cflags``. For example,
for targetting the emulator:

.. code-block:: shell

   TARGET_ABI=x86_64 ./configure-android --use-ndk-cflags ...

.. note::

   * If you build third party libraries from the source (such as OpenSSL), you need to rebuild them
     for the same architecture as well.

   * If you have built PJSIP for other architecture, it's recommended to clean it up first before running
     configure above:

     .. code-block:: shell

        $ cd /path/to/pjproject
        $ make distclean


Supporting 16 KB page sizes (Android 15)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As described in `Android official doc <https://developer.android.com/guide/practices/page-sizes>`__,
Android from version 15 onwards supports devices that are configured to use a page size of 16 KB
(16 KB devices).

In order for PJSIP to support flexible page sizes (both 4 and 16 KB), you need to use NDK r27 or later and apply https://github.com/pjsip/pjproject/pull/4068. Alternatively, you can manually specify the build flags to the configure script:

.. code-block:: shell

    CFLAGS="-D__BIONIC_NO_PAGE_SIZE_MACRO" LDFLAGS="-Wl,-z,max-page-size=16384" ./configure-android


Verifying configuration
---------------------------------
Now we need to check that all the intended features are detected by ``./configure-android`` script
by observing the configure output:

* Check that OpenSSL is detected and enabled:

.. code-block::

   checking for OpenSSL installations..
   checking for openssl/ssl.h... yes
   checking for ERR_load_BIO_strings in -lcrypto... yes
   checking for SSL_CTX_new in -lssl... yes
   OpenSSL library found, SSL support enabled

* Check that Oboe is detected and enabled:

.. code-block::

   checking Oboe usability... yes
   Checking sound device backend... Oboe


Building PJSIP
---------------------------------
Now we can build PJSIP with:

.. code-block:: shell

   $ make dep && make clean && make



Building PJSUA2 Java interface with SWIG
-----------------------------------------------------

#. Set ``JAVA_HOME`` environment variable to the directory containing ``javac`` executable. Since
   we have installed Android Studio, I find this to be the easiest:

   .. code-block:: shell

      $ export JAVA_HOME=/path/to/android-studio/jbr/bin


#. Build the SWIG interface:

   .. code-block:: shell

      # In pjproject dir
      $ cd pjsip-apps/src/swig
      $ make


This produces the following artefacts:

::

    pjsip-apps/src/swig/java/android/pjsua2/src/main
    ├── jniLibs/<ARCH>
    │   ├── libpjsua2.so
    │   └── libc++_shared.so
    ├── java/org/pjsip/pjsua2
    │   └── *.java


.. _android_copy_3rd_party_libs:

Copy third party native libraries
-----------------------------------------------------
You need to manually copy third party native libraries that are used by PJSIP to **jniLibs/$ARCH** 
directory of the Android application so that they are packaged with the application. So far we have added OpenSSL and Oboe
as our dependencies, so we will copy them. Follow the steps below.

1. Go to the directory of your Android application (the directory that has
   ``build.gradle`` file and that needs the native libs), for example :source:`pjsip-apps/src/swig/java/android/pjsua2/`.
2. Set the arch which you want to copy.

   .. code-block:: shell

      # Replace ARCH with arm64-v8a, x86_64, or whatever arch
      $ export ARCH=arm64-v8a
      $ cd src/main/jniLibs/$ARCH

3. Copy OpenSSL libs:

   .. code-block:: shell

      $ cp -v $OPENSSL_DIR/lib/*.so .
      '/home/whoever/Android/openssl-3.4.0/lib/libcrypto.so' -> './libcrypto.so'
      '/home/whoever/Android/openssl-3.4.0/lib/libssl.so' -> './libssl.so'

4. Copy Oboe libs:

   .. code-block:: shell

      $ cp -v $OBOE_DIR/prefab/modules/oboe/libs/android.$ARCH/*.so .
      '/home/whoever/Android/oboe-1.9....oid.arm64-v8a/liboboe.so' -> './liboboe.so'

5. Check the libraries to be packaged:

   .. code-block:: shell

      $ ls
      libcrypto.so  libc++_shared.so  liboboe.so  libpjsua2.so  libssl.so


What's next
---------------------------
The PJSIP library, the JNI interface, and the third party libraries are ready. Now we are ready do build
the sample applications.



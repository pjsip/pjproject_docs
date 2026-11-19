Build with CMake
=======================================

In this section, we will build PJSIP as a native library for Android, and
:doc:`PJSUA2 API </api/pjsua2/index>` Java/JNI interface that can be used by Android Java and
Kotlin applications, using CMake. The result is the same as :doc:`build_gnu`, and the sample
applications use it the same way.

.. note::

   Supported since release 2.18. See :doc:`/get-started/cmake/index` for CMake in general.


.. contents:: Configuration and build steps:
   :depth: 2
   :local:


Requirements
-----------------------------------
In addition to what we installed in :doc:`requirements`:

* **CMake 3.28** or newer, from Android Studio's SDK Manager (*SDK Tools* tab, *CMake*), from
  `cmake.org <https://cmake.org/download/>`__, or from your package manager. Check with
  ``cmake --version``.
* **Ninja**, only if Gradle is to drive CMake (see :ref:`android_cmake_gradle` below). The SDK
  Manager's CMake includes it.

No JDK is needed for this step: Gradle compiles the Java classes when the application is built.


Create *config_site.h*
-----------------------------------
Create :ref:`pjlib/include/pj/config_site.h <dev_start>` file with a text editor and set the
contents to the following:

.. code-block:: c

   /* Activate Android specific settings in the 'config_site_sample.h' */
   #define PJ_CONFIG_ANDROID 1
   #include <pj/config_site_sample.h>

This is the same as for :doc:`build_gnu`, so a *config_site.h* from there works as it is. Video is
on by default with CMake, so ``PJMEDIA_HAS_VIDEO`` is not needed.

.. warning::

   Note that settings in *config_site.h* can clash with CMake options, and silently override them,
   so changing the option later can cause link errors. For anything that has a CMake option, such
   as video, use the option rather than *config_site.h*. See
   :ref:`config_site.h with CMake <cmake_config_site>`.


Configuring PJSIP
---------------------------------
Using ``OPENSSL_DIR`` and ``OBOE_DIR`` environment variables that we set earlier in
:doc:`requirements`, run the commands below, replacing the Android NDK path with the correct path:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ export ANDROID_NDK_ROOT=/home/whoever/Android/android-sdk/ndk/28.0.12916984
   $ cmake -B build-android \
         -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK_ROOT/build/cmake/android.toolchain.cmake \
         -DCMAKE_BUILD_TYPE=Release \
         -DPJ_BUILD_SWIG_JAVA=ON \
         -DPJLIB_WITH_SSL=openssl -DOPENSSL_ROOT_DIR=$OPENSSL_DIR \
         -DOboe_ROOT=$OBOE_DIR

* ``-DPJ_BUILD_SWIG_JAVA=ON`` builds the PJSUA2 Java interface with SWIG.
* ``-DPJLIB_WITH_SSL=openssl`` makes configure fail if OpenSSL cannot be used, rather than
  building without TLS.
* ``-DOboe_ROOT`` points at the extracted Oboe ``.aar``. Without it, Oboe is switched off and the
  Java audio device is used.

Oboe audio, Java audio, camera capture, OpenGL ES rendering and the MediaCodec codecs are on by
default.

By default this builds **arm64-v8a**, for API level **23**, with the shared C++ runtime
(``libc++_shared.so``), as ``./configure-android`` does. The next sections show how to change
the first two.

``-DANDROID_STL=c++_static`` uses the static C++ runtime instead. It is only for when
``libpjsua2.so`` is the application's only native library using C++, as the NDK does not support a
static C++ runtime alongside other C++ shared libraries. So it cannot be used with the prebuilt
Oboe AAR, whose ``liboboe.so`` needs ``libc++_shared.so``, and configure stops on that combination.
Use it without Oboe, or with an Oboe built as a static library.

.. tip::

   * Each build directory holds one configuration. Use a new directory for each architecture,
     e.g. ``build-android-x86_64``.
   * Other libraries built for Android are found the same way, from their ``<Package>_ROOT``,
     e.g. ``-DOPUS_ROOT=...`` or ``-DOpenH264_ROOT=...``.
   * More options, such as disabling a codec, are in :doc:`/get-started/cmake/options`.
   * Everyday CMake commands are in :doc:`/get-started/cmake/build_instructions`.

Specifying Android API level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify the Android API level target in ``ANDROID_PLATFORM``. For example:

.. code-block:: shell

   $ cmake -B build-android -DANDROID_PLATFORM=android-28 ...

.. note::

   * Some features need a minimum API level on the device. For example, native Android audio &
     video codecs are built at any API level, but are only used on devices with API level 28 or
     higher.
   * If you build third party libraries from the source (such as OpenSSL), you need to rebuild
     them for the same API level as well.
   * To change the API level of an existing build directory, delete the directory, or add
     ``--fresh`` to the ``cmake`` command. Configure stops with an error otherwise.

Configuring for other architectures (including emulator)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Specify the target arch in ``ANDROID_ABI``, in a build directory of its own. For example, for
targeting the emulator on an x86_64 host:

.. code-block:: shell

   $ cmake -B build-android-x86_64 -DANDROID_ABI=x86_64 ...

``arm64-v8a``, ``armeabi-v7a``, ``x86_64`` and ``x86`` are supported. Repeat the build for each
one the application should carry.

.. note::

   If you build third party libraries from the source (such as OpenSSL), you need to rebuild them
   for the same architecture as well, and give the matching ``OPENSSL_DIR``.

Supporting 16 KB page sizes (Android 15)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As described in `Android official doc <https://developer.android.com/guide/practices/page-sizes>`__,
Android from version 15 onwards supports devices that are configured to use a page size of 16 KB
(16 KB devices). This applies to the 64-bit architectures only.

With NDK r28 or later, nothing is needed: the NDK's toolchain file builds for 16 KB pages by
default. With NDK r27, add:

.. code-block:: shell

   $ cmake -B build-android -DANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON ...


Verifying configuration
---------------------------------
Check that all the intended features are detected by observing the configure output:

* Check that OpenSSL is detected and enabled:

  .. code-block::

     -- [pjlib] SSL backend: openssl

* Check that Oboe is detected and enabled:

  .. code-block::

     -- [pjmedia] Checking if Oboe is available - yes (PJMEDIA_WITH_AUDIODEV_OBOE)

A feature whose library is not found is switched off and configure carries on; look for lines
starting with ``-- [!]``.

With the Oboe AAR, configure also warns that ``liboboe.so`` is not packaged with the bindings'
library. That is expected: it is copied in :ref:`a later step <android_cmake_copy_libs>`. The final values can be listed with:

.. code-block:: shell

   $ cmake -LA -N build-android | grep -E "ANDROID_|PJLIB_WITH_SSL|AUDIODEV_OBOE"


Building PJSIP
---------------------------------
Now we can build PJSIP with:

.. code-block:: shell

   $ cmake --build build-android -j

This builds the libraries, the PJSUA2 Java interface, and copies the latter into the sample
applications' ``pjsua2`` module:

::

    pjsip-apps/src/swig/java/android/pjsua2/src/main
    ├── jniLibs/<ARCH>
    │   ├── libpjsua2.so
    │   └── libc++_shared.so
    ├── java/org/pjsip
    │   ├── pjsua2/*.java
    │   ├── PjCamera*.java
    │   └── PjAudioDevInfo.java (with Oboe)

``-DPJSUA2_ANDROID_DIR=/path/to/your/app/src/main`` copies into your own application instead, and
``-DPJSUA2_ANDROID_DIR=`` copies nothing. Each build updates only the generated classes that
changed. The ``org.pjsip.pjsua2`` package is reserved for them: any other class directly in it is
removed. Keep your application's own sources in another package, or in a subpackage such as
``org.pjsip.pjsua2.app`` as the sample application does; those are left alone. ``libc++_shared.so`` is left out when building with
``-DANDROID_STL=c++_static``.


.. _android_cmake_copy_libs:

Copy third party native libraries
-----------------------------------------------------
As with :doc:`build_gnu`, third party libraries that are shared libraries must be packaged with the
application. Follow :ref:`android_copy_3rd_party_libs`; with the setup in :doc:`requirements`:

* **Oboe**: copy ``liboboe.so``, which the Oboe AAR has as a shared library only.
* **OpenSSL**: nothing to copy, as it was built as static libraries.
* **libc++_shared.so**: nothing to copy, CMake has done it.

To check what ``libpjsua2.so`` needs, run the NDK's ``llvm-readelf``; every library listed that is
not part of Android has to be in ``jniLibs/<ARCH>``:

.. code-block:: shell

   $ $ANDROID_NDK_ROOT/toolchains/llvm/prebuilt/*/bin/llvm-readelf -d \
         build-android/pjsip-apps/src/swig/libpjsua2.so | grep NEEDED


.. _android_cmake_gradle:

Alternative: let Gradle build it
-----------------------------------------------------
Instead of running CMake yourself, the sample applications' ``pjsua2`` module can run it, for all
four architectures in one go:

.. code-block:: shell

   $ cd pjsip-apps/src/swig/java/android
   $ ./gradlew -PpjBuildWithCMake=true :app:assembleDebug

This needs CMake 3.28 or newer and Ninja, either from the SDK Manager or on ``PATH``. It uses
the NDK at ``ANDROID_NDK_ROOT`` when that is set, and otherwise one installed with the SDK
Manager. It builds with the
default options only, so without OpenSSL and Oboe unless they are added to the ``arguments`` in
:source:`pjsip-apps/src/swig/java/android/pjsua2/build.gradle`. In this mode the module ignores
what the steps above copied into ``pjsua2/src/main``. ``:pjsua2:assembleRelease`` builds the
module as an AAR. See :source:`build/android/README.md` for the details.


What's next
---------------------------
The PJSIP library, the JNI interface, and the third party libraries are ready. Now we are ready to
build the sample applications.

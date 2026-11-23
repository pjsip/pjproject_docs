Android Archive (AAR, experimental)
=======================================

.. warning::

   Building the AAR is **experimental**, and :source:`build/android/build-aar.sh` is provided for
   reference purposes only. The script builds one fixed configuration and does not provide all
   the customization options of PJSIP. For a customized build, building PJSIP with
   :doc:`build_gnu` or :doc:`build_cmake` is still recommended. The script, its configuration and
   the contents of the AAR may change in future releases.

The PJSUA2 AAR packages PJSIP for Android applications: one file that an application adds as a
dependency, instead of building PJSIP as part of the application. It contains:

* the ``org.pjsip.pjsua2`` Java classes, and the ``org.pjsip`` camera and Oboe helper classes,
* ``libpjsua2.so`` for ``arm64-v8a``, ``armeabi-v7a``, ``x86_64`` and ``x86``, with OpenSSL, Opus,
  Oboe and the C++ runtime linked in, so there are no other native libraries to copy,
* the licence notices of everything bundled, under ``META-INF``.

.. note::

   Available since release 2.18.


.. contents:: Steps:
   :depth: 2
   :local:


Build the AAR
-----------------------------------
:source:`build/android/build-aar.sh` downloads and builds pinned releases of OpenSSL, Opus and
Oboe, then PJSIP for each architecture, and packages the result. It runs on Linux and macOS, and
needs CMake 3.28 or newer, SWIG, ``curl``, a JDK, and Perl and ``make`` for building OpenSSL, in
addition to the Android NDK and SDK:

.. code-block:: shell

   $ cd /path/to/pjproject
   $ export ANDROID_NDK_ROOT=/home/whoever/Android/android-sdk/ndk/28.0.12916984
   $ export ANDROID_HOME=/home/whoever/Android/android-sdk
   $ ./build/android/build-aar.sh

The AAR is written to ``out-android/dist/pjsua2-<version>.aar``. The other files there (sources and
javadoc jars, POM, checksums) are for publishing the AAR to a Maven repository of your own, and an
application does not need them.

.. tip::

   * ``ABIS="arm64-v8a x86_64"`` builds only the architectures listed, and ``ANDROID_API=26``
     raises the minimum API level from 23.
   * The script uses its own configuration, so it ignores ``config_site.h`` and refuses to run in a
     tree configured with ``./configure-android``; run ``make distclean`` first.
   * See :source:`build/android/README.md` for what is included and excluded, and why.


Use the AAR in an application
-----------------------------------
Copy the AAR into the application module's ``libs`` directory, and add it to the module's
``build.gradle``:

.. code-block:: groovy

   dependencies {
       implementation files('libs/pjsua2-<version>.aar')
   }

The AAR has no dependencies of its own, so this is all that is needed.

.. note::

   The Android Gradle plugin accepts a local AAR file in an application module only. A library
   module that depends on it fails with *"Direct local .aar file dependencies are not supported
   when building an AAR"*. Publish the AAR to a Maven repository of your own (a local one works)
   and take it from there instead.


Use the AAR with the sample applications
-----------------------------------------
The sample applications in :source:`pjsip-apps/src/swig/java/android` normally take PJSUA2 from
the project's ``pjsua2`` module. To use the AAR instead:

#. Copy the AAR into both ``app/libs`` and ``app-kotlin/libs``.
#. In both ``app/build.gradle`` and ``app-kotlin/build.gradle``, replace:

   .. code-block:: groovy

      implementation project(path: ':pjsua2')

   with:

   .. code-block:: groovy

      implementation files('libs/pjsua2-<version>.aar')

#. In ``settings.gradle``, remove ``include ':pjsua2'``. Change both modules first, even to run
   only one of the samples: Gradle configures every module that ``settings.gradle`` includes, and
   fails on one that still refers to ``:pjsua2``.

Then build the applications as described in :doc:`java-sip-client` and :doc:`kotlin-sip-client`.

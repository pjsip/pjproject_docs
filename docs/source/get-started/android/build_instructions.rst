Configure and build PJSIP for Android
=======================================

In this section, we will build PJSIP as a native library for Android, and the
:doc:`PJSUA2 API </api/pjsua2/index>` Java/JNI interface that can be used by Android Java and
Kotlin applications. There are three ways to build it:

.. toctree::
   :maxdepth: 1

   build_gnu
   build_cmake
   aar

* :doc:`build_gnu` uses ``./configure-android`` and ``make``. It is the established way, and
  what the rest of this guide was written with.
* :doc:`build_cmake` uses CMake and the NDK's CMake toolchain file. It is newer; see
  :doc:`/get-started/cmake/index`.
* :doc:`aar` (experimental) builds PJSUA2 into an Android Archive (AAR): one file that an
  application adds as a dependency. Its script is provided for reference purposes only, and
  builds one fixed configuration without all the customization options; for a customized build,
  use one of the first two.

The first two produce the same thing, ``libpjsua2.so`` and the ``org.pjsip.pjsua2`` Java
classes, in the same place, ``pjsip-apps/src/swig/java/android/pjsua2/src/main``, ready for the
sample applications in Android Studio. Pick one of them; the sample applications use whichever
ran last.

Configure and build PJSIP for Android
=======================================

In this section, we will build PJSIP as a native library for Android, and the
:doc:`PJSUA2 API </api/pjsua2/index>` Java/JNI interface that can be used by Android Java and
Kotlin applications. Both ways below produce the same thing: ``libpjsua2.so`` and the
``org.pjsip.pjsua2`` Java classes in the sample applications' ``pjsua2`` module, ready for
Android Studio.

.. toctree::
   :maxdepth: 1

   build_gnu
   build_cmake
   aar

* :doc:`build_gnu` uses ``./configure-android`` and ``make``. It is the established way, and
  what the rest of this guide was written with.
* :doc:`build_cmake` uses CMake and the NDK's CMake toolchain file. It is newer; see
  :doc:`/get-started/cmake/index`.
* :doc:`aar` packages PJSUA2 as an Android Archive (AAR) for distribution: one file an
  application adds as a dependency, with no PJSIP build of its own.

Pick one of the first two. Both put their output in the same place,
``pjsip-apps/src/swig/java/android/pjsua2/src/main``, so the sample applications use whichever
ran last.

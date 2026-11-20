Build Instructions
===================

There are three ways to get PJSIP for iOS:

.. toctree::
   :maxdepth: 1

   build_gnu
   build_cmake
   framework

* :doc:`build_gnu` uses ``./configure-iphone`` and ``make``. It is the established way, and what
  the rest of this guide was written with.
* :doc:`build_cmake` uses CMake. It is newer; see :doc:`/get-started/cmake/index`.
* :doc:`framework` is PJSIP prebuilt as ``PJSIP.xcframework``, for Xcode applications, with no
  PJSIP build of their own.

The first two build the same libraries from source; pick one. Both link them into the sample
applications in :source:`pjsip-apps/src/pjsua/ios`, :source:`pjsip-apps/src/pjsua/ios-swift` and
:source:`pjsip-apps/src/pjsua2/ios-swift-pjsua2`, so the samples use whichever ran last.

Build Instructions
=======================================

There are three ways to get PJSIP for Linux, macOS and other Unix-like systems:

.. toctree::
   :maxdepth: 1

   build_gnu
   build_cmake
   framework

* :doc:`build_gnu` uses ``./configure`` and ``make``. It is the established way, works on every
  target listed there, including cross compilation, and is what the rest of this guide was written
  with.
* :doc:`build_cmake` uses CMake. It is newer, tested on Linux and macOS; see
  :doc:`/get-started/cmake/index`.
* :doc:`framework` (macOS) is PJSIP prebuilt as ``PJSIP.xcframework``, for Xcode applications,
  with no PJSIP build of their own.

The first two build the same libraries and applications from source; pick one.

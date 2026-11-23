Build Instructions
=======================================

There are three ways to build PJSIP for Linux, macOS and other Unix-like systems:

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
* :doc:`framework` (macOS, experimental) builds PJSIP into ``PJSIP.xcframework``: one bundle
  that an Xcode application adds. Its script is provided for reference purposes only, and builds
  one fixed configuration without all the customization options; for a customized build, use one
  of the first two.

The first two build the same libraries and applications; pick one of them.

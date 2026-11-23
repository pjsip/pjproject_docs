Build Instructions
===================

There are two ways to build PJSIP for Windows with Microsoft Visual Studio:

.. toctree::
   :maxdepth: 1

   build_vs
   build_cmake

* :doc:`build_vs` uses the solution files shipped in pjproject, e.g. ``pjproject-vs14.sln``. It
  is the established way, covers the 32-bit, x64 and ARM64 targets, and is what the rest of this
  guide was written with. Visual Studio versions older than 2022 are deprecated since release
  2.18.
* :doc:`build_cmake` uses CMake to generate a Visual Studio solution and build it. It is newer,
  tested on x64 with Visual Studio 2022; see :doc:`/get-started/cmake/index`.

Both build the same libraries and applications from source; pick one.

.. note::

   For building with MinGW-w64, see :any:`/specific-guides/build_int/mingw`.

CMake (experimental)
*****************************************

PJSIP can be built with CMake 3.28 or newer, as an alternative to the GNU
build (``./configure && make``) and the Visual Studio solution. The CMake
build also installs a ``find_package(Pj)`` package for use by other CMake
projects.

CMake support is **experimental**. Its status per platform:

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Platform
     - Status
     - Notes
   * - Linux x86_64
     - CI
     -
   * - macOS (Intel, Apple Silicon)
     - CI
     -
   * - Android (arm64-v8a, armeabi-v7a, x86_64, x86)
     - CI
     - Also builds the pjsua2 JNI bindings and the AAR.
   * - Windows x64, Visual Studio 2022
     - CI
     -
   * - iOS (device, simulator)
     - Verified manually
     - Also used to build the PJSIP XCFramework.
   * - Windows, MinGW-w64 (MSYS2)
     - Verified manually
     -
   * - Other targets (BSD, RTEMS, other cross builds)
     - Not validated
     - Use the GNU build.

The GNU build, and on Windows the Visual Studio solution, remain the
reference builds.

.. toctree::
   :maxdepth: 1
   :caption: Table of Contents

   build_instructions
   options
   using

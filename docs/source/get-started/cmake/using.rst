Using PJSIP in CMake Projects
===============================

.. contents:: Table of Contents
    :depth: 2


After ``cmake --install`` (see :doc:`build_instructions`), another CMake
project uses PJSIP with ``find_package(Pj)``.


Minimal Example
---------------

``CMakeLists.txt``:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.16)
   project(myapp C CXX)

   find_package(Pj REQUIRED)

   add_executable(myapp myapp.c)
   target_link_libraries(myapp PRIVATE Pj::pjsua-lib)

``myapp.c``:

.. code-block:: c

   #include <pjsua-lib/pjsua.h>

   int main(void)
   {
       pjsua_create();
       PJ_LOG(3, ("myapp.c", "Hello PJSIP! Bye PJSIP."));
       pjsua_destroy();
       return 0;
   }

Build it, pointing CMake at the PJSIP install prefix:

.. code-block:: shell

   $ cmake -S . -B cmake-build -DCMAKE_PREFIX_PATH=/opt/pjsip -DCMAKE_BUILD_TYPE=Release
   $ cmake --build cmake-build

Enable C++ in ``project()`` even for a C application: the PJSIP libraries
contain C++ code, and a static build needs the C++ runtime at link time.

``find_package(Pj)`` also finds whatever PJSIP was built with (OpenSSL,
SDL2, ALSA, and so on), so the application needs no ``find_package()`` of
its own for those.

Instead of ``CMAKE_PREFIX_PATH``, the package directory can be given
directly, e.g. ``-DPj_DIR=/opt/pjsip/lib/cmake/Pj``.

A version can be requested, e.g. ``find_package(Pj 2.17 REQUIRED)``. Any
installed 2.x release from that version on satisfies it
(``SameMajorVersion``).

.. note::

   With MSVC, the Debug and Release C runtimes cannot be mixed. Build the
   application in the configuration PJSIP was installed with. To have
   both, install them to separate prefixes, as the two configurations
   use the same library names.


Targets
-------

All libraries are exported in the ``Pj::`` namespace. An application
normally links ``Pj::pjsua-lib`` (C) or ``Pj::pjsua2`` (C++); the
libraries below them come along.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Target
     - Library
   * - ``Pj::pjsua2``
     - PJSUA2, the C++ API.
   * - ``Pj::pjsua-lib``
     - PJSUA, the high-level C API.
   * - ``Pj::pjsip-ua``
     - SIP user agent: dialogs, INVITE sessions, call transfer.
   * - ``Pj::pjsip-simple``
     - SIP presence and messaging (SIMPLE).
   * - ``Pj::pjsip``
     - SIP core: parser, transport, transactions.
   * - ``Pj::pjmedia``, ``Pj::pjmedia-codec``, ``Pj::pjmedia-audiodev``, ``Pj::pjmedia-videodev``
     - Media framework, codecs, audio devices and video devices.
   * - ``Pj::pjnath``
     - NAT traversal: STUN, TURN, ICE.
   * - ``Pj::pjlib-util``
     - Utilities: DNS resolver, XML, JSON, and others.
   * - ``Pj::pjlib``
     - Base library: OS abstraction, data structures, pool allocator.

A narrower set can be linked directly, e.g. a SIP-only tool:

.. code-block:: cmake

   target_link_libraries(sip_tool PRIVATE Pj::pjsip)


Building PJSIP as Part of a Project
-----------------------------------

PJSIP can also be built inside another project, without installing it:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.28)
   project(super C CXX)

   set(PJ_SKIP_EXPERIMENTAL_NOTICE ON)
   set(PJMEDIA_WITH_VIDEO OFF)            # any PJSIP option
   add_subdirectory(third_party/pjproject EXCLUDE_FROM_ALL)

   add_executable(myapp myapp.c)
   target_link_libraries(myapp PRIVATE pjsua-lib)

The targets then have no ``Pj::`` prefix: link ``pjsua-lib``, ``pjsua2``,
``pjsip``, and so on.


Without CMake
-------------

The installation also has a pkg-config file. For a static build, ask for
the libraries PJSIP itself links too, with ``--static``:

.. code-block:: shell

   $ export PKG_CONFIG_PATH=/opt/pjsip/lib/pkgconfig
   $ cc myapp.c -o myapp $(pkg-config --static --cflags --libs libpjproject)

The file locates the installation relative to itself, so it stays valid
when the installation is moved. Use it with GCC or Clang; it requires
:pr:`5301`.

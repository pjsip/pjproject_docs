Using PJSIP in CMake Projects
===============================

.. contents:: Table of Contents
    :depth: 2


After ``cmake --install`` has placed PJSIP under a prefix (see
:any:`build_instructions`), a downstream CMake project can consume it
with a standard ``find_package`` call. This page covers the installed
package layout, the exported targets, and a minimal working example.


Minimal Example
---------------

Assuming PJSIP was installed under ``/usr/local`` (or the prefix is on
``CMAKE_PREFIX_PATH``):

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.28)
   project(myapp C)

   find_package(Pj REQUIRED)

   add_executable(myapp myapp.c)
   target_link_libraries(myapp PRIVATE Pj::pjsua-lib)

``myapp.c``:

.. code-block:: c

   #include <pjsua-lib/pjsua.h>
   #include <pj/log.h>

   int main(void)
   {
       pjsua_create();
       PJ_LOG(3, ("myapp.c", "Hello PJSIP! Bye PJSIP."));
       pjsua_destroy();
       return 0;
   }

Configure and build:

.. code-block:: shell

   $ cmake -S . -B build -DCMAKE_PREFIX_PATH=/usr/local
   $ cmake --build build -j

``find_package(Pj)`` transitively pulls in everything PJSIP was linked
against at install time (OpenSSL, SDL2, FFMPEG, ALSA, and so on). No
additional ``find_package`` calls are required in the consumer project
unless the application itself uses those libraries directly.


Exported Targets
----------------

All PJSIP libraries are exported under the ``Pj::`` namespace. The
targets mirror the library layout described in :any:`/overview/intro`:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Target
     - What it is
   * - ``Pj::pjlib``
     - Base framework: OS abstraction, data structures, pool allocator.
   * - ``Pj::pjlib-util``
     - Utilities: DNS, STUN, XML, JSON, WebSocket.
   * - ``Pj::pjnath``
     - NAT traversal: STUN, TURN, ICE.
   * - ``Pj::pjmedia``
     - Core media framework: transports, streams, ports, sessions.
   * - ``Pj::pjmedia-codec``
     - Codec implementations and the codec manager.
   * - ``Pj::pjmedia-audiodev``
     - Audio device abstraction (ALSA, Core Audio, WASAPI, Oboe, …).
   * - ``Pj::pjmedia-videodev``
     - Video device abstraction (V4L2, AVFoundation, DirectShow, …).
   * - ``Pj::pjsip``
     - SIP core: transactions, transport, parsing.
   * - ``Pj::pjsip-simple``
     - SIP event/presence (SIMPLE) package.
   * - ``Pj::pjsip-ua``
     - SIP UA layer: dialogs, calls, INVITE/REFER sessions.
   * - ``Pj::pjsua-lib``
     - High-level PJSUA C API (the library most applications link).
   * - ``Pj::pjsua2``
     - PJSUA2 C++ API.

There is also one infrastructure target you normally do not link
directly:

* ``Pj::pjlib-ssl`` – an ``INTERFACE`` target that carries the selected
  SSL backend's compile and link flags. It is pulled in automatically
  by any target that needs SSL.

The ``pjsua`` command-line application is installed as an **executable**
(``<prefix>/bin/pjsua``); it is not a library and should not be linked
into downstream code.


Selecting Components
--------------------

Most applications only need ``Pj::pjsua-lib`` or ``Pj::pjsua2``; the
other targets are brought in transitively. When you want a narrower
link set – for example, a tool that only does SIP parsing without a
full UA – link against the specific targets:

.. code-block:: cmake

   target_link_libraries(sip_tool PRIVATE Pj::pjsip Pj::pjlib-util Pj::pjlib)

CMake resolves the transitive dependencies between PJSIP libraries
automatically.


Pointing CMake at the Install Prefix
------------------------------------

If PJSIP is installed outside the default search path, tell the
consumer project where to look via one of:

.. code-block:: shell

   $ cmake -S . -B build -DCMAKE_PREFIX_PATH=/opt/pjsip

.. code-block:: shell

   $ export CMAKE_PREFIX_PATH=/opt/pjsip
   $ cmake -S . -B build

.. code-block:: shell

   $ cmake -S . -B build -DPj_DIR=/opt/pjsip/lib/cmake/Pj

``Pj_DIR`` is the most explicit form and bypasses the rest of CMake's
search logic.


Version Requirements
--------------------

``find_package(Pj)`` supports the usual CMake version request:

.. code-block:: cmake

   find_package(Pj 2.17 REQUIRED)

The package is configured with ``COMPATIBILITY SameMajorVersion``, so
a request for ``2.16`` is satisfied by any installed ``2.x`` release
(``x ≥ 16``) but not by a future ``3.x``.


Embedding PJSIP via ``add_subdirectory``
----------------------------------------

PJSIP can also be embedded into a super-project without a separate
install step:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.28)
   project(super C CXX)

   set(PJ_SKIP_EXPERIMENTAL_NOTICE ON)
   add_subdirectory(third_party/pjproject EXCLUDE_FROM_ALL)

   add_executable(myapp myapp.c)
   target_link_libraries(myapp PRIVATE pjsua-lib)

In this mode the targets exist without the ``Pj::`` namespace prefix
(CMake's ALIAS mechanism is set up by the export step, which is only
run on ``install``). Use the bare target names — ``pjsua-lib``,
``pjsua2``, ``pjsip``, and so on — when linking.

The same ``PJ_DEP_*`` and ``PJMEDIA_WITH_*`` options can be set in
the super-project's cache before ``add_subdirectory()`` to control
the embedded build.


Interaction with System Dependencies
------------------------------------

When PJSIP was built with ``PJ_DEP_<NAME>=system`` (for example,
``-DPJ_DEP_SRTP=system``), the installed ``PjConfig.cmake`` records
this choice and calls ``find_dependency()`` on the same system
packages when you run ``find_package(Pj)``. You do not need to call
``find_package(libsrtp)`` yourself; it is handled by the config
module.

For SSL, the backend chosen at build time is also recorded, so
consumers that call ``find_package(Pj)`` automatically get the right
``OpenSSL`` / ``GnuTLS`` / ``MbedTLS`` dependency pulled in.

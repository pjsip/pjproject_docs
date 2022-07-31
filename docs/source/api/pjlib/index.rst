PJLIB
===================

PJLIB is an Open Source, small footprint framework library written in C for making scalable applications. 
It can be used in wide range of applications, from embedded systems, mobile applications, to high performance systems.


Key Features
-------------

- Extreme Portability

  From 16-bit, 32-bit, to 64-bit, big or little endian, single or multi-processors, wide range of
  operating systems, Unicode support. With or without floating point support. Multi-threading or not.
  With/without ANSI LIBC. Currently known to run on these platforms:
  
  - Mobile platforms:
  
    - Android
    - iOS (iPhone, iPad, iPod Touch)
    - UWP and Windows Phone 8
    - BlackBerry 10
    - Symbian S60 3rd Edition
    - Windows Mobile/CE
    
  - Desktop platforms:
  
    - MacOS X (Intel and powerpc)
    - Win32/x86_64 (Win95/98/ME, NT/2000/XP/2003)
    - Linux/x86_64
    
  - Embedded platforms:
  
    - Embedded Linux
    - WinCE
    - RTEMS (x86 and powerpc)
    
  - Others:
  
    - Solaris/ultra
    - Linux/alpha
  

- Small in Size

  - Size around 100 KB.

- Big in Performance

  - Everything is designed for highest performance.
  
- No Dynamic Memory Allocations

  - alloc() is a O(1) operation.
  - no mutex is used inside alloc().
  - no free(). All chunks will be deleted when the pool is destroyed.

- Rich Features

  - Operating system abstraction
  - Low and high level network I/O
  - Timer management
  - Rich data structures
  - Exception construct
  - Logging facility
  - Random and GUID generation
  
  
API Reference
-------------------

Basic Types and Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`Configs & Macros </api/generated/pjlib/group/group__pj__config>`
- :doc:`Basic Types and Init/Shutdown Functions </api/generated/pjlib/group/group__PJ__BASIC>`
- :doc:`DLL Build Target </api/generated/pjlib/group/group__pj__dll__target>`


Infrastructure
^^^^^^^^^^^^^^^^^^^^^

- Error Number Management

  - :doc:`Errno Framework </api/generated/pjlib/group/group__pj__errno>`
  - :doc:`Standard Error Constants </api/generated/pjlib/group/group__pj__errnum>`

- :doc:`Ctype </api/generated/pjlib/group/group__pj__ctype>`
- :doc:`Logging </api/generated/pjlib/group/group__PJ__LOG>`
- :doc:`Assertion </api/generated/pjlib/group/group__pj__assert>`
- :doc:`Math </api/generated/pjlib/group/group__pj__math>`
- :doc:`Exception Handling </api/generated/pjlib/group/group__PJ__EXCEPT>`


Data structure
^^^^^^^^^^^^^^^

- :doc:`Array </api/generated/pjlib/group/group__PJ__ARRAY>` 
- :doc:`Hash Table </api/generated/pjlib/group/group__PJ__HASH>`
- :doc:`Linked List </api/generated/pjlib/group/group__PJ__LIST>`
- :doc:`RB Tree </api/generated/pjlib/group/group__PJ__RBTREE>`


Network
^^^^^^^^^^

- Address Resolution

  - :doc:`IP Helper </api/generated/pjlib/group/group__pj__ip__helper>`
  - :doc:`Address Resolution </api/generated/pjlib/group/group__pj__addr__resolve>`

- Network I/O

  - :doc:`Socket </api/generated/pjlib/group/group__PJ__SOCK>`
  - :doc:`select() Abstraction </api/generated/pjlib/group/group__PJ__SOCK__SELECT>`
  - :doc:`Active Socket </api/generated/pjlib/group/group__PJ__ACTIVESOCK>`
  - :doc:`IOQueue (Event Proactor pattern) </api/generated/pjlib/group/group__PJ__IOQUEUE>`

- :ref:`qos`
- :doc:`SSL Socket </api/generated/pjlib/group/group__PJ__SSL__SOCK>`

File
^^^^^^^^^^
- :doc:`File Access </api/generated/pjlib/group/group__PJ__FILE__ACCESS>`
- :doc:`File I/O </api/generated/pjlib/group/group__PJ__FILE__IO>`


Memory Management
^^^^^^^^^^^^^^^^^^^^^
- :doc:`Introduction to Memory Pool </api/generated/pjlib/group/group__PJ__POOL__GROUP>`
- :doc:`Pool </api/generated/pjlib/group/group__PJ__POOL>`
- :doc:`Pool on Fixed Buffer </api/generated/pjlib/group/group__PJ__POOL__BUFFER>`
- :doc:`Caching Pool </api/generated/pjlib/group/group__PJ__CACHING__POOL>`

  - :doc:`Pool Factory Concept </api/generated/pjlib/group/group__PJ__POOL__FACTORY>`



String & Unicode
^^^^^^^^^^^^^^^^^^^^
String in PJLIB is non-zero terminated, and represented with ``pj_str_t``. A full
set of API is provided to manipulate such strings.

- :doc:`String Manipulations </api/generated/pjlib/group/group__PJ__PSTR>`
- :doc:`Unicode Helper </api/generated/pjlib/group/group__PJ__UNICODE>`



Multithreading and Concurrency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`Thread </api/generated/pjlib/group/group__PJ__THREAD>`
- Concurrency

  - :doc:`Atomic Operation </api/generated/pjlib/group/group__PJ__ATOMIC>`
  - :doc:`Critical Section </api/generated/pjlib/group/group__PJ__CRIT__SEC>`
  - :doc:`Mutex </api/generated/pjlib/group/group__PJ__MUTEX>`
  - :doc:`RW Mutex </api/generated/pjlib/group/group__PJ__RW__MUTEX>`
  - :doc:`Semaphore </api/generated/pjlib/group/group__PJ__SEM>`
  - :doc:`Lock </api/generated/pjlib/group/group__PJ__LOCK>`
  - :doc:`Group Lock </api/generated/pjlib/group/group__PJ__GRP__LOCK>`
  - :doc:`Event </api/generated/pjlib/group/group__PJ__EVENT>`
  
- :doc:`Thread Local Storage </api/generated/pjlib/group/group__PJ__TLS>`

OS Abstraction
^^^^^^^^^^^^^^^^^
- :doc:`OS Abstraction </api/generated/pjlib/group/group__PJ__OS>`
 
   - :doc:`Symbian OS Specific </api/generated/pjlib/group/group__PJ__SYMBIAN__OS>`

- :doc:`System Information </api/generated/pjlib/group/group__PJ__SYS__INFO>`


Time and Timer
^^^^^^^^^^^^^^^^^
- :doc:`Time </api/generated/pjlib/group/group__PJ__TIME>`
- :doc:`High Resolution Timestamp </api/generated/pjlib/group/group__PJ__TIMESTAMP>`
- :doc:`Timer API </api/generated/pjlib/group/group__PJ__TIMER>`


Random and GUID 
^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Random </api/generated/pjlib/group/group__PJ__RAND>`
- :doc:`GUID </api/generated/pjlib/group/group__PJ__GUID>`


Application Microframework
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`main() </api/generated/pjlib/group/group__PJ__APP__OS>`


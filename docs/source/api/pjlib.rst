PJLIB
===================

PJLIB is an Open Source, small footprint framework library written in C for making scalable applications. 
It can be used in wide range of applications, from embedded systems, mobile applications, to high performance systems.


Key Features
-------------

- Extreme Portability

  From 16-bit, 32-bit, to 64-bit, big or little endian, single or multi-processors, wide range of
  operating systems. With or without floating point support. Multi-threading or not. With/without ANSI LIBC. 
  Currently known to run on these platforms:
  
  - Mobile platforms:
  
    - Android
    - iOS (iPhone, iPad, iPod Touch)
    - UWP and Windows Phone 8
    - BlackBerry 10
    - Symbian S60 3rd Edition
    - Windows Mobile
    
  - Desktop platforms:
  
    - MacOS X (Intel and powerpc)
    - Win32/x86 (Win95/98/ME, NT/2000/XP/2003, mingw)
    - Linux/x86, (user mode and as kernel module(!))
    
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

- :doc:`Configs & Macros <generated/pjlib/group/group__pj__config>`
- :doc:`Basic Types and Init/Shutdown Functions <generated/pjlib/group/group__PJ__BASIC>`
- :doc:`DLL Build Target <generated/pjlib/group/group__pj__dll__target>`


Infrastructure
^^^^^^^^^^^^^^^^^^^^^

- Error Number Management

  - :doc:`Errno Framework <generated/pjlib/group/group__pj__errno>`
  - :doc:`Standard Error Constants <generated/pjlib/group/group__pj__errnum>`

- :doc:`Ctype <generated/pjlib/group/group__pj__ctype>`
- :doc:`Logging <generated/pjlib/group/group__PJ__LOG>`
- :doc:`Assertion <generated/pjlib/group/group__pj__assert>`
- :doc:`Math <generated/pjlib/group/group__pj__math>`
- :doc:`Exception Handling <generated/pjlib/group/group__PJ__EXCEPT>`


Data structure
^^^^^^^^^^^^^^^

- :doc:`Array <generated/pjlib/group/group__PJ__ARRAY>` 
- :doc:`Hash Table <generated/pjlib/group/group__PJ__HASH>`
- :doc:`Linked List <generated/pjlib/group/group__PJ__LIST>`
- :doc:`RB Tree <generated/pjlib/group/group__PJ__RBTREE>`


Network
^^^^^^^^^^

- Address Resolution

  - :doc:`IP Helper <generated/pjlib/group/group__pj__ip__helper>`
  - :doc:`Address Resolution <generated/pjlib/group/group__pj__addr__resolve>`

- Network I/O

  - :doc:`Socket <generated/pjlib/group/group__PJ__SOCK>`
  - :doc:`select() Abstraction <generated/pjlib/group/group__PJ__SOCK__SELECT>`
  - :doc:`Active Socket <generated/pjlib/group/group__PJ__ACTIVESOCK>`
  - :doc:`IOQueue <generated/pjlib/group/group__PJ__IOQUEUE>`
  
- :doc:`SSL Socket <generated/pjlib/group/group__PJ__SSL__SOCK>`

File
^^^^^^^^^^
- :doc:`File Access <generated/pjlib/group/group__PJ__FILE__ACCESS>`
- :doc:`File I/O <generated/pjlib/group/group__PJ__FILE__IO>`


Memory Management
^^^^^^^^^^^^^^^^^^^^^
- :doc:`Introduction to Memory Pool <generated/pjlib/group/group__PJ__POOL__GROUP>`
- :doc:`Pool <generated/pjlib/group/group__PJ__POOL>`
- :doc:`Pool on Fixed Buffer <generated/pjlib/group/group__PJ__POOL__BUFFER>`
- :doc:`Caching Pool <generated/pjlib/group/group__PJ__CACHING__POOL>`

  - :doc:`Pool Factory Concept <generated/pjlib/group/group__PJ__POOL__FACTORY>`



String & Unicode
^^^^^^^^^^^^^^^^^^^^
String in PJLIB is non-zero terminated, and represented with ``pj_str_t``. A full
set of API is provided to manipulate such strings.

- :doc:`String Manipulations <generated/pjlib/group/group__PJ__PSTR>`
- :doc:`Unicode Helper <generated/pjlib/group/group__PJ__UNICODE>`



Multithreading and Concurrency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`Thread <generated/pjlib/group/group__PJ__THREAD>`
- Concurrency

  - :doc:`Atomic Operation <generated/pjlib/group/group__PJ__ATOMIC>`
  - :doc:`Critical Section <generated/pjlib/group/group__PJ__CRIT__SEC>`
  - :doc:`Mutex <generated/pjlib/group/group__PJ__MUTEX>`
  - :doc:`RW Mutex <generated/pjlib/group/group__PJ__RW__MUTEX>`
  - :doc:`Semaphore <generated/pjlib/group/group__PJ__SEM>`
  - :doc:`Lock <generated/pjlib/group/group__PJ__LOCK>`
  - :doc:`Group Lock <generated/pjlib/group/group__PJ__GRP__LOCK>`
  - :doc:`Event <generated/pjlib/group/group__PJ__EVENT>`
  
- :doc:`Thread Local Storage <generated/pjlib/group/group__PJ__TLS>`

OS Abstraction
^^^^^^^^^^^^^^^^^
- :doc:`OS Abstraction <generated/pjlib/group/group__PJ__OS>`
 
   - :doc:`Symbian OS Specific <generated/pjlib/group/group__PJ__SYMBIAN__OS>`

- :doc:`System Information <generated/pjlib/group/group__PJ__SYS__INFO>`


Time and Timer
^^^^^^^^^^^^^^^^^
- :doc:`Time <generated/pjlib/group/group__PJ__TIME>`
- :doc:`High Resolution Timestamp <generated/pjlib/group/group__PJ__TIMESTAMP>`
- :doc:`Timer API <generated/pjlib/group/group__PJ__TIMER>`


Random and GUID 
^^^^^^^^^^^^^^^^^^^^^^
- :doc:`Random <generated/pjlib/group/group__PJ__RAND>`
- :doc:`GUID <generated/pjlib/group/group__PJ__GUID>`


Application Microframework
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- :doc:`main() <generated/pjlib/group/group__PJ__APP__OS>`



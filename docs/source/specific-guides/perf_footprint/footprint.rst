Footprint Optimization
=========================

.. note::

   Although this article is very old (was written in 2007) and 
   the numbers have changed, most of the principles for reducing footprint 
   still apply.

.. contents:: Table of Contents
   :depth: 3

Overview
--------------
With the default settings, PJSIP is not heavily optimized for size (nor
speed), since the main objective is to have sufficient information for
troubleshooting. Taking Windows as reference platform, the executable
size of Release build with Visual C++ 6 is as follows:

::

     pjsua_vc6.exe: file size=749,672 bytes

         241664 .data
         102400 .rdata
          24576 .reloc
         536576 .text

     (all numbers in decimal, bytes)

.. note::
        
        With default settings, *pjsua* includes as many features as available
        in the source distribution, for example, all the codecs,
        statically linked with the application. Hence the executable size is 
        a bit large for *pjsua*.

The heap usage with 2 connected calls using Speex wideband codec and AEC
enabled (press **dd** in pjsua menu, and scroll up to the portion where
it dumps the memory pool statistic):

::

   >>> dd
   ..
     Total    908508 of   1046304 (86 %) used!
   ..


Reducing executable size
------------------------------
To reduce the executable size, the following settings can be applied by declaring
the settings in :any:`config_site.h`:

#. **Disable Speex AEC**. If AEC is provided by the hardware, Speec AEC can be disabled
   by setting :c:macro:`PJMEDIA_HAS_SPEEX_AEC` to 0, to reduce executable size
   by **32 KB**. 
#. **Disable resampling**. If all media components are running at the same 
   clock rate, disable resampling by setting
   :c:macro:`PJMEDIA_HAS_LIBRESAMPLE` to 0, to reduce executable size by **45 KB**.
#. **Disable unused codecs**. For example, 
   disable speex by declaring  :c:macro:`PJMEDIA_HAS_SPEEX_CODEC` to 0, 
   disable iLBC by declaring :c:macro:`PJMEDIA_HAS_ILBC_CODEC` to 0, 
   disable GSM codec by declaring:c:macro:`PJMEDIA_HAS_GSM_CODEC` to 0, and
   disable L16 codecs by declaring :c:macro:`PJMEDIA_HAS_L16_CODEC` to 0.
   This will reduce executable size by approximately **114 KB**. 

   .. note::

        Latest PJSIP version contains more codecs. See
        :source:`pjmedia/include/pjmedia-codec/config.h` to see
        what built-in codecs are available and how to disable them, 
        using code similar to above.

#. **Disable alaw/ulaw table**. By default, a
   table based alaw/ulaw implementation is used. You can disable this by
   setting :c:macro:`PJMEDIA_HAS_ALAW_ULAW_TABLE` to 0, which makes PJMEDIA
   calculates the alaw/ulaw value rather than using the table. This will
   reduce executable size by approximately **28 KB**, at the expense of more
   CPU processing.
#. **Disable error string**. All libraries keep the description of the error codes in some
   static variables. You can omit this error description by setting
   :c:macro:`PJ_HAS_ERROR_STRING` to 0. When the error description is omitted,
   :cpp:any:`pj_strerror()` will just print the error code rather than the error
   message. You can then look for the error description in libraries
   source codes. Omitting the error
   description will reduce executable size by approximately **20 KB**. 
#. **Disable run-time checks**. All the libraries are equipped with
   run-time checks to prevent bad parameters from crashing the software.
   Although this is not recommended, it can be disabled by setting :c:macro:`PJ_ENABLE_EXTRA_CHECK` to
   0. This will reduce executable size by approximately **20 KB**. 
#. **Disable stack checks**. PJLIB is equipped with stack overflow
   detection. This can be disabled by setting
   :c:macro:`PJ_OS_HAS_CHECK_STACK` to 0, to reduce executable size by
   approximately **4 KB**. 
#. **Disable CRC32 table**, by setting
   :c:macro:`PJ_CRC32_HAS_TABLES` to 0, to reduce executable size by about **1 KB**,
   only if you use ICE. Note the non-table based is more than an order of magnitude slower.
#. **Use your own sound device abstraction**,
   rather than PortAudio. If you are porting PJSIP to an embedded platform,
   you will need to create your own sound device abstraction. So supposing
   we don't use PortAudio and use the NULL sound device implementation
   (by declaring :c:macro:`PJMEDIA_SOUND_IMPLEMENTATION` to :c:macro:`PJMEDIA_SOUND_NULL_SOUND`), we will
   reduce executable size by approximately **49 KB**.

   .. note::

        This has been deprecated since the use of :any:`PJMEDIA-AudioDev API </api/pjmedia/pjmedia-audiodev>`.
        See :source:`pjmedia/include/pjmedia-audiodev/config.h`
        for supported audio device backends.

#. **Reduce logging verbosity**. 
   The default logging level is 5, to provide enough information for debugging. 
   If price is really really tight, the logging verbosity level can be decreased,
   for example to level 3 so that only vital
   information is displayed, by setting :c:macro:`PJ_LOG_MAX_LEVEL` macro to 3. 
   This will reduce executable size by
   approximately **28 KB**. 
#. **Turn off logging**. 
   Alternatively you can disable logging altogether, by setting :c:macro:`PJ_LOG_MAX_LEVEL` to 0. 
   This is not recommended, and will reduce executable size by another **28 KB**. 

With all above optimizations set, we now have pjsua size (still with
ICE/PJNATH and many media goodies like conference, WAV, etc.
**statically linked** in the executable):

::

     pjsua_vc6.exe: file size= 381,032 bytes

      184320 .data
        8192 .rdata
       16384 .reloc
      319488 .text

Using the same settings, if we take the executable size of
**simpleua.exe** (this is a sample program to do simple call with audio,
without conference bridge nor ICE/STUN):

::

     simpleua.exe: file size= 155,648 bytes

       28672 .data
        4096 .rdata
      139264 .text

At this point, the heap memory usage of pjsua with 2 calls has been
reduced by about 100 KB:

::

   >>> dd
   ..
    Total    793624 of    909024 (87 %) used!
   ..


Reducing heap memory usage
-----------------------------
Now, assuming that the product will only need to support, say, 8 calls,
we can apply these settings to **reduce heap memory usage**: 

#. **Transaction/dialog/call count**. Set the maximum number of concurrent
   transactions/dialogs/calls with

   .. code-block:: c

      #   define PJSIP_MAX_TSX_COUNT      31
      #   define PJSIP_MAX_DIALOG_COUNT   31
      #   define PJSUA_MAX_CALLS          31

   For reference: see :c:macro:`PJSIP_MAX_TSX_COUNT`, 
   :c:macro:`PJSIP_MAX_DIALOG_COUNT`, :c:macro:`PJSUA_MAX_CALLS`.

#. **Optimize pool sizes**. These settings not only will reduce heap
   memory usage, but will also prevent the libraries from allocating too
   many large memory blocks. With the default settings, most memory
   pools are configured to allocate memory in 4KB blocks, and some
   system like Symbian will have difficulties in providing these blocks
   to PJSIP. Use the following setting to reduce the memory block size
   used by memory pools, at the expense of more calls to system's memory
   allocators (``new`` or ``malloc``) to allocate memory:

   ::

        #   define PJSIP_POOL_LEN_ENDPT     1000
        #   define PJSIP_POOL_INC_ENDPT     1000
        #   define PJSIP_POOL_RDATA_LEN     2000
        #   define PJSIP_POOL_RDATA_INC     2000
        #   define PJSIP_POOL_LEN_TDATA     2000
        #   define PJSIP_POOL_INC_TDATA     512
        #   define PJSIP_POOL_LEN_UA        2000
        #   define PJSIP_POOL_INC_UA        1000
        #   define PJSIP_POOL_TSX_LAYER_LEN 256
        #   define PJSIP_POOL_TSX_LAYER_INC 256
        #   define PJSIP_POOL_TSX_LEN       512
        #   define PJSIP_POOL_TSX_INC       128
        #   define PJMEDIA_SESSION_SIZE     1000
        #   define PJMEDIA_SESSION_INC      1000

   With these settings applied, heap memory usage will be reduced very
   significantly. Looking at heap memory usage of pjsua with two G.711
   calls:

   ::

        pjsua_vc6 --clock-rate 8000 --ec-tail 0 --max-calls 2 --no-tcp

        >>> dd
        ..
        Total    120532 of    150344 (80 %) used!
        ..


At this stage, the heap usage is about 150 KB for two calls, which should be affordable.

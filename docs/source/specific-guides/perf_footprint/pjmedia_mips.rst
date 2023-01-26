Media Performance (MIPS test)
===================================================

.. note::

   Although this article is very old (last updated 2008), the listed PJMEDIA algorithms
   haven't changed very much, hence the result may still be useful.


.. contents:: Table of Contents
   :depth: 3

This page attempts to show the typical performance characteristic of
various PJMEDIA components, which could be useful to evaluate PJMEDIA
performance. Please do not interpret these numbers as an official or
definite performance number, as there are many compilation flags in
PJMEDIA as well as compiler switches that can be set to increase (or
decrease) the performance.


Test Method
-----------

Each test should measure the overall performance for both directions. So
for example for resampling, the test shows the total upsample and
downsample time in a single test, and for codec it will show the total
encoding and decoding time.

The test program depends on correct settings of CPU_MHZ and MIPS value
of the processor being set correctly during compilation time. We used
the MIPS information in the following links to assume the MIPS value of
the processor: 

- http://en.wikipedia.org/wiki/Million_instructions_per_second 
- http://en.wikipedia.org/wiki/ARM_architecture

To measure the MIPS score of a component, the program calculates the
time to process 1 second worth of audio samples using that component,
then calculates the MIPS score based on the configured MIPS value of the
processor. Because of this, the calculated MIPS shouldn't be interpreted
as a *real* MIPS value since it's purely based on time measurement, and
our assumed MIPS value for the processor may be wrong.

The test uses strictly one thread only.

All the results below are done with the default settings that come with
PJSIP distribution. The test source code are available in
:source:`pjmedia/src/test/mips_test.c`.

Interpreting the Results
------------------------

Columns
~~~~~~~

There are four columns in the result table:

**Clock Rate:**

This shows the sampling rate of the component being
tested, in KHz. We test both 8KHz and 16KHz. Most components can work in
both 8KHz and 16KHz hence there will be two test result rows for the
same component, each with different clock rate. Some components (mostly
related codec) can only work in one of the clock rate (e.g. GSM is only
shown in 8KHz, while G.722 is only shown in 16KHz) hence there will only
be one test result row for these components.

**Time (usec):** 

This shows the time elapsed to process 1 second
worth of audio samples, in microseconds.

**CPU (%):** 

This shows how much CPU usage (in percent) this
component will consume when running it in real-time. The value is
derived from the time measurement above. For example, if the time
elapsed is 1 secondthen this component will take 100% of CPU time when
run in real-time. Or if the time elapsed is 0.5 second then this
component will take 50% of the CPU time when run in real-time.

The CPU percentage maybe larger than 100% if the time taken to process 1
second worth of audio samples is more than 1 second. It may happen when
we perform the test on slower processor.

**MIPS:** 

The MIPS (Million Instructions per Second) score roughly
means how many instructions will be executed by this component per
second when we run this component in real-time. The value is derived
from the time measurement above, and calculated based on the assumed
MIPS value of the processor. Once again, the score may be incorrect for
many reasons so it shouldn't be interpreted as an official/definite
score, and especially one MUST NOT use the MIPS score to compare
performance of different processor families/architectures.

Rows
~~~~

The rows show the measurement result of a particular components. The
components tested are described below.

**get from memplayer:** 

The memory/buffer based player port supplies
the audio samples for almost all of the tests, so its time adds as
overhead for all tests.

**conference bridge with N call(s):** 

This measures the performance
of the conference bridge with N calls. Note that we don't use actual
call for the test since we only want to measure the conference bridge
performance and not codec performance (this will be measured in separate
tests). So for this test we use memplayer for each "call" to supply
audio to the bridge. During the test all the calls (ports) will be
connected to port zero and port zero will be connected to all calls. No
connection among calls are created.

**upsample+downsample:** 

This measures the performance of the
resampling algorithm used. The test gets the audio from the memplayer,
upsample it twice the clock rate, then downsample it half the clock rate
again so that the clock rate now is the same as originally. This test
measures both linear and non-linear resampling using small filter and
large filter. Some resampling backend algorithms may not support
selecting between linear/non-linear and small/large filter, in that case
the results will be equal for all settings.

**WSOLA PLC - N% loss:** 

This measures the performance of Waveform
Similarity based Overlap and Add (WSOLA) algorithm when it is used to
generate/emulate lost packet (a.k.a Packet Lost Concealment/PLC). Timing
for various loss percentages are shown.

The WSOLA algorithm is used by both the delay buffer and PLC algorithm
in pjmedia. The delay buffer itself is used by the splitcomb, sound
port, and the conference bridge to adapt to audio burst and clock
drifts.

**WSOLA discard N% excess:** 

This measures the performance of
Waveform Similarity based Overlap and Add (WSOLA) algorithm when it is
used to discard excess audio samples (e.g. caused by clock drifts).
Timing for various excess percentages are shown.

**echo canceller Nms tail len:** 

This measures the performance of the
acoustic echo canceller (AEC) for various echo tail settings. The audio
source is taken from memplayer, and there is no acoustic delay in the
AEC input.

**tone generator with single/dual freq:** 

This measures the
performance of the tone generator to continuously generate single or
dual frequency tone for 1 second.

**codec encode/decode:** 

This measures the time to encode and then
decode 1 second worth of audio samples using the specified codec for 1
second.

**stream TX/RX:** 

This test is intended to measure the
performance/overhead of the stream, which consist of codec, RTP/RTCP
processing, and de-jitter buffering. In addition it also tests the
performance of Secure RTP (SRTP) for various setting combinations and
codec bandwidth. Since the test here also consists of codec processing
(encoding and decoding), you need to subtract the result with the result
of the corresponding codec to measure the overhead of the stream and
SRTP only.

Results
-------

PJSIP-0.9.0, Linux, ARM9 (ARM926EJ-S), gcc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::
   
   +-------------------+--------------------------------------------------+
   | Hardware:         | Olimex SAM9-L9260 board                          |
   +===================+==================================================+
   | Platform:         | Linux 2.6.23                                     |
   +-------------------+--------------------------------------------------+
   | Processor:        | ARM926EJ-S rev 5 (v5l)                           |
   +-------------------+--------------------------------------------------+
   | Speed:            | 180 MHz                                          |
   +-------------------+--------------------------------------------------+
   | Assumed MIPS:     | 198 MIPS                                         |
   +-------------------+--------------------------------------------------+
   | BogoMIPS:         | 98.91                                            |
   +-------------------+--------------------------------------------------+
   | Compilation:      | arm-926-linux-gnu-gcc -O2 -msoft-float -DNDEBUG  |
   |                   | -DPJ_HAS_FLOATING_POINT=0                        |
   +-------------------+--------------------------------------------------+
   | gcc:              | version 4.2.1 -with-cpu=arm926ej-s               |
   |                   | -march=armv5te -msoft-float -with-float=soft     |
   +-------------------+--------------------------------------------------+

Result:

::

   00:59:38.531 os_core_unix.c pjlib 0.9.0-trunk for POSIX initialized
   MIPS test, with CPU=180Mhz,  198.0 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                          181    0.018    0.04
    8KHz conference bridge with 1 call              6682    0.668    1.32
    8KHz conference bridge with 2 calls            11943    1.194    2.36
    8KHz conference bridge with 4 calls            22402    2.240    4.44
    8KHz conference bridge with 8 calls            42969    4.297    8.51
    8KHz conference bridge with 16 calls           83328    8.333   16.50
    8KHz upsample+downsample - linear               5815    0.581    1.15
    8KHz upsample+downsample - small filter        66786    6.679   13.22
    8KHz upsample+downsample - large filter       870754   87.075  172.41
    8KHz WSOLA PLC - 0% loss                         605    0.060    0.12
    8KHz WSOLA PLC - 2% loss                        1004    0.100    0.20
    8KHz WSOLA PLC - 5% loss                        1541    0.154    0.31
    8KHz WSOLA PLC - 10% loss                       1803    0.180    0.36
    8KHz WSOLA PLC - 20% loss                       3102    0.310    0.61
    8KHz WSOLA PLC - 50% loss                       8431    0.843    1.67
    8KHz WSOLA discard 2% excess                     214    0.021    0.04
    8KHz WSOLA discard 5% excess                     488    0.049    0.10
    8KHz WSOLA discard 10% excess                   1178    0.118    0.23
    8KHz WSOLA discard 20% excess                   2009    0.201    0.40
    8KHz WSOLA discard 50% excess                   6432    0.643    1.27
    8KHz echo canceller 100ms tail len            335870   33.587   66.50
    8KHz echo canceller 128ms tail len            336225   33.623   66.57
    8KHz echo canceller 200ms tail len            349240   34.924   69.15
    8KHz echo canceller 256ms tail len            363206   36.321   71.91
    8KHz echo canceller 400ms tail len            400026   40.003   79.21
    8KHz echo canceller 500ms tail len            426646   42.665   84.48
    8KHz echo canceller 512ms tail len            432291   43.229   85.59
    8KHz echo canceller 600ms tail len            454965   45.496   90.08
    8KHz echo canceller 800ms tail len            516487   51.649  102.26
    8KHz tone generator with single freq             920    0.092    0.18
    8KHz tone generator with dual freq              1428    0.143    0.28
    8KHz codec encode/decode - G.711                2701    0.270    0.53
    8KHz codec encode/decode - GSM                 75750    7.575   15.00
    8KHz codec encode/decode - iLBC              2856203  285.620  565.53
    8KHz codec encode/decode - Speex 8Khz         436162   43.616   86.36
    8KHz codec encode/decode - L16/8000/1           1704    0.170    0.34
    8KHz stream TX/RX - G.711                       6786    0.679    1.34
    8KHz stream TX/RX - G.711 SRTP 32bit           21688    2.169    4.29
    8KHz stream TX/RX - G.711 SRTP 32bit +auth     33501    3.350    6.63
    8KHz stream TX/RX - G.711 SRTP 80bit           21725    2.172    4.30
    8KHz stream TX/RX - G.711 SRTP 80bit +auth     33551    3.355    6.64
    8KHz stream TX/RX - GSM                        82035    8.203   16.24
    8KHz stream TX/RX - GSM SRTP 32bit             90890    9.089   18.00
    8KHz stream TX/RX - GSM SRTP 32bit + auth      99334    9.933   19.67
    8KHz stream TX/RX - GSM SRTP 80bit             90893    9.089   18.00
    8KHz stream TX/RX - GSM SRTP 80bit + auth      99356    9.936   19.67
   16KHz get from memplayer                          239    0.024    0.05
   16KHz conference bridge with 1 call             12780    1.278    2.53
   16KHz conference bridge with 2 calls            23052    2.305    4.56
   16KHz conference bridge with 4 calls            43174    4.317    8.55
   16KHz conference bridge with 8 calls            82096    8.210   16.26
   16KHz conference bridge with 16 calls          158565   15.856   31.40
   16KHz upsample+downsample - linear              11469    1.147    2.27
   16KHz upsample+downsample - small filter       133088   13.309   26.35
   16KHz upsample+downsample - large filter      1739742  173.974  344.47
   16KHz WSOLA PLC - 0% loss                         980    0.098    0.19
   16KHz WSOLA PLC - 2% loss                        1910    0.191    0.38
   16KHz WSOLA PLC - 5% loss                        3734    0.373    0.74
   16KHz WSOLA PLC - 10% loss                       7867    0.787    1.56
   16KHz WSOLA PLC - 20% loss                      13007    1.301    2.58
   16KHz WSOLA PLC - 50% loss                      29022    2.902    5.75
   16KHz WSOLA discard 2% excess                     551    0.055    0.11
   16KHz WSOLA discard 5% excess                    1027    0.103    0.20
   16KHz WSOLA discard 10% excess                   1973    0.197    0.39
   16KHz WSOLA discard 20% excess                  10454    1.045    2.07
   16KHz WSOLA discard 50% excess                  22276    2.228    4.41
   16KHz echo canceller 100ms tail len            664649   66.465  131.60
   16KHz echo canceller 128ms tail len            682686   68.269  135.17
   16KHz echo canceller 200ms tail len            720924   72.092  142.74
   16KHz echo canceller 256ms tail len            752928   75.293  149.08
   16KHz echo canceller 400ms tail len            877528   87.753  173.75
   16KHz echo canceller 500ms tail len            970559   97.056  192.17
   16KHz echo canceller 512ms tail len            989839   98.984  195.99
   16KHz echo canceller 600ms tail len           1065465  106.547  210.96
   16KHz echo canceller 800ms tail len           1285075  128.508  254.44
   16KHz tone generator with single freq            1617    0.162    0.32
   16KHz tone generator with dual freq              2632    0.263    0.52
   16KHz codec encode/decode - G.722              148080   14.808   29.32
   16KHz codec encode/decode - Speex 16Khz        979202   97.920  193.88
   16KHz codec encode/decode - L16/16000/1          3244    0.324    0.64
   16KHz stream TX/RX - G.722                     155685   15.568   30.83

PJSIP-0.9.0, PocketPC 2003, XScale PXA270, embedded Visual C++, Optimized Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ===================== ====================================
   Hardware:             Dell Axim X30 PDA
   ===================== ====================================
   Platform:             PocketPC 2003
   Processor:            Intel XScale PXA270
   Speed:                312 MHz
   Assumed MIPS:         400 MIPS
   BogoMIPS:             -
   Compilation switches: /Oxt /QRarch5T /QRdsp /QRxscale
   Compiler:             Embedded Visual C++ 4 (v4.00.1610.0)
   Settings:             PJ_HAS_FLOATING_POINT=0
   ===================== ====================================

**Note:**
   
   All PJMEDIA features are enabled for this test, which
   normally is not the case for typical use (e.g. normally we would replace
   AEC with the simpler echo suppressor).

Result:

::

   06:19:52.000 os_core_win32. pjlib 0.9.0-trunk for win32 initialized
   MIPS test, with CPU=312Mhz,  400.0 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                          154    0.015    0.06
    8KHz conference bridge with 1 call              7499    0.750    3.00
    8KHz conference bridge with 2 calls            13244    1.324    5.30
    8KHz conference bridge with 4 calls            23570    2.357    9.43
    8KHz conference bridge with 8 calls            37377    3.738   14.95
    8KHz conference bridge with 16 calls           60895    6.089   24.36
    8KHz upsample+downsample - linear               3695    0.370    1.48
    8KHz upsample+downsample - small filter        43537    4.354   17.41
    8KHz upsample+downsample - large filter       393547   39.355  157.41
    8KHz WSOLA PLC - 0% loss                         501    0.050    0.20
    8KHz WSOLA PLC - 2% loss                         542    0.054    0.22
    8KHz WSOLA PLC - 5% loss                         568    0.057    0.23
    8KHz WSOLA PLC - 10% loss                        960    0.096    0.38
    8KHz WSOLA PLC - 20% loss                       1656    0.166    0.66
    8KHz WSOLA PLC - 50% loss                       4464    0.446    1.79
    8KHz WSOLA discard 2% excess                     157    0.016    0.06
    8KHz WSOLA discard 5% excess                     296    0.030    0.12
    8KHz WSOLA discard 10% excess                    621    0.062    0.25
    8KHz WSOLA discard 20% excess                    931    0.093    0.37
    8KHz WSOLA discard 50% excess                   3237    0.324    1.29
    8KHz echo canceller 100ms tail len            298351   29.835  119.34
    8KHz echo canceller 128ms tail len            296880   29.688  118.75
    8KHz echo canceller 200ms tail len            324207   32.421  129.68
    8KHz echo canceller 256ms tail len            316040   31.604  126.41
    8KHz echo canceller 400ms tail len            346520   34.652  138.60
    8KHz echo canceller 500ms tail len            363378   36.338  145.35
    8KHz echo canceller 512ms tail len            363101   36.310  145.23
    8KHz echo canceller 600ms tail len            382216   38.222  152.88
    8KHz echo canceller 800ms tail len            410368   41.037  164.14
    8KHz tone generator with single freq            1400    0.140    0.56
    8KHz tone generator with dual freq              2554    0.255    1.02
    8KHz codec encode/decode - G.711                1536    0.154    0.61
    8KHz codec encode/decode - GSM                 68559    6.856   27.42
    8KHz codec encode/decode - iLBC              6337042  633.704 2534.72
    8KHz codec encode/decode - Speex 8Khz         318969   31.897  127.58
    8KHz codec encode/decode - L16/8000/1           2607    0.261    1.04
    8KHz stream TX/RX - G.711                       5022    0.502    2.01
    8KHz stream TX/RX - G.711 SRTP 32bit           12869    1.287    5.15
    8KHz stream TX/RX - G.711 SRTP 32bit +auth     21636    2.164    8.65
    8KHz stream TX/RX - G.711 SRTP 80bit           12905    1.291    5.16
    8KHz stream TX/RX - G.711 SRTP 80bit +auth     21558    2.156    8.62
    8KHz stream TX/RX - GSM                        86629    8.663   34.65
    8KHz stream TX/RX - GSM SRTP 32bit             95385    9.538   38.15
    8KHz stream TX/RX - GSM SRTP 32bit + auth     104510   10.451   41.80
    8KHz stream TX/RX - GSM SRTP 80bit             96748    9.675   38.70
    8KHz stream TX/RX - GSM SRTP 80bit + auth     109251   10.925   43.70
   16KHz get from memplayer                          134    0.013    0.05
   16KHz conference bridge with 1 call              9107    0.911    3.64
   16KHz conference bridge with 2 calls            16020    1.602    6.41
   16KHz conference bridge with 4 calls            30208    3.021   12.08
   16KHz conference bridge with 8 calls            56875    5.688   22.75
   16KHz conference bridge with 16 calls          124328   12.433   49.73
   16KHz upsample+downsample - linear               6994    0.699    2.80
   16KHz upsample+downsample - small filter        87700    8.770   35.08
   16KHz upsample+downsample - large filter       823986   82.399  329.58
   16KHz WSOLA PLC - 0% loss                         639    0.064    0.26
   16KHz WSOLA PLC - 2% loss                        1119    0.112    0.45
   16KHz WSOLA PLC - 5% loss                        1372    0.137    0.55
   16KHz WSOLA PLC - 10% loss                       5312    0.531    2.12
   16KHz WSOLA PLC - 20% loss                       7274    0.727    2.91
   16KHz WSOLA PLC - 50% loss                      13206    1.321    5.28
   16KHz WSOLA discard 2% excess                      80    0.008    0.03
   16KHz WSOLA discard 5% excess                     342    0.034    0.14
   16KHz WSOLA discard 10% excess                   2084    0.208    0.83
   16KHz WSOLA discard 20% excess                   3286    0.329    1.31
   16KHz WSOLA discard 50% excess                  10756    1.076    4.30
   16KHz echo canceller 100ms tail len            567743   56.774  227.09
   16KHz echo canceller 128ms tail len            580722   58.072  232.28
   16KHz echo canceller 200ms tail len            637630   63.763  255.04
   16KHz echo canceller 256ms tail len            627308   62.731  250.91
   16KHz echo canceller 400ms tail len            709140   70.914  283.64
   16KHz echo canceller 500ms tail len            744817   74.482  297.91
   16KHz echo canceller 512ms tail len            741073   74.107  296.42
   16KHz echo canceller 600ms tail len            760064   76.006  304.01
   16KHz echo canceller 800ms tail len           1231781  123.178  492.69
   16KHz tone generator with single freq            2372    0.237    0.95
   16KHz tone generator with dual freq              4679    0.468    1.87
   16KHz codec encode/decode - G.722               91761    9.176   36.70
   16KHz codec encode/decode - Speex 16Khz        642039   64.204  256.81
   16KHz codec encode/decode - L16/16000/1          5077    0.508    2.03
   16KHz stream TX/RX - G.722                     106951   10.695   42.78

PJSIP-0.9.0, PocketPC 2003, XScale PXA270, embedded Visual C++, Default Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ===================== ====================================
   Hardware:             Dell Axim X30 PDA
   ===================== ====================================
   Platform:             PocketPC 2003
   Processor:            Intel XScale PXA270
   Speed:                312 MHz
   Assumed MIPS:         400 MIPS
   BogoMIPS:             -
   Compilation switches: /O2
   Compiler:             Embedded Visual C++ 4 (v4.00.1610.0)
   Settings:             PJ_HAS_FLOATING_POINT=0
   ===================== ====================================

**Note:**
   
   - All PJMEDIA features are enabled for this test, which
     normally is not the case for typical use (e.g. normally we would replace
     AEC with the simpler echo suppressor). 
   - This test is the same as
     PocketPC test before (on the same device etc.), except it uses default
     compilation switch ("/O2"). As you can see some components are actually
     running faster in this test (e.g. resample with large filter).

Result:

::

   05:54:44.000 os_core_win32. pjlib 0.9.0-trunk for win32 initialized
   MIPS test, with CPU=312Mhz,  400.0 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                          223    0.022    0.09
    8KHz conference bridge with 1 call              7645    0.765    3.06
    8KHz conference bridge with 2 calls            13513    1.351    5.40
    8KHz conference bridge with 4 calls            23714    2.371    9.49
    8KHz conference bridge with 8 calls            43852    4.385   17.54
    8KHz conference bridge with 16 calls           62205    6.220   24.88
    8KHz upsample+downsample - linear               3706    0.371    1.48
    8KHz upsample+downsample - small filter        45347    4.535   18.14
    8KHz upsample+downsample - large filter       295105   29.510  118.04
    8KHz WSOLA PLC - 0% loss                         477    0.048    0.19
    8KHz WSOLA PLC - 2% loss                         557    0.056    0.22
    8KHz WSOLA PLC - 5% loss                         563    0.056    0.23
    8KHz WSOLA PLC - 10% loss                        894    0.089    0.36
    8KHz WSOLA PLC - 20% loss                       1653    0.165    0.66
    8KHz WSOLA PLC - 50% loss                       4591    0.459    1.84
    8KHz WSOLA discard 2% excess                     157    0.016    0.06
    8KHz WSOLA discard 5% excess                     410    0.041    0.16
    8KHz WSOLA discard 10% excess                    587    0.059    0.23
    8KHz WSOLA discard 20% excess                    953    0.095    0.38
    8KHz WSOLA discard 50% excess                   3309    0.331    1.32
    8KHz echo canceller 100ms tail len            304226   30.423  121.69
    8KHz echo canceller 128ms tail len            303622   30.362  121.44
    8KHz echo canceller 200ms tail len            311213   31.121  124.48
    8KHz echo canceller 256ms tail len            328946   32.895  131.57
    8KHz echo canceller 400ms tail len            349967   34.997  139.98
    8KHz echo canceller 500ms tail len            380970   38.097  152.38
    8KHz echo canceller 512ms tail len            391733   39.173  156.69
    8KHz echo canceller 600ms tail len            409381   40.938  163.75
    8KHz echo canceller 800ms tail len            440756   44.076  176.30
    8KHz tone generator with single freq            1420    0.142    0.57
    8KHz tone generator with dual freq              2576    0.258    1.03
    8KHz codec encode/decode - G.711                1549    0.155    0.62
    8KHz codec encode/decode - GSM                 64635    6.464   25.85
    8KHz codec encode/decode - iLBC              6389367  638.937 2555.64
    8KHz codec encode/decode - Speex 8Khz         349407   34.941  139.76
    8KHz codec encode/decode - L16/8000/1           2610    0.261    1.04
    8KHz stream TX/RX - G.711                       5131    0.513    2.05
    8KHz stream TX/RX - G.711 SRTP 32bit           12962    1.296    5.18
    8KHz stream TX/RX - G.711 SRTP 32bit +auth     21958    2.196    8.78
    8KHz stream TX/RX - G.711 SRTP 80bit           13017    1.302    5.21
    8KHz stream TX/RX - G.711 SRTP 80bit +auth     22050    2.205    8.82
    8KHz stream TX/RX - GSM                        91707    9.171   36.68
    8KHz stream TX/RX - GSM SRTP 32bit             98428    9.843   39.37
    8KHz stream TX/RX - GSM SRTP 32bit + auth     105968   10.597   42.39
    8KHz stream TX/RX - GSM SRTP 80bit             98289    9.829   39.31
    8KHz stream TX/RX - GSM SRTP 80bit + auth     106072   10.607   42.43
   16KHz get from memplayer                          128    0.013    0.05
   16KHz conference bridge with 1 call              8802    0.880    3.52
   16KHz conference bridge with 2 calls            15742    1.574    6.30
   16KHz conference bridge with 4 calls            29302    2.930   11.72
   16KHz conference bridge with 8 calls            59364    5.936   23.74
   16KHz conference bridge with 16 calls          127470   12.747   50.99
   16KHz upsample+downsample - linear               7160    0.716    2.86
   16KHz upsample+downsample - small filter        94963    9.496   37.98
   16KHz upsample+downsample - large filter       587947   58.795  235.17
   16KHz WSOLA PLC - 0% loss                         630    0.063    0.25
   16KHz WSOLA PLC - 2% loss                        1115    0.112    0.45
   16KHz WSOLA PLC - 5% loss                        1367    0.137    0.55
   16KHz WSOLA PLC - 10% loss                       5167    0.517    2.07
   16KHz WSOLA PLC - 20% loss                       7275    0.728    2.91
   16KHz WSOLA PLC - 50% loss                      12988    1.299    5.19
   16KHz WSOLA discard 2% excess                      71    0.007    0.03
   16KHz WSOLA discard 5% excess                     333    0.033    0.13
   16KHz WSOLA discard 10% excess                   2094    0.209    0.84
   16KHz WSOLA discard 20% excess                   4164    0.416    1.67
   16KHz WSOLA discard 50% excess                  11057    1.106    4.42
   16KHz echo canceller 100ms tail len            584349   58.435  233.73
   16KHz echo canceller 128ms tail len            613118   61.312  245.24
   16KHz echo canceller 200ms tail len            622998   62.300  249.19
   16KHz echo canceller 256ms tail len            677070   67.707  270.82
   16KHz echo canceller 400ms tail len            726984   72.698  290.78
   16KHz echo canceller 500ms tail len            743772   74.377  297.50
   16KHz echo canceller 512ms tail len            762680   76.268  305.06
   16KHz echo canceller 600ms tail len            767136   76.714  306.84
   16KHz echo canceller 800ms tail len           1244816  124.482  497.91
   16KHz tone generator with single freq            2416    0.242    0.97
   16KHz tone generator with dual freq              4819    0.482    1.93
   16KHz codec encode/decode - G.722               98258    9.826   39.30
   16KHz codec encode/decode - Speex 16Khz        680165   68.017  272.06
   16KHz codec encode/decode - L16/16000/1          4994    0.499    2.00
   16KHz stream TX/RX - G.722                     102490   10.249   40.99

PJSIP-0.9.0, Linux, Pentium3, gcc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::
   
   ============= =================================================
   Hardware:     IBM X21 Notebook
   ============= =================================================
   Platform:     Linux 2.6.23
   Processor:    Pentium III
   Speed:        700 MHz
   Assumed MIPS: 1895.6 MIPS
   BogoMIPS:     1395.36
   Compilation:  -O3 -march=pentium3 -fomit-frame-pointer -DNDEBUG
   gcc:          version 4.2.3
   ============= =================================================


Result:

::

   02:01:45.561 os_core_unix.c pjlib 0.9.0-trunk for POSIX initialized
   MIPS test, with CPU=700Mhz, 1895.6 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)       
   ----------------------------------------------------------------------
    8KHz get from memplayer                           23    0.002    0.04
    8KHz conference bridge with 1 call               800    0.080    1.52
    8KHz conference bridge with 2 calls             1395    0.140    2.64
    8KHz conference bridge with 4 calls             2522    0.252    4.78
    8KHz conference bridge with 8 calls             4704    0.470    8.92
    8KHz conference bridge with 16 calls            9146    0.915   17.34
    8KHz upsample+downsample - linear                589    0.059    1.12
    8KHz upsample+downsample - small filter         9563    0.956   18.13
    8KHz upsample+downsample - large filter        46644    4.664   88.42
    8KHz WSOLA PLC - 0% loss                         107    0.011    0.20
    8KHz WSOLA PLC - 2% loss                         240    0.024    0.45
    8KHz WSOLA PLC - 5% loss                         466    0.047    0.88
    8KHz WSOLA PLC - 10% loss                        524    0.052    0.99
    8KHz WSOLA PLC - 20% loss                        958    0.096    1.82
    8KHz WSOLA PLC - 50% loss                       2667    0.267    5.06
    8KHz WSOLA discard 2% excess                      57    0.006    0.11
    8KHz WSOLA discard 5% excess                     142    0.014    0.27
    8KHz WSOLA discard 10% excess                    364    0.036    0.69
    8KHz WSOLA discard 20% excess                    631    0.063    1.20
    8KHz WSOLA discard 50% excess                   2081    0.208    3.94
    8KHz echo canceller 100ms tail len             40050    4.005   75.92
    8KHz echo canceller 128ms tail len             33179    3.318   62.89
    8KHz echo canceller 200ms tail len             35161    3.516   66.65
    8KHz echo canceller 256ms tail len             37470    3.747   71.03
    8KHz echo canceller 400ms tail len             45104    4.510   85.50
    8KHz echo canceller 500ms tail len             50504    5.050   95.74
    8KHz echo canceller 512ms tail len             50940    5.094   96.56
    8KHz echo canceller 600ms tail len             56113    5.611  106.37
    8KHz echo canceller 800ms tail len             71677    7.168  135.87
    8KHz tone generator with single freq            1758    0.176    3.33
    8KHz tone generator with dual freq              3506    0.351    6.65
    8KHz codec encode/decode - G.711                 357    0.036    0.68
    8KHz codec encode/decode - GSM                 11382    1.138   21.58
    8KHz codec encode/decode - iLBC                46894    4.689   88.89
    8KHz codec encode/decode - Speex 8Khz          64428    6.443  122.13
    8KHz codec encode/decode - L16/8000/1            248    0.025    0.47
    8KHz stream TX/RX - G.711                        617    0.062    1.17
    8KHz stream TX/RX - G.711 SRTP 32bit            1751    0.175    3.32
    8KHz stream TX/RX - G.711 SRTP 32bit +auth      3161    0.316    5.99
    8KHz stream TX/RX - G.711 SRTP 80bit            1773    0.177    3.36
    8KHz stream TX/RX - G.711 SRTP 80bit +auth      3108    0.311    5.89
    8KHz stream TX/RX - GSM                        11755    1.176   22.28
    8KHz stream TX/RX - GSM SRTP 32bit             12439    1.244   23.58
    8KHz stream TX/RX - GSM SRTP 32bit + auth      13285    1.329   25.18
    8KHz stream TX/RX - GSM SRTP 80bit             12270    1.227   23.26
    8KHz stream TX/RX - GSM SRTP 80bit + auth      13358    1.336   25.32
   16KHz get from memplayer                           27    0.003    0.05
   16KHz conference bridge with 1 call              1522    0.152    2.89
   16KHz conference bridge with 2 calls             2711    0.271    5.14
   16KHz conference bridge with 4 calls             4772    0.477    9.05
   16KHz conference bridge with 8 calls             8913    0.891   16.90
   16KHz conference bridge with 16 calls           18759    1.876   35.56
   16KHz upsample+downsample - linear               1136    0.114    2.15
   16KHz upsample+downsample - small filter        19231    1.923   36.45
   16KHz upsample+downsample - large filter        93066    9.307  176.42
   16KHz WSOLA PLC - 0% loss                         177    0.018    0.34
   16KHz WSOLA PLC - 2% loss                         534    0.053    1.01
   16KHz WSOLA PLC - 5% loss                        1165    0.116    2.21
   16KHz WSOLA PLC - 10% loss                       2796    0.280    5.30
   16KHz WSOLA PLC - 20% loss                       4515    0.451    8.56
   16KHz WSOLA PLC - 50% loss                      10482    1.048   19.87
   16KHz WSOLA discard 2% excess                     168    0.017    0.32
   16KHz WSOLA discard 5% excess                     326    0.033    0.62
   16KHz WSOLA discard 10% excess                    654    0.065    1.24
   16KHz WSOLA discard 20% excess                   3526    0.353    6.68
   16KHz WSOLA discard 50% excess                   7507    0.751   14.23
   16KHz echo canceller 100ms tail len             68547    6.855  129.94
   16KHz echo canceller 128ms tail len             72619    7.262  137.66
   16KHz echo canceller 200ms tail len             78054    7.805  147.96
   16KHz echo canceller 256ms tail len             84739    8.474  160.63
   16KHz echo canceller 400ms tail len            107738   10.774  204.23
   16KHz echo canceller 500ms tail len            129879   12.988  246.20
   16KHz echo canceller 512ms tail len            133796   13.380  253.62
   16KHz echo canceller 600ms tail len            152166   15.217  288.45
   16KHz echo canceller 800ms tail len            205415   20.542  389.38
   16KHz tone generator with single freq            3489    0.349    6.61
   16KHz tone generator with dual freq              6996    0.700   13.26
   16KHz codec encode/decode - G.722               32803    3.280   62.18
   16KHz codec encode/decode - Speex 16Khz        156629   15.663  296.91
   16KHz codec encode/decode - L16/16000/1           434    0.043    0.82
   16KHz stream TX/RX - G.722                      20959    2.096   39.73

PJSIP-0.9.0, Windows 2000, Pentium3, Visual C++ 2005
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ============= ====================
   Hardware:     IBM X21 Notebook
   ============= ====================
   Platform:     Windows 2000 SP3
   Processor:    Pentium III
   Speed:        700 MHz
   Assumed MIPS: 1895.6 MIPS
   BogoMIPS:     -
   Compilation:  Default Release mode
   Compiler:     Visual C++ 2005
   ============= ====================

Result:

::

   15:18:06.721 os_core_win32. pjlib 0.9.0-trunk for win32 initialized
   MIPS test, with CPU=700Mhz, 1895.6 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                           32    0.003    0.06
    8KHz conference bridge with 1 call              1358    0.136    2.57
    8KHz conference bridge with 2 calls             2164    0.216    4.10
    8KHz conference bridge with 4 calls             3887    0.389    7.37
    8KHz conference bridge with 8 calls             7291    0.729   13.82
    8KHz conference bridge with 16 calls           14098    1.410   26.72
    8KHz upsample+downsample - linear               1194    0.119    2.26
    8KHz upsample+downsample - small filter        22243    2.224   42.16
    8KHz upsample+downsample - large filter       101072   10.107  191.59
    8KHz WSOLA PLC - 0% loss                         187    0.019    0.35
    8KHz WSOLA PLC - 2% loss                         304    0.030    0.58
    8KHz WSOLA PLC - 5% loss                         647    0.065    1.23
    8KHz WSOLA PLC - 10% loss                       1125    0.112    2.13
    8KHz WSOLA PLC - 20% loss                       1452    0.145    2.75
    8KHz WSOLA PLC - 50% loss                       4230    0.423    8.02
    8KHz WSOLA discard 2% excess                      27    0.003    0.05
    8KHz WSOLA discard 5% excess                     161    0.016    0.31
    8KHz WSOLA discard 10% excess                    567    0.057    1.07
    8KHz WSOLA discard 20% excess                    903    0.090    1.71
    8KHz WSOLA discard 50% excess                   2931    0.293    5.56
    8KHz echo canceller 100ms tail len             56454    5.645  107.01
    8KHz echo canceller 128ms tail len             57805    5.780  109.58
    8KHz echo canceller 200ms tail len             60698    6.070  115.06
    8KHz echo canceller 256ms tail len             63832    6.383  121.00
    8KHz echo canceller 400ms tail len             71578    7.158  135.68
    8KHz echo canceller 500ms tail len             76887    7.689  145.75
    8KHz echo canceller 512ms tail len             78265    7.826  148.36
    8KHz echo canceller 600ms tail len             82767    8.277  156.89
    8KHz echo canceller 800ms tail len             96976    9.698  183.83
    8KHz tone generator with single freq            3151    0.315    5.97
    8KHz tone generator with dual freq              5812    0.581   11.02
    8KHz codec encode/decode - G.711                 497    0.050    0.94
    8KHz codec encode/decode - GSM                 20364    2.036   38.60
    8KHz codec encode/decode - iLBC                94382    9.438  178.91
    8KHz codec encode/decode - Speex 8Khz         119001   11.900  225.58
    8KHz codec encode/decode - L16/8000/1            944    0.094    1.79
    8KHz stream TX/RX - G.711                        928    0.093    1.76
    8KHz stream TX/RX - G.711 SRTP 32bit            2372    0.237    4.50
    8KHz stream TX/RX - G.711 SRTP 32bit +auth      4181    0.418    7.93
    8KHz stream TX/RX - G.711 SRTP 80bit            2380    0.238    4.51
    8KHz stream TX/RX - G.711 SRTP 80bit +auth      4186    0.419    7.93
    8KHz stream TX/RX - GSM                        21365    2.136   40.50
    8KHz stream TX/RX - GSM SRTP 32bit             22069    2.207   41.83
    8KHz stream TX/RX - GSM SRTP 32bit + auth      23227    2.323   44.03
    8KHz stream TX/RX - GSM SRTP 80bit             22077    2.208   41.85
    8KHz stream TX/RX - GSM SRTP 80bit + auth      23223    2.322   44.02
   16KHz get from memplayer                           39    0.004    0.07
   16KHz conference bridge with 1 call              2692    0.269    5.10
   16KHz conference bridge with 2 calls             4222    0.422    8.00
   16KHz conference bridge with 4 calls             7487    0.749   14.19
   16KHz conference bridge with 8 calls            13969    1.397   26.48
   16KHz conference bridge with 16 calls           27026    2.703   51.23
   16KHz upsample+downsample - linear               2323    0.232    4.40
   16KHz upsample+downsample - small filter        44385    4.438   84.14
   16KHz upsample+downsample - large filter       202334   20.233  383.54
   16KHz WSOLA PLC - 0% loss                         257    0.026    0.49
   16KHz WSOLA PLC - 2% loss                        2253    0.225    4.27
   16KHz WSOLA PLC - 5% loss                         763    0.076    1.45
   16KHz WSOLA PLC - 10% loss                       3265    0.326    6.19
   16KHz WSOLA PLC - 20% loss                       5994    0.599   11.36
   16KHz WSOLA PLC - 50% loss                      14935    1.493   28.31
   16KHz WSOLA discard 2% excess                      27    0.003    0.05
   16KHz WSOLA discard 5% excess                     520    0.052    0.99
   16KHz WSOLA discard 10% excess                   1765    0.176    3.35
   16KHz WSOLA discard 20% excess                   3255    0.326    6.17
   16KHz WSOLA discard 50% excess                  10756    1.076   20.39
   16KHz echo canceller 100ms tail len            115632   11.563  219.19
   16KHz echo canceller 128ms tail len            119961   11.996  227.40
   16KHz echo canceller 200ms tail len            126901   12.690  240.55
   16KHz echo canceller 256ms tail len            133028   13.303  252.17
   16KHz echo canceller 400ms tail len            157148   15.715  297.89
   16KHz echo canceller 500ms tail len            182438   18.244  345.83
   16KHz echo canceller 512ms tail len            186894   18.689  354.28
   16KHz echo canceller 600ms tail len            212014   21.201  401.89
   16KHz echo canceller 800ms tail len            267639   26.764  507.34
   16KHz tone generator with single freq            6209    0.621   11.77
   16KHz tone generator with dual freq             11484    1.148   21.77
   16KHz codec encode/decode - G.722               36735    3.674   69.63
   16KHz codec encode/decode - Speex 16Khz        271141   27.114  513.97
   16KHz codec encode/decode - L16/16000/1          1817    0.182    3.44
   16KHz stream TX/RX - G.722                      38036    3.804   72.10

PJSIP-0.9.0, Windows XP, Pentium 4, Visual Studio 2005
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ============= ===========================================
   Hardware:     HP PC
   ============= ===========================================
   Platform:     Windows XP SP2
   Processor:    Pentium 4 (single core, no Hyper-Threading)
   Speed:        2.6 GHz
   Assumed MIPS: 8102 MIPS
   BogoMIPS:     -
   Compilation:  Default Release settings (/O2)
   Compiler:     Visual Studio 2005
   ============= ===========================================

Result:

::

   09:46:14.571 os_core_win32. pjlib 0.9.0-trunk for win32 initialized
   MIPS test, with CPU=2666Mhz, 8102.0 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                           11    0.001    0.09
    8KHz conference bridge with 1 call               337    0.034    2.73
    8KHz conference bridge with 2 calls              512    0.051    4.15
    8KHz conference bridge with 4 calls              919    0.092    7.45
    8KHz conference bridge with 8 calls             1658    0.166   13.43
    8KHz conference bridge with 16 calls            3180    0.318   25.76
    8KHz upsample+downsample - linear                288    0.029    2.33
    8KHz upsample+downsample - small filter         7822    0.782   63.37
    8KHz upsample+downsample - large filter        38386    3.839  311.00
    8KHz WSOLA PLC - 0% loss                          53    0.005    0.43
    8KHz WSOLA PLC - 2% loss                          61    0.006    0.49
    8KHz WSOLA PLC - 5% loss                         103    0.010    0.83
    8KHz WSOLA PLC - 10% loss                        152    0.015    1.23
    8KHz WSOLA PLC - 20% loss                        195    0.020    1.58
    8KHz WSOLA PLC - 50% loss                        520    0.052    4.21
    8KHz WSOLA discard 2% excess                       8    0.001    0.06
    8KHz WSOLA discard 5% excess                      27    0.003    0.22
    8KHz WSOLA discard 10% excess                     74    0.007    0.60
    8KHz WSOLA discard 20% excess                    117    0.012    0.95
    8KHz WSOLA discard 50% excess                    370    0.037    3.00
    8KHz echo canceller 100ms tail len             20945    2.095  169.70
    8KHz echo canceller 128ms tail len             20484    2.048  165.96
    8KHz echo canceller 200ms tail len             21017    2.102  170.28
    8KHz echo canceller 256ms tail len             21562    2.156  174.69
    8KHz echo canceller 400ms tail len             23030    2.303  186.59
    8KHz echo canceller 500ms tail len             24102    2.410  195.27
    8KHz echo canceller 512ms tail len             24441    2.444  198.02
    8KHz echo canceller 600ms tail len             25380    2.538  205.63
    8KHz echo canceller 800ms tail len             28751    2.875  232.94
    8KHz tone generator with single freq              84    0.008    0.68
    8KHz tone generator with dual freq               125    0.013    1.01
    8KHz codec encode/decode - G.711                 135    0.014    1.09
    8KHz codec encode/decode - GSM                  6898    0.690   55.89
    8KHz codec encode/decode - iLBC                39783    3.978  322.32
    8KHz codec encode/decode - Speex 8Khz          24543    2.454  198.85
    8KHz codec encode/decode - L16/8000/1            161    0.016    1.30
    8KHz stream TX/RX - G.711                        298    0.030    2.41
    8KHz stream TX/RX - G.711 SRTP 32bit             633    0.063    5.13
    8KHz stream TX/RX - G.711 SRTP 32bit +auth      1063    0.106    8.61
    8KHz stream TX/RX - G.711 SRTP 80bit             634    0.063    5.14
    8KHz stream TX/RX - G.711 SRTP 80bit +auth      1066    0.107    8.64
    8KHz stream TX/RX - GSM                         7182    0.718   58.19
    8KHz stream TX/RX - GSM SRTP 32bit              7353    0.735   59.57
    8KHz stream TX/RX - GSM SRTP 32bit + auth       7693    0.769   62.33
    8KHz stream TX/RX - GSM SRTP 80bit              7313    0.731   59.25
    8KHz stream TX/RX - GSM SRTP 80bit + auth       7673    0.767   62.17
   16KHz get from memplayer                            8    0.001    0.06
   16KHz conference bridge with 1 call               592    0.059    4.80
   16KHz conference bridge with 2 calls              907    0.091    7.35
   16KHz conference bridge with 4 calls             1620    0.162   13.13
   16KHz conference bridge with 8 calls             3055    0.306   24.75
   16KHz conference bridge with 16 calls            5799    0.580   46.98
   16KHz upsample+downsample - linear                560    0.056    4.54
   16KHz upsample+downsample - small filter        15505    1.551  125.62
   16KHz upsample+downsample - large filter        76944    7.694  623.40
   16KHz WSOLA PLC - 0% loss                          52    0.005    0.42
   16KHz WSOLA PLC - 2% loss                         263    0.026    2.13
   16KHz WSOLA PLC - 5% loss                         113    0.011    0.92
   16KHz WSOLA PLC - 10% loss                        383    0.038    3.10
   16KHz WSOLA PLC - 20% loss                        742    0.074    6.01
   16KHz WSOLA PLC - 50% loss                       1757    0.176   14.24
   16KHz WSOLA discard 2% excess                       9    0.001    0.07
   16KHz WSOLA discard 5% excess                      69    0.007    0.56
   16KHz WSOLA discard 10% excess                    220    0.022    1.78
   16KHz WSOLA discard 20% excess                    403    0.040    3.27
   16KHz WSOLA discard 50% excess                   1301    0.130   10.54
   16KHz echo canceller 100ms tail len             42084    4.208  340.96
   16KHz echo canceller 128ms tail len             42697    4.270  345.93
   16KHz echo canceller 200ms tail len             43782    4.378  354.72
   16KHz echo canceller 256ms tail len             45008    4.501  364.65
   16KHz echo canceller 400ms tail len             49519    4.952  401.20
   16KHz echo canceller 500ms tail len             51945    5.194  420.86
   16KHz echo canceller 512ms tail len             52492    5.249  425.29
   16KHz echo canceller 600ms tail len             54984    5.498  445.48
   16KHz echo canceller 800ms tail len             60065    6.006  486.65
   16KHz tone generator with single freq             161    0.016    1.30
   16KHz tone generator with dual freq               239    0.024    1.94
   16KHz codec encode/decode - G.722                9354    0.935   75.79
   16KHz codec encode/decode - Speex 16Khz         51086    5.109  413.90
   16KHz codec encode/decode - L16/16000/1           304    0.030    2.46
   16KHz stream TX/RX - G.722                       9570    0.957   77.54

PJSIP-0.9.0, Windows Vista 64bit, AMD Phenom 9850, Visual Studio 2005
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   ============= =================================================
   Hardware:     Self-assembled
   ============= =================================================
   Platform:     Windows Vista 64bit SP1
   Processor:    AMD Phenom 9850 (quad core, with Hyper-Threading)
   Speed:        2.5 GHz
   Assumed MIPS: 8783.3 MIPS (per core)
   BogoMIPS:     -
   Compilation:  Default Release settings (/O2)
   Compiler:     Visual Studio 2005
   ============= =================================================

Result:

::

   18:42:52.441 os_core_win32. pjlib 0.9.0-trunk for win32 initialized
   MIPS test, with CPU=2500Mhz, 8783.3 MIPS
   Clock  Item                                      Time     CPU    MIPS
    Rate                                           (usec)    (%)
   ----------------------------------------------------------------------
    8KHz get from memplayer                            9    0.001    0.08
    8KHz conference bridge with 1 call               452    0.045    3.97
    8KHz conference bridge with 2 calls              780    0.078    6.85
    8KHz conference bridge with 4 calls             1551    0.155   13.62
    8KHz conference bridge with 8 calls             3117    0.312   27.38
    8KHz conference bridge with 16 calls            6184    0.618   54.32
    8KHz upsample+downsample - linear                348    0.035    3.06
    8KHz upsample+downsample - small filter         7888    0.789   69.28
    8KHz upsample+downsample - large filter        34632    3.463  304.18
    8KHz WSOLA PLC - 0% loss                          46    0.005    0.40
    8KHz WSOLA PLC - 2% loss                          79    0.008    0.69
    8KHz WSOLA PLC - 5% loss                         179    0.018    1.57
    8KHz WSOLA PLC - 10% loss                        316    0.032    2.78
    8KHz WSOLA PLC - 20% loss                        416    0.042    3.65
    8KHz WSOLA PLC - 50% loss                       1230    0.123   10.80
    8KHz WSOLA discard 2% excess                      10    0.001    0.09
    8KHz WSOLA discard 5% excess                      49    0.005    0.43
    8KHz WSOLA discard 10% excess                    166    0.017    1.46
    8KHz WSOLA discard 20% excess                    263    0.026    2.31
    8KHz WSOLA discard 50% excess                    849    0.085    7.46
    8KHz echo canceller 100ms tail len             15281    1.528  134.22
    8KHz echo canceller 128ms tail len             16319    1.632  143.33
    8KHz echo canceller 200ms tail len             17098    1.710  150.18
    8KHz echo canceller 256ms tail len             18079    1.808  158.79
    8KHz echo canceller 400ms tail len             20356    2.036  178.79
    8KHz echo canceller 500ms tail len             21685    2.168  190.46
    8KHz echo canceller 512ms tail len             21992    2.199  193.16
    8KHz echo canceller 600ms tail len             23288    2.329  204.54
    8KHz echo canceller 800ms tail len             26313    2.631  231.11
    8KHz tone generator with single freq             675    0.068    5.93
    8KHz tone generator with dual freq              1320    0.132   11.59
    8KHz codec encode/decode - G.711                 161    0.016    1.41
    8KHz codec encode/decode - GSM                  6462    0.646   56.76
    8KHz codec encode/decode - iLBC                40037    4.004  351.65
    8KHz codec encode/decode - Speex 8Khz          23053    2.305  202.48
    8KHz codec encode/decode - L16/8000/1             87    0.009    0.76
    8KHz stream TX/RX - G.711                        172    0.017    1.51
    8KHz stream TX/RX - G.711 SRTP 32bit             461    0.046    4.05
    8KHz stream TX/RX - G.711 SRTP 32bit +auth       701    0.070    6.16
    8KHz stream TX/RX - G.711 SRTP 80bit             461    0.046    4.05
    8KHz stream TX/RX - G.711 SRTP 80bit +auth      1342    0.134   11.79
    8KHz stream TX/RX - GSM                         6729    0.673   59.10
    8KHz stream TX/RX - GSM SRTP 32bit              6965    0.697   61.18
    8KHz stream TX/RX - GSM SRTP 32bit + auth       7320    0.732   64.29
    8KHz stream TX/RX - GSM SRTP 80bit              6966    0.697   61.18
    8KHz stream TX/RX - GSM SRTP 80bit + auth       7323    0.732   64.32
   16KHz get from memplayer                            7    0.001    0.06
   16KHz conference bridge with 1 call               882    0.088    7.75
   16KHz conference bridge with 2 calls             1514    0.151   13.30
   16KHz conference bridge with 4 calls             2943    0.294   25.85
   16KHz conference bridge with 8 calls             5747    0.575   50.48
   16KHz conference bridge with 16 calls           11432    1.143  100.41
   16KHz upsample+downsample - linear                672    0.067    5.90
   16KHz upsample+downsample - small filter        15662    1.566  137.56
   16KHz upsample+downsample - large filter        34666    3.467  304.48
   16KHz WSOLA PLC - 0% loss                          26    0.003    0.23
   16KHz WSOLA PLC - 2% loss                         315    0.032    2.77
   16KHz WSOLA PLC - 5% loss                         183    0.018    1.61
   16KHz WSOLA PLC - 10% loss                        927    0.093    8.14
   16KHz WSOLA PLC - 20% loss                       1716    0.172   15.07
   16KHz WSOLA PLC - 50% loss                       4321    0.432   37.95
   16KHz WSOLA discard 2% excess                      11    0.001    0.10
   16KHz WSOLA discard 5% excess                     156    0.016    1.37
   16KHz WSOLA discard 10% excess                    518    0.052    4.55
   16KHz WSOLA discard 20% excess                    952    0.095    8.36
   16KHz WSOLA discard 50% excess                   3117    0.312   27.38
   16KHz echo canceller 100ms tail len             33300    3.330  292.48
   16KHz echo canceller 128ms tail len             17047    1.705  149.73
   16KHz echo canceller 200ms tail len             17643    1.764  154.96
   16KHz echo canceller 256ms tail len             37227    3.723  326.97
   16KHz echo canceller 400ms tail len             40963    4.096  359.79
   16KHz echo canceller 500ms tail len             43948    4.395  386.01
   16KHz echo canceller 512ms tail len             26078    2.608  229.05
   16KHz echo canceller 600ms tail len             23438    2.344  205.86
   16KHz echo canceller 800ms tail len             26229    2.623  230.38
   16KHz tone generator with single freq             669    0.067    5.88
   16KHz tone generator with dual freq              1323    0.132   11.62
   16KHz codec encode/decode - G.722               10382    1.038   91.19
   16KHz codec encode/decode - Speex 16Khz         55105    5.510  484.00
   16KHz codec encode/decode - L16/16000/1           161    0.016    1.41
   16KHz stream TX/RX - G.722                      10755    1.076   94.46

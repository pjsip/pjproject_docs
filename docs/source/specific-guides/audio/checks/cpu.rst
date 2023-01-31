Check CPU utilization
======================


High CPU utilization could cause audio problems, hence check that CPU utilization is 
not too high during the call. Sometimes CPU utilization as low as 75% is enough to 
cause audio distruptions in some systems, while in others the audio quality is 
still fine even with >90% CPU utilization. 

If the CPU utilization is too high, the following suggestions can be followed:

#. Disable echo canceller (with pjsua, EC is by default enabled. Use ``--ec-tail 0`` 
   command line argument to disable EC).
#. If complex codecs such as Speex or iLBC is used, try to use PCMU or PCMA 
   (pjsua by default uses Speex/16KHz. Use ``--add-codec pcmu`` to use PCMU).
#. Use the release build instead of debug build (remove ``-g`` option from 
   ``CFLAGS`` if gcc is used).
#. Lower the pjmedia's internal sampling rate (by default pjsua uses 16KHz or 
   44.1KHz-48KHz in Mac OS. 
   Use ``---clock-rate 8000`` command line argument to *pjsua* to override the 
   internal clockrate to 8000). However, when changing the clock rate, make sure 
   that this clock rate matches the clock rate of the codec to be used, or otherwise 
   resampling will be applied!
#. Close other applications that consume CPU.
#. Have a look at :any:`/specific-guides/perf_footprint/pjmedia_mips` for detailed
   performance assessment of each PJMEDIA (audio) media components, and consider
   disabling or replacing complex components when necessary.


.. tip::

   This article was originally written in 2006, when the author's main computer was
   a PIII/600MHz, and even then PJSIP was running fine. Fast forward to 2023, nowdays
   most hardware should be faster than that.


Using PJSIP in applications
===============================

#. Build ``pjproject``.
#. Create application source directory (outside the PJSIP sources).
#. Create a sample ``myapp.c``:

   .. code-block:: c

      #include <pjsua-lib/pjsua.h>
      #include <pj/log.h>

      int main()
      {
         pj_status_t status;

         status = pjsua_create();
         PJ_LOG(3,("myapp.c", "Hello PJSIP! Bye PJSIP."));
         pjsua_destroy();
         return 0;
      }

#. Create ``Makefile`` for the sample application:

   .. code-block:: makefile

      PJDIR = /path/to/pjproject
      include $(PJDIR)/build.mak

      myapp: myapp.o
              $(PJ_CC) -o $@ $< $(PJ_LDFLAGS) $(PJ_LDLIBS)

      myapp.o: myapp.c
              $(PJ_CC) -c -o $@ $< $(PJ_CFLAGS)

      clean:
              rm -f myapp.o myapp


   .. note::

      Replace ``PJDIR`` with path to pjproject source tree.

   Alternatively, if ``make install`` was run (on PJSIP) and if **pkg-config** tool is available,
   you can use ``pkg-config --cflags`` and ``pkg-config --libs`` as usual.

#. Run ``make``.


Using thread with PJSUA initialization and shutdown
====================================================

To use PJSIP, it is recommended to call :cpp:any:`pj_init` and :cpp:any:`pj_shutdown()` from the main thread. After :cpp:any:`pj_init()` is completed, application can continue with the initialization or create a secondary/worker thread and register the thread by calling :cpp:any:`pj_thread_register()` 

Creating a secondary thread is especially recommended, sometimes necessary, for apps that require main thread to be responsive, such as GUI apps, or apps that use video, or real-time apps.

As described in :doc:`Basic API documentation </api/generated/pjsip/group/group__PJSUA__LIB__BASE>`, app needs to call :cpp:any:`pjsua_create()`, :cpp:any:`pjsua_pool_create()`, :cpp:any:`pjsua_init()` to perform the initialization. Then app must call :cpp:any:`pjsua_start()` to start PJSUA and finally after everything is done, call :cpp:any:`pjsua_destroy()` to shut it down. Sample code:

.. code-block:: c

 int main()
 {
     pj_init();
     // Continue with PJSUA initialization here or create a secondary thread
     ....
     // After pjsua_destroy() is called
     pj_shutdown();
 }

 int worker_thread()
 {
     // Register the thread, after pj_init() is called
     pj_thread_register();

     // Create pjsua and pool
     pjsua_create();
     pjsua_pool_create();

     // Init pjsua
     pjsua_init();

     // Start pjsua
     pjsua_start();

     .........

     // Destroy pjsua
     pjsua_destroy();
 }


When restarting the library, after :cpp:any:`pjsua_destroy()` is completed, application needs to call :cpp:any:`pj_shutdown()` and :cpp:any:`pj_init()` in the main thread.

Application also needs to make sure that the number of calls to :cpp:any:`pj_shutdown()` matches with the calls to :cpp:any:`pj_init()`.

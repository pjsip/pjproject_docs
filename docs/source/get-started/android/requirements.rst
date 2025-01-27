Install the required tools and library
=======================================

In this section, we will install the required libraries and tools to build and develop Android SIP
client applications supporting voice/VoIP calls, video, and secure communication using TLS and
secure RTP (SRTP).

We tried to present the minimum and optimum features in this tutorial. You can install other,
optional features by clicking the relevant feature in :doc:`sip-sdk-features` page.


.. contents:: Installation steps:
   :depth: 2
   :local:



Install Android Android Studio and Android NDK
------------------------------------------------------

While PJSIP only requires the NDK to build, you usually need Android Studio to develop your
application, and it is recommended to install the NDK from Android Studio's SDK manager anyway,
hence let's install them by following the instructions here:

  - Install `Android Studio <https://developer.android.com/studio>`__
  - Install `Android NDK <https://developer.android.com/ndk>`__.

This tutorial uses *Android Studio Ladybug Feature Drop 2024.2.2* and *NDK 28.0.12916984*
on *Ubuntu 22.04*.


Install SWIG
-------------------------------------------

SWIG is used to create high level language bindings (such as Java, C#, Python) for
:doc:`PJSUA2 API </api/pjsua2/index>`.

To install it, follow the instructions from `SWIG <http://www.swig.org/download.html>`__ homepage.

Make sure SWIG is accessible in the PATH. You can check by running:

.. code-block:: shell

  $ swig -version

  SWIG Version 4.0.2

  Compiled with g++ [x86_64-pc-linux-gnu]

  Configured options: +pcre

  Please see http://www.swig.org for reporting bugs and further information



Download and extract Oboe
-------------------------------------------

We recommend Oboe for Android audio device:

- download Oboe prefab package (`.aar` file) from https://github.com/google/oboe/releases
- extract it somewhere in your system, save the location to **OBOE_DIR** environment variable
  (we will refer to it later).

  .. code-block:: shell

    $ export OBOE_DIR=/home/whoever/Android/oboe-1.9.3

For additional information, see :ref:`oboe`.


.. _android_openssl:

Install OpenSSL
-------------------------------------------

Let's use TLS in our demo as a good security practice. To install it:

1. Download OpenSSL release from https://github.com/openssl/openssl/releases (we tested with
   versions from 1.1.0 to 3.4)
2. Extract to some directory
3. follow the instructions in `Notes-ANDROID <https://github.com/openssl/openssl/blob/master/NOTES-ANDROID.md>`__
   to build it for Android. Sample commands:

   .. code-block:: shell

    # in OpenSSL directory
    $ export ANDROID_NDK_ROOT=[your_android_ndk_path]
    $ PATH=$ANDROID_NDK_ROOT/toolchains/llvm/prebuilt/linux-x86_64/bin:$ANDROID_NDK_ROOT/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin:$PATH
    $ ./Configure android-arm64 -D__ANDROID_API__=29
    $ make

   There is no need to run **make install**.

4. Create a ``lib`` directory and copy the libraries to it:

   .. code-block:: shell

    # in OpenSSL directory
    $ mkdir lib
    $ cp lib*.a lib/
    $ ls lib
    libcrypto.a  libssl.a

5. Save the location to **OPENSSL_DIR** environment variable (we will refer to it later).

   .. code-block:: shell

    $ export OPENSSL_DIR=/home/whoever/Android/openssl-3.4.0



Download PJSIP
-------------------------------------------

Download PJSIP tarballs from `PJSIP download page <https://pjsip.org/download.htm>`__, or clone 
`pjproject GitHub repository <https://github.com/pjsip/pjproject>`__ to get the latest
and greatest version.

Extract or clone ``pjproject`` somewhere in your system. This tutorial uses PJSIP version 2.15.1.


What's next
-------------------------------------------
Now that we have all the required libraries and tools installed, we are ready to build PJSIP and
its JAVA interface.

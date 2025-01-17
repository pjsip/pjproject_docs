Install the required tools and library
=======================================

In this section, we will install the required libraries and tools to build our Android SIP VoIP and
video call client application.

.. contents:: In this page:
   :depth: 2
   :local:



Install Android Android Studio and Android NDK
------------------------------------------------------

While PJSIP only requires the NDK to build, you usually need Android Studio to develop your
application, and it is recommended to install the NDK from Android Studio's SDK manager anyway,
hence let's install them by following the instructions here:

  - `Android Studio <https://developer.android.com/studio>`__
  - `Android NDK <https://developer.android.com/ndk>`__.


Install SWIG
-------------------------------------------

SWIG is used to create Java language binding for :doc:`PJSUA2 API </api/pjsua2/index>`.

To install it, follow the instructions from `SWIG <http://www.swig.org/download.html>`__ homepage.

You can check your installation:

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
- extract it somewhere in your system, take note of the location, e.g.

.. code-block:: shell

  $ export OBOE_DIR=/home/whoever/Android/oboe-1.9.3

For additional information, see :ref:`oboe`.


Install OpenSSL
-------------------------------------------

While TLS is optional for our demo, let's install and use it for demonstration purpose.

- download OpenSSL release from https://github.com/openssl/openssl/releases (we tested with
  version 3.4)
- extract to some directory
- follow the instructions in `Notes-ANDROID <https://github.com/openssl/openssl/blob/master/NOTES-ANDROID.md>`__
  to build it for Android
- copy the libraries to ``lib`` directory:

.. code-block:: shell

  # in OpenSSL directory
  $ mkdir lib
  $ cp lib*.a lib/
  $ ls lib
  libcrypto.a  libssl.a

- take note of the location, e.g.

.. code-block:: shell

  $ export OPENSSL_DIR=/home/whoever/Android/openssl-3.4.0


Installing OpenH264 (optional)
----------------------------------
#. For general information on OpenH264 integration see :ref:`openh264`
#. Copy all library .so files into your Android application project directory, 
   for example:

   .. code-block:: shell

     cp /Users/me/openh264/android/*.so /Users/me/pjproject-2.0/pjsip-apps/src/swig/java/android/libs/armeabi


Installing libvpx (optional)
-----------------------------------
See :ref:`libvpx`


Installing ffmpeg (optional)
------------------------------------
See :doc:`/specific-guides/build_int/ffmpeg`


Installing AMediaCodec, native Android codecs (experimental)
-----------------------------------------------------------------
See :ref:`amediacodec`


Download PJSIP
-------------------------------------------

Download PJSIP tarballs from `PJSIP download page <https://pjsip.org/download.htm>`__, or clone 
`pjproject GitHub repository <https://github.com/pjsip/pjproject>`__ to get the latest
and greatest version.

Extract or clone ``pjproject`` somewhere in your system.


Coming up
-------------------------------------------
Now that we have all the required libraries and tools installed, we are ready to build PJSIP and
the SIP client application samples for Android.

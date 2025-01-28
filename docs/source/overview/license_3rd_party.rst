.. _licensing_3rd_party:

Third Party SOFTWARE
=====================

.. contents:: Table of Contents
    :depth: 2


The SOFTWARE may provide links to third party libraries or code (collectively "Third Party 
Software") to implement various functions, and access to Third Party Software may be 
included along with the SOFTWARE delivery as a convenience. Third Party Software does not 
comprise part of the SOFTWARE.

The use of Third Party Software may or may not be made optional (depending on the nature of 
the software).


Contributed and Public Domain Third Party Software
-------------------------------------------------------

ACE Timer Heap
~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Timer heap management of ​Adaptive Communication Framework (ACE) Library
   * - Author
     - Douglas C. Schmidt and his research group at Washington University, University of 
       California, Irvine, and Vanderbilt University, Copyright (c) 1993-2006, all rights reserved
   * - Location
     - - :source:`pjlib/include/pj/timer.h`
       - :source:`pjlib/src/pj/timer.c`
   * - Description
     - The timer heap in PJLIB was based on ACE's Timer_Heap
   * - License
     - Permissions have been obtained from the copyright holder/original author (Douglas C. 
       Schmidt) to use and redistribute this code according to the SOFTWARE licenses. You may, 
       at your option, opt to use ACE license for this particular software.
   * - Usage
     - This code is integral part of the library and can not be disabled.


Alaw/Ulaw Converter
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Alaw/ulaw conversion algorithm 
   * - Author
     - Sun Microsystems, Inc 
   * - Location
     - :source:`pjmedia/src/pjmedia/alaw_ulaw.c`
   * - Description
     - PCM Alaw and U-law conversion
   * - License
     - Free and unrestricted use, see the source code for details.
   * - Usage
     - This software is not used by default unless :c:macro:`PJMEDIA_HAS_ALAW_ULAW_TABLE` is disabled. 
       When :c:macro:`PJMEDIA_HAS_ALAW_ULAW_TABLE` is enabled (the default setting), a table based 
       alaw/ulaw conversion will be used instead. 


CRC32 Algorithm
~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - CRC32 algorithm 
   * - Author
     - Unknown
   * - Location
     - :source:`pjlib-util/src/pjlib-util/crc32.c`
   * - Description
     - 
   * - License
     - This software is put in public domain, and can be used for any purpose with no warranty::

         This is an implementation of CRC32. See ISO 3309 and ITU-T V.42 
         for a formal specification

         This file is partly taken from Crypto++ library (http://www.cryptopp.com)
         and http://www.di-mgt.com.au/crypto.html#CRC.

         Since the original version of the code is put in public domain,
         this file is put on public domain as well.

   * - Usage
     - This code is needed by the STUN implementation in PJNATH and can not be disabled. 


MD5 Hashing Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - MD5 hashing implementation 
   * - Author
     - Written by Colin Plumb in 1993 based on MD5 algorithm by Ron Rivest, no copyright is claimed.
   * - Location
     - :source:`pjlib-util/src/pjlib-util/md5.c`
   * - Description
     - MD5 hashing for digest authentication. 
   * - License
     - Public domain, see the source code for details.
   * - Usage
     - This code is needed by SIP digest authentication procedure, and can not be disabled. 



SHA1 Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - SHA1 Encryption
   * - Author
     - Steve Reid, James H. Brown, Saul Kravitz, Ralph Giles
   * - Location
     - :source:`pjlib-util/src/pjlib-util/sha1.c`
   * - License
     - Public domain, see the source code for details.
   * - Usage
     - This code is needed by the STUN implementation in PJNATH and can not be disabled.


G.722 Codec
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - G.722 audio encoding and decoding algorithm
   * - Author
     - Based on the implementation found in 
       ftp://ftp.cs.cmu.edu/project/fgdata/speech-compression/CCITT-ADPCM/64kbps/adpcm64_g722/. 
       No copyright is claimed on the original source code. The author is possibly Milton Anderson 
       (milton@thumper.bellcore.com) from BELLCORE
   * - Location
     - :sourcedir:`pjmedia/src/pjmedia-codec/g722/`
   * - Description
     - The G.722 codec algorithms are included in PJMEDIA source directory
   * - License
     - Public domain software
   * - Usage
     - This software will only be linked if application explicitly initialize the G.722 library 
       by calling :cpp:any:`pjmedia_codec_g722_init()`. Note that if PJSUA-LIB is used, then this call is 
       made by PJSUA-LIB, hence causing your application to be linked with the software. The 
       software can be explicitly disabled from the link process by defining 
       :c:macro:`PJMEDIA_HAS_G722_CODEC` to zero. 



Third Party Software with Licensing Requirements
-------------------------------------------------------
The use of Third Party Software below will require compliance of the licensing requirements of 
the Third Party Software. You must make sure that your software meets the licensing requirements 
of the third party libraries below. Some third party libraries may require attributions to be 
placed in the software, significant portion of the software, and/or in the accompanying 
documentation. 


GNU Getopt
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Command line parsing library, part of GNU LIBC
   * - Author
     - Copyright (C) 1987,88,89,90,91,92,93,94,96,97 Free Software Foundation, Inc
   * - Location
     - - :source:`pjlib-util/include/pjlib-util/getopt.h`
       - :source:`pjlib-util/src/pjlib-util/getopt.c`
   * - Description
     - Command line parsing library that is used by our sample applications
   * - License
     - GNU LGPL
   * - Usage
     - This code will only be linked if applications explicitly call :cpp:any:`pj_getopt()`
       or :cpp:any:`pj_getopt_long()`. Normally application doesn't need to use this, since this 
       functionality is useful for command line/console types of applications only.


Resample
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - High Quality Sample Rate Conversion
   * - Author
     - https://ccrma.stanford.edu/~jos/resample/
   * - Location
     - :sourcedir:`third_party/resample/`
   * - Description
     - PJMEDIA uses ``resample-1.7.tar.gz`` from 
       `Digital Audio Resampling Home Page <https://ccrma.stanford.edu/~jos/resample/>`__.
   * - License
     - LGPL: :source:`third_party/resample/COPYING`
   * - Usage
     - This resampling software is used by the conference bridge. This software is used 
       when the :c:macro:`PJMEDIA_RESAMPLE_IMP` macro is set to :c:macro:`PJMEDIA_RESAMPLE_LIBRESAMPLE`, 
       which is the default. Other options for resampling backends include Speex and 
       Secret Rabbit Code (which is dual licensed). Please see :c:macro:`PJMEDIA_RESAMPLE_IMP` 
       documentation for more info. 


GSM Codec 06.10
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - `GSM 06.10 <http://kbs.cs.tu-berlin.de/%7Ejutta/toast.html>`_
   * - Author
     - Copyright 1992, 1993, 1994 by Jutta Degener and Carsten Bormann, Technische 
       Universitaet Berlin
   * - Location
     - :sourcedir:`third_party/gsm`
   * - Description
     - PJMEDIA includes uses GSM 06.10 version 1.0 at patchlevel 12 
   * - License
     - Free to use with no warranty: :source:`third_party/gsm/COPYRIGHT`
   * - Usage
     - This software will only be linked if application explicitly initialize the
       GSM library by calling :cpp:any:`pjmedia_codec_gsm_init()`. Note that if PJSUA-LIB 
       is used, then this call is made by PJSUA-LIB, hence causing your application 
       to be linked with the software. The software can be explicitly disabled from 
       the link process by defining :c:macro:`PJMEDIA_HAS_GSM_CODEC` to zero. 


Speex
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Speex codec, acoustic echo cancellation, and sampling rate conversion.
   * - Author
     - https://speex.org/
   * - Location
     - :sourcedir:`third_party/speex/`
   * - Description
     - PJMEDIA uses Speex codec version 1.1.12. Speex is a high quality, Open source, 
       patent free codec implementation developed by open source community.
   * - License
     - :source:`third_party/speex/COPYING`
   * - Usage
     - - **Speex codec**:  this software will only be linked if application explicitly 
         initialize the Speex library by calling :cpp:any:`pjmedia_codec_speex_init()`.
         Note that if PJSUA-LIB is used, then this call is made by PJSUA-LIB, 
         hence causing your application to be linked with the software. The 
         software can be explicitly disabled from the link process by defining 
         :c:macro:`PJMEDIA_HAS_SPEEX_CODEC` to zero.

       - **Speex AEC**: Speex acoustic echo cancellation is enabled by default for 
         the sound device. Application can disable this by setting 
         :c:macro:`PJMEDIA_HAS_SPEEX_AEC` to zero.

       - **Speex sample rate converter**: Speex sample rate converter is only used 
         when :c:macro:`PJMEDIA_HAS_SPEEX_RESAMPLE` macro is set to non-zero. The 
         default is disabled.


iLBC Codec
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - iLBC Audio Codec 
   * - Author
     - `WebRTC Project <http://www.webrtc.org/ilbc-freeware>`_
   * - Location
     - :sourcedir:`third_party/ilbc/`
   * - Description
     - PJMEDIA supports iLBC codec, and iLBC codec implementation is included in PJSIP 
       source distribution. 
   * - License
     - ::
        
        iLBC is distributed under the following free license::

            Copyright 2011 The WebRTC project authors

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions
        are met:

        - Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.

        - Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.

        - Neither the name of Google nor the names of its
          contributors may be used to endorse or promote products derived from
          this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
        A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR
        CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
        PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

   * - Usage
     - This software will only be linked if application explicitly initialize 
       the iLBC library by calling :cpp:any:`pjmedia_codec_ilbc_init()`. Note that if 
       PJSUA-LIB is used, then this call is made by PJSUA-LIB, hence causing 
       your application to be linked with the software. The software can be 
       explicitly disabled from the link process by defining 
       :c:macro:`PJMEDIA_HAS_ILBC_CODEC` to zero. 


G.722.1/C (aka Siren7 and Siren14) codecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Siren7/ITU-T G.722.1, licensed from Polycom, and Siren14/ITU-T 
       G.722.1 Annex C, licensed from Polycom
   * - Author
     - `Polycom <http://www.polycom.com/>`_
   * - Location
     - :sourcedir:`third_party/g7221/`
   * - Description
     - PJMEDIA supports G.722.1/C codecs, and G.722.1/C codec implementation is 
       included in PJSIP source distribution.
   * - License
     - We have acquired a license from Polycom to distribute the codec with PJSIP, 
       however you (the user of PJSIP software) MUST acquire the license from Poly 
       (previously Polycom) yourself to use the codec and/or distribute software 
       linked with the codec. Please see 
       https://web.archive.org/web/20140709022721/http://www.polycom.com/company/about-us/technology/siren/siren-faq.html 
       for more info (this is temporarily a web archive link because when Polycom 
       became Poly the original link disappeared). 
   * - Usage
     - This software is by default disabled, due to the licensing restriction above. 
       The software can be explicitly enabled by defining :c:macro:`PJMEDIA_HAS_G7221_CODEC`
       to one.


Milenage and Rijndael
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Milenage
   * - Author
     - The implementation was taken from 
       `3GPP TS 35.206 V7.0.0 <http://www.3gpp.org/ftp/Specs/archive/35_series/35.206/>`__ 
       document
   * - Location
     - :sourcedir:`third_party/milenage/`
   * - Description
     - Milenage algorithm is used for AKAv1-MD5 and AKAv2 SIP digest authentication.
   * - License
     - Please consult `3GPP TS documents <http://www.3gpp.org/specifications/60-confidentiality-algorithms>`__ ::

         The 3GPP authentication and key generation functions (MILENAGE) have been developed
         through the collaborative efforts of the 3GPP Organizational Partners.

         They may be used only for the development and operation of 3G Mobile Communications and 
         services. There are no additional requirements or authorizations necessary for these 
         algorithms to be implemented.

   * - Usage
     - The Milenage and Rijndael implementation will only be linked with application if 
       AKA authentication is used and application explicitly calls or makes reference to 
       :cpp:any:`pjsip_auth_create_aka_response()` function. 


libSRTP
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - `libSRTP <https://github.com/cisco/libsrtp>`_
   * - Author
     - David A. McGrew, Cisco Systems, Inc. 
   * - Location
     - :sourcedir:`third_party/srtp/`
   * - Description
     - libSRTP implements Secure RTP/RTCP (SRTP and SRTCP).
   * - License
     - BSD 3-clause: :source:`third_party/srtp/README.md`
   * - Usage
     - Copy of libSRTP is included in PJSIP distribution, and it is built by 
       default on all supported platforms. SRTP functionality is also enabled 
       by default. If you wish to disable SRTP, declare :c:macro:`PJMEDIA_HAS_SRTP`
       macro to zero. 


DirectShow Base Classes Microsoft SDK Sample
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - `​DirectShow Base Classes <http://msdn.microsoft.com/en-us/library/windows/desktop/dd375456%28v=vs.85%29.aspx>`_
   * - Author
     - Microsoft
   * - Location
     - :sourcedir:`third_party/BaseClasses/`
   * - Description
     - The DirectShow base classes are a set of C++ classes and utility functions 
       designed for implementing DirectShow filters. Several of the helper classes 
       are also useful for application developers. 
   * - License
     - Microsoft Windows SDK Licence (Licence.htm in Windows SDK installation directory)::

          Sample Code.  You may modify, copy, and distribute the source and 
          object code form of code marked as "sample."

   * - Usage
     - Used in DirectShow device driver for video capture support on Windows platform. 
       If you wish to disable it define macro :c:macro:`PJMEDIA_VIDEO_DEV_HAS_DSHOW` to 0. 
       This will disable video capture on Windows. 


libYUV
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://chromium.googlesource.com/libyuv/libyuv/
   * - Author
     - The LibYuv Project Authors
   * - Location
     - :sourcedir:`third_party/yuv/`
   * - Description
     - Video conversion utilities. 
   * - License
     - - BSD 3-clause: :source:`third_party/yuv/LICENSE`
       - Third-party: :source:`third_party/yuv/LICENSE_THIRD_PARTY`
   * - Usage
     - Libyuv may be detected and enabled by the configure script, either automatically 
       or manually via ``--with-libyuv`` option. It may be forcefully disabled by 
       defining :c:macro:`PJMEDIA_HAS_LIBYUV` to 0 in :any:`config_site.h`. 


WebRTC
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://chromium.googlesource.com/external/webrtc/+/master
   * - Location
     - :sourcedir:`third_party/webrtc/`
   * - Description
     - WebRTC Acoustic Echo Cancellation
   * - License
     - Please consult:

       - :source:`third_party/webrtc/LICENSE`
       - :source:`third_party/webrtc/LICENSE_THIRD_PARTY`

   * - Usage
     - WebRTC AEC is by default enabled, but can be disabled by passing 
       ``--disable-webrtc`` to the configure script or defining 
       :c:macro:`PJMEDIA_HAS_WEBRTC_AEC` to 0 in :any:`config_site.h`.


WebRTC AEC3
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://webrtc.googlesource.com/src
   * - Location
     - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/
   * - Description
     - WebRTC AEC3 
   * - License
     - Please consult:

       - :source:`third_party/webrtc_aec3/PJSIP_NOTES`

       Specifically, please consult WebRTC's license in:

       - :source:`third_party/webrtc_aec3/LICENSE`
        
       as well as the licenses of the third party components required in:

       - :source:`third_party/webrtc_aec3/src/absl/LICENSE` (abseil),
       - :source:`third_party/webrtc_aec3/src/third_party/rnnoise/COPYING`
         (rnnoise),
       - :source:`third_party/webrtc_aec3/src/third_party/pffft/README.txt` (pffft)

   * - Usage
     - WebRTC AEC3 can be enabled by passing ``--enable-libwebrtc-aec3`` to the 
       ``configure`` script. 



External Third Party Software
-------------------------------------------------------

The SOFTWARE may be linked with these external third party software (i.e. libraries that are
not shipped with the SOFTWARE).


bcg729
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.linphone.org/technical-corner/bcg729
   * - Location
     - - :source:`pjmedia/include/pjmedia-codec/bcg729.h`
       - :source:`pjmedia/src/pjmedia-codec/bcg729.c`
   * - Description
     - G.729 codec using backend implementation from bcg729
   * - License
     - Please consult the bcg729 website
   * - Usage
     - See :ref:`bcg729`


ffmpeg and libx264
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     -  - https://www.ffmpeg.org
        - http://www.videolan.org/developers/x264.html
   * - Location
     -  - :source:`pjmedia/src/pjmedia-codec/ffmpeg_vid_codecs.c`
        - :source:`pjmedia/src/pjmedia/ffmpeg_util.c`
        - :source:`pjmedia/src/pjmedia/converter_libswscale.c`
   * - Description
     - Ffmpeg and libx264 are used as codec backends for H.263 and H.264 and as video 
       format converter.
   * - License
     - Please consult the Ffmpeg and libx264 websites. 
   * - Usage
     - See :ref:`ffmpeg`. 


Oboe
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://github.com/google/oboe
   * - Author
     - https://github.com/google/oboe/blob/main/AUTHORS
   * - Location
     - :source:`pjmedia/src/pjmedia-audiodev/oboe_dev.cpp`
   * - Description
     - PJSIP may be configured to use Oboe capture and playback audio device on Android
   * - License
     - Apache 2.0. See https://github.com/google/oboe/blob/main/LICENSE
   * - Usage
     - See :ref:`oboe`


OpenCore AMR
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://sourceforge.net/projects/opencore-amr/
   * - Location
     - :source:`pjmedia/src/pjmedia-codec/opencore_amr.c`
   * - Description
     - OpenCore AMR NB/WB codec can be used with the SOFTWARE
   * - License
     - Apache v2 license, but it may contain derived work of other project. Please check the
       website for the details.
   * - Usage
     - See :ref:`opencore_amr`


OpenH264
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.openh264.org/
   * - Location
     - :source:`pjmedia/src/pjmedia-codec/openh264.cpp`
   * - Description
     - OpenH264 codec
   * - License
     - Please consult the OpenH264 website
   * - Usage
     - See :ref:`openh264`


OpenSSL
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.openssl.org/
   * - Location
     - :source:`pjlib/src/pj/ssl_sock_ossl.c`
   * - Description
     - OpenSSL is used as the backend implementation of PJLIB's secure socket, which among 
       other thing is used by PJSIP's SIP TLS transport object. 
   * - License
     - The OpenSSL library is licensed under 
       `Apache-style license <http://www.openssl.org/source/license.html>`__, but this is 
       deemed to be `incompatible with GPL <http://ftp-master.debian.org/REJECT-FAQ.html>`_
       (hence we give explicit permission to link with it).
   * - Usage
     - See :any:`/specific-guides/security/ssl`


Opus
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Opus is a totally open, royalty-free, highly versatile audio codec.
   * - Author
     - https://www.opus-codec.org/
   * - Location
     - :source:`pjmedia/src/pjmedia-codec/opus.c`
   * - License
     - https://www.opus-codec.org/license/
   * - Usage
     - See :ref:`opus`



Silk
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://github.com/mycelialold/spore/tree/master/jni/silk/sources
   * - Location
     - :source:`pjmedia/src/pjmedia-codec/silk.c`
   * - Description
     - Silk codec
   * - License
     - Please check the website
   * - Usage
     - See :ref:`silk`



VPX
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - libvpx: https://www.webmproject.org/code/
   * - Location
     - :source:`pjmedia/src/pjmedia-codec/vpx.c`
   * - Description
     - VP8 and VP9 video codecs
   * - License
     - BSD 3-clause: https://github.com/webmproject/libvpx/blob/main/LICENSE
   * - Usage
     - See :ref:`libvpx`

License
*******************************

Overview
=====================
In a nutshell, PJSIP is released under dual-license scheme, namely GPL and
proprietary license. PJSIP is shipped with third-party software, and may be
linked with external third-party software, most of them are open source.

If you are building open source software, probably this is everything 
you need to know and you should be all set (but IANAL).

If you are developing closed source software, however, you probably want to
know the details of the terms of the licenses below.


The SOFTWARE
=====================
PJSIP software ("**The SOFTWARE**") consists of:

.. list-table::
   :header-rows: 0

   * - `PJLIB <../api/pjlib/index.html>`_
     - A cross-platforms portability and framework library
   * - `PJLIB-UTIL <../api/pjlib-util/index.html>`_
     - An adjunct library to pjlib which provides various utility functions
   * - `PJNATH <../api/pjnath/index.html>`_
     - A NAT traversal helper library
   * - `PJMEDIA <../api/pjmedia/index.html>`_
     - A multimedia communications library
   * - `PJSIP <../api/pjsip/index.html>`_
     - A SIP protocol stack collections
   * - `PJSUA-LIB <../api/pjsua-lib]/index.html>`_
     - High level C user agent library
   * - `PJSUA2 <../api/pjsua2/index.html>`_
     - High level C++/Java/Python/SWIG user agent library

and any and all build scripts, makefiles, tools, samples, and/or applications available 
and/or required to use or modify such software.

The SOFTWARE may provide links to third party libraries or code (collectively 
"**Third Party Software**") to implement various functions, and access to Third Party Software 
may be included along with the SOFTWARE delivery as a convenience. Third Party Software 
does not comprise part of the SOFTWARE. 


License
------------------------
The SOFTWARE is released under dual license, open source (GPL) or 
an alternative license.

The SOFTWARE may be used according to Free Software GNU General Public License (GPL) version 2, 
or (at your option) any later version, with special exception to permit linking with 
some Open Source Third Party libraries set out below.

The GPL allows you to compile, modify, link, or combine The SOFTWARE with other software, 
commercial or non-commercial, as long as the resulting program complies with GPL (see 
the GPL Compliance Guide for what this means). Copy of GNU General Public License is 
available on the http://www.gnu.org. More information about GPL can be found in
`GPL FAQ <http://www.gnu.org/licenses/gpl-faq.html>`_.


Alternative license
------------------------
If you can't comply with GPL, an alternative licensing scheme may be arranged.

If you still have questions, just email icensing@pjsip.org and we'll help you sort it out.


Special Exception
------------------------
As a special exception to GPL, the author of the SOFTWARE gives permission to link 
the SOFTWARE with Open Source Third Party Software below, and distribute the linked 
combinations. GNU General Public License must be obeyed in all respects for all of the 
code used other than those Third Party Software. 


Third Party Software Licensing Requirements
------------------------------------------------
In addition to the licensing requirements of the SOFTWARE, you must make sure that your 
software meets the licensing requirements of the third party libraries below. Some third 
party libraries may require attributions to be placed in the software, significant portion 
of the software, and/or in the accompanying documentation. 


Third Party SOFTWARE
=====================
The SOFTWARE may provide links to third party libraries or code (collectively "Third Party 
Software") to iplement various functions, and access to Third Party Software may be 
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
     - pjlib/timer.[hc]
   * - Description
     - The timer heap in PJLIB was based on ACE's Timer_Heap
   * - License
     - Permissions have been obtained from the copyright holder/original author (Douglas C. 
       Schmidt) to use and redistribute this code according to the SOFTWARE licenses. You may, 
       at your option, opt to use ACE license for this particular software.
   * - Using the Software
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
     - ``pjmedia/alaw_ulaw.c``
   * - Description
     - PCM Alaw and U-law conversion
   * - License
     - ::

         This source code is a product of Sun Microsystems, Inc. and is provided
         for unrestricted use.  Users may copy or modify this source code without
         charge.
         
         SUN SOURCE CODE IS PROVIDED AS IS WITH NO WARRANTIES OF ANY KIND INCLUDING
         THE WARRANTIES OF DESIGN, MERCHANTIBILITY AND FITNESS FOR A PARTICULAR
         PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE OR TRADE PRACTICE.

         Sun source code is provided with no support and without any obligation on
         the part of Sun Microsystems, Inc. to assist in its use, correction,
         modification or enhancement.

         SUN MICROSYSTEMS, INC. SHALL HAVE NO LIABILITY WITH RESPECT TO THE
         INFRINGEMENT OF COPYRIGHTS, TRADE SECRETS OR ANY PATENTS BY THIS SOFTWARE
         OR ANY PART THEREOF.

         In no event will Sun Microsystems, Inc. be liable for any lost revenue
         or profits or other special, indirect and consequential damages, even if
         Sun has been advised of the possibility of such damages.

         Sun Microsystems, Inc.
         2550 Garcia Avenue
         Mountain View, California  94043
   * - Using the Software
     - This software is not used by default unless ``PJMEDIA_HAS_ALAW_ULAW_TABLE`` is disabled. 
       When ``PJMEDIA_HAS_ALAW_ULAW_TABLE`` is enabled (the default setting), a table based 
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
     - ``pjlib-util/crc32.c``
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

   * - Using the Software
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
     - ``pjlib-util/md5.c``
   * - Description
     - MD5 hashing for digest authentication. 
   * - License
     - This software is put in public domain, and can be used for any purpose with no warranty::

         This code implements the MD5 message-digest algorithm.
         The algorithm is due to Ron Rivest.  This code was
         written by Colin Plumb in 1993, no copyright is claimed.
         This code is in the public domain; do with it what you wish.

         Equivalent code is available from RSA Data Security, Inc.
         This code has been tested against that, and is equivalent,
         except that you don't need to include two pages of legalese
         with every copy.

         To compute the message digest of a chunk of bytes, declare an
         MD5Context structure, pass it to MD5Init, call MD5Update as
         needed on buffers full of bytes, and then call MD5Final, which
         will fill a supplied 16-byte array with the digest.

   * - Using the Software
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
     - ``pjlib-util/sha1.c``
   * - License
     - This software is put in public domain, and can be used for any purpose with no warranty::

         SHA-1 in C
         By Steve Reid 
         100% Public Domain
         -----------------
         Modified 7/98 
         By James H. Brown 
         Still 100% Public Domain
         -----------------
         Modified 4/01
         By Saul Kravitz 
         Still 100% PD
         Modified to run on Compaq Alpha hardware.  
         -----------------
         Modified 07/2002
         By Ralph Giles 
         Still 100% public domain

   * - Using the Software
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
     - ``pjmedia-codec/g722/`` directory
   * - Description
     - The G.722 codec algorithms are included in PJMEDIA source directory
   * - License
     - Public domain software
   * - Using the Software
     - This software will only be linked if application explicitly initialize the G.722 library 
       by calling ``pjmedia_codec_g722_init()``. Note that if PJSUA-LIB is used, then this call is 
       made by PJSUA-LIB, hence causing your application to be linked with the software. The 
       software can be explicitly disabled from the link process by defining 
       ``PJMEDIA_HAS_G722_CODEC`` to zero. 



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
     - ``pjlib-util/getopt.[hc``
   * - Description
     - Command line parsing library that is used by our sample applications
   * - License
     - Distributed under opensource GNU LGPL
   * - Using the Software
     - This code will only be linked if applications explicitly call ``pj_getopt()`` 
       or pj_getopt_long(). Normally application doesn't need to use this, since this 
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
     - ``third_party/resample/``
   * - Description
     - PJMEDIA uses ``resample-1.7.tar.gz`` from 
       `Digital Audio Resampling Home Page <https://ccrma.stanford.edu/~jos/resample/>`_.
   * - License
     - LGPL
   * - Using the Software
     - This resampling software is used by the conference bridge. This software is used 
       when the ``PJMEDIA_RESAMPLE_IMP`` macro is set to ``PJMEDIA_RESAMPLE_LIBRESAMPLE``, 
       which is the default. Other options for resampling backends include Speex and 
       Secret Rabbit Code (which is dual licensed). Please see ``PJMEDIA_RESAMPLE_IMP`` 
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
     - ``third_party/gsm/``
   * - Description
     - PJMEDIA includes uses GSM 06.10 version 1.0 at patchlevel 12 
   * - License
     - Free to use with no warranty::
        
         Copyright 1992, 1993, 1994 by Jutta Degener and Carsten Bormann,
         Technische Universitaet Berlin

         Any use of this software is permitted provided that this notice is not
         removed and that neither the authors nor the Technische Universitaet Berlin
         are deemed to have made any representations as to the suitability of this
         software for any purpose nor are held responsible for any defects of
         this software.  THERE IS ABSOLUTELY NO WARRANTY FOR THIS SOFTWARE.

         As a matter of courtesy, the authors request to be informed about uses
         this software has found, about bugs in this software, and about any
         improvements that may be of general interest.

         Berlin, 28.11.1994
         Jutta Degener
         Carsten Bormann        

   * - Using the Software
     - This software will only be linked if application explicitly initialize the
       GSM library by calling ``pjmedia_codec_gsm_init()``. Note that if PJSUA-LIB 
       is used, then this call is made by PJSUA-LIB, hence causing your application 
       to be linked with the software. The software can be explicitly disabled from 
       the link process by defining ``PJMEDIA_HAS_GSM_CODEC`` to zero. 


Speex
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Speex codec, accoustic echo cancellation, and sampling rate conversion.
   * - Author
     - https://speex.org/
   * - Location
     - ``third_party/speex/``
   * - Description
     - PJMEDIA uses Speex codec version 1.1.12. Speex is a high quality, Open source, 
       patent free codec implementation developed by open source community.
   * - License
     - Speex is distributed under the following free license::

        Copyright 2002-2005 
              Xiph.org Foundation
              Jean-Marc Valin
              David Rowe
              EpicGames
              Analog Devices

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions
        are met:

        - Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.

        - Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.

        - Neither the name of the Xiph.org Foundation nor the names of its
          contributors may be used to endorse or promote products derived from
          this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
        A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR
        CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
        PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
            
   * - Using the Software
     - **Speex codec**: this software will only be linked if application explicitly 
       initialize the Speex library by calling ``pjmedia_codec_speex_init()``.
       Note that if PJSUA-LIB is used, then this call is made by PJSUA-LIB, 
       hence causing your application to be linked with the software. The 
       software can be explicitly disabled from the link process by defining 
       ``PJMEDIA_HAS_SPEEX_CODEC`` to zero.

       **Speex AEC**: Speex accoustic echo cancellation is enabled by default for 
       the sound device. Application can disable this by setting 
       ``PJMEDIA_HAS_SPEEX_AEC`` to zero.

       **Speex sample rate converter**: Speex sample rate converter is only used 
       when ``PJMEDIA_HAS_SPEEX_RESAMPLE`` macro is set to non-zero. The 
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
     - ``third_party/ilbc/``
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

   * - Using the Software
     - This software will only be linked if application explicitly initialize 
       the iLBC library by calling ``pjmedia_codec_ilbc_init()``. Note that if 
       PJSUA-LIB is used, then this call is made by PJSUA-LIB, hence causing 
       your application to be linked with the software. The software can be 
       explicitly disabled from the link process by defining 
       ``PJMEDIA_HAS_ILBC_CODEC`` to zero. 


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
     - ``third_party/g7221/``
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
   * - Using the Software
     - This software is by default disabled, due to the licensing restriction above. 
       The software can be explicitly enabled by defining ``PJMEDIA_HAS_G7221_CODEC`` 
       to one.


Milenage and Rijndael
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - Milenage
   * - Author
     - The implementation was taken from 
       `3GPP TS 35.206 V7.0.0 <http://www.3gpp.org/ftp/Specs/archive/35_series/35.206/>`_ 
       document
   * - Location
     - ``third_party/milenage/``
   * - Description
     - Milenage algorithm is used for AKAv1-MD5 and AKAv2 SIP digest authentication.
   * - License
     - Please consult `3GPP TS documents <http://www.3gpp.org/specifications/60-confidentiality-algorithms>`_ ::

         The 3GPP authentication and key generation functions (MILENAGE) have been developed
         through the collaborative efforts of the 3GPP Organizational Partners.

         They may be used only for the development and operation of 3G Mobile Communications and 
         services. There are no additional requirements or authorizations necessary for these 
         algorithms to be implemented.

   * - Using the Software
     - The Milenage and Rijndael implementation will only be linked with application if 
       AKA authentication is used and application explicitly calls or makes reference to 
       ``pjsip_auth_create_aka_response()`` function. 


libSRTP
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - `libSRTP <https://github.com/cisco/libsrtp>`_
   * - Author
     - David A. McGrew, Cisco Systems, Inc. 
   * - Location
     - ``third_party/srtp/``
   * - Description
     - libSRTP implements Secure RTP/RTCP (SRTP and SRTCP).
   * - License
     - libSRTP is distributed under the following free license:: 

        /*
         *	
         * Copyright (c) 2001-2006 Cisco Systems, Inc.
         * All rights reserved.
         * 
         * Redistribution and use in source and binary forms, with or without
         * modification, are permitted provided that the following conditions
         * are met:
         * 
         *   Redistributions of source code must retain the above copyright
         *   notice, this list of conditions and the following disclaimer.
         * 
         *   Redistributions in binary form must reproduce the above
         *   copyright notice, this list of conditions and the following
         *   disclaimer in the documentation and/or other materials provided
         *   with the distribution.
         * 
         *   Neither the name of the Cisco Systems, Inc. nor the names of its
         *   contributors may be used to endorse or promote products derived
         *   from this software without specific prior written permission.
         * 
         * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
         * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
         * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
         * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
         * COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
         * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
         * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
         * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
         * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
         * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
         * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
         * OF THE POSSIBILITY OF SUCH DAMAGE.
         *
        */
        
   * - Using the Software
     - Copy of libSRTP is included in PJSIP distribution, and it is built by 
       default on all supported platforms. SRTP functionality is also enabled 
       by default. If you wish to disable SRTP, declare ``PJMEDIA_HAS_SRTP`` 
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
     - ``third_party/BaseClasses/``
   * - Description
     - The DirectShow base classes are a set of C++ classes and utility functions 
       designed for implementing DirectShow filters. Several of the helper classes 
       are also useful for application developers. 
   * - License
     - Microsoft Windows SDK Licence (Licence.htm in Windows SDK installation directory)::

          Sample Code.  You may modify, copy, and distribute the source and 
          object code form of code marked as "sample."

   * - Using the Software
     - Used in DirectShow device driver for video capture support on Windows platform. 
       If you wish to disable it define macro ``PJMEDIA_VIDEO_DEV_HAS_DSHOW`` to 0. 
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
     - ``third_party/yuv/``
   * - Description
     - Video conversion utilities. 
   * - License
     - ::

         Copyright 2011 The LibYuv Project Authors. All rights reserved.

         Redistribution and use in source and binary forms, with or without
         modification, are permitted provided that the following conditions are
         met:

         * Redistributions of source code must retain the above copyright
           notice, this list of conditions and the following disclaimer.

         * Redistributions in binary form must reproduce the above copyright
           notice, this list of conditions and the following disclaimer in
           the documentation and/or other materials provided with the
           distribution.

         * Neither the name of Google nor the names of its contributors may
           be used to endorse or promote products derived from this software
           without specific prior written permission.

         THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
         "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
         LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
         A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
         HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
         SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
         LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
         DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
         THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
         (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
         OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

   * - Using the Software
     - Libyuv may be detected and enabled by the configure script, either automatically 
       or manually via ``--with-libyuv`` option. It may be forcefully disabled by 
       defining ``PJMEDIA_HAS_LIBYUV`` to 0 in ``config_site.h``. 


WebRTC
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://chromium.googlesource.com/external/webrtc/+/master
   * - Location
     - ``third_party/webrtc/``
   * - Description
     - WebRTC Acoustic Echo Cancellation
   * - License
     - Please consult:

       - https://github.com/pjsip/pjproject/blob/master/third_party/webrtc/LICENSE
       - https://github.com/pjsip/pjproject/blob/master/third_party/webrtc/LICENSE_THIRD_PARTY

   * - Using the Software
     - WebRTC AEC is by default enabled, but can be disabled by passing 
       ``--disable-webrtc`` to the configure script or defining 
       ``PJMEDIA_HAS_WEBRTC_AEC`` to 0 in ``config_site.h``.


WebRTC AEC3
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - https://webrtc.googlesource.com/src
   * - Location
     - ``third_party/webrtc_aec3/``
   * - Description
     - WebRTC AEC3 
   * - License
     - Please consult:

       - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/PJSIP_NOTES

       Specifically, please consult WebRTC's license in:

       - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/LICENSE
        
       as well as the licenses of the third party components required in:

       - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/src/absl/LICENSE (abseil),
       - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/src/third_party/rnnoise/COPYING
         (rnnoise),
       - https://github.com/pjsip/pjproject/tree/master/third_party/webrtc_aec3/src/third_party/pffft/README.txt (pffft)

   * - Using the Software
     - WebRTC AEC3 can be enabled by passing ``--enable-libwebrtc-aec3`` to the 
       ``configure`` script. 



External Third Party Software
-------------------------------------------------------

The SOFTWARE may be linked with these external third party software (i.e. libraries that are
not shipped with the SOFTWARE).


OpenSSL
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.openssl.org/
   * - Location
     - ``pjlib/src/pj/ssl_sock_ossl.c``
   * - Description
     - OpenSSL is used as the backend implementation of PJLIB's secure socket, which among 
       other thing is used by PJSIP's SIP TLS transport object. 
   * - License
     - The OpenSSL library is licensed under 
       `Apache-style license <http://www.openssl.org/source/license.html>`_, but this is 
       deemed to be `incompatible with GPL <http://ftp-master.debian.org/REJECT-FAQ.html>`_
       (hence we give explicit permission to link with it).
   * - Using the Software
     - The library will use OpenSSL if ``PJ_HAS_SSL_SOCK`` is set to non-zero. It is 
       detected automatically with the GNU build system, and must be set manually on 
       other build systems (e.g. Windows and Symbian) 


ffmpeg and libx264
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     -  - https://www.ffmpeg.org
        - http://www.videolan.org/developers/x264.html
   * - Location
     -  - ``pjmedia/src/pjmedia-codec/ffmpeg_vid_codecs.c``
        - ``pjmedia/src/pjmedia/ffmpeg_util.c``
        - ``pjmedia/src/pjmedia/converter_libswscale.c``
   * - Description
     - Ffmpeg and libx264 are used as codec backends for H.263 and H.264 and as video 
       format converter.
   * - License
     - Please consult the Ffmpeg and libx264 websites. 
   * - Using the Software
     - Ffmpeg may be detected and enabled by the configure script, either automatically 
       or manually via ``--with-ffmpeg`` option. It may be forcefully disabled by 
       defining ``PJMEDIA_HAS_LIBAVCODEC`` to 0 in ``config_site.h``. 


OpenH264
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.openh264.org/
   * - Location
     - ``pjmedia/src/pjmedia-codec/openh264.cpp``
   * - Description
     - OpenH264 codec
   * - License
     - Please consult the OpenH264 website
   * - Using the Software
     - OpenH264 may be detected and enabled by the ``configure`` script, either 
       automatically or manually via ``--with-openh264`` option. It may be forcefully 
       disabled by defining ``PJMEDIA_HAS_OPENH264_CODEC`` to 0 in ``config_site.h``


bcg729
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - http://www.linphone.org/technical-corner/bcg729
   * - Location
     -  - ``pjmedia/include/pjmedia-codec/bcg729.h``
        - ``pjmedia/src/pjmedia-codec/bcg729.c``

   * - Description
     - G.729 codec using backend implementation from bcg729
   * - License
     - Please consult the bcg729 website
   * - Using the Software
     - bcg729 may be detected and enabled by the configure script, either automatically
       or manually via ``--with-bcg729`` option. It may be forcefully disabled by defining 
       ``PJMEDIA_HAS_BCG729`` to 0 in ``config_site.h``


Template
~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 0

   * - Software
     - 
   * - Author
     - 
   * - Location
     - 
   * - Description
     - 
   * - License
     - 
   * - Using the Software
     - 



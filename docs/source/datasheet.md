# PJSIP Datasheet

## Operating Systems Supported
 * Mac OS X
 * Windows (32 and 64bit), including Windows 10
 * Linux/uClinux
 * Smartphones:
    * iOS
    * Android
    * Windows !Mobile/Windows CE
    * Windows Phone 10/Universal Windows Platform (UWP)
    * BlackBerry (BB10)
    * Symbian S60 3rd Edition and 5th Edition
 * Community supported:
    * OpenBSD
    * FreeBSD
    * Solaris
    * MinGW
    * RTEMS

## SIP Capabilities
 * Base specs:
    * Core methods: [RFC 3261](http://tools.ietf.org/html/rfc3261): INVITE, CANCEL, BYE, REGISTER, OPTIONS, INFO
    * Digest authentication ([RFC 2617](http://tools.ietf.org/html/rfc2617))
 * Transports:
    * UDP, TCP, TLS (server or mutual)
    * DNS SRV resolution ([RFC 3263](http://tools.ietf.org/html/rfc3263))
    * IPv6
    * [ QoS](QoS) (DSCP, WMM)
 * Routing/NAT:
    * rport ([RFC 3581](http://tools.ietf.org/html/rfc3581))
    * Service-Route header ([RFC 3608](http://tools.ietf.org/html/rfc3608))
    * SIP outbound for TCP/TLS ([RFC 5626](http://tools.ietf.org/html/rfc5626))
    * Path header (with SIP outbound) ([RFC 3327](http://tools.ietf.org/html/rfc3327)) 
 * Call:
    * Offer/answer ([RFC 3264](http://tools.ietf.org/html/rfc3264))
    * hold, unhold
    * [redirection](SIP_Redirection)
    * transfer/REFER (attended and unattended):
       * Base ([RFC 3515](http://tools.ietf.org/html/rfc3515))
       * replaces ([RFC 3891](http://tools.ietf.org/html/rfc3891))
       * Referred-by ([RFC 3892](http://tools.ietf.org/html/rfc3892))
    * sipfrag support ([RFC 3420](http://tools.ietf.org/html/rfc3420))
    * norefersub ([RFC 4488](http://tools.ietf.org/html/rfc4488))
    * UPDATE ([RFC 3311](http://tools.ietf.org/html/rfc3311))
    * 100rel/PRACK ([RFC 3262](http://tools.ietf.org/html/rfc3262))
    * tel: URI ([RFC 3966](http://tools.ietf.org/html/rfc3966))
    * Session Timers ([RFC 4028](http://tools.ietf.org/html/rfc4028))
    * Reason header ([RFC 3326](http://tools.ietf.org/html/rfc3326), [partially supported](https://trac.pjsip.org/repos/wiki/FAQ#custom-header))
    * P-Header ([RFC 3325](http://tools.ietf.org/html/rfc3325), [partially supported](https://trac.pjsip.org/repos/wiki/FAQ#custom-header))
 * SDP:
    * [RFC 2327](http://tools.ietf.org/html/rfc2327) (obsoleted by [RFC 4566](http://tools.ietf.org/html/rfc4566))
    * RTCP attribute ([RFC 3605](http://tools.ietf.org/html/rfc3605))
    * IPv6 support ([RFC 3266](http://tools.ietf.org/html/rfc3266))
 * Multipart ([RFC 2046](http://tools.ietf.org/html/rfc2046), [RFC 5621](http://tools.ietf.org/html/rfc5621))
 * Presence and IM:
    * Event framework (SUBSCRIBE, NOTIFY) ([RFC 3265](http://tools.ietf.org/html/rfc3265))
    * Event publication (PUBLISH) ([RFC 3903](http://tools.ietf.org/html/rfc3903))
    * MESSAGE ([RFC 3428](http://tools.ietf.org/html/rfc3428))
    * typing indication ([RFC 3994](http://tools.ietf.org/html/rfc3994))
    * pidf+xml ([RFC 3856](http://tools.ietf.org/html/rfc3856), [RFC 3863](http://tools.ietf.org/html/rfc3863))
    * xpidf+xml
    * RPID (subset) ([RFC 4480](http://tools.ietf.org/html/rfc4480))
 * Other extensions:
    * INFO ([RFC 2976](http://tools.ietf.org/html/rfc2976))
    * AKA, AKA-v2 authentication ([RFC 3310](http://tools.ietf.org/html/rfc3310), [RFC 4169](http://tools.ietf.org/html/rfc4169))
    * ICE option tag ([RFC 5768](http://tools.ietf.org/html/rfc5768))
    * [Message summary/message waiting indication](https://trac.pjsip.org/repos/ticket/982) (MWI, [RFC 3842](http://tools.ietf.org/html/rfc3842))
 * Compliance, best current practices:
    * Issues with Non-INVITE transaction ([RFC 4320](http://tools.ietf.org/html/rfc4320))
    * Issues with INVITE transaction ([RFC 4321](http://tools.ietf.org/html/rfc4321))
    * Multiple dialog usages ([RFC 5057](http://tools.ietf.org/html/rfc5057))
    * SIP torture messages ([RFC 4475](http://tools.ietf.org/html/rfc4475), tested when applicable)
    * SIP torture for IPv6 ([RFC 5118](http://tools.ietf.org/html/rfc5118))
    * Message Body Handling ([RFC 5621](http://tools.ietf.org/html/rfc5621). Partial compliance: multipart is supported, but _Content-Disposition_ header is not handled)
    * The use of SIPS ([RFC 5630](http://tools.ietf.org/html/rfc5630). Partial compliance: SIPS is supported, but still make use of _transport=tls_ parameter)

## NAT Traversal
 * STUN:
    * [RFC 5389](http://tools.ietf.org/html/rfc5389)
    * Some [RFC 3489](http://tools.ietf.org/html/rfc3489) compatibility
    * DNS SRV resolution
    * short/long term authentication
    * fingerprinting
 * TURN:
    * [RFC 5766](http://tools.ietf.org/html/rfc5766)
    * DNS SRV resolution
    * UDP and TCP client connection
    * TCP allocations ([RFC 6062](http://tools.ietf.org/html/rfc6062))
 * ICE:
    * [RFC 5245](http://tools.ietf.org/html/rfc5245)
    * host, srflx, and relayed candidates
    * aggressive and regular nomination
    * ICE option tag ([RFC 5768](http://tools.ietf.org/html/rfc5768))
 * NAT type detection:
    * legacy [RFC 3489](http://tools.ietf.org/html/rfc3489)
 * Other:
    * [ QoS](QoS) support on sockets (DSCP, WMM)



## Media/audio capabilities
 * Core:
    * any clockrates
    * N-channels support
    * zero thread
 * Base:
    * DTMF ([RFC 4733](http://tools.ietf.org/html/rfc4733)/[RFC 2833](http://tools.ietf.org/html/rfc2833))
    * echo cancellation (WebRTC, Speex, suppressor, or native)
        * Third party acoustic echo cancellation (AEC)
            * [Echo cancellation software from voice INTER connect](http://www.voiceinterconnect.de/echo-cancellation.html)
            * [CANEC from DSP Algorithms](http://www.dspalgorithms.com/products/canec.html)
            * [VQE from Wave Arts](http://wavearts.com/licensing/#vqe)
            * [bdIMAD from bdSound](http://www.bdsound.com/products/bdimad-for-pjsip.html)
            * [TrueVoice from Limes Audio](http://www.limesaudio.com/truevoice-acoustic-echo-cancellation-software/)
            * [Echo cancellation software from SoliCall](http://solicall.com/products.html)
    * inband DTMF/tone generation
    * WAV file playback and recording
    * WAV file playlist
    * memory based playback and capture
    * adaptive jitter buffer
    * packet lost concealment
    * clock drift recovery
 * Audio conferencing (in client)
 * Flexible media flow management
 * Audio Codecs:
    * Bundled:
       * Speex 8KHz, 16Khz, 32KHz
       * iLBC, GSM,
       * L16, G.711A/U (PCMA/PCMU), 
       * G.722,
       * G.722.1 16KHz/32KHz (Siren7/Siren14, [licensed from Polycom](http://www.polycom.com/company/about_us/technology/siren14_g7221c/license_agreement.html))
    * with third party libraries (may need additional licensing, please check each codec provider):
       * [Opus](https://www.opus-codec.org) codec (see ticket #1904)
       * [Intel IPP](Intel_IPP_Codecs):
          * AMR-NB, AMR-WB, 
          * G.722, G.722.1,
          * G.723.1, G.726, G.728, G.729A,
       * [SILK](https://developer.skype.com/silk) codec (see ticket #1586)
       * [OpenCore AMR](http://sourceforge.net/projects/opencore-amr/):
          * AMR-NB (see ticket #1388)
          * AMR-WB (see ticket #1608)
       * [bcg729](http://www.linphone.org/technical-corner/bcg729/): G.729 (see ticket #2029)
    * Hardware codecs:
       * on Nokia with [APS/VAS-Direct](Nokia_APS_VAS_Direct): AMR-NB, G.729, iLBC, PCMA, PCMU
       * on iPhone: iLBC
 * Transports:
    * RTP and RTCP with media statistic ([RFC 3550](http://tools.ietf.org/html/rfc3550), [RFC 3551](http://tools.ietf.org/html/rfc3551))
    * RTCP XR (subset, [RFC 3611](http://tools.ietf.org/html/rfc3611))
    * UDP, STUN, ICE
    * IPv6 (UDP only)
    * SRTP ([RFC 3711](http://tools.ietf.org/html/rfc3711)), SRTP SDES ([RFC 4568](http://tools.ietf.org/html/rfc4568)), and DTLS-SRTP ([RFC 5763](http://tools.ietf.org/html/rfc5763))
    * [ QoS](QoS) (DSCP, WMM)
    * Symmetric RTP/RTCP ([RFC 4961](http://tools.ietf.org/html/rfc4961))
    * Multiplexing RTP and RTCP (rtcp-mux) ([RFC 5671](http://tools.ietf.org/html/rfc5671)) (see ticket #2087)
    * Third Party
        * ZRTP
            * [Zorg](http://www.zrtp.org/)
            * [ZRTP4PJ](https://github.com/wernerd/ZRTP4PJ)
 * [Audio devices](Audio_Dev_API):
    * native WMME (Windows, Windows Mobile)
    * native ALSA (Linux)
    * native CoreAudio (Mac OS X, iPhone) with support for native/hardware EC
    * OpenSL (Android)
    * native Symbian MMF (!Symbian/Nokia S60)
    * native [APS](APS) (Nokia S60) with hardware EC, and [APS-Direct](Nokia_APS_VAS_Direct) to support hardware codecs
    * native [VAS](VAS) (Nokia S60) with hardware EC, and [VAS-Direct](Nokia_APS_VAS_Direct) to support hardware codecs
    * PortAudio (WMME, DirectSound, OSS, ALSA, CoreAudio, etc.)

## Video Media
 * Platforms: 
   - Windows, 
   - Linux, 
   - Mac
   - iOS
   - Android
 * Codecs: 
   - H.263-1998 (ffmpeg)
   - H.264 ([OpenH264](http://www.openh264.org), VideoToolbox (iOS and Mac), ffmpeg+x264)
   - VP8 (libvpx)
   - VP9 (libvpx)
 * Capture devices: 
   - colorbar (all platforms)
   - DirectShow (Windows)
   - Video4Linux2 (Linux)
   - QuickTime (Mac OS X)
   - AVFoundation (iOS)
 * Rendering devices: 
   - SDL (Windows, Linux, and Mac OS X)
   - OpenGL ES or UIView (iOS)
 * Video conferencing (in client)
 * Flexible media flow management

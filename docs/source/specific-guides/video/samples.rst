.. _vid_ug_samples:

Sample Applications with Video
===============================

The pages in this Video section are deep-dives on individual topics
(codec tuning, conference bridge, A/V sync, orientation, keyframes,
best practices, components). For an end-to-end walkthrough on adding
video to a PJSUA2 application, start at
:any:`/pjsua2/using/media_video`.

PJPROJECT ships several sample applications that exercise the video
feature. They are the recommended starting points for learning the API
and for verifying that a video build works end-to-end.

- **Desktop (Windows, macOS, Linux)** — :sourcedir:`pjsip-apps/src/pjsua` is
  the cross-platform PJSUA-LIB (C) console app. It is the most
  thoroughly exercised sample and effectively serves as the reference
  full-featured SIP video client: interactive command-line UI, video
  calls and preview, codec selection and parameter tuning, video
  conference, AVI playback, key-frame request, etc. Use this when you
  need to verify that a video build works or when you want a feature to
  copy from.

- **iOS, PJSUA-LIB (C / Objective-C)** — :sourcedir:`pjsip-apps/src/pjsua/ios`
  contains *ipjsua*, the maintained iOS reference. It is a usable SIP
  video client built directly on the C API, and the most complete iOS
  sample. See :doc:`/get-started/ios/build_instructions` for build
  steps.

- **iOS, PJSUA-LIB with Swift** — :sourcedir:`pjsip-apps/src/pjsua/ios-swift`
  contains *ipjsua-swift*, a smaller demo that shows how to call the
  PJSUA-LIB C API from Swift via a bridging header. Useful as a starting
  template; not as feature-complete as *ipjsua*.

- **iOS, PJSUA2 with Swift (C++)** — :sourcedir:`pjsip-apps/src/pjsua2/ios-swift-pjsua2`
  is a proof-of-concept showing how to consume PJSUA2 (C++) from Swift
  via an Objective-C++ bridge. Scope is narrow — it demonstrates the
  binding pattern rather than acting as a full client.

- **Android, PJSUA2 (Java)** — :sourcedir:`pjsip-apps/src/swig/java/android/app`
  is a working Android sample that supports TLS, AMR-NB/WB audio, and
  H.264 video over PJSUA2. It also demonstrates handling device
  orientation changes and preserving the video aspect ratio in the
  renderer view. The UI is intentionally minimal so the PJSUA2 usage
  stands out. See :doc:`/get-started/android/java-sip-client`.

- **Android, PJSUA2 (Kotlin)** — :sourcedir:`pjsip-apps/src/swig/java/android/app-kotlin`
  is a Kotlin port of the Java sample, with most settings hard-coded.
  It is primarily a proof-of-concept for using PJSUA2 from Kotlin
  rather than a feature showcase. See
  :doc:`/get-started/android/kotlin-sip-client`.

.. note::

   A Qt-based desktop GUI sample, *vidgui*, also exists at
   :sourcedir:`pjsip-apps/src/vidgui`. It is provided as an example of
   embedding video into a GUI toolkit but is rarely tested and may not
   build or run on current toolchains. Prefer one of the samples above.

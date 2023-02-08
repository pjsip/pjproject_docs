Switchboard
==========================================================
Audio switchboard is drop-in (compile-time) replacement for the 
:doc:`Conference Bridge </api/generated/pjmedia/group/group__PJMEDIA__CONF>`.
The main benefits of using the switchboard are its ability to handle encoded
audio frames, its low latency, and higher performance. 
Its main drawback is it doesn't do conferencing.

The switchboard is implemented in :source:`pjmedia/src/pjmedia/conf_switch.c`, and can be 
activated by declaring :c:macro:`PJMEDIA_CONF_USE_SWITCH_BOARD` to non-zero in
:any:`config_site.h`.

The main features of the switchboard are:

- it has the same API as the conference bridge, except that one port
  can only receive from once source port

  .. tip::

    The :cpp:any:`pjmedia_conf_connect_port()` will
    disconnect previous source if it is called again for the same sink port while
    that sink port is currently listening to a source port

- It supports encoded audio frames

  .. tip::

     For example when the audio frames from/to the audio device are already in encoded form.

- One source may transmit to more than one destinations. 

  .. tip::

     This is useful for example to implement call recording feature in the application.

- Supports routing audio from ports with different *ptime* settings.
- Optimized for low latency

  .. tip::
  
     It has zero latency unless the *ptimes*  are different between *ports*.

- Lightweight, both in footprint and performance.

Some conference bridge features are not available:

 - audio mixing feature (i.e. no conferencing feature),
 - audio level adjustment and query are not available when the port is using 
   non-PCM format,
 - audio resampling,
 - passive ports.

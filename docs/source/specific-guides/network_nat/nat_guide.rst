Getting around NAT (for media)
==================================

.. contents:: Table of Contents
    :depth: 2


Problems with NAT will cause no packets are getting received, either by
local or remote party. Below are general guide to get around the NAT problem.


Use STUN and/or TURN and/or ICE
-------------------------------

One of the obvious reason why no incoming packet is received is because
the application sends private IP address as its RTP address. This can be
verified by looking at the SDP ``c=`` line that is sent by the
application.

If the SDP ``c=`` line contains private address, then probably you need
to use STUN or TURN. You can enable STUN support in *pjsua* by using
``--stun-srv`` option from the command line. For example:

.. code-block:: shell

    $ ./pjsua --stun-srv stun.pjsip.org

Another example to use TURN and ICE:

.. code-block:: shell

    $ ./pjsua --use-ice --use-turn --turn-srv turn.pjsip.org --turn-user [username] --turn-passwd ***

Disabling VAD
-------------

Normally NAT router only forwards incoming packets to internal network
after the internal host has sent some packets to remote destination. But
this may not happen if Voice Activity Detector (VAD)/Silence Detector is
enabled, because then no RTP packet will be transmitted when there is no
voice activity on the microphone.

So as workaround solution, try to disable VAD to see if this is the
case. You can disable VAD in *pjsua* by using ``--no-vad`` option
from the command line.

Using Port Forwarding
---------------------

*pjsua* can also be configured in port forwarding environment, for both
SIP UDP/TCP and media (RTP) transports. To do this, you have to
configure your router to forward UDP/TCP port 5060 to the application,
and also UDP ports for RTP. By default, *pjsua* (and *PJSUA-API*)
allocates UDP ports for RTP/RTCP from port 4000 for RTP and 4001 for
RTCP, and upwards up to the maximum number of calls configured in pjsua
(for example, if *max-calls* is 10, then the port range allocated for
RTP/RTCP will be UDP ports 4000 - 4019, since each call will need two
UDP sockets).

.. note::

   The default port 5060 for SIP can be changed with ``--local-port``
   option, while the default RTP start port of 4000 can be changed with
   ``--rtp-port`` option.

After port forwarding has been configured in the router, you just need
to specify the router’s public IP address to pjsua, with
``--ip-addr`` command line option. With this option, all addresses
advertised by *pjsua* will use this address rather than the internal IP
address.

Still having NAT problem?
--------------------------
Also check :any:`/specific-guides/network_nat/nat_blocked` for potential solutions.

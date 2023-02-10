Troubleshooting ICE negotiation failure
=======================================

.. contents:: Table of Contents
    :depth: 3


ICE negotiation may fail because of several reasons, which will be
explained below. With pjsua application, ICE negotiation failure will
cause pjsua to disconnect the call with call disconnection reason set to
500 “ICE negotiation failed”.


How ICE works
-------------

The basic principle of ICE is actually very simple: 

- each party gathers
  candidate addresses to be used to receive media, and encode and send
  them in the SDP. Below is a sample SDP containing ICE candidates:

  ::

   v=0
   o=- 3400859894 3400859894 IN IP4 1.1.1.1
   s=pjmedia
   c=IN IP4 1.1.1.1
   t=0 0
   a=X-nat:6 Symmetric
   a=ice-ufrag:349219da
   a=ice-pwd:50644d54
   m=audio 16902 RTP/AVP 103 101
   a=rtpmap:103 speex/16000
   a=rtpmap:101 telephone-event/8000
   a=fmtp:101 0-15
   a=candidate:Hc0a80265 1 UDP 1694498815 192.168.2.101 16052 typ host
   a=candidate:Sc0a80266 1 UDP 2130706431 1.1.1.1 16902 typ srflx raddr 192.168.2.101 rport 16052

-  In the SDP above, there is only one media line (the ``m=`` line) and
   one ICE *component* in the media line, that is the RTP component,
   indicated by component id 1 (the number before the keyword “UDP” in
   the *candidate* lines). The second component, the RTCP component, is
   omited in this article for brevity.
-  The RTP component above in turn has two *candidates*: one host
   candidate which corresponds to local interface IP address
   192.168.2.101, and another is server reflexive candidate (the one
   with *srflx* keyword) which was acquired by querying STUN server.
-  When media is started and each party has got the SDP of the remote
   party, they will start procedures called *ICE connectivity checks*,
   or *ICE negotiation*. The *ICE connectivity check* is done by
   *pairing* each candidate in local SDP with the candidates found in
   remote SDP, and perform connectivity check for each pair by sending
   STUN *Binding request* to the remote address in the pair. When this
   STUN *Binding Request* yields a successful response, then the party
   knows that this pair of local and remote candidates may be used for
   the media transmission. The remote party will do the same *pairing*
   and *connectivity checks* process too.
-  There are two possible outcomes for this process: successful, and
   failure. ICE negotiation/connectivity check is successful if for each
   component in each media line, at least one pair can be used for media
   transmission. This means that a successful STUN *Binding response*
   has been received for the pair. If any of the component has not
   received successful STUN *Binding response*, ICE negotiation is
   considered failed.

Sample session
--------------

ICE process can be traced in the log by turning up log verbosity to 5.
The ICE events can be seen by looking at ``icstr`` letters in the log
sender column. Below are sample of ICE logging.

Failed scenario
~~~~~~~~~~~~~~~

::

    16:16:46.672  icstr015DB3D0 ICE session created, comp_cnt=1, role is Controlled agent
    16:16:46.672  icstr015DB3D0 Candidate 0 added: comp_id=1, type=Host, foundation=Hc0a80102, addr=192.168.1.2:14210, base=192.168.1.2:14210, prio=0x64ffffff (1694498815)
    16:16:46.672  icstr015DB3D0 Candidate 1 added: comp_id=1, type=Server Reflexive, foundation=Sc0a80102, addr=76.102.231.35:14210, base=192.168.1.2:14210, prio=0x7effffff (2130706431)
    16:16:46.679  icstr015DB3D0 Check 1: [1] 192.168.1.2:14210-->71.166.160.226:16902 pruned (duplicate found)
    16:16:46.679  icstr015DB3D0 Check 2: [1] 192.168.1.2:14210-->192.168.2.101:16052 pruned (duplicate found)
    16:16:46.679  icstr015DB3D0 Checklist created:
    16:16:46.679  icstr015DB3D0  0: [1] 192.168.1.2:14210-->71.166.160.226:16902 (not nominated, state=Frozen)
    16:16:46.679  icstr015DB3D0  1: [1] 192.168.1.2:14210-->192.168.2.101:16052 (not nominated, state=Frozen)
    16:16:46.679  icstr015DB3D0 Starting ICE check..
    16:16:46.679  icstr015DB3D0 Check 0: [1] 192.168.1.2:14210-->71.166.160.226:16902: state changed from Frozen to Waiting
    16:16:46.679  icstr015DB3D0 Checklist: state changed from Idle to Running
    16:16:46.679  icstr015DB3D0 Starting checklist periodic check
    16:16:46.679  icstr015DB3D0 Sending connectivity check for check 0: [1] 192.168.1.2:14210-->71.166.160.226:16902
    16:16:46.680  icstr015DB3D0 Check 0: [1] 192.168.1.2:14210-->71.166.160.226:16902: state changed from Waiting to In Progress
    16:16:46.701  icstr015DB3D0 Starting checklist periodic check
    16:16:46.701  icstr015DB3D0 Sending connectivity check for check 1: [1] 192.168.1.2:14210-->192.168.2.101:16052
    16:16:46.701  icstr015DB3D0 Check 1: [1] 192.168.1.2:14210-->192.168.2.101:16052: state changed from Frozen to In Progress
    16:16:46.722  icstr015DB3D0 Starting checklist periodic check
    16:16:54.634  icstr015DB3D0 Check 0: [1] 192.168.1.2:14210-->71.166.160.226:16902 (not nominated): connectivity check FAILED: STUN transaction has timed out (PJNATH_ESTUNTIMEDOUT)
    16:16:54.634  icstr015DB3D0 Check 0: [1] 192.168.1.2:14210-->71.166.160.226:16902: state changed from In Progress to Failed
    16:16:54.634  icstr015DB3D0 Check 1: [1] 192.168.1.2:14210-->192.168.2.101:16052 (not nominated): connectivity check FAILED: STUN transaction has timed out (PJNATH_ESTUNTIMEDOUT)
    16:16:54.634  icstr015DB3D0 Check 1: [1] 192.168.1.2:14210-->192.168.2.101:16052: state changed from In Progress to Failed
    16:16:54.634  icstr015DB3D0 ICE process complete, status=All ICE checklists failed (PJNATH_EICEFAILED)
    16:16:54.634  icstr015DB3D0 Valid list
    16:16:54.634  icstr015DB3D0 ICE negotiation failed after 7:955s: All ICE checklists failed (PJNATH_EICEFAILED)

Successful scenario
~~~~~~~~~~~~~~~~~~~

::

    16:01:46.168  icstr00DCB6D8 ICE session created, comp_cnt=2, role is Controlling agent
    16:01:46.168  icstr00DCB6D8 Candidate 0 added: comp_id=1, type=Host, foundation=Hc0a80001, addr=192.168.0.1:4000, base=192.168.0.1:4000, prio=0x64ffffff (1694498815)
    16:01:46.168  icstr00DCB6D8 Candidate 1 added: comp_id=1, type=Host, foundation=Hc0a80001, addr=192.168.131.1:4000, base=192.168.0.1:4000, prio=0x640000ff (1677721855)
    16:01:46.168  icstr00DCB6D8 Candidate 2 added: comp_id=1, type=Host, foundation=Hc0a80001, addr=172.26.2.79:4000, base=192.168.0.1:4000, prio=0x640000ff (1677721855)
    16:01:46.168  icstr00DCB6D8 Candidate 3 added: comp_id=1, type=Server Reflexive, foundation=Sc0a80001, addr=202.152.240.222:42972, base=192.168.0.1:4000, prio=0x7effffff (2130706431)
    16:01:46.168  icstr00DCB6D8 Candidate 4 added: comp_id=2, type=Host, foundation=Hc0a80001, addr=192.168.0.1:4001, base=192.168.0.1:4001, prio=0x64fffffe (1694498814)
    16:01:46.168  icstr00DCB6D8 Candidate 5 added: comp_id=2, type=Host, foundation=Hc0a80001, addr=192.168.131.1:4001, base=192.168.0.1:4001, prio=0x640000fe (1677721854)
    16:01:46.168  icstr00DCB6D8 Candidate 6 added: comp_id=2, type=Host, foundation=Hc0a80001, addr=172.26.2.79:4001, base=192.168.0.1:4001, prio=0x640000fe (1677721854)
    16:01:46.168  icstr00DCB6D8 Candidate 7 added: comp_id=2, type=Server Reflexive, foundation=Sc0a80001, addr=202.152.240.222:42973, base=192.168.0.1:4001, prio=0x7efffffe (2130706430)
    16:01:49.884  icstr00DCB6D8 Check 2: [1] 192.168.0.1:4000-->192.168.0.2:4000 pruned (duplicate found)
    16:01:49.884  icstr00DCB6D8 Check 3: [1] 172.26.2.79:4000-->192.168.0.2:4000 pruned (equal base)
    16:01:49.884  icstr00DCB6D8 Check 3: [1] 192.168.131.1:4000-->192.168.0.2:4000 pruned (equal base)
    16:01:49.884  icstr00DCB6D8 Check 2: [2] 192.168.0.1:4001-->192.168.0.2:4001 pruned (duplicate found)
    16:01:49.884  icstr00DCB6D8 Check 2: [2] 172.26.2.79:4001-->192.168.0.2:4001 pruned (equal base)
    16:01:49.884  icstr00DCB6D8 Check 2: [2] 192.168.131.1:4001-->192.168.0.2:4001 pruned (equal base)
    16:01:49.884  icstr00DCB6D8 Checklist created:
    16:01:49.884  icstr00DCB6D8  0: [1] 192.168.0.1:4000-->192.168.0.2:4000 (not nominated, state=Frozen)
    16:01:49.894  icstr00DCB6D8  1: [2] 192.168.0.1:4001-->192.168.0.2:4001 (not nominated, state=Frozen)
    16:01:49.894  icstr00DCB6D8 Starting ICE check..
    16:01:49.894  icstr00DCB6D8 Check 0: [1] 192.168.0.1:4000-->192.168.0.2:4000: state changed from Frozen to Waiting
    16:01:49.904  icstr00DCB6D8 Checklist: state changed from Idle to Running
    16:01:49.904  icstr00DCB6D8 Starting checklist periodic check
    16:01:49.904  icstr00DCB6D8 Sending connectivity check for check 0: [1] 192.168.0.1:4000-->192.168.0.2:4000
    16:01:49.904  icstr00DCB6D8 Check 0: [1] 192.168.0.1:4000-->192.168.0.2:4000: state changed from Waiting to In Progress
    16:01:49.924  icstr00DCB6D8 Starting checklist periodic check
    16:01:49.924  icstr00DCB6D8 Sending connectivity check for check 1: [2] 192.168.0.1:4001-->192.168.0.2:4001
    16:01:49.924  icstr00DCB6D8 Check 1: [2] 192.168.0.1:4001-->192.168.0.2:4001: state changed from Frozen to In Progress
    16:01:49.924  icstr00DCB6D8 Check 0: [1] 192.168.0.1:4000-->192.168.0.2:4000 (nominated): connectivity check SUCCESS
    16:01:49.924  icstr00DCB6D8 Check 0: [1] 192.168.0.1:4000-->192.168.0.2:4000: state changed from In Progress to Succeeded
    16:01:49.924  icstr00DCB6D8 Check 0 is successful and nominated
    16:01:49.934  icstr00DCB6D8 Triggered check for check 0 not performed because it's completed
    16:01:49.934  icstr00DCB6D8 Check 0 is successful and nominated
    16:01:49.944  icstr00DCB6D8 Starting checklist periodic check
    16:01:49.954  icstr00DCB6D8 Triggered check for check 1 not performed because it's in progress. Retransmitting
    16:01:49.954  icstr00DCB6D8 Check 1: [2] 192.168.0.1:4001-->192.168.0.2:4001 (nominated): connectivity check SUCCESS
    16:01:49.964  icstr00DCB6D8 Check 1: [2] 192.168.0.1:4001-->192.168.0.2:4001: state changed from In Progress to Succeeded
    16:01:49.964  icstr00DCB6D8 Check 1 is successful and nominated
    16:01:49.964  icstr00DCB6D8 ICE process complete, status=Success
    16:01:49.964  icstr00DCB6D8 Valid list
    16:01:49.964  icstr00DCB6D8  0: [1] 192.168.0.1:4000-->192.168.0.2:4000 (nominated, state=Succeeded)
    16:01:49.964  icstr00DCB6D8  1: [2] 192.168.0.1:4001-->192.168.0.2:4001 (nominated, state=Succeeded)
    16:01:49.974  icstr00DCB6D8 ICE negotiation completed in 0.090s. Sending from 192.168.0.1:4000 to 192.168.0.2:4000

ICE negotiation failures
------------------------

ICE negotiation failure is normally caused by no successful STUN
*Binding response* is received by the client for any of the candidate
pairs. This could be caused by one of the following.

Incompatile firewall/NAT
~~~~~~~~~~~~~~~~~~~~~~~~

This is the most common cause of negotiation failure. If one endpoint is
behind a symmetric NAT (address and port dependent mapping) and the
other is behind another symmetric NAT or an open cone NAT but with
address and port dependent filtering capability, then the STUN *Binding
request* will not reach the destination, and the connectivity check will
fail with time out error :c:macro:`PJNATH_ESTUNTIMEDOUT`.

To assist troubleshooting this type of problem, pjsip (pjsua-lib) adds
the NAT type information in the SDP content, for example:

::

   a=X-nat:6 Symmetric

The possible types as classified by pjnath are:

::

     Type    Name
    -----------------------
      0    Unknown
      1    ErrUnknown
      2    Open
      3    Blocked
      4    Symmetric UDP
      5    Full Cone
      6    Symmetric
      7    Restricted
      8    Port Restricted

By examining the NAT types in both local and remote SDPs, one should
have a rough idea on the behavior of the NAT in front of each endpoints.
However please be warned that NAT type classification should not be
considered as a definite type, since some NAT routers are known to
change its type based on traffic type and other parameters. This
information is provided as additional information only.

Unreachable IP address
~~~~~~~~~~~~~~~~~~~~~~

It is also possible that the candidates specified in SDP are all
unreachable directly from the other endpoint, for example if the
candidates all specify private IP addresses. To troubleshoot this
problem, check the *candidate* lines in the SDP.

Incompatible STUN version
~~~~~~~~~~~~~~~~~~~~~~~~~

In rare cases, it may be possible that the STUN version used by the two
endpoints are not compatible with one another, for example when either
party implements different STUN draft version which happen to be
incompatible with the version that the other implements. This could
result in various errors, for example the STUN *Binding
request/response* will not be able to authenticate.

Other causes
~~~~~~~~~~~~

The list above are definitely not exhaustive, as there may be other
causes of ICE negotiation failures.

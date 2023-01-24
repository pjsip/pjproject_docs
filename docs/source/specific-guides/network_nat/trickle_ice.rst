Using Trickle ICE
====================

Brief info about Trickle ICE
--------------------------------

Trickle ICE is a supplementary mode of ICE operation in which candidates can be exchanged incrementally as soon as they become available (and simultaneously with the gathering of other candidates).  Connectivity checks can also start as soon as candidate pairs have been created.  Because Trickle ICE enables candidate gathering and connectivity checks to be done in parallel, the method can considerably accelerate the process of establishing a communication session.

Two operation modes of trickle ICE:

 #. Full trickle, the typical mode of operation for Trickle ICE agents, an agent is supposed to enable this mode only when it knows that remote supports trickle ICE. Determining support of trickle ICE can be done by following the recommendations described https://tools.ietf.org/html/rfc8838#section-3 and specifically for SIP https://tools.ietf.org/html/rfc8840#section-5.

 #. Half trickle, mode of operation in which the initiator gathers a full generation of candidates strictly before creating and conveying the initial ICE description. Once conveyed, this candidate information can be processed by regular ICE agents, which do not require support for Trickle ICE. It also allows Trickle ICE capable responders to still gather candidates and perform connectivity checks in a non-blocking way, thus providing roughly "half" the advantages of Trickle ICE. The half trickle mechanism is mostly meant for use when the responder's support for Trickle ICE cannot be confirmed prior to conveying the initial ICE description.


How to enable
--------------------------------
For app using PJSUA
~~~~~~~~~~~~~~~~~~~~~~~~
 #. Enable and configure ICE as usual.
 #. Configure trickle ICE, it can be configured globally (for all SIP accounts) or per account basis:

    - global setting: set :cpp:any:`pjsua_media_config::ice_opt::trickle` to :cpp:any:`PJ_ICE_SESS_TRICKLE_HALF` or :cpp:any:`PJ_ICE_SESS_TRICKLE_FULL`.
    - account setting:

      - set :cpp:any:`pjsua_acc_config::ice_cfg_use` to :cpp:any:`PJSUA_ICE_CONFIG_USE_CUSTOM`
      - set :cpp:any:`pjsua_acc_config::ice_cfg::ice_opt::trickle` to :cpp:any:`PJ_ICE_SESS_TRICKLE_HALF` or :cpp:any:`PJ_ICE_SESS_TRICKLE_FULL`.

For app using PJSUA2
~~~~~~~~~~~~~~~~~~~~~~~~
 #. Enable and configure ICE as usual.
 #. Configure trickle ICE, it can only be configured per account basis:

    - set :cpp:any:`pj::AccountConfig::natConfig::iceTrickle` to :cpp:any:`PJ_ICE_SESS_TRICKLE_HALF` or :cpp:any:`PJ_ICE_SESS_TRICKLE_FULL`.

For pjsua app
~~~~~~~~~~~~~~~~~~~~~~~~
 #. Enable and configure ICE as usual, e.g: ``--use-ice``, STUN & TURN settings.
 #. Add pjsua param ``--ice-trickle=N``, note: N=0:disabled, 1:half, 2:full.

References
-----------------
 - Trickle ICE: https://tools.ietf.org/html/rfc8838
 - SIP usage for Trickle ICE: https://tools.ietf.org/html/rfc8840
 
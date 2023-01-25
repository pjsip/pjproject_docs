Group Lock
==========

.. contents:: Table of Contents
    :depth: 2

Group Lock (:cpp:any:`pj_grp_lock_t`) is a synchronization object in PJLIB
for deadlock avoidance and session management. It is implemented by
ticket :issue:`1616` for PJSIP version 2.1.

Introduction
------------

Group lock is a synchronization object to manage concurrency among
members within the same logical group. Example of such groups are:

- dialog, which has members such as the dialog itself, an invite session, and several transactions
- ICE, which has members such as ICE stream transport, ICE session, STUN socket, TURN socket, and down to ioqueue key

Group lock has three functions:

- mutual exclusion: to protect resources from being accessed by more than one threads at the same time
- session management: to make sure that the resource is not destroyed while others are still using or about to use it.
- lock coordinator: to provide uniform lock ordering among more than one lock objects to avoid deadlock.

The requirements of the group lock are:

- must satisfy all the functions above
- must allow members to join or leave the group (for example, transaction may be added or removed from a dialog)
- must be able to synchronize with external lock (for example, a dialog lock must be able to sync itself with PJSUA lock)


Usage
--------

Creation
~~~~~~~~

Create the group lock by calling :cpp:any:`pj_grp_lock_create`, specifying
:cpp:any:`pj_grp_lock_config` as one of the parameters. A :cpp:any:`pj_grp_lock_t`
object will be returned.

The group lock can be created either by the first member in the group or
by the higher object that manages the members. Once created, the
ownership of the group lock will be shared by the members, using a
reference counter. The group lock will have its own pool. Also a group
lock is a :cpp:any:`pj_lock_t` object, hence lock API can be used.


Lock and Unlock
~~~~~~~~~~~~~~~

The group lock is a lock that can be used as mutex. You can use lock APIs:

- :cpp:any:`pj_lock_acquire()`, 
- :cpp:any:`pj_lock_tryacquire()`, and
- :cpp:any:`pj_lock_release()`, 

or the group lock's own API:

- :cpp:any:`pj_grp_lock_acquire()`, 
- :cpp:any:`pj_grp_lock_tryacquire()`, and
- :cpp:any:`pj_grp_lock_release()`. 

Locking the group lock temporarily increases
the reference counter to prevent it from being destroyed. The side
effect is, the :cpp:any:`pj_grp_lock_release()` may cause the group to be
destroyed, if it is the last one that holds the reference counter. In
that case, it returns :cpp:any:`PJ_EGONE`.

Destroy
~~~~~~~

The group lock lifetime is governed by an internal reference counter
(see [#session Session Management] below). It will be destroyed once the
reference counter reaches zero.

Since group lock is a lock object, it can be destroyed with
:cpp:any:`pj_lock_destroy()` API. This will forcefully destroy the group lock
without adhering to the reference counter, thus should be avoided.

Registering Member to The Group Lock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The purpose of registering a member to the group lock is to prevent that
member from being destroyed prematurely, when other threads are
referencing the member. To achieve that, the member registers a callback
to be called by the group lock to destroy itself when the reference
counter of the group reaches zero. In other words, once registered, a
member must not allow itself to be destroyed unless the request comes
from the group lock's destroy callback.

To register a member, use :cpp:any:`pj_grp_lock_add_handler()`.

Sometimes a member needs to die early (for example, transactions may
come and go in a dialog). A member may unregister the handler using 
:cpp:any:`pj_grp_lock_del_handler()`.


Session Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This API manages the reference counter of the group:

- :cpp:any:`pj_grp_lock_add_ref()`
- :cpp:any:`pj_grp_lock_dec_ref()`

The :cpp:any:`pj_grp_lock_dec_ref()` returns :cpp:any:`PJ_EGONE` when that operation
causes the group lock to be destroyed (because the reference counter
reaches zero).

Synchronization with External Locks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often it is necessary to synchronize the group lock with an external
lock. By external, it means a lock owned by object outside the group,
and it's not possible to to add that object to the group. The PJSUA lock
is an example of such locks. It is not possible for PJSUA to use the
group lock of ICE, for example, simply because there can be many of
them. And ICE sessions come and goe (hence their group locks will be
destroyed), while PJSUA lock needs to live forever. An alternative
approach exists, i.e. for PJSUA to instantiate a group lock and make ICE
(and other objects that potentially can use group lock) use this group
lock as their lock. But by using this approach, effectively we are
making the whole library single threaded, which is not efficient.

The synchronization feature solves this problem by "chaining” the
external lock to the group lock. Once lock A is *chained* to the group
lock, then every time the group lock is acquired, lock A will be
acquired too, and always in the same order, hence preventing the
deadlock. And better yet, the code that uses lock A does not need to be
aware about the group lock. It can continue to use only lock A, and
still the lock ordering is obeyed.

Consider the following example with PJSUA lock. (Note: this example is
currently only hypothetical since it's not yet implemented)

1. The PJSUA-LIB library continues to use an internal lock object for
   it's synchronization.
2. ICE object creates group lock, and chain PJSUA-LIB's lock to its
   group lock at the first position (hence PJSUA-LIB's lock will be
   locked first when group lock is acquired).
3. An operation is performed in PJSUA-LIB, and PJSUA-LIB acquires PJSUA
   lock. This is done using existing lock API since PJSUA-LIB is not
   made aware about group lock. At some point during this operation, ICE
   operation is performed and ultimately the ICE group lock is acquired.
   All of these operations will cause locks to be acquired with the
   order that is depicted below:

   .. code-block::

      pjsua --> { pjsua --> ice }

   Note: 
   
     the locks inside curly brackets are the group lock's total lock, which consists of pjsua as an external (chained) lock in the first position and it's own lock (marked as "ice" that is created by the group lock).

4. From a worker thread, an event occurs in ICE (such as incoming packet), which cause ice group lock to be acquired. The processing then calls a high level PJSUA-LIB callback, which acquires PJSUA's lock. The whole lock order then is depicted below.
   
   .. code-block::

      { pjsua --> ice } --> pjsua

As shown above, the lock order between "pjsua" and "ice" is maintained uniformly, hence deadlock is avoided.

For a more complete solution, the PJSUA-LIB's lock itself can be changed to a group lock, which can be synchronized to external lock such as application lock, hence making the whole system deadlock proof.

Use :cpp:any:`pj_grp_lock_chain_lock` API synchronize an external lock with the group lock.

The ``pos`` argument specifies the lock order and also the relative
position with regard to lock ordering against the group lock. Lock with
lower ``pos`` value will be locked first, and those with negative value
will be locked before the group lock (the group lock's ``pos`` value is
zero).

The :cpp:any:`pj_grp_lock_unchain_lock` unregisters external lock:



Lock Replace
~~~~~~~~~~~~

The :cpp:any:`pj_grp_lock_replace` API is used to move things from the old lock to the new lock and
close the old lock.


Debugging
---------

To enable debugging, declare :cpp:any:`PJ_GRP_LOCK_DEBUG` to non-zero in your
:any:`config_site.h`. With this, now every call to
:cpp:any:`pj_grp_lock_dec_ref()` will cause the group lock state to be printed
to log at level four. This info includes the current value of the
reference counter, along with the source file and line number info of
the code that adds the reference counter.

Note though that each :cpp:any:`pj_grp_lock_acquire()` and
:cpp:any:`pj_grp_lock_release()` also increments and decrements the reference
counter, hence they will also cause info to be dump.

If you after this find out that the leaking reference is caused by
timer, you can enable timer heap debugging by setting :cpp:any:`PJ_TIMER_DEBUG`
to non-zero and call :cpp:any:`pj_timer_heap_dump()` to dump the state of the
timer heap including information about the source file and line number
of code that registered currently active timer entries.

Notes
-----

Deadlock When Synchronizing to More Than One External Locks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding more than one external locks to a group lock may introduce
deadlock potential. Consider the following example.

1. External lock EA and EB (read: external A and B) are added to group
   lock G, resulting in group lock's chain: ``{EA --> EB --> G}``
2. Thread 1 locks EA then G. The lock order then is:
   ``EA --> { EA --> EB --> G }``
3. Thread 2 locks EB then G. The lock order then is:
   ``EB --> { EA --> EB --> G }``
4. The lock orders in 2 and 3 are not uniform, potentially causing
   deadlock.

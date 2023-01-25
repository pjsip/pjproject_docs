General Concepts
==================

.. contents:: Table of Contents
    :depth: 3


Classes Overview
----------------------
Here are the main classes of the PJSUA2:

:cpp:class:`pj::Endpoint`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the main class of PJSUA2. You need to instantiate one and exactly one of 
this class, and from the instance you can then initialize and start the library.

:cpp:class:`pj::Account`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An account specifies the identity of the person (or endpoint) on one side of SIP 
conversation. At least one account instance needs to be created before anything 
else, and from the account instance you can start making/receiving calls as well 
as adding buddies.

:cpp:class:`pj::Media`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is an abstract base class that represents a media element which is capable 
to either produce media or takes media. It is then subclassed into :cpp:class:`pj::AudioMedia`, 
which is then subclassed into concrete classes such as :cpp:class:`pj::AudioMediaPlayer` 
and :cpp:class:`pj::AudioMediaRecorder`.

:cpp:class:`pj::Call`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This class represents an ongoing call (or speaking technically, an INVITE session) and 
can be used to manipulate it, such as to answer the call, hangup the call, put the call 
on hold, transfer the call, etc.

:cpp:class:`pj::Buddy`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This class represents a remote buddy (a person, or a SIP endpoint). You can 
subscribe to presence status of a buddy to know whether the buddy is 
online/offline/etc., and you can send and receive instant messages to/from the buddy.


Guidelines
---------------------
Class Usage Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With the methods of the main classes above, you will be able to invoke various 
operations to the object quite easily. But how can we get events/notifications 
from these classes? Each of the main classes above (except Media) will get their 
events in the callback methods. So to handle these events, just derive a class 
from the corresponding class (Endpoint, Call, Account, or Buddy) and implement/override 
the relevant method (depending on which event you want to handle). More will be 
explained in later sections.

Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We use exceptions as means to report error, as this would make the program flows 
more naturally. Operations which yield error will raise :cpp:class:`pj::Error` 
exception. If you prefer to display the error in more structured manner, the 
:cpp:class:`pj::Error` class has 
several members to explain the error, such as the operation name that raised the 
error, the error code, and the error message itself.

Asynchronous Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have developed applications with PJSIP, you'll know about this already. 
In PJSIP, all operations that involve sending and receiving SIP messages are 
asynchronous, meaning that the function that invokes the operation will complete 
immediately, and you will be given the completion status in a callback.

Take a look for example the :cpp:func:`pj::Call::makeCall()` method of the :cpp:class:`pj::Call` 
class. This function  is used to initiate outgoing call to a destination. When 
this function returns  successfully, it does not mean that the call has been 
established, but rather  it means that the call has been initiated successfully. 
You will be given the report of the call progress and/or completion in the 
:cpp:func:`pj::Call::onCallState()` callback method of :cpp:class:`pj::Call` class.

Threading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For platforms that require polling, the PJSUA2 module provides its own worker 
thread to poll PJSIP, so it is not necessary to instantiate own your polling 
thread. Application should be prepared to have the 
callbacks called by different thread than the main thread. The PJSUA2 module 
itself is thread safe.

Often though, especially if you use PJSUA2 with high level languages such as 
Python, it is required to disable PJSUA2 internal worker threads by setting 
:cpp:struct:`EpConfig.uaConfig.threadCnt <pj::EpConfig>` to 0, because Python 
doesn't  like to be called by external thread (such as PJSIP's worker thread).


Problems with Garbage Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Garbage collection (GC) exists in run-time such as Java and Python, and there 
are some problems with it when it comes to PJSUA2 usage:

- it delays the destruction of objects (including PJSUA2 objects), causing 
  the code in object's destructor to be executed out of order
- the GC operation may run on different thread not previously registered 
  to PJLIB, causing assertion

Due to problems above, application '''MUST immediately destroy PJSUA2 objects 
using object's delete() method (in Java)''', instead of relying on the GC 
to clean up the object.

For example, to delete an Account, it's **NOT** enough to just let it go 
out of scope. Application MUST delete it manually like this (in Java):

.. code-block:: c++

    acc.delete();


Objects Persistence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PJSUA2 includes :cpp:class:`pj::PersistentObject` class to provide functionality 
to read/write data from/to a document (string or file). The data can be simple 
data types such as boolean, number, string, and string arrays, or a user defined 
object. Currently the implementation supports reading and writing from/to JSON 
document (`RFC 4627 <https://datatracker.ietf.org/doc/html/rfc4627>`__), 
but the framework allows application to extend the API to support other document formats.

As such, classes which inherit from PersistentObject, such as 
:cpp:class:`pj::EpConfig` (endpoint configuration), 
:cpp:class:`pj::AccountConfig` (account configuration), and 
:cpp:class:`pj::BuddyConfig` (buddy configuration) can be loaded/saved from/to 
a file. Heres an example to save a config to a file:

.. code-block:: c++

    EpConfig epCfg;
    JsonDocument jDoc;
    epCfg.uaConfig.maxCalls = 61;
    epCfg.uaConfig.userAgent = "Just JSON Test";
    jDoc.writeObject(epCfg);
    jDoc.saveFile("jsontest.json");

To load from the file:

.. code-block:: c++

    EpConfig epCfg;
    JsonDocument jDoc;
    jDoc.loadFile("jsontest.json");
    jDoc.readObject(epCfg);



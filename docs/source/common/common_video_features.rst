- :ref:`guide_vidconf`
- :ref:`AVI streaming <avi_device>`
- Sending/receiving missing video keyframe indication using the following techniques:

  * SIP INFO with XML Schema for Media Control (`RFC 5168 <https://datatracker.ietf.org/doc/html/rfc5168#section-7.1>`_), using:

     - Full Intra Request (`RFC 5104 section 3.5.1 <https://datatracker.ietf.org/doc/html/rfc5104#section-3.5.1>`_)
     - Picture Loss Indication feedback (`RFC 4585 section 6.3.1 <https://datatracker.ietf.org/doc/html/rfc4585#section-6.3.1>`_)
     - See `issue #1234 <https://github.com/pjsip/pjproject/issues/1234>`_ for more info

  * RTCP Picture Loss Indication feedback (`RFC 4585 section 6.3.1 <https://datatracker.ietf.org/doc/html/rfc4585#section-6.3.1>`_):

     - See `issue #1437 <https://github.com/pjsip/pjproject/issues/1437>`_ for more info

- :doc:`Video source duplicator </api/generated/pjmedia/group/group__PJMEDIA__VID__TEE>`

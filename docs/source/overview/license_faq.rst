Licensing FAQ
=============================

.. contents:: Table of Contents
    :depth: 2

Why is PJSIP licensed as GPL and not (LGPL|Apache|BSD|choose your OSS license here)?
-------------------------------------------------------------------------------------

Basically we agree with FSF on this issue. Quoting the `GPL
FAQ <http://www.gnu.org/licenses/gpl-faq.html>`__:

  - Q: `Why should I use the GNU GPL rather than other free software 
    licenses? <http://www.gnu.org/licenses/gpl-faq.html#WhyUseGPL>`__ 
  - A: *Using the GNU GPL will require that all the released improved
    versions be free software. This means you can avoid the risk of having 
    to compete with a proprietary modified version of your own work.*

We don't want people to take PJSIP, mess it up (erm, improve it), and
keep the improvements as proprietary code. On the contrary, we want
everybody to enjoy PJSIP and all its improvements, and the only way to
make sure of this is by releasing PJSIP as GPL. Sure this still leaves
some debate over why not use, say LGPL, but I guess this page is
probably too short to cover that. Our stand on LGPL is explained much
better `here <http://www.fsf.org/licensing/licenses/why-not-lgpl.html>`__.

What about the “viral” nature of the GPL?
--------------------------------------------------------

People often think that using GPL-ed software means that other software
linked with the GPL software have to be GPL too, hence GPL is considered
as viral. **That is not exactly true**. Don't forget that GPL **is
compatible** with many other free software licenses, including: 

- Public domain 
- `Berkeley Database License <http://www.gnu.org/licenses/info/Sleepycat.html>`__, 
- `eCos license version 2.0 <http://www.gnu.org/licenses/ecos-license.html>`__,
- `Modified BSD license <http://www.xfree86.org/3.3.6/COPYRIGHT2.html#5>`__ (the
  original BSD license modified by removal of the advertising clause,
  sometimes is referred to as the 3-clause BSD license), 
- `Expat License <http://www.jclark.com/xml/copying.txt>`__, 
- `FreeBSD license <http://www.freebsd.org/copyright/freebsd-license.html>`__, 
- `X11 License <http://www.xfree86.org/3.3.6/COPYRIGHT2.html#3>`__, and of
  course, 
- `GNU LGPL <http://www.gnu.org/licenses/lgpl.html>`__.

And don't forget that the PJSIP license is GPLv2 **or later**, which
means one can use PJSIP under GPLv3, which is compatible with even more
licenses such as: 

- `Apache License Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__ and 
- `Microsoft Public License (Ms-PL) <http://www.microsoft.com/resources/sharedsource/licensingbasics/publiclicense.mspx>`__.

For more complete list of licenses that are compatible with GPL, please
see http://www.gnu.org/licenses/license-list.html.

In addition, we specifically allow linking PJSIP with some open source
third party libraries, as they are listed in :any:`/overview/license_3rd_party`.

Can I develop closed source products with PJSIP?
---------------------------------------------------
It depends. We use the standard GPL v2 or later for PJSIP, and GPL does
allow using GPL-ed code for closed source development, **as long as the
resulting product is not redistributed** (for example, it is only used
for internal purpose). Please see `GPL FAQ <http://www.gnu.org/licenses/gpl-faq.html>`__ 
for more information about what can/can't be done with GPL software.

Alternatively, PJSIP can be used with :any:`alt_license`.

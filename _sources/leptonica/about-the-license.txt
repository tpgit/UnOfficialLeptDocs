:version: $RCSfile: about-the-license.rst,v $ $Revision: a76523e9125f $ $Date: 2010/04/02 18:24:40 $

.. default-role:: fs

.. _`about-the-license`:

=============================
 About the Copyright License
=============================

:date: Oct 22, 2008

Leptonica has adopted a **highly unrestricted** form of copyright
license for source code. The terms are summarized at the top of each
source file::

   /*====================================================================*
   -  Copyright (C) 2001 Leptonica.  All rights reserved.
   -  This software is distributed in the hope that it will be
   -  useful, but with NO WARRANTY OF ANY KIND.
   -  No author or distributor accepts responsibility to anyone for the
   -  consequences of using this software, or for whether it serves any
   -  particular purpose or works at all, unless he or she says so in
   -  writing.  Everyone is granted permission to copy, modify and
   -  redistribute this source code, for commercial or non-commercial
   -  purposes, with the following restrictions: (1) the origin of this
   -  source code must not be misrepresented; (2) modified versions must
   -  be plainly marked as such; and (3) this notice may not be removed
   -  or altered from any source or modified source distribution.
   *====================================================================*/

A comparison with the GNU open source General Public License (GPL) is
instructive. The GPL aggressively promotes open source by requiring that
if any modification of open source is used in a commercial product, the
source for the ENTIRE product must be made open source, along with any
modification of the open source code that was imported.  This is the
reason that Bill Gates is terrified of open source. He has forbidden
Microsoft employees from having any contact with open source!

A far less restrictive license would omit the "infection" clause, but
still require that any modifications used in products must be made
available to the open source community.

The Leptonica copyright is less restrictive still. It is similar to the
Apache license. I modeled it after after the copyright used by the
developers of PNG. PNG does not require that modifications of their
source --- which may be used in commercial products --- be made available in
open source. They (and Leptonica) only require that any use of the
source, whether in original or modified form, must include the Leptonica
copyright notice, and that modified versions must be clearly marked as
such.

This is also similar to the BSD license, which Kirk McKusick playfully
called a `copycenter <http://en.wikipedia.org/wiki/Copycenter>`_, as
differentiated from the usual *copyright* and the GPL *copyleft*: "Take
it down to the copy center and make as many copies as you want." The BSD
restrictions can be approximately summarized as: (1) Don't pretend that
you wrote this, and (2) Don't sue us if it doesn't work.

Why use a minimally restrictive license? Simple. Between NIH ("not
invented here") and the learning curve for a large software package, it
makes no sense to add any further barriers to the use of this
library. Also, as explained elsewhere (e.g., see `README.html`), I have
done everything I could to simplify the integration of Leptonica with
any other C and C++ packages that you are using.

At present there are over 50 different licenses that have been approved
by the *Open Source Initiative*, all of which can be found `here
<http://www.opensource.org/licenses/>`_! The Leptonica license has not
been submitted to OSI --- I figure they have enough already. And GNU has
finished their third version of GPL, which is twice as long and four
times as complicated as the previous one.

..
   Local Variables:
   coding: utf-8
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 72
   mode: auto-fill
   standard-indent: 3
   tab-stop-list: (3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60)
   End:

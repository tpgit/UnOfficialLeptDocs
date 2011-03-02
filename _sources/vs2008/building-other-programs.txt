:version: $RCSfile: building-other-programs.rst,v $ $Revision: ab7f322f4578 $ $Date: 2011/02/08 03:40:07 $

.. default-role:: fs

============================================
 Building programs that link with |liblept|
============================================

It's simple to make projects that link with |liblept| since you can
just use the standard Visual Studio :menuselection:`&File --> &New -->
&Project...` wizards.  Most of the compiler and linker setting will be
dictated by your application's needs; you only have to add where to find
the header files and libraries needed with |liblept| and which
libraries you want to link with.

First open up your project's :guilabel:`Property Pages` (right-click the
project then choose :menuselection:`P&roperties` from the context
menu). Change :guilabel:`&Configuration:` to :guilabel:`All
Configurations`. You then have to set three items:

#. Set :guilabel:`Configuration Properties | C/C++ | General | Inherited
   Property Sheets` to:

   .. parsed-literal::

     C:\\BuildFolder\\leptonica-\ |versionF|\ \\vs2008\\leptonica_versionnumbers.vsprops

   This lets you use the ``*_VERSION`` user macros when specifying the
   libraries you want to link with. See :ref:`this section
   <using-versionnumbers-property-sheet>` for more information on this
   Property Sheet and "user macros".

#. To :guilabel:`Configuration Properties | C/C++ | General | Additional
   Include Directories` add::
   
      C:\BuildFolder\include;C:\BuildFolder\include\leptonica

#. To :guilabel:`Configuration Properties | Linker | General |
   Additional Library Directories` add::

      C:\BuildFolder\lib

Of course, if you've used some other location/name instead of
`C:\\BuildFolder` for where the `vs2008`, `include` and `lib`
directories reside, then use that instead.

Alternatively, if you don't mind having :bi:`all` programs use these
header files and libraries, you could also globally change where Visual
Studio 2008 looks for include files and libraries by setting
:menuselection:`&Tools --> &Options...` :guilabel:`| Project and
Settings | VC++ Directories`.

The last step is setting :guilabel:`Configuration Properties | Linker |
Input | Additional Dependencies`. To link with the dynamic library
Release version of |liblept| add this::

   liblept$(LIBLEPT_VERSION).lib

To link with the dynamic library Debug version of |liblept| add this::

   liblept$(LIBLEPT_VERSION)d.lib

To link with the static Release version of |liblept| add these::

   giflib$(GIFLIB_VERSION)-static-mtdll.lib
   libjpeg$(LIBJPEG_VERSION)-static-mtdll.lib
   libpng$(LIBPNG_VERSION)-static-mtdll.lib
   libtiff$(LIBTIFF_VERSION)-static-mtdll.lib
   zlib$(ZLIB_VERSION)-static-mtdll.lib
   liblept$(LIBLEPT_VERSION)-static-mtdll.lib

To link with the static Debug version of |liblept| add these::

   giflib$(GIFLIB_VERSION)-static-mtdll-debug.lib
   libjpeg$(LIBJPEG_VERSION)-static-mtdll-debug.lib
   libpng$(LIBPNG_VERSION)-static-mtdll-debug.lib
   libtiff$(LIBTIFF_VERSION)-static-mtdll-debug.lib
   zlib$(ZLIB_VERSION)-static-mtdll-debug.lib
   liblept$(LIBLEPT_VERSION)-static-mtdll-debug.lib

You can also use `create_unnumbered_hardlinks.bat` to make simplified
versions of the library filenames via NTFS hardlinks and link with those
instead. See :ref:`here <making-hardlinks>` for more details.

Any `.c` files that use |Leptonica| functions have to include
`allheaders.h`. If you want to use the Windows-only
``pixGetWindowsHBITMAP(PIX *pixs)`` to convert a |Leptonica| ``PIX`` to
a Windows ``HBITMAP`` you also have to include `leptwin.h`. It's not
automatically included by `allheaders.h`.

.. _create-tmp-directory:

Create a `\\tmp` directory
==========================

Create a `\\tmp` directory on the same drive from which you will be
running your |liblept| based programs. Some parts of |liblept| assume
they can write to `/tmp` and will mysteriously fail if this directory
doesn't exist. 

.. note::

   This issue has been addressed starting with `liblept168`, but it's
   still a good idea for now to have a `\\tmp` directory.

   |Leptonica| should now write all temporary files to your temp
   directory. This is normally `C:\\Documents and
   Settings\\<username>\\Local Settings\\Temp` but can be changed by
   setting the ``TEMP`` and ``TMP`` environment variables.


.. _intellisense-and-liblept:

Intellisense and |liblept|
============================

Intellisense is a great Visual Studio feature that automatically
completes function names, shows function arguments, quickly lets you go
to a function's definition, etc. There seems to be a problem, however,
with navigating to |liblept| function definitions. When you right
click a function name that is part of the |liblept| library and choose
:menuselection:`&Go To Definition` (or press the :kbd:`F12` key),
instead of jumping to the definition it shows you the declaration in
`leptprotos.h`.

Adding the location of `leptonica-`\ |versionF|\ `\\src` to
:menuselection:`&Tools --> &Options` :guilabel:`| Projects and Solutions
| VC++ Directories | Show Directories For | Source Files` doesn't help,
even though that list is described as "Path to use when searching for
source files to use for Intellisense."

(The commercial program `Visual Assist X for Visual Studio
<http://www.wholetomato.com/>`_ has the command
:menuselection:`VAssist&X --> &Goto Implementation` (:kbd:`Alt+G`) that
does do the correct thing as long as you follow `these instructions
<http://www.wholetomato.com/products/features/goto.asp>`_.)

In order to have Visual Studio's :menuselection:`&Go To Definition`
command work correctly with |liblept|, you have to add its project to
your current solution:

#. Right click your solution in the Solution Explorer, and choose
   :menuselection:`A&dd --> &Existing Project...` from the context menu.

#. Select the `leptonica-`\ |versionF|\ `\\vs2008\\leptonica.vcproj`
   file and click :guilabel:`&Open`.

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

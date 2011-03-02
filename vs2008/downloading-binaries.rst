:version: $RCSfile: downloading-binaries.rst,v $ $Revision: ab7f322f4578 $ $Date: 2011/02/08 03:40:07 $

.. default-role:: fs


.. _downloading-pre-built-binaries:

=======================================================================
 Downloading |liblept| pre-built binaries and header files for Windows
=======================================================================

The easiest way to use |liblept| is to download the latest version of
`leptonica-`\ |versionF|\ `-win32-lib-include-dirs.zip`, the pre-built
binary archive, from `the Leptonica website
<http://tpgit.github.com/UnOfficialLeptDocs/leptonica/source-downloads.html#windows-pre-built-binaries>`_.

It contains the entire `lib` and `include` directories needed to build
Windows-based programs that use the static or dynamic versions of the
|liblept| library (including static library versions of `zlib`,
`libpng`, `libjpeg`, `libtiff`, and `giflib`). The libraries are built
with Microsoft Visual Studio 2008 32-bit. The complete contents of the
archive can be seen :ref:`here <include-contents>`.

Unpack this file to the same directory that |liblept| will be in. For
example, after unpacking you should have something similar to this:

.. parsed-literal::
  
   BuildFolder\\
     include\\
     leptonica-|version|\\
     lib\\

The archive contains the latest releases of the supported image
libraries at the time |liblept| was released. For the current version
(Leptonica-|version|) these are:

.. _image-library-versions:

.. table:: Image Library Versions
   :class: centered, centercells

   +----------+---------+-------------+
   | Library  | Version |    Date     |
   +==========+=========+=============+
   |  zlib    | 1.2.5__ |19-Apr-2010  |
   +----------+---------+-------------+
   |  libpng  | 1.4.3__ | 25-Jun-2010 |
   +----------+---------+-------------+
   | libjpeg  | 8c__    | 16-Jan-2011 |
   +----------+---------+-------------+
   | libtiff  | 3.9.4__ | 15-Jun-2010 |
   +----------+---------+-------------+
   |  giflib  | 4.1.6__ | 10-Nov-2007 |
   +----------+---------+-------------+

.. __: http://www.zlib.net/zlib125.zip
.. __: http://prdownloads.sourceforge.net/libpng/lpng143.zip
.. __: http://www.ijg.org/files/jpegsr8c.zip
.. __: http://download.osgeo.org/libtiff/tiff-3.9.4.zip
.. __: http://sourceforge.net/projects/giflib/files/giflib%204.x/giflib-4.1.6/giflib-4.1.6.tar.gz/download

A simple method to print out the versions of |liblept| and its image
libraries is shown in the :ref:`Quickstart <building-hello-liblept>`.

If you'd like to determine the compiler options used to build these
binaries or build them yourself see :doc:`building-liblept` and
:doc:`building-image-libraries`.

.. note::

   Executables for the programs in the |liblept| `/prog` directory are
   **not** included in this archive. Follow these :doc:`instructions
   <building-prog-dir>` to build them yourself.

.. _about-version-numbers:

About version numbers in library filenames
==========================================

To make it possible to tell at a glance which version of the libraries
are being provided, they all now have version numbers as part of their
filenames. This, however, this makes them somewhat more difficult to use
in Visual Studio Projects and external makefiles when the versions
change.

.. _making-hardlinks:

There are two different solutions to this versioning problem. The first
is the `create_unnumbered_hardlinks.bat` batch file which uses the
built-in Windows command-line program :cmd:`fsutil` to make simplified
filenames by creating NTFS hardlinks to the versioned files.

Copy `C:\BuildFolder\\leptonica-`\ |versionF|\
`\\vs2008\\create_unnumbered_hardlinks.bat` and
`remove_unnumbered_hardlinks.bat` to `C:\\BuildFolder\\lib`. Then, after
opening a Command Window, switching to the `C:\\BuildFolder\\lib`
directory and running `create_unnumbered_hardlinks.bat` (or just
double-clicking it in Windows Explorer) you'll be able to refer to the
static |liblept| library:

   .. parsed-literal::

      liblept\ |vnum|\ -static-mtdll.lib

as any of the following:

   .. parsed-literal::

      leptonlib-static-mtdll.lib
      liblept\ |vnum|\ -static.lib
      liblept-static.lib

and the import library for the |liblept| DLL:

   .. parsed-literal::

      liblept\ |vnum|\ .lib

as:

   .. parsed-literal::

      leptonlib.lib
      liblept\ |vnum|\ .lib
      liblept.lib

Similarly, you'll be able to refer to::

   libtiff394-static-mtdll.lib

as::

   libtiff-static-mtdll.lib
   libtiff394.lib
   libtiff.lib


.. warning::

   A NTFS hardlink doesn't act quite the same as a unix symbolic
   link. If the target of the link is deleted or renamed, the hardlink
   becomes a :bi:`copy` of the original file. When in doubt after
   updating/rebuilding the targets, it's best to remake the hardlinks by
   first running `remove_unnumbered_hardlinks.bat` and then running
   `create_unnumbered_hardlinks.bat` again.

.. _using-versionnumbers-property-sheet:

For those who don't want to rely on NTFS hardlinks, another solution is
provided for handling numbered library filenames within Visual Studio
Projects. To use it, set your Project's :guilabel:`Configuration
Properties | C/C++ | General | Inherited Property Sheets` to:

   .. parsed-literal::

     C:\\BuildFolder\\leptonica\ |versionF|\ \\vs2008\\leptonica_versionnumbers.vsprops

This lets you use the provided ``*_VERSION`` user macros when specifying
the libraries you want to link with.

For example, to link with the |liblept| DLL you should now set
:guilabel:`Configuration Properties | Linker | Input | Additional
Dependencies` to::

   liblept$(LIBLEPT_VERSION).lib

And to link with the static Release version of |liblept| use these::

   giflib$(GIFLIB_VERSION)-static-mtdll.lib
   libjpeg$(LIBJPEG_VERSION)-static-mtdll.lib
   libpng$(LIBPNG_VERSION)-static-mtdll.lib
   libtiff$(LIBTIFF_VERSION)-static-mtdll.lib
   zlib$(ZLIB_VERSION)-static-mtdll.lib
   liblept$(LIBLEPT_VERSION)-static-mtdll.lib

You can view the user macros defined in `leptonica_versionnumbers.vsprops` by opening the :menuselection:`&View --> Oth&er Windows --> Property &Manager` and looking at the :guilabel:`Common Properties | User Macros` page.

If you copy this file to a known location, reference it in your own
Projects, and use the new ``*_VERSION`` macros when specifying linker
dependencies, you will be isolated from worrying about version number
changes in library filenames. After that, you can use the Property
Manager (or a text editor since it's a simple XML file) to fix any
version number updates by changing this one file.


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


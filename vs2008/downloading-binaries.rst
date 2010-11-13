:version: $RCSfile: downloading-binaries.rst,v $ $Revision: 0191b0f4799d $ $Date: 2010/11/11 12:02:43 $

.. default-role:: fs


.. _downloading-pre-built-binaries:

Downloading |leptonlib| pre-built binaries and header files for Windows
=======================================================================

The easiest way to use |leptonlib| is to download the latest version of
`leptonica-`\ |versionF|\ `-win32-lib-include-dirs.zip`, the pre-built
binary archive, from :ref:`the Leptonica website
<windows-pre-built-binaries>`.

It contains the entire `lib` and `include` directories needed to build
Windows-based programs that use the static or dynamic versions of the
|leptonlib| library (including static library versions of `zlib`,
`libpng`, `libjpeg`, `libtiff`, and `giflib`). The libraries are built
with Microsoft Visual Studio 2008 32-bit. The complete contents of the
archive can be seen :ref:`here <include-contents>`.

Unpack this file to the same directory that |leptonlib| will be in. For
example, after unpacking you should have something similar to this:

.. parsed-literal::
  
   BuildFolder\\
     include\\
     leptonlib-|version|\\
     lib\\

The archive contains the latest releases of the supported image
libraries at the time |leptonlib| was released. For the current version
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
   | libjpeg  | 8b__    | 16-May-2010 |
   +----------+---------+-------------+
   | libtiff  | 3.9.4__ | 15-Jun-2010 |
   +----------+---------+-------------+
   |  giflib  | 4.1.6__ | 10-Nov-2007 |
   +----------+---------+-------------+

.. __: http://www.zlib.net/zlib125.zip
.. __: http://prdownloads.sourceforge.net/libpng/lpng143.zip
.. __: http://www.ijg.org/files/jpegsr8b.zip
.. __: http://download.osgeo.org/libtiff/tiff-3.9.4.zip
.. __: http://sourceforge.net/projects/giflib/files/giflib%204.x/giflib-4.1.6/giflib-4.1.6.tar.gz/download

A simple method to get the versions of |leptonlib| and its image
libraries is shown in the :ref:`Quickstart <building-hello-leptonlib>`.

If you'd like to determine the compiler options used to build these
binaries or build them yourself see :doc:`building-leptonlib` and
:doc:`building-image-libraries`.

.. note::

   Executables for the programs in the |leptonlib| `/prog` directory are
   **not** included in this archive. Follow these :doc:`instructions
   <building-prog-dir>` to build them yourself.


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

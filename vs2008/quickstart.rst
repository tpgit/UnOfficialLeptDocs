:version: $RCSfile: quickstart.rst,v $ $Revision: 37f29fe52bad $ $Date: 2011/03/02 14:34:46 $

.. default-role:: fs

.. _quickstart:

============
 Quickstart
============

Using |liblept| on Windows is now very easy, given that you no longer
need to build the library (and more importantly the supporting image
libraries) yourself. This page discusses the basics.

Getting |liblept|
=================

Here's the items you need to get:

1. Download the `latest version
   <http://tpgit.github.com/UnOfficialLeptDocs/leptonica/source-downloads.html#windows-pre-built-binaries>`__
   of the |liblept| :doc:`pre-built binaries for Windows archive
   <downloading-binaries>` and extract it to a directory of your choice
   (here called |BuildFolder|).

Strictly speaking the |liblept| sources aren't needed to build
applications that use |liblept| but the `src` and `prog` directories
are the best way to learn how to call Leptonica functions. It also has a
number of test programs and images that are useful. So . . .

2. Download the latest version of leptonica from `here
   <http://tpgit.github.com/UnOfficialLeptDocs/leptonica/source-downloads.html#leptonica>`__
   and also extract it to |BuildFolder|.

Downloading the VS2008 build package will make life easier if you plan
on using the Visual Studio 2008 IDE to write programs that use
|liblept|. This is highly recommended since the Visual Studio
:ref:`Intellisense <intellisense-and-liblept>` code-completion feature
works very nicely for figuring out how to call the multitudinous
Leptonica functions.

3. Download the Microsoft Visual Studio 2008 build package from `here
   <http://tpgit.github.com/UnOfficialLeptDocs/leptonica/source-downloads.html#microsoft-visual-studio-2008>`__. Extract
   the archive to the `BuildFolder\\leptonica-`\ |versionF|
   directory. You should now have:

.. parsed-literal::

   BuildFolder\\
     include\\
     leptonica-|version|\\
       vs2008\\
         prog_projects\\
     lib\\

4. In addition, you'll eventually have to install the :doc:`core cygwin
   utilities <installing-cygwin>` which various parts of |liblept|
   assume you have; :doc:`IrFanview <installing-irfanview>`, if you want
   to automatically view Leptonica generated images; and :doc:`gnuplot
   <installing-gnuplot>` to view Leptonica generated plots.

   You can skip this step for simple programs, but you'll probably
   eventually need to get all three.


.. _building-hello-liblept:

Building `"Hello, liblept"`
===========================

The easiest way to use |liblept| is by linking with the DLL
version. Here's a simple example of building a program that just prints
out the |liblept| library's version numbers:

1. Open a :guilabel:`Visual Studio 2008 Command Prompt` Window and
   switch to the `BuildFolder\\leptonica-`\ |versionF|\
   `\\vs2008\\prog_projects` directory.

#. Create a new directory called `hellolept` and create `hellolept.c`
   there with the following contents:

   .. code-block:: c

      #include <stdio.h>
      /* The only leptonica header file you normally need to include: */
      #include "allheaders.h"

      main(int argc, char **argv)
      {
          printf("liblept version:\n%s\n", getLeptonicaVersion());
          printf("image library versions:\n%s", getImagelibVersions());
      }

#. Compile and link `hellolept.c`::

      cl /O2 /I "..\..\..\..\include" /I "..\..\..\..\include\leptonica" /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /FD /EHsc /MD hellolept.c /link /LIBPATH:"..\..\..\..\lib" liblept168.lib

#. You should see the following:

   .. parsed-literal::

      Microsoft (R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
      Copyright (C) Microsoft Corporation.  All rights reserved.

      hellolept.c
      Microsoft (R) Incremental Linker Version 9.00.30729.01
      Copyright (C) Microsoft Corporation.  All rights reserved.

      /out:hellolept.exe
      /LIBPATH:..\\..\\..\\..\\lib
      liblept\ |vnum|\ .lib
      hellolept.obj

#. In order to execute `hellolept.exe` Windows needs to be able to find
   `liblept`\ |vnumF|\ `.dll` somewhere in its `PATH`::

      set path=..\..\..\..\lib;%PATH%

#. Now execute `hellolept` and you should see:

   .. parsed-literal::

      liblept version:
      leptonica-\ |version| (Feb 7 2011, 14:58:38) [MSC v.1500 DLL Release 32 bit]
      image library versions:
      libgiff 4.1.6 : libjpeg 8c : libpng 1.4.3 : libtiff 3.9.4 : zlib 1.2.5

If you instead want to link with the static library version of
|liblept|, you have to also link with all the image libraries. Here's
the command line to do that::

      cl /O2 /I "..\..\..\..\include" /I "..\..\..\..\include\leptonica" /D "WIN32" /D "NDEBUG" /D "_CONSOLE" /FD /EHsc /MD hellolept.c /link /LIBPATH:"..\..\..\..\lib" zlib125-static-mtdll.lib libpng143-static-mtdll.lib libjpeg8c-static-mtdll.lib libtiff394-static-mtdll.lib giflib416-static-mtdll.lib liblept168-static-mtdll.lib 


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

:version: $RCSfile: building-image-libraries.rst,v $ $Revision: 26bd0c5c4b08 $ $Date: 2010/08/14 01:12:28 $

.. default-role:: fs

.. _building-requisite-libraries:

=========================================================================
 (Optional) Building `zlib`, `libjpeg`, `libpng`, `libtiff` and `giflib`
=========================================================================

For some reason, you might want to build the image libraries |leptonlib|
uses. The process involves downloading and extracting the library
sources, building them, and then copying the required header files to
`BuildFolder\\include`, and the libraries to `BuildFolder\\lib`.


Image library links
===================

Here's a summary of the image libraries that |leptonlib| can use and
their dependencies:

.. parsed-literal::
    
   `zlib <http://www.zlib.net>`_
     current version: http://www.zlib.net/zlib125.zip
     zlib has no other dependencies.
     An older Visual Studio Workspace file is provided
      (but Visual 2008 can convert it to a Solution)

   `libpng <http://libpng.org/pub/png/libpng.html>`_
     current version: http://prdownloads.sourceforge.net/libpng/lpng143.zip
     libpng depends on zlib.
     A Visual Studio solution file is provided.
     libpng can also build zlib but we build zlib separately.

   `libjpeg <http://www.ijg.org/>`_
     current version: http://www.ijg.org/files/jpegsr8b.zip
     libjpeg has no other dependencies.
     A Visual Studio 2010 solution file is provided.

   `libtiff <http://www.remotesensing.org/libtiff/>`_
     current version: http://download.osgeo.org/libtiff/tiff-3.9.4.zip
     libtiff depends on libjpeg and zlib.
     Only a nmake file is provided.

   `giflib <http://sourceforge.net/projects/giflib/>`_
     current version:
     http://sourceforge.net/projects/giflib/files/giflib%204.x/giflib-4.1.6/giflib-4.1.6.tar.gz/download
     giflib has no other dependencies.


Using the same runtime library
==============================

A very important consideration to keep in mind is that :bi:`all` parts
of a program have to be built with references to the exact same
runtime library. Or as `Visual C++ Compiler Options /MD, /MT, /LD (Use
Run-Time Library)
<http://msdn.microsoft.com/en-us/library/2kzt1wy3.aspx>`_ succinctly
states:

   All modules passed to a given invocation of the linker must have
   been compiled with the same run-time library compiler option (``/MD``,
   ``/MT``, ``/LD``).

In our case this means consistently using the **Multi-threaded Debug
DLL** (``/MDd``) or the **Multi-threaded DLL** (``/MD``) compiler
option. See `How to link with the correct C Run-Time (CRT) library
<http://support.microsoft.com/kb/140584>`_ for more details. If you
attempt to mix and match libraries and object files built with
references to different runtime libraries you'll get lots of warning
messages similar to the following::

      LINK : warning LNK4098: defaultlib 'LIBCMT' conflicts with use of
      other libs; use /NODEFAULTLIB:library

      LIBCMTD.lib(crt0dat.obj) : error LNK2005: _exit already defined in
      MSVCRTD.lib(MSVCR90D.dll)

In particular you can't even mix and match libraries built with
references to the Multi-threaded Debug DLL (``/MDd``) runtime library
with those built with references to the Multi-threaded DLL (``/MD``)
runtime library. This is the reason why the libraries built in this
section have such long filenames. They are needed to make sure that only
libraries referencing the same runtime library are used together.

To diagnose these kinds of issues you can use ``dumpbin /directives
somelibrary.lib`` from the command line to see which runtime
library `somelibrary.lib` was built to use.

The ``/MD`` and ``/MDd`` switches were chosen because the ``/clr``
option which enables linking with .NET languages can only be used with
those runtime libraries. See `C Run-Time Libraries
<http://msdn.microsoft.com/en-us/library/abx4dbyh.aspx>`_ for more
details.


Download and extract the image libraries
========================================

1. Download `zlib125.zip` and extract its contents to
   `BuildFolder\\zlib`.  Note that the `libpng.sln` provided with
   `libpng` :bi:`requires` `zlib` to be in this location.

#. Download `lpng143.zip`, `jpegsr8b.zip`, `tiff-3.9.4.zip` and
   `giflib-4.1.6`. Extract them to |BuildFolder|. You should now have:

   .. parsed-literal::

      BuildFolder\\
        giflib-4.1.6\\
        include\\
        jpeg-8b\\
        leptonlib-|version|\ \\
        lib\\
        libtiff-3.9.4\\
        lpng143\\
        zlib\\

At this point you might want to empty your `include` and `lib`
directories to get rid of any files that were supplied with the
pre-built binaries archive.


Building `zlib`
===============

1. Open a Command Prompt window and execute `C:\\Program
   Files\\Microsoft Visual Studio 9.0\\VC\\bin\\vcvars32.bat` to set
   some environmental variables correctly.

#. :cmd:`cd` to the `BuildFolder\\zlib\\contrib\\masmx86`
   directory. Then execute::

      bld_ml32.bat

   to assemble the `asm` files required for the `zlib` Release
   configuration.

#. Using Visual Studio 2008, open
   `BuildFolder\\zlib\\contrib\\vstudio\\vc9\\zlibvc.sln`.

#. Select the desired build configuration (either :guilabel:`Debug` or
   :guilabel:`Release` and probably :guilabel:`Win32`).

#. Right-click :guilabel:`zlibstat` and choose
   :menuselection:`Properties`. Change :guilabel:`Configuration
   Properties | C/C++ | Code Generation | Runtime Library` to either
   :guilabel:`Multi-threaded Debug DLL (/MDd)` if building a
   :guilabel:`Debug` configuration or :guilabel:`Multi-threaded DLL
   (/MD)` if building a :guilabel:`Release` configuration.

   Also remove `ZLIB_WINAPI` from :guilabel:`Configuration Properties |
   C/C++ | Preprocessor | Preprocessor Definitions`. If you don't do
   this you'll get `undefined symbol` error messages when trying to
   build `libpng` and `libtiff`.

#. Right-click :guilabel:`zlibstat` and choose
   :menuselection:`Build`. This will make `zlibstat.lib`. It will be in
   `zlib\\contrib\\vstudio\\vc9\\x86\\ZlibStatDebug` or
   `zlib\\contrib\\vstudio\\vc9\\x86\\ZlibStatRelease`. Copy it to
   `BuildFolder\\lib`. To avoid confusion (and to match what the
   `leptonlib.vcproj` settings say), rename it to follow the ClanLib
   naming conventions.  So they should be::

      zlib-static-mtdll.lib or 
      zlib-static-mtdll-debug.lib

#. Copy `zlib\\zlib.h` and `zconf.h` to `BuildFolder\\include`.

To test the `zlib` static library, you first have to change the
:guilabel:`testzlib` project (the supplied project just directly
includes the `.c` source files instead of linking with the static
library).

1. From its Source Files solution folder, remove all files except for
   `testzlib.c`.

   Then right-click :guilabel:`testzlib` and choose
   :menuselection:`Properties`. Change :guilabel:`Configuration
   Properties | Linker | General | Additional Library Directories` to
   `x86/ZlibStatRelease`. To :guilabel:`Configuration Properties |
   Linker | Input | Additional Dependencies` add `zlibstat.lib`.

#. Right-click :guilabel:`testzlib` and choose
   :menuselection:`Properties`. Change :guilabel:`Configuration
   Properties | C/C++ | Code Generation | Runtime Library` to either
   :guilabel:`Multi-threaded Debug DLL (/MDd)` if building a
   :guilabel:`Debug` configuration or :guilabel:`Multi-threaded DLL
   (/MD)` if building a :guilabel:`Release` configuration.

   Also remove `ZLIB_WINAPI` from :guilabel:`Configuration Properties |
   C/C++ | Preprocessor | Preprocessor Definitions`.

   Change :guilabel:`Configuration Properties | Linker | Manifest File |
   Generate Manifest` to :guilabel:`Yes`, otherwise when you attempt to
   run `testzlib.exe` you'll get a "MSVCR90.dll was not found" error.

#. Right-click :guilabel:`testzlib` and choose :menuselection:`Build`.

#. In a Command Prompt window, :cmd:`cd` to the
   `BuildFolder\\zlib\\contrib\\vstudio\\vc9\\x86\\TestZlibRelease`
   directory. Then execute::

      testzlib.exe testzlib.pdb
 
   You should see the following::

      file testzlib.pdb read, 1100800 bytes
      total compress size = 178215, in 34 step
      time = 125 msec = 0.125000 sec
      defcpr time QP = 129 msec = 0.129000 sec
      defcpr result rdtsc = 1025607f

      total uncompress size = 1100800, in 34 step
      time = 16 msec = 0.016000 sec
      uncpr  time QP = 0 msec = 0.000000 sec
      uncpr  result rdtsc = 139d5ce

      compare ok
   
Building `libpng`
=================

1. Open `BuildFolder\\lpng143\\projects\\visualc71\\libpng.sln` (Just
   click :guilabel:`Next` thru the Visual Studio Conversion
   Wizard). There are five different configurations you can
   build. Normally you'll want :guilabel:`LIB Release` or :guilabel:`LIB
   Debug`.

#. To be compatible with the way the other library Debug versions are
   built, you might want to change the :guilabel:`LIB Debug
   Configuration Properties | C/C++ | General | Debug Information
   Format` from :guilabel:`Program Database for Edit & Continue (/ZI)`
   to :guilabel:`C7 Compatible (/Z7)`. This embeds debug information
   directly in the generated `.lib` so you don't have to worry about
   also copying `.pdb` files.

#. Build the :guilabel:`libpng` by right-clicking it and choosing
   :menuselection:`Build`. This will make `libpng.lib` (or
   `libpngd.lib`). They'll be in
   `lpng143\\projects\\visualc71\\Win32_LIB_Release` or
   `lpng143\\projects\\visualc71\\Win32_LIB_Debug`. Copy them to
   `BuildFolder\\lib`. To avoid confusion (and to match what the
   `leptonlib.vcproj` settings say), rename them following the ClanLib
   naming conventions.  So they should be::

      libpng-static-mtdll.lib or 
      libpng-static-mtdll-debug.lib

   The :guilabel:`libpng` project erroneously includes a dependency on
   the :guilabel:`zlib` project, so you'll get an error message about
   not being able to find `gzio.c`. Since you previously made `zlib`
   separately (specifically to avoid this problem), you can ignore this
   message.

#. Copy `lpng143\\png.h` and `pngconf.h` to `BuildFolder\\include`.

You can test `libpng` by building `pngtest.exe`.

1. Right-click :guilabel:`pngtest` and choose
   :menuselection:`Properties`. Change :guilabel:`Configuration
   Properties | Linker | General | Additional Library Directories` to
   `..\\..\\..\\lib`. To :guilabel:`Configuration Properties | Linker |
   Input | Additional Dependencies` add `zlib-static-mtdll-debug.lib`.


#. Build and run :guilabel:`pngtest` by right-clicking it and choosing
   :menuselection:`Build`.

   You should see the following::

      2>Testing...
      2> Testing libpng version 1.4.3
      2>   with zlib   version 1.2.5
      2>libpng version 1.4.3 - June 26, 2010
        Copyright (c) 1998-2010 Glenn Randers-Pehrson
        Copyright (c) 1996-1997 Andreas Dilger
        Copyright (c) 1995-1996 Guy Eric Schalnat, Group 42, Inc. library (10403):
        libpng version 1.4.3 - June 26, 2010
      2> pngtest (10403): libpng version 1.4.3 - June 26, 2010
      2> sizeof(png_struct)=656, sizeof(png_info)=288
      2> Testing ..\..\pngtest.png:
      2> Pass 0: rwrwrwrwrwrwrwrwrw
      2> Pass 1: rwrwrwrwrwrwrwrwrw
      2> Pass 2: rwrwrwrwrwrwrwrw
      2> Pass 3: rwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrw
      2> Pass 4: rwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrw
      2> Pass 5: rwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrw
      2>         rwrwrwrw
      2> Pass 6: rwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrwrw
      2>         rwrwrwrwrw
      2> PASS (9782 zero samples)
      2> Filter 0 was used 21 times
      2> Filter 1 was used 15 times
      2> Filter 2 was used 52 times
      2> Filter 3 was used 10 times
      2> Filter 4 was used 33 times
      2> tIME = 7 Jun 1996 17:58:08 +0000
      2> libpng passes test


.. _building-libjpeg:

Building `libjpeg`
==================

Unfortunately, as of `jpeg-8b` Visual Studio 2008 is no longer
supported, only Visual Studio 2010. This seems a bit premature to me but
the solution recommended by the developers is to download `jpeg-8a` and
copy the required solution and project files.

Therefore, I supply a Visual Studio 2008 Solution for `jpeg-8b` in
`leptonlib-`\ |versionF|\ `\\vs2008\\jpeg-8b-vs2008.zip`. Extract it to
`BuildFolder\\jpeg-8b`.

#. Open `BuildFolder\\jpeg-8b\jpeg.sln`.

#. Select the desired build configuration (either :guilabel:`Debug` or
   :guilabel:`Release` and probably :guilabel:`Win32`).

#. Build the Solution.

#. Copy `BuildFolder\\jpeg-8b\\Release\\jpeg.lib` to `BuildFolder\\lib`.
   Rename it to: `libjpeg-static-mtdll.lib`

   and/or copy `BuildFolder\\jpeg-8b\\Debug\\jpeg.lib` to `BuildFolder\\lib`.
   Rename it to: `libjpeg-static-mtdll-debug.lib`.

#. Copy `jpeglib.h`, `jconfig.h`, `jmorecfg.h`, and `jerror.h` to
   `BuildFolder\\include`.

.. _building-libtiff:

Building `libtiff`
==================

After a long quiet period, `libtiff` is undergoing a flurry of changes
so it seems best to get the latest version (currently 3.9.4).

1. `Building the Software under Windows 95/98/NT/2000 with MS VC++
   <http://www.remotesensing.org/libtiff/build.html#PC>`_ explains the
   overall process of building `libtiff`. However, in order to use the
   correct `include` and `lib` dirs, and allow creation of Debug builds
   without manual editing of the `nmake.opt` file, I supply
   `leptonlib-`\ |versionF|\ 
   `\\vs2008\\libtiff3.9.2-vs2008-makefiles-for-leptonica.zip` which
   contains custom versions of `nmake.opt`, `libtiff\\Makefile.vc` and
   `tools\\Makefile.vc`.

#. Extract `libtiff3.9.2-vs2008-makefiles-for-leptonica.zip` to
   `BuildFolder\\tiff-3.9.4`. This will overwrite the existing
   versions of the above files so you might want to back them up
   first.

#. To build `libtiff` open a Command Prompt window and first
   execute `C:\\Program Files\\Microsoft Visual Studio
   9.0\\VC\\bin\\vcvars32.bat` to set some environmental variables
   correctly.

#. :cmd:`cd` to the `BuildFolder\\tiff-3.9.4\\libtiff`
   directory. Then do::

      nmake /f makefile.vc clean

   Then to make a Debug build of libtiff::

      nmake /f makefile.vc DEBUG=1
      nmake /f makefile.vc DEBUG=1 install

   or to make a Release build::

      nmake /f makefile.vc
      nmake /f makefile.vc install

   The last :cmd:`nmake` command copies the required `libtiff` header
   files and the library to the `BuildFolder\\include` and
   `BuildFolder\\lib` directories.

#. (Optional but recommended) To build the tiff tools, :cmd:`cd` to the
   `BuildFolder\\tiff-3.9.4` directory.

   Then to make the tiff tools::

      nmake /f makefile.vc DEBUG=1

   or to make a Release build::

      nmake /f makefile.vc

   You can't build the tiff tools and `libtiff` together initially
   because the linker expects to find `.pdb` files where the
   `.lib` is. Thus you first have to make and :bi:`install`
   `libtiff-static-mtdll(-debug).lib` so that the linker can find
   `libjpeg-static-mtdll.pdb` and
   `libjpeg-static-mtdll-debug.pdb`.

   To test your build of `libtiff`, :cmd:`cd` to the
   `BuildFolder\\tiff-3.9.4\\tools` directory, then execute the
   following from the command line:

   .. parsed-literal::

      tiffinfo.exe ..\\..\\leptonlib-|version|\\prog\\feyn.tif

   You should see the following output::

      TIFF Directory at offset 0x1989e (104606)
        Image Width: 2528 Image Length: 3300
        Resolution: 300, 300 pixels/inch
        Bits/Sample: 1
        Compression Scheme: CCITT Group 4
        Photometric Interpretation: min-is-white
        Orientation: row 0 top, col 0 lhs
        Samples/Pixel: 1
        Rows/Strip: 3300
        Planar Configuration: single image plane


.. _building-giflib:

Building `giflib`
=================

#. I supply a Visual Studio 2008 Solution for `giflib` in
   `leptonlib-`\ |versionF|\ `\\vs2008\\giflib4.1.6.zip`. Extract it to
   `BuildFolder\\giflib-4.1.6\\windows`.

#. `giflib` requires `stdint.h` Before building it you’ll need to
   download http://www.azillionmonkeys.com/qed/pstdint.h, rename it to
   stdint.h, and then move it to the standard Visual C++ include
   directory: `C:\\Program Files\\Microsoft Visual Studio
   9.0\\VC\\include`.

#. Open `BuildFolder\\giflib-4.1.6\\windows\\giflib\\giflib.sln`.

#. Select the desired build configuration (either :guilabel:`Debug` or
   :guilabel:`Release` and probably :guilabel:`Win32`).

   :guilabel:`Debug` builds use the following C compiler options::

      /Od
      /D "WIN32" /D "WINDOWS32" /D "_DEBUG" /D "_LIB" /D "_OPEN_BINARY"
      /D "HAVE_IO_H" /D "HAVE_FCNTL_H" /D "HAVE_STDARG_H" /D "HAVE_BASETSD_H"
      /D "HAVE_STDINT_H" /D "HAVE_SYS_TYPES_H" /D "_MBCS"
      /FD /EHsc /RTC1 /MDd /Fo"Debug\\" /Fd"Debug\vc90.pdb"
      /W3 /nologo /c /Z7 /errorReport:prompt

   :guilabel:`Release` builds use the following C compiler options::

      /O2 /Oi
      /D "WIN3" /D "WINDOWS32" /D "NDEBUG" /D "_LIB" /D "_OPEN_BINARY"
      /D "HAVE_IO_H" /D "HAVE_FCNTL_H" /D "HAVE_STDARG_H" /D "HAVE_BASETSD_H"
      /D "HAVE_STDINT_H" /D "HAVE_SYS_TYPES_H" /D "_MBCS"
      /FD /EHsc /MD /Fo"Release\\" /Fd"Release\vc90.pdb"
      /W3 /nologo /c /errorReport:prompt

#. Build the Solution.

   This will make `giflib.lib` (or `giflibd.lib`). They'll be in
   `BuildFolder\\giflib-4.1.6\\windows\\giflib\\Release` or
   `BuildFolder\\giflib-4.1.6\\windows\\giflib\\Debug`. Copy them to
   `BuildFolder\\lib`. To avoid confusion (and to match what the
   `leptonlib.vcproj` settings say), rename them following the ClanLib
   naming conventions.  So they should be::

      giflib-static-mtdll.lib or 
      giflib-static-mtdll-debug.lib

#. Copy `giflib-4.1.6\\lib\\gif_lib.h` to `BuildFolder\\include`.

#. To help test `giflib`, the Solution also makes :cmd:`giftext` in the
   same directory that it puts the library. :cmd:`cd` to that directory
   and then run the following command::

      giftext ..\..\..\pic\porsche.gif

   You should see the following::

      ..\..\..\pic\porsche.gif:
              Screen Size - Width = 320, Height = 200.
              ColorResolution = 4, BitsPerPixel = 5, BackGround = 0.
              Has Global Color Map.
      Image #1:
              Image Size - Left = 0, Top = 0, Width = 320, Height = 200.
              Image is Non Interlaced.
              No Image Color Map.
      Gif file terminated normally.


Re-adding `GIF` support to |leptonlib|
======================================

The `include\\leptonica\\environ.h` that is part of the pre-built binary
package already has GIF support enabled. However, if you are building
from the official distribution of |leptonlib| you have to turn on
`giflib` support yourself.

#. Edit `leptonlib-`\ |versionF|\ `\\src\\environ.h`. Change::

      #define  HAVE_LIBGIF      0

   to::

      #define  HAVE_LIBGIF      1

#. Copy the changed `leptonlib-`\ |versionF|\ `\\src\\environ.h` to
   `BuildFolder\\include\\leptonica`.


.. _testing-giflib:

Statically linking with `giflib`
================================

Any applications that statically link with either
`leptonlib-static-mtdll.lib` or `leptonlib-static-mtdll-debug.lib` will
also have to be linked with `giflib` now. This is already done with the
supplied `ioformats_reg` project but we'll demonstrate the process
anyway by building a :guilabel:`LIB Debug` version of `gifio_reg` to
make sure the library was built correctly.

#. See :ref:`using-create-prog-project-addin` to create a Visual Studio
   2008 Project for `leptonlib-`\ |versionF|\ `\\prog\\gifio_reg.c`.

#. In Solution Explorer right-click :guilabel:`gifio_reg`, then choose
   :menuselection:`P&roperties` from the context menu.

#. Set :guilabel:`&Configuration:` to :guilabel:`LIB Debug`.

#. Add `giflib-static-mtdll-debug.lib` to :guilabel:`Configuration
   Properties | Linker | Input | Additional Dependencies`. (You would
   add `giflib-static-mtdll.lib` if you were building :guilabel:`LIB
   Release`)

#. Right-click :guilabel:`gifio_reg` and choose :menuselection:`Set as
   St&artup Project`.

#. Choose :menuselection:`&Build --> B&uild gifio_reg` (:kbd:`Shift+F6`).

#. Choose :menuselection:`&Debug --> &Start Debugging` (:kbd:`F5`).

   A Command Prompt window will pop-up, and show something like the
   following::

      Read time for 8 Mpix 1 bpp:   0.281 sec
      Write time for 8 Mpix 1 bpp:   0.438
      Correct for feyn.tif
         depth: pixs = 1, pix1 = 1
      Correct for weasel2.4g.png
         depth: pixs = 2, pix1 = 2
      Correct for weasel4.16c.png
         depth: pixs = 4, pix1 = 4
      Info in pixEqualWithCmap: colormap sizes are different
      Correct for dreyfus8.png
         depth: pixs = 8, pix1 = 8
      Info in pixEqualWithCmap: colormap sizes are different
      Correct for weasel8.240c.png
         depth: pixs = 8, pix1 = 8
      Correct for test8.jpg
         depth: pixs = 8, pix1 = 8
      Correct for test16.tif
         depth: pixs = 16, pix1 = 8
      Info in pixConvertRGBToColormap: More than 256 colors; using octree quant with dithering
      Correct for marge.jpg
         depth: pixs = 32, pix1 = 8

   And then an IrFanview Thumbnails window will appear showing you a number
   of png's. Hit the :kbd:`Escape` key to close the window and exit the
   program.

.. image:: images/gifio_reg-thumbs.png
   :align: center
   :alt: gifio_reg IrFanview Thumbnail window output


Build |leptonlib|
=================

Since header files may have changed, build |leptonlib| by following
these :ref:`instructions <building-leptonlib>`.

At this point you should build and create `ioformats_reg` by following
the instructions for either the :ref:`command
line<building-prog-programs-commandline>` or :ref:`Visual Studio
2008<building-prog-programs-vs2008>` to make sure all the image
libraries were built successfully.

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

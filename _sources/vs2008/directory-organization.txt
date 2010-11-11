:version: $RCSfile: directory-organization.rst,v $ $Revision: 1ed365cd2585 $ $Date: 2010/11/09 23:18:38 $

.. default-role:: fs

========================
 Directory organization
========================

Unlike Linux where libraries and their dependencies are usually in
consistent places, there is no standard for organizing directories in
Windows. In order to build and link with |leptonlib| this procedure has
to assume one such organization. All required files should reside
within a single directory. This guide calls that directory
|BuildFolder| but you can call it whatever you want, only the
relative placement and names of the subdirectories matter. In
addition, this discussion uses the latest actual directories from the
required libraries at the time this guide was written. You can of
course use different versions and name these directories as you
please.


|BuildFolder| contents
======================

To give an idea of what will be required to build and link with
|leptonlib| using Visual Studio 2008, here's what the complete top-level
contents of |BuildFolder| will need to look like. All the subdirectories
are required if you decide to build the image file libraries
yourself. If you instead opt to use pre-built libraries the
:bi:`italicized` directories can be omitted:

.. parsed-literal::

   BuildFolder
      :bi:`giflib-4.1.6\\`
      include\\
      :bi:`jpeg-8b\\`
      leptonlib-|version|\\
      lib\\
      :bi:`lpng143\\`
      :bi:`tiff-3.9.4\\`
      :bi:`zlib\\`


.. _include-contents:

`BuildFolder\\include` contents
===============================

::

    leptonica\
    gif_lib.h
    jconfig.h 
    jerror.h
    jmorecfg.h
    jpeglib.h
    png.h
    pngconf.h
    tiff.h
    tiffconf.h
    tiffio.h
    tiffvers.h 
    tif_config.h
    zconf.h
    zlib.h


.. _include-leptonica-contents:

`BuildFolder\\include\\leptonica` contents
==========================================

::

    allheaders.h
    alltypes.h
    array.h
    arrayaccess.h
    bbuffer.h
    bmf.h
    bmp.h
    ccbord.h
    dewarp.h
    environ.h
    freetype.h
    gplot.h
    heap.h
    imageio.h
    jbclass.h
    leptprotos.h
    leptwin.h
    list.h
    morph.h
    pix.h
    ptra.h
    queue.h
    readbarcode.h
    regutils.h
    stack.h
    sudoku.h
    watershed.h


.. _lib-contents:

`BuildFolder\\lib` contents
===========================

::

    giflib-static-mtdll.lib
    giflib-static-mtdll-debug.lib
    leptonlib-static-mtdll-debug.lib
    leptonlib-static-mtdll.lib
    leptonlib.dll
    leptonlib.lib
    leptonlibd.dll
    leptonlibd.lib
    libjpeg-static-mtdll-debug.lib 
    libjpeg-static-mtdll.lib
    libpng-static-mtdll-debug.lib
    libpng-static-mtdll.lib
    libtiff-static-mtdll-debug.lib 
    libtiff-static-mtdll.lib
    zlib-static-mtdll-debug.lib
    zlib-static-mtdll.lib

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

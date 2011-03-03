:version: $RCSfile: README.rst,v $ $Revision: 37d6fa039681 $ $Date: 2011/03/02 17:31:30 $

.. default-role:: fs

.. _README:

========
 README
========

:date: Mar 3, 2011

.. contents::
   :local:

::

   /\*====================================================================\*
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
    \*====================================================================\*/

.. parsed-literal::

   gunzip leptonica-|version|.tar.gz
   tar -xvf leptonica-|version|.tar

Building |Leptonica|
====================

Overview
--------

This tar includes:

+ :doc:`src <src-dir>`: library source and function prototypes for
  building `liblept`

+ :doc:`prog <prog-dir>`: source for regression test, usage example
  programs, and sample images

for building on these platforms:

+ Linux on x86 (i386) and AMD 64 (x64)

+ OSX (both powerPC and x86).

+ cygwin and mingw on x86

It should compile properly with any version of gcc from 2.95.3 onward.
There is an additional zip file for building with MS Visual Studio.

Libraries, executables and prototypes are easily made, as described
below.

When you extract from the archive, all files are put in a subdirectory
`leptonica-`\ |versionF|. In that directory you will find a `src/`
directory containing the source files for the library, and a `prog/`
directory containing source files for various testing and example
programs.


.. _building-on-linux:

Building on Linux/Unix/MacOS
----------------------------

There are two ways to build the library:

1. By customization: Use the existing `src/makefile` and customize by
   setting flags in `src/environ.h`.  See `src/environ.h` and
   `src/makefile` for details.

   .. Note:: If you are going to develop with |Leptonica|, I
             encourage you to use the static makefiles.

2. Using :cmd:`autoconf`.  Run :cmd:`./configure` in this directory to
   build `Makefiles` here and in `src`.  Autoconf handles the following
   automatically:

   + architecture endianness

   + enabling |Leptonica| I/O image read/write functions that depend on
     external libraries (if the libraries exist)

   + enabling functions for redirecting formatted image stream I/O to
     memory (on linux only)

   after running::

      ./configure
      make
      make install


In more detail:

.. _building-using-static-makefiles:

1. Customization using the static makefiles:

   + **First Thing**: Run :cmd:`make-for-local`.  This simply
     renames::

        src/makefile.static  -->  src/makefile
        prog/makefile.static -->  prog/makefile

     .. Note:: The :cmd:`autoconf` build will not work if you have any
               files named `makefile` in `src` or `prog`.  If you've
               already run :cmd:`make-for-local` and renamed the static
               makefiles, and you then want to build with
               :cmd:`autoconf`, run :cmd:`make-for-auto` to rename them
               back to `makefile.static`.

   + You can customize for:

     + Including |Leptonica| I/O functions that depend on external
       libraries [use flags in `src/environ.h`]

     + Adding functions for redirecting formatted image stream I/O to
       memory [use flag in `src/environ.h`]

     + Specifying the location of the object code.  By default it goes
       into a tree whose root is also the parent of the `src` and `prog`
       directories.  This can be changed using the ``ROOT_DIR`` variable
       in `makefile`.

   + Build the library:

     + To make an optimized version of the library (in `src`)::

         make

     + To make a debug version of the library (in `src`)::

         make DEBUG=yes debug

     + To make a shared library version (in `src`)::

         make SHARED=yes shared

     + To make the prototype extraction program (in `src`)::

         make   (to make the library first)
         make xtractprotos

   + To use shared libraries, you need to include the location of
     the shared libraries in your ``LD_LIBRARY_PATH``.

   + To make the programs in the `prog` directory, first make
     `liblept` in `src`, and then do :cmd:`make` in the `prog`
     directory.

   **VERY IMPORTANT**: the 190+ programs in the :doc:`prog directory
   <prog-dir>` are an integral part of this package.  These can be
   divided into three types:

   a. Programs that are complete regression tests.  The most
      important of these are named `\*_reg`.  We are in the process
      of standardizing the regression tests, and making it easy to
      write them.  See `regutils.h` for details.

   #. Programs that were used to test library functions or auto-gen
      library code.  These are useful for testing the behavior of
      small sets of functions, and for providing example code.

   #. Programs that are useful applications in their own right.
      Examples of these are the PostScript conversion programs
      `converttops`, `convertfilestops`, `convertsegfilestops`,
      `printimage` and `printsplitimage`.

   :doc:`This <prog-dir>` page summarizes the types and categories of
   files in the `prog` directory, and also gives a short description for
   each file.

.. _building-using-autoconf:

2. Building using :cmd:`autoconf`  (Thanks to James Le Cuirot)

   Use the standard incantation, in the root directory (the
   directory with `configure`)::

      ./configure    [build the Makefile]
      make           [builds the library and shared library 
                      versions of all the progs]
      make install   [as root; this puts liblept.a into /usr/local/lib/
                      and all the progs into /usr/local/bin/ ]

   Configure also supports building in a separate directory from the
   source.  Run :cmd:`/(path-to)/leptonica-`\ |versionC|\
   :cmd:`/configure` and then :cmd:`make` from the desired build
   directory.

   Configure has a number of useful options; run ``configure
   --help`` for details.  If you're not planning to modify the library,
   adding the ``--disable-dependency-tracking`` option will speed
   up the build.  By default, both static and shared versions of the
   library are built.  Add the ``--disable-shared`` or
   ``--disable-static`` option if one or the other isn't needed.

   By default, the library is built with debugging symbols.  If you do
   not want these, use :cmd:`CFLAGS=-O2 ./configure` to eliminate
   symbols for subsequent compilations, or :cmd:`make CFLAGS=-O2` to
   override for this compilation only.


#. Cross-compiling for windows

   You can use `src/makefile.mingw` for cross-compiling in linux.


Building on Windows
-------------------

1. Building with Visual Studio

   Tom Powers has provided a set of developer notes and project files
   for building the library and applications under windows with VC++
   2008/2010:

      :doc:`Microsoft Visual Studio 2008 Developer Notes
      </vs2008/index>`

      :ref:`Microsoft Visual Studio 2008 Solution and Project Files
      <http://tpgit.github.com/UnOfficialLeptDocs/leptonica/source-downloads.html#microsoft-visual-studio-2008>`

   He has also supplied a zip file that contains the entire `lib` and
   `include` directories needed to build Windows-based programs using
   static or dynamic versions of the |Leptonica| library (including
   static library versions of `zlib`, `libpng`, `libjpeg`, `libtiff`,
   and `giflib`).

      :sourceurl:`leptonica-1.68-win32-lib-include-dirs.zip`

#. Building with a static makefile via `MinGW <http://www.mingw.org/>`_
   (Thanks to David Bryan)

   MSYS is a Unix-compatible build environment for the mingw compiler.
   Installing the "MinGW Compiler Suite C Compiler" and the "MSYS Basic
   System" will allow building the library with :cmd:`autoconf` as
   :ref:`above <building-using-autoconf>`.  It will also allow building
   with the static makefile as :ref:`above
   <building-using-static-makefiles>` if this option is added to the
   :cmd:`make` command::

      CC="gcc -D_BSD_SOURCE -DANSI"

   Only the static library may be built this way; the :ref:`autoconf
   method <building-using-autoconf>` must be used if a shared (DLL)
   library is desired.

   :ref:`External image libraries <io-libraries>` must be downloaded
   separately, built, and installed before building the library.
   Pre-built libraries are available from the GnuWin project.

#. Building for `Cygwin <http://cygwin.com/>`_ (Thanks to David Bryan)

   Cygwin is a Unix-compatible build and runtime environment.
   Installing the "Base", "Devel", and "Graphics" packages will allow
   building the library with autoconf as :ref:`above
   <building-using-autoconf>`.  If the graphics libraries are not
   present in the `/lib`, `/usr/lib`, or `/usr/local/lib` directories,
   you must run :cmd:`make` with the ``LDFLAGS=-L/(path-to-image)/lib``
   option.  It will also allow building with the static makefile as
   :ref:`above <building-using-static-makefiles>` if this option is
   added to the make command::

     CC="gcc -ansi -D_BSD_SOURCE -DANSI"

   Only the static library may be built this way; the :ref:`autoconf
   <building-using-autoconf>` method must be used if a shared (DLL)
   library is desired.


.. _io-libraries:

I/O libraries |Leptonica| is dependent on
=========================================

|Leptonica| is configured to handle image I/O using these external
libraries: `libjpeg`, `libtiff`, `libpng`, `libz`, `libgif`, `libwebp`.

These libraries are easy to obtain.  For example, using the debian
package manager::

   sudo apt-get install <package>

where `<package> = {libpng12-dev, libjpeg62-dev, libtiff4-dev}`.

|Leptonica| also allows image I/O with `bmp` and `pnm` formats, for
which we provide the serializers (encoders and decoders).  It also gives
output drivers for wrapping images in PostScript, which in turn use
`tiffg4`, `jpeg` and `png` encoding.

There is also a programmatic interface to :cmd:`gnuplot`.  To use it,
you need only the :cmd:`gnuplot` executable (suggest version 3.7.2 or
later); the `gnuplot` library is not required.

If you build with :cmd:`automake`, libraries on your system will be
automatically found and used.

The rest of this section is for building with the static makefiles.
The entries in `environ.h` specify which of these libraries to use.
The default is to link to these four libraries::

   libjpeg.a  (standard jfif jpeg library, version 6b or 7 or 8))
   libtiff.a  (standard Leffler tiff library, version 3.7.4 or later;
   libpng.a   (standard png library, suggest version 1.4.0 or later)
   libz.a     (standard gzip library, suggest version 1.2.3)
               current non-beta version is 3.8.2)

These libraries (and their shared versions) should be in `/usr/lib`.
(If they're not, you can change the ``LDFLAGS`` variable in the
makefile.)  Additionally, for compilation, the following header files
are assumed to be in `/usr/include`::

   jpeg:  jconfig.h
   png:   png.h, pngconf.h
   tiff:  tiff.h, tiffio.h

If for some reason you do not want to link to specific libraries, even
if you have them, stub files are included for the eight different output
formats (`bmp`, `jpeg`, `png`, `pnm`, `ps`, `tiff`, `gif` and `webp`).
For example, if you don't want to include the `tiff` library, in
`environ.h` set::

   #define  HAVE_LIBTIFF   0

and the stubs will be linked in.

If additionally, you wish to read and write gif files:

1. Download version `giflib-4.1.6` from sourceforge

#. ``#define  HAVE_LIBGIF   1``  (in `environ.h`)

#. If the library is installed into `/usr/local/lib`, you may need to
   add that directory to ``LDFLAGS``; or, equivalently, add that path
   to the ``LD_LIBRARY_PATH`` environment variable.

#. Note: do not use `giflib-4.1.4`: binary comp and decomp
   don't pack the pixel data and are ridiculously slow.

To link these libraries, see `prog/makefile` for instructions on
selecting or altering the ``ALL_LIBS`` variable.  It would be nice to
have this done automatically.

See :ref:`Image I/O <supported-image-file-formats>` for more details on
supported image I/O formats.


Developing with |Leptonica|
===========================

You are encouraged to use the static makefiles if you are developing
applications using |Leptonica|.  The following instructions assume that
you are using the static makefiles and customizing `environ.h`.


Simplicity
----------

For virtually any program you write, you only need::

   #include "allheaders.h"

to include all the function prototypes and struct definitions for the
leptonica library!

It is this simple to write a program using |Leptonica|:

.. code-block:: c

   #include "allheaders.h"
   int main(int argc, char **argv) {
       PIX *pixs, *pixd;
       pixs = pixRead("example.png");
       pixd = pixScale(pixs, 0.35, 0.35);  /* downscale by 0.35 */
       pixWrite("downscaled-example.png", pixd, IFF_PNG);
       pixDestroy(&pixs);
       pixDestroy(&pixd);
       return 0;
   }


`leptprotos.h`
--------------

The prototype header file `leptprotos.h` (supplied) can be automatically
generated using `xtractprotos`. To generate `leptprotos.h`, first make
`xtractprotos` (all in `src`)::

   make  (to make liblept)
   make xtractprotos

Then run it::

   make allprotos   (generates leptprotos.h)

Things to note about `xtractprotos`, assuming that you are developing
in |Leptonica| and need to regenerate the prototype file
`leptprotos.h`:

+ `xtractprotos` is part of |Leptonica|.  You can :cmd:`make` it in
  either `src` or `prog` (see the `makefile`).

+ You can output the prototypes for any C file by running::

     xtractprotos <cfile>     or
     xtractprotos -prestring=[string] <cfile>

+ The source for xtractprotos has been packaged up into a tar
  containing just the |Leptonica| files necessary for building it
  in linux.  The tar file is available at:

     http://www.leptonica.com/source/xtractlib-1.4.tar.gz


GNU runtime functions for stream redirection to memory
------------------------------------------------------

There are two non-standard gnu functions, ``fmemopen()`` and
``open_memstream()``, that only work on linux and conveniently allow
memory I/O with a file stream interface.  This is convenient for
compressing and decompressing image data to memory rather than to
file.  Stubs are provided for all these I/O functions.  Default is
not to enable them, in deference to the OSX developers, who don't
have these functions available.  To enable, ``#define HAVE_FMEMOPEN
1`` (in `environ.h`).  See :ref:`below
<supported-image-file-formats>` for more details on image I/O
formats.

If you're building with the :cmd:`autoconf` programs, these two
functions are automatically enabled if available.


Typedefs
--------

A deficiency of C is that no standard has been universally adopted for
typedefs of the built-in types.  As a result, typedef conflicts are
common, and cause no end of havoc when you try to link different
libraries.  If you're lucky, you can find an order in which the
libraries can be linked to avoid these conflicts, but the state of
affairs is aggravating.

The most common typedefs use lower case variables: ``uint8``, ``int8``,
...  The png library avoids typedef conflicts by altruistically
appending ``png_`` to the type names.  Following that approach,
|Leptonica| appends ``l_`` to the type name.  This should avoid just
about all conflicts.  In the highly unlikely event that it doesn't,
here's a simple way to change the type declarations throughout the
|Leptonica| code:

1. customize a file `converttypes.sed` with the following lines::

      /l_uint8/s//YOUR_UINT8_NAME/g
      /l_int8/s//YOUR_INT8_NAME/g
      /l_uint16/s//YOUR_UINT16_NAME/g
      /l_int16/s//YOUR_INT16_NAME/g
      /l_uint32/s//YOUR_UINT32_NAME/g
      /l_int32/s//YOUR_INT32_NAME/g
      /l_float32/s//YOUR_FLOAT32_NAME/g
      /l_float64/s//YOUR_FLOAT64_NAME/g

#. in the `src` and `prog` directories:

   + if you have a version of :cmd:`sed` that does in-place
     conversion::

        sed -i -f converttypes.sed *

   + else, do something like (in csh)::

        foreach file (*)
        sed -f converttypes.sed $file > tempdir/$file
        end

If you are using |Leptonica| with a large code base that typedefs the
built-in types differently from |Leptonica|, just edit the typedefs in
`environ.h`.  This should have no side-effects with other libraries, and
no issues should arise with the location in which `liblebt` is included.

For compatibility with 64 bit hardware and compilers, where necessary we
use the typedefs in `stdint.h` to specify the pointer size (either 4 or
8 byte).  This may not work properly if you use an ancient gcc compilers
before 2.95.3.


Compile-time control over `stderr` output
-----------------------------------------

|Leptonica| provides some compile-time control over messages and debug
output.  Messages are of three types: error, warning and informational.
They are all macros, and are suppressed when ``NO_CONSOLE_IO`` is
defined on the compile line.  Likewise, all debug output is
conditionally compiled, within a ``#ifndef NO_CONSOLE_IO`` clause, so
these sections are omitted when ``NO_CONSOLE_IO`` is defined.  For
production code where no output is to go to `stderr`, compile with
``-DNO_CONSOLE_IO``.


In-memory raster format (Pix)
-----------------------------

Unlike many other open source packages, |Leptonica| uses packed data
for images with all bit/pixel (bpp) depths, allowing us to process
pixels in parallel. For example, rasterops works on all depths with
32-bit parallel operations throughout.  |Leptonica| is also
explicitly configured to work on both little-endian and big-endian
hardware.  RGB image pixels are always stored in 32-bit words, and a
few special functions are provided for scaling and rotation of RGB
images that have been optimized by making explicit assumptions about
the location of the R, G and B components in the 32-bit pixel. In
such cases, the restriction is documented in the function header.
The in-memory data structure used throughout |Leptonica| to hold the
packed data is a ``PIX``, which is defined and documented in `pix.h`.


Conversion between Pix and other in-memory raster formats
---------------------------------------------------------

If you use |Leptonica| with other imaging libraries, you will need
functions to convert between the ``PIX`` and other image data
structures.  To make a ``PIX`` from other image data structures, you
will need to understand pixel packing, pixel padding, component ordering
and byte ordering on raster lines.  See the file `pix.h` for the
specification of image data in the pix and :doc:`byte-addressing`.


Custom memory management
------------------------

|Leptonica| allows you to use custom memory management (allocator,
deallocator).  For ``PIX``, which tend to be large, the alloc/dealloc
functions can be set programmatically.  For all other structs and
arrays, the allocators are specified in `environ.h`.  Default functions
are ``malloc()`` and ``free()``.  We have also provided a sample custom
allocator/deallocator in `pixalloc.c`.


What's in |Leptonica|?
======================

There is a sortable and searchable categorized list of all the functions
available in |Leptonica| at :doc:`functions` (Warning: this page may
take a long time to load). There are also summaries of the files in the
:doc:`src <src-dir>` and :doc:`prog <prog-dir>` directories with short
descriptions of each file.

Rasterops
---------

This is a source for a clean, fast implementation of
:doc:`rasterops`. Besides reading that page you should also look
directly at the source code. The low-level code is in `roplow.c` and
`ropiplow.c`, and an interface is given in `rop.c` to the simple ``PIX``
image data structure.


Binary morphology
-----------------

This is a source for efficient implementations of
:doc:`binary-morphology` and :doc:`grayscale-morphology`. Besides
reading those pages you should also look directly at the source code.

Binary morphology is implemented two ways:

1. Successive full image rasterops for arbitrary structuring elements
   (Sels)

#. Destination word accumulation (dwa) for specific Sels.  This code is
   automatically generated.  See, for example, the code in
   `fmorphgen.1.c` and `fmorphgenlow.1.c`.  These files were generated
   by running the program `prog/fmorphautogen.c`. Results can be checked
   by comparing dwa and full image rasterops; e.g.,
   `prog/fmorphauto_reg.c`.

Method (2) is considerably faster than (1), which is the reason we've
gone to the effort of supporting the use of this method for all Sels.
We also support two different boundary conditions for erosion.

Similarly, dwa code for the general hit-miss transform can be
auto-generated from an array of hit-miss Sels.  When
`prog/fhmtautogen.c` is compiled and run, it generates the dwa C code in
`fhmtgen.1.c` and `fhmtgenlow.1.c`.  These files can then be compiled
into the libraries or into other programs.  Results can be checked by
comparing dwa and rasterop results; e.g., `prog/fhmtauto_reg.c`.

Several functions with simple parsers are provided to execute a sequence
of morphological operations (plus binary rank reduction and replicative
expansion). See `morphseq.c`.

The structuring element is represented by a simple Sel data structure
defined in `morph.h`.  We provide (at least) seven ways to generate Sels
in `sel1.c`, and several simple methods to generate hit-miss Sels for
pattern finding in `selgen.c`.

In use, the most common morphological Sels are separable bricks, of
dimension n x m (where either n or m, but not both, is commonly 1).
Accordingly, we provide separable morphological operations on brick
Sels, using for binary both rasterops and dwa.  Parsers are provided for
a sequence of separable binary (rasterop and dwa) and grayscale brick
morphological operations, in `morphseq.c`.  The main advantage in using
the parsers is that you don't have to create and destroy Sels, or do any
of the intermediate image bookkeeping.

We also give composable separable brick functions for binary images, for
both rasterop and dwa.  These decompose each of the linear operations
into a sequence of two operations at different scales, reducing the
operation count to a sum of decomposition factors, rather than the
(un-decomposed) product of factors.  As always, parsers are provided for
a sequence of such operations.


Grayscale morphology and rank order filters
-------------------------------------------

We give an efficient implementation of grayscale morphology for brick
Sels.  See :doc:`grayscale-morphology` and the source code.

Brick Sels are separable into linear horizontal and vertical
elements.  We use the :ref:`van Herk/Gil-Werman algorithm
<van-herk-gil-werman>`, that performs the calculations in a time that
is independent of the size of the Sels.  Implementations of tophat
and hdome are also given.  The low-level code is in `graymorphlow.c`.

We also provide grayscale rank order filters for brick filters.
The rank order filter is a generalization of grayscale morphology,
that selects the rank-valued pixel (rather than the min or max).
A color rank order filter applies the grayscale rank operation
independently to each of the (r,g,b) components.


Image scaling
-------------

|Leptonica| provides many simple and relatively efficient
implementations of image scaling.  Some of them are listed here; for
the full set see :doc:`image scaling <scaling>` and the source code.

Grayscale and color images are scaled using:

+ sampling
+ lowpass filtering followed by sampling,
+ area mapping
+ linear interpolation

Scaling operations with antialiased sampling, area mapping, and
linear interpolation are limited to 2, 4 and 8 bpp gray, 24 bpp full
RGB color, and 2, 4 and 8 bpp colormapped (bpp == bits/pixel).
Scaling operations with simple sampling can be done at 1, 2, 4, 8, 16
and 32 bpp.  Linear interpolation is slower but gives better results,
especially for upsampling.  For moderate downsampling, best results
are obtained with area mapping scaling.  With very high downsampling,
either area mapping or antialias sampling (lowpass filter followed by
sampling) give good results.  Fast area map with power-of-2 reduction
are also provided.  Optional sharpening after resampling is provided
to improve appearance by reducing the visual effect of averaging
across sharp boundaries.

For fast analysis of grayscale and color images, it is useful to
have integer subsampling combined with pixel depth reduction.
RGB color images can thus be converted to low-resolution
grayscale and binary images. 

For binary scaling, the dest pixel can be selected from the
closest corresponding source pixel.  For the special case of 
power-of-2 binary reduction, low-pass rank-order filtering can be
done in advance.  Isotropic integer expansion is done by pixel
replication.

We also provide 2x, 3x, 4x, 6x, 8x, and 16x scale-to-gray reduction
on binary images, to produce high quality reduced grayscale images.
These are integrated into a scale-to-gray function with arbitrary
reduction.

Conversely, we have special 2x and 4x scale-to-binary expansion
on grayscale images, using linear interpolation on grayscale
raster line buffers followed by either thresholding or dithering.  

There are also image depth converters that don't have scaling, such
as unpacking operations from 1 bpp to grayscale, and thresholding and
dithering operations from grayscale to 1, 2 and 4 bpp.


Image shear and rotation (and affine, projective, ...)
------------------------------------------------------

:ref:`Image shear <rotation-by-shear>` is implemented with both
rasterops and linear interpolation.  The rasterop implementation is
faster and has no constraints on image depth.  We provide horizontal and
vertical shearing about an arbitrary point (really, a line), both
in-place and from source to dest.  The interpolated shear is used on 8
bpp and 32 bpp images, and gives a smoother result.  Shear is used for
the fastest implementations of rotation.

There are three different types of general image rotators:

1. Grayscale rotation using :ref:`area mapping <rotation-by-area-mapping>`

   + ``pixRotateAM()`` for 8 bit gray and 24 bit color, about center

   + ``pixRotateAMCorner()`` for 8 bit gray, about image UL corner

   + ``pixRotateAMColorFast()`` for faster 24 bit color, about
     center

#. Rotation of an image of arbitrary bit depth, using either 2 or 3
   shears.  These rotations can be done about an arbitrary point, and
   they can be either from source to dest or in-place; e.g.

   + ``pixRotateShear()``

   + ``pixRotateShearIP()``

#. Rotation by sampling.  This can be used on images of arbitrary depth,
   and done about an arbitrary point.  Colormaps are retained.

The area mapping rotations are slower and more accurate, because each
new pixel is composed using an average of four neighboring pixels in the
original image; this is sometimes also called "antialiasing".  Very fast
color area mapping rotation is provided.  The low-level code is in
`rotateamlow.c`.

The shear rotations are much faster, and work on images of arbitrary
pixel depth, but they just move pixels around without doing any
averaging.  The ``pixRotateShearIP()`` operates on the image in-place.

We also provide :ref:`orthogonal rotators <orthogonal_rotations>` (90,
180, 270 degree; left-right flip and top-bottom flip) for arbitrary
image depth.  And we provide implementations of :doc:`affine <affine>`,
projective and bilinear transforms, with both sampling (for speed) and
interpolation (for antialiasing).


Sequential algorithms
---------------------

We provide a number of fast sequential algorithms, including binary and
grayscale :doc:`seedfill <filling>`, and the :ref:`distance function
<distance-function-within-connected-components>` for a binary image.
The most efficient binary seedfill is ``pixSeedfill()``, which uses
Vincent's algorithm to iterate raster- and antiraster-ordered
propagation, and can be used for either 4- or 8-connected fills.
Similar raster/antiraster sequential algorithms are used to generate a
distance map from a binary image, and for grayscale seedfill.  We also
use Heckbert's stack-based filling algorithm for identifying 4- and
8-connected components in a binary image.  A fast implementation of the
:ref:`watershed transform <watershed-transform-seeded-images>`, using a
priority queue, is included.


Image enhancement
-----------------

A few simple :doc:`image enhancement <enhancement>` routines for
grayscale and color images have been provided.  These include intensity
mapping with gamma correction and contrast enhancement, as well as edge
sharpening, smoothing, and hue and saturation modification.

Convolution and cousins
-----------------------

A number of standard image processing operations are also included, such
as :doc:`block convolution <convolution>`, :ref:`binary block rank
filtering <binary-rank-order-and-median-filter-using-accumulator>`,
grayscale and rgb rank order filtering, and edge and local
minimum/maximum extraction.  Generic convolution is included, for both
separable and non-separable kernels, using float arrays in the ``PIX``.


.. _supported-image-file-formats:

Image I/O
---------

Some facilities have been provided for image input and output.  This
is of course required to build executables that handle images, and
many examples of such programs, most of which are for testing, can be
built in the `prog` directory.  Functions have been provided to allow
reading and writing of files in `JPEG`, `PNG`, `TIFF`, `BMP`, `PNM`
`GIF`, and `WEBP` formats.  These formats were chosen for the
following reasons:

+ `JFIF` `JPEG` is the standard method for lossy compression of
  grayscale and color images.  It is supported natively in all
  browsers, and uses a good open source compression library.
  Decompression is supported by the rasterizers in `PS` and `PDF`,
  for level 2 and above.  It has a progressive mode that compresses
  about 10% better than standard, but is considerably slower to
  decompress.  See `jpegio.c`.

+ `PNG` is the standard method for lossless compression of binary,
  grayscale and color images.  It is supported natively in all
  browsers, and uses a good open source compression library (`zlib`).
  It is superior in almost every respect to `GIF` (which, until
  recently, contained proprietary LZW compression). See `pngio.c`.

+ `TIFF` is a common interchange format, which supports different
  depths, colormaps, etc., and also has a relatively good and widely
  used binary compression format (CCITT Group 4).  Decompression of
  G4 is supported by rasterizers in `PS` and `PDF`, level 2 and
  above.  G4 compresses better than `PNG` for most text and line art
  images, but it does quite poorly for halftones.  It has good and
  stable support by Leffler's open source library, which is clean and
  small.  `TIFF` also supports multipage images through a directory
  structure. See `tiffio.c`.

+ `BMP` has (until recently) had no compression. It is a simple
  format with colormaps that requires no external libraries.  It is
  commonly used because it is a Microsoft standard, but has little
  besides simplicity to recommend it. See `bmpio.c`.

+ `PNM` is a very simple, old format that still has surprisingly wide
  use in the image processing community.  It does not support
  compression or colormaps, but it does support binary, grayscale and
  rgb images.  Like `BMP`, the implementation is simple and requires
  no external libraries.  See `pnmio.c`.

+ `GIF` is still widely used in the world.  With the expiration of
  the LZW patent, it is practical to add support for `GIF` files.
  The open source `GIF` library is relatively incomplete and
  unsupported (because of the Sperry-Rand-Burroughs-Univac patent
  history). See `gifio.c`.

+ `WEBP <http://code.google.com/speed/webp/>`_ is a new wavelent
  encoding method derived from `libvpx
  <http://www.webmproject.org/code/#libvpx_the_vp8_codec_sdk>`_, a video
  compression library.  |Leptonica| provides an interface through webp
  into the underlying codec.  You need to download `libvpx`, `libwebp`
  and `yasm <http://www.tortall.net/projects/yasm/wiki/Download>`_.

Here's a summary of compression support and limitations:

+ All formats except `JPEG` support 1 bpp binary.

+ All formats support 8 bpp grayscale (`GIF` must have a colormap).

+ All formats except `GIF` support 24 bpp rgb color.

+ All formats except `PNM` support 8 bpp colormap. 

+ `PNG` and `PNM` support 2 and 4 bpp images.

+ `PNG` supports 2 and 4 bpp colormap, and 16 bpp without colormap.

+ `PNG`, `JPEG`, `TIFF` and `GIF` support image compression; `PNM`
  and `BMP` do not.

+ `WEBP` supports **only** 24 bpp rgb color.

Use `prog/ioformats_reg` for a regression test on all but `GIF` and
`WEBP`.  Use `prog/gifio_reg` for testing `GIF`.

We provide wrappers for `PS` output, from all types of input
images.  The output can be either uncompressed or compressed with
level 2 (ccittg4 or dct) or level 3 (flate) encoding.  You have
flexibility for scaling and placing of images, and for printing at
different resolutions.  You can also compose mixed raster (text,
image) `PS`.  See `psio1.c` for examples of how to output `PS` for
different applications.  As examples of usage, see:

+ `prog/converttops.c` for a general image --> PS conversion for
  printing. You can specify compression level (1, 2, or 3).

+ `prog/convertfilestops.c` to generate a multipage level 3
  compressed `PS` file that can then be converted to pdf with
  :cmd:`ps2pdf`.

+ `prog/convertsegfilestops.c` to generate a multipage, mixed
  raster, level 2 compressed `PS` file.

We provide wrappers for PDF output, again from all types of input
images.  You can do the following for PDF:

+ Put any number of images onto a page, with specified input resolution,
  location and compression.

+ Write a mixed raster PDF, given an input image and a segmentation
  mask.  Non-image regions are written in G4 (fax) encoding.

+ Concatenate single-page PDF wrapped images into a single PDF file.

+ Build a PDF file of all images in a directory or array of file names.

.. note:: Any or all of these I/O library calls can be stubbed out at
          compile time, using the environment variables in
          `environ.h`.

For all formatted reads and writes, we support read from memory and
write to memory.  (We cheat with `GIF`, using a file intermediary.)

For all formats except for `TIFF`, these memory I/O functions are
supported through ``open_memstream()`` and ``fmemopen()``, which only
is available with the gnu C runtime library (`glibc`).  Therefore,
except for `TIFF`, you will not be able to do memory supported
read/writes on these platforms:

   OSX, Windows, Solaris

By default, these non-POSIX functions are disabled.  To enable memory
I/O for image formatted read/writes, see `environ.h`.


Colormap removal and color quantization
---------------------------------------

|Leptonica| provides functions that remove colormaps, for conversion to
either 8 bpp gray or 24 bpp RGB.  It also provides the inverse function
to colormap removal; namely, color quantization from 24 bpp full color
to 8 bpp colormap with some number of colormap colors.  Several versions
are provided, some that use a fast octree vector quantizer and others
that use a variation of the median cut quantizer.  For high-level
interfaces, see for example: ``pixConvertRGBToColormap()``,
``pixOctreeColorQuant()``, ``pixOctreeQuantByPopulation()``,
``pixFixedOctcubeQuant256()``, and ``pixMedianCutQuant()``.


Programmatic image display
--------------------------

For debugging, several ``pixDisplay*()`` functions in `writefile.c` are
given.  Two (``pixDisplay()`` and ``pixDisplayWithTitle()``) can be
called to display an image using one of several display programs
(:cmd:`xv`, :cmd:`xli`, :cmd:`xzgv`, :cmd:`l_view`).  If necessary to
fit on the screen, the image is reduced in size, with 1 bpp images being
converted to grayscale for readability.  (This is much better than
letting :cmd:`xv` do the reduction).  Another function,
``pixDisplayWrite()``, writes images to disk under control of a
reduction/disable flag, which then allows either viewing with
``pixDisplayMultiple()``, or the generation of a composite image using,
for example, ``pixaDisplayTiledAndScaled()``.  These files can also be
gathered up into a compressed PostScript file, using
`prog/convertfilestops`, and viewed with :cmd:`evince`, or converted to
pdf.  Common image display programs are: :cmd:`xv`, :cmd:`display`,
:cmd:`gthumb`, :cmd:`gqview`, :cmd:`xli`, :cmd:`evince`, :cmd:`gv`,
:cmd:`xpdf` and :cmd:`acroread`.  The |Leptonica| program :cmd:`xvdisp`
generates nice quality images for display with :cmd:`xv`.  Finally, a
set of images can be saved into a ``PIXA`` (array of ``PIX``),
specifying the eventual layout into a single ``PIX``, using
``pixSaveTiled*()``.


.. _readme-document-image-analysis-applications:

Document image analysis
-----------------------

Some functions have been included specifically to help with
:doc:`document image analysis <document-image-analysis>`.  These include
:doc:`skew <skew-measurement>` and text orientation detection; page
segmentation; baseline finding for text; unsupervised classification of
connected components, characters and words; :doc:`dewarping camera
images <dewarping>`, and digit recognition.


Data structures
---------------

Simple data structures are provided for safe and efficient handling of
arrays of numbers, strings, pointers, and bytes.  The generic pointer
array is implemented in four ways: as a stack, a queue, a heap (used to
implement a priority queue), and an array with insertion and deletion,
from which the stack operations form a subset.  Byte arrays are
implemented both as a wrapper around the actual array and as a queue.
The string arrays are particularly useful for both parsing and composing
text.  Generic lists with doubly-linked cons cells are also provided.


Examples of programs that are easily built using the library
------------------------------------------------------------

+ for plotting x-y data, we give a programmatic interface
  to the gnuplot program, with output to X11, png, ps or eps.
  We also allow serialization of the plot data, in a form
  such that the data can be read, the commands generated,
  and (finally) the plot constructed by running gnuplot.

+ a simple :doc:`jbig2-type classifier <jbig2>`, using various
  distance metrics between image components (correlation, rank
  hausdorff); see `prog/jbcorrelation.c`, `prog/jbrankhaus.c`.

+ a simple :doc:`color segmenter <color-segmentation>`, giving a
  smoothed image with a small number of the most significant colors.

+ a program for converting all `TIFF` images in a directory to a
  PostScript file, and a program for printing an image in any
  (supported) format to a PostScript printer.

+ converters between binary images and SVG format.

+ a bitmap font facility that allows painting text onto images.  We
  currently support one font in several sizes.  The font images and
  postscript programs for generating them are stored in
  `prog/fonts/`.

+ a binary maze game lets you generate mazes and find shortest
  paths between two arbitrary points, if such a path exists.
  You can also compute the "shortest" (i.e., least cost) path
  between points on a grayscale image.

+ a 1D barcode reader.  This is in an early stage of development,
  with little testing, and it only decodes 6 formats.

+ a utility that will :doc:`dewarp images of text <dewarping>` that
  were captured with a camera at close range.

+ a sudoku solver, including a pretty good test for uniqueness.

+ see :ref:`above <readme-document-image-analysis-applications>` for
  other document image applications.


JBig2 encoder
-------------

|Leptonica| supports an open source `jbig2` encoder (yes, there is
one!), which can be downloaded from:

   http://github.com/agl/jbig2enc.

To build the encoder, use the most recent version.  This bundles
|Leptonica| 1.63.  Once you've built the encoder, use it to compress
a set of input image files (e.g.)::

   ./jbig2 -v -s <imagefile1 ...>  >  <jbig2_file>

You can also generate a `pdf` wrapping for the output `jbig2`.  To do
that, call :cmd:`jbig2` with the ``-p`` arg, which generates a symbol
file (`output.sym`) plus a set of location files for each input image
(`output.0000`, ...)::

   ./jbig2 -v -s -p <imagefile1 ...>

and then generate the `pdf`::

   python pdf.py output  >  <pdf_file>

See the usage documentation for the `jbig2` compressor at:

   http://github.com/agl/jbig2enc

You can uncompress the `jbig2` files using :cmd:`jbig2dec`, which can
be downloaded and built from:

   http://jbig2dec.sourceforge.net/


Versions
========

New versions of the |Leptonica| library are released approximately 6
times a year, and version numbers are provided for each release in the
`makefile` and in `allheaders.h`.  Version numbers are also available
programatically via the functions ``getLeptonicaVersion()`` (in
`utils.c`) and ``getImagelibVersions()`` (in `libversions.c`). All even
versions from 1.42 to 1.60 are archived at
http://code.google.com/p/leptonica, as well as all versions after 1.60.

A brief version chronology is maintained in :doc:`version-notes`.
Starting with gcc 4.3.3, error warnings (``-Werror``) are given for
minor infractions like not checking return values of built-in C
functions.  I have attempted to eliminate these warnings.  In any event,
you can expect some warnings with the ``-Wall`` flag.

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

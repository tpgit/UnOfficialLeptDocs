:version: $RCSfile: library-overview.rst,v $ $Revision: 9b4bc79ae714 $ $Date: 2010/04/03 08:37:01 $

.. default-role:: fs

===================================
 Overview of the Leptonica Library
===================================

:date: March 27, 2005 -- **Under construction!**

Introduction
============

First, if you haven't already done so, read the :ref:`README`.

A set of web pages is provided for many of the fundamental imaging
operations in the library. These describe the underlying algorithmic
details, as well as some of the implementations to be found in
leptonica.

After you read this file, you may find that a more detailed
:ref:`description <library-notes>` of the contents of the leptonica
library is helpful. This is also a guide to programs in the `/prog`
directory, containing regression tests and other scripts for testing and
demonstrating the library functions.

These various descriptions (README, library overview, web pages on
algorithms, library notes) have been written because the leptonica
library covers a wide array of tools for both image processing and image
analysis, including fundamental imaging operations, affine transforms,
rendering techniques, I/O, and a number of examples of useful
applications, such as color quantization, jbig2 classification, document
image deskew and segmentation, PostScript wrapping for various print and
display applications, etc. If you are to use leptonica effectively, you
need to be aware of these diverse functions.

If anything is not clear in these descriptions, it should help to scan
the source code, which is the final arbiter. I have made an attempt to
document the code sufficiently so that if you know what it is supposed
to do, you will be able to understand all the implementation details.

Leptonica has a very small number of data structures, and a relatively
large number of operations on them. We use an object-oriented approach
throughout. The data structures go through a life-cycle where they are
created, acted upon, and destroyed. Implementation is through functions
whose name typically begins with the name of the primary data structure
involved. We attempt to follow a set of :ref:`design principles
<design-principles>` that make the code as safe, portable and
transparent to use as possible (with C). For writing your own
applications, you should find it useful to look at the programs in the
`prog` directory, which were written to test functions in the
library. Most of these have been run through `valgrind
<http://valgrind.org/>`_, and I strongly encourage you to use valgrind
on your applications. You may also want to look at a description of some
of the :ref:`testing methods <testing-methods>` we have used in
Leptonica.

The functions are divided into two libraries: a high-level one that uses
the sparse set of data structures such as ``Pix``, ``Box``, etc., and a
low-level library that uses only intrinsic C data types. When you build
the libraries, you also make a single library that combines both of
these. The low-level library file names have "low" appended to the name
of the corresponding high-level file. The function names also follow a
pattern: the low-level function name is generated from the high-level
function by removing the object prefix and appending "Low".  For
example, ``pixScaleToGray4()`` calls ``scaleToGray4Low()`` to do the
work.  When a data structure is aggregated into an array, the name of
the struct has an "a" appended. For example, the struct ``Pixa``
contains an array of struct ``Pix``.


Reading and writing images
==========================

Before you can do anything with images, you need to be able to read and
write them. Of the large number of image formats in existence, we
support a small set that are the most useful. Some like BMP and PNM are
very simple, but the most important support compressed file formats with
open libraries. These include the two formats supported by all browsers,
PNG and (JFIF) JPEG. There is also TIFF-wrapped CCITT-G4 compression,
which, for some strange reason is not supported by browsers. Note that
Leptonica doesn't support GIF, because the specific universal
compression scheme it uses (LZW) has until recently been covered by
patents that Burroughs-Sperry-Rand attempted to enforce. You'll also
find that PNG, which uses gzip compression in libz, is usually about 10%
more efficient than GIF, and the Burrows-Wheeler encoder used in bzip2
is better still.

Most of the fileio functions can be found in `readfile.c` and
`writefile.c`. The top-level functions are ``pixRead()`` and
``pixWrite()``.  Specific encoders are supported by functions in files
that end in "`io.c`". These functions, most of which use streams for
I/O, are the link between our image data structure, the ``Pix``, and the
low-level code that reads and writes the image data. There are also
special high-level functions. For example, `tiffio.c` has functions for
reading and writing files containing multiple images and writing files
with special tiff tags embedded in the header. See `prog/mtifftest.c`
for examples. Also, `jpegio.c` has a function that reads jpeg files,
optionally converting RGB to 8 bpp with a colormap, reducing by a power
of 2, and returning warnings if the compressed data is corrupted.

Additionally, you can write PostScript files in a variety of formats,
both level 1 (uncompressed) and level 2 (using DCT aka JPEG) and
CCITT-G4 compression with the option to paint through the binary mask.
This is implemented in `psio.c`, where you will find a number of
functions that support these two compressed formats, as well as as the
ascii85 error-correction encoder that encodes 4 bytes of binary data
into 5 bytes of ascii. See `prog/psiotest.c` for examples.

What about reading PostScript files into raster images? Fortunately, we
have Aladdin's ghostscript to do this. I have put several bash scripts
in `prog`, such as :cmd:`ps2png`, that use ghostscript with various
output devices to convert a PostScript file to a set of compressed image
files, one file per page. PDF files are also easily generated from
PostScript using Aladdin's :cmd:`ps2pdf`, which is a shell script that
also runs ghostscript with the appropriate output device.


Affine transforms
=================

Affine transforms are linear transformations that generate coordinates
in the dest image (x', y') from those in the source (x, y). Three
corresponding points in the source and dest are sufficient to specify
the affine transform completely. There are thus 3 linear equations, with
6 coefficients. The set of affine transforms is {translation, rotation,
shear, scaling}, and any set of those 6 coefficients is equivalent to an
instance of this set. It is actually a surprising amount of work to
implement all these transforms efficiently on images of various pixel
depths, including RGB, and we have tutorial pages for each of these
transforms. Translation is a special case of rasterops, which is
described in detail because of its universal importance in image
composition and analysis. Rotation can be implemented by three shears,
and, for small angles, approximated by two shears. Shear is efficiently
implemented with rasterops, as a set of translations. Scaling here can
be anisotropic, with different scaling factors in orthogonal
directions. We give a quick overview here, leaving the details for the
specific pages... 


Rasterops
---------

Rasterops is the single most useful image processing function. It
performs an arbitrary logical operation between two rectangles of source
and dest images, storing the result in the dest image. See the
:ref:`rasterops page <rasterops>` to understand how it is used for many
different purposes, such as image composition, display, translation,
binary morphology, etc. It works on images of arbitrary depth, and does
the minimum clipping required to stay within the allocated rasters. The
high-level interface to rasterops is implemented in `rop.c`. The general
function ``pixRasterop()`` takes nine arguments: 5 for the dest image
and rectangle, 3 for the source image and rectangle corner to be used,
and 1 to specify the actual operation. Simple translation can be done
either between a source and dest image using the general function, or
in-place using ``pixRasteropIP()``.

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

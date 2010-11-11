:version: $RCSfile: library-notes.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _library-notes:

=========================================
 Supplemental Notes on Using the Library
=========================================

:date: August 26, 2006 -- **Still under construction**

First, read the :ref:`README` to get an overview of what is available and how
to use it.

This supplements that information in particular areas.


I/O: File read/write
====================

(ref: section 12 of the :ref:`README`)

When building programs, it is often important to look at images. The
function

.. sourcecode:: c

   pixWrite(char *filename, PIX *pix, l_int32 format)

writes an image to a file. See any of the programs in the `prog`
directory for examples. You can display this image with a variety of
programs, such as :cmd:`xv` (which scales the image automatically to fit
on the screen), :cmd:`display` (which displays at full resolution),
:cmd:`gqview` (which displays at full resolution and allows easy
zooming), and :cmd:`gimp` (which is set up for image manipulation and
displays by default at low resolution). For programmatic display with
:cmd:`xv`, we provide a function

.. sourcecode:: c

   pixDisplay(PIX *pix, l_int32 x, l_int32 y)

which scales the image to fit on the screen if necessary and then
displays it with the UL corner at (x, y).

Images are read into memory from a file using

.. sourcecode:: c

   PIX *pixRead(char *filename)

For the file formats that are supported (PNG, JFIF_JPEG, TIFF (various
compressions), PNM and BMP), the extension (if any) is ignored and the
format type is determined from the file itself.

**Regression test:** `prog/ioformats.c`


The Pix data structure
======================

The ``Pix`` data structure is the internal (memory) representation of
images in this library. It is very simple, and is described in `pix.h`,
along with some of the flags and other data structures that are
associated with it. The field accessors for ``Pix``, provided in
`pix1.c`, should ALWAYS be used. The ``pixClone()`` function is used to
get a new handle (pointer) to the same ``Pix`` data structure, without
actually copying the image data to a new array. The ``pixDestroy(PIX
**)`` function should be used on every handle you have --- see the
comments in `pix1.c` at the ``pixClone()`` definition.

Throughout we use these definitions:

   bpp
      bits/pixel  (leptonica supports 1, 2, 4, 8, 16 and 32)
   ppi
      pixels/inch  (resolution of image relative to original scanned page)
   src
      source image in image processing operation
   dest
      destination image in image processing operation

A ``Pix`` can also have a colormap, and we support a number of
operations on colormaps in `colormap.c`. Colormapped images can have
depths of 1, 2, 4 or 8 bpp. Where appropriate, functions will handle
both colormapped and non-colormapped ``Pix``. Functions that use
interpolation, such as grayscale or color area-mapping rotation, will
make a temporary image without the colormap, and use that to compute the
dest ``Pix``, which will then not have a colormap. It should be noted
that except for in-place functions, the src ``Pix`` is never altered.

Except for RGB images, all pixels in a ``Pix`` are packed (the pixels
are represented as compactly as possible without compression). Each
raster line is 32-bit aligned. See the comments in `pix.h` that describe
the constraints and conventions for the image data representation. RGB
images are packed into 32 bits, leaving 8 bits for an alpha channel that
is not used.


Rasterops
=========

A fundamental imaging operation, this is an operation that takes a
rectangular region of one image and combines it with a rectangular
region of a second image, using one of 12 boolean operations, and
writing the result into the second image. The 12 operations between two
images are described in detail in `rop.c`.

There are also in-place rasterops, where a rectangular region of a
single image is painted according to its (shifted) values. The in-place
rasterops can be used to translate a full image, or a vertical or
horizontal band of the image. The latter are used to shear the image;
e.g., a horizontal shear is implemented by shifting full-width bands
horizontally, as described in `shear.c`. With in-place rasterops, one
must be careful not to overwrite data that will be used later.

All rasterops operate on images of any depth, and they are automatically
clipped to the respective images to avoid illegal reads and writes.
They have a large number of uses, including a relatively fast
implementation of binary morphology (for 1 bpp images). For examples and
details, see also the writeup at :ref:`rasterops`.


Scaling
=======

A large variety of efficient scaling functions can be found in
`scale.c`, many of which are described in :doc:`scaling`. The generic
function, ``pixScale()``, does the best job given the image type and the
scaling factors. The best upscaling is typically done with linear
interpolation, and the best downscaling is done either with a lowpass
filter followed by subsampling, or by area mapping. The former is a fast
anti-aliased approximation, particularly for small scaling factors
(i.e., large downscaling). The area mapping method integrates with
subpixel accuracy over the region of the src image that corresponds to
each dest pixel.

Some of the other fast scaling operations given in `scale.c` are:

+ sampling: ``pixScaleBySampling()``
+ 2x and 4x linear interpolation upscaling for gray and color images:
  e.g., ``pixScaleColorLI()``
+ integer subsampling of RGB to gray or binary; e.g.,
  ``pixScalRGBToGrayFast()``
+ antialias lowpass filter downscaling: ``pixScaleSmooth()``
+ antialias area-mapping downscaling: ``pixScaleAreaMap()``
+ antialias downscaling from RGB to gray by 2x: ``pixScaleRGBToGray2()``
+ downscaling 1 bpp images to 8 bpp gray by several downscaling
  factors (2, 3, 4, 6, 8, 16): ``pixScaleToGray()``
+ binary scaling by pixel sampling: ``pixScaleBinary()``
+ mipmap pyramid downscaling 1 bpp images to 8 bpp gray:
  ``pixScaleToGrayMipmap()``
+ mipmap pyramid gray downscaling: ``pixScaleMipmap()``
+ gray upscaling by 2x or 4x, followed by binarization using a
  threshold: e.g., ``pixScaleGray2xLIThresh()``
+ gray upscaling by 2x or 4x, followed by binarization using
  dithering: e.g., ``pixScaleGray2xLIDither()``

Special fast scaling on binary images is also available, and is useful
for image analysis of scanned binary text. Examples are:

+ in `binreduce.c`, 2x reduction of 1 bpp images using either
  subsampling or rank filtering: e.g., ``pixReduceRankBinary2()``
+ in `binexpand.c`, power-of-2 replicative expansion of 1 bpp images:
  ``pixExpandBinary()``

**Some scaling scripts**:

+ `prog/scaletest1.c`: different general scaling functions
+ `prog/scaletest2.c`: multiple tests of scale-to-gray; color scaling
  tests.
+ `prog/reducetest.c`: rank binary cascade of up to four 2x reductions.
+ `prog/expandtest.c`: power-of-2 replicative expansion.

**Regression test:** `prog/scaletest3.c`


Rotation
========

Rotation seems mundane, but there are in fact a large number of ways of
doing it, some of which are described in :doc:`rotation`. The top-level
general rotator is ``pixRotate()`` in `rotate.c`. Here's the description
from the source file:

   ::

      The general rotation pixRotate() does the best job for
      rotating about the image center.  For 1 bpp, it uses shear;
      for others, it uses either shear or area mapping.
      If requested, it expands the output image so that no pixels are
      lost in the rotation, and this can be done on multiple
      successive shears without expanding beyond the maximum
      necessary size.
            

There are three other top-level rotation source files, each of which
uses different methods for different purposes:

+ `rotateshear.c`: This has the top-level ``pixRotateShear()`` to do
  rotation by either 2 or 3 shears about an arbitrary point. This is
  very fast, being implemented by a sequence of rasterops, and works for
  images of all depths, including colormapped. An in-place version is
  also implemented, using in-place rasterops to perform the in-place
  shear operations.

+ `rotateam.c`: This has the top-level ``pixRotateAM()`` to do area
  mapping rotation about the image center for grayscale and color
  images. It also has a similar function, ``pixRotateAMCorner()`` for
  rotating about the UL corner.

+ `rotateorth.c`: This has the top-level functions for 90 and 180 degree
  rotation, ``pixRotate90()`` and ``pixRotate180()``, along with LR and
  TB flipping, ``pixRotateLR()`` and ``pixRotateTB()``, using LUTs when
  feasable.

**Some rotation scripts**:

+ `prog/rotatetest1.c`: selection of different rotations, including
  successive rotations with unwinding.

+ `prog/rotateorthtest1.c`: various orth rotations, with timing and
  other tests.

**Regression tests:**

+ `prog/rotatetest2.c`
+ `prog/rotateorthtest2.c`


Shear
=====

Image shear is another special linear transform in the plane. It can be
used to approximate a continuous rotation, using either 2 shears (for
small angles) or 3 shears. Because it is implemented with rasterops, it
is both very fast and it works for all depths. For its use in rotation,
see :doc:`rotation`.

Shear can be performed either with src and dest, or in-place. The latter
uses in-place rasterops. Vertical shear is used in the implementation of
the skew angle finder. The definition of the shear transform is given in
:doc:`affine`.

**Some scripts using shear**:

+ `prog/rotatetest1.c`: includes timing for various rotation by shear.

+ `prog/sheartest.c`: various shear operations about arbitrary lines,
  both between src and dest and in-place.


Affine, projective and bilinear transforms
==========================================

Affine transforms are the most general linear transforms in a
plane. They are specified by 3 corresponding points (i.e., 6
coefficients) in the two coordinate spaces. They can be implemented both
in a pointwise fashion (with or without interpolation) and as a set of
successive special linear transforms (translation, scaling, shear). We
provide an example of the latter, but its use in applications is
deprecated; in all situations you should use the pointwise
transforms. See the code in `affine.c` for details.

Projective and bilinear transforms are more general, nonlinear, 4-point
transforms in the plane, and they are specified by 8 coefficients. The
implementations are in `projective.c` and `bilinear.c`,
respectively. Whereas affine transforms keep straight lines straight and
preserve parallel lines, projective transforms only keep straight lines
straight. And bilinear transforms do not even preserve straight
lines. Affine transforms project a 3-dimensional scene onto a plane at
infinity, whereas projective transforms view the 3-D scene at a finite
distance, so that lines that are parallel in the affine transform all
meet at a 'vanishing point' in the projective transform. For example,
projective transforms can remove "keystoning" in an object imaged by a
camera at close range. See :doc:`affine` for details.

**Some scripts using 3- and 4-point transforms**:

+ `prog/affinetest.c`: basic affine transform tests, plus a comparison
  between pointwise and sequential implementations.

+ `prog/projectivetest.c`: compares sampled and interpolated projective
  transforms; i.e., ``pixProjectiveSampled()`` and
  ``pixProjectiveInterpolated()``. Sampled transforms use, for each dest
  pixel, the closest pixel in the src, whereas interpolated transforms
  take a weighted average of four src pixels for each dest pixel. For 1
  bpp images, only sampled can be used; for images with depth > 1,
  interpolation is slower but gives better results.

+ Likewise, `prog/bilineartest.c` compares sampled and interpolated
  bilinear transforms; i.e., ``pixBilinearSampled()`` and
  ``pixBilinearInterpolated()`` transforms.


Binary morphology
=================

Bin morph ...


Grayscale morphology
====================

Bin morph ...


Block convolution
=================

Block convolution is my term for a convolution, applied to a grayscale
image, using a rectangular kernel with constant value. For this case,
the so-called "integral image" formulation can be used to compute the
convolution in a time that is independent of the size of the convolving
kernel. To do this, it is necessary to precompute an accumulation matrix
from which each value in the dest can be computed by adding (or
subtracting) four entries in the matrix. For details, see range. See
:doc:`convolution`. Using the same technique, it is also possible to
apply a rank order filter with a rectangular kernel to binary images,
again in a time independent of the size of the kernel.


Connected components
====================

Conn comps ...

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

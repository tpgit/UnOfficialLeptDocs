:version: $RCSfile: affine.rst,v $ $Revision: f1256d0ba63d $ $Date: 2010/08/28 08:54:39 $

.. default-role:: math

.. Speed up Internet Explorer 8's handling of MathJax
.. meta::
   :http-equiv=X-UA-Compatible: IE=EmulateIE7

.. _affine-transformations:

====================================
Affine Transformations (and cousins)
====================================

:date: Aug 10, 2006

.. contents::
   :local:


What is an affine transformation?
=================================

An *affine transformation* is the most general linear transformation
on an image:

.. math::
   :label: general-linear-transformation

   \begin{align}
   x' &= ax + by + c\\ 
   y' &= dx + ey + f\\ 
   \end{align}

or in (transposed) matrix notation:

.. math::
   :label: matrix-form
    
   \begin{bmatrix}
     x'& y'
   \end{bmatrix}
   = 
   \begin{bmatrix}
     x & y & 1
   \end{bmatrix} \, T

where T is a 3x2 matrix of coefficients:

.. math::
   :label: T
    
   T = \begin{bmatrix}
         a & d \\
         b & e \\
         c & f
       \end{bmatrix}

There are a couple of ways this can be visualized geometrically. If
you look at a two-dimensional surface (coordinate system) from a great
distance with arbitrary orientation in the third dimension, you will
see that any object in the two-dimensional surface appears to be
distorted by a combination, in general, of translation, shear and
scaling. So an affine transformation takes any coordinate system in a
plane into another coordinate system that can be found from such a
projection. Under affine transformation, parallel lines remain
parallel and straight lines remain straight.

Consider this transformation of coordinates. A coordinate system (or
*coordinate space*) in two-dimensions is defined by an origin, two
non-parallel axes (they need not be perpendicular), and two scale
factors, one for each axis. This can be described by 3 points, one for
the origin and one for the unit distance along each of the two axes.  It
takes six numbers to specify three points. Suppose we have these three
points: `(x_1, y_1)`, `(x_2, y_2)` and `(x_3, y_3)`. Then given an
affine transformation as above, we can find the corresponding three
transformed points from:

.. math::
   :label: 3pt-transformation

   \begin{align}
   x'_1 &= ax_1 + by_1 + c \\
   y'_1 &= dx_1 + ey_1 + f \\
   x'_2 &= ax_2 + by_2 + c \\
   y'_2 &= dx_2 + ey_2 + f \\
   x'_3 &= ax_3 + by_3 + c \\
   y'_3 &= dx_3 + ey_3 + f
   \end{align}

Conversely, if we are given the three points in the transformed (primed)
coordinate space that correspond to the three unprimed points, we could
solve the set of 6 equations in :eq:`3pt-transformation` for the six
coefficients. These coefficents could then be used in
:eq:`general-linear-transformation` to transform any point in the
original coordinate space to its location in the primed coordinate
space.


How are affine transformations implemented?
===========================================

There are two very different approaches to implement an affine
transformation on an image:

#. **Pointwise.** Each point in the dest is determined from the
   corresponding point in the src. We start with 3 points specifying the
   initial coordinate space and the 3 corresponding points that specify
   the transformed coordinate space, and transform an entire image
   pointwise by the transformation :eq:`general-linear-transformation`.

#. **Sequential.** The entire image is successively transformed by a
   sequence of shear, scale and translation operations.

In practice, the pointwise approach is the most useful. For each dest
pixel, the corresponding src pixel (or pixels) are located, and the
dest pixel value is computed.

For binary images, the *pointwise* transform is about 3 times slower
than the *sequential* transform, whereas for grayscale images the
pointwise transform is an order of magnitude faster! However, of more
importance, the results, particularly on text, are far better with the
pointwise transform. The sequential transform involves a number of
shears, which cause visible dislocation lines through characters.
After such a set of sequential transforms, the edges, that were
initially smooth, become irregular, significantly degrading the visual
quality of the text. The pointwise transform has a minimal number of
such artifacts, and any shear lines that are developed tend to have
shorter spatial correlation. It is thus strongly urged that *in any
situation where the quality of the resulting text image is important,
the pointwise transformation should be used.*

The following image fragments show the image quality resulting from
the same affine transformation. The first fragment has been done
pointwise, whereas the second one was done sequentially.

.. figure:: figs/pointwise-affine.png
   :align: center
   :alt: Pointwise affine transformation
   :class: border

   Figure 1 -- Pointwise Affine Transformation

.. figure:: figs/sequential-affine.png
   :align: center
   :alt: Sequential affine transformation
   :class: border

   Figure 2 -- Sequential Affine Transformation

See the documentation in :fs:`affine.c`, where it is shown that the
pointwise transformation should be performed *backwards*, so that for
every point in the (primed) dest, you find the corresponding point in
the (unprimed) src. For binary images, the implementation is slower in
the backwards direction, because you have to find the corresponding
point in the src for *every* point in the dest, whereas going in the
forward direction, you only write to the dest when the src pixel is
ON. However, the forward direction implementation can miss some pixels
entirely in the dest. When a solid black region is transformed, this
will in general result in a regular pattern of white pixels within it,
even when no overall scaling is done.

With the affine transform, as with the :ref:`projective
<affine-projective-transform>` and :ref:`bilinear transforms
<affine-bilinear-transform>`, the pointwise transform can be done for
all pixel depths by *sampling*. For 8 bpp and RGB images, better results
are obtained, particularly on document images that have sharp edges,
using *interpolation*. Interpolation involves subdividing the src pixels
into subpixels (we divide each into 16 x 16 subpixels), and using the
subpixel location to generate weighting factors for the four neighboring
src pixels. Interpolation is about 5x slower than sampling the nearest
src pixel. When there is relatively little scale change, interpolation
is nearly equivalent to area mapping, as we have shown with
:ref:`rotation <rotation-by-area-mapping>`.


Sequential affine transform
---------------------------

We now describe the situation where the affine transform is performed as
a sequence of translations, scalings, shears and, optionally,
rotations. Because a rotation is equivalent to :ref:`three shears
<rotation-by-shear>`), we need in principle only translations, scaling
and shear. We have already demonstrated that there are 6 independent
parameters in the affine transformation. This can also be seen from the
transformation from one coordinate space to another. There are 2
parameters to align the origins, 2 parameters for the scaling of the two
axes, and 2 parameters describing the *change* in angle of each
axis. Now, suppose you are given the two coordinate spaces, and want to
transform from one to the other. How do we do this with the image
operations in |Leptonica|?

These operations are as follows:

+ Arbitrary translation, implemented by ``pixRasterop()``. We also have
  an in-place version ``pixRasteropIP()``.

+ Anisotropic scaling in x and y, implemented by ``pixScale()``.

+ Horizontal shear about an arbitrary horizontal line ``pixHShear()``,
  with an in-place version ``pixHShearIP()``.

+ Vertical shear about an arbitrary vertical line ``pixVShear()``, with
  an in-place version ``pixVShearIP()``.

+ Rotation about an arbitrary point, implemented by
  ``pixRotateShear()``, with an in-place version ``pixRotateShearIP()``.

To make use of these transforms to align our two coordinate spaces, we
use the following construction, described also in :fs:`affine.c`. The
problem to be solved is to take an image with one coordinate space
(unprimed) and transform it by an affine transformation to coincide
with another coordinate space (primed). We use only shears parallel to
the x and y axes, orthogonal scaling with scaling factors in x and y,
and translation.

A typical application is to align the image with a second image in
another coordinate space, related by the affine transformation. This
invites the following model for making the affine transform. Imagine
that the unprimed coordinate space is in our original image (image 1)
and the corresponding primed coordinate space is in a second image
(image 2). We can transform *both* images so that the coordinate spaces
coincide and are aligned with the x and y axes. After both the unprimed
and primed coordinate spaces are coincident, we finally shear the
unprimed coordinate space to coincide with the original primed
space. Thus, all operations really happen on a single image.
Specifically, we do the following:

#. *Horizontal shear transform* about point 1 to align point 3 with
   the y axis.

#. *Vertical shear transform* about point 1 to align point 2 with the x
   axis.

#. *Compute the horizontal shear angle and the final location of point*
   `3'` required to put point `3'` on the y axis.

#. *Compute the vertical shear angle and the final location of point*
   `2'` required to put point `2'` on the x axis.

#. *Scale* x and y axes anisotropically so that points 2 and 3, which
   are on the x and y axes, move out to a distance equal to the distance
   of the newly sheared points `2'` and `3'` from their origin
   `1'`. This scaling operation will translate the origin (point 1).

#. *Translate* the origin 1, after it has been moved by scaling, to
   coincide with the origin `1'`.

#. *Vertical shear transform* about the new origin (point 1, which is
   now aligned with `1'`), using the negative of the angle computed in
   step 3 above.

#. *Horizontal shear transform* about the new origin (point 1), using
   the negative of the angle computed in step 4 above.

In all this, it is only necessary to keep track of the shear angles and
translations of points during the shears. What has been accomplished is
a general affine transformation on the image. See :fs:`affine.c` for the
specifics of the implementation.

Use these links for more detail on :doc:`rotation <rotation>`,
:ref:`translation <what-else-rasterops>` and :doc:`scaling
<scaling>`. :ref:`Shear <affine-image-shear>` is described below.


Some related transforms
=======================


.. _affine-conformal-affine-transform:

Conformal affine transform
--------------------------

A *conformal affine transform* is special case of an affine transform
where all angles remain the same. It is specified by two corresponding
pairs of points, or four parameters, which satisfy equation
:eq:`matrix-form` with T given by:

.. math::
   :label: conformal-affine-transform

   T =
     \begin{bmatrix}
        a & -b \\
        b &  a \\
        c &  d
     \end{bmatrix}

The four parameters correspond to homogeneous scaling, rotation, and x
and y translation.


.. _affine-projective-transform:

Projective transform
--------------------

When you look at an object in a plane from some arbitrary direction at
a *finite distance*, you get an additional "keystone" distortion in
the image. This is a *projective transform*, which keeps straight
lines straight but does not preserve the angles between lines. This
warping cannot be described by a linear affine transformation, and in
fact differs by x- and y-dependent terms in the denominator:

.. math::
   :label: projective-transform

   x' &= \frac{(ax + by + c)}{(gx + hy + 1)} \\
   {} \\
   y' &= \frac{(dx + ey + f)}{(gx + hy + 1)}

It takes 4 points, or eight coefficients, to describe this
transformation. The projective transform can equivalently be described
by the (transposed) matrix equations:

.. math::
   :label: projective-transform-matrix

   x' &= u / w \\
   y' &= v / w

where:

.. math::
   :label: uvw
    
   \begin{bmatrix}
     u & v & w
   \end{bmatrix}
   = 
   \begin{bmatrix}
    x & y & 1
   \end{bmatrix} \, T

and T is the 3x3 matrix:

.. math::
   :label: T3x3

   T =
   \begin{bmatrix}
     a & d & g \\
     b & e & h \\
     c & f & 1
   \end{bmatrix}

Compared with the affine transform, the extra point (or 2 parameters)
allows specification of a keystone warp by the relative distances
between pairs of points. Because the projective transform is not
linear, it cannot be composed as a sequence of translations, shears,
scalings and (optionally) rotations.

The eight coefficients in :eq:`projective-transform` can be computed
from four corresponding pairs of points (8 equations). No three points
may be collinear.  Projective transforms, and their effects on images,
are implemented in :fs:`projective.c`. As with the affine transform,
both sampling and interpolation implementations are given of the
transform, with the interpolation method being about 5x slower.

It is possible to speed up the interpolation by a small amount by
dividing the pixels into 4 x 4 subpixels (instead of 16 x 16 subpixels),
and inlining an approximation for each of the 16 cases.  (See the
low-level implementation of ``pixRotateAMColorFast()`` for the method.)
This can be also be done for affine and bilinear transforms.  The speed
increase is less than 20%, so in most cases it is not worth the increase
in complexity.


.. _affine-bilinear-transform:

Bilinear transform
------------------

The *bilinear transform* is another nonlinear 4-point transform, which
is somewhat better-conditioned than the projective transform, and a
little faster to compute because it doesn't require a division.
Although the bilinear transform does not preserve straight lines, it can
be used to approximate a projective transform in situations where the
warp is small.

The bilinear transform has a nonlinear cross-term in the
transformation equation:

.. math::
   :label: bilinear-transform

   x' &= ax + by + cxy + d \\
   y' &= ex + fy + gxy + h

and can equivalently be described by the matrix equation:

.. math::
   :label: bilinear-transform-matrix
    
   \begin{bmatrix}
     x' & y'
   \end{bmatrix}
   = 
   \begin{bmatrix}
    x & y & xy & 1
   \end{bmatrix} \, T

where T is the 4x2 matrix:

.. math::
   :label: T4x2

   T =
   \begin{bmatrix}
     a & e \\
     b & f \\
     c & g \\
     d & h
   \end{bmatrix}

Like the projective transform, the bilinear transform cannot be
composed as a sequence of translation, scaling and shears. Bilinear
tranforms of images are implemented in :fs:`bilinear.c`, for both
sampling and interpolation of the src image.


.. _affine-image-shear:

Shearing an image
=================

It is useful to have horizontal shears about an arbitrary horizontal
line, and vertical shears about an arbitrary vertical line. For
horizontal shears, pixels are moved horizontally by a distance that
increases linearly with the (vertical) distance from the horizontal
line, moving to the right above the line and to the left below the
line for positive angles. Likewise, for vertical shear, pixels are
moved vertically by a distance the increases linearly with the
(horizontal) distance from the vertical line, moving downward to the
right of the line and upward to the left of the line for positive
angles.

Formally, a horizontal shear of angle `\theta` about a line `y = b`, with
the origin at the UL corner and a cw rotation taken to be positive, is:

.. math::
   :label: shear

   \begin{bmatrix}
     x' & y'
   \end{bmatrix}
   = 
   \begin{bmatrix}
    x & y & 1
   \end{bmatrix} \, T

where T is the 3x2 matrix:

.. math::
   :label: T-h-shear

   T =
   \begin{bmatrix}
          1          & 0 \\
     -\tan (\theta)  & 1 \\
     b \tan (\theta) & 0
   \end{bmatrix}

Likewise, a vertical shear of angle `\theta` about a line `x = a` is
given by :eq:`shear` with:

.. math::
   :label: T-v-shear

   T =
   \begin{bmatrix}
     1 & -\tan (\theta) \\
     0 & 1 \\
     0 &  a \tan (\theta)
   \end{bmatrix}
    
All interfaces to implementations of shear in |Leptonica| are given at
a high level, using the ``PIX`` data structure. Two-image shear, where
the src is unchanged, is implemented by ``pixRasterop()``.  For example,
a horizontal shear requires moving full-width blocks of pixels
horizontally by varying amounts, depending on the vertical location of
the block. The height of the block is inversely proportional to the
shear angle, appropriately integerized. We express angles in radians,
which are a natural unit, because for small angles the height of each
block is approximately equal to the inverse of the shear angle.

We provide special cases where the image is sheared about the upper-left
corner and also about the center. When shearing by very small angles,
the block height (for horizontal shear) is large. When shearing about
the upper-left corner, the height of the block that is not moved is only
half the block height, whereas when shearing about the center of the
image, the "dead zone" is the full block height.

We also provide in-place versions of shear, implemented by block
shearing of the in-place rasterop functions ``pixRasteropHip()`` and
``pixRasteropVip()``. The higher level two-image horizontal and vertical
shear functions ``pixHShear()`` and ``pixVShear()`` call the in-place
shear functions ``pixHShearIP()`` and ``pixVShearIP()`` when the src and
dest images are the same.


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

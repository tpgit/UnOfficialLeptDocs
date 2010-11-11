:version: $RCSfile: dewarping.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _dewarping-text-pages:

======================
 Dewarping Text Pages
======================

:date: Aug 1, 2010


What distortions do you expect with camera images?
==================================================

If a picture of a flat page were taken at infinite distance, it would
only require an affine transform to rectify it, and even that would
only be necessary if the page were not perpendicular to the optic axis
(OA) of the camera.

Taking the same picture at a finite distance introduces various
distortions, the most serious of which (the "fisheye" effect) causes
horizontal and vertical lines to be curved. This can be corrected by
calibrating the disparity, using an image of a flat page on which
horizontal and vertical lines are drawn. We define the *horizontal and
vertical disparity fields*, as the components of a two-dimensional
vector field that can be used to transform the camera image to the image
that would be acquired from a camera at infinity. In that image, the
lines would again be straight and perpendicular.

A further complication occurs when the page bends (without stretching
or folding) out of the plane perpendicular to the OA. Call the OA the
"z-axis". Then the bending of the page can be described by a scalar
field Z(x,y), which is the position of the paper above or below a
plane perpendicular to the OA. Let the origin (x = 0, y = 0) be the
point where the OA intersects the page. Consider a page with thin
horizontal lines. For a camera at "infinity", these lines continue to
appear straight if Z(x,y) is independent of y (e.g., bending around
vertical lines), But if the camera is at a finite distance they will
bend symmetrically about a vertical line (x = 0) that goes through the
OA. For the general case with a camera at finite distance and Z
depending on both x and y, a perfect dewarping of the image based on
only horizontal lines in the page is not possible. But we can do
fairly well with a very simple approach, described in the next
section.


How do you dewarp a camera image based on text lines?
=====================================================

Intuitively, if you have a number of lines that are known to be
horizontal when rectified, it is possible to generate a vertical
disparity field V(x,y) that maps every point in the image to another
point such that after all points are mapped, the lines are all
straight. This is not unique, and in fact it is important that each
line have a point where the x-derivative of the vertical disparity
V(x,y) goes to zero. Call this point (x0,y0). Then each point (x,y) on
the line gets mapped to (x,y0). So we know the value of V(x,y) on the
points of each line.

Then to get a smooth vertical disparity function V(x,y), we fit each
line to a parametric curve. In most cases a quadratic will suffice;
higher order fits tend to amplify outliers and printing defects. After
the quadratic fit, the result is sampled at equally spaced intervals
in x. Then for each value of x for which we have sampled disparities
at several values of y, fit another quadratic, and sample that at
equally spaced intervals in y. The result is a smoothed V(x,y) at
equally spaced intervals in both x and y. Now interpolate, equivalent
to up-scaling, to get the disparity values at all points (x,y). After
mapping, all the lines should be horizontal.

What about the horizontal disparity? We used a very simple model for
H(x,y) == H(x), independent of y and based on the difference in
vertical disparity at the top and bottom. See the description in the
code header in `dewarp.c` for details.


Example showing images and disparity fields
===========================================

This example is taken from `prog/dewarptest.c`, and the images were
computed there. We start with image `1555-7.jpg`. After doing background
normalization and binarization, we get this image:

.. image:: figs/dewarp-initial.png
   :align: center
   :alt:   Initial Image
   :class: border

We then find the centers of the textlines and do a least squares
quadratic fit to the longest of them:

.. image:: figs/dewarp-fitted-lines.png
   :align: center
   :alt:   Textline Centers
   :class: border

The short, randomly-colored segments (where they are not obliterated
by the green overlay) show the initial estimate of the vertical center
of each component. The green lines show the quadratic fit over the
full textline. The three lines that are shorter than 0.8 of the
maximum line length are not fitted.

The contours of constant vertical disparity, calculated from these
smoothed lines, and the dewarped result on the input image after
applying the vertical disparity, are:

.. image:: figs/dewarp-vert-disparity.jpg
   :align: center
   :alt:   Contours of constant vertical disparity
   :class: border

The horizontal disparity field is then applied to this image. The
field and the final result are:

.. image:: figs/dewarp-horiz-disparity.jpg
   :align: center
   :alt:   Horizontal disparity field and final image
   :class: border

For this page the results look fairly ragged, but the baseline
wobblyness is in the original, which was typeset in a very crude
manner. There are still problems with the horizontal disparity because
of our assumption of y-independence. In any event, I believe that we
do not have the information available in the image to compute the
horizontal disparity with much higher accuracy. This is a challenge to
the reader: if you can figure out a way to find the horizontal
disparity more accurately, let me know (and for extra credit send me
the result).


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

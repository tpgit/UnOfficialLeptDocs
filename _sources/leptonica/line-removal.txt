:version: $RCSfile: line-removal.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

=================================================
 Removing dark lines from a light pencil drawing
=================================================

Here is an interesting exercise in grayscale image processing (see
`prog/lineremoval.c`), The goal is to remove some (nearly) horizontal
lines from a scanned image, so that it is not obvious that the lines
were ever there. The image is a pencil drawing that has relatively light
pencil marks over dark lines that were printed on a ruled pad. The
subject is Dave Carman, a venerable Exum Mountain Guide in Grand Teton
National Park.

.. figure:: figs/dave-start.png
   :align: center
   :alt:   Original Image
   :class: border

   Fig 1. --  Original image

   ::

      pixs = pixRead("dave-orig.png")

This is the original, scanned in grayscale and scaled down to about
2/3 size for easy viewing here. I first summarize the approach, and
then show you the details. Here are the main steps:

#. **Deskew the image.** We want the lines to be horizontal so the can
   be effectively removed by large morphological openings.

#. **Extract the horizontal lines.** Ideally, we want just these
   lines, but we get some of the background as well.

#. **Remove the background.** If the light background is not removed,
   we will lighten the final result when we remove the lines. The light
   background is removed by setting to white given a threshold.

#. **Darken the lines.** If the lines are not dark enough, they will
   not be entirely removed. The lines are darkened by setting to black
   given a threshold.

#. **Remove the lines from the deskewed version of the original.**
   This is done by adding the inverse (value --> 255 - value) of the line
   image.

#. **Reconstitute the missing pixels.** Set those pixels to the
   minimum values above and below, using morphological opening followed
   by pixel selection.

The total time to run all the processing on a 1 megapixel image is
about 1 second on a fast P4! The details follow.

.. figure:: figs/dave-proc1.png
   :align: center
   :alt:   Threshold to binary
   :class: border

   Fig 2. 

   ::

      pix1 = pixThresholdToBinary(pixs, 150);

The first step is to deskew the image, so that the lines are
horizontal. We will then be able to apply large filters to extract the
lines. First threshold to binary, extracting enough of the lines to make
a good measurement, as shown in **Fig. 2**.

.. figure:: figs/dave-proc2.png
   :align: center
   :alt:   Deskew image
   :class: border

   Fig 3.

   ::

      pixFindSkew(pix1, &angle, &conf);
      pix2 = pixRotateAMGray(pixs, deg2rad * angle);

Then compute the skew angle, which turns out to be 0.66 degrees
clockwise, and deskew using an interpolated rotator for anti-aliasing
(to avoid jaggies). The result is in **Fig. 3**.

.. figure:: figs/dave-proc3.png
   :align: center
   :alt:   Extract lines via grayscale closing
   :class: border

   Fig 4. 

   ::
   
      pix3 = pixCloseGray(pix2, 51, HORIZ);

Now, extract the lines to be removed, trying not to get too much else in
the process. Unfortunately, we get a lot of light background stuff that
we're going to eventually want to save. This is done with a grayscale
morphological closing with a large horizontal structuring element, as
shown in **Fig. 4**.

.. figure:: figs/dave-proc4.png
   :align: center
   :alt:   Grayscale vertical erosion
   :class: border

   Fig 5. 

   ::

      pix4 = pixErodeGray(pix3, 5, VERT);

Not only did we get some background that we didn't want, we also got
lines that are narrower than the actual lines. We need to solidify them
in the vertical direction, and do this with a small grayscale vertical
erosion. The result is in **Fig. 5**.

.. figure:: figs/dave-proc5.png
   :align: center
   :alt:   Threshold 210 to white
   :class: border
   
   Fig 6. 

   ::

      pix5 = pixThresholdToValue(pix4, 210, 255);

This solidifies the lines, but it also darkens the other background that
we want to save! Now, we want to remove the lines, which we will do by
adding the inverse. But first we need to get as much of the background
set to white as possible; otherwise, the addition will lighten the gray
regions. To do the cleaning, choose a threshold and for any pixel
lighter than the threshold, set it to white (255). We have to set the
threshold very high (210) because the lines themselves are very
light. The result is in **Fig. 6,** where you can see that the light
gray has been removed. Notice that there is still some stuff we want to
keep that we may eventually lose.

.. figure:: figs/dave-proc6.png
   :align: center
   :alt:   Threshold 200 to black
   :class: border

   Fig 7.

   ::

      pix6 = pixThresholdToValue(pix5, 200, 0);

It turns out that the smearing of the lines has made them lighter in the
center than the original lines. If we add the inverse as it is, we'll
get black residuals in the center. We must darken the lines, and we do
it with the same grayscale thresholding function, but this time setting
the pixels to black (and still using a high threshold because the lines
are quite light). The result is in **Fig. 7**.

.. figure:: figs/dave-proc7.png
   :align: center
   :alt:   Threshold 210 to black
   :class: border

   Fig 8. 

   ::
   
      pix7 = pixThresholdToBinary(pix6, 210);

Carrying on, the basic idea is to remove the lines, then close up the
holes. But when we close up the holes, with a vertical opening, we also
smear the image. So we will want to select only those pixels in the gap
from the opened image. Thus, we need a paint-through selection mask,
which is simply a binarized version of the image of lines that we just
made. The threshold we use here is the same as the one used in the
previous step (210), but here we are making a binary image where all
pixels in the lines that are below 210 become black; the rest are
white. The mask is in **Fig. 8**, and we'll put it aside and use it
later.

.. figure:: figs/dave-proc8.png
   :align: center
   :alt:   Invert and add gray
   :class: border

   Fig 9.
 
   ::  

      pixInvert(pix6, pix6);
      pix8 = pixAddGray(NULL, pix2, pix6);


We can now invert the grayscale lines and add the result to the original
(rotated) image. Shown in **Fig. 9**, the lines mostly vanish, but we
lose some stuff that we really want where the lines were. Because we
previously whitened the other parts, we don't damage the light gray
areas that are not on the lines. (Addition is clipped to 255 (white), so
that any sum larger than 255 is white.)

.. figure:: figs/dave-proc9.png
   :align: center
   :alt:   Grayscale vertical opening
   :class: border

   Fig 10. 

   ::

      pix9 = pixOpenGray(pix8, 9, VERT);

Of course, we don't know what the missing pixel values would have been
in the absence of the lines, so we make a "guess" that they're similar
to the values above and below the white stripes. We implement this by a
grayscale opening in the vertical direction, as shown in **Fig.
10**. This smears the image (``pix9``), making it look quite fuzzy. But
not to worry. We're only going to use the parts of this image that are
under the line mask (``pix7``); for the rest, we use the previous image
(``pix8``).

.. figure:: figs/dave-result.png
   :align: center
   :alt:   Final image
   :class: border

   Fig 11. 

   ::

      pixCombineMasked(pix8, pix9, pix7);


The result is composed of two grayscale images, with a binary
selector mask choosing which pixels come from which, and is shown in
**Fig. 11**.

We'll stop here. It isn't perfect yet, but it shows what can be done
with a little experimentation.


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

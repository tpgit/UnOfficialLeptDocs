:version: $RCSfile: filling.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _seed-filling-and-connected-components:

=======================================
 Seed Filling and Connected Components
=======================================

:date: Jan 11, 2009

.. contents::
   :local:


What is the seed fill operation?
================================

The *seed fill* operation, and various generalizations, is arguably
the most important technique in image analysis. I won't give an
"analysis" of image analysis here, but the central position of seed
fill is crucial. The most basic part of image analysis is *image
segmentation*, which is the division of the image into regions that
have different properties. For example, finding the text characters
and the line graphics in a text image is part of document image
segmentation. Most image segmentation methods, whether they are
"bottom-up" or "top-down" or a mixture of the two, have, at their
core, two parts:

#. the identification of *seeds*, which are pixels within the image
   that have a specific property, and

#. a *region-filling* operation that includes constraints to prevent
   each region from overfilling.

.. _luc-paper-Morphological-grayscale-reconstruction:

The region-filling constraints can be pre-determined masks, which are
typically used in binary image segmentation, and they can also be
expressed as a boundary negotiation process where regions expand and
meet, thus preventing further expansion. We will be primarily concerned
here with seed fill methods on binary images. For a discussion of
various algorithms for both binary and grayscale, and their use, see the
`paper <http://www.vincent-net.com/luc/papers/>`_ by Luc Vincent:
:title:`Morphological grayscale reconstruction in image analysis:
applications and efficient algorithms`, :journal:`IEEE Trans. on Image
Processing`, :jvolume:`Vol. 2, No. 2`, pp. 176-201, April 1993. (To view
this paper, you need to download the djvu viewer, available from that
site.)

A *seed fill* is an image processing operation where pixels in some
region of an image are assigned a label. Often this is described as
having the pixels change "color." As we will be filling on binary
images, the color change is from black to white or v.v. A *seed* is a
single pixel or a collection of pixels where the change is selected to
begin. The seed is allowed to grow, under the constraint of a *mask*
that limits the growth. The seed fill process ends when the seed has
grown under the mask as far as possible.

There are multiple names for this process. The graphics community uses
the terms *seed fill* and *flood fill*, with a typical application
being the filling of pixels within an outline for device indpendent
graphics. The image morphology community calls it *binary
reconstruction* (and *grayscale reconstruction*), with the primary
application being image segmentation.

There are also multiple ways of implementing seed fill, which are
described in more detail below. In all cases that we consider, seed
fill works by a growing process that is constrained by a mask image.
The most simple conceptual method is an iterative process where you
start by flipping a single seed pixel, and then flip every pixel that
is (either 4- or 8-) connected to it, subject to the mask constraint.
This can be done recursively by procedure calls or with a stack.
Because there are potentially a large number of pixels that can be
changing, I prefer to use a dynamic stack rather than recursive
procedure calls that can generate an arbitrarily deep call stack. As
each pixel is popped from the stack, it is inspected, its color is
flipped, and you put its eligible neighbors on the stack for future
work.

With large images, the stack can get quite large, and, furthermore,
unless you are careful, you end up inspecting each pixel several
times. A better method puts *runs of adjacent pixels* on the stack,
and we provide an efficient version of this that was written by Paul
Heckbert for identifying connected components.

A much less efficient, but conceptually simple method, is to iterate a
morphological dilation with an AND to the clipping mask. This grows
the boundary at the rate of one pixel per iteration, so for a large
image it may require hundreds or thousands of iterations to grow the
seed into the mask. Nevertheless, we provide a function to do this,
for either 4- or 8-connected filling. This works well if the masks are
relatively small, it has pedagogic value from its simplicity, and it
provides a baseline implementation against which other, more
complicated but more efficient, filling operations can be checked for
correctness.

The stack-based methods are much more efficient because they only work
on pixels at the boundary where growth can occur. An iterative seed
fill method by Luc Vincent allows raster-ordered growth (from UL to
LR, or v.v.). For typical images only a few iterations are required
until filling is complete, but one can imagine pathological images
(such as a maze) that can take many iterations.

There are two ways to visualize the operation of the mask. Consider
the morphological operation of binary reconstruction. In the software
here, we use a *filling* mask; the seed fills in under the mask up to
the boundary of the region (or component) that is being filled. The
mask clips the filling operation by a logical AND with the growing
seed. Another way to visualize the operation of the mask is as
*blocking* mask, where the seed is allowed to grow until it hits
elements of the blocking mask. It is easy to see that the blocking
mask and filling masks are just bit-inverses of each other. Use of a
blocking mask is common in the description of a flood fill, where you
have a single image containing both the growing seed and the pixels
that stop the growth. For example, the seed can be growing in a region
of OFF pixels which are being flipped ON, and the growth is delimited
by ON pixels in the same image --- you can't tunnel through ON pixels
to start growing in another region of OFF pixels.

There are two different growth processes on a rectangular lattice.
These are called 4-connected and 8-connected seed filling, and they fill
into 4-connected and 8-connected regions of the mask, respectively. The
French, who invented image morphology, liked to work on hexagonal
lattices where every pixel is 6-connected to another pixel, because on
such lattices there is an exact symmetry between the foreground and
background of binary images. (Hexagonal lattices can be imagined as
distortions of rectangular lattices where every odd row is shifted 1/2
pixel to the left or right.) That symmetry doesn't exist on rectangular
lattices, where the connectivity of foreground and background are
usually taken to be complementary, so that the component boundaries do
not cross. This can be seen intuitively as follows. Imagine an 2x2 pixel
binary image with ON pixels at the UL and LR and OFF pixels at the other
two corners. The ON pixels are two 4-connected components, or 1
8-connected component, and likewise for the OFF pixels. If both
foreground and background were 8-connected, there would be one component
in each, and they would intersect. As another example, take an image and
embed a 3x3 square as a foreground component. Then remove the 4 corners
and the center, leaving a hollow 4 pixel diamond in the foreground. This
foreground is a single component if it is 8-connected. Intuitively, this
leaves 2 components in the background, the center pixel and all the
rest, which we get using 4-connectivity for the background. If we used
8-connectivity for the background as well, we would get a single
component, with the center pixel surrounded by the single component of
the foreground!  Likewise, taking 4-connectivity for the foreground, we
have 4 single-pixel components in the diamond pattern, and it is
reasonable to take the background as a single 8-connected component that
includes the center pixel.

4-connected filling is typically (but not always) less work
computationally than 8-connected filling, because there are fewer
pixels that need to be checked. (But there are usually more resulting
components.) We now give some more details about each of the seed fill
implementations.


.. _seed-filling-identify-connected-components:

Seed filling to identify connected components
=============================================

The seed fill operation can be used to identify connected components, by
sequentially filling them; i.e., by changing their color, or erasing
them. This can be done *in situ* on the image. Typically, we are
interested in the foreground components, and these are erased by turning
the pixels OFF. In `conncomp.c`, we use Paul Heckbert's algorithm
exactly as it was described and coded in :title:`Graphic Gems`, edited
by Andrew Glassner, :publisher:`Academic Press`, 1990, pp. 275ff and
721ff.  This algorithm reverses the pixel value of all pixels within a
4-connected component in the image, starting with the seed pixel. The
only change we made to Heckbert's code is to use function calls instead
of macros for pushing data on and popping data off a stack. A stack
utility is used to automatically grow the stack size as required, and a
second stack is used to store the structures that are not in use.

Heckbert's algorithm identifies horizontal runs of similarly colored
pixels recursively within each connected component. It is efficient
because each run "remembers" the direction of its parent and thus does
not look back at the parent when searching for other connected pixels.
As a result, each pixel in the image is scanned essentially once.
Here's what happens. For each segment, corresponding to a parent run
of pixels, that is popped off the stack, one checks for connected runs
on the adjacent raster line in the direction specified within the
segment. The side specified is always *away from* the segment parent,
so one never looks back toward the parent, which, in any event, has
already been erased. For each run that is detected on this new raster
line, the pixels are erased and a new segment is pushed on the stack,
with a direction in the same direction as that of the parent. Call
this the "direct" direction. This allows you to follow a c.c. down
from top to bottom (or up from bottom to top). Keep in mind that when
a segment is pushed on the stack, the pixels in its run have already
been erased. The action when it is popped is to explore the adjacent
raster line in the direction indicated. Additionally, one must account
for potential "leaks" where connected runs extend on the new line
beyond the parent segment and, consequently, *may have connected
pixels back onto the raster line of the parent* (but not touching the
parent, of course). The "leak" direction, being backwards toward the
parent, is opposite to the "direct" direction. These potential leaks
can occur on either side of the parent, and any such runs that are
found result in another segment pushed on the stack. Note that the run
of pixels of such potential leak segments will result in two segments
being pushed on the stack, a "direct" one pointing in the same
direction as specified in the segment and the a "leak" one pointing in
the opposite direction. (For every segment popped from the stack, you
can have no more than two "leak" direction segments, but you can have
as many "direct" segments as you have runs that are connected to the
parent run of the segment.) That is the essence of the algorithm. When
the stack is finally empty, all connected pixels in the c.c. have been
found and erased. A picture may be worth a thousand words here, but
you'll have to settle for this description and, of course, the code.

The connected components are detected in raster order, and we invoke
Heckbert's filling method repeatedly to erase them. We have generalized
Heckbert's algorithm to allow seed filling of 8-connected components as
well. The details are in `conncomp.c`. As each c.c. is erased, we can
keep track of the minimum bounding box for the set of pixels. If
desired, we can also reconstruct the images of the c.c., and store them
in a data structure that holds an array of ``PIX``\ s.

Whereas the seed fill operation is by definition an image processing
operation (the input and output are images), the c.c. finder is an
example of a different type of imaging operation. For the c.c. finder,
the result is put in auxiliary data structures that are not images.  For
the bounding boxes of the c.c., we use an array of rectangles called a
``BOXA``.

The top level call is ``pixConnComp()``. This generates the bounding
boxes of the 4- or 8-connected components in the foreground, and,
additionally, an array of the images of each c.c. if requested. The
request for an array of images is made by supplying the function with
the address of a pointer to the image array (a ``PIXA``), which is
subsequently allocated, built and saved. The images of each component
are found by maintaining two page images. A component is erased from
the first one, and the region within the bounding box of the two
images is compared (by XOR) to yield an image of the erased component.
The region in the second image within the bounding box is then copied
from the first image, so that the two images again become identical.
This procedure is repeated for each c.c. until all c.c. have been
erased.


.. _seed-filling-binary-morphology:

Seed filling using binary morphology
====================================

A seed can be filled into a mask using an iterative sequence of
dilations followed by ANDing the dilated seed with the mask. As
mentioned above, except for small components, this is inefficient,
because the only changes occur at the seed boundaries, but the
computation must be performed over the entire image on each iteration.

For an 8-connected component fill, one uses a 3x3 brick SE with the SE
center in the center of the 3x3 array. A dilation with such a SE
obviously propagates the center value to its eight neighbors. For a
4-connected fill, remove the corner elements of the SE, so that the
3x3 SE has elements to N, S, E and W of the center. Implemented
without using a separated SE, the 8-c.c. fill thus requires about
twice the computation of the 4-c.c fill. However, with separation, so
that the 3x3 brick is implemented as a sequence of 3x1 and 1x3
dilations, the computation is nearly equivalent. For details (and
there are very few), see ``pixSeedfillMorph()`` in `morphapp.c`.


.. _seed-filling-iterative-filling:

Seed filling using iterative raster-ordered filling
===================================================

The method for iterative raster-ordered filling is due to Luc Vincent.
The basic method in the Vincent seedfill algorithm is simple. Pixels
are sampled in raster order in the seed image. For 4-connected fill,
consider an arbitrary pixel. If this pixel is ON, or if there is an ON
pixel either directly above or to the left, and if it is not masked
out by the mask image, the pixel is turned on (or remains on). The
rule is similar for 8-connected fill, except you need to check three
pixels (directly above, to the left, and to the right) on the previous
line as well as the pixel to the left on the current line. In most
images this is extra computational work for relatively little gain, so
it is often preferable to use the 4-connected version. The algorithm
proceeds in raster order from UR to LL of the image, and then reverses
and sweeps up in anti-raster order from LL to UR. These double sweeps
are iterated until there is no further change in the image, at which
point the seed has entirely filled the region it is allowed to (as
delimited by the mask image).

It should be noted that for some applications, the filled seed will
later be OR'd with the negative of the mask. The negative of the
filling mask is the blocking mask. By ORing the filled seed with the
blocking mask, you get the result for flood filling into a region of
OFF pixels that is delimited by the ON pixels on its boundary. A nice
example of this is to flood fill starting from seeds around the image
boundary. For an image of text, this will fill everything except for
the holes within characters. We give an interesting example of such
topological extraction in `prog/topotest.c`

For efficiency, the pixels should be taken in larger units for
processing, but still in raster order. It is natural to take them in
32-bit words. The outline of the work to be done for 4-cc (not
including special cases for boundary words, such as the first line or
the last word in each line) is as follows, and it corresponds almost
exactly to the per-pixel version described above. Let the filling mask
be m. The seed is to fill "under" the mask; i.e., limited by an AND
with the mask. Let the current word of the seed be w, the word in the
line above be wa, and the previous word in the current line be wp. Let
t be a temporary word that is used in computation. Note that masking
is performed by w & m. (If we had instead used a blocking mask, we
would perform masking by the set subtraction operation, w - m, which
is defined to be w & ~m.) The entire operation can be implemented with
shifts, logical operations and tests. For each word in the seed image
there are two steps. The first step is to OR the word with the word
above and with the rightmost pixel in wp (call it "x"). Because wp is
shifted one pixel to its right, "x" is ORed to the leftmost pixel of
w. We then clip to the ON pixels in the mask. The result is::
    
   t  <--  (w | wa | x000...) & m

We've now finished taking data from above and to the left. The second
step is to allow filling to propagate horizontally in t, as it would
if we were using the per-pixel version, and always making sure that
the word is properly masked at each step. If filling can be done at
all --- i.e., t is neither all 0s nor all 1s --- iteratively take::

   t  <--  (t | (t >> 1) | (t << 1)) & m

until t stops changing. Then write t back into w. Note that if we were
strictly following the per-pixel version, we would not use propagation
to the left, represented by (t << 1) above. However, this is
inexpensive and may act to speed convergence.

Finally, boundary conditions require we note that in doing the above
steps,

+ The words in the first row have no wa.

+ The first word in each row has no wp in that row.

+ The last word in each row must be masked so that pixels don't
  propagate beyond the right edge of the actual image. This is easily
  accomplished by setting the out-of-bound pixels in m to OFF.

The sweep up from LR to UL is similar, and can be written on inspection
from the down sweep. The details are in `seedfill.c`. The special cases
at the boundary are slightly different, in that the first two items are
modified to

+ The words in the last image row have no words below.

+ The last word in each row has no word following in that row.

For 8-connected fills, we simply alter the first step in the down
sweep to::
    
   t  <--  (w | wa | wa >> 1 | wa << 1 | wal << 31 | war >> 31 | wp << 31) & m

where ``wal`` and ``war`` are the words to left and right of wa, and we
have shown how to get x000.... explicitly for wp. Note that for 8-cc
fills, we must include the influence of 3 pixels on the line above and
one on the same line for each pixel in w. Can you identify which terms
in the expression above go with which pixels?

The expression above for 8-cc fills looks like a dilation with a SE that
has 4 elements: 3 in a row below the center and 1 to the right of the
center. It is written in the same form as the :ref:`destination word
accumulation <dwa-implementation-binary-morphology>` implementation of
binary morphology! Can we do this efficiently using binary morphology?
For example, for the down sweep we dilate as described above. Then for
the second step we repeatedly dilate and mask with a horizontal brick SE
of length 3, either until convergence or, in any event, not more than 31
times. The up sweep uses a SE inverted about the center.

Alas, this is *not* equivalent to to the Vincent algorithm. The reason
is that the Vincent algorithm is *sequential*, where the result acting
on a pixel can be propagated in the same sweep down and to the left.
The order in which pixels are processed is crucial. For sufficiently
simple masks, an entire image can be filled with a single downward
sweep! Binary morphology, in contrast, is a *parallel* operation. It
takes place between two separate images, and the result of the
operation doesn't depend on the order in which the dest pixels are
computed. The operation on each pixel in the dest depends only on a
set of pixels in the source, never on any of the newly computed pixels
in the dest. The expanding boundary of the seed can move at most only
one pixel on each iteration. An analogy from 1-dimensional signal
processing may help. The Vincent algorithm is a two-dimensional
version of a (rather complicated) infinite impulse response (IIR)
filter, where the new values depend on values changed in this
iteration, whereas binary morphology is analogous to a finite impulse
response (FIR) filter, where the new values depend only on values from
the previous iteration.

Looking back on the various methods of seed fill that we have
discussed, every method is sequential except for the one implemented
by binary morphology, which is parallel. The recursive sequential
methods, that are typically implemented with a stack, focus all the
action on growing the boundary pixels; interior pixels are completely
ignored. The Vincent sequential raster-order method does not
distinguish between boundary and non-boundary pixels. Luc Vincent has
presented modified versions of his method that use the raster-order
sweep for the first iteration, noting which pixels are on the
boundary, and following with a purely boundary-growing sequential
method. As you can see, these sequential algorithms have a great
amount of variation and flexibility.

Consequently, it is interesting to ask what other purely iterative
sequential filling algorithms are possible. The two we've explored,
for 4- and 8-connected filling, fill each word from 2 and 4
neighboring pixels, respectively, followed by horizontal flood fill.
Because of the raster order, filling proceeds down and to the right in
UL --> LR. (For such fills, on a single raster-ordered sweep any
particular pixel can only affect pixels in the rectangular region
below and to its right.) Alternatively, one can fill vertically only,
using either a 2- or a 6-connected fill. This would miss some pixels
that can be filled horizontally but are protected from vertical
filling by the mask. One can also fill with only the down/up shifts
for one down/up raster sweep iteration, alternating with only the
left/right shifts for one left/right raster sweep iteration. This is
more complicated to implement, and may be slower to converge, but the
end results of the filling would be identical to the 4-cc and 8-cc
filling described above.

In a similar way, you can do a restricted seed filling operation,
``pixSeedfillBinaryRestricted()``. The maximal region of permitted
filling is found by dilating the seed. This is often useful if you
have an idea of the maximum expected range of the fill, and if an
unrestricted fill can cause serious problems.

.. _seed-filling-grayscale:

Seed filling extended to grayscale images (*grayscale reconstruction*)
======================================================================

Luc Vincent has also described, in the paper cited :ref:`above
<luc-paper-Morphological-grayscale-reconstruction>`, how the iterative
raster-ordered binary reconstruction algorithm is easily adapted to
grayscale seed filling. The rules for sequential pixel update are nearly
identical to those for binary images, with the only change being that
the logical OR operation is replaced by *Max* and the logical AND
operation for clipping to the mask is replaced by *Min*.

Let the pixel neighborhood be labelled as follows::
  
   1 2 3
   4 x 5
   6 7 8

At each point in the sweep, we are working on the center pixel ("x").
For 4-connected reconstruction, the previous pixels on the raster-order
sweep are 2 and 4; for 8-connected they are 1, 2, 3 and 4. Pixel x is
replaced by::

   x <--  Min (m, Max(2, 4, x))            4-connected
   x <--  Min (m, Max(1, 2, 3, 4, x))      8-connected

where m is the pixel value in the "mask" image that corresponds to
pixel x. This should all look very familiar. We replace x by the
maximum of its raster-ordered prior neighbors, and then clip to the
mask. Note that *Min* and *Max* are the grayscale generalizations of
bit-and and bit-or, respectively.

How do we visualize this reconstruction process and the resulting
filled seed? Think of the mask image as an elevation map in three
dimensions, where the third (vertical) dimension is the value of the
mask pixels. As the iterations proceed, the seed expands to fill under
the mask as a flat image with height equal to the maximum value of the
seed, clipped, however, by the mask elevation. If the mask is
everywhere greater than this maximum seed value, the seed image goes
to a constant height over the entire image. However, if the mask is
anywhere less than this maximum seed value, the seed value is pushed
down at those points so as not to exceed the mask there. Furthermore,
suppose the mask has a closed minimum encircling the maximum seed
value that is less than the seed value. Visualize this as the mask
being a mountain above the seed with low valley regions, relative to
the maximum of the seed, all around it. Then the seed will fill out
under the mountain to a fixed height, and be clipped by the sides of
the mountain so as not to exceed it. If the low points around the
mountain are greater than zero, some of the seed value will escape
from under the mask mountain, but it will be clipped to the maximum
height that can "leak" out beyond the mountain. Thus, it will be lower
outside than inside. With binary images and masks, we don't have any
of this fuzziness. The seed comes all the way up to the mask (of value
1), and outside the mask connected component it is clipped to 0 (no
leakage is possible). The implementation is ``pixSeedfillGray()``.


.. _distance-function-within-connected-components:

Generation of a distance function within connected components
=============================================================

Let's go back to binary images. We can use the same type of iterative
raster-order filling algorithms described above for binary seed filling
to compute the *distance function* in connected components.  The
distance function is an assignment from a binary image to a grayscale
image, where for each foreground pixel of a binary image we compute
either a 4-connected "manhattan distance" or an 8-connected
quasi-euclidean distance from the background. (These values are stored
in the grayscale distance image.) The background pixels in the binary
image map to the value 0 in the distance image. Boundary pixels adjacent
to the background are assigned a distance 1. Pixels adjacent to those
boundary pixels have a distance 2, etc. Geometrically, each connected
component can be thought of an island, where the assignment of a
distance is the smallest horizontal distance to the water. The largest
distance value in a connected component is the maximum of such minimum
distances over all pixels of the c.c. We will see how to *label* every
pixel in a connected component by this maximum distance, which is a
particular measure of the "size" of the connected
component. Specifically, it is the size of the minimum ball structuring
element that will entirely erode the connected component.

It's worth noting that the computation of distance can also be
performed on the background; namely, each pixel can be labeled by the
shortest distance to a foreground pixel. All foreground pixels are
naturally given the value 0. The implementation for foreground
distance can be used for background distance by inverting the image
before computing the distance.

The distance function can be calculated with a *single*
raster/anti-raster pair of sweeps. No iteration is necessary. On the
down-sweep the rule is to *add one to the minimum distance of the
neighbors*; on the up-sweep the rule is to take the same augmented
minimum (from the other direction, of course) and to choose the minimum
of that value and the current value, and add 1.

One never knows if an algorithm is correct unless it is implemented
and tested, so you can find the distance function in
``pixDistanceFunction()``. There are a few details that should be
mentioned. First, the grayscale distance image (the result), which is
typically an 8 bpp or 16 bpp image, needs to be initialized to have
values 1 on pixels corresponding to the foreground of the binary image
and 0 for the background. It is also convenient to maintain an
exterior ring of pixels with value 0, because when the sweep starts it
must have these values available to guarantee that the next ring of
pixels can not have a value that exceeds 1. This is easily seen as
follows. Suppose some of the foreground extends to the top boundary of
the image, and suppose that the top row of pixels are initialized to
be 1 for the foreground part. We must have at least one 0 pixel
adjacent in order to prevent these foreground boundary pixels from
getting a value of 2! Where are we going to get those pixels? Clearly,
the outer ring of pixels, whether 0 or 1, doesn't change due to the
iterative sweeps, so we can start our computation at the interior of
this ring. The exterior ring is set to 0 so that the calculation
proceeds properly. This also removes the necessity of special-casing
the calculation of boundary pixels!

Note that once the distance image has been initialized, all
computation proceeds directly on this image. Then, using the pixel
3-neighborhood labelling given above, the down-sweep distance is found
from::

   x <--  Min(2, 4) + 1            4-connected
   x <--  Min(1, 2, 3, 4) + 1      8-connected

(If an 8 bpp image is used, it may be necessary to clip the minimum
distance to 254 before adding 1 to avoid overflow. In such a case, the
distance function artificially saturates at 255.)

The result of this down-sweep is to give the distance from the
"upper-left shores". All the pixels on the boundary of the connected
components should have a distance 1, but the lower-right boundary pixels
now typically have values greater than 1. (And, remember that the outer
ring of pixels has value 0.) We must follow with an up-sweep (starting
at the lower-right "shores") to recompute distances::
    
   x <--  Min(x, Min(7, 5) + 1)            4-connected
   x <--  Min(x, Min(8, 7, 6, 5) + 1)      8-connected

Note that the condition for up-sweep differs from the down-sweep in
that the current value of the pixel is also included in the
calculation of the minimum. We don't want the values to keep
increasing once we get over half way across a connected component, as
they did on the down-sweep! This can also be expressed as follows: the
inner Min finds the distance from the lower-right "shore" and the
outer Min chooses the minimum between the sweeps in the two
directions.

To visualize these distance images we provide a function
``pixMaxDynamicRange()``, that either linearly or logarithmically maps
an 8 or 16 bpp image to an 8 bpp image with the maximum dynamic range
(0-255). Without this function, for binary images where the maximum
value in the distance map (image) is much less than 255 pixels, the
distance maps typically look very dark.


.. _labelling-pixels-distance-function:

Labelling pixels using distance function and grayscale reconstruction
=====================================================================

As an illustration of what we can do with the various filling and
distance operations described here, we can combine the distance
function with grayscale seedfill to label each pixel in a connected
component by the largest distance in that connected component. This is
equivalent to labelling each pixel by the smallest ball structuring
element that could be used in an erosion to entirely eliminate the
connected component. This measure of the maximum "width" of the c.c.
is a particular measure of its "size."

We start with a binary image, and generate the distance function on
the foreground connected components (either 4-cc or 8-cc). We then
take the binary image and construct a grayscale clipping mask of the
same size that has the values 0 and 255 wherever the binary image has
values 0 and 1, respectively. If we then use the distance function
image as a seed and fill into this mask, the maximum value of the seed
in each c.c. will eventually be propagated to all the pixels in the
c.c. Each c.c. will fill independently because the clipping mask has
value 0 in the spaces between the connected components. The function
``pixSetMasked()`` is used to generate the clipping mask from the
binary seed. An example implementation is given in
`prog/distancetest.c`.


.. _watershed-transform-seeded-images:

Watershed transform on seeded grayscale images
==============================================

The watershed "transform" proceeds from a set of seeds to identify the
"watersheds" associated with each seed. This is computed by filling
from the local minima in the image, where the filling operation is
analogous to pouring water into the image, filling it uniformly. Each
watershed (or "catch-basin") will overflow at some height, and our job
is to identify the set of pixels corresponding to the watershed just
before it overflows. Each watershed is thus represented by a connected
component giving its extent, and the set of such connected components,
along with their filling heights, constitutes the solution.

But if we're filling from each minimum, what is the function of the
seed? The set of seeds is exceedingly important, because we *only record
a watershed when there is a seed somewhere inside*! In addition, we
provide an input parameter, which is the minimum height that a watershed
can have. This is necessary to avoid having tiny watersheds due to noise
in the image. Any watershed of less depth than the minimum is either
absorbed into a deeper watershed during filling, or abandoned if it
can't be merged with a deeper watershed.

The implementation is in `watershed.{c,h}`, and it uses a priority
queue (prioritized by height --- aka, pixel value) to hold the pixels
along the expanding boundaries as filling progresses. In addition, we
have a 32-bit image to label, with the seed index, the pixels found.

Here's the tricky part. When two watersheds flow together, we identify
each of the individual watersheds. To allow filling to continue, these
must be re-indexed in some way. Re-indexing must also occur when a
too-shallow watershed is merged with a deep one, or when an unseeded
minima merges with a watershed, or two unseeded minima merge, etc. To
avoid changing the labels in the 32-bit image, which would be a
nightmare, we use a set of lookup tables and backpointers to keep track
of all the re-indexing.

The implementation as it presently exists is buggy. Run
`prog/watershedtest` to see how this works.


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

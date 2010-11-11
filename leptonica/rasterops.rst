:version: $RCSfile: rasterops.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _rasterops:

==========================
 Rasterop (a.k.a. Bitblt)
==========================

:date: Nov 23, 2006

What is rasterop?
=================

One of the most useful operations in image composition, image
transformation and image analysis is the **rasterop**. This is the
low-level operation that your window system uses to paint bitmap
characters to your frame buffer, and to paint and repaint windows when
they are generated, resized, or moved.

This operation has a long and distinguished history, with the driving
force being the desire to use bitmapped graphics terminals for realtime
I/O. According to Eric Raymond's *New Hacker's Dictionary* (1991, MIT
Press), the PDP-10 had a BLT (BLock Transfer) machine instruction to
copy or move a contiguous block of data within memory. (This is not to
be confused with the common BLT (Branch if Less Than zero) assembly
instruction, or the BLT (Bacon Lettuce and Tomato) sandwich.) Suppose
you have an image that is represented by a contiguous block of memory in
line raster order, but you want to copy or move data between rectangular
sub-blocks. In general, this data will be composed of disconnected
fragments of the original block of data. One version of rasterop that
worked on rectangular two-dimensional subimages of the display buffer
was implemented at Xerox PARC in the early 1970s by Dan Ingalls. This
utility was used to display character bitmaps on the Alto, a 16-bit
computer derived from the Data General Nova minicomputer. At Xerox, the
operation was called *Bitblt*, pronounced "bit blit", which is short for
"Bit Block Transfer." (The Alto displays were 1 bit/pixel, monochrome.)
Many implementations were subsequently written for other computers with
bitmapped graphics displays, such as Sun's Unix workstations dating from
the early 1980s that used Sun's proprietary *Sunview* window system.

For efficiency, some of the display bitblt operations need to work *in
place*, so that the display buffer is both the source and the
destination of the pixels. In such situations, bits have to be copied in
a particular order so as not to overwrite bits that need to be moved
later. Some bitblt (rasterop) operations do not use the display buffer
as either the source or destination of the bits. Such memory-to-memory
operations are used, for example, by *imagers* that compose page images
for display or printing, or, as we shall see, for many image processing
operations in general.

There are two well-tested versions of rasterop in open source that I
know of: one with X windows and one with ghostscript. However, these are
both complicated by internal reference to graphical display imaging, and
they have a very large set of operators. They do not have a clean
interface to the low-level bit manipulation routines, and they are
encumbered by Gnu's GPL "copyleft" (for X) and by Aladdin's own copyleft
(for ghostscript). For these reasons, I have made a set of efficient
low-level routines for rasterop, with a clean interface between the
user's image data structure and low-level data. If you want to use a
different image data structure, it is a simple matter to rewrite the
interface shim to the low-level operations.

The general binary rasterop function replaces a rectangular part of a
destination (``dest``) image with a bitwise combination of the pixels in
the ``dest`` and those in an arbitrary rectangle of the same size in a
source (``src``) image. The bitwise combination can be one of the
following::

   PIX_SRC                             s      (replacement)
   PIX_NOT(PIX_SRC)                   ~s      (replacement with bit inversion)
   PIX_SRC | PIX_DST                   s | d
   PIX_SRC & PIX_DST                   s & d
   PIX_SRC ^ PIX_DST                   s ^ d
   PIX_NOT(PIX_SRC) | PIX_DST         ~s | d
   PIX_NOT(PIX_SRC) & PIX_DST         ~s & d
   PIX_NOT(PIX_SRC) ^ PIX_DST         ~s ^ d
   PIX_SRC | PIX_NOT(PIX_DST)          s | ~d
   PIX_SRC & PIX_NOT(PIX_DST)          s & ~d
   PIX_SRC ^ PIX_NOT(PIX_DST)          s ^ ~d
   PIX_NOT(PIX_SRC | PIX_DST)         ~(s | d)
   PIX_NOT(PIX_SRC & PIX_DST)         ~(s & d)
   PIX_NOT(PIX_SRC ^ PIX_DST)         ~(s ^ d)

where the version on the left uses the macros that Sun originally
defined around 1981 for their Pixrect library, and the version on the
right is an obvious shorthand. The first two are independent of the data
in the ``dest``, but they are "binary" in the sense that the low-level
functions need to index into both the ``src`` and ``dest`` arrays. Of
these 14 operations, only 12 are unique. The following three operations
are identical::

   PIX_NOT(PIX_SRC) ^ PIX_DST         ~s ^ d
   PIX_SRC ^ PIX_NOT(PIX_DST)          s ^ ~d
   PIX_NOT(PIX_SRC ^ PIX_DST)         ~(s ^ d)

In addition to the 12 unique binary operations, there are two unary
rasterop functions, that operate on the ``dest`` and only depend on the
the ``dest``::

   PIX_DST                             d   (this is a no-op)
   PIX_NOT(PIX_DST)                   ~d   (bit inversion)

And finally there are two unary operations that operate on the ``dest``
and are independent of both ``src`` and ``dest``::

   PIX_CLR                             (set all bits to 0)
   PIX_SET                             (set all bits to 1)

In all, there are a total of 16 unique boolean operations. The Sun
definition of these macros, along with an analysis of how they work
properly in composition, is given in `rop.c`.  Before we go into any
details, let me explain some of the things besides image composition
that rasterop can do.

.. _what-else-rasterops:

What else can you do with rasterop?
===================================

Affine transforms are the set of linear geometrical transforms on a
two-dimensional image that encompass translation, shear, rotation and
scaling. Except for scaling, all of these operations can be implemented
using rasterop! Translation is obvious: you choose entire image as the
source block, and place it, appropriately translated, in the
destination. Shear is implemented by translating blocks of image by
different amounts. For example, you can imagine a horizontal "clockwise"
shear about the center of the image where horizontal full width blocks
are shoved to the right above the center and to the left below the
center. Blocks near the top and bottom are pushed farther than blocks
near the center; the distance a block moves horizontally increases
linearly with the vertical distance of the block from the center of the
image. Rotation is accomplished by three successive shears, alternating
in horizontal and vertical directions; the details are given in the
source code. (For small angles, a two-shear approximation to a rotation
can be used. Th resulting rotation angle is correct, but the
length-to-width ratio is altered by a fraction equal to the square of
the angle. So for a 1 degree rotation angle, the two-shear rotation
changes the length-to-width ratio by about 1/3000 -- about 1 pixel for a
typical document image.) It should be noted that all these operations
can be done *in-place*, by which we mean that the ``src`` and ``dest``
are the same image. In such situations when there is translation, care
must be taken to clear those parts of the image that are not translated.

Binary morphology is most easily implemented by full-image rasterop. A
*dilation* takes a (bit) *union* of various translates of the ``src``
image, whereas an *erosion* takes a (bit) *intersection* of
translates. Dilation and erosion are *dual* operations, in that a
dilation on the foreground is equivalent to an erosion of the
background, and v.v. However, we typically visualize binary images
non-symmetrically, with emphasis on the foreground (ON) pixels. Viewed
this way, dilation has the effect of smearing out the foreground,
whereas erosion thins the foreground and acts as a pattern matching
operation for foreground patterns. The pattern that specifies the
translations for a dilation or erosion is called a *structuring
element*. If we view a morphological operation from the vantage point of
each ``dest`` pixel, we see that the outcome (ON or OFF) depends on a
set of pixels in the ``src`` image whose positions relative to the
``dest`` pixel are given by the structuring element.

The morphological *opening* and *closing* operations are derived from
dilation and erosion: the opening is a sequence of erosion and dilation,
using the same structuring element; the closing is a dilation/erosion
sequence. Opening and closing have the particularly nice property of
*idempotence*, so that repeated opening or dilation has no further
effect. This is a filtering property that we associate with ideal sieves
or projection operators, and for this reason image morphology operations
are often called morphological *filters*. For a further introduction, go
to the section on :doc:`binary-morphology`.

Grayscale morphology is a generalization of binary morphology to images
with more than one bit/pixel, with dilation and erosion being defined as
a *max* and *min*, respectively, of a set of pixels. Binary morphology
occupies a central role in document image analysis, because
(particularly with multiscale extensions) it is able to extract both
shape and texture. For an introduction to these methods, see
:papersurl:`Multiresolution morphological approach to document image
analysis <mrm-icdar.pdf>`, published in :journal:`SPIE Conf. 1818`,
Boston, Nov. 1992.


How is rasterop implemented efficiently?
========================================

Rasterop is implemented by shifting and masking operations, that use the
low-level bit arithmetic operations available to the C compiler. These
include the binary bit logical operations (\|, &, ^), the unary bit
negation operation (~), and the bit shifting operations (<< and
>>). There are three basic things one must do to make an efficient and
flexible rasterop function.

#. **Pack the image data.** The pixels must be bit-contiguous within
   words. For example, for binary images, which have 1 bit/pixel (1
   *bpp*), 32 pixels are put in each 32-bit word.

#. **Access the data by word.** The word today is typically 32 bits.
   Using word access allows the maximum number of pixels to be affected
   by each machine operation. If and when 64-bit registers become the
   standard "word" size, the routines should be altered to handle 8
   bytes at a time.

#. **Order the image data.** The pixels, ordered from left to right,
   must be placed in bytes with the *most significant byte* (MSB) in
   each word to the left. This is required so that pixels within each
   word shift properly across byte boundaries. For big-endian machines
   (e.g., Sun) the byte order from left to right is 0123; for
   little-endian machines (e.g., Intel) the byte order is 3210. The CPUs
   are internally wired so that 32 bit words shift properly from MSB
   <--> LSB with the << and >> bit shift operators.

Using 32-bit operations, the speed of a general rasterop is
approximately 2 binary pixels/machine cycle. With a 1 GHz processor, you
can expect to operate on *2 x 10*\ :sup:`9` destination pixels/second!


What special cases have been implemented?
=========================================

It is also important to treat the special cases efficiently. For
example, suppose you know in advance that the ``src`` and ``dest``
blocks are bit-aligned within 32-bit words. A vertical block shift is
such a special case. In such a situation, a large fraction of the
shifting and masking operations are not required, and a special
low-level function for aligned blocks is used. Besides efficiency,
however, it is useful to have this function, ``rasteropVAlignedLow()``,
because the general rasterop function ``rasteropGeneralLow()`` can be
derived as a straightforward generalization of the special one. This is
a common situation, where to write the general function it is easiest
first to write and debug a simpler, special case, and then to generalize
that. An even more specialized rasterop is one where both the ``src``
and ``dest`` rectangles have their left edges on a 32-bit word boundary.
This is a common situation, such as when the rectangle comprises each
entire image, and a specialized function ``rasteropWordAlignedLow()``
handles it.

Another set of special cases are unary rasterops that operate on a
general rectangular region of a single image. There are only 3
non-trivial operations::

   PIX_CLR, PIX_SET, and PIX_NOT(PIX_DST).  

These operations are implemented as special cases of word-aligned binary
rasterops. When called with the high-level, 9 parameter
``pixRasterop()`` function, the last 3 arguments (src Pix and UL corner
coordinates) are ignored. There is even a special case of unary rasterop
where the left edge of the rectangle is aligned on a 32-bit word
boundary.

Yet another special case of unary rasterops has been implemented to
*move* pixels *in-place* within special rectangular regions. These two
functions are

+ ``rasteropVipLow()``. This does an in-place full height vertical block
  transfer, moving a set of pixel columns up or down by a given amount,
  and clearing the region that was not "blitted" into. For example, when
  a pixel column is moved down by n pixels, the lowest rows are moved
  first, and then the first n rows at the top of the column must be
  cleared.

+ ``rasteropHipLow()``. This does an in-place full width horizontal
  block transfer, moving a set of pixel rows left or right by a given
  amount, and clearing the region that was unchanged.

For example, for a vertical block transfer, the columns are moved by
copying words, properly masked, that have been shifted up or down in the
image. If the columns are moved upward, the words are taken row by row,
moving sequentially down the image, and written up a number of rows
given by the shift amount; and v.v. for shifting a column down. These
unary (in-place) block shift functions are particularly useful for
performing in-place shear and rotation of an image.

These horizontal and vertical in-place operations have been combined.
By taking the block to be moved equal to the entire image,
``pixRasteropIP()`` is the high-level function that performs an
arbitrary in-place shift of an image.

That's the big picture. We now look down at a few of the internal
details.


What is the calling sequence for rasterops?
===========================================

The top-level function ``pixRasterop()`` should be thought of as the
application programmer's interface (API) for rasterop. It is in essence
a shim that accepts pointers to the ``PIX`` data structure for the
images, along with a description of the rectangular areas to be operated
on. It extracts the image data, decides if the operation is a unary or
binary rasterop, and passes the image data to the appropriate low-level
routine::

   (9 args) pixRasterop(PIX  *pixd,
                        INT32 dx, INT32 dy, INT32 dw, INT32 dh,
                        INT32 op,
                        PIX *pixs,
                        INT32 sx, INT32 sy);

If the operation is unary, the last three arguments of ``pixRasterop()``
are ignored, and ``rasteropUniLow()`` is called with 10 arguments. The
width is scaled and the rectangle is clipped if necessary, and the
remaining 7 arguments are passed to either
``rasteropUniWordAlignedLow()`` or to the more general function
``rasteropUniGeneralLow()``. These do the work.

If the operation is binary, all the arguments in ``pixRasterop()`` are
used, and ``rasteropLow()`` is called with 16 arguments::

   (16 args) --> rasteropLow(UINT32 *datad,
                             INT32 dpixw, INT32 dpixh, INT32 depth, INT32 dwpl,
                             INT32 dx, INT32 dy, INT32 dw, INT32 dh,
                             INT32 op,
                             UINT32 *datas,
                             INT32 spixw, INT32 spixh, INT32 swpl,
                             INT32 sx, INT32 sy);

At this point, two simple operations are carried out immediately:

#. The depth of the image is set to 1 and the width is scaled
   appropriately. The rectangle size and left edge are also scaled. This
   generalizes the binary rasterop so that it can be used on an image of
   any depth.

#. The rectangle is clipped to both the ``src`` and ``dest``. This is
   done to minimize computation and prevent any operation beyond the
   array bounds. Sun's rasterop macros used a bit that determined
   whether or not clipping was enabled, presumably because they were
   typically "blitting" small character images for which no overflow
   checking was needed and they were taking all possible measures to
   save compute cycles. We ignore this flag bit and always clip the
   rectangle(s).

After width scaling and clipping (if necessary), the left edge alignment
of the rectangle in both ``src`` and ``dest`` are compared. We
distinguish three cases:

#. If they are both aligned on a 32-bit word boundary, the simple
   function ``rasteropWordAlignedLow()`` is called;

#. Else, if they have the same relative 32-bit alignment, the function
   ``rasteropVAlignedLow()`` is called;

#. Otherwise, the most general function ``rasteropGeneralLow()`` is
   called.

Each of these three functions has the same 11 arguments, e.g.::

   (11 args) --> rasteropGeneralLow(UINT32 *datad,
                                    INT32 dwpl,
                                    INT32 dx, INT32 dy, INT32 dw, INT32 dh,
                                    INT32 op,
                                    UINT32 *datas,
                                    INT32 swpl,
                                    INT32 sx, INT32 sy);

Due to the width adjustment and clipping that are performed in
``rasteropLow()``, the low-level function that does all the work,
``rasteropGeneralLow()``, does not need five of the arguments passed to
``rasteropLow()``; namely, the width, height and depth of the ``dest``
and the width and height of the ``src``.

Note that because ``rasteropLow()`` does width adjustment and clipping,
it is safe to call it directly with an arbitrary image depth and
un-clipped rectangular regions. It also makes it easier to call these
low-level functions using a different high-level shim that uses some
other packed image data structure. This separation between high-level
functions that use the Pix image data structure and low-level functions
that use only built-in C data types makes it much easier to port the
low-level functions to applications that use other image data
structures.


.. Note:: On abbreviations

   + *bpp* bits/pixel. A binary image has 1 bpp.
   + *ppi* pixels/inch. Yes, this non-metric measure shows our North
     American provincialism.

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

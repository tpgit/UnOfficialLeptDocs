:version: $RCSfile: byte-addressing.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _byte-addressing:

================================================
 Byte Addressing for Efficiency and Portability
================================================

Because the |Leptonica| library is designed to work efficiently and
transparently on both big-endian and little-endian machines, the
relation between the byte order and the image pixels must be handled
properly. Unlike computer languages or visual editors, this is not a
religious issue. It may also be unfamiliar to people in the image
processing community who have not tried to write *efficient image
processing algorithms on binary packed images for both endian
architectures*.

All hardware allows byte addressing. If we didn't care about efficiency,
and had no grayscale images with pixel depth greater than 8, we could
simply address all image data by byte. The byte order would increment in
left-to-right scan order, and from top to bottom.  We could then write
and read image data, completely oblivious to the underlying byte order
maintained within the machine for multi-byte data types (16-bit and
32-bit quantities).

If all processors were big-endian, like the Motorola and Sun hardware,
you wouldn't even be reading this. However, long ago, sometime soon
after the beginning of the computer age, Intel's engineers decided to
use a little-endian numbering scheme for bytes within a 32-bit word.
Little-endian numbering seems to be a reasonable ordering: the least
significant byte in a 32 bit word is byte 0. But this can cause problems
for efficient image processing applications.

I visualize byte ordering and the hardware as follows. For all machines,
32-bit words are held in 32-bit registers where the MSbit is on the left
and the LSbit is on the right. Left and right shifts apply to these
32-bit words. For example, right shifts will move some bits off the
right (LS) end of the word. The only difference between endians is that
for byte addressing, the two machines choose different bytes out of the
32-bit words.

This situation, where two different conventions are cognitively very
different but both widely used, is similar to the vexing problem of
units in electromagnetism. There are two widely-used units: *gaussian*
and *rationalized mks*. I prefer the former for many reasons: electric
and magnetic fields have the same units and are treated symmetrically;
the speed of light is explicit, showing the covariance of the equations
under Lorentz transformation because time is always multiplied by c and
particle velocity (e.g., currents) are always divided by c; the units of
magnetization **M**, magnetic induction **B** and field intensity **H**
are all the same; capacitance has units of distance rather than farad,
showing directly that the capacitance of a sphere is proportional to the
radius; etc. But for practical calculations in electromagnetism with
dielectrics and magnetically permeable materials, one has to use both
sets of units and the relations between them.

Back to image processing. For efficient calculations on images of all
pixel sizes, including 16 bit pixels, we want to handle the data in
the largest units possible; namely, the 32 bit machine word. We need
to shift multiple pixels simultaneously, to the left and right (also
up and down, but that's easy). When we shift pixels within words and
across word boundaries, as is done with rasterop, we require that the
shifted pixels maintain the same logical relation to their neighbors.
(Of course, when pixels are shifted between 32-bit words, we have to
do all the bookkeeping; the hardware just handles the shift within
words.) There are two ways to do this: one simple and intuitive; the
other very strange. In |Leptonica|, we have chosen the simple,
intuitive way. The image is represented in 32-bit words, and the bits
in each 32-bit word correspond to image location, from left to right,
as follows::

                 MSB       2nd MSB    3rd MSB     LSB
               xxxxxxxx | xxxxxxxx | xxxxxxxx | xxxxxxxx

   Big-endian     0           1         2          3
   Little-endian  3           2         1          0

Then, when 32-bit units are shifted, bits flow properly between
pixels. We can describe this situation by saying that *for each 32-bit
word, the bytes must be arranged in memory such that the MSB corresponds
to the left-most image byte, and the less significant bytes follow to
the right*. When the pixels are arranged this way, the byte order of the
underlying hardware is transparent for memory operations that only
address the entire 32-bit word.

Rasterops, and many other 32-bit based operations, use this organization
to handle image pixels correctly, regardless of the pixel depth (bpp).

However, endian differences become apparent when we address pixels in
sub-word quantities --- such as 1 bpp (bits), 4 bpp (nybbles), 8 bpp
(bytes) or 16 bpp (short ints) --- or when we read to or write from files.

For addressing bytes or short ints, using the above memory organization,
we get the expected left-to-right incrementing of data for big-endians,
but bytes within a word go backward for little-endians. These are
handled by the access macros in `arrayaccess.h`, that compile
differently on big-endian and small-endian machines. The 32-bit words
are cast to 8 or 16 bit pointers. For big-endian machines, the pixels
are accessed directly by index, whereas for little-endians, the index is
XORed with a small integer to handle the reversed byte order.

Macros in `arrayaccess.h` are also available to extract individual
binary pixels from the indexed 32-bit words. This is done in a manner
that is independent of the machine endian-ness, again by virtue of the
MSB-to-LSB byte ordering in the data array.

For writing and reading from files, the bytes are emitted and absorbed
in byte order determined by the machine. In order to be able to read
images written by any machine, conventions must be set relating the byte
order in the file stream to the byte order in the image. Because BMP is
a PC image file format, the header is written in little-endian order. On
the other hand, tiff allows the multi-byte header data to be written in
either order: the first two bytes are either "MM" or "II", designating
big-endian (Motorola) or little-endian (Intel), respectively. The image
data is always written such that the byte stream represents the image in
left-to-right pixel order. That is why for little-endians we must flip
the bytes in each word to get it into MSB-to-LSB order.

A summary of the byte ordering conventions in the |Leptonica| library,
including the convention for the RGBA samples in a 32-bit color pixel,
is given in `pix.h`.

If you are still a bit confused by all this, do not despair. Read on.

Consider two 32-bit words (8 bytes) in a 1 bpp image with binary packed
data. We describe *three* byte orderings within each word: internal byte
ordering; byte ordering as the image pixels go from left to right;
internal byte ordering as wired within words for left-right shifts. The
first and and third lines are always the same, because shifts are 32-bit
word based, so they move the bits across byte boundaries exactly as they
appear in the internal byte order.

First, suppose the machine is big-endian. The three orderings are as
follows::

                          xx | xx | xx | xx | xx | xx | xx | xx 
   Internal byte order     0    1    2    3    4    5    6    7
   Image l/r byte order    0    1    2    3    4    5    6    7
   Internal shift order    0    1    2    3    4    5    6    7

We have deliberately chosen the ordering of the middle line --- the
image pixels --- to agree with the others (which are determined by the
hardware). All three orderings are the same. You can address the bytes
across the image from left to right with an increasing index, by
virtue of the equivalence of the first two lines. And you can shift
image pixels left or right in the image by shifting the bits in each
word left or right, respectively, and by handling the bits transferred
between words in an easily visualized way, by virtue of the last two
lines. So you can see that if all machines were big-endian, life would
be quite simple.

Now consider the situation for little-endians. We have two choices for
the image pixel ordering. The ordering we choose is::

                          xx | xx | xx | xx | xx | xx | xx | xx 
   Internal byte order     3    2    1    0    7    6    5    4
   Image l/r byte order    3    2    1    0    7    6    5    4
   Internal shift order    3    2    1    0    7    6    5    4

Because the image byte order and the internal byte order agree, *all
operations with left or right shifts, such as rasterops, will be
identical on big-endian and little-endian machines*. We don't want to
implement all functions with shifts two times, once for big-endians and
once for little-endians! The penalty we pay on little-endians for this
choice is that for access in less than 32-bit word chunks, the pixel
order is scrambled. There is no penalty on big-endians.

However, we could have made the opposite choice for both big- and
little-endians; namely, to have the byte order within a word go from LSB
to MSB as you traverse the image data from left to right within each
word. For big-endians, we get this::

                          xx | xx | xx | xx | xx | xx | xx | xx 
   Internal byte order     0    1    2    3    4    5    6    7
   Image l/r byte order    3    2    1    0    7    6    5    4
   Internal shift order    0    1    2    3    4    5    6    7

which looks a bit crazy, because everything was just fine with the other
image byte ordering. For little-endians, we get this::

                          xx | xx | xx | xx | xx | xx | xx | xx 
   Internal byte order     3    2    1    0    7    6    5    4
   Image l/r byte order    0    1    2    3    4    5    6    7
   Internal shift order    3    2    1    0    7    6    5    4

Because the internal hardwired shift order is different from the image
data order, a left shift on image pixels requires a right shift, and,
additionally, all 32-bit masks used with the other ordering must be
bit-inverted. You can see why the shifts are reversed as follows.
Suppose you want to shift the image to the right, so that 0 goes to 1
and 3 goes to 4 in the middle line. The shift line shows you need *left*
shifts to get byte 0 into byte 1 and byte 3 into byte 4. The excess bits
that are left-shifted out of the first word from byte 3 go into the
least significant bits of byte 4 in the second word.

This is relatively hard for normal people to implement directly. If you
want to use this image pixel ordering (LSB on left and MSB on right in
the image), it is easiest to start with the |Leptonica|
implementations and reverse all shifts and masks. Rasterops will then
still work properly on both endians. On little-endians, you can access
bytes directly from left to right in the image; however, on big-endians
the bytes will now be scrambled.

Still confused? Let's try once more!

For efficient image computation and endian independence you must do two
things. The first is that you must allow shifting and masking on 32 bit
words, and they must generate the same results. Consider 8 bpp
images. Each word has 4 pixels, and you want them to be in the order
from left-to-right in the word exactly as they are in the image. Then
you can extract the left-most 8 bit pixel by right-shifting the word by
24 bits, for example. It's completely intuitive.

The endian issue comes up when you try to address a specific 8-bit pixel
in the 32-bit word. The simplest way to do this (conceptually) is to
have the MSB at the left and the LSB at the right. Then not only do
pixels shift properly within words, but they also flow in a natural way
to adjacent words.

Take the 4 pixels in a word. If we number them as they appear in the
image, from 0 to 3 in left-to-right order, these 4 pixels can be
visualized as::

   0   1   2   3

This corresponds exactly to big-endian numbering because byte 0 is the
MSB in the word. To get pixel 13 in the scanline, just take the 13th
byte in the data array for the line of the image. If all machines were
big-endian, we wouldn't even be having this discussion!

However, on little-endian machines, these 4 pixels (bytes) in the word
are numbered in the opposite direction, because byte 3 is the MSB::

   3   2   1   0

This does not correspond with the left-to-right pixel numbering! Byte 3
is still the left-most image pixel in the first word, but now if you
traverse the image from left to right, you get image bytes in the mixed
up order::

   3   2   1   0   7   6   5   4   ...


If you want to get the first byte in the image line, you must access
byte 3 of the first word. The trick to make this access endian
independent is to pretend everything is big-endian, even for little-
endians. So if you want that first byte, pretend it is byte 0, but XOR
the byte address with 3 under the covers. We do this in the accessor:
the accessor differs for big and little-endians, but the usage is endian
independent. See `arrayaccess.h` for the implementation.

Still confused? Start over at the top.

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

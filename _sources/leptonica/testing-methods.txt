:version: $RCSfile: testing-methods.rst,v $ $Revision: 63dbb54495e2 $ $Date: 2010/08/15 19:48:25 $

.. default-role:: fs

.. _`testing-methods`:

===============================
 What is "Well-Tested" C Code?
===============================

:date: Oct 7, 2007

As indicated on the copyright notice, there are no warrantees that
anything here works at all. That's the legal language. On the positive
side, much of this software has been heavily used over the past four
years, indicating that it is quite reliable. It has been subjected to
variable amounts of regression testing. Nearly every program in the
`prog` directory is a regression test, and some of the most thorough
ones, of which there are 33, have the suffix `_reg`.

I have seen estimates that commercial software has between 5 and 20
errors per 1000 lines of code. This may seem high, but many of these
errors do not result in serious bugs. Taking the low end, one might
guess that the code in the Leptonica library, which at present is about
100K lines, would have about 1000 errors. I hope it is much smaller, but
obviously cannot prove it.

To illustrate some of the methods I've used to prevent errors, consider
the rasterop implementation, which is some of the most intricate, and
hence error-prone, code you will find here. It is about 2600 lines. You
can find a thorough description of rasterop :ref:`here <rasterops>`, and
the source code is annotated with comments that should be sufficient to
understand what is happening if you know in general what it is supposed
to do.

Now rasterop, which works on packed data, has implicitly many different
cases. Besides the obvious ones of the specific logical operation that
is used, rasterop requires clipping of the source and destination
images, and a rectangular region can be taken from any arbitrary part of
the source (i.e., the left and right edges of the rectangular region can
have any possible alignment with respect to the word boundaries in the
source image) and it can be placed on any arbitrary part of the
destination (again, all possible locations of left and right edges,
relative to destination word alignment, are possible). These pieces can
vary from a few pixels in width to the entire image. For example, when
the source image fragment is very small, all pixels on a raster line may
fit within one 32-bit word, or may span two words, and likewise for the
destination image. How can one test all this?

There are really two types of tests that need to be performed. The first
is to test that the result is correct. That is the problem of "many
cases" described above. The second is to test that no illegal memory
operations are performed. These are of course related, in that if you
are fairly sure the algorithm always gives the correct answer, and it
never crashes, it is unlikely to be making serious memory errors.

Consider first the problem of correctness. We have tested this in many
ways, but the most thorough is to use rasterop to implement
:doc:`binary-morphology`. For example, consider dilation. We can dilate
an image with a structuring element (Sel) in the following two ways, and
compare the results:

+ For each *hit* in the Sel, do a union of the full image, translating
  the image for each rasterop by an amount given by the location of the
  hit relative to the center of the Sel.

+ For each ON *pixel* in the image, do a union of the image composed of
  the hits in the Sel, where the center of the Sel is aligned with the
  ON pixel.

These two methods should give identical results. For a large image with
many ON pixels, and for a variety of sizes of Sel, the second method
should give many instances of each possible combination of source and
dest image alignment. Here is a program that was written to make the
test. An image file is read, generating the internal source image
``pixs``. The outermost loop sets the Sel widths and heights to span all
sizes between the desired limits. Inside, ``pixDilate()`` uses the
standard rasterop method for dilation, given by the first method
above. Then the second method is used, where a small image of ON pixels
is generated that has the same shape as the Sel used by the first
method. The rest of the program should be self-explanatory. With a
million ON pixels in the source image, it does a million rasterops using
the small image of the Sel.

.. sourcecode:: c

   for (width = MINW; width <= MAXW; width++) {
       for (height = MINH; height <= MAXH; height++) {

           cx = width / 2;
           cy = height / 2;

               /* dilate using an actual sel */
           sel = selCreateBrick(height, width, cy, cx, HIT);
           pixd1 = pixDilate(NULL, pixs, sel);

               /* dilate using a pix as a sel */
           pixse = pixCreate(width, height, 1);
           pixSetAll(pixse);
           pixd2 = pixCopy(NULL, pixs);
           w = pixGetWidth(pixs);
           h = pixGetHeight(pixs);
           for (i = 0; i < h; i++) {
               for (j = 0; j < w; j++) {
                   pixGetPixel(pixs, j, i, &val);
                   if (val)
                       pixRasterop(pixd2, j - cx, i - cy, width, height,
                                   PIX_SRC | PIX_DST, pixse, 0, 0);
               }
           }

           pixEqual(pixd1, pixd2, &same);
           if (same == 1)
               fprintf(stderr, "Correct: results for (%d,%d) are identical!\n",
                                width, height);
           else {
               fprintf(stderr, "Error: results are different!\n");
               fprintf(stderr, "SE: width = %d, height = %d\n", width, height);
               pixWrite("junkout1", pixd1, IFF_PNG);
               pixWrite("junkout2", pixd2, IFF_PNG);
               exit(1);
           }

           pixDestroy(&pixse);
           pixDestroy(&pixd1);
           pixDestroy(&pixd2);
           selDestroy(&sel);
       }
   }

This has been used to dilate large and small images, including images
with pixels distributed somewhat randomly and extending to the
boundaries. No errors have been observed. Once we are convinced that the
rasterop is working properly, the rasterop implementation can then be
used to test the fast :ref:`destination word accumulation
<dwa-implementation-binary-morphology>` implementation method.

What about the second type of test, for illegal memory operations? The
only real test is a memory checker. This is a program that checks every
memory reference to make sure that all reads and writes are to valid
memory on the stack or allocated on the heap. These programs also note
uninitialized memory that is read, allocated memory that is not freed,
and other such pecadillos. Not all invalid memory references will cause
a program to crash. Debuggers like :cmd:`gdb` do not check memory
references; they only catch signals from the kernel that are intended to
kill the program. The real cause of a crash may be an illegal write that
put bad data in a memory address. Only later, when this is read, does
the program terminate. In 2001, a memory management debugger for
x86/Linux, called `valgrind <http://valgrind.org/>`_, became
available. The early versions worked beautifully, and it has been
continuously improved and expanded. Valgrind is very simple to use, and
provides essentially the same functionality as "purify" but at a more
reasonable price (*free: it is open source*). This is described in more
:ref:`detail <valgrind-information>`. When using valgrind, the program runs
about 50 times slower, But I have used valgrind with the test program
above (and just about every other testing program) to search
(unsuccessfully) for illegal memory operations in rasterop.

Obviously, not everything in the Leptonica library has been checked
this thoroughly, but I'm doing my best. Please let me know if you find
any problems.

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

:version: $RCSfile: skew-measurement.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _measuring-skew-document-images:

=======================================
 Measuring the Skew of Document Images
=======================================

:date: Aug 31, 2006

As with most applications of practical importance, there have been
many published papers, using diverse methods, on ways to determine the
skew of document images. It may not come as a surprise that,
notwithstanding the size of this bibliography, there is only one
method that can be recommended for both speed and accuracy. It
maximizes, in essence, the variance of differential line sums, where
the line sums are the pixel projections taken at different angles.
When the angle chosen is equal to the skew angle, the difference in
pixel projections on adjacent raster lines, when squared and summed
over all raster lines, has a maximum value. This method was first
published by W. Postl in a 1988 U.S. patent, #4,723,297.

I can't resist telling a little story here. Way back in 1991 I gave a
paper at the first ICDAR Conference, held in the beautiful medieval
town of St. Malo, France. The format had the speakers sitting at a
table at the front of the room, and I was placed next to a well-known
graybeard who had published a textbook on algorithms for image
processing way back in 1982. We started talking about our recent work,
and he said his paper was on segmenting a scanned document page that
was skewed by a few degrees. I volunteered that it would be much
harder to do that on a skewed page, and he agreed. So I asked him the
obvious question: "Why do something so difficult when there is a much
easier way to do it? Deskew the image first." (I didn't add a second
reason: that the result of segmenting a scanned image is also expected
to be much poorer if the image hasn't been deskewed.) He replied that
it would be preferable to deskew the image, but it was much too slow.
I replied that surely it took longer to segment an image than to
deskew it. No, he said, it takes at least a minute just to determine
the skew angle. I was surprised, and asked him what method he was
using for deskew. He said he was using a Hough Transform, but was
vague on the details of the search scheme. I then told him that the
skew angle could be found to sufficient accuracy in a few seconds
using Postl's variance of line sums (or of differential line sums). He
was skeptical; if what I said was true, his attempt to solve a
difficult problem was meaningless. There are several conclusions we
can draw from this tale:

#. Don't believe something just because an *eminence grise* says it is
   true --- figure it out for yourself.

#. Always look for elegant solutions. They have lasting value and
   usually teach you something important, which can be used in other
   situations as well.

#. Remember two things about computer algorithms. Computers get faster
   in accordance with *Moore's Law*, so you can assume that algorithms
   that are too slow today will eventually become practical.  But, that
   being said, at any time, it is important to search for efficient
   methods.

How fast is deskew on a 1 GHz P3 with an 8 Mpixel image (standard page
at 300 ppi) that is skewed about 1 degree? It depends on how much
accuracy you want. But if you do it at 4x reduction, which will give
you an accuracy of about 1/20 of a degree, it takes about 0.10 seconds
to find the skew angle and about 0.12 seconds to rotate the image.
That is less than 1/4 second in total. And on a 2.5 GHz P4, the entire
operation will take less than 0.1 second. Just the blink of an eye.


For further reading . . .
=========================

+ I have written :papersurl:`technical notes <docskew.pdf>` that
  summarize my understanding of the different methods and their relative
  merits and deficiencies, with emphasis (of course) on the method that
  uses the variance of differential line sums.

+ In the section on :doc:`recent publications <recent-pubs>`, you can
  find a :papersurl:`paper <skew-measurement.pdf>` where the preferred
  method for measuring skew is tested on a database of about 1000 pages.


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

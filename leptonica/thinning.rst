:version: $RCSfile: thinning.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

.. _connectivity-preserving-thinning:

==================================
 Connectivity-preserving Thinning
==================================

:date: Aug 30, 2007

.. contents::
   :local:

As with skew detection, there has been a great industry involved in
publishing papers on methods for thinning connected components in 1 bpp
images. The reason is simple: there are a great many ways to do it! Most
involve an iterative process where a subset of boundary pixels is
removed at each interation, and the subset is determined from the result
of hit-miss pattern matching. The smallest hit-miss Sels that have been
used are 3x3, and there are a very large number that can be used. I made
an attempt in 1991 to examine these 3x3 Sels systematically, and to
determine how they can be applied in combination to produce smooth
(non-dendritic) skeletons that do not have significant erosion of free
ends. That paper is :title:`Connectivity-preserving morphological image
transformations`, and it was published in :journal:`SPIE Visual
Communications and Image Processing`, :jvolume:`Conference 1606`,
pp. 320-334, November 1991, Boston, MA. A web version is also available
:papersurl:`here <conn.pdf>`.

All the 3x3 hit-miss Sels that satisfy what I've called "strong
connectivity preservation" have been extracted from this paper and
placed in `ccthin.c`. There you'll find three functions, all of which
are iterative and which have, in general, both parallel and sequential
parts within each iteration:

#. ``pixThin()``: a specific thinning method (namely, two specific sets
   of 3x3 Sels) that gives very good results, for either 4 or 8 connected
   thinning.

#. ``pixThinGeneral()``: a general thinning function that uses an
   arbitrary input set of Sels that are to be used in parallel.

#. ``pixThinExamples()``: a function that demonstrates several different
   thinnings, most of which are reasonably good, as well as a couple of
   thickenings.


All of these functions have a parallel operation that takes the union
of the hit-miss operations from a set of Sels, and subtracts this from
the image. In each iteration, this is done sequentially for four
successive clockwise 90 degree rotations of the Sels. Thus, for
example, for 8 connected thinning in ``pixThin()``, there are four Sels,
and a total of 16 hit-miss operations are required for each iteration.

Thickening the fg is equivalent to thinning the bg, using opposite
connectivity. For example, to thicken the fg while maintaining
4-connectivity, we invert the image (swap fg and bg), thin the
resulting fg using Sels that preserve 8-connectivity, and finally
invert the result. All functions take a parameter that specifies
whether we are thinning the fg or the bg.

There are two programs, `prog/ccthin1_reg` and `prog/ccthin2_reg`, that
test these functions and display both the 3x3 Sels and the results.

For further information, refer to the paper above and, as always, to
the source code.


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

:version: $RCSfile: jbig2.rst,v $ $Revision: aa1808cf90ca $ $Date: 2010/08/22 23:25:46 $

.. default-role:: fs

==================
 Jbig2 Classifier
==================

:date: Sept 27, 2008

.. contents::
   :local:

What is the origin of the Jbig2 application?
============================================

The original jbig facsimile encoder was an effort to make an improvement
over the old CCITT fax encoding standard. A little history may
help. CCITT used two different encoders, both of which computed
run-lengths (of ON pixels) followed by Huffmann encoding on the runs.
The Huffmann codes were derived from a set of 8 binary images, scanned
at 200 ppi. None of the 8 images had halftones, and one consequence is
that the CCITT encodings work very poorly on halftone images. One
encoder, G3 (for Group 3), was specifically designed to work in the
presence of uncorrected fax errors. It was originally 1-dimensional,
encoding each raster line individually. It had a special end-of-line
symbol. If an error occurred in a raster line, determined by a check of
some error detection bits, it would just copy the previous line.  This
limited the error propagation to typically a single line. The second
encoder, G4 (for Group 4), was designed to work with much better
compression on an error-free communication channel. It was
two-dimensional, in that it encoded the runs in each line relative to
the runs in the line above, and it omitted the end-of-line symbols. It
could not be used for fax because any error would be propagated through
the rest of the page. Later, the G3 encoder was improved by adopting up
to 4 lines of two-dimensional encoding. The first line would use the
original one-dimensional G3 method, and the next 1 to 3 lines would use
a modified G4 method, still preserving the end-of-line symbols.

This remained the state of the art for nearly 20 years. jbig encoding
of binary images was designed in the early '90s to give better
lossless compression on error-free channels. It could thus not be used
on ordinary fax, because fax modems were not designed to correct all
errors. However, given the existence of 33.6 KHz data modems, which
have very low error rates on typical phone lines, there is no reason
why jbig could not be used on modified fax machines that used data
modems. Things didn't work out that way, however. New fax machines
were not built, and problems arose in the jbig standardization
process. I have heard several "sides" of the fiasco, and I believe the
main problem was that IBM held several critical patents on arithmetic
coding of the image, which prevented others from freely implementing
the standard.

In the mid to late 90s, the jbig2 compression standard was proposed.
Although there is a lossless mode for jbig2, it would typically be used
for lossy (but "visually lossless") compression. It also requires an
error-free channel, so that the main applications would be compression
of scanned binary images, and perhaps image transmission on internet
fax. Because the standard needed to be written for maximum flexibility,
jbig2 can be used for grayscale or color images. However, the most
practical use of jbig2 with grayscale or color images is for the
compression of a binary layer in a *mixed raster* format (MR format;
more on this :ref:`below <mixed-raster-format>`). The image and data can
be compressed in a variety of ways; the best is probably to do
everything with arithmetic coding. The final ISO draft specifications
for jbig2 were published in 1999, and can be found at
http://www.jpeg.org/jbig/jbigpt2.html.


What is jbig2?
==============

From here on, when I refer to "jbig2" it is to the generic method of
compression, not to the specific file format in the ISO draft. jbig2
builds a dictionary of shapes from the connected components in the
image. It does this with an *unsupervised classifier*: shapes that are
sufficiently similar are placed in the same class, and every instance
of that shape in the image is rendered using a single representative
image, or *template*. This is particularly effective for compressing
text documents, which are composed of connected components
representing characters from a limited set of fonts and font styles.
Further, the compression efficiency generally improves with longer
documents, because the templates need only be stored once. Documents
compressed with jbig2 are typically between 10K and 15K bytes/page,
which is about 5 times better compression that that achievable with
CCITT/G4.

A jbig2 implementation consists of these three steps:


#. The connected components (either 4 or 8 connected) are identified.

#. The components are placed in similarity classes, using an
   unsupervised classifier. Each class has an image template as a
   representative. The location of each instance is recorded.

#. The templates and the (index, location) triples are compressed and
   written to file. If done according to the ISO draft, the templates are
   compressed using arithmetic coding and the triplets are compressed
   using arithmetic or Huffmann coding on coordinate differences.

We provide the first two steps, which are the low-level imaging part
of the encoder. For the third step, Leptonica gives you the option of
tiling the templates in a single image written in png format, and
writing the uncompressed (index, location) triples for each instance
into a second file.

For the classification step, the goal is to do a minimal *over*\
classification. We are willing to split some classes, as long as we
never put two truly different characters into the same class. The
over-classification results in a loss of efficiency, which is in the
best case relatively small, and is compensated by avoiding substitution
errors.


What is provided in Leptonica?
==============================

We provide implementations of two different classifiers. One is based
on image *correlation*. The correlation method compares two bitmaps by
computing the ratio of the square of the number of pixels in the AND
of the two bitmaps to the product of the number of ON pixels in each.
This ratio has a maximum of 1 when the two bitmaps are identical and
properly aligned. *All pixels that differ in the two bitmaps are
weighted equally in the correlation method*. We provide two
parameters: a base threshold on the correlation and a weight factor
that increases the threshold for templates that have a larger fraction
of ON pixels. Judicious use of these two parameters will result in
visually lossless substitutions.

Another classifier that results in roughly the same image quality for
the same number of classes is based on *hausdorff distance*. This
comparator gives a (yes/no) answer to the question of whether the two
bitmaps are within a certain *distance* of each other. We can speak of
a hausdorff "distance" between two images because the hausdorff forms
a true metric. The hausdorff method is theoretically better for this
application because it tolerates differences in the bitmap shapes near
the foreground/background boundary. In effect, it gives a small
effective weight to boundary pixels and a large effective weight to
pixels that are farther from the boundary. This weighting is expected
statistically because the difference in two printed and scanned
instances of a character occur almost entirely at the boundary. Thus,
the Hausdorff weighting corresponds better to the expected
probabilities of pixel values in scanned images.

However, in practice for typical font sizes scanned at 300 ppi, this
advantage is not achieved, and the reason is interesting. The hausdorff
comparator can result in class confusion for small characters, and
particularly for very small components such as dots.  The latter look
bad when there are halftone dots on the page from which templates can be
selected. To avoid the class confusion, it is necessary to choose a
hausdorff distance less than 1. As a result, all pixels become of
roughly equal importance.

Nevertheless, we do provide a *rank* hausdorff comparator, which is a
generalization of the hausdorff comparator that permits a match if some
fraction of the pixels exceeds the given hausdorff distance. In
practice, for scanned text at 300 or 400 ppi, we suggest using 2x2 Sel
with a rank value of about 0.97. For other applications, such as
comparison of word images in *document image summarization*, where a few
different words can be put in the same class in order to avoid the worse
error of splitting a word equivalent class, it is useful to use a larger
Sel and a smaller value of the rank order.)

The main problem with the rank hausdorff method, as mentioned above,
is that if there are a lot of very small components, such as from a
halftone image, it is necessary to choose dilation with a 2x2
structuring element to avoid choosing bad templates. This is a very
small dilation, and furthermore it is not symmetric. It corresponds to
a hausdorff distance of 0 in two directions (say, north and west) and
1 in the other two. To avoid expanding the number of classes too far,
it is then necessary to choose a rank value of about 0.97. A value of
about 0.95 can cause substitutions, whereas a value of about 0.99 will
result in too many classes. Even without small halftone dots in the
image, use of a 3x3 structuring element, which corresponds to a
hausdorff distance of 1, can result in obvious confusions. For
example, the small letter 'o' can be confused with the italic 'o' in
the same font: when the centroids are lined up, a small 'o' and a
small italic 'o' can have a hausdorff distance of 1, even using a
strict match with rank = 1.0! So if absolute accuracy is required, one
needs to use either a 2x2 Sel with an appropriate rank value for
hausdorff, or else use a correlation comparator.


.. _hausdorff-distance-definition:

What is the definition of the hausdorff distance, and how is it implemented efficiently?
========================================================================================

The hausdorff distance between two images A and B is defined as
follows. After the images are aligned, find the distance of the pixel in
B that is farthest from any pixel in A, and v.v. Each of those distances
is called the *directed hausdorff distance* from one image to another,
and the hausdorff distance is the maximum of the directed distances. Two
images whose pixels differ only at the boundaries will have a small
hausdorff distance. The comparator is implemented efficiently by
dilating first one image by a structuring element of a given size,
testing whether the other image fits within it, and then carrying out
the same procedure with the two images reversed. For example, if the two
images are to be tested to see if they are within a hausdorff distance
of 1, a 3x3 structuring element is used; for a distance of 2, a 5x5 is
used, etc. A hausdorff distance of 1 is a good parameter to use for the
jbig2 character classifier.


How are the images aligned for comparison?
==========================================

To use either of these comparators, it is necessary to align the two
images. The easiest way to align is by using a corner. However, because
the corners are delimited by boundary pixels, which are variable from
instance to instance, this would introduce considerable variability in
the alignment. Two images could easily be misaligned by up to two pixels
in either direction. A much better way to do alignment is by aligning
the centroids. Centroid alignment averages over many boundary pixels,
greatly reducing the statistical error, so that when aligning to the
nearest (integer) pixels, the alignment error is usually less than 1/2
pixel in either direction. It certainly gives an accuracy that is
adequate for the unsupervised classification.

In the final step where each instance is re-aligned with the class
template in order to derive the coordinates where the *template* should
be placed to substitute for the instance, it turns out that for about
25% of the instances, the correlation score can be improved by moving
the instance one pixel up or down from the position where the centroids
are aligned. (The correlation score is given by minimizing the XOR
between the two binary images.) It's a little expensive to check for
nine positions before making the final placement of each instance, but
it's worth doing.


What's special about the Leptonica implementation?
==================================================

Well, you say, "Big deal. Get the connected components, compare them,
and you're done." And it's true that this prescription for a
classifier is quite simple. But there are a number subtleties
(features, lurking buglets, and efficiencies) in the implementation
that are very important.

+ Wouldn't it be nice if the classes corresponded to characters rather
  than connected components? This would simplify the process if it were
  used as part of an OCR system.

+ How do you choose the image comparator, including the parameters?
  Too loose and you corrupt the classes; too tight and the number of
  classes explodes.

+ How do you place the templates when substituting for each instance
  in the compressed file version? The eye is extremely sensitive to
  wobbling baselines, and can sense any inaccuracy in the vertical
  position of a character.

+ When trying to decide if a new instance matches some existing
  template, or is to become a template for a new class, how do you
  prevent the process from exploding linearly with the number of
  templates? And how is the match done efficiently between an instance
  and an individual template?

These questions and others are implicit in the low-level part of the
jbig2 encoder provided here, which has the following useful features:

+ It allows you to use as components for classification either the
  connected components, the characters, or the words.

+ It is accurate in the identification of templates and classes
  because it uses either correlation or a windowed rank hausdorff
  distance metric.

+ It is accurate in the placement of the connected components, because
  it aligns the centroids of the template with those of each instance,
  and then if required, does a final adjustment (e.g., for rendering) by
  minimizing the number of pixels not matched.

+ It is relatively fast because for the hausdorff distance it uses a
  morphologically based matching algorithm, and for both correlation and
  hausdorff it does the measurement once where the centroids are
  aligned. It also makes comparisons only with templates that are nearly
  the same size as the instance, and chooses those templates through a
  size-based hashing function that greatly limits the number of matches,
  even for a document with hundreds of pages.


Open source implementation of jbig2
===================================

Adam Langley has released an open source jbig2-compliant encoder, the
first one yet built. It uses leptonica to classify similar elements,
generate the templates representing each cluster, and compute the offset
for rendering each instance using its template. You can get this at
http://github.com/agl/jbig2enc.

Langley's implementation uses arithmetic encoding throughout for the
images. It can encode binary images losslessly with a single
arithmetic coding over the full image. It also does both lossy and
lossless encoding from connected components, using the clusters found
with unsupervised classification. To build the encoder, use the most
recent version (0.26). This bundles liblept-1.53, but you can use more
recent versions as well. Once you've built the encoder, you can use it
to compress a set of input image files: e.g.::

   ./jbig2 -v -s [imagefile1 ...]  >   [jbig2_file]

You can also generate a pdf wrapping for the output jbig2. To do that,
call cmd:`jbig2` with the -p arg, which generates a symbol file
(output.sym) plus a set of location files for each input image
(output.0000, ...)::

   ./jbig2 -v -s -p [imagefile1 ...]

and then generate the pdf::

   python pdf.py output  >  [pdf_file]

See the `usage documentation <http://github.com/agl/jbig2enc>`_ for the
jbig2 compression. You can uncompress the jbig2 files using
:cmd:`jbig2dec`, which can be downloaded and built from `here
<http://jbig2dec.sourceforge.net/>`_.

.. _mixed-raster-format:

What is Mixed Raster format?
============================

For pages with mixed text and graphics/images, jbig2 is the best choice
for the compression of the text layer, which is usually called the
*foreground* layer in a more general MR format. MR format is a general
way to represent an image for compression. It is composed of an ordered
set of (mask, image) pairs. It works by painting the first image through
the first mask, then overlaying the painting of the second image through
the second mask, and so forth.

The best implementation of MR format is the open DjVu format, for which
there exists both `proprietary
<http://www.celartem.com/en/products/djvu.asp>`_ and `open source
<http://djvu.sourceforge.net/>`_ implementations. The DjVu format
uses a restriction of the general MR format to three layers: a
foreground mask (e.g., the text), a foreground image (the image painted
through the text mask; often black), and a background image.  The
background image is painted first, and the masked foreground image is
overlaid. Typically, the background image is represented at about 100
ppi, the foreground image at 25 ppi, and the foreground mask at 300 --
400 ppi.

The DjVu format uses a jbig2-type classifier for the foreground mask,
and compresses the templates in that mask using an arithmetic coder.  It
compresses both the foreground and background images using
wavelets. There are several tricky parts, such as the method by which
the foreground and background are segmented, and the method of
compressing the background image in the presence of the high resolution
foreground mask that obscures parts of it. Many of the details and a
reference open source `implementation <http://djvu.sourceforge.net/>`_
can be found at `djvu.org <http://djvu.org>`_.


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

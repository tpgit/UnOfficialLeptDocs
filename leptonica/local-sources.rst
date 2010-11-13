:version: $RCSfile: local-sources.rst,v $ $Revision: 0631ab298a88 $ $Date: 2010/11/11 15:38:02 $

=============================
 Source Code and Information
=============================

:date: Nov 9, 2010

.. epigraph::

   | The road to wisdom? -- Well, it's plain
   | and simple to express:
   |     Err
   |     and err
   |     and err again
   |     but less
   |     and less
   |     and less.

         --Piet Hein :unconverted:`(Grooks)
         <cachedpages/grooks/grooks.html>`


This site contains :ref:`well-tested <testing-methods>` C code for some
basic image processing operations, along with a description of the
functions and some design methods. A full set of affine transformations
(*translation*, *shear*, *rotation*, *scaling*) on images of all depths
is included, with the exception that some of the scaling methods do not
work at all depths. There are also implementations of binary morphology,
grayscale morphology, convolution and rank order filters, and
applications such as jbig2 image processing and color quantization.

You will also find basic utilities for the safe and efficient handling
of arrays (of strings, numbers, number pairs and image-related
geometrical objects), byte queues, generic stacks, generic lists, and
endian-independent indexing into 32-bit arrays.

There are summaries of the files in the :doc:`src <src-dir>` and
:doc:`prog <prog-dir>` directories with short descriptions of each file.
You can use these to quickly get an idea of where you may find a needed
function or see how to use it.

See :ref:`image-processing-operations` and
:ref:`image-processing-applications` for more detailed information that
expands on what's present in the source files.


Download
========

Click :ref:`here <source-downloads>` to download the source. [**update:
Nov 9, 2010**]

Be sure to download the :ref:`README` as well.

If you are building the library and applications on Windows, read the
:ref:`developer notes <vs2008-notes>` by Tom Powers and download his
Microsoft Visual Studio package from :ref:`here
<microsoft-visual-studio-download>`. [**--new: Jan 5, 2010**]

You may also find these pages useful:

+ brief notes on the :ref:`version history <version-notes>`
+ information on the :ref:`library contents and usage <library-notes>`
+ an explanation of the :ref:`byte-ordering conventions
  <byte-addressing>` used in the |Leptonica| library


Related Publications
====================

Here are some references to selected :ref:`papers <recent-pubs>` on image
processing and image analysis that you might find interesting.

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

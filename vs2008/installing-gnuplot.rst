:version: $RCSfile: installing-gnuplot.rst,v $ $Revision: 9edcdd8f1ac9 $ $Date: 2010/03/30 15:49:08 $

.. default-role:: fs

==================================
 Installing gnuplot to view plots
==================================

Leptonica uses `gnuplot <http://www.gnuplot.info/>`_ to display
plots. Download the standard gnuplot Windows version (:bi:`not` the
Windows X11 version unless you know what you are doing). Besides
installing gnuplot you have to set the following environment variables:

1. Add `c:\\gnuplot\\bin` to your system's ``PATH``.

#. Create a new environment variable called ``GDFONTPATH`` and set it to
   `c:/windows/fonts`

#. Create a new environment variable called ``GNUPLOT_FONTPATH`` and
   also set it to `c:/windows/fonts`

After showing a plot, the calling program will pause until both the
plot window and gnuplot window are closed.

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

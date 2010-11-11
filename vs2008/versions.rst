:version: $RCSfile: versions.rst,v $ $Revision: c86e54b7d564 $ $Date: 2010/11/11 05:20:26 $

.. default-role:: fs

===============
 Version Notes
===============

1.67 -- November 10, 2010
=========================

+ The webp image format is not supported under Visual Studio 2008 since
  libwebp doesn't support building with Visual C++.

+ Added the following files to the :guilabel:`leptonlib-1.67` Project::
	
   convertfiles.c
   sudoku.c
   sudoku.h
   webpio.c
   webpiostub.c

+ Added the following files to :guilabel:`prog_files` Solution Folder::

   graymorph1_reg.c
   graymorph2_reg.c
   projection_reg.c
   sudokutest.c
   writemtiff.c

+ Removed the following files from :guilabel:`prog_files` Solution
  Folder::

   graymorph_reg.c

+ Added descriptions of the following files to `srcs.csv` file::

   convertfiles.c
   endianness.h
   sudoku.c
   sudoku.h
   webpio.c
   webpiostub.c

+ Removed descriptions of the following files from `progs.csv` file::

   graymorph_reg.c

+ Added descriptions of the following files to `progs.csv` file::

   graymorph1_reg.c
   graymorph2_reg.c
   projection_reg.c
   sudokutest.c
   writemtiff.c

1.66 -- August 9, 2010
======================

+ Updated VS2008notes:

  + Added a :ref:`Quickstart <quickstart>` section.

  + Reorganized now that it's possible to use the |leptonlib|
    :doc:`binaries for Windows zip file <downloading-binaries>` instead
    of having to build all the libraries.

  + Updated :doc:`build instructions <building-image-libraries>` for
    `libtiff 3.9.4`, `libjpeg 8b`, `libpng 1.4.3`, and `zlib 1.2.5`.

  + Added information on :doc:`Visual Studio 2010 compatibility
    <vs2010-notes>`.

+ Removed definitions of ``COMPILER_MSVC=1`` and ``USE_PSTDINT`` from
  all projects.

+ Changed the :guilabel:`leptonlib-1.66` Project to be more compatible
  with Visual Studio 2010.

  + For :guilabel:`Lib Debug` and :guilabel:`Lib Release` configurations
    reset linker and librarian :guilabel:`Output File` property to
    default to avoid VC++ 2010 problems.

  + Removed the conditional :guilabel:`Custom Build Step` and added an
    unconditional :guilabel:`Post-Build Event` to avoid VC++ 2010 bug
    where setting :guilabel:`Outputs` causes the linker to be invoked
    when building `leptonlib`. See `VC++ in VS2010 fails if there is a
    command to copy lib file in 'Custom Build Step'
    <http://connect.microsoft.com/VisualStudio/feedback/details/557340/vc-in-vs2010-fails-if-there-is-a-command-to-copy-lib-file-in-custom-build-step>`_
    for details.

+ Added the following files to the :guilabel:`leptonlib-1.66` Project::
	
   dewarp.c
   dewarp.h
   leptwin.c
   leptwin.h
   pix5.c
   ptabasic.c
   ptafunc1.c
   spixio.c

+ Added the following files to :guilabel:`prog_files` Solution Folder::

   alphaxform_reg.c
   convolve_reg.c
   dewarp_reg.c
   dewarptest.c
   findpattern_reg.c
   livre_adapt.c
   livre_hmt.c
   livre_makefigs.c
   livre_orient.c
   livre_pageseg.c
   livre_seedgen.c
   livre_tophat.c
   otsutest1.c
   otsutest2.c
   overlap_reg.c

+ Removed the following files from :guilabel:`prog_files` Solution
  Folder::

   pagesegtest3.c

+ Added descriptions of the following files to `srcs.csv` file::

   dewarp.c
   dewarp.h
   leptwin.c
   leptwin.h
   pix5.c
   ptabasic.c
   ptafunc1.c
   spixio.c

+ Removed descriptions of the following files from `progs.csv` file::

   otsutest.c
   pagesegtest3.c

+ Added descriptions of the following files to `progs.csv` file::

   alphaxform_reg.c
   convolve_reg.c
   dewarp_reg.c
   dewarptest.c
   findpattern_reg.c
   livre_adapt.c
   livre_hmt.c
   livre_makefigs.c
   livre_orient.c
   livre_pageseg.c
   livre_seedgen.c
   livre_tophat.c
   otsutest1.c
   otsutest2.c
   overlap_reg.c


1.65 -- April 07, 2010
======================

+ Added the following files to the :guilabel:`leptonlib-1.65` Project::
	
   gifio.c
   regutils.c
   regutils.h

+ Added the following files to :guilabel:`prog_files` Solution Folder::

   alltests_reg.c
   alphaclean_reg.c
   dwalinear.3.c
   dwalineargen.c
   dwalinearlow.3.c
   maze_reg.c
   pixa1_reg.c
   pixa2_reg.c
   psio_reg.c
   rankbin_reg.c
   rankhisto_reg.c
   shear2_reg.c
   warpertest.c

+ Removed the following files from :guilabel:`prog_files` Solution
  Folder::

   affinetest.c
   binmazetest.c
   graymazetest.c
   pixa_reg.c
   plotprog.c

+ Added descriptions of the following files to `srcs.csv` file::

   gifio.c
   regutils.c
   regutils.h

+ Added descriptions of the following files to `progs.csv` file::

   alltests_reg.c
   alphaclean_reg.c
   dwalinear.3.c
   dwalineargen.c
   dwalinearlow.3.c
   maze_reg.c
   pixa1_reg.c
   pixa2_reg.c
   psio_reg.c
   rankbin_reg.c
   rankhisto_reg.c
   shear2_reg.c
   warpertest.c

+ Added `CreateLeptonicaProgProjects.AddIn`,
  `CreateLeptonicaProgProjects.zip`, and `CreateLPP.dll` to `vs2008`
  directory. Implements VS2008 add-in to automatically create Project
  for currently selected `prog/` file(s).

+ Added :guilabel:`DLL Debug` and :guilabel:`DLL Release` build
  configurations.
	
+ Updated VS2008notes:

  + Converted documentation over to ReStructured Text. Sphinx is used to
    generate the HTML files.

  + The `vs2008\\` folder is no longer part of standard Leptonica releases.

  + Explained the use of the new `CreateLeptonicaProgProjects` AddIn.

  + Updated instructions to the latest versions of `libjpeg`, `libpng`,
    and `zlib`.

  + Added enabling `giflib` support section.


1.64 -- Jan 05, 2010
====================

Initial Release.

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

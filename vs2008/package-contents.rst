:version: $RCSfile: package-contents.rst,v $ $Revision: b84e08108423 $ $Date: 2011/03/03 07:29:25 $

.. default-role:: fs

==================
 Package Contents
==================

This package consists of the following files:

`leptonica.sln`
   |liblept| Visual Studio 2008 Solution. See :doc:`vs2008-solution` for
   more information.

`leptonica.vcproj`
   |liblept| Visual Studio 2008 Project.

`leptonica_versionnumbers.vsprops`
   Visual Studio Property Sheet that contains ``*_VERSION`` user macros
   that simplify specifying possibly changing library filenames to the
   linker. See :ref:`about-version-numbers` for more information.

`liblept.rc`
   Version resource file (used to display the :guilabel:`Version` tab on
   the `liblept`\ |vnumF|\ `.dll` Properties dialog).

`resource.h`
   Header file for `liblept.rc`. 

`prog_projects\\`
   `ioformats_reg` Visual Studio 2008 Project. See
   :doc:`building-prog-dir` for more information.

`doc\\`
   Documentation for using |liblept| and Visual Studio 2008.

`CreateLeptonicaProgProjects.AddIn`
   Visual Studio 2008 AddIn definition file. See
   :ref:`using-create-prog-project-addin` for more information.

`CreateLeptonicaProgProjects.zip`
   Source for the Create Leptonica `prog\\` Projects AddIn.

`CreateLPP.dll`
   The Create Leptonica `prog\\` Projects AddIn.

`LeptonicaVS2008Samples.zip`
   Examples showing how to call liblept from c#. See
   :doc:`csharp-and-liblept` for more information.

`checkprogs.py`
   Python script that checks for new or removed `prog\\` programs using
   `progs.csv`.

`checksrc.py`
   Python script that:

   + checks for new or removed `src\\` files.
   + makes sure that all `src\\` files are in `liblept.vcproj`.

`progs.csv`
   Categorized list of programs in the `prog\\` folder.

`srcs.csv`
   Categorized list of files in the `src\\` folder.

`jpeg-8c-vs2008.zip`
   jpeg-8b Visual Studio 2008 Solution and Project file. See
   :ref:`building-libjpeg` for more information.

`libtiff3.9.4-vs2008-makefiles-for-leptonica.zip`
   libtiff3.9.4 makefiles modified for use with |liblept|.  See
   :ref:`building-libtiff` for more information.

`giflib4.1.6.zip`
   giblib-4.1.6 Visual Studio 2008 Solution and Project file.  See
   :ref:`building-giflib` for more information.

`create_unnumbered_hardlinks.bat`
   Batch file to create simplified library filenames using NTFS
   hardlinks.  See :ref:`about-version-numbers` for more information.

`remove_unnumbered_hardlinks.bat`
   Batch file to remove simplified library filenames created by
   `create_unnumbered_hardlinks.bat`

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

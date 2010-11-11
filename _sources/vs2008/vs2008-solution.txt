:version: $RCSfile: vs2008-solution.rst,v $ $Revision: 26bd0c5c4b08 $ $Date: 2010/08/14 01:12:28 $

.. default-role:: fs

=============================================
 The |leptonlib| Visual Studio 2008 Solution
=============================================

.. image:: images/leptonlib-solution-explorer.png
   :align: center
   :alt: Screenshot of Leptonlib Solution Explorer pane

The Visual Studio 2008 Solution Explorer shows these three main
sections for the |leptonlib| solution:

1. :guilabel:`leptonlib-`\ |versionG| is the main project for building
   the library.

#. The `prog_projects` Solution Folder contains a sample project for
   building a `prog` program. As explained :ref:`later
   <building-prog-programs-vs2008>` you can use this project as the
   basis for building projects for the other programs in the `prog`
   directory.

#. The `prog_files` Solution Folder contains entries for all the `.c`
   files in the `leptonlib-`\ |versionF|\ `\\prog` folder further broken
   down by filename, type, and category. These are :bi:`not` Visual
   C/C++ projects.  You can't use this Solution Folder to build the
   `prog` programs. It just gives you an easy way to look at the files.

.. note::

   The free Express editions of Visual Studio do **not** support
   Solution Folders. They will be displayed as
   :guilabel:`(unavailable)`.


`leptonlib.sln` Solution Explorer contents
==========================================

.. parsed-literal::
    
   leptonlib-|version|\\            Main project for building leptonlib
    Header files\\
    Source files\\
   prog_files\\                Solution Folder (NOT projects) for prog directory contents
    ByFilename\\
    ByCategory\\
     Basic Box, Boxa and Boxaa Functions\\
     Basic Image Operations\\
     Basic Pix Array Functions\\
     Basic Pix Functions\\
     Colormap Utilities and Related Operations\\
     Connected Components in Binary Images\\
     Formatted IO\\
     Fundamental Data Structures for Computation\\
     Image Display\\
     Image Morphology\\
     Image Operations With Filling\\
     Image Quantization, Depth Conversion\\
     Image Scaling\\
     Line Graphics and Special Output\\
     Low-level Pixel Access\\
     Misc\\
     Other Geometric Image Transformations\\
     Postscript\\
     Printing\\
     Specialized Document Image Processing\\
     Specialized Image Filters\\
    ByType
     Example\\
     Exploration\\
     Helper\\
     Regression Test\\
     Test\\
     Utility\\
   proj_projects              Projects for building prog programs
    ioformats_reg\\
     Source Files

`BuildFolder\\leptonlib-`\ |versionF| contents
==============================================

::
    
   config\                    Not used for Windows builds
   prog\                      Regression tests, examples, utilities
   src\                       Source files for leptonlib  
   vs2008\                    Visual Studio 2008 specific files
    DLL Debug\                 leptonlib DLL Debug build output
    DLL Release\               leptonlib DLL Release build output
    LIB Debug\                 leptonlib LIB Debug build output
    LIB Release\               leptonlib LIB Release build output
    prog_projects\             Projects for prog programs
     ioformats_reg\             Sample project for prog\ioformats_reg.exe
      DLL Debug\                 DLL Debug build output for sample project
      DLL Release\               DLL Release build output for sample project
      LIB Debug\                 LIB Debug build output for sample project
      LIB Release\               LIB Release build output for sample project
      ioformats_reg.vcproj       The ioformats_reg project file
    leptonlib.sln              The leptonlib solution file
    leptonlib.vcproj           The leptonlib project file

Visual Studio 2008 Tab settings
===============================

The |leptonlib| source files assume that tabs are 8 spaces, indents are
4 spaces wide, and that indentation uses spaces and tabs. To set this in
Visual Studio 2008 choose :menuselection:`&Tools --> &Options`
:guilabel:`| Text Editor | C/C++ | Tabs` and set as follows:

   |   :guilabel:`&Tab Size:` 8
   |   :guilabel:`&Indent Size:` 4
   |   :guilabel:`(*) Insert S&paces`
   |   :guilabel:`( ) &Keep Tabs`

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

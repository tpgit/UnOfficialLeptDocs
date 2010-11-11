:version: $RCSfile: vs2010-notes.rst,v $ $Revision: 26bd0c5c4b08 $ $Date: 2010/08/14 01:12:28 $

.. default-role:: fs

.. _vs2010-notes:

==========================
 Visual Studio 2010 Notes
==========================

* Programs built with Visual Studio 2010 can link with the **static** binary
  libraries supplied in the |leptonlib| :doc:`Visual Studio 2008
  pre-built binaries for Windows archive <downloading-binaries>`.

  For reasons unclear to me you have to rebuild the DLL versions of
  |leptonlib| using Visual Studio 2010. If you don't, simple things
  like::

        fp = fopen(filename, "rb"); /* in ioformats_reg.c */
         ...
        rewind(fp);                 /* in leptonlib.dll */

  will cause crashes. It must have something to do with the C Runtime
  Library DLLs but I can't figure out what yet. Luckily :doc:`building
  <building-leptonlib>` |leptonlib| is pretty easy (it's rebuilding all
  the static image libraries that's the tough part).

* When converting the VS2008 Solution, you'll get a number of warnings
  like the following in the Conversion Report::

    MSB8012: $(TargetName) ('leptonlib-1.66') does not match the Linker's OutputFile property value 'DLL Release\leptonlib.dll' ('leptonlib') in project configuration 'DLL Release|Win32'. This may cause your project to build incorrectly. To correct this, please make sure that $(TargetName) property value matches the value specified in %(Link.OutputFile).

  Fix the |leptonlib| project by doing the following:

  1. Right-click on :guilabel:`leptonlib-`\ |versionG| and choose
     :menuselection:`P&roperties`.

  #. Then change :guilabel:`leptonlib-`\ |versionG| :guilabel:`Property
     Pages | General | Target Name` to :guilabel:`leptonlib` for the DLL
     Release configuration or :guilabel:`leptonlibd` for the DLL Debug
     configuration.

  The `ioformats_reg` project also needs to be fixed:

  1. Right-click on :guilabel:`ioformats_reg` and choose
     :menuselection:`P&roperties`.

  #. From the :guilabel:`&Configuration` dropdown menu choose
     :guilabel:`All Configurations`.

  #. Change :guilabel:`ioformats_reg Property Pages | Linker | General |
     Output File` to :guilabel:`$(OutDir)$(TargetName)$(TargetExt)`.

  Exit and restart Visual Studio (or close and reopen the |leptonlib|
  solution).

* To use the "Create Leptonica prog Project AddIn" follow the
  :ref:`instructions <building-prog-programs-vs2008>` for Visual
  Studio 2008 but copy `vs2008\CreateLeptonicaProgProjects.AddIn`
  and `vs2008\CreateLPP.dll` to your Visual Studio 2010 Addins folder
  (normally `C:\\My Documents\\Visual Studio 2010\\Addins`).

  Edit `CreateLeptonicaProgProjects.AddIn` and change::

     <Version>9.0</Version>
 
  to::

     <Version>10.0</Version>

* The :doc:`building <building-image-libraries>` of the image libraries
  has not been tested using Visual Studio 2010. Given the problems
  encountered while building |leptonlib| you can probably expect to have
  some issues.


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

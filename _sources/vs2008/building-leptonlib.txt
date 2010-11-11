:version: $RCSfile: building-leptonlib.rst,v $ $Revision: 440c6687684b $ $Date: 2010/11/09 23:19:38 $

.. default-role:: fs

.. _building-leptonlib:

=============================================
 (Optional) Building the |leptonlib| library
=============================================

Assuming that you've :doc:`downloaded <downloading-binaries>` or
:doc:`built <building-image-libraries>` the requisite image libraries,
building |leptonlib| itself is straightforward since a Visual Studio
solution file is provided.

1. Download the latest version of leptonica from `here
   <http://www.leptonica.com/download.html>`__. Extract the archive to
   the |BuildFolder| directory. You should now have:

   .. parsed-literal::

      BuildFolder\\
        giflib-4.1.6\\
        include\\
        jpeg-8b\\
        leptonlib-|version|\\
        lib\\
        libtiff-3.9.4\\
        lpng143\\
        zlib\\

#. Download the Microsoft Visual Studio 2008 build package from `here
   <http://www.leptonica.com/download.html#VS2008>`__. Extract the
   archive to the `BuildFolder\\leptonlib-`\ |versionF| directory. You
   should now have:

   .. parsed-literal::

      BuildFolder\\
        include\\
        leptonlib-|version|\\
          vs2008\\
        lib\\
        tiff-3.9.4\\

#. `leptprotos.h` has the wrong declaration for
   ``setPixMemoryManager()`` under Windows. Change it from::

      LEPT_DLL extern void setPixMemoryManager ( void * ( allocator (size_t ) ), void  ( deallocator ( void * ) ) );

   to::

      LEPT_DLL extern void setPixMemoryManager (void *((*allocator)(size_t)), void ((*deallocator)(void *)) );

#. Copy all the `.h` header files from `leptonlib-`\ |versionF|\ `\\src`
   to `BuildFolder\\include\\leptonica`.

#. Open `BuildFolder\\leptonlib-`\ |versionF|\ `\\vs2008\\leptonlib.sln` with Visual
   Studio 2008.

#. Select the desired build configuration (either :guilabel:`LIB Debug`,
   :guilabel:`LIB Release`, :guilabel:`DLL Debug`, or :guilabel:`DLL
   Release` and probably :guilabel:`Win32`).

   :guilabel:`LIB Debug` builds use the following C compiler options::

      /Od /I "..\..\include"
      /D "WIN32" /D "_DEBUG" /D "_LIB" /D "L_LITTLE_ENDIAN"
      /D "snprintf=_snprintf" /D "XMD_H"
      /FD /EHsc /RTC1 /MDd /Fo"LIB Debug\\" /Fd"LIB Debug\vc90.pdb"
      /W3 /nologo /c /Z7 /errorReport:prompt

   :guilabel:`LIB Release` builds use the following C compiler options::

      /O2 /I "..\..\include"
      /D "WIN32" /D "NDEBUG" /D "_LIB" /D "L_LITTLE_ENDIAN"
      /D "snprintf=_snprintf" /D "XMD_H" /D "NO_CONSOLE_IO"
      /FD /EHsc /MD /Fo"LIB Release\\" /Fd"LIB Release\vc90.pdb"
      /W3 /nologo /c /errorReport:prompt

   :guilabel:`DLL Debug` builds use the following C compiler options::

       /Od /I "..\..\include"
       /D "WIN32" /D "_DEBUG" /D "_USRDLL" /D "_WINDLL" 
       /D "LEPTONLIB_EXPORTS" /D "L_LITTLE_ENDIAN"
       /D "snprintf=_snprintf" /D "XMD_H"
       /FD /EHsc /RTC1 /MDd /Fo"DLL Debug\\" /Fd"DLL Debug\vc90.pdb"
       /W3 /nologo /c /Z7 /errorReport:prompt

   :guilabel:`DLL Release` builds use the following C compiler options::

       /O2 /I "..\..\include"
       /D "WIN32" /D "NDEBUG" /D "_USRDLL" /D "_WINDLL"
       /D "LEPTONLIB_EXPORTS" /D "L_LITTLE_ENDIAN"
       /D "snprintf=_snprintf" /D "XMD_H" /D "NO_CONSOLE_IO"
       /FD /EHsc /MD /Fo"DLL Release\\" /Fd"DLL Release\vc90.pdb"
       /W3 /nologo /c /errorReport:prompt

   All configurations turn off some warnings with the following
   options::

      /wd4244 /wd4305 /wd4018 /wd4267 /wd4996

#. Right-click :guilabel:`leptonlib-`\ |versionG| in the Solution Explorer and
   Choose :menuselection:`B&uild` or :menuselection:`R&ebuild` from the
   context menu (Choosing :menuselection:`&Build --> &Build Solution`
   (:kbd:`F6`) or :menuselection:`&Build --> &Rebuild Solution` from the
   Visual Studio menubar will result in `ioformats_reg` also being
   built). The resultant library will automatically be copied to
   `BuildFolder\\lib`.

   The libraries are named as follows:

   +----------------+-----------------------------------+----------------------------------+
   |                |           Debug Builds            |         Release Builds           |
   +================+===================================+==================================+
   | Static library | leptonlib-static-mtdll-debug.lib  | leptonlib-static-mtdll.lib       |
   +----------------+-----------------------------------+----------------------------------+
   | DLL            | | leptonlibd.lib (import library) | | leptonlib.lib (import library) |
   |                | | leptonlibd.dll                  | | leptonlib.dll                  |
   +----------------+-----------------------------------+----------------------------------+

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

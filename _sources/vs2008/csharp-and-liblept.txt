:version: $RCSfile: csharp-and-liblept.rst,v $ $Revision: ab7f322f4578 $ $Date: 2011/02/08 03:40:07 $

.. default-role:: fs

==================
 c# and |liblept|
==================

`vs2008\\LeptonicaVS2008Samples.zip` contains a sample Visual Studio
Solution which shows how simple it is to call |liblept| functions from
c# (or any other .NET language). Unpack it to |BuildFolder|. You should
have:

.. parsed-literal::

   BuildFolder\\
     include\\
     leptonica-|version|\\
     LeptonicaVS2008Samples\\
       deskew1bpp\\
       LeptonicaCLR\\
       TestLeptonica\\
       LeptonicaVS2008Samples.sln
     lib\\

:cmd:`deskew1bpp` is a standard C++ Win32 Console program, using
precompiled headers, C++ strings, Unicode support, and ATL macros to
convert Unicode to null-terminated C strings. In other words, it's a
typical Visual C++ style program. :cmd:`deskew1bpp` demonstrates the
problems with directly rotating 1bpp images. It shows how first
converting a b&w image to gray, block convolving, rotating using area
mapping, and then thresholding back to b&w yields better results.

`LeptonicaCLR` contains the same basic functionality as
:cmd:`deskew1bpp` but written in C++/CLI. In fact two of the routines,
``renderCC()`` and ``binImageDiff()``, are copied verbatim from
`deskew1bpp.cpp` showing how easy it is to port C/C++ to C++/CLI. The
resultant DLL is a bridge between the native |liblept| library and the
.NET Common Language Runtime (CLR). It calls native code while at the
same time exposing functions to c#. The main difference from a normal
DLL is that `LeptonicaCLR.cpp` is compiled with the ``/clr`` switch.

:cmd:`TestLeptonica` is a c# program that has a Reference to the
`LeptonicaCLR` DLL to demonstrate calling |liblept| functions from
c#. It does a bit of argument checking and then calls
``LeptonicaCLR.Utils.DeskewBinaryImage()`` to actually deskew a b&w
image. If you want to be able to step into |liblept| functions while
debugging c#, just right-click the :guilabel:`TestLeptonica` project and
choose :menuselection:`P&roperties`. Then make sure :guilabel:`Debug |
Enable unmanaged code debugging` is checked.

You'll notice that the |liblept| project is also included in this
Solution. As explained :ref:`above <intellisense-and-liblept>`, that's
to allow Visual Studio's Intellisense to correctly navigate to
|liblept| function definitions.

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

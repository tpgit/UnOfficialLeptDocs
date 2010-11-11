:version: $RCSfile: installing-irfanview.rst,v $ $Revision: 9edcdd8f1ac9 $ $Date: 2010/03/30 15:49:08 $

.. default-role:: fs

=====================================
 Installing IrfanView to view images
=====================================

The ``pixDisplay()`` function is used throughout |leptonlib| to display
images for debugging purposes. Under Windows this uses the free
`IrfanView <http://www.irfanview.com/>`_ image viewer application. We
have to assume the presence of IrfanView because many Leptonica routines
don't use file extensions when naming files. Since Windows depends on
the file extension to determine a file's type (unlike Linux), it is
unable to automatically determine what application to use when opening
extensionless files. In addition, unlike other Windows image viewers
(for example, `ACDSee's Photo Manager
<http://store.acdsee.com/store/acd/en_US/DisplayProductDetailsPage/productID.106
893200>`_), IrfanView will correctly display an image file even if it
doesn't have an extension.

Besides installing IrfanView, you also have to add the location of
`i_view32.exe` (normally `C:\\Program Files\\IrfanView`) to your
system's ``PATH`` environment variable.

Each time ``pixDisplay()`` is called, it will display an image using
IrfanView and wait for it to be closed. You can hit the :kbd:`<Escape>`
key to quickly close IrfanView.

Alternatively, you can manually edit ``pixDisplayWithTitle()`` in
`src\\writefile.c` to change the executable used to display images under
Windows.

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

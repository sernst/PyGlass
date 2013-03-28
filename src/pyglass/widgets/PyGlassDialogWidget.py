# PyGlassDialogWidget.py
# (C)2012-2013
# Scott Ernst

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ PyGlassDialogWidget
class PyGlassDialogWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PyGlassDialogWidget."""
        PyGlassWidget.__init__(self, parent, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: canceled
    @property
    def canceled(self):
        return self.dialogWindow.canceled if self.dialogWindow else False

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ closeDialog
    def closeDialog(self):
        if not self.dialogWindow:
            return False
        self.dialogWindow.successClose()
        return True

#___________________________________________________________________________________________________ cancelDialog
    def cancelDialog(self):
        if not self.dialogWindow:
            return False
        self.dialogWindow.cancelClose()
        return True

# LineSeparatorWidget.py
# (C)2013
# Scott Ernst

from PySide import QtGui

#___________________________________________________________________________________________________ LineSeparatorWidget
class LineSeparatorWidget(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, horizontal =True, color =None, **kwargs):
        """Creates a new instance of LineSeparatorWidget."""
        QtGui.QWidget.__init__(self, parent)
        if horizontal:
            self.setFixedHeight(1)
        else:
            self.setFixedWidth(1)

        if not color:
            color = QtGui.QColor.fromHsvF(0, 0, 0, 0.1)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

# PyGlassOverlay.py
# (C)2014
# Scott Ernst

from PySide import QtCore
from PySide import QtGui
from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.PyGlassElement import PyGlassElement

#___________________________________________________________________________________________________ PyGlassOverlay
class PyGlassOverlay(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, name, parent =None, **kwargs):
        """Creates a new instance of PyGlassOverlay."""
        super(PyGlassOverlay, self).__init__(parent=parent, **kwargs)
        self.name = name
        self._manager = ArgsUtils.get('manager', None, kwargs)
        self._backColor = QtGui.QColor(0, 0, 0, 200)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: manager
    @property
    def manager(self):
        return self._manager
    @manager.setter
    def manager(self, value):
        self._manager = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ changeSize
    def changeSize(self, width, height):
        """changeSize doc..."""
        self.move(0, 0)
        self.setFixedSize(width, height)
        self.updateGeometry()
        self.update()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, event):
        if not self._backColor:
            return

        p = QtGui.QPainter(self)
        p.setPen(QtCore.Qt.NoPen)

        brush = QtGui.QBrush(self._backColor)
        p.setBrush(brush)

        p.drawRect(0, 0, self.size().width(), self.size().height())

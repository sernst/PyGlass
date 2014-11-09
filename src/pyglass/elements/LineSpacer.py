# LineSpacer.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui
from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ LineSpacer
class LineSpacer(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    SOLID_LINE  = 'solid'
    DASHED_LINE = 'dashed'
    DOTTED_LINE = 'dotted'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of LineSpacer."""
        super(LineSpacer, self).__init__(parent)
        self._lineType   = kwargs.get('lineType', self.SOLID_LINE)
        self._isVertical = kwargs.get('isVertical', False)
        self._color      = QtGui.QColor(255, 255, 255, 255)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: lineType
    @property
    def lineType(self):
        return self._lineType
    @lineType.setter
    def lineType(self, value):
        self._lineType = value
        self._updateDisplay()

#___________________________________________________________________________________________________ GS: color
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value
        self._updateDisplay()

#___________________________________________________________________________________________________ GS: isVertical
    @property
    def isVertical(self):
        return self._isVertical
    @isVertical.setter
    def isVertical(self, value):
        if self._isVertical == value:
            return
        self._isVertical = value
        self._updateDisplay()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, event):
        """paintEvent doc..."""

        p = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(self.color)

        if self.lineType == self.DASHED_LINE:
            pen.setDashPattern((6, 6))
        elif self.lineType == self.DOTTED_LINE:
            pen.setDashPattern((2, 2))
        p.setPen(pen)

        if self.isVertical:
            p.drawLine(1, 0, 1, self.size().height())
        else:
            p.drawLine(0, 1, self.size().width(), 1)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateDisplay
    def _updateDisplay(self):
        """_updateDisplay doc..."""
        if self.isVertical:
            self.setFixedSize(3, self.maximumHeight())
        else:
            self.setFixedSize(self.maximumWidth(), 3)
        self.update()

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__



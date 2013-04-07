# ColorQValue.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyaid.color.ColorValue import ColorValue

#___________________________________________________________________________________________________ ColorQValue
class ColorQValue(ColorValue):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, sourceColor, normalized =False, opacity =1.0):
        """Creates a new instance of ColorQValue."""
        super(ColorQValue, self).__init__(sourceColor, normalized, opacity)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: qColor
    @property
    def qColor(self):
        color = QtGui.QColor.fromRgba(self._rawColor)
        color.setAlphaF(self._opacity)
        return color


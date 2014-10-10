# ColorQValue.py
# (C)2013-2014
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

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ compareQColors
    @classmethod
    def compareQColors(cls, color1, color2):
        if not color1 or not color2:
            return False

        if color1.redF() != color2.redF():
            return False
        elif color1.greenF() != color2.greenF():
            return False
        elif color1.blueF() != color2.blueF():
            return False

        return True

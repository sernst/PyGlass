# IconElement.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.enum.SizeEnum import SizeEnum

#___________________________________________________________________________________________________ IconElement
class IconElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ICON_SIZES  = [16, 20, 24, 32]
    _ICON_SHEETS = dict()

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, *args, **kwargs):
        """Creates a new instance of IconElement."""
        super(IconElement, self).__init__(parent, **kwargs)

        self._mapCoords = ArgsUtils.get('icon', [0, 0], kwargs, args, 0)
        self._size      = ArgsUtils.get('size', SizeEnum.MEDIUM, kwargs)
        self._sizeIndex = [SizeEnum.SMALL, SizeEnum.MEDIUM, SizeEnum.LARGE, SizeEnum.XLARGE].index(self._size)
        self._isDark    = ArgsUtils.get('dark', True, kwargs)
        self._opacity   = ArgsUtils.get('opacity', 1.0, kwargs)

        size = self._ICON_SIZES[self._sizeIndex]
        self.setFixedSize(size, size)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isDark
    @property
    def isDark(self):
        return self._isDark
    @isDark.setter
    def isDark(self, value):
        if bool(self._isDark) == bool(value):
            return
        self._isDark = bool(value)
        self.repaint()

#___________________________________________________________________________________________________ GS: opacity
    @property
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        if value == self._opacity:
            return
        self._opacity = value
        self.repaint()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
        """Doc..."""
        painter   = QtGui.QPainter(self)
        painter.setOpacity(self._opacity)
        iconSize  = self._ICON_SIZES[self._sizeIndex]
        iconSheet = self._getIconSheet()
        if not self._isDark:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Lighten)
        else:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Multiply)

        iconX = iconSize*self._mapCoords[1]
        iconY = iconSize*self._mapCoords[0]
        painter.drawPixmap(
            0, 0, iconSize, iconSize, iconSheet, iconX, iconY, iconSize, iconSize
        )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getIconSheet
    def _getIconSheet(self):
        key = str(self._sizeIndex) + '-' + str(self._isDark)
        if key not in self._ICON_SHEETS:
            self._ICON_SHEETS[key] = QtGui.QPixmap(PyGlassEnvironment.getPyGlassResourcePath(
                'icons-%s-%s.png' % (
                    'dark' if self._isDark else 'light', str(self._ICON_SIZES[self._sizeIndex])
            ), isFile=True))
        return self._ICON_SHEETS[key]


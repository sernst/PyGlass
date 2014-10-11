# IconElement.py
# (C)2013-2014
# Scott Ernst

from PySide import QtGui
from PySide import QtCore

from pyaid.ArgsUtils import ArgsUtils
from pyaid.dict.DictUtils import DictUtils

from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.themes.ColorQValue import ColorQValue

#___________________________________________________________________________________________________ IconElement
class IconElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, name =None, atlas =None, **kwargs):
        """Creates a new instance of IconElement."""
        super(IconElement, self).__init__(parent, **kwargs)
        self._name       = name
        self._atlas      = atlas
        self._definition = None
        self._opacity    = ArgsUtils.get('opacity', 1.0, kwargs)
        self._color      = None
        self._scale      = 1.0

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: textureScale
    @property
    def textureScale(self):
        return None
    @textureScale.setter
    def textureScale(self, value):
        if self._scale == value:
            return
        self._scale = value
        self._refreshTexture()

#___________________________________________________________________________________________________ GS: color
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if ColorQValue.compareQColors(value, self._color):
            self._color = value
            return
        self._color = value
        self.repaint()

#___________________________________________________________________________________________________ GS: definition
    @property
    def definition(self):
        return self._definition

#___________________________________________________________________________________________________ GS: name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if self._name == value:
            return
        self._name = value
        self._refreshTexture()

#___________________________________________________________________________________________________ GS: atlas
    @property
    def atlas(self):
        return self._atlas
    @atlas.setter
    def atlas(self, value):
        if self._atlas == value:
            return
        self._atlas = value
        self._refreshTexture()

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
        if not self._definition or not self.atlas:
            return

        d     = self._definition
        image = self.atlas.image
        img = QtGui.QImage()

        x           = int(round(self._scale*float(d.x)))
        y           = int(round(self._scale*float(d.y)))
        width       = int(round(self._scale*float(d.width)))
        height      = int(round(self._scale*float(d.height)))
        frameX      = int(round(self._scale*float(d.frameX)))
        frameY      = int(round(self._scale*float(d.frameY)))
        frameWidth  = int(round(self._scale*float(d.frameWidth)))
        frameHeight = int(round(self._scale*float(d.frameHeight)))

        if not self._color:
            painter = QtGui.QPainter(self)
            painter.scale(self._scale, self._scale)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            painter.setOpacity(self.opacity)
            painter.drawImage(0, 0, image, d.x, d.y, d.width, d.height)
            painter.end()
            return

        pix     = QtGui.QPixmap(frameWidth, frameHeight)
        painter = QtGui.QPainter(pix)
        painter.scale(self._scale, self._scale)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.fillRect(0, 0, d.frameWidth, d.frameHeight, QtCore.Qt.transparent)

        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.setOpacity(self.opacity)
        painter.drawImage(-d.frameX, -d.frameY, image, d.x, d.y, d.width, d.height)

        painter.setOpacity(1.0)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(0, 0, d.frameWidth, d.frameHeight, QtGui.QColor(100, 100, 100))

        painter.end()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.drawPixmap(0, 0, pix)

#___________________________________________________________________________________________________ echo
    def echo(self):
        return unicode(self) + u': ' + DictUtils.prettyPrint({
            'DEF':self._definition,
            'ATLAS':self.atlas,
            'NAME':self.name,
            'SIZE':(self.size().width(), self.size().height()) })

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _refreshTexture
    def _refreshTexture(self):
        if not self.name or not self.atlas:
            return

        self._definition = self.atlas.getDefinition(self.name)
        if not self._definition:
            return

        self.setFixedSize(
            int(round(self._scale*float(self._definition.frameWidth))),
            int(round(self._scale*float(self._definition.frameHeight))) )
        self.repaint()


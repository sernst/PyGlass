# ResizableImage.py
# (C) 2014
# Scott Ernst

import math

from PySide import QtCore
from PySide import QtGui

from pyglass.elements.PyGlassElement import PyGlassElement

#___________________________________________________________________________________________________ ResizableImage
class ResizableImage(PyGlassElement):

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, pixmap =None, **kwargs):
        super(ResizableImage, self).__init__(parent=parent, **kwargs)
        self._pixmap    = None
        self.pixmap     = pixmap
        self._scale     = 1.0
        self._xOffset   = 0
        self._yOffset   = 0

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: xOffset
    @property
    def xOffset(self):
        return self._xOffset

#___________________________________________________________________________________________________ GS: yOffset
    @property
    def yOffset(self):
        return self._yOffset

#___________________________________________________________________________________________________ GS: imageScale
    @property
    def imageScale(self):
        return self._scale

#___________________________________________________________________________________________________ GS: pixmap
    @property
    def pixmap(self):
        return self._pixmap
    @pixmap.setter
    def pixmap(self, value):
        if self._pixmap == value:
            return
        self._pixmap = value
        self.setMaximumHeight(value.size().height() if value else 16777215)
        self._updateLayoutData()

#___________________________________________________________________________________________________ GS: aspectRatio
    @property
    def aspectRatio(self):
        if not self._pixmap or self._pixmap.isNull():
            return 1.0
        s = self._pixmap.size()
        return float(s.width())/float(s.height())

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ sizeHint
    def sizeHint(self, *args, **kwargs):
        if not self._pixmap or self._pixmap.isNull():
            return super(ResizableImage, self).sizeHint(*args, **kwargs)
        s = self._pixmap.size()
        return QtCore.QSize(s.width(), s.height())

#___________________________________________________________________________________________________ heightForWidth
    def heightForWidth(self, width):
        if not self._pixmap or self._pixmap.isNull():
            return super(ResizableImage, self).heightForWidth(width)

        size = self._pixmap.size()
        scale = float(width)/float(size.width())
        return math.ceil(scale*float(size.height()))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateLayoutData
    def _updateLayoutData(self, size =None):
        if not self._pixmap or self._pixmap.isNull():
            return

        if size is None:
            size = self.size()

        pixmapSize = self._pixmap.size()

        pw = float(pixmapSize.width())
        ph = float(pixmapSize.height())
        w  = float(size.width())
        h  = float(size.height())

        oldScale        = self._scale
        self._scale     = min(1.0, w/pw, h/ph)
        self._xOffset   = round(0.5*(w - self._scale*pw))
        self._yOffset   = round(0.5*(h - self._scale*ph))

        if oldScale == self._scale:
            return

        self.updateGeometry()
        self.update()

#___________________________________________________________________________________________________ _resizeImpl
    def _resizeImpl(self, event):
        super(ResizableImage, self)._resizeImpl(event)
        self._updateLayoutData(event.size())

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, event):
        super(ResizableImage, self)._paintImpl(event)

        if not self._pixmap or self._pixmap.isNull():
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.scale(self._scale, self._scale)
        painter.drawPixmap(self._xOffset, self._yOffset, self._pixmap)

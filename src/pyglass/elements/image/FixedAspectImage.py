# FixedAspectImage.py
# (C) 2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtCore
from PySide import QtGui

from pyglass.elements.PyGlassElement import PyGlassElement


#___________________________________________________________________________________________________ FixedAspectImage
class FixedAspectImage(PyGlassElement):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, pixmap =None, aspectRatio =1.25, preferredWidth =-1, **kwargs):
        super(FixedAspectImage, self).__init__(parent=parent, **kwargs)

        self._preferredWidth = preferredWidth
        self._aspect         = aspectRatio
        self._pixmap         = None
        self._scale          = 1.0
        self._xOffset        = 0
        self._yOffset        = 0

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        self.pixmap = pixmap

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: preferredWidth
    @property
    def preferredWidth(self):
        return self._preferredWidth
    @preferredWidth.setter
    def preferredWidth(self, value):
        if self._preferredWidth == value:
            return
        self._preferredWidth = value
        self._updateLayoutData()

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
        return self._aspect

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ sizeHint
    def sizeHint(self, *args, **kwargs):
        if not self._pixmap or self._pixmap.isNull():
            return super(FixedAspectImage, self).sizeHint(*args, **kwargs)

        w = self.preferredWidth if self.preferredWidth > 0 else float(self._pixmap.size().width())
        h = w/self.aspectRatio
        return QtCore.QSize(round(w), round(h))

#___________________________________________________________________________________________________ heightForWidth
    def heightForWidth(self, width):
        return round(float(width)/self.aspectRatio)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateLayoutData
    def _updateLayoutData(self, size =None):
        if not self._initialized:
            return

        if not self._pixmap or self._pixmap.isNull():
            return

        if size is None:
            size = self.size()

        pixSize = self._pixmap.size()

        pw = float(pixSize.width())
        ph = float(pixSize.height())
        w  = float(size.width())
        h  = float(size.height())

        oldScale        = self._scale
        oldXOff         = self._xOffset
        oldYOff         = self._yOffset
        self._scale     = min(1.0, w/pw, h/ph)
        self._xOffset   = round(0.5*(w - self._scale*pw))
        self._yOffset   = round(0.5*(h - self._scale*ph))

        if oldScale != self._scale and oldXOff != self._xOffset and oldYOff != self._yOffset:
            self.updateGeometry()
            self.update()

#___________________________________________________________________________________________________ _resizeImpl
    def _resizeImpl(self, event):
        super(FixedAspectImage, self)._resizeImpl(event)
        self._updateLayoutData(event.size())

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, event):
        super(FixedAspectImage, self)._paintImpl(event)

        if not self._pixmap or self._pixmap.isNull():
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.scale(self._scale, self._scale)
        painter.drawPixmap(
            round(self._xOffset/self._scale),
            round(self._yOffset/self._scale),
            self._pixmap)
        painter.end()


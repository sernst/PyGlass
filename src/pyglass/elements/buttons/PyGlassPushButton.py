# PyGlassPushButton.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import math

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.buttons.InteractiveButtonBase import InteractiveButtonBase
from pyglass.elements.icons.IconElement import IconElement
from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum
from pyglass.enum.SizeEnum import SizeEnum
from pyglass.themes.ThemeColorBundle import ThemeColorBundle
from pyglass.themes.ColorSchemes import ColorSchemes

#___________________________________________________________________________________________________ PyGlassPushButton
class PyGlassPushButton(InteractiveButtonBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ROUNDNESS   = [4, 6, 8, 8]
    _MARGINS     = [(10, 5), (12, 6), (16, 8), (20, 10)]
    _LINE_WIDTH  = 2
    _GLOSS_QCOLORS = (
        QtGui.QColor(255, 255, 255, 100),
        QtGui.QColor(255, 255, 255, 75),
        QtGui.QColor(255, 255, 255, 50),
        QtGui.QColor(255, 255, 255, 0) )
    _LABEL_STYLE = "QLabel { color:#C#; font-weight:500; font-size:#FS#px; }"
    _FONT_SIZES  = [10, 14, 16, 20]

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, *args, **kwargs):
        """Creates a new instance of PyGlassPushButton."""
        super(PyGlassPushButton, self).__init__(parent, **kwargs)
        labelText               = ArgsUtils.get('text', '', kwargs, args, 0)
        self._size              = ArgsUtils.get('size', SizeEnum.MEDIUM, kwargs)
        self._sizeIndex         = [
            SizeEnum.SMALL, SizeEnum.MEDIUM, SizeEnum.LARGE, SizeEnum.XLARGE
        ].index(self._size)
        self._colorScheme       = ArgsUtils.get('colorScheme', None, kwargs)
        self._toggleColorScheme = ArgsUtils.get('toggleColorScheme', None, kwargs)
        self._normalBundle      = ArgsUtils.get('normalColors', None, kwargs, args, 1)
        self._overBundle        = ArgsUtils.get('overColors', None, kwargs)
        self._pressBundle       = ArgsUtils.get('pressColors', None, kwargs)
        self._disabledBundle    = ArgsUtils.get('disabledColors', None, kwargs)
        self._activeBundle      = ArgsUtils.get('toggleColors', None, kwargs)
        self._populateColorBundles()

        layout  = self._getLayout(self, QtGui.QHBoxLayout)
        margins = self._MARGINS[self._sizeIndex]
        layout.setContentsMargins(margins[0], margins[1], margins[0], margins[1])
        layout.addStretch()

        iconPosition = ArgsUtils.get('icon', None, kwargs)
        if iconPosition:
            icon = IconElement(self, iconPosition, size=self._size)
            layout.addWidget(icon)
            self._icon = icon
        else:
            self._icon = None

        label = QtGui.QLabel(self)
        label.setText(labelText)
        label.setVisible(len(labelText) > 0)
        layout.addWidget(label)
        self._label = label

        layout.addStretch()

        self.sizePolicy().setControlType(QtGui.QSizePolicy.ToolButton)
        self._updateDisplay()
        self.layout().setSpacing(3)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: shrink
    @property
    def shrink(self):
        return self.sizePolicy().horizontalPolicy() == QtGui.QSizePolicy.Maximum
    @shrink.setter
    def shrink(self, value):
        hPolicy = QtGui.QSizePolicy.Maximum if value else QtGui.QSizePolicy.Preferred
        self.setSizePolicy(hPolicy, self.sizePolicy().verticalPolicy())

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ text
    def text(self):
        return self._label.text()

#___________________________________________________________________________________________________ setText
    def setText(self, value):
        self._label.setText(value)
        self._updateDisplay()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, event):
        size   = self.size()
        w      = size.width()
        h      = size.height()
        halfW  = math.ceil(float(w)/2.0)
        halfH  = math.ceil(float(h)/2.0)
        bundle = self._getColorBundle()
        matrix = QtGui.QMatrix()
        matrix.translate(halfW, halfH)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        #--- MAIN FILL ---#
        gradient = QtGui.QLinearGradient(halfW, -halfH - 1, halfW, halfH + 1)
        gradient.setColorAt(0.0, bundle.light.qColor)
        gradient.setColorAt(1.0, bundle.dark.qColor)

        brush = QtGui.QBrush(gradient)
        brush.setMatrix(matrix)

        pen = QtGui.QPen()
        pen.setWidth(self._LINE_WIDTH)
        col = bundle.strong.clone()
        col.opacity = 0.25*bundle.strong.opacity
        pen.setColor(col.qColor)

        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(
            self._LINE_WIDTH,
            self._LINE_WIDTH,
            w - 2*self._LINE_WIDTH,
            h - 2*self._LINE_WIDTH,
            self._ROUNDNESS[self._sizeIndex],
            self._ROUNDNESS[self._sizeIndex] )

        #--- EDGE HIGHLIGHT ---#

        pen   = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(self._GLOSS_QCOLORS[1])

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(pen)
        painter.drawRoundedRect(
            self._LINE_WIDTH + 1,
            self._LINE_WIDTH + 1,
            w - 2*self._LINE_WIDTH - 2,
            h - 2*self._LINE_WIDTH - 2,
            self._ROUNDNESS[self._sizeIndex],
            self._ROUNDNESS[self._sizeIndex] )

        #--- SPECULAR GLOSS ---#
        gradient = QtGui.QLinearGradient(halfW, -halfH - 1, halfW, halfH + 1)
        gradient.setColorAt(0.0, self._GLOSS_QCOLORS[0])
        gradient.setColorAt(0.5, self._GLOSS_QCOLORS[2])
        gradient.setColorAt(0.51, self._GLOSS_QCOLORS[-1])

        brush = QtGui.QBrush(gradient)
        brush.setMatrix(matrix)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRoundedRect(
            self._LINE_WIDTH,
            self._LINE_WIDTH,
            w - 2*self._LINE_WIDTH,
            h - 2*self._LINE_WIDTH,
            self._ROUNDNESS[self._sizeIndex],
            self._ROUNDNESS[self._sizeIndex] )

#___________________________________________________________________________________________________ _populateColorBundles
    def _populateColorBundles(self):
        if not self._normalBundle:
            self._normalBundle = ThemeColorBundle(
                self._colorScheme if self._colorScheme else ColorSchemes.GREY)

        if not self._disabledBundle:
            self._disabledBundle = self._normalBundle.clone()
            self._disabledBundle.opacityShift(-0.33)

        if not self._overBundle:
            self._overBundle = self._normalBundle.clone()
            self._overBundle.opacityShift(-0.33)
            if not self._pressBundle:
                self._pressBundle = self._normalBundle.clone()
                self._pressBundle.hsvShift(h=0, s=0, v=-40)
        elif not self._pressBundle:
            self._pressBundle = self._overBundle.clone()
            self._pressBundle.hsvShift(h=0, s=0, v=-40)
        if not self._activeBundle:
            if self._toggleColorScheme:
                self._activeBundle = ThemeColorBundle(self._toggleColorScheme)
            else:
                self._activeBundle = self._normalBundle.clone(invert=True)

#___________________________________________________________________________________________________ _updateDisplayImpl
    def _updateDisplayImpl(self):
        bundle = self._getColorBundle()
        self._label.setStyleSheet(
            self._LABEL_STYLE.replace(
                '#C#', bundle.strong.asWebRgbOpacity(None if self.isEnabled() else 0.5)).replace(
                '#FS#', str(self._FONT_SIZES[self._sizeIndex]) ))
        if not self._label.isVisible() and self._label.text():
            self._label.setVisible(True)
        elif self._label.isVisible() and not self._label.text():
            self._label.setVisible(False)

        if self._icon:
            self._icon.opacity = 1.0 if self.isEnabled() else 0.5
            self._icon.isDark = not bundle.isDark

#___________________________________________________________________________________________________ _getFirstNone
    @classmethod
    def _getFirstNone(cls, *args):
        for arg in args:
            if arg is not None:
                return arg
        return None

#___________________________________________________________________________________________________ _getColorBundle
    def _getColorBundle(self):
        """Doc..."""
        if not self.isEnabled():
            return self._getFirstNone(self._disabledBundle, self._normalBundle)

        if self.checked:
            return self._getFirstNone(self._activeBundle, self._normalBundle)
        elif self._mode == InteractionStatesEnum.PRESS_MODE:
            return self._getFirstNone(self._pressBundle, self._overBundle, self._normalBundle)
        elif self._mode == InteractionStatesEnum.OVER_MODE:
            return self._getFirstNone(self._overBundle, self._pressBundle, self._normalBundle)

        return self._normalBundle

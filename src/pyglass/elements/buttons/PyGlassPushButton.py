# PyGlassPushButton.py
# (C)2013
# Scott Ernst

import math

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.buttons.InteractiveButtonBase import InteractiveButtonBase
from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum
from pyglass.themes.ThemeColorBundle import ThemeColorBundle
from pyglass.themes.ColorSchemes import ColorSchemes

#___________________________________________________________________________________________________ PyGlassPushButton
class PyGlassPushButton(InteractiveButtonBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ROUNDNESS   = 8
    _LINE_WIDTH  = 2
    _GLOSS_QCOLORS = (
        QtGui.QColor(255, 255, 255, 100),
        QtGui.QColor(255, 255, 255, 75),
        QtGui.QColor(255, 255, 255, 50),
        QtGui.QColor(255, 255, 255, 0)
    )
    _LABEL_STYLE = "QLabel { color:#C#; font-weight:500; font-size:14px; }"

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, *args, **kwargs):
        """Creates a new instance of PyGlassPushButton."""
        super(PyGlassPushButton, self).__init__(parent, **kwargs)
        labelText               = ArgsUtils.get('text', u'', kwargs, args, 0)
        self._colorScheme       = ArgsUtils.get('colorScheme', None, kwargs)
        self._toggleColorScheme = ArgsUtils.get('toggleColorScheme', None, kwargs)
        self._normalBundle      = ArgsUtils.get('normalColors', None, kwargs, args, 1)
        self._overBundle        = ArgsUtils.get('overColors', None, kwargs)
        self._pressBundle       = ArgsUtils.get('pressColors', None, kwargs)
        self._disabledBundle    = ArgsUtils.get('disabledColors', None, kwargs)
        self._activeBundle      = ArgsUtils.get('toggleColors', None, kwargs)
        self._populateColorBundles()

        layout = self._getLayout(self, QtGui.QVBoxLayout)
        layout.setContentsMargins(12, 6, 12, 6)

        label = QtGui.QLabel(self)
        label.setText(labelText)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(label)
        self._label = label

        self._updateDisplay()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ text
    def text(self):
        return self._label.text()

#___________________________________________________________________________________________________ setText
    def setText(self, value):
        self._label.setText(value)
        self._updateDisplay()

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
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
        col.opacity = 0.25
        pen.setColor(col.qColor)

        painter.setBrush(brush)
        painter.setPen(pen) #QtCore.Qt.NoPen)
        painter.drawRoundedRect(
            self._LINE_WIDTH,
            self._LINE_WIDTH,
            w - 2*self._LINE_WIDTH,
            h - 2*self._LINE_WIDTH,
            self._ROUNDNESS,
            self._ROUNDNESS
        )

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
            self._ROUNDNESS,
            self._ROUNDNESS
        )

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
            self._ROUNDNESS,
            self._ROUNDNESS
        )


#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _populateColorBundles
    def _populateColorBundles(self):
        if not self._normalBundle:
            self._normalBundle = ThemeColorBundle(
                self._colorScheme if self._colorScheme else ColorSchemes.GREY
            )

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
        self._label.setStyleSheet(self._LABEL_STYLE.replace('#C#', bundle.strong.web))

#___________________________________________________________________________________________________ _getFirstNone
    def _getFirstNone(self, *args):
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

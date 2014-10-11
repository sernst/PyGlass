# TopIconButton.py
# (C)2014
# Scott Ernst

import math
from collections import namedtuple

from PySide import QtCore
from PySide import QtGui
from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.buttons.InteractiveButtonBase import InteractiveButtonBase
from pyglass.elements.icons.IconElement import IconElement

#___________________________________________________________________________________________________ TopIconButton
from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum


class TopIconButton(InteractiveButtonBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    PAINT_PROPS = namedtuple(
        'PAINT_PROPS', ['state', 'width', 'height', 'halfWidth', 'halfHeight'])

    ICON_STYLE_SPEC     = namedtuple('ICON_STYLE_SPEC', ['color', 'alpha', 'name', 'atlas', 'scale'])
    LABEL_STYLE_SPEC    = namedtuple('LABEL_SPEC', ['color', 'fontFamily', 'size'])
    FILL_PAINT_SPEC     = namedtuple('FILL_PAINT_SPEC', ['lightColor', 'darkColor'])
    EDGE_PAINT_SPEC     = namedtuple('EDGE_DRAW_SPEC', ['color', 'lineWidth', 'higlightColor'])

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of TopIconButton."""
        super(TopIconButton, self).__init__(parent, **kwargs)
        self._roundness = 4.0

        layout  = self._getLayout(self, QtGui.QVBoxLayout)
        layout.setContentsMargins(12.0, 8.0, 12.0, 8.0)
        self.layout().setSpacing(0)
        layout.addStretch()

        iconBox, iconBoxLayout = self._createWidget(self, QtGui.QHBoxLayout, add=True)
        iconBoxLayout.setContentsMargins(0, 0, 0, 0)
        iconBoxLayout.setSpacing(0)
        iconBoxLayout.addStretch()

        label = IconElement(
            parent=iconBox,
            name=ArgsUtils.get('iconName', None, kwargs),
            atlas=ArgsUtils.get('iconAtlas', None, kwargs) )
        iconBoxLayout.addWidget(label)
        iconBoxLayout.addStretch()
        self.icon = label

        label = QtGui.QLabel()
        label.setVisible(False)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label.setParent(self)
        layout.addWidget(label)
        self.label = label

        label = QtGui.QLabel()
        label.setVisible(False)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label.setParent(self)
        layout.addWidget(label)
        self.subLabel = label

        layout.addStretch()

        self.sizePolicy().setControlType(QtGui.QSizePolicy.ToolButton)

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

#___________________________________________________________________________________________________ GS: iconAtlas
    @property
    def iconAtlas(self):
        return self.icon.atlas
    @iconAtlas.setter
    def iconAtlas(self, value):
        if self.icon.atlas == value:
            return
        self.icon.atlas = value
        self._updateIcon()

#___________________________________________________________________________________________________ GS: iconName
    @property
    def iconName(self):
        return self.icon.name
    @iconName.setter
    def iconName(self, value):
        if self.icon.name == value:
            return
        self.icon.name = value
        self._updateIcon()

#___________________________________________________________________________________________________ GS: shrink
    @property
    def shrink(self):
        return self.sizePolicy().horizontalPolicy() == QtGui.QSizePolicy.Maximum
    @shrink.setter
    def shrink(self, value):
        policy = QtGui.QSizePolicy.Maximum if value else QtGui.QSizePolicy.Preferred
        self.setSizePolicy(policy, policy)

#___________________________________________________________________________________________________ GS: text
    @property
    def text(self):
        return self.label.text()
    @text.setter
    def text(self, value):
        if self.label.text() == value:
            return

        self.label.setVisible(value and len(value) > 0)
        if value:
            self.label.setText(value)

#___________________________________________________________________________________________________ GS: subtext
    @property
    def subtext(self):
        return self.subLabel.text()
    @subtext.setter
    def subtext(self, value):
        if self.subLabel.text() == value:
            return

        self.subLabel.setVisible(value and len(value) > 0)
        if value:
            self.subLabel.setText(value)

#___________________________________________________________________________________________________ GS: roundness
    @property
    def roundness(self):
        return self._roundness
    @roundness.setter
    def roundness(self, value):
        if self._roundness == value:
            return
        self._roundness = value
        self.repaint()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initialize
    def _initialize(self):
        self._updateDisplay(InteractionStatesEnum.NORMAL_MODE)

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, *args, **kwargs):
        interactionState = self.getInteractionState()

        size  = self.size()
        w     = size.width()
        h     = size.height()
        halfW =math.ceil(float(w)/2.0)
        halfH =math.ceil(float(h)/2.0)

        props = self.PAINT_PROPS(
            state=interactionState,
            width=w,
            height=h,
            halfWidth=halfW,
            halfHeight=halfH)

        matrix = QtGui.QMatrix()
        matrix.translate(halfW, halfH)

        edge = self._getEdgePaintSpec(props)
        fill = self._getFillPaintSpec(props)
        if not edge and not fill:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        lineWide = edge.lineWidth if edge else 0.0

        #--- MAIN FILL ---#
        if fill:
            gradient = QtGui.QLinearGradient(halfW, -halfH - 1, halfW, halfH + 1)
            gradient.setColorAt(0.0, self._getAsQColor(fill.lightColor))
            gradient.setColorAt(1.0, self._getAsQColor(fill.darkColor))

            brush = QtGui.QBrush(gradient)
            brush.setMatrix(matrix)
            painter.setBrush(brush)
        else:
            painter.setBrush(QtCore.Qt.NoBrush)

        if edge and lineWide > 0.0:
            pen = QtGui.QPen()
            pen.setWidth(lineWide)
            pen.setColor(self._getAsQColor(edge.color))
            painter.setPen(pen)
        else:
            painter.setPen(QtCore.Qt.NoPen)

        painter.drawRoundedRect(
            lineWide, lineWide,
            w - 2*lineWide, h - 2*lineWide,
            self.roundness, self.roundness)

        #--- EDGE HIGHLIGHT ---#
        if lineWide <= 0.0:
            return

        pen = QtGui.QPen()
        pen.setWidth(lineWide)
        pen.setColor(self._getAsQColor(edge.higlightColor))

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(pen)
        painter.drawRoundedRect(
            lineWide + 1.0, lineWide + 1.0,
            w - 2.0*lineWide - 2.0, h - 2.0*lineWide - 2.0,
            self.roundness, self.roundness)

#___________________________________________________________________________________________________ _getIconSpec
    def _getIconSpec(self, state):
        return None

#___________________________________________________________________________________________________ _getSubLabelStyleSpec
    def _getSubLabelStyleSpec(self, state):
        return self.LABEL_STYLE_SPEC(fontFamily='Arial', color=0x999999, size=12)

#___________________________________________________________________________________________________ _getLabelStyleSpec
    def _getLabelStyleSpec(self, state):
        return self.LABEL_STYLE_SPEC(fontFamily='Arial', color=0x333333, size=16)

#___________________________________________________________________________________________________ _getFillPaintSpec
    def _getFillPaintSpec(self, paintProps):
        return self.FILL_PAINT_SPEC(lightColor=0xCCDDDDDD, darkColor=0xCCAAAAAA)

#___________________________________________________________________________________________________ _getEdgePaintSpec
    def _getEdgePaintSpec(self, paintProps):
        return self.EDGE_PAINT_SPEC(lineWidth=2.0, color=0xFF000000, higlightColor=0xFFCCCCCC)

#___________________________________________________________________________________________________ _updateDisplayImpl
    def _updateDisplay(self, mode =None):
        super(TopIconButton, self)._updateDisplay(mode=mode)

        state = self.getInteractionState()
        labelStyle = self._getLabelStyleSpec(state)

        css = 'font-size:%spx; color:#%s; font-family:%s;' % (
            labelStyle.size, hex(labelStyle.color)[2:], labelStyle.fontFamily)
        self.label.setStyleSheet(css)

        labelStyle = self._getSubLabelStyleSpec(state)
        css = 'font-size:%spx; color:#%s; font-family:%s;' % (
            labelStyle.size, hex(labelStyle.color)[2:], labelStyle.fontFamily)
        self.subLabel.setStyleSheet(css)

        self._updateIcon()

#___________________________________________________________________________________________________ _updateIcon
    def _updateIcon(self):
        state = self.getInteractionState()
        spec = self._getIconSpec(state)
        if not spec:
            return

        self.icon.atlas   = spec.atlas
        self.icon.name    = spec.name
        self.icon.opacity = spec.alpha
        self.icon.color   = spec.color
        self.icon.textureScale = spec.scale

#___________________________________________________________________________________________________ _getAsQColor
    @classmethod
    def _getAsQColor(cls, color):
        if isinstance(color, QtGui.QColor):
            return color
        return QtGui.QColor.fromRgba(color)



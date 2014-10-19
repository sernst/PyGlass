# SideBarOverlay.py
# (C)2014
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.overlay.PyGlassOverlay import PyGlassOverlay

#___________________________________________________________________________________________________ SideBarOverlay
class SideBarOverlay(PyGlassOverlay):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, name, parent =None, **kwargs):
        """Creates a new instance of SideBarOverlay."""
        self._anim = None
        self._dockOnLeft = ArgsUtils.get('dockOnLeft', True, kwargs)
        super(SideBarOverlay, self).__init__(name=name, parent=parent, **kwargs)

        self._sideWidget = self._createSideWidget()
        self._sideWidget.setVisible(False)
        self._sideWidth = None
        self._widthRatio = 0.5
        self._isOpen = False
        self._minimumSideWidth = 0

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: minimumSideWidth
    @property
    def minimumSideWidth(self):
        return self._minimumSideWidth
    @minimumSideWidth.setter
    def minimumSideWidth(self, value):
        self._minimumSideWidth = value
        self._updateSideWidgetSize()

#___________________________________________________________________________________________________ GS: widthRatio
    @property
    def widthRatio(self):
        return self._widthRatio
    @widthRatio.setter
    def widthRatio(self, value):
        if self._widthRatio == value:
            return
        self._widthRatio = value
        self._updateSideWidgetSize()

#___________________________________________________________________________________________________ GS: dockOnLeft
    @property
    def dockOnLeft(self):
        return self._dockOnLeft
    @dockOnLeft.setter
    def dockOnLeft(self, value):
        self._dockOnLeft = value

#___________________________________________________________________________________________________ GS: sideWidget
    @property
    def sideWidget(self):
        return self._sideWidget
    @sideWidget.setter
    def sideWidget(self, value):
        self._sideWidget = value

#___________________________________________________________________________________________________ GS: isOpen
    @property
    def isOpen(self):
        return self._isOpen
    @isOpen.setter
    def isOpen(self, value):
        if self._isOpen == value:
            return
        self._isOpen = value
        self._toggleSideWidget(value)

#___________________________________________________________________________________________________ GS: sideWidgetX
    @property
    def sideWidgetX(self):
        return self.sideWidget.x()
    @sideWidgetX.setter
    def sideWidgetX(self, value):
        self.sideWidget.setX(value)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _toggleSideWidget
    def _toggleSideWidget(self, open =True):
        """_openWidget doc..."""

        if self._anim:
            self._anim.stop()
            self._anim.deleteLater()
            self._anim = None

        self.sideWidget.show()
        anim = QtCore.QPropertyAnimation(self.sideWidget, "pos")
        anim.setDuration(250)

        if self.dockOnLeft:
            outValue = -self._getSideWidgetWidth()
            inValue  = 0
        else:
            w = self.size().width()
            outValue = w
            inValue  = w - self._getSideWidgetWidth()

        anim.setStartValue(QtCore.QPoint(outValue if open else inValue, 0))
        anim.setEndValue(QtCore.QPoint(inValue if open else outValue, 0))
        anim.finished.connect(self._handleAnimFinished)
        self._anim = anim
        anim.start()

#___________________________________________________________________________________________________ _resizeImpl
    def _resizeImpl(self, *args, **kwargs):
        self._updateSideWidgetSize()

#___________________________________________________________________________________________________ _createSideWidget
    def _createSideWidget(self):
        """_createSideWidget doc..."""
        return self._createWidget(self, None, True)

#___________________________________________________________________________________________________ _updateSideWidgetSize
    def _updateSideWidgetSize(self):
        """_updateSideWidgetSize doc..."""
        self._sideWidget.setFixedSize(self._getSideWidgetWidth(), self.size().height())

#___________________________________________________________________________________________________ _getSideWidgetWidth
    def _getSideWidgetWidth(self):
        """_getSideWidgetWidth doc..."""
        width = self.size().width()
        return min(width, max(
            self._minimumSideWidth,
            int(round(self._widthRatio*float(width))) ))

#___________________________________________________________________________________________________ _onAnimationComplete
    def _onAnimationComplete(self):
        """_onAnimationComplete doc..."""
        pass

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleAnimFinished
    def _handleAnimFinished(self):
        """_handleAnimFinished doc..."""
        try:
            self._anim.deleteLater()
        except Exception, err:
            pass
        self._anim = None
        self.sideWidget.setVisible(self.isOpen)
        self._onAnimationComplete()

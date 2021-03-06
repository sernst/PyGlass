# InteractiveElement.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum
from pyglass.elements.PyGlassElement import PyGlassElement

#___________________________________________________________________________________________________ InteractiveElement
class InteractiveElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    clicked  = QtCore.Signal()
    press    = QtCore.Signal()
    rollOver = QtCore.Signal()
    rollOut  = QtCore.Signal()

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, toggles =False, clickOn =False, **kwargs):
        """Creates a new instance of InteractiveElement."""
        self._clickCallback = ArgsUtils.extract('callback', None, kwargs)
        super(InteractiveElement, self).__init__(parent, **kwargs)

        self._toggles      = toggles
        self._clickOn      = clickOn
        self._checked      = False
        self._mode         = InteractionStatesEnum.NORMAL_MODE
        self._isHovering   = False
        self._mouseEnabled = True
        self._displayIsDirty = True

        c = QtGui.QCursor()
        c.setShape(QtCore.Qt.PointingHandCursor)
        self.setCursor(c)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isHovering
    @property
    def isHovering(self):
        return self.mouseEnabled and self._isHovering

#___________________________________________________________________________________________________ GS: mouseEnabled
    @property
    def mouseEnabled(self):
        return self._mouseEnabled
    @mouseEnabled.setter
    def mouseEnabled(self, value):
        wasEnabled         = self._mouseEnabled
        self._mouseEnabled = value
        if wasEnabled != value:
            self._exitInteractivityStates()
            if wasEnabled:
                self.unsetCursor()
            else:
                c = QtGui.QCursor()
                c.setShape(QtCore.Qt.PointingHandCursor)
                self.setCursor(c)

#___________________________________________________________________________________________________ GS: isChecked
    @property
    def isChecked(self):
        return self.checked
    @isChecked.setter
    def isChecked(self, value):
        self.checked = value

#___________________________________________________________________________________________________ GS: checked
    @property
    def checked(self):
        return self._toggles and self._checked
    @checked.setter
    def checked(self, value):
        if not self._toggles or self._checked == value:
            return

        wasChecked = self._checked
        self._checked = value
        if wasChecked and not value:
            self._updateDisplay(InteractionStatesEnum.NORMAL_MODE)
        elif not wasChecked and value:
            self._updateDisplay(InteractionStatesEnum.SELECTED_MODE)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getInteractionState
    def getInteractionState(self):
        if not self.isEnabled():
            return InteractionStatesEnum.DISABLED_MODE
        elif self.checked:
            return InteractionStatesEnum.SELECTED_MODE
        return self._mode

#___________________________________________________________________________________________________ setEnabled
    def setEnabled(self, *args, **kwargs):
        super(InteractiveElement, self).setEnabled(*args, **kwargs)
        self._updateDisplay()

#___________________________________________________________________________________________________ mousePressEvent
    def mousePressEvent(self, mouseEvent):
        """Doc..."""
        if not self.mouseEnabled:
            return

        if self._toggles and self._clickOn and self._checked:
            return

        self._updateDisplay(InteractionStatesEnum.PRESS_MODE)
        self.press.emit()

#___________________________________________________________________________________________________ mouseReleaseEvent
    def mouseReleaseEvent(self, mouseEvent):
        if not self.mouseEnabled:
            return

        self._isHovering = False

        ISE  = InteractionStatesEnum
        pos  = mouseEvent.pos()
        size = self.size()
        if 0 <= pos.x() <= size.width() and 0 <= pos.y() <= size.height():
            if self._toggles:
                self.checked = True if self._clickOn else not self._checked
            else:
                self._updateDisplay(ISE.OVER_MODE)
            self.onClickEvent(mouseEvent)
        else:
            self._updateDisplay(ISE.SELECTED_MODE if self.checked else ISE.NORMAL_MODE)

#___________________________________________________________________________________________________ enterEvent
    def enterEvent(self, *args, **kwargs):
        if not self.mouseEnabled:
            return

        self._isHovering = True

        if self._toggles and self._clickOn and self._checked:
            return

        self._updateDisplay(InteractionStatesEnum.OVER_MODE)

        self.rollOver.emit()

#___________________________________________________________________________________________________ leaveEvent
    def leaveEvent(self, *args, **kwargs):
        self._isHovering = False

        if not self.mouseEnabled:
            return

        self._exitInteractivityStates()
        self.rollOut.emit()

#___________________________________________________________________________________________________ onClickEvent
    def onClickEvent(self, event):
        self._onClickEventImpl(event)
        self.clicked.emit()
        if self._clickCallback is not None:
            self._clickCallback(self)

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, event):
        if self._displayIsDirty:
            self._displayIsDirty = False
            self._updateDisplayImpl()
        super(InteractiveElement, self).paintEvent(event)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initialize
    def _initialize(self):
        super(InteractiveElement, self)._initialize()
        self._updateDisplay(self._mode)

#___________________________________________________________________________________________________ _onClickEventImpl
    def _onClickEventImpl(self, event):
        pass

#___________________________________________________________________________________________________ _exitInteractivityStates
    def _exitInteractivityStates(self):
        if self.checked:
            self._updateDisplay(InteractionStatesEnum.SELECTED_MODE)
        else:
            self._updateDisplay(InteractionStatesEnum.NORMAL_MODE)

#___________________________________________________________________________________________________ _updateDisplay
    def _updateDisplay(self, mode =None):
        """Doc..."""
        if mode:
            self._mode = mode
        elif self.isChecked:
            self._mode = InteractionStatesEnum.SELECTED_MODE
        else:
            self._mode = InteractionStatesEnum.NORMAL_MODE
        self._displayIsDirty = True
        self.update()

#___________________________________________________________________________________________________ _updateDisplayImpl
    def _updateDisplayImpl(self):
        pass

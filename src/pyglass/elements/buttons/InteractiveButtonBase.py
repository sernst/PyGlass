# InteractiveButtonBase.py
# (C)2013
# Scott Ernst

from PySide import QtCore

from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.PyGlassElement import PyGlassElement

#___________________________________________________________________________________________________ InteractiveButtonBase
class InteractiveButtonBase(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    NORMAL_MODE   = 'normal'
    OVER_MODE     = 'over'
    PRESS_MODE    = 'press'
    SELECTED_MODE = 'selected'
    DISABLED_MODE = 'disabled'
    MODES    = ['normal', 'over', 'press', 'selected', 'disabled']

    clicked = QtCore.Signal()

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, toggles =False, clickOn =False, **kwargs):
        """Creates a new instance of InteractiveButtonBase."""
        PyGlassElement.__init__(self, parent, **kwargs)
        self._toggles      = toggles
        self._clickOn      = clickOn
        self._userData     = ArgsUtils.get('userData', None, kwargs)
        self._checked      = False
        self._mode         = InteractiveButtonBase.NORMAL_MODE
        self._mouseEnabled = True

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: userData
    @property
    def userData(self):
        return self._userData
    @userData.setter
    def userData(self, value):
        self._userData = value

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

#___________________________________________________________________________________________________ GS: checked
    @property
    def checked(self):
        return self._toggles and self._checked
    @checked.setter
    def checked(self, value):
        if not self._toggles:
            return

        wasChecked    = self._checked
        self._checked = value
        if wasChecked and not value:
            self._updateDisplay(InteractiveButtonBase.NORMAL_MODE)
        elif not wasChecked and value:
            self._updateDisplay(InteractiveButtonBase.SELECTED_MODE)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ mousePressEvent
    def mousePressEvent(self, mouseEvent):
        """Doc..."""
        if not self.mouseEnabled:
            return

        if self._toggles and self._clickOn and self._checked:
            return

        self._updateDisplay(InteractiveButtonBase.PRESS_MODE)

#___________________________________________________________________________________________________ mouseReleaseEvent
    def mouseReleaseEvent(self, mouseEvent):
        if not self.mouseEnabled:
            return

        pos  = mouseEvent.pos()
        size = self.size()
        if 0 <= pos.x() <= size.width() and 0 <= pos.y() <= size.height():
            if self._toggles:
                self.checked = True if self._clickOn else not self._checked
            else:
                self._updateDisplay(InteractiveButtonBase.OVER_MODE)
            self.clicked.emit()
        else:
            self._updateDisplay(InteractiveButtonBase.NORMAL_MODE)

#___________________________________________________________________________________________________ enterEvent
    def enterEvent(self, *args, **kwargs):
        if not self.mouseEnabled:
            return

        if self._toggles and self._clickOn and self._checked:
            return

        self._updateDisplay(InteractiveButtonBase.OVER_MODE)

#___________________________________________________________________________________________________ leaveEvent
    def leaveEvent(self, *args, **kwargs):
        if not self.mouseEnabled:
            return
        self._exitInteractivityStates()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _exitInteractivityStates
    def _exitInteractivityStates(self):
        if self.checked:
            self._updateDisplay(InteractiveButtonBase.SELECTED_MODE)
        else:
            self._updateDisplay(InteractiveButtonBase.NORMAL_MODE)

#___________________________________________________________________________________________________ _updateDisplay
    def _updateDisplay(self, mode =None):
        """Doc..."""
        self._mode = mode if mode else InteractiveButtonBase.NORMAL_MODE

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__



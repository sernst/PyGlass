# InteractiveLineEdit.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtCore
from PySide import QtGui


from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ InteractiveLineEdit
class InteractiveLineEdit(QtGui.QLineEdit):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    FOCUS_IN_EVENT  = 'focus_in_event'
    FOCUS_OUT_EVENT = 'focus_out_event'
    TEXT_CHANGED    = 'text_changed'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of InteractiveLineEdit."""
        QtGui.QLineEdit.__init__(self, parent, **kwargs)

        class ILEEventSignal(QtCore.QObject):
            signal = QtCore.Signal(dict)
        self._eventSignal = ILEEventSignal()

        self._eventCallbacks = []
        self.textChanged.connect(self._handleTextChanged)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: eventSignal
    @property
    def eventSignal(self):
        return self._eventSignal.signal

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ focusOutEvent
    def focusOutEvent(self, event):
        """Doc..."""
        QtGui.QLineEdit.focusOutEvent(self, event)
        self._triggerEvent(self.FOCUS_OUT_EVENT, None)

#___________________________________________________________________________________________________ focusInEvent
    def focusInEvent(self, event):
        QtGui.QLineEdit.focusInEvent(self, event)
        self._triggerEvent(self.FOCUS_IN_EVENT, None)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _triggerEvent
    def _triggerEvent(self, eventEnum, data):
        """Doc..."""

        skipTrigger = self._triggerEventImpl(eventEnum, data)
        if skipTrigger:
            return

        self.eventSignal.emit({
            'type':eventEnum,
            'target':self,
            'data':data })

#___________________________________________________________________________________________________ _triggerEventImpl
    def _triggerEventImpl(self, eventEnum, data):
        return None

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleTextChanged
    def _handleTextChanged(self):
        self._triggerEvent(self.TEXT_CHANGED, self.text())

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

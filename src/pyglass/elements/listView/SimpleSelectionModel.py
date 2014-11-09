# SimpleSelectionModel.py
# (C)2012
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtCore
from PySide import QtGui

#___________________________________________________________________________________________________ SimpleSelectionModel
from pyaid.string.StringUtils import StringUtils


class SimpleSelectionModel(QtGui.QItemSelectionModel):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, model, parent =None):
        """Creates a new instance of SimpleSelectionModel."""

        class SELECTION_CHANGED_SIGNAL(QtCore.QObject):
            signal = QtCore.Signal(QtGui.QItemSelection, QtGui.QItemSelection)
        self._onSelectionChanged = SELECTION_CHANGED_SIGNAL()

        QtGui.QItemSelectionModel.__init__(self, model, parent)
        self.selectionChanged.connect(self._handleSelectionChanged)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: onSelectionChanged
    @property
    def onSelectionChanged(self):
        return self._onSelectionChanged.signal

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleSelectionChanged
    @QtCore.Slot(QtGui.QItemSelection, QtGui.QItemSelection)
    def _handleSelectionChanged(self, current, previous):
        self.onSelectionChanged.emit(current, previous)

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

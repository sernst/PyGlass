# PaintableWidget.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui

#___________________________________________________________________________________________________ PaintableWidget
from pyaid.string.StringUtils import StringUtils


class PaintableWidget(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, paintCallback =None, **kwargs):
        """Creates a new instance of PaintableWidget."""
        super(PaintableWidget, self).__init__(parent, **kwargs)
        self._paintCallback = paintCallback

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: paintCallback
    @property
    def paintCallback(self):
        return self._paintCallback
    @paintCallback.setter
    def paintCallback(self, value):
        if self._paintCallback == value:
            return
        self._paintCallback = value
        self.updateGeometry()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ publicMethod
    def paintEvent(self, event):
        """Doc..."""
        super(PaintableWidget, self).paintEvent(event)
        if self._paintCallback is None:
            return
        self._paintCallback(self, event)

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


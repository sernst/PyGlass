# PyGlassBackgroundParent.py
# (C)2012-2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui

from pyaid.debug.Logger import Logger
from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ PyGlassBackgroundParent
class PyGlassBackgroundParent(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, proxy =None):
        """Creates a new instance of PyGlassBackgroundParent."""
        super(PyGlassBackgroundParent, self).__init__(parent)
        self._gui        = proxy if proxy else parent
        self._log        = parent.log if parent and hasattr(parent, 'log') else None
        if not self._log:
            self._log = Logger(self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isOnDisplay
    @property
    def isOnDisplay(self):
        return False

#___________________________________________________________________________________________________ GS: isBackgroundParent
    @property
    def isBackgroundParent(self):
        return True

#___________________________________________________________________________________________________ GS: backgroundTarget
    @property
    def backgroundTarget(self):
        return self._gui

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __getattr__
    def __getattr__(self, item):
        """Doc..."""
        return getattr(self._gui, item)

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


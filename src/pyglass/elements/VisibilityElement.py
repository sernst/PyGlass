# VisibilityElement.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui

from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils
from pyglass.elements.VisibilityManager import VisibilityManager

#___________________________________________________________________________________________________ VisibilityElement
class VisibilityElement(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of VisibilityElement."""
        super(VisibilityElement, self).__init__(parent=parent)
        self._instanceUid = TimeUtils.getUidTimecode(
            prefix=self.__class__.__name__,
            suffix=StringUtils.getRandomString(8))
        self._visibility = VisibilityManager(target=self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: instanceUid
    @property
    def instanceUid(self):
        return self._instanceUid

#___________________________________________________________________________________________________ GS: propertyName
    @property
    def visibility(self):
        return self._visibility

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setVisible
    def setVisible(self, *args, **kwargs):
        """Doc..."""
        super(VisibilityElement, self).setVisible(*args, **kwargs)
        self._visibility.rawState = bool(args[0])

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


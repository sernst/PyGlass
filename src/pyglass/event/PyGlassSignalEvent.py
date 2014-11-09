# PyGlassSignalEvent.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ PyGlassSignalEvent
class PyGlassSignalEvent(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, target, data):
        """Creates a new instance of PyGlassSignalEvent."""
        super(PyGlassSignalEvent, self).__init__()
        self._target = target
        self._data = data

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: target
    @property
    def target(self):
        return self._target

#___________________________________________________________________________________________________ GS: data
    @property
    def data(self):
        return self._data

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None):
        try:
            return self._data[key]
        except Exception as err:
            return defaultValue

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



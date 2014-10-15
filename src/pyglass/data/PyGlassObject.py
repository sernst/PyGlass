# PyGlassObject.py
# (C)2014
# Scott Ernst

from pyaid.string.StringUtils import StringUtils
from pyaid.time.TimeUtils import TimeUtils

#___________________________________________________________________________________________________ PyGlassObject
class PyGlassObject(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _INSTANCE_INDEX = 0

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of PyGlassObject."""
        self._INSTANCE_INDEX += 1
        self._instanceUid = TimeUtils.getUidTimecode(
            prefix=self.__class__.__name__,
            suffix=unicode(self._INSTANCE_INDEX) + '-' + StringUtils.getRandomString(8) )

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: instanceUid
    @property
    def instanceUid(self):
        return self._instanceUid

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


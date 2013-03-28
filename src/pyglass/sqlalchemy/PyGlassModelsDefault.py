# PyGlassModelsDefault.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import orm
from sqlalchemy import UnicodeText
from sqlalchemy.ext.hybrid import hybrid_property

from pyaid.json.JSON import JSON
from pyaid.radix.Base64 import Base64
from pyaid.time.TimeUtils import TimeUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.sqlalchemy.AbstractPyGlassModelsMeta import AbstractPyGlassModelsMeta
from pyglass.sqlalchemy.PyGlassModelUtils import PyGlassModelUtils

#___________________________________________________________________________________________________ PyGlassModelsDefault
class PyGlassModelsDefault(object):

#===================================================================================================
#                                                                                       C L A S S

    __metaclass__  = AbstractPyGlassModelsMeta
    __abstract__   = True
    __table_args__ = {'sqlite_autoincrement': True}

    _i         = Column(Integer, primary_key=True)
    _upts      = Column(DateTime, default=datetime.datetime.utcnow())
    _cts       = Column(DateTime, default=datetime.datetime.utcnow())
    _json_data = Column(UnicodeText, default=u'')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        super(PyGlassModelsDefault, self).__init__(**kwargs)
        self.ormInit()

#___________________________________________________________________________________________________ ormInit
    @orm.reconstructor
    def ormInit(self):
        pass

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: data
    @hybrid_property
    def json_data(self):
        return JSON.fromString(self._json_data) if self._json_data else None
    @json_data.setter
    def json_data(self, value):
        if value is None:
            self.json_data = u''
            return

        self.json_data = JSON.asString(value)

#___________________________________________________________________________________________________ GS: upts
    @hybrid_property
    def upts(self):
        return self._upts
    @upts.setter
    def upts(self, value):
        self._upts = self.__class__._parseTimestamp(value)

#___________________________________________________________________________________________________ GS: cts
    @hybrid_property
    def cts(self):
        return self._cts
    @cts.setter
    def cts(self, value):
        self._cts = self.__class__._parseTimestamp(value)

#___________________________________________________________________________________________________ GS: _log
    @property
    def _log(self):
        return PyGlassModelUtils.logger

#___________________________________________________________________________________________________ _getPrintAttrs
    def _getPrintAttrs(self):
        return None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getValue
    def getValue(self, name):
        """Returns the value of the specified property, or None if the property is not specified.

        @@@param name:string
            The name of the property to retrieve.
        """

        return getattr(self, name)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _parseTimestamp
    @classmethod
    def _parseTimestamp(cls, value):
        if value is None:
            return datetime.datetime.utcnow()
        elif isinstance(value, basestring):
            return TimeUtils.secondsToDatetime(
                Base64.from64(value) + PyGlassEnvironment.BASE_UNIX_TIME
            )
        return value

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        modelInfo = self._getPrintAttrs()
        if isinstance(modelInfo, dict):
            out = u''
            for n,v in modelInfo.iteritems():
                out += u' ' + unicode(n) + u'[' + unicode(v) + u']'
            modelInfo = out
        elif modelInfo:
            modelInfo = u' ' + unicode(modelInfo)
        else:
            modelInfo = u''

        return u'<%s[%s] cts[%s] upts[%s]%s>' % (
            self.__class__.__name__,
            unicode(self.i),
            unicode(self.cts.strftime('%m-%d-%y %H:%M:%S') if self.cts else u'None'),
            unicode(self.upts.strftime('%m-%d-%y %H:%M:%S') if self.upts  else u'None'),
            modelInfo
        )

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

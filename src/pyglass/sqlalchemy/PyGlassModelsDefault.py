# PyGlassModelsDefault.py
# (C)2012-2013
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import datetime
from pyaid.dict.DictUtils import DictUtils
from pyaid.string.StringUtils import StringUtils

import sqlalchemy as sqla
from sqlalchemy.ext.hybrid import hybrid_property

from pyaid.json.JSON import JSON
from pyaid.radix.Base64 import Base64
from pyaid.time.TimeUtils import TimeUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.sqlalchemy.AbstractPyGlassModelsMeta import AbstractPyGlassModelsMeta
from pyglass.sqlalchemy.PyGlassModelUtils import PyGlassModelUtils

import six

#___________________________________________________________________________________________________ PyGlassModelsDefault
@six.add_metaclass(AbstractPyGlassModelsMeta)
class PyGlassModelsDefault(object):

#===================================================================================================
#                                                                                       C L A S S

    __abstract__   = True
    __table_args__ = {'sqlite_autoincrement': True}

    _i         = sqla.Column(sqla.Integer, primary_key=True)
    _upts      = sqla.Column(sqla.DateTime, default=datetime.datetime.utcnow())
    _cts       = sqla.Column(sqla.DateTime, default=datetime.datetime.utcnow())
    _json_data = sqla.Column(sqla.UnicodeText, default='')

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        super(PyGlassModelsDefault, self).__init__()
        self.ormInit()

#___________________________________________________________________________________________________ ormInit
    def ormInit(self):
        self.transientData = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: data
    @hybrid_property
    def json_data(self):
        return JSON.fromString(self._json_data) if self._json_data else None
    @json_data.setter
    def json_data(self, value):
        if value is None:
            self.json_data = ''
            return

        self.json_data = JSON.asString(value)

#___________________________________________________________________________________________________ GS: upts
    @hybrid_property
    def upts(self):
        return self._upts
    @upts.setter
    def upts(self, value):
        self._upts = self._parseTimestamp(value)

#___________________________________________________________________________________________________ GS: cts
    @hybrid_property
    def cts(self):
        return self._cts
    @cts.setter
    def cts(self, value):
        self._cts = self._parseTimestamp(value)

#___________________________________________________________________________________________________ GS: mySession
    @property
    def mySession(self):
        try:
            return sqla.inspect(self).session
        except Exception:
            return None

#___________________________________________________________________________________________________ GS: _log
    @property
    def _log(self):
        return PyGlassModelUtils.logger

#___________________________________________________________________________________________________ _getPrintAttrs
    def _getPrintAttrs(self):
        return None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ fetchTransient
    def fetchTransient(self, key, defaultValue =None):
        return self.transientData.get(key, defaultValue) if self.transientData else defaultValue

#___________________________________________________________________________________________________ putTransient
    def putTransient(self, key, value):
        if self.transientData is None:
            self.transientData = dict()
        self.transientData[key] = value

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
        elif StringUtils.isStringType(value):
            return TimeUtils.secondsToDatetime(
                Base64.from64(value) + PyGlassEnvironment.BASE_UNIX_TIME)
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
            out = ''
            for n,v in DictUtils.iter(modelInfo):
                out += ' ' + StringUtils.toUnicode(n) + '[' + StringUtils.toUnicode(v) + ']'
            modelInfo = out
        elif modelInfo:
            modelInfo = ' ' + StringUtils.toUnicode(modelInfo)
        else:
            modelInfo = ''

        return '<%s[%s] cts[%s] upts[%s]%s>' % (
            self.__class__.__name__,
            StringUtils.toUnicode(self.i),
            StringUtils.toUnicode(self.cts.strftime('%m-%d-%y %H:%M:%S') if self.cts else 'None'),
            StringUtils.toUnicode(self.upts.strftime('%m-%d-%y %H:%M:%S') if self.upts  else 'None'),
            modelInfo
        )

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

# SQLAlchemyResult.py
# (C) 2012
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import time

from sqlalchemy import exc

from pyaid.debug.Logger import Logger

#___________________________________________________________________________________________________ SQLAlchemyResult
class SQLAlchemyResult(object):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, modelClass, query, lock =False):
        self._modelClass = modelClass
        self._query      = query
        self._lock       = lock

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ count
    def count(self):
        return self._getResult(self._query.count)

#___________________________________________________________________________________________________ scalar
    def scalar(self):
        try:
            return self._getResult(self._query.scalar, exc.MultipleResultsFound)
        except Exception as err:
            return None

#___________________________________________________________________________________________________ one
    def one(self):
        try:
            return self._getResult(self._query.one, (exc.NoResultFound, exc.MultipleResultsFound))
        except Exception as err:
            return None

#___________________________________________________________________________________________________ first
    def first(self):
        return self._getResult(self._query.first)

#___________________________________________________________________________________________________ all
    def all(self):
        return self._getResult(self._query.all)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getResult
    def _getResult(self, function, passErrors =None):
        # SLAVE models are read-only, so make sure to lock the table in read mode only to prevent
        # lock collisions. MASTER models query for updates, so use the stronger update lockmode
        # to prevent read collisions.

        # 3 iterations is significant to SQLAlchemy.
        for i in range(3):
            try:
                result = function()
                if self._lock:
                    if self._modelClass.IS_MASTER:
                        result = result.with_lockmode("update")
                    else:
                        result = result.with_lockmode("read")
                return result
            except passErrors as err:
                raise err
            except Exception as err:
                stackData = Logger.getStackData()
                self._modelClass._log.writeError('[%s] BAD CURSOR ACTION: %s'
                                                 % (str(i), str(function)), err)
                pass

        # Sleeps away collisions.
        time.sleep(1)

        try:
            result = function()
            if self._lock:
                if self._modelClass.IS_MASTER:
                    result = result.with_lockmode("update")
                else:
                    result = result.with_lockmode("read")
            return result
        except passErrors as err:
            raise err
        except Exception as err:
            stackData = Logger.getStackData()
            # noinspection PyProtectedMember
            self._modelClass._log.writeError('FAILED CURSOR ACTION: %s'% str(function), err)

        return None

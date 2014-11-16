# PyGlassModelUtils.py
# (C)2012-2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os
import re
import zipfile

from pyaid.OsUtils import OsUtils
from pyaid.debug.Logger import Logger
from pyaid.decorators.ClassGetter import ClassGetter

#AS NEEDED: pyglass.alembic.AlembicUtils import AlembicUtils
from pyaid.string.StringUtils import StringUtils
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ ModelUtils
class PyGlassModelUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ZIP_FIND = os.sep + OsUtils.getPerOsValue('library', 'site-packages', 'fictional') + '.zip' + os.sep

    _logger = Logger('SQLAlchemyModels', printOut=True)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ logger
    # noinspection PyMethodParameters
    @ClassGetter
    def logger(cls):
        return cls._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ modelsInit
    @classmethod
    def modelsInit(cls, initPath, initName):
        out = dict()
        zipIndex = initPath[0].find(PyGlassModelUtils._ZIP_FIND)
        if  zipIndex == -1:
            moduleList = os.listdir(initPath[0])
        else:
            splitIndex = zipIndex+len(PyGlassModelUtils._ZIP_FIND)
            zipPath    = initPath[0][:splitIndex-1]
            modulePath = initPath[0][splitIndex:]
            z          = zipfile.ZipFile(zipPath)
            moduleList = []
            for item in z.namelist():
                item = os.sep.join(item.split('/'))
                if item.startswith(modulePath):
                    moduleList.append(item.rsplit(os.sep, 1)[-1])

        items = []
        for module in moduleList:
            if module.startswith('__init__.py') or module.find('_') == -1:
                continue

            parts    = module.rsplit('.', 1)
            parts[0] = parts[0].rsplit(os.sep, 1)[-1]
            if not parts[-1].startswith(StringUtils.toStr2('py')) or parts[0] in items:
                continue
            items.append(parts[0])

            m = None
            n = None
            r = None
            c = None
            try:
                n = module.rsplit('.', 1)[0]
                m = initName + '.' + n
                r = __import__(m, locals(), globals(), [n])
                c = getattr(r, StringUtils.toText(n))
                out[n] = c
                if not c.__table__.exists(c.ENGINE):
                    c.__table__.create(c.ENGINE, True)

                    from pyglass.alembic.AlembicUtils import AlembicUtils
                    if AlembicUtils.hasAlembic:
                        AlembicUtils.stampDatabase(c.DATABASE_URL)
                        cls._logger.write('CREATED: %s %s [STAMPED head]' % (c, c.__table__))
            except Exception as err:
                cls._logger.writeError([
                    'MODEL INITIALIZATION FAILURE:',
                    'INIT PATH: %s' % initPath,
                    'INIT NAME: %s' % initName,
                    'MODULE IMPORT: %s' % m,
                    'IMPORT CLASS: %s' % n,
                    'IMPORT RESULT: %s' % r,
                    'CLASS RESULT: %s' % c ], err)

        return out

#___________________________________________________________________________________________________ getMigrationPathFromDatabaseUrl
    @classmethod
    def getMigrationPathFromDatabaseUrl(cls, databaseUrl, root =False):
        urlParts = databaseUrl.split('://')
        if urlParts[0].lower() == 'shared':
            path = ['shared', 'migration']
        else:
            path = ['apps', urlParts[0], 'migration']

        if not root:
            path += urlParts[-1].split('/')

            # Remove the extension
            if path[-1].endswith('.vdb'):
                path[-1] = path[-1][:-4]

        return PyGlassEnvironment.getRootResourcePath(*path)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromDatabaseUrl(cls, databaseUrl):
        urlParts = databaseUrl.split('://')

        # Determine the sqlite database path
        if urlParts[0].lower() == 'shared':
            path = ['shared', 'data']
        else:
            path = ['apps', urlParts[0], 'data']

        path += urlParts[1].strip('/').split('/')
        if not path[-1].endswith('.vdb'):
            path[-1] += '.vdb'

        return PyGlassEnvironment.getRootLocalResourcePath(*path)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromEngineUrl(cls, engineUrl):
        out = cls._getEngineUrlPath(engineUrl)

        # On Windows the extra slash added to the beginning of the path must be removed
        if PyGlassEnvironment.isWindows and re.compile('^/.{1}:').match(out):
            return out[1:]

        return out

#___________________________________________________________________________________________________ getEngineUrl
    @classmethod
    def getEngineUrl(cls, databaseUrl):
        databasePath = cls.getPathFromDatabaseUrl(databaseUrl)

        d = os.path.dirname(databasePath)
        if not os.path.exists(d):
            os.makedirs(d)

        # Windows compatibility requires an additional slash before the drive letter to conform
        # to a unix type root path.
        if PyGlassEnvironment.isWindows:
            if not databasePath.startswith('/'):
                databasePath = '/' + databasePath
            return 'sqlite://' + databasePath

        # On unix file systems an additional slash is required before specifying the path element
        return 'sqlite:///' + databasePath

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getEngineUrlPath
    @classmethod
    def _getEngineUrlPath(cls, engineUrl):
        if PyGlassEnvironment.isWindows:
            return engineUrl.split('://')[-1]
        return engineUrl.split(':///')[-1]

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
from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#AS NEEDED: pyglass.alembic.AlembicUtils import AlembicUtils

#___________________________________________________________________________________________________ ModelUtils
class PyGlassModelUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ZIP_FIND = '%s%s.zip%s' % (
        os.sep, OsUtils.getPerOsValue('library', 'site-packages', 'fictional'), os.sep)

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

#___________________________________________________________________________________________________ upgradeDatabase
    @classmethod
    def upgradeDatabase(cls, databaseUrl):
        """upgradeDatabase doc..."""
        from pyglass.alembic.AlembicUtils import AlembicUtils
        if not AlembicUtils.hasAlembic:
            return False

        AlembicUtils.upgradeDatabase(
            databaseUrl=databaseUrl,
            resourcesPath=PyGlassEnvironment.getRootResourcePath(isDir=True),
            localResourcesPath=PyGlassEnvironment.getRootLocalResourcePath(isDir=True))
        return True

#___________________________________________________________________________________________________ modelsInit
    @classmethod
    def modelsInit(cls, databaseUrl, initPath, initName):
        out = dict()
        zipIndex = initPath[0].find(cls._ZIP_FIND)
        if  zipIndex == -1:
            moduleList = os.listdir(initPath[0])
        else:
            splitIndex = zipIndex+len(cls._ZIP_FIND)
            zipPath    = initPath[0][:splitIndex-1]
            modulePath = initPath[0][splitIndex:]
            z          = zipfile.ZipFile(zipPath)
            moduleList = []
            for item in z.namelist():
                item = os.sep.join(item.split('/'))
                if item.startswith(modulePath):
                    moduleList.append(item.rsplit(os.sep, 1)[-1])

        # Warn if module initialization occurs before pyglass environment initialization and
        # then attempt to initialize the environment automatically to prevent errors
        if not PyGlassEnvironment.isInitialized:
            cls.logger.write(StringUtils.dedent("""
                [WARNING]: Database initialization called before PyGlassEnvironment initialization.
                Attempting automatic initialization to prevent errors."""))
            PyGlassEnvironment.initializeFromInternalPath(initPath)

        if not cls.upgradeDatabase(databaseUrl):
            cls.logger.write(StringUtils.dedent("""
                [WARNING]: No alembic support detected. Migration support disabled."""))

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
    def getMigrationPathFromDatabaseUrl(cls, databaseUrl, root =False, resourcesPath =None):
        urlParts = databaseUrl.split('://')
        if urlParts[0].lower() == 'shared':
            path = ['shared', 'alembic']
        else:
            path = ['apps', urlParts[0], 'alembic']

        if not root:
            path += urlParts[-1].split('/')

            # Remove the extension
            if path[-1].endswith('.vdb'):
                path[-1] = path[-1][:-4]

        if resourcesPath:
            return FileUtils.makeFolderPath(resourcesPath, *path, isDir=True)

        return PyGlassEnvironment.getRootResourcePath(*path, isDir=True)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromDatabaseUrl(cls, databaseUrl, localResourcesPath =None):
        urlParts = databaseUrl.split('://')

        # Determine the sqlite database path
        if urlParts[0].lower() == 'shared':
            path = ['shared', 'data']
        else:
            path = ['apps', urlParts[0], 'data']

        path += urlParts[1].strip('/').split('/')
        if not path[-1].endswith('.vdb'):
            path[-1] += '.vdb'

        if localResourcesPath:
            return FileUtils.makeFilePath(localResourcesPath, *path)

        return PyGlassEnvironment.getRootLocalResourcePath(*path, isFile=True)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromEngineUrl(cls, engineUrl):
        out = cls._getEngineUrlPath(engineUrl)

        # On Windows the extra slash added to the beginning of the path must be removed
        if PyGlassEnvironment.isWindows and re.compile('^/.:').match(out):
            return out[1:]

        return out

#___________________________________________________________________________________________________ getRelativeEngineUrl
    @classmethod
    def getRelativeEngineUrl(cls, databaseUrl, localResourcesPath =None):
        """getRelativeEngineUrl doc..."""
        if not localResourcesPath:
            localResourcesPath = PyGlassEnvironment.getRootLocalResourcePath(isDir=True)
        url = cls.getEngineUrl(databaseUrl=databaseUrl, localResourcesPath=localResourcesPath)
        return url.replace(localResourcesPath, '')

#___________________________________________________________________________________________________ getEngineUrl
    @classmethod
    def getEngineUrl(cls, databaseUrl, localResourcesPath =None):
        databasePath = cls.getPathFromDatabaseUrl(
            databaseUrl=databaseUrl,
            localResourcesPath=localResourcesPath)

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

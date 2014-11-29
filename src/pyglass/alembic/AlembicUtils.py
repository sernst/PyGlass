# AlembicUtils.py
# (C)2012
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os
import sys
from collections import namedtuple

from pyaid.string.StringUtils import StringUtils
from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.sqlalchemy.PyGlassModelUtils import PyGlassModelUtils
import sqlalchemy as sqla

if sys.version > '3':
    import configparser
else:
    # noinspection PyUnresolvedReferences
    import ConfigParser as configparser

try:
    # Alembic functionality is optional. Availability is determined during module imports.
    from alembic import config as alembicConfig
    from alembic import command as alembicCmd
    from alembic import script as alembicScript
    from alembic import environment as alembicEnv
    from alembic.migration import MigrationContext
    ALEMBIC_SUPPORTED = True
except Exception:
    ALEMBIC_SUPPORTED = False

#___________________________________________________________________________________________________ AlembicUtils
class AlembicUtils(object):
    """ A utility class for Alembic migration management within PyGlass applications """

#===================================================================================================
#                                                                                       C L A S S

    DATABASE_ITEM_NT = namedtuple('DATABASE_ITEM_NT', ['databaseUrl', 'name', 'path'])

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: hasAlembic
    # noinspection PyMethodParameters
    @ClassGetter
    def hasAlembic(cls):
        """Specifies whether or not the Alembic package is available for use."""
        global ALEMBIC_SUPPORTED
        return ALEMBIC_SUPPORTED

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ hasMigrationEnvironment
    @classmethod
    def hasMigrationEnvironment(cls, databaseUrl, resourcesPath =None):
        """ Determines whether or not the specified application database currently has a migration
            environment setup
            :param databaseUrl:
            :param resourcesPath:
            :return: True or false depending on the presence of a migration environment """

        if not resourcesPath:
            resourcesPath = PyGlassEnvironment.getRootResourcePath(isDir=True)

        migrationPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(
            databaseUrl=databaseUrl, resourcesPath=resourcesPath)

        if not os.path.exists(migrationPath):
            return False
        if not os.path.exists(FileUtils.makeFilePath(migrationPath, 'alembic.ini')):
            return False
        if not os.path.exists(FileUtils.makeFolderPath(migrationPath, 'versions')):
            return False
        return True

#___________________________________________________________________________________________________ getConfig
    @classmethod
    def getConfig(cls, databaseUrl, resourcesPath, localResourcesPath, writeCallback =None):
        """ Retrieves the Alembic configuration for the specified database URL stored within the
            resources and local resources path for the target application """

        logger = Logger(
            databaseUrl.replace('://', '~').replace('/', '--').replace('.vdb', ''),
            useStorageBuffer=True)

        if writeCallback is not None:
            logger.addWriteCallback(writeCallback)

        migrationPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(
            databaseUrl, resourcesPath=resourcesPath)

        config = alembicConfig.Config(os.path.join(migrationPath, 'alembic.ini'), stdout=logger)

        engineUrl = PyGlassModelUtils.getEngineUrl(
            databaseUrl=databaseUrl, localResourcesPath=localResourcesPath)

        # These options are overridden during loading to prevent issues of absolute path corruption
        # when running in different deployment modes and when installed on different computers
        config.set_main_option('url', engineUrl)
        section = config.get_section('alembic')
        section['script_location'] = migrationPath
        section['sqlalchemy.url'] = engineUrl
        section['url'] = engineUrl

        return config

#___________________________________________________________________________________________________ getScriptsData
    @classmethod
    def getScriptsData(
            cls, databaseUrl, resourcesPath =None, localResourcesPath =None, config =None
    ):
        """ Returns the scripts data for the specified database and the resources path """
        if not config:
            config = cls.getConfig(
                databaseUrl=databaseUrl,
                resourcesPath=resourcesPath,
                localResourcesPath=localResourcesPath)
        result = alembicScript.ScriptDirectory.from_config(config)
        return result

#___________________________________________________________________________________________________ getCurrentDatabaseRevision
    @classmethod
    def getCurrentDatabaseRevision(
            cls, databaseUrl, resourcesPath =None, localResourcesPath =None, config =None
    ):
        url = PyGlassModelUtils.getEngineUrl(
            databaseUrl=databaseUrl,
            localResourcesPath=localResourcesPath)
        engine = sqla.create_engine(url)
        conn = engine.connect()

        context = MigrationContext.configure(conn)
        result = context.get_current_revision()
        conn.close()
        return result

#___________________________________________________________________________________________________ getCurrentDatabaseRevision
    @classmethod
    def getHeadDatabaseRevision(
            cls, databaseUrl, resourcesPath =None, localResourcesPath =None, config =None):
        scripts = cls.getScriptsData(databaseUrl, resourcesPath=resourcesPath, config=config)
        result = scripts.get_current_head()
        return result

#___________________________________________________________________________________________________ getRevisionList
    @classmethod
    def getRevisionList(cls, databaseUrl, resourcesPath =None, localResourcesPath =None, config =None):
        if not cls.hasMigrationEnvironment(databaseUrl, resourcesPath=resourcesPath):
            return []

        scripts = cls.getScriptsData(databaseUrl, resourcesPath=resourcesPath, config=config)
        out = []
        for rev in scripts.iterate_revisions('head', 'base'):
            out.append(rev)
        return out

#___________________________________________________________________________________________________ stampDatabase
    @classmethod
    def stampDatabase(
            cls, databaseUrl, resourcesPath =None, localResourcesPath =None, revision ='head',
            config =None
    ):

        if config is None:
            config = cls.getConfig(
                databaseUrl=databaseUrl,
                resourcesPath=resourcesPath,
                localResourcesPath=localResourcesPath)

        alembicCmd.stamp(config=config, revision=revision)
        return True

#___________________________________________________________________________________________________ upgradeAppDatabases
    @classmethod
    def upgradeAppDatabases(
            cls, appName, resourcesPath =None, localResourcesPath =None, revision ='head'
    ):
        for db in cls.getAppDatabaseItems(
                appName=appName,
                localResourcesPath=localResourcesPath):

            cls.upgradeDatabase(
                databaseUrl=db.databaseUrl,
                resourcesPath=resourcesPath,
                localResourcesPath=localResourcesPath,
                revision=revision)

#___________________________________________________________________________________________________ upgradeDatabase
    @classmethod
    def upgradeDatabase(
            cls, databaseUrl, resourcesPath =None, localResourcesPath =None, revision ='head',
            config =None
    ):
        if config is None:
            config = cls.getConfig(
                databaseUrl,
                resourcesPath=resourcesPath,
                localResourcesPath=localResourcesPath)

        if config is None:
            return False

        current = cls.getCurrentDatabaseRevision(
            databaseUrl=databaseUrl,
            resourcesPath=resourcesPath,
            localResourcesPath=localResourcesPath,
            config=config)

        head = cls.getHeadDatabaseRevision(
            databaseUrl=databaseUrl,
            localResourcesPath=localResourcesPath,
            resourcesPath=resourcesPath,
            config=config)

        if current == head:
            return False

        alembicCmd.upgrade(config=config, revision=revision)
        return True

#___________________________________________________________________________________________________ databaseUrl
    @classmethod
    def createRevision(
            cls, databaseUrl, message, resourcesPath =None, localResourcesPath =None, info =None
    ):
        config = cls.getConfig(
            databaseUrl=databaseUrl,
            resourcesPath=resourcesPath,
            localResourcesPath=localResourcesPath)

        previousRevisions = cls.getRevisionList(
            databaseUrl=databaseUrl,
            resourcesPath=resourcesPath,
            localResourcesPath=localResourcesPath,
            config=config)

        alembicCmd.revision(
            config=config,
            message=StringUtils.toUnicode(len(previousRevisions)) + ': ' + message)

        if not info:
            return True

        scriptInfo = alembicScript.ScriptDirectory.from_config(config)
        scriptPath = None
        for item in os.listdir(scriptInfo.versions):
            if item.startswith(scriptInfo.get_current_head()):
                scriptPath = os.path.join(scriptInfo.versions, item)
                break
        if not scriptPath:
            return True

        info = StringUtils.toUnicode(info)

        f = open(scriptPath, 'r+')
        script = StringUtils.toUnicode(f.read())
        f.close()

        index   = script.find('"""')
        index   = script.find('"""', index + 1)
        script  = script[:index] + info + '\n' + script[index:]
        f       = open(scriptPath, 'w+')
        f.write(StringUtils.toStr2(script))
        f.close()
        return True

#___________________________________________________________________________________________________ getAppDatabaseItems
    @classmethod
    def getAppDatabaseItems(cls, appName, localResourcesPath =None):
        if not localResourcesPath:
            localResourcesPath = PyGlassEnvironment.getRootLocalResourcePath(isDir=True)

        databaseRoot = FileUtils.makeFolderPath(localResourcesPath, 'apps', appName, 'data')
        if not os.path.exists(databaseRoot):
            return []

        results = []
        FileUtils.walkPath(databaseRoot, cls._findAppDatabases, {
            'root':databaseRoot,
            'results':results,
            'appName':appName })

        return results

#___________________________________________________________________________________________________ initializeAppDatabases
    @classmethod
    def initializeAppDatabases(cls, appName, resourcesPath =None, localResourcesPath =None):
        out = False
        for r in cls.getAppDatabaseItems(appName, localResourcesPath=localResourcesPath):
            out = out or cls.initializeDatabase(
                databaseUrl=r.databaseUrl,
                resourcesPath=resourcesPath,
                localResourcesPath=localResourcesPath)
        return out

#___________________________________________________________________________________________________ initializeDatabase
    @classmethod
    def initializeDatabase(cls, databaseUrl, resourcesPath =None, localResourcesPath =None):

        migrationRootPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(
            databaseUrl=databaseUrl,
            root=True,
            resourcesPath=resourcesPath)

        migrationPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(
            databaseUrl=databaseUrl,
            resourcesPath=resourcesPath)

        configPath = FileUtils.makeFilePath(migrationPath, 'alembic.ini')

        if not os.path.exists(migrationRootPath):
            os.makedirs(migrationRootPath)

        if os.path.exists(migrationPath + 'alembic.ini'):
            return False

        os.chdir(migrationRootPath)

        config = alembicConfig.Config()
        config.config_file_name = configPath

        alembicCmd.init(config=config, directory=migrationPath)

        # Refresh config with proper settings
        cp = configparser.ConfigParser()
        cp.read(configPath)
        cp.set('alembic', 'sqlalchemy.url', PyGlassModelUtils.getEngineUrl(
            databaseUrl=databaseUrl,
            localResourcesPath=localResourcesPath))

        f = open(configPath, 'w+')
        cp.write(f)
        f.close()

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _changeDirToLocalAppPath
    @classmethod
    def _changeDirToLocalAppPath(cls, localResourcesPath):
        """_changeDirToLocalAppPath doc..."""
        if not localResourcesPath:
            localResourcesPath = PyGlassEnvironment.getRootLocalResourcePath(isDir=True)
        lastDir = os.path.abspath(os.curdir)
        os.chdir(localResourcesPath)
        return lastDir

#___________________________________________________________________________________________________ _findAppDatabases
    @classmethod
    def _findAppDatabases(cls, data):
        args    = data.data
        dirName = data.folder

        for item in os.listdir(dirName):
            itemPath = FileUtils.createPath(dirName, item)
            if os.path.isfile(itemPath) and itemPath.endswith('.vdb'):
                name = itemPath.replace(args['root'], '')[:-4]
                args['results'].append(cls.DATABASE_ITEM_NT(
                    path=itemPath,
                    name=name,
                    databaseUrl=args['appName'] + '://' + name ))

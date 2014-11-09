# AlembicUtils.py
# (C)2012
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os
import sys
from pyaid.string.StringUtils import StringUtils

if sys.version > '3':
    import configparser
else:
    import ConfigParser as configparser

from collections import namedtuple

try:
    # Alembic functionality is optional. Availability is determined during module imports.
    import alembic.config as alembicConfig
    import alembic.command as alembicCmd
    import alembic.script as alembicScript
    import alembic.environment as alembicEnv
    ALEMBIC_SUPPORTED = True
except Exception:
    ALEMBIC_SUPPORTED = False

from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.sqlalchemy.PyGlassModelUtils import PyGlassModelUtils

#___________________________________________________________________________________________________ AlembicUtils
class AlembicUtils(object):
    """A utility class for Alembic migration management within PyGlass applications."""

#===================================================================================================
#                                                                                       C L A S S

    DATABASE_ITEM_NT = namedtuple('DATABASE_ITEM_NT', ['databaseUrl', 'name', 'path'])

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: hasAlembic
    @ClassGetter
    def hasAlembic(cls):
        """Specifies whether or not the Alembic package is available for use."""
        global ALEMBIC_SUPPORTED
        return ALEMBIC_SUPPORTED

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ hasMigrationEnvironment
    @classmethod
    def hasMigrationEnvironment(cls, databaseUrl):
        migrationPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(databaseUrl)
        if not os.path.exists(migrationPath):
            return False
        if not os.path.exists(os.path.join(migrationPath, 'alembic.ini')):
            return False
        if not os.path.exists(migrationPath + 'versions'):
            return False
        return True

#___________________________________________________________________________________________________ getConfig
    @classmethod
    def getConfig(cls, databaseUrl, writeCallback =None):
        logger = Logger(
            databaseUrl.replace('://', '~').replace('/', '--').replace('.vdb', ''),
            useStorageBuffer=True)

        if writeCallback is not None:
            logger.addWriteCallback(writeCallback)

        migrationPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(databaseUrl)
        config = alembicConfig.Config(os.path.join(migrationPath, 'alembic.ini'), stdout=logger)

        config.set_main_option(
            'script_location',
            migrationPath)

        config.set_main_option(
            'sqlalchemy.url',
            PyGlassModelUtils.getEngineUrl(databaseUrl))

        config.set_main_option(
            'url',
            PyGlassModelUtils.getEngineUrl(databaseUrl))

        return config

#___________________________________________________________________________________________________ getScriptsData
    @classmethod
    def getScriptsData(cls, databaseUrl, config =None):
        if not config:
            config = cls.getConfig(databaseUrl)
        return alembicScript.ScriptDirectory.from_config(config)

#___________________________________________________________________________________________________ getCurrentDatabaseRevision
    @classmethod
    def getCurrentDatabaseRevision(cls, databaseUrl, config =None):
        if not config:
            config = cls.getConfig(databaseUrl)
        return alembicCmd.current(config)

#___________________________________________________________________________________________________ getCurrentDatabaseRevision
    @classmethod
    def getHeadDatabaseRevision(cls, databaseUrl, config =None):
        scripts = cls.getScriptsData(databaseUrl, config)
        return scripts.get_current_head()

#___________________________________________________________________________________________________ getRevisionList
    @classmethod
    def getRevisionList(cls, databaseUrl, config =None):
        if not cls.hasMigrationEnvironment(databaseUrl):
            return []

        scripts = cls.getScriptsData(databaseUrl, config)
        out = []
        for rev in scripts.iterate_revisions('head', 'base'):
            out.append(rev)
        return out

#___________________________________________________________________________________________________ stampDatabase
    @classmethod
    def stampDatabase(cls, databaseUrl, revision ='head'):
        alembicCmd.stamp(cls.getConfig(databaseUrl), revision)
        return True

#___________________________________________________________________________________________________ upgradeAppDatabases
    @classmethod
    def upgradeAppDatabases(cls, appName, revision ='head'):
        for db in cls.getAppDatabaseItems(appName):
            cls.upgradeDatabase(db.databaseUrl, revision=revision)

#___________________________________________________________________________________________________ upgradeDatabase
    @classmethod
    def upgradeDatabase(cls, databaseUrl, revision ='head', config =None):
        if config is None:
            config = cls.getConfig(databaseUrl)

        current = cls.getCurrentDatabaseRevision(databaseUrl, config)
        if current is None:
            return False

        head = cls.getHeadDatabaseRevision(databaseUrl, config)
        if current == head:
            return False

        alembicCmd.upgrade(config=config, revision=revision)
        return True

#___________________________________________________________________________________________________ databaseUrl
    @classmethod
    def createRevision(cls, databaseUrl, message, info =None):
        config = cls.getConfig(databaseUrl)

        previousRevisions = cls.getRevisionList(databaseUrl, config=config)

        alembicCmd.revision(
            config=config,
            message=StringUtils.toUnicode(len(previousRevisions)) + ': ' + message
        )
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

        f      = open(scriptPath, 'r+')
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
    def getAppDatabaseItems(cls, appName):
        databaseRoot = PyGlassEnvironment.getRootResourcePath('apps', appName, 'data')
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
    def initializeAppDatabases(cls, appName):
        out = False
        for r in cls.getAppDatabaseItems(appName):
            out = out or cls.initializeDatabase(r.databaseUrl)
        return out

#___________________________________________________________________________________________________ initializeDatabase
    @classmethod
    def initializeDatabase(cls, databaseUrl):
        migrationRootPath = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(databaseUrl, root=True)
        migrationPath     = PyGlassModelUtils.getMigrationPathFromDatabaseUrl(databaseUrl)
        configPath        = os.path.join(migrationPath, 'alembic.ini')
        workingPath       = os.curdir

        if not os.path.exists(migrationRootPath):
            os.makedirs(migrationRootPath)

        if os.path.exists(migrationPath + 'alembic.ini'):
            return False

        os.chdir(migrationRootPath)

        config                  = alembicConfig.Config()
        config.config_file_name = configPath

        alembicCmd.init(
            config=config,
            directory=migrationPath
        )

        # Refresh config with proper settings
        cp = configparser.ConfigParser()
        cp.read(configPath)
        cp.set('alembic', 'sqlalchemy.url', PyGlassModelUtils.getEngineUrl(databaseUrl))

        f = open(configPath, 'w+')
        cp.write(f)
        f.close()

        os.chdir(workingPath)
        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _findAppDatabases
    @classmethod
    def _findAppDatabases(cls, data):
        args    = data.data
        dirname = data.folder

        for item in os.listdir(dirname):
            itemPath = FileUtils.createPath(dirname, item)
            if os.path.isfile(itemPath) and itemPath.endswith('.vdb'):
                name = itemPath.replace(args['root'], '')[:-4]
                args['results'].append(cls.DATABASE_ITEM_NT(
                    path=itemPath,
                    name=name,
                    databaseUrl=args['appName'] + '://' + name ))

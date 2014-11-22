# PyGlassEnvironment.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os
from pyaid.string.StringUtils import StringUtils


try:
    import appdirs
except Exception as err:
    appdirs = None

import requests.utils

from pyaid.OsUtils import OsUtils
from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

# AS NEEDED: from pyglass.elements.icons.TextureAtlasManager import TextureAtlasManager

#___________________________________________________________________________________________________ PyGlassEnvironment
class PyGlassEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    BASE_UNIX_TIME         = 1293868800

    _ENV_PATH              = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    _ENV_SETTINGS          = None
    _GLOBAL_SETTINGS_FILE  = 'environment.vcd'

    _application           = None
    _rootResourcePath      = None
    _rootLocalResourcePath = None
    _isDeployed            = None
    _atlasManager          = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isInitialized
    @ClassGetter
    def isInitialized(cls):
        return bool(cls._rootLocalResourcePath is not None)

#___________________________________________________________________________________________________ GS: atlasManager
    @ClassGetter
    def atlasManager(cls):
        if cls._atlasManager is None:
            from pyglass.elements.icons.TextureAtlasManager import TextureAtlasManager
            cls._atlasManager = TextureAtlasManager()
        return cls._atlasManager

#___________________________________________________________________________________________________ GS: mainWindow
    @ClassGetter
    def mainWindow(cls):
        return cls._application.mainWindow

#___________________________________________________________________________________________________ GS: application
    @ClassGetter
    def application(cls):
        return cls._application

#___________________________________________________________________________________________________ GS: qApplication
    @property
    def qApplication(cls):
        return cls._application.q

#___________________________________________________________________________________________________ isDeployed
    @ClassGetter
    def isDeployed(cls):
        try:
            if cls._isDeployed is None:
                if OsUtils.isWindows():
                    cls._isDeployed = cls._ENV_PATH.find(os.sep + 'library.zip' + os.sep) != -1
                elif OsUtils.isMac():
                    cls._isDeployed = cls._ENV_PATH.find(os.sep + 'site-packages.zip' + os.sep) != -1
            return cls._isDeployed
        except Exception as err:
            return True

#___________________________________________________________________________________________________ GS: isWindows
    @ClassGetter
    def isWindows(cls):
        return OsUtils.isWindows()

#___________________________________________________________________________________________________ requestsCABundle
    @ClassGetter
    def requestsCABundle(cls):
        if cls.isDeployed:
            return  cls.getRootResourcePath(
                'pythonRoot', 'site-packages', 'requests', 'cacert.pem', isFile=True)
        return requests.utils.DEFAULT_CA_BUNDLE_PATH

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getInstallationPath
    @classmethod
    def getInstallationPath(cls, *args, **kwargs):
        """getInstallationPath doc..."""
        if not cls.isDeployed or not OsUtils.isWindows():
            return None
        parts = cls._ENV_PATH.split(os.sep + 'library.zip' + os.sep)
        return FileUtils.createPath(parts[0], *args, **kwargs)

#___________________________________________________________________________________________________ initializeCreatePathAppSettings
    @classmethod
    def initializeCreatePathAppSettings(cls, *args, **kwargs):
        rootPath = FileUtils.createPath(*args, **kwargs)
        cls._rootResourcePath       = FileUtils.createPath(rootPath, 'resources', isDir=True)
        cls._rootLocalResourcePath  = FileUtils.createPath(rootPath, 'resources', 'local', isDir=True)

#___________________________________________________________________________________________________ initializeCurrentPathAppSettings
    @classmethod
    def initializeCurrentPathAppSettings(cls):
        cls.initializeCreatePathAppSettings(os.path.abspath(os.curdir), isDir=True)

#___________________________________________________________________________________________________ initializeFromInternalPath
    @classmethod
    def initializeFromInternalPath(cls, referencePath, force =False):
        """ Used to explicitly initialiize the pyglass environment when running inside the source
            code respository with a standard structure where the repository root has a src and
            a resources folder. """

        if cls.isInitialized and not force:
            return True

        path = FileUtils.cleanupPath(referencePath, noTail=True)
        if os.path.isfile(path):
            path = FileUtils.getDirectoryOf(referencePath, noTail=True)

        rootPath = None
        while path:
            srcPath = FileUtils.makeFolderPath(path, 'src', isDir=True)
            resPath = FileUtils.makeFolderPath(path, 'resources', isDir=True)
            if os.path.exists(srcPath) and os.path.exists(resPath):
                rootPath = path
                break
            path = FileUtils.getDirectoryOf(path, noTail=True)

        if not rootPath:
            return False

        cls._rootResourcePath       = FileUtils.makeFolderPath(rootPath, 'resources')
        cls._rootLocalResourcePath  = FileUtils.makeFolderPath(rootPath, 'resources', 'local')
        return True

#___________________________________________________________________________________________________ initializeExplicitAppSettings
    @classmethod
    def initializeExplicitAppSettings(cls, rootResourcePath, rootLocalResourcePath):
        cls._rootResourcePath = FileUtils.cleanupPath(rootResourcePath, isDir=True)
        cls._rootLocalResourcePath = FileUtils.cleanupPath(rootLocalResourcePath, isDir=True)

#___________________________________________________________________________________________________ initializeAppSettings
    @classmethod
    def initializeAppSettings(cls, application):
        cls._application           = application
        cls._rootResourcePath      = cls._getRootResourcePath(application)
        cls._rootLocalResourcePath = cls._getRootLocalResourcePath(application)

#___________________________________________________________________________________________________ getPyGlassResourcePath
    @classmethod
    def getPyGlassResourcePath(cls, *args, **kwargs):
        if cls.isDeployed:
            return cls.getRootResourcePath('pyglass', *args, **kwargs)

        return FileUtils.createPath(
            cls._ENV_PATH, '..', '..', '..', 'resources', 'pyglass', *args, **kwargs)

#___________________________________________________________________________________________________ getRootResourcePath
    @classmethod
    def getRootResourcePath(cls, *args, **kwargs):
        return FileUtils.createPath(cls._rootResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getRootLocalResourcePath
    @classmethod
    def getRootLocalResourcePath(cls, *args, **kwargs):
        return FileUtils.createPath(cls._rootLocalResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ settingsFileExists
    @classmethod
    def settingsFileExists(cls):
        return os.path.exists(
            cls.getRootLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getRootResourcePath
    @classmethod
    def _getRootResourcePath(cls, application):
        if cls.isDeployed:
            if OsUtils.isWindows():
                out = FileUtils.createPath(
                    appdirs.user_data_dir(application.appID, application.appGroupID),
                    'resources', isDir=True)
            else:
                out = FileUtils.createPath(
                    cls._ENV_PATH.split('/Resources/lib/')[0],
                    'Resources', 'resources', isDir=True)
        else:
            rootPath = application.debugRootResourcePath
            if not rootPath:
                return None
            elif StringUtils.isStringType(rootPath):
                rootPath = rootPath.replace('\\', '/').strip('/').split('/')

            out = FileUtils.createPath(
                application.applicationCodePath, *rootPath, isDir=True)

        if out and not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ _getRootLocalResourcePath
    @classmethod
    def _getRootLocalResourcePath(cls, application):
        if cls.isDeployed:
            out = FileUtils.createPath(
                appdirs.user_data_dir(application.appID, application.appGroupID),
                'local_resources', isDir=True)
        else:
            rootPath = application.debugRootResourcePath
            if not rootPath:
                return None
            elif StringUtils.isStringType(rootPath):
                rootPath = rootPath.replace('\\', '/').strip('/').split('/')

            out = FileUtils.createPath(
                application.applicationCodePath, rootPath, 'local', isDir=True)

        if out and not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ _setEnvValue
    @classmethod
    def _setEnvValue(cls, key, value):
        settings = cls._getEnvValue(None) if cls._ENV_SETTINGS is None else cls._ENV_SETTINGS
        if settings is None:
            settings = dict()
            cls._ENV_SETTINGS = settings

        if StringUtils.isStringType(key):
            key = [key]

        src = settings
        for k in key[:-1]:
            src = src[k]
        src[key[-1]] = value

        envPath = cls.getRootLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True)
        envDir  = os.path.dirname(envPath)
        if not os.path.exists(envDir):
            os.makedirs(envDir)

        f = open(envPath, 'w+')
        try:
            f.write(JSON.asString(cls._ENV_SETTINGS))
        except Exception:
            print('ERROR: Unable to write environmental settings file at: ' + envPath)
            return False
        finally:
            f.close()

        return True

#___________________________________________________________________________________________________ _getEnvValue
    @classmethod
    def _getEnvValue(cls, key, defaultValue =None, refresh =False, error =False):
        if cls._ENV_SETTINGS is None or refresh:
            if not cls.settingsFileExists():
                print('WARNING: No environmental settings file found.')
                return defaultValue

            envPath = cls.getRootLocalResourcePath(cls._GLOBAL_SETTINGS_FILE, isFile=True)
            f = open(envPath, 'r+')
            try:
                res = f.read()
            except Exception:
                print('ERROR: Unable to read the environmental settings file at: ' + envPath)
                return
            finally:
                f.close()

            try:
                settings = JSON.fromString(res)
            except Exception:
                print('ERROR: Unable to parse environmental settings file at: ' + envPath)
                return

            cls._ENV_SETTINGS = settings
        else:
            settings = cls._ENV_SETTINGS

        if key is None:
            return settings

        if StringUtils.isStringType(key):
            key = [key]
        value = settings
        for k in key:
            if k in value:
                value = value[k]
            else:
                if error:
                    raise Exception('Missing environmental setting: ' + str(key))
                return defaultValue

        return value

# PyGlassApplicationCompiler.py
# (C)2013
# Scott Ernst

import os
import shutil
import inspect

from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON
from pyaid.reflection.Reflection import Reflection
from pyaid.string.StringUtils import StringUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum
from pyglass.compile.ResourceCollector import ResourceCollector
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ PyGlassApplicationCompiler
class PyGlassApplicationCompiler(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _CLEANUP_FOLDERS = ['build', 'dist', 'resources', 'src']

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of PyGlassApplicationCompiler."""
        self._application = self.applicationClass()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: siteLibraries
    @property
    def siteLibraries(self):
        return Reflection.getReflectionList(SiteLibraryEnum)

#___________________________________________________________________________________________________ GS: iconPath
    @property
    def iconPath(self):
        return None

#___________________________________________________________________________________________________ GS: resources
    @property
    def resources(self):
        return []

#___________________________________________________________________________________________________ GS: binPath
    @property
    def binPath(self):
        return None

#___________________________________________________________________________________________________ GS: appFilename
    @property
    def appFilename(self):
        return None

#___________________________________________________________________________________________________ GS: appDisplayName
    @property
    def appDisplayName(self):
        if self.appFilename:
            return self.appFilename
        return self.application.appID if self.application else None

#___________________________________________________________________________________________________ GS: applicationClass
    @property
    def applicationClass(self):
        return None

#___________________________________________________________________________________________________ GS: ignoreExtensions
    @property
    def ignoreExtensions(self):
        return ['.ui', '.ai', '.psd']

#___________________________________________________________________________________________________ GS: application
    @property
    def application(self):
        return self._application

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""

        binPath = self.getBinPath(isDir=True)
        if not os.path.exists(binPath):
            os.makedirs(binPath)

        for d in self._CLEANUP_FOLDERS:
            path = os.path.join(binPath, d)
            if os.path.exists(path):
                shutil.rmtree(path)

        os.chdir(binPath)
        result = SystemUtils.executeCommand('python %s py2exe' % self._createSetupFile(binPath))
        if result['code']:
            print 'COMPILATION ERROR:'
            print result['error']
            return False

        if self.appFilename:
            name   = self.applicationClass.__name__
            source = FileUtils.createPath(binPath, 'dist', name + '.exe', isFile=True)
            dest   = FileUtils.createPath(binPath, 'dist', self.appFilename + '.exe', isFile=True)
            os.rename(source, dest)

        ResourceCollector(self, verbose=True).run()

        self._createNsisInstallerScript(binPath)

        return True

#___________________________________________________________________________________________________ getBinPath
    def getBinPath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            os.path.dirname(inspect.getabsfile(self.__class__)), self.binPath, *args, **kwargs
        )

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getIconPath
    def _getIconPath(self):
        path = self.iconPath
        if not path:
            return ''

        if isinstance(path, basestring):
            if os.path.isabs(path) and os.path.exists(path):
                return FileUtils.cleanupPath(path)
            else:
                path = path.replace('\\', '/').strip('/').split('/')

        out = PyGlassEnvironment.getRootResourcePath(*path, isFile=True)
        if os.path.exists(out):
            return out
        return ''

#___________________________________________________________________________________________________ _createSetupFile
    def _createSetupFile(self, binPath):
        path = FileUtils.createPath(binPath, 'setup.py', isFile=True)
        scriptPath = inspect.getabsfile(self.applicationClass)

        try:
            sourcePath = PyGlassEnvironment.getPyGlassResourcePath(
                '..', 'setupSource.txt', isFile=True
            )
            f      = open(sourcePath, 'r+')
            source = f.read()
            f.close()
        except Exception, err:
            print err
            return None

        try:
            f = open(path, 'w+')
            f.write(source.replace(
                '##SCRIPT_PATH##', StringUtils.escapeBackSlashes(scriptPath)
            ).replace(
                '##RESOURCES##', StringUtils.escapeBackSlashes(JSON.asString(self.resources))
            ).replace(
                '##INCLUDES##', StringUtils.escapeBackSlashes(JSON.asString(self.siteLibraries))
            ).replace(
                '##ICON_PATH##', StringUtils.escapeBackSlashes(self._getIconPath())
            ))
            f.close()
        except Exception, err:
            print err
            return None

        return path

#___________________________________________________________________________________________________ _createNsisInstallerScript
    def _createNsisInstallerScript(self, binPath):
        path = FileUtils.createPath(binPath, 'installer.nsi', isFile=True)

        try:
            sourcePath = PyGlassEnvironment.getPyGlassResourcePath(
                '..', 'installer.tmpl.nsi', isFile=True
            )
            f = open(sourcePath, 'r+')
            source = f.read()
            f.close()
        except Exception, err:
            print err
            return None

        try:
            f = open(path, 'w+')
            f.write(source.replace(
                '##APP_NAME##', self.appDisplayName
            ).replace(
                '##APP_ID##', self.application.appID
            ).replace(
                '##APP_GROUP_ID##', self.application.appGroupID
            ))
            f.close()
        except Exception, err:
            print err
            return None

        return path

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

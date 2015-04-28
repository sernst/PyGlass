# PyGlassApplicationCompiler.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import sys
import os
import shutil
import inspect

from pyaid.OsUtils import OsUtils
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
        # noinspection PyCallingNonCallable
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

#___________________________________________________________________________________________________ GS: resourceAppIds
    @property
    def resourceAppIds(self):
        return [self._application.appID]

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

        # Create the bin directory where the output will be stored if it does not already exist
        binPath = self.getBinPath(isDir=True)
        if not os.path.exists(binPath):
            os.makedirs(binPath)

        # Remove any folders created by previous build attempts
        for d in self._CLEANUP_FOLDERS:
            path = os.path.join(binPath, d)
            if os.path.exists(path):
                shutil.rmtree(path)

        os.chdir(binPath)

        ResourceCollector(self, verbose=True).run()

        cmd = [
            FileUtils.makeFilePath(sys.prefix, 'bin', 'python'),
            '"%s"' % self._createSetupFile(binPath),
            OsUtils.getPerOsValue('py2exe', 'py2app'), '>',
            '"%s"' % self.getBinPath('setup.log', isFile=True)]

        print('[COMPILING]: Executing %s' % OsUtils.getPerOsValue('py2exe', 'py2app'))
        print('[COMMAND]: %s' % ' '.join(cmd))
        result = SystemUtils.executeCommand(cmd, remote=False, wait=True)
        if result['code']:
            print('COMPILATION ERROR:')
            print(result['out'])
            print(result['error'])
            return False

        if self.appFilename and OsUtils.isWindows():
            name   = self.applicationClass.__name__
            source = FileUtils.createPath(binPath, 'dist', name + '.exe', isFile=True)
            dest   = FileUtils.createPath(binPath, 'dist', self.appFilename + '.exe', isFile=True)
            os.rename(source, dest)

        if OsUtils.isWindows() and not self._createWindowsInstaller(binPath):
            print('Installer Creation Failed')
            return False
        elif OsUtils.isMac() and not self._createMacDmg(binPath):
            print('DMG Creation Failed')
            return False

        # Remove the resources path once compilation is complete
        resourcePath = FileUtils.createPath(binPath, 'resources', isDir=True)
        SystemUtils.remove(resourcePath)

        buildPath = FileUtils.createPath(binPath, 'build', isDir=True)
        SystemUtils.remove(buildPath)

        FileUtils.openFolderInSystemDisplay(binPath)

        return True

#___________________________________________________________________________________________________ getBinPath
    def getBinPath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            os.path.dirname(inspect.getabsfile(self.__class__)), self.binPath, *args, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createMacDmg
    def _createMacDmg(self, binPath):
        print('CREATING Mac DMG')
        target   = FileUtils.createPath(binPath, self.application.appID + '.dmg', isFile=True)
        tempTarget = FileUtils.createPath(binPath, 'pack.tmp.dmg', isFile=True)
        distPath = FileUtils.createPath(binPath, 'dist', isDir=True, noTail=True)

        if os.path.exists(tempTarget):
            SystemUtils.remove(tempTarget)

        cmd = ['hdiutil', 'create', '-size', '500m', '"%s"' % tempTarget, '-ov', '-volname',
            '"%s"' % self.appDisplayName, '-fs', 'HFS+', '-srcfolder', '"%s"' % distPath]

        result = SystemUtils.executeCommand(cmd, wait=True)
        if result['code']:
            print('Failed Command Execution:')
            print(result)
            return False

        cmd = ['hdiutil', 'convert', "%s" % tempTarget, '-format', 'UDZO', '-imagekey',
               'zlib-level=9', '-o', "%s" % target]

        if os.path.exists(target):
            SystemUtils.remove(target)

        result = SystemUtils.executeCommand(cmd)
        if result['code']:
            print('Failed Command Execution:')
            print(result)
            return False

        SystemUtils.remove(tempTarget)
        return True

#___________________________________________________________________________________________________ _createWindowsInstaller
    def _createWindowsInstaller(self, binPath):
        self._createNsisInstallerScript(binPath)

        nsisPath = 'C:\\Program Files (x86)\\NSIS\\makensis.exe'
        if os.path.exists(nsisPath):
            print('PACKAGING: NSIS Installer')
            result = SystemUtils.executeCommand('"%s" "%s"' % (
                nsisPath, FileUtils.createPath(binPath, 'installer.nsi', isFile=True)))
            if result['code']:
                print('PACKAGING ERROR:')
                print(result['error'])
                return False

        return True

#___________________________________________________________________________________________________ _getIconPath
    def _getIconPath(self):
        path = self.iconPath
        if not path:
            return ''

        if StringUtils.isStringType(path):
            path = StringUtils.toUnicode(path)
            if os.path.isabs(path) and os.path.exists(path):
                return FileUtils.cleanupPath(path)
            else:
                path = path.replace('\\', '/').strip('/').split('/')

        path.append('icons' if OsUtils.isWindows() else 'icons.iconset')
        out = PyGlassEnvironment.getRootResourcePath(*path, isDir=True)
        if os.path.exists(out):
            return out
        return ''

#___________________________________________________________________________________________________ _createIcon
    def _createIcon(self, binPath):
        iconPath = self._getIconPath()
        if not iconPath:
            return iconPath

        if os.path.isfile(iconPath):
            return iconPath

        #-------------------------------------------------------------------------------------------
        # MAC ICON CREATION
        #       On OSX use Apple's iconutil (XCode developer tools must be installed) to create an
        #       icns file from the icons.iconset folder at the specified location.
        if OsUtils.isMac():
            targetPath = FileUtils.createPath(binPath, self.appDisplayName + '.icns', isFile=True)
            result = SystemUtils.executeCommand([
                'iconutil', '-c', 'icns', '-o', '"' + targetPath + '"', '"' + iconPath + '"'])
            if result['code']:
                return ''
            return targetPath

        #-------------------------------------------------------------------------------------------
        # WINDOWS ICON CREATION
        #       On Windows use convert (ImageMagick must be installed and on the PATH) to create an
        #       ico file from the icons folder of png files.
        result = SystemUtils.executeCommand('where convert')
        if result['code']:
            return ''
        items = result['out'].replace('\r', '').strip().split('\n')
        convertCommand = None
        for item in items:
            if item.find('System32') == -1:
                convertCommand = item
                break
        if not convertCommand:
            return ''

        images = os.listdir(iconPath)
        cmd = ['"' + convertCommand + '"']
        for image in images:
            if not StringUtils.ends(image, ('.png', '.jpg')):
                continue
            imagePath = FileUtils.createPath(iconPath, image, isFile=True)
            cmd.append('"' + imagePath + '"')
        if len(cmd) < 2:
            return ''

        targetPath = FileUtils.createPath(binPath, self.appDisplayName + '.ico', isFile=True)
        cmd.append('"' + targetPath + '"')

        result = SystemUtils.executeCommand(cmd)
        if result['code'] or not os.path.exists(targetPath):
            print('FAILED:')
            print(result['command'])
            print(result['error'])
            return ''

        return targetPath

#___________________________________________________________________________________________________ _createSetupFile
    def _createSetupFile(self, binPath):
        path = FileUtils.createPath(binPath, 'setup.py', isFile=True)
        scriptPath = inspect.getabsfile(self.applicationClass)

        try:
            sourcePath = PyGlassEnvironment.getPyGlassResourcePath(
                '..', 'setupSource.txt', isFile=True)
            f      = open(sourcePath, 'r+')
            source = f.read()
            f.close()
        except Exception as err:
            print(err)
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
                '##ICON_PATH##', StringUtils.escapeBackSlashes(self._createIcon(binPath))
            ).replace(
                '##APP_NAME##', self.appDisplayName
            ).replace(
                '##SAFE_APP_NAME##', self.appDisplayName.replace(' ', '_') ))
            f.close()
        except Exception as err:
            print(err)
            return None

        return path

#___________________________________________________________________________________________________ _createNsisInstallerScript
    def _createNsisInstallerScript(self, binPath):
        path = FileUtils.createPath(binPath, 'installer.nsi', isFile=True)

        try:
            sourcePath = PyGlassEnvironment.getPyGlassResourcePath(
                '..', 'installer.tmpl.nsi', isFile=True)
            f = open(sourcePath, 'r+')
            source = f.read()
            f.close()
        except Exception as err:
            print(err)
            return None

        try:
            f = open(path, 'w+')
            f.write(source.replace(
                '##APP_NAME##', self.appDisplayName
            ).replace(
                '##APP_ID##', self.application.appID
            ).replace(
                '##APP_GROUP_ID##', self.application.appGroupID
            ).replace(
                '##SAFE_APP_NAME##', self.appDisplayName.replace(' ', '_') ))
            f.close()
        except Exception as err:
            print(err)
            return None

        return path

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

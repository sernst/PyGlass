# SetupConstructor.py
# (C)2013
# Scott Ernst

import os
import sys
from glob import glob

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.reflection.Reflection import Reflection

from pyglass.compile.SiteLibrarySetup import LIBRARY_INCLUDES
from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum

#___________________________________________________________________________________________________ SetupConstructor
class SetupConstructor(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _PROGRAM_FILES_PATHS = ['C:\\Program Files\\', 'C:\\Program Files (x86)\\']

#___________________________________________________________________________________________________ __init__
    def __init__(self, fileReference, **kwargs):
        """Creates a new instance of SetupConstructor."""
        self.sourceFile  = os.path.abspath(fileReference)
        self.sourcePath  = os.path.dirname(self.sourceFile)

        self._scriptPath = None
        self._iconPath   = None
        self._paths      = None
        self._includes   = None

        os.chdir(self.sourcePath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getSetupKwargs
    def getSetupKwargs(self, **kwargs):
        """Doc..."""
        # Adds tools vmi packages to python system path
        os.chdir(self.sourcePath)

        self._iconPath   = ArgsUtils.get('iconPath', '', kwargs)
        self._scriptPath = ArgsUtils.get('scriptPath', None, kwargs)
        self._paths      = ArgsUtils.getAsList('resources', kwargs)
        self._includes   = ArgsUtils.getAsList('includes', kwargs)
        for path in self._paths:
            sys.path.append(path)

        #-------------------------------------------------------------------------------------------
        # FIND MS VISUAL STUDIO RUNTIME DLLS
        dllPath = None
        for rootPath in self._PROGRAM_FILES_PATHS:
            path = rootPath + "Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT"
            if os.path.exists(path):
                dllPath = path
                break
        if dllPath is None:
            raise Exception, "Unable to find Microsoft Visual Studio 9.0 installation."

        sys.path.append(dllPath)
        dataFiles = [("Microsoft.VC90.CRT", glob(dllPath + r'\*.*'))]
        values    = self._getSiteValues(dataFiles, [], [])

        window = {'script':self._scriptPath}

        if self._iconPath:
            window['icon_resources'] = [(1, self._iconPath)]

        out = dict(
            windows=[window],
            data_files=values['dataFiles'],
            options={
                'py2exe':{
                    'packages':values['packages'],
                    'includes':values['includes']
                }
            }
        )
        return out

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getDataFiles
    def _getSiteValues(self, dataFiles, packages, includes):
        out = {'dataFiles':dataFiles, 'packages':packages, 'includes':includes}

        definitions = Reflection.getReflectionList(LIBRARY_INCLUDES)
        for d in definitions:
            if d.id != SiteLibraryEnum.COMMON and d.id not in self._includes:
                continue

            if d.dataFiles:
                dataFiles += d.dataFiles
            if d.packages:
                packages += d.packages
            if d.includes:
                includes += d.includes

        return out

#___________________________________________________________________________________________________ createPath
    def createPath(self, root, *args, **kwargs):
        return FileUtils.createPath(root, *args, **kwargs)

#___________________________________________________________________________________________________ createSourceRelativePath
    def createSourceRelativePath(self, *args, **kwargs):
        return FileUtils.createPath(self.sourcePath, *args, **kwargs)

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


# WidgetUiCompiler.py
# (C)2013
# Scott Ernst

import sys
import os
import re
import py_compile
import subprocess

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ WidgetUiCompiler
class WidgetUiCompiler(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _CLASS_NAME_RE = re.compile('(?<=class )(?P<classname>[a-zA-z0-9_]+)(?=\()')

    _SETUP_UI_RE = re.compile('(?<=def setupUi\(self, )(?P<parentName>[a-zA-z0-9_\-]+)(?=\):)')

    _RETRANSLATE_RE = re.compile(
        '(?<=def retranslateUi\(self, )(?P<parentName>[a-zA-z0-9_\-]+)(?=\):)'
    )

    _SELF_RE = re.compile('(?P<self>self\.)(?!retranslateUi\()')

#___________________________________________________________________________________________________ __init__
    def __init__(self, rootPath =None, recursive =True, **kwargs):
        """Creates a new instance of WidgetUiCompiler."""
        self._log        = Logger(self)
        self._verbose    = ArgsUtils.get('verbose', False, kwargs)
        self._recursive  = recursive
        self._pythonPath = os.path.normpath(sys.exec_prefix)

        if rootPath and os.path.isabs(rootPath):
            self._rootPath = FileUtils.cleanupPath(rootPath, isDir=True)
        elif rootPath:
            parts = rootPath.split(os.sep if rootPath.find(os.sep) != -1 else '/')
            self._rootPath = PyGlassEnvironment.getRootResourcePath(*parts, isDir=True)
        else:
            self._rootPath = PyGlassEnvironment.getRootResourcePath()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""

        arg = dict()
        if self._recursive:
            os.path.walk(self._rootPath, self._compileInFolder, arg)
        else:
            self._compileInFolder(arg, self._rootPath, os.listdir(self._rootPath))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _compileInFolder
    def _compileInFolder(self, arg, dirname, names):
        for name in names:
            if not name.endswith('.ui'):
                continue
            self._compileUiFile(dirname, name)

#___________________________________________________________________________________________________ _compileUiFile
    def _compileUiFile(self, path, filename):
        """Doc..."""

        source = FileUtils.createPath(path, filename, isFile=True)
        if self._verbose:
            self._log.write('COMPILING: ' + source)

        cmd = '%s %s' % (
            FileUtils.createPath(self._pythonPath, 'Scripts', 'pyside-uic.exe'),
            source
        )
        pipe = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, error = pipe.communicate()

        if pipe.returncode or error:
            self._log.write('ERROR: Failed to compile %s widget: %s' % (str(source), str(error)))
            return False

        res = WidgetUiCompiler._CLASS_NAME_RE.search(out)
        if not res:
            self._log.write('ERROR: Failed to find widget class name for ' + str(source))
            return False
        out = WidgetUiCompiler._CLASS_NAME_RE.sub('PySideUiFileSetup', out, 1)

        res = WidgetUiCompiler._SETUP_UI_RE.search(out)
        if not res:
            self._log.write('ERROR: Failed to find widget setupUi method for ' + str(source))
            return False
        targetName = res.groupdict().get('parentName')
        out = WidgetUiCompiler._SETUP_UI_RE.sub('\g<parentName>', out, 1)

        res = WidgetUiCompiler._RETRANSLATE_RE.search(out)
        if not res:
            self._log.write('ERROR: Failed to find widget retranslateUi method for ' + str(source))
            return False
        out = WidgetUiCompiler._RETRANSLATE_RE.sub('\g<parentName>', out, 1)

        if isinstance(out, unicode):
            out = out.encode('utf8', 'ignore')

        out = WidgetUiCompiler._SELF_RE.sub(targetName + '.', out)

        dest = FileUtils.createPath(path, filename[:-3] + '.py', isFile=True)
        if os.path.exists(dest):
            os.remove(dest)
        f = open(dest, 'w+')
        f.write(out)
        f.close()

        py_compile.compile(dest)
        return True


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

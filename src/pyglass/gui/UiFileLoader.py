# UiFileLoader.py
# (C)2012-2014
# Scott Ernst


from __future__ import print_function, absolute_import, unicode_literals, division

import os
import sys
import importlib
from pyaid.list.ListUtils import ListUtils

if sys.version < '3':
    # noinspection PyDeprecation
    import imp
else:
    imp = None

from PySide import QtCore
from PySide import QtGui

try:
    # Fixes issue in 1.2.2 for Python 3.4 missing this module in the module listing
    from PySide import QtUiTools
except Exception:
    QtUiTools = None

from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ UiFileLoader
class UiFileLoader(QtUiTools.QUiLoader):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, target):
        super(UiFileLoader, self).__init__()
        self._target = target

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createWidget
    def createWidget(self, class_name, parent=None, name=''):
        # Case where target should be used as widget.
        if parent is None and self._target:
            return self._target

        # Otherwise create a new widget
        else:
            # create a new widget for child widgets
            widget = QtUiTools.QUiLoader.createWidget(self, class_name, parent, name)

            # Adds attribute for the new child widget on the target to mimic PyQt4.uic.loadUi.
            if self._target:
                setattr(self._target, name, widget)

            return widget

#___________________________________________________________________________________________________ loadFileIntoTarget
    @classmethod
    def loadFileIntoTarget(cls, target, widgetPath):
        """ Loads the given UI file directly into the target object instead of creating a new
            child widget.

            @@@param target:QWidget
                The object in which to load the values from the ui file.

            @@@param uiFile:String
                Absolute file path to the ui file on which to load.
        """

        f = QtCore.QFile(widgetPath)
        f.open(QtCore.QFile.ReadOnly)

        loader = cls(target)
        widget = loader.load(f)
        f.close()
        QtCore.QMetaObject.connectSlotsByName(widget)
        return widget

#___________________________________________________________________________________________________ loadWidgetFile
    @classmethod
    def loadWidgetFile(cls, widget, names =None, loadAsWidget =True, target =None):
        """ Loads the UI file for the widget from its resource path. """

        widgetName = widget.__class__.__name__
        lookups = ListUtils.asList(names, allowTuples=False) + [widgetName, 'widget', 'main', 'gui']

        if not target:
            target = widget

        try:
            path = widget.getResourcePath(isDir=True)
        except Exception:
            raise IOError('[ERROR]: No widget resource path found for "%s" widget' % (widgetName))

        if not os.path.exists(path):
            raise IOError('[ERROR]: Missing widget resource path [%s]: %s' % (widgetName, path))

        for item in lookups:
            testPath    = widget.getResourcePath(item, isFile=True)
            uiPath      = testPath + '.ui'
            uiModTime   = os.path.getmtime(uiPath) if os.path.exists(uiPath) else 0
            pyPath      = testPath + '.py'
            pyModTime   = os.path.getmtime(uiPath) if os.path.exists(uiPath) else 0
            pycPath     = cls._getCachedPath(pyPath)
            pycModTime  = os.path.getmtime(pycPath) if os.path.exists(pycPath) else 0

            # If no files exist for the lookup item move on to the next one
            if uiModTime == 0 and pyModTime == 0 and pycModTime == 0:
                continue

            if uiModTime > pyModTime:
                result = cls.loadFileIntoTarget(target if loadAsWidget else None, uiPath)
                break

            if pyModTime >= pycModTime:
                setup = cls._importSource(pyPath)
            else:
                setup = cls._importCompiled(pycPath)

            if not setup:
                continue
            result = target if loadAsWidget else QtGui.QWidget()
            setup.PySideUiFileSetup().setupUi(result)
            break

        if not result:
            raise Exception('[ERROR]: No UI file found at: ' + path)

        if result is not target:
            layout = QtGui.QVBoxLayout()
            layout.addWidget(result)
            target.setLayout(layout)

            elements = []
            for item in dir(result):
                item = getattr(result, item)
                if isinstance(item, QtGui.QWidget):
                    elements.append(item)
        else:
            layout   = target.layout()
            elements = None

        return {'widget':result, 'layout':layout, 'elements':elements}

#___________________________________________________________________________________________________ _getCachedPath
    @classmethod
    def _getCachedPath(cls, sourcePath):
        """_getCachedPath doc..."""
        if sys.version < '3':
            return sourcePath + 'c'
        return importlib.util.cache_from_source(sourcePath)

#___________________________________________________________________________________________________ _importSource
    # noinspection PyDeprecation
    @classmethod
    def _importSource(cls, widgetPath):
        """_importSource doc..."""
        if imp:
            pycPath = widgetPath
            return imp.load_source('PySideUiFileSetup', widgetPath)

        loader = importlib.machinery.SourceFileLoader('PySideUiFileSetup', widgetPath)
        return loader.load_module()

#___________________________________________________________________________________________________ _importCompiled
    # noinspection PyDeprecation
    @classmethod
    def _importCompiled(cls, widgetPath):
        """_importCompiled doc..."""
        if imp:
            return imp.load_compiled('PySideUiFileSetup', widgetPath)

        loader = importlib.machinery.SourcelessFileLoader('PySideUiFileSetup', widgetPath)
        return loader.load_module()

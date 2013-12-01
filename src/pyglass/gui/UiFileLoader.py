# UiFileLoader.py
# (C)2012-2013
# Scott Ernst

import os
import imp

from PySide import QtCore
from PySide import QtGui
from PySide.QtUiTools import QUiLoader

#___________________________________________________________________________________________________ UiFileLoader
class UiFileLoader(QUiLoader):

#===================================================================================================
#                                                                                       C L A S S

    _WIDGET_EXTENSIONS = ['.ui', '.py', '.pyc']

#___________________________________________________________________________________________________
    def __init__(self, target):
        QUiLoader.__init__(self)
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
            widget = QUiLoader.createWidget(self, class_name, parent, name)

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
        lookups = names if names and names[0] \
            else [widget.__class__.__name__, 'widget', 'main', 'gui']

        if not target:
            target = widget

        widgetPath     = None
        widgetModified = 0
        for item in lookups:
            w = widget.getResourcePath(item, isFile=True)
            for ext in UiFileLoader._WIDGET_EXTENSIONS:
                if not os.path.exists(w + ext):
                    continue

                modTime = os.path.getmtime(w + ext)
                if modTime >= widgetModified:
                    widgetPath     = w + ext
                    widgetModified = modTime
            if widgetPath:
                break

        if widgetPath is None:
            try:
                path = widget.getResourcePath()
            except Exception, err:
                raise Exception, 'ERROR: No widget resource path found for "%s" widget' % (
                    widget.__class__.__name__)

            if not os.path.exists(path):
                raise Exception, 'ERROR: Missing widget resource path [%s]: %s' % (
                    widget.__class__.__name__, path)

            widgetModified = 0
            for item in os.listdir(widget.getResourcePath()):
                if ('.' + item.rsplit('.', 1)[-1]) not in UiFileLoader._WIDGET_EXTENSIONS:
                    continue

                item    = widget.getResourcePath(item, isFile=True)
                modTime = os.path.getmtime(item)
                if modTime >= widgetModified:
                    widgetModified = modTime
                    widgetPath     = item
                if widgetPath:
                    break

        if widgetPath is None:
            raise Exception, 'Error: No UI file found at: ' + widget.getResourcePath()

        if widgetPath.endswith('.ui'):
            result = cls.loadFileIntoTarget(
                target if loadAsWidget else None,
                widgetPath)
        else:
            if widgetPath.endswith('.py'):
                setup = imp.load_source('PySideUiFileSetup', widgetPath).PySideUiFileSetup()
            else:
                setup = imp.load_compiled('PySideUiFileSetup', widgetPath).PySideUiFileSetup()
            result = target if loadAsWidget else QtGui.QWidget()
            setup.setupUi(result)

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

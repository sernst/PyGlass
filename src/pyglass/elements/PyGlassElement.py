# PyGlassElement.py
# (C)2012-2013
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils
from pyaid.file.FileUtils import FileUtils

from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils

#___________________________________________________________________________________________________ PyGlassElement
class PyGlassElement(QtGui.QWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PySideGuiWidget."""
        QtGui.QWidget.__init__(self, parent)
        self._mainWindow = None
        self._id         = ArgsUtils.get('id', self.__class__.__name__, kwargs)
        self._widgetID   = ArgsUtils.get('widgetID', None, kwargs)
        self._resourceFolderParts = PyGlassGuiUtils.getResourceFolderParts(self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: allowsOwnership
    @property
    def allowsOwnership(self):
        return False

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        if self._mainWindow is None:
            self._mainWindow = PyGlassGuiUtils.getMainWindow(self)
        return self._mainWindow

#___________________________________________________________________________________________________ GS: dialogWindow
    @property
    def dialogWindow(self):
        """ Returns the dialog window ancestor parent that owns this widget, or None if the widget
            is not inside a dialog window.
        """

        out = self.parent()
        while out:
            if hasattr(out, 'isDialogWindow') and out.isDialogWindow:
                return out
            out = out.parent()

        return None

#___________________________________________________________________________________________________ GS: owner
    @property
    def owner(self):
        return PyGlassGuiUtils.getOwner(self)

#___________________________________________________________________________________________________ GS: appConfig
    @property
    def appConfig(self):
        return self.mainWindow.appConfig

#___________________________________________________________________________________________________ GS: commonAppConfig
    @property
    def commonAppConfig(self):
        return self.mainWindow.commonAppConfig

#___________________________________________________________________________________________________ GS: log
    @property
    def log(self):
        return self.mainWindow.log

#___________________________________________________________________________________________________ GS: id
    @property
    def id(self):
        return self._id

#___________________________________________________________________________________________________ GS: widgetID
    @property
    def widgetID(self):
        return self._widgetID

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ refreshGui
    def refreshGui(self):
        self.mainWindow.refreshGui()

#___________________________________________________________________________________________________ getSharedResourcePath
    def getSharedResourcePath(self, *args, **kwargs):
        return FileUtils.createPath(self.mainWindow.sharedResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getLocalSharedResourcePath
    def getLocalSharedResourcePath(self, *args, **kwargs):
        return FileUtils.createPath(self.mainWindow.localSharedResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getAppResourcePath
    def getAppResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(self.mainWindow.appResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getLocalAppResourcePath
    def getLocalAppResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(self.mainWindow.localAppResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getResourcePath
    def getResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            self.mainWindow.rootResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs
        )

#___________________________________________________________________________________________________ getLocalResourcePath
    def getLocalResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            self.mainWindow.rootLocalResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs
        )

#___________________________________________________________________________________________________ refreshWidgetDisplay
    def refreshWidgetDisplay(self):
        self._refreshWidgetDisplayImpl()

#___________________________________________________________________________________________________ activateWidgetDisplay
    def activateWidgetDisplay(self, **kwargs):
        self._activateWidgetDisplayImpl(**kwargs)

#___________________________________________________________________________________________________ deactivateWidgetDisplay
    def deactivateWidgetDisplay(self, **kwargs):
        self._deactivateWidgetDisplayImpl(**kwargs)

#___________________________________________________________________________________________________ getOwnerOf
    def getOwnerOf(self, target):
        return PyGlassGuiUtils.getOwner(target)

#___________________________________________________________________________________________________ getMainWindowOf
    def getMainWindowOf(self, target):
        return PyGlassGuiUtils.getMainWindow(target)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createWidget
    def _createWidget(self, parent, layoutClass =None, add =False):
        w = QtGui.QWidget(parent)

        if add and parent:
            layout = parent.layout()
            if layout:
                layout.addWidget(w)

        if layoutClass:
            return w, self._getLayout(w, layoutClass)
        return w

#___________________________________________________________________________________________________ _getLayout
    def _getLayout(self, targetWidget, layoutClass =None, force =False, cleanupForceRemoval =True):
        layout = targetWidget.layout()
        if layout and (layoutClass is None or isinstance(layout, layoutClass)):
            return layout

        if layout and force:
            layout.setParent(None)
            layout.deleteLater()
            for child in targetWidget.children():
                child.setParent(None)
                if cleanupForceRemoval:
                    child.deleteLater()
        elif layout:
            print 'WARNING: Invalid layout change attempt:', targetWidget, layoutClass, layout
            return layout

        if not layoutClass:
            layoutClass = QtGui.QVBoxLayout
        layout = layoutClass(targetWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        targetWidget.setLayout(layout)
        return layout

#___________________________________________________________________________________________________ _refreshWidgetDisplayImpl
    def _refreshWidgetDisplayImpl(self):
        pass

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _deactivateWidgetDisplayImpl
    def _deactivateWidgetDisplayImpl(self, **kwargs):
        pass

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

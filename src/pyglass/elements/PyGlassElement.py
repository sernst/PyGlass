# PyGlassElement.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui
from pyaid.file.FileUtils import FileUtils

from pyglass.elements.VisibilityElement import VisibilityElement
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.overlay.OverlayManager import OverlayManager

#___________________________________________________________________________________________________ PyGlassElement
class PyGlassElement(VisibilityElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PySideGuiWidget."""
        super(PyGlassElement, self).__init__(parent=parent, **kwargs)
        self._overlayManager      = None
        self._initialized         = False
        self._mainWindow          = None
        self._isWidgetActive      = False
        self._id                  = kwargs.get('id', self.__class__.__name__)
        self._widgetID            = kwargs.get('widgetID', self._id)
        self._userData            = kwargs.get('userData', None)
        self._resourceFolderParts = PyGlassGuiUtils.getResourceFolderParts(self)
        self._isPainting          = False

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: overlayManager
    @property
    def overlayManager(self):
        return self._overlayManager

#___________________________________________________________________________________________________ GS: allowOverlays
    @property
    def allowOverlays(self):
        return self._overlayManager is not None
    @allowOverlays.setter
    def allowOverlays(self, value):
        if self.allowOverlays == value:
            return

        if value:
            self._overlayManager = OverlayManager(self)
        else:
            self._overlayManager.dispose()
            self._overlayManager = None
        self.updateGeometry()
        self.update()

#___________________________________________________________________________________________________ GS: isOnDisplay
    @property
    def isOnDisplay(self):
        if not self.isVisible():
            return False

        parent = self.parent()
        while parent:
            try:
                if not parent.isVisible():
                    return False
                if parent.isBackgroundParent:
                    return False
            except Exception:
                pass
            parent = parent.parent()

        return True

#___________________________________________________________________________________________________ GS: userData
    @property
    def userData(self):
        return self._userData
    @userData.setter
    def userData(self, value):
        self._userData = value

#___________________________________________________________________________________________________ GS: allowsOwnership
    @property
    def allowsOwnership(self):
        return False

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        """
        :rtype: PyGlassWindow
        """

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
    @id.setter
    def id(self, value):
        self._id = value

#___________________________________________________________________________________________________ GS: widgetID
    @property
    def widgetID(self):
        return self._widgetID
    @widgetID.setter
    def widgetID(self, value):
        self._widgetID = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ resizeEvent
    def resizeEvent(self, *args, **kwargs):
        if not self._initialized:
            self._initialize()
            self._initialized = True
        self._resizeImpl(*args, **kwargs)

        if self._overlayManager:
            self._overlayManager.resize()

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
        if not self._isPainting:
            self._isPainting = True
            self._paintImpl(*args, **kwargs)
            self._isPainting = False

#___________________________________________________________________________________________________ getAncestor
    def getAncestor(self, ident):
        parent = self.parent()
        while parent:
            if hasattr(parent, 'id') and parent.id == ident:
                return parent
            parent = parent.parent()
        return None

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
        inApp = kwargs.get('inApp', False)
        if inApp:
            return self.getAppResourcePath('widget', self._resourceFolderParts, *args, **kwargs)
        return FileUtils.createPath(
            self.mainWindow.rootResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs )

#___________________________________________________________________________________________________ getLocalResourcePath
    def getLocalResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            self.mainWindow.rootLocalResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs )

#___________________________________________________________________________________________________ refreshWidgetDisplay
    def refreshWidgetDisplay(self):
        self._refreshWidgetDisplayImpl()

#___________________________________________________________________________________________________ activateWidgetDisplay
    def activateWidgetDisplay(self, **kwargs):
        if self._isWidgetActive:
            return
        self._activateWidgetDisplayImpl(**kwargs)
        self._isWidgetActive = True
        self.updateGeometry()
        self.update()

#___________________________________________________________________________________________________ deactivateWidgetDisplay
    def deactivateWidgetDisplay(self, **kwargs):
        if not self._isWidgetActive:
            return
        self._deactivateWidgetDisplayImpl(**kwargs)
        self._isWidgetActive = False

#___________________________________________________________________________________________________ getOwnerOf
    # noinspection PyMethodMayBeStatic
    def getOwnerOf(self, target):
        return PyGlassGuiUtils.getOwner(target)

#___________________________________________________________________________________________________ getMainWindowOf
    def getMainWindowOf(self, target):
        return PyGlassGuiUtils.getMainWindow(target)

#___________________________________________________________________________________________________ clearLayout
    @classmethod
    def clearLayout(cls, layout, unparent =True, deleteLater =False):
        if layout is None:
            return []

        out = []
        item = layout.takeAt(0)
        while item:
            w = item.widget()
            if w:
                out.append(w)
                if unparent:
                    w.setParent(None)
            del item
            item = layout.takeAt(0)

        if deleteLater:
            for item in out:
                try:
                    item.deleteLater()
                except Exception:
                    print('[WARNING]: Delete later failure %s -> %s' % (cls.__name__, item))
            return []
        return out

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initialize
    def _initialize(self):
        pass

#___________________________________________________________________________________________________ resizeEvent
    def _resizeImpl(self, event):
        pass

#___________________________________________________________________________________________________ _paintImpl
    def _paintImpl(self, event):
        pass

#___________________________________________________________________________________________________ _createElementWidget
    def _createElementWidget(self, parent, layoutClass =None, add =False):
        return self._createWidget(parent, layoutClass, add, PyGlassElement)

#___________________________________________________________________________________________________ _createWidget
    def _createWidget(self, parent, layoutClass =None, add =False, widgetClass =None):
        if widgetClass is None:
            widgetClass = QtGui.QWidget
        w = widgetClass(parent)

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
            print('[WARNING]: Invalid layout change attempt on %s in %s with %s -> %s' % (
                targetWidget, self, layoutClass, layout))
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

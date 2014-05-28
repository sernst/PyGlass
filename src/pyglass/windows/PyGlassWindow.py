# PyGlassWindow.py
# (C)2012-2013
# Scott Ernst

import sys
import os

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.decorators.ClassGetter import ClassGetter
from pyaid.file.FileUtils import FileUtils

from pyglass.alembic.AlembicUtils import AlembicUtils
from pyglass.app.ApplicationConfig import ApplicationConfig
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.gui.PyGlassBackgroundParent import PyGlassBackgroundParent
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.gui.UiFileLoader import UiFileLoader
from pyglass.widgets.LoadingWidget import LoadingWidget

#___________________________________________________________________________________________________ PyGlassWindow
class PyGlassWindow(QtGui.QMainWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of PyGlassWindow."""
        parent = ArgsUtils.extract('parent', None, kwargs)
        self._application  = ArgsUtils.extract('pyGlassApp', None, kwargs)
        self._qApplication = ArgsUtils.extract('qApp', None, kwargs)
        self._isMainWindow = ArgsUtils.extract('isMainWindow', bool(parent is None), kwargs)
        self._mainWindow   = ArgsUtils.extract('mainWindow', None, kwargs)
        self._centerWidget = None
        self._hasShown     = False

        self._keyboardCallback = ArgsUtils.extract('keyboardCallback', None, kwargs)

        if not self._mainWindow:
            if self._isMainWindow:
                self._mainWindow = self
            elif self._application:
                self._mainWindow = self._application.mainWindow

        self._dependentWindows = []
        self._currentWidget    = None

        QtGui.QMainWindow.__init__(self, parent, ArgsUtils.extract('flags', 0, kwargs))

        if self._keyboardCallback is not None:
            self.setFocusPolicy(QtCore.Qt.StrongFocus)

        if self._isMainWindow:
            self._log                 = Logger(self, printOut=True)
            self._config              = ApplicationConfig(self)
            self._commonConfig        = ApplicationConfig(self, common=True)
            self._resourceFolderParts = PyGlassGuiUtils.getResourceFolderParts(self)

            icon = PyGlassGuiUtils.createIcon(
                ArgsUtils.get('iconsPath', self.getAppResourcePath('icons', isDir=True), kwargs) )
            if icon:
                self.setWindowIcon(icon)

        elif self._mainWindow:
            icon = self._mainWindow.windowIcon()
            if icon:
                self.setWindowIcon(icon)

        # Loads the ui file if it exists
        hasWindowFile = ArgsUtils.get('mainWindowFile', False, kwargs)
        if hasWindowFile:
            if not self._centerWidget:
                self._createCentralWidget()
            UiFileLoader.loadWidgetFile(self, target=self._centerWidget)

        self._styleSheet = ArgsUtils.get('styleSheet', None, kwargs)
        if self._styleSheet:
            self.setStyleSheet(self.styleSheetPath)

        # Sets a non-standard central widget
        centralWidgetName = ArgsUtils.get('centralWidgetName', None, kwargs)
        if centralWidgetName and hasattr(self, centralWidgetName):
            self._centerWidget = getattr(self, centralWidgetName)
        elif not hasWindowFile:
            self._centerWidget = None
            if ArgsUtils.get('defaultCenterWidget', False, kwargs):
                self._createCentralWidget()

        self._lastWidgetID  = None
        self._widgetParent  = None
        self._widgets       = None
        self._widgetFlags   = None

        self._widgetClasses = ArgsUtils.get('widgets', None, kwargs)
        if self._widgetClasses:
            self._initializeWidgetChildren()
        else:
            self._widgetClasses = dict()

        self.setWindowTitle(ArgsUtils.get('title', self._createTitleFromClass(), kwargs))
        self.updateStatusBar()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isDeployed
    @ClassGetter
    def isDeployed(cls):
        return PyGlassEnvironment.isDeployed

#___________________________________________________________________________________________________ GS: isOnDisplay
    @property
    def isOnDisplay(self):
        return self.isVisible()

#___________________________________________________________________________________________________ GS: appID
    @property
    def appID(self):
        return self.pyGlassApplication.appID

#___________________________________________________________________________________________________ GS: isMainWindow
    @property
    def isMainWindow(self):
        return self._isMainWindow

#___________________________________________________________________________________________________ GS: allowsOwnership
    @property
    def allowsOwnership(self):
        return True

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        if self.isMainWindow:
            return self
        if self._mainWindow:
            return self._mainWindow

        self._mainWindow = PyGlassGuiUtils.getMainWindow(self)

        # Handle case where main window turns out to this window
        if self._mainWindow == self:
            self._isMainWindow = True
            self._mainWindow = None
            return self

        return self._mainWindow

#___________________________________________________________________________________________________ GS: owner
    @property
    def owner(self):
        if self.isMainWindow:
            return self
        return self.mainWindow

#___________________________________________________________________________________________________ GS: pyGlassApplication
    @property
    def pyGlassApplication(self):
        return self._application if self.isMainWindow else self.mainWindow.pyGlassApplication

#___________________________________________________________________________________________________ GS: qApplication
    @property
    def qApplication(self):
        if self._qApplication is not None:
            return self._qApplication

        return self._qApplication if self.isMainWindow else self.mainWindow.qApplication

#___________________________________________________________________________________________________ GS: appConfig
    @property
    def appConfig(self):
        return self._config if self.isMainWindow else self.mainWindow.appConfig

#___________________________________________________________________________________________________ GS: commonAppConfig
    @property
    def commonAppConfig(self):
        return self._commonConfig if self.isMainWindow else self.mainWindow.commonAppConfig

#___________________________________________________________________________________________________ GS: log
    @property
    def log(self):
        return self._log if self.isMainWindow else self.owner.log

#___________________________________________________________________________________________________ GS: styleSheetPath
    @property
    def styleSheetPath(self):
        if not self._styleSheet:
            return None

        if os.path.isabs(self._styleSheet):
            return self._styleSheet

        parts = self._resourceFolderParts + self._stylesheet.split('/')
        return self.getResourcePath(*parts, isFile=True)

#___________________________________________________________________________________________________ GS: rootResourcePath
    @property
    def rootResourcePath(self):
        return PyGlassEnvironment.getRootResourcePath()

#___________________________________________________________________________________________________ GS: rootLocalResourcePath
    @property
    def rootLocalResourcePath(self):
        return PyGlassEnvironment.getRootLocalResourcePath()

#___________________________________________________________________________________________________ GS: appResourcePath
    @property
    def appResourcePath(self):
        if not self.isMainWindow:
            return self.owner.appResourcePath

        out = self.getRootResourcePath('apps', self.appID, isDir=True)
        if not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ GS: localAppResourcePath
    @property
    def localAppResourcePath(self):
        if not self.isMainWindow:
            return self.owner.localAppResourcePath

        out = self.getRootLocalResourcePath('apps', self.appID, isDir=True)
        if not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ GS: sharedResourcePath
    @property
    def sharedResourcePath(self):
        out = self.getRootResourcePath('shared', isDir=True)
        if not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ GS: localSharedResourcePath
    @property
    def localSharedResourcePath(self):
        out = self.getLocalResourcePath('shared', isDir=True)
        if not os.path.exists(out):
            os.makedirs(out)
        return out

#___________________________________________________________________________________________________ GS: widgets
    @property
    def widgets(self):
        return self._widgets

#___________________________________________________________________________________________________ GS: screenWidth
    @property
    def screenWidth(self):
        rect = self._qApplication.desktop().screenGeometry()
        return rect.width()

#___________________________________________________________________________________________________ GS: screenHeight
    @property
    def screenHeight(self):
        rect = self._qApplication.desktop().screenGeometry()
        return rect.height()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ keyPressEvent
    def keyPressEvent(self, event):
        if self._keyboardCallback is None or not self._keyboardCallback(event):
            super(PyGlassWindow, self).keyPressEvent(event)

#___________________________________________________________________________________________________ showEvent
    def showEvent(self, *args, **kwargs):
        if not self._hasShown:
            self._firstShowImpl()
            self._hasShown = True

#___________________________________________________________________________________________________ closeEvent
    def closeEvent(self, *args, **kwargs):
        if self.isMainWindow:
            for depWindow in self._dependentWindows:
                depWindow.close()
        return super(PyGlassWindow, self).closeEvent(*args, **kwargs)

#___________________________________________________________________________________________________ addDependentWindow
    def addDependentWindow(self, window):
        if window in self._dependentWindows:
            return True

        self._dependentWindows.append(window)
        return True

#___________________________________________________________________________________________________ removeDependentWindow
    def removeDependentWindow(self, window):
        if window not in self._dependentWindows:
            return True

        self._dependentWindows.remove(window)
        return True

#___________________________________________________________________________________________________ refreshWidgets
    def refreshWidgets(self, **kwargs):
        for name, widget in self._widgets.iteritems():
            widget.refresh(**kwargs)
        self.refreshGui()

#___________________________________________________________________________________________________ updateStatusBar
    def updateStatusBar(self, message =None, timeout =-1):
        if not message:
            self.statusBar().clearMessage()
            self.statusBar().setVisible(False)
        else:
            if timeout < 0:
                timeout = 3000
            self.statusBar().showMessage(message, timeout=timeout)
            self.statusBar().setVisible(True)

#___________________________________________________________________________________________________ getWidgetFromID
    def getWidgetFromID(self, widgetID):
        if widgetID in self._widgets:
            return self._widgets[widgetID]
        return None

#___________________________________________________________________________________________________ getSharedResourcePath
    def getSharedResourcePath(self, *args, **kwargs):
        return FileUtils.createPath(self.sharedResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getLocalSharedResourcePath
    def getLocalSharedResourcePath(self, *args, **kwargs):
        return FileUtils.createPath(self.localSharedResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getAppResourcePath
    def getAppResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(self.appResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getLocalAppResourcePath
    def getLocalAppResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(self.localAppResourcePath, *args, **kwargs)

#___________________________________________________________________________________________________ getRootResourcePath
    def getRootResourcePath(self, *args, **kwargs):
        return PyGlassEnvironment.getRootResourcePath(*args, **kwargs)

#___________________________________________________________________________________________________ getRootLocalResourcePath
    def getRootLocalResourcePath(self, *args, **kwargs):
        return PyGlassEnvironment.getRootLocalResourcePath(*args, **kwargs)

#___________________________________________________________________________________________________ getResourcePath
    def getResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            self.rootResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs)

#___________________________________________________________________________________________________ getLocalResourcePath
    def getLocalResourcePath(self, *args, **kwargs):
        """Doc..."""
        return FileUtils.createPath(
            self.rootLocalResourcePath, 'widget', self._resourceFolderParts, *args, **kwargs)

#___________________________________________________________________________________________________ showLoading
    def showLoading(self, **kwargs):
        if self._currentWidget.widgetID != 'loading':
            self._lastWidgetID = self._currentWidget.widgetID
        self._showLoadingImpl(**kwargs)
        self.setActiveWidget('loading', force=True, args=kwargs)

#___________________________________________________________________________________________________ hideLoading
    def hideLoading(self, **kwargs):
        if self._currentWidget.widgetID != 'loading':
            return

        self._hideLoadingImpl(**kwargs)
        if self._lastWidgetID:
            self.setActiveWidget(self._lastWidgetID, args=kwargs)

#___________________________________________________________________________________________________ addWidget
    def addWidget(self, key, widgetClass, setActive =False):
        self._widgetClasses[key] = widgetClass
        if self._widgets is None:
            self._initializeWidgetChildren(key if setActive else None)
        elif setActive:
            return self.setActiveWidget(key)
        return True

#___________________________________________________________________________________________________ setActiveWidget
    def setActiveWidget(self, widgetID, force =False, args =None, doneArgs =None):
        if not self._centerWidget or widgetID is None or widgetID not in self._widgetClasses:
            return False

        if not force and self._currentWidget and self._currentWidget.widgetID == widgetID:
            return True

        if widgetID not in self._widgets:
            self.loadWidgets(widgetID)
        widget = self._widgets[widgetID]

        # Deactivates the current widget if the widgets are being switched. However, ignored if the
        # same widget is being activated for a second time.
        if self._currentWidget and widgetID != self._currentWidget.widgetID:
            if self._currentWidget.widgetID == 'loading':
                self._hideLoadingImpl()

            if doneArgs is None:
                doneArgs = dict()
            self._currentWidget.deactivateWidgetDisplay(**doneArgs)
            self._currentWidget.setParent(self._widgetParent)

        self._currentWidget = widget
        if self._centerWidget:
            layout = self._centerWidget.layout()
            if not layout:
                layout = QtGui.QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                self._centerWidget.setLayout(layout)
            layout.addWidget(widget)
        else:
            self.setCentralWidget(widget)
        self.setContentsMargins(0, 0, 0, 0)
        self.refreshGui()

        if args is None:
            args = dict()
        widget.activateWidgetDisplay(**args)
        return True

#___________________________________________________________________________________________________ loadWidgets
    def loadWidgets(self, widgetIdents =None):
        if not widgetIdents:
            widgetIdents = self._widgetClasses.keys()
        elif isinstance(widgetIdents, basestring):
            widgetIdents = [widgetIdents]

        for widgetID in widgetIdents:
            if widgetID in self._widgets:
                continue

            if widgetID not in self._widgetClasses:
                self._log.write(
                    'ERROR: Unrecognized widgetID "%s" in %s' % (str(widgetID), str(self)))

            widget = self._widgetClasses[widgetID](
                self._widgetParent, flags=self._widgetFlags, widgetID=widgetID)
            self._widgets[widgetID] = widget

#___________________________________________________________________________________________________ refreshGui
    def refreshGui(self):
        self.qApplication.processEvents()

#___________________________________________________________________________________________________ exit
    def exit(self):
        self.qApplication.exit()

#___________________________________________________________________________________________________ initialize
    def initialize(self, *args, **kwargs):
        if AlembicUtils.hasAlembic:
            self.pyGlassApplication.updateSplashScreen('Conforming internal data')
            AlembicUtils.upgradeAppDatabases(self.appID)

        self._initializeImpl(*args, **kwargs)

#___________________________________________________________________________________________________ initializeComplete
    def initializeComplete(self, preDisplay =None):
        self.pyGlassApplication.closeSplashScreen()

        result = False
        if preDisplay:
            preDisplay.show()
            result = self.qApplication.exec_()

        if not result:
            self.preShow()
            self.show()
            result = self.qApplication.exec_()
            self.postShow()

        sys.exit(result)

#___________________________________________________________________________________________________ preShow
    def preShow(self, **kwargs):
        self._preShowImpl(**kwargs)

#___________________________________________________________________________________________________ postShow
    def postShow(self, **kwargs):
        self._postShowImpl(**kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createCentralWidget
    def _createCentralWidget(self):
        w1 = self.centralWidget()
        w2 = self._centerWidget
        if w1 and w2:
            return w2
        elif w1 and not w2:
            self._centerWidget = w1
            return w1

        layout = self.layout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        w = QtGui.QWidget(self)
        layout.addWidget(w)
        self.setCentralWidget(w)
        self._centerWidget = w
        return w

#___________________________________________________________________________________________________ _initializeWidgetChildren
    def _initializeWidgetChildren(self, activeWidgetID =None):
        if not self._widgetClasses or self._widgets:
            return False

        self._widgetParent = PyGlassBackgroundParent(proxy=self)
        self._widgets      = dict()

        if 'loading' not in self._widgetClasses:
            self._widgetClasses['loading'] = LoadingWidget

        if activeWidgetID:
            self.setActiveWidget(activeWidgetID)

#___________________________________________________________________________________________________ _preShowImpl
    def _preShowImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _firstShowImpl
    def _firstShowImpl(self):
        pass

#___________________________________________________________________________________________________ _postShowImpl
    def _postShowImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _showLoadingImpl
    def _showLoadingImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _hideLoadingImpl
    def _hideLoadingImpl(self, **kwargs):
        pass

#___________________________________________________________________________________________________ _createTitleFromClass
    def _createTitleFromClass(self):
        """Doc..."""
        src = self.__class__.__name__
        out = src[0]
        wasCaps = True
        for c in src[1:]:
            if c.lower() == c:
                out += c
                wasCaps = False
            elif wasCaps:
                out += c
            else:
                out += ' ' + c
                wasCaps = True

        return out

#___________________________________________________________________________________________________ _initializeImpl
    def _initializeImpl(self, *args, **kwargs):
        self.initializeComplete()

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

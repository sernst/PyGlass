# PyGlassApplication.py
# Vizme, Inc. (C)2013
# Scott Ernst

import sys
import os
import inspect

from PySide import QtCore
from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ PyGlassApplication
class PyGlassApplication(QtCore.QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of PyGlassApplication."""
        QtCore.QObject.__init__(self)
        self._qApplication = None
        self._window       = None
        self._splashScreen = None

        # Sets a temporary standard out and error for deployed applications in a write allowed
        # location to prevent failed write results.
        if PyGlassEnvironment.isDeployed and PyGlassEnvironment.isWindows:
            sys.stdout = open(
                FileUtils.createPath(
                    os.environ['LOCALAPPDATA'], self.appID + '_out.log', isFile=True
                ), 'w'
            )

            sys.stderr = open(
                FileUtils.createPath(
                    os.environ['LOCALAPPDATA'], self.appID + '_error.log', isFile=True
                ), 'w'
            )

        PyGlassEnvironment.initializeAppSettings(self)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: applicationCodePath
    @property
    def applicationCodePath(self):
        """ Determines the application code path where this file is located. the abspath enforces
            the absolute path with the correct os.sep to prevent issues with file path format in
            resources.
        """
        return os.path.abspath(os.path.dirname(inspect.getfile(self.__class__)))

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return None

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return self.__class__.__name__

#___________________________________________________________________________________________________ GS: appID
    @property
    def appID(self):
        return self.__class__.__name__

#___________________________________________________________________________________________________ GS: splashScreenUrl
    @property
    def splashScreenUrl(self):
        return None

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        return None

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        return self._window

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ updateSplashScreen
    def updateSplashScreen(self, message =None):
        if not self._splashScreen:
            return False

        self._splashScreen.showMessage(
            message if message else 'Loading...', alignment=QtCore.Qt.AlignBottom
        )
        self._qApplication.processEvents()
        return True

#___________________________________________________________________________________________________ closeSplashScreen
    def closeSplashScreen(self):
        if not self._splashScreen:
            return False

        self._splashScreen.finish(self._window)
        self._splashScreen = None
        return True

#___________________________________________________________________________________________________ run
    def run(self, appArgs =None, **kwargs):
        """Doc..."""
        try:
            if PyGlassEnvironment.isDeployed:
                logPath = PyGlassEnvironment.getRootLocalResourcePath('logs', isDir=True)
                if not os.path.exists(logPath):
                    os.makedirs(logPath)

                try:
                    sys.stdout.close()
                except Exception, err:
                    pass
                sys.stdout = open(logPath + 'out.log', 'w')

                try:
                    sys.stderr.close()
                except Exception, err:
                    pass
                sys.stderr = open(logPath + 'error.log', 'w')
        except Exception, err:
            raise

        self._qApplication = QtGui.QApplication(appArgs if appArgs else [])
        if self.splashScreenUrl:
            parts = str(self.splashScreenUrl).split(':', 1)
            if len(parts) == 1 or parts[0].lower == 'app':
                splashImagePath = PyGlassEnvironment.getRootResourcePath(
                    'apps', self.appID, parts[-1], isFile=True
                )
            else:
                splashImagePath = None

            if splashImagePath and os.path.exists(splashImagePath):
                splash = QtGui.QSplashScreen(QtGui.QPixmap(splashImagePath))
                splash.show()
                self._splashScreen = splash
                self.updateSplashScreen('Initializing User Interface')

        windowClass = self.mainWindowClass
        assert inspect.isclass(windowClass)

        self._window = windowClass(
            parent=None,
            qApp=self._qApplication,
            pyGlassApp=self,
            isMainWindow=True,
            **kwargs
        )
        self._window.initialize()
        self._qApplication.processEvents()

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

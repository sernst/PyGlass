# PyGlassApplication.py
# (C)2013-2014
# Scott Ernst

import sys
import os
import inspect

try:
    import appdirs
except Exception, err:
    appdirs = None

import PySide
from PySide import QtCore
from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ PyGlassApplication
class PyGlassApplication(QtCore.QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _MIN_PYSIDE_VERSION = u'1.2.2'
    _LOCATION_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of PyGlassApplication."""
        QtCore.QObject.__init__(self)
        self._qApplication = None
        self._window       = None
        self._splashScreen = None

        # Checks the version of the PySide library being used. If the version is out-of-date,
        # raise a runtime error.
        minVersion = self._MIN_PYSIDE_VERSION.split(u'.')
        version = PySide.__version__.split('.')
        if int(version[0]) < int(minVersion[0]):
            if int(version[1]) < int(minVersion[1]):
                if int(version[2]) < minVersion[2]:
                    raise RuntimeError, (
                        u'[ERROR]: The installed PySide version of %s is below PyGlass\''
                        + u' minimum required version of %s.%s.%s. Please update the library.') % (
                        version, minVersion[0], minVersion[1], minVersion[2])

        # Sets a temporary standard out and error for deployed applications in a write allowed
        # location to prevent failed write results.
        if PyGlassEnvironment.isDeployed:
            if appdirs:
                userDir = appdirs.user_data_dir(self.appID, self.appGroupID)
            else:
                userDir = FileUtils.createPath(
                    os.path.expanduser('~'), '.pyglass', self.appGroupID, self.appID, isDir=True)

            path = FileUtils.createPath(
                userDir,
                self.appID + '_out.log', isFile=True)
            FileUtils.getDirectoryOf(path, createIfMissing=True)
            sys.stdout = open(path, 'w+')

            FileUtils.createPath(
                appdirs.user_data_dir(self.appID, self.appGroupID),
                self.appID + '_error.log',
                isFile=True)
            FileUtils.getDirectoryOf(path, createIfMissing=True)
            sys.stderr = open(path, 'w+')

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
            message if message else 'Loading...', alignment=QtCore.Qt.AlignBottom)
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

        # Test for compatible Qt version installation and raise an error if an unsupported version
        # is being used
        qtVersion = QtCore.__version_info__
        if qtVersion[0] < 4 or qtVersion[1] < 8:
            raise Exception, 'ERROR: Unsupported Qt Version "%s"' % QtCore.__version__

        qApp = QtGui.QApplication(appArgs if appArgs else [])
        self._qApplication = qApp

        ### FUTURE ### self._qApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

        if self.splashScreenUrl:
            parts = str(self.splashScreenUrl).split(':', 1)
            if len(parts) == 1 or parts[0].lower == 'app':
                splashImagePath = PyGlassEnvironment.getRootResourcePath(
                    'apps', self.appID, parts[-1], isFile=True)
            else:
                splashImagePath = None

            if splashImagePath and os.path.exists(splashImagePath):
                splash = QtGui.QSplashScreen(QtGui.QPixmap(splashImagePath))
                splash.show()
                self._splashScreen = splash
                self.updateSplashScreen('Initializing User Interface')

        self._runPreMainWindowImpl()

        windowClass = self.mainWindowClass
        if windowClass is None:
            raise RuntimeError, u'No Main Window Class was specified in your application class.'

        assert inspect.isclass(windowClass), (
            u'%s.mainWindowClass getter must return a class for your main window' %
            self.__class__.__name__)

        self._window = windowClass(
            parent=None,
            qApp=self._qApplication,
            pyGlassApp=self,
            isMainWindow=True,
            **kwargs)
        self._window.initialize()

        self._qApplication.aboutToQuit.connect(self._onApplicationExit)
        self._intializeComplete()
        self._qApplication.processEvents()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runPreMainWindowImpl
    def _runPreMainWindowImpl(self):
        pass

#___________________________________________________________________________________________________ _intializeComplete
    def _intializeComplete(self):
        pass

#___________________________________________________________________________________________________ _onApplicationExit
    def _onApplicationExit(self):
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

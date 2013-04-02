# PyGlassWebView.py
# (C)2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit

from pyaid.ArgsUtils import ArgsUtils

from pyglass.gui.web.PyGlassWebPage import PyGlassWebPage
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils

#___________________________________________________________________________________________________ PyGlassWebView
class PyGlassWebView(QtWebKit.QWebView):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, communicator =None, debug =False, **kwargs):
        """Creates a new instance of PyGlassWebView."""
        QtWebKit.QWebView.__init__(self, parent)
        self._debug      = debug
        self._mainWindow = None
        self._comm       = communicator
        if self._comm:
            self._comm.webView = self

        self._webPage = PyGlassWebPage(self, view=self)
        self.setPage(self._webPage)
        settings = self._webPage.settings()
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessFileUrls, True)

        self._transparent = ArgsUtils.get('transparent', True, kwargs)
        if self._transparent:
            p = self.palette()
            p.setBrush(QtGui.QPalette.Base, QtCore.Qt.transparent)
            self.setPalette(p)
            self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)

        if self._debug:
            self._webInspector = QtWebKit.QWebInspector()
            self._webInspector.setPage(self._webPage)

            settings.setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
            shortcut = QtGui.QShortcut(self)
            shortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_F12))
            shortcut.activated.connect(self._handleToggleInspector)
            self._webInspector.setVisible(False)

        self.loadFinished.connect(self._handleLoadFinished)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ GS: pluginsEnabled
    @property
    def pluginsEnabled(self):
        return self.settings().attribute(QtWebKit.QWebSettings.PluginsEnabled)
    @pluginsEnabled.setter
    def pluginsEnabled(self, value):
        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, value)

#___________________________________________________________________________________________________ GS: communicator
    @property
    def communicator(self):
        return self._comm
    @communicator.setter
    def communicator(self, value):
        self._comm = value

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

#___________________________________________________________________________________________________ GS: owner
    @property
    def owner(self):
        return PyGlassGuiUtils.getOwner(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ openUrl
    def openUrl(self, url):
        """Doc..."""
        self.setUrl(QtCore.QUrl(url))

#___________________________________________________________________________________________________ openLocalWebUrl
    def openLocalWebUrl(self, url):
        """Doc..."""
        if isinstance(url, basestring):
            url = url.split(u'/')

        url = self.mainWindow.getRootResourcePath('web', *url)
        self.load(QtCore.QUrl('file:///' + url))

#___________________________________________________________________________________________________ contextMenuEvent
    def contextMenuEvent(self, *args, **kwargs):
        if self._debug:
            return QtWebKit.QWebView.contextMenuEvent(self, *args, **kwargs)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleToggleInspector
    def _handleToggleInspector(self):
        self._webInspector.setVisible(not self._webInspector.isVisible())

#___________________________________________________________________________________________________ _handleLoadFinished
    def _handleLoadFinished(self, result):
        if not self._comm:
            return

        frame = self._webPage.mainFrame()
        self._comm.frame = frame
        frame.addToJavaScriptWindowObject(self._comm.javaScriptID, self._comm)
        frame.evaluateJavaScript(
            u'try{ window.initialize%s(); } catch (e) {}' % self._comm.javaScriptID
        )

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

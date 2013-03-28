# PyGlassWebPage.py
# (C)2013
# Scott Ernst

from PySide import QtWebKit

from pyglass.gui.web.PyGlassNetworkManager import PyGlassNetworkManager
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils

#___________________________________________________________________________________________________ PyGlassWebPage
class PyGlassWebPage(QtWebKit.QWebPage):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, view, debug =False, **kwargs):
        self._view = view
        QtWebKit.QWebPage.__init__(self, parent)
        manager = self.networkAccessManager()
        self.setNetworkAccessManager(PyGlassNetworkManager(self, manager))
        self._mainWindow = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: webView
    @property
    def webView(self):
        return self._view

#___________________________________________________________________________________________________ GS: webViewUrl
    @property
    def webViewUrl(self):
        return self._view.url()

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        if not self._mainWindow:
            self._mainWindow = PyGlassGuiUtils.getMainWindow(self)
        return self._mainWindow

#___________________________________________________________________________________________________ GS: owner
    @property
    def owner(self):
        return PyGlassGuiUtils.getOwner(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ javaScriptConsoleMessage
    def javaScriptConsoleMessage(self, msg, line, source):
        if msg == 'Empty trace item':
            return

        print 'LOG:', msg
        print '    LINE: #%d OF %s' % (line, source)

#___________________________________________________________________________________________________ javaScriptAlert
    def javaScriptAlert(self, originatingFrame, msg):
        print 'ALERT:', msg

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ handleToggleInspector
    def handleToggleInspector(self):
        self._webInspector.setVisible(not self._webInspector.isVisible())

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

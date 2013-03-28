# PyGlassNetworkManager.py
# (C)2013
# Scott Ernst

from PySide import QtNetwork

from pyglass.gui.web.ResourceCustomNetworkReply import ResourceCustomNetworkReply

#___________________________________________________________________________________________________ PyGlassNetworkManager
class PyGlassNetworkManager(QtNetwork.QNetworkAccessManager):

    SCHEMES = ['resource', 'page', 'web', 'sharedweb', 'shared', 'https', 'app']

#___________________________________________________________________________________________________ __init__
    def __init__(self, page, standardManager):
        QtNetwork.QNetworkAccessManager.__init__(self)
        self._page            = page
        self._standardManager = standardManager

        self.setCache(standardManager.cache())
        self.setCookieJar(standardManager.cookieJar())
        self.setProxy(standardManager.proxy())
        self.setProxyFactory(standardManager.proxyFactory())

#___________________________________________________________________________________________________ createRequest
    def createRequest(self, operation, request, data):
        scheme = request.url().scheme()
        if scheme not in PyGlassNetworkManager.SCHEMES:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)

        return ResourceCustomNetworkReply(self, request, operation, data, self._page)

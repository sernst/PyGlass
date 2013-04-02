# PyGlassNetworkManager.py
# (C)2013
# Scott Ernst

from PySide import QtNetwork

from pyglass.gui.web.ResourceCustomNetworkReply import ResourceCustomNetworkReply

#___________________________________________________________________________________________________ PyGlassNetworkManager
class PyGlassNetworkManager(QtNetwork.QNetworkAccessManager):

    HOSTS   = None
    DOMAIN  = 'localhost.com'
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

        if self.HOSTS is None:
            out = []
            for scheme in self.SCHEMES:
                out.append(scheme + '.' + self.DOMAIN)
            self.HOSTS = out

#___________________________________________________________________________________________________ createRequest
    def createRequest(self, operation, request, data):
        scheme = request.url().scheme()
        host   = request.url().host()
        if host in self.HOSTS or scheme in self.SCHEMES:
            return ResourceCustomNetworkReply(self, request, operation, data, self._page)

        return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)



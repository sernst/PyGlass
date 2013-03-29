# ResourceCustomNetworkReply.py
# (C)2013
# Scott Ernst

import os
import requests

from PySide import QtCore
from PySide import QtNetwork

from pyaid.enum.MimeTypeEnum import MIME_TYPES
from pyaid.file.FileUtils import FileUtils

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils

#___________________________________________________________________________________________________ ResourceCustomNetworkReply
class ResourceCustomNetworkReply(QtNetwork.QNetworkReply):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, request, operation, data, page):
        QtNetwork.QNetworkReply.__init__(self, parent)
        mainWindow = page.mainWindow
        url        = request.url()
        scheme     = url.scheme()

        self.offset = 0

        if scheme == 'https':
            self._buildHttpsReply(parent, request, url, operation, data, page)
            self._finalize(url)
            return

        path = url.path()
        if not path:
            path = [url.host()]
        else:
            path = url.path().strip().strip('/').split('/')
            path.insert(0, url.host())

        if path[-1].endswith('.js'):
            contentType = MIME_TYPES.JAVASCRIPT
        elif path[-1].endswith('.css'):
            contentType = MIME_TYPES.CSS
        elif path[-1].endswith('.png'):
            contentType = MIME_TYPES.PNG_IMAGE
        elif path[-1].endswith('.jpg'):
            contentType = MIME_TYPES.JPEG_IMAGE
        else:
            contentType = MIME_TYPES.HTML

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, contentType + '; charset=UTF8')

        if scheme == 'page':
            pagePath = page.webViewUrl.host() + '/' + page.webViewUrl.path()
            pagePath = pagePath.split('://', 1)[-1].rsplit(os.sep, 1)[0]
            if pagePath[:5].find(':') != -1:
                pagePath = pagePath.lstrip('/')
            path = FileUtils.createPath(pagePath, *path, isFile=True)
        elif scheme == 'web':
            path.insert(0, 'web')
        elif scheme == 'sharedweb':
            path = ['shared', 'web'] + path
        elif scheme == 'shared':
            path = path.insert(0, 'shared')
        elif scheme == 'app':
            path = mainWindow.getAppResourcePath(*path, isFile=True)

        if isinstance(path, list):
            path = mainWindow.getRootResourcePath(*path, isFile=True)

        if os.path.exists(path):
            if contentType in [MIME_TYPES.JPEG_IMAGE, MIME_TYPES.PNG_IMAGE]:
                f = open(path, 'rb+')
            else:
                f = open(path, 'r+')
            self.content = f.read()
            f.close()
        else:
            print 'WARNING: Resource URL does not exist ->', path
            self.content = ''

        self._finalize(url)

#___________________________________________________________________________________________________ abort
    def abort(self):
        pass

#___________________________________________________________________________________________________ bytesAvailable
    def bytesAvailable(self):
        return len(self.content) - self.offset + QtNetwork.QNetworkReply.bytesAvailable(self)

#___________________________________________________________________________________________________ isSequential
    def isSequential(self):
        return True

#___________________________________________________________________________________________________ readData
    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _finalize
    def _finalize(self, url):
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))

#___________________________________________________________________________________________________
    def _buildHttpsReply(self, parent, request, url, operation, data, page):
        headers = dict()
        for header in request.rawHeaderList():
            headers[unicode(header)] = unicode(request.rawHeader(header))

        if operation == QtNetwork.QNetworkAccessManager.PostOperation:
            if data:
                data = data.readAll()
            result = requests.post(
                url.toString(),
                data=data,
                verify=PyGlassEnvironment.requestsCABundle,
                headers=headers
            )
        else:
            result = requests.get(
                url.toString(),
                verify=PyGlassEnvironment.requestsCABundle,
                headers=headers
            )

        self.content = result.content
        for headerName, headerValue in result.headers.iteritems():
            if headerName in ['content-length', 'connection', 'content-encoding']:
                continue
            self.setRawHeader(headerName, headerValue)

        self._finalize(url)
        return


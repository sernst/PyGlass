# ResourceCustomNetworkReply.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os

from PySide import QtCore
from PySide import QtNetwork
from pyaid.dict.DictUtils import DictUtils
from pyaid.enum.MimeTypeEnum import MIME_TYPES
from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils

from pyglass.web.HttpsRemoteExecutionThread import HttpsRemoteExecutionThread

#___________________________________________________________________________________________________ ResourceCustomNetworkReply
class ResourceCustomNetworkReply(QtNetwork.QNetworkReply):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, request, operation, data, page):
        QtNetwork.QNetworkReply.__init__(self, parent)
        mainWindow  = page.mainWindow
        url         = request.url()
        scheme      = url.scheme()
        self.offset = 0

        self.setRequest(request)
        self.setOperation(operation)
        self.setUrl(url)

        if scheme == 'https':
            self._buildHttpsReply(parent, request, url, operation, data, page)
            return

        if scheme == 'http':
            host = url.host()
            scheme = host.split('.', 1)[0]
            pathHost = None
        else:
            pathHost = url.host()

        path = url.path()
        if not path and pathHost:
            path = [pathHost]
        else:
            path = url.path().strip().strip('/').split('/')
            if pathHost:
                path.insert(0, pathHost)

        if path[-1].endswith('.js'):
            contentType = MIME_TYPES.JAVASCRIPT
        elif path[-1].endswith('.css'):
            contentType = MIME_TYPES.CSS
        elif path[-1].endswith('.png'):
            contentType = MIME_TYPES.PNG_IMAGE
        elif path[-1].endswith('.jpg'):
            contentType = MIME_TYPES.JPEG_IMAGE
        elif path[-1].endswith('.swf'):
            contentType = MIME_TYPES.SWF
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
            if contentType in [MIME_TYPES.JPEG_IMAGE, MIME_TYPES.PNG_IMAGE, MIME_TYPES.SWF]:
                f = open(path, 'rb+')
            else:
                f = open(path, 'r+')
            self.content = f.read()
            f.close()
        else:
            print('WARNING: Resource URL does not exist ->', path)
            self.content = ''

        self._finalize()

#___________________________________________________________________________________________________ abort
    def abort(self, *args, **kwargs):
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
    def _finalize(self):
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))
        self.setError(QtNetwork.QNetworkReply.NoError, '')
        self.open(self.ReadOnly | self.Unbuffered)
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))

#___________________________________________________________________________________________________
    def _buildHttpsReply(self, parent, request, url, operation, data, page):
        headers = dict()
        for header in request.rawHeaderList():
            headers[StringUtils.toUnicode(header)] = StringUtils.toUnicode(request.rawHeader(header))
        if data:
            data = data.readAll()

        thread = HttpsRemoteExecutionThread(
            parent=self,
            operation=operation,
            data=data,
            headers=headers,
            url=url.toString()
        )
        thread.completeSignal.signal.connect(self._handleHttpsResult)
        thread.start()

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleHttpsResult
    def _handleHttpsResult(self, threadResult):
        result = threadResult['output']

        self.content = result.content
        for headerName, headerValue in DictUtils.iter(result.headers):
            if headerName in ['content-length', 'connection', 'content-encoding']:
                continue
            self.setRawHeader(headerName, headerValue)

        self._finalize()
        return


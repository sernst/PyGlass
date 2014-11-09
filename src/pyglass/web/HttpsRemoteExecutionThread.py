# HttpsRemoteExecutionThread.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import requests

from PySide import QtNetwork

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

#___________________________________________________________________________________________________ HttpsRemoteExecutionThread
class HttpsRemoteExecutionThread(RemoteExecutionThread):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._kwargs = kwargs

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        operation = self._kwargs.get('operation', None)
        headers   = self._kwargs.get('headers', None)
        data      = self._kwargs.get('data', None)
        url       = self._kwargs.get('url', None)

        if operation == QtNetwork.QNetworkAccessManager.PostOperation:
            result = requests.post(
                url,
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

        self._output = result
        return 0

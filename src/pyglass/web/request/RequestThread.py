# RequestThread.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.web.request.RequestUtils import RequestUtils
from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

#___________________________________________________________________________________________________ RequestThread
class RequestThread(RemoteExecutionThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, url, args =None, **kwargs):
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._url  = url
        self._args = args

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        try:
            self._output = RequestUtils.executeRequest(
                url=self._url,
                args=self._args,
                logger=self._log
            )
        except Exception as err:
            self._log.writeError('FAILED: Request attempt.', err)
            return 1

        if self._output is None:
            return 1
        return 0

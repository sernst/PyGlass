# RemoteExecutionThread.py
# (C)2012-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import warnings

from PySide import QtCore

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyglass.threading.RemoteThreadEvent import RemoteThreadEvent

#___________________________________________________________________________________________________ RemoteExecutionThread
class RemoteExecutionThread(QtCore.QThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVE_THREAD_STORAGE = []

    completeSignal = QtCore.Signal(object)
    eventSignal    = QtCore.Signal(object)
    logSignal      = QtCore.Signal(object)
    progressSignal = QtCore.Signal(object)

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        QtCore.QThread.__init__(self, parent)

        self.userData = ArgsUtils.get('userData', None, kwargs)

        self._events           = dict()
        self._log              = Logger(self)
        self._log.trace        = True
        self._log.addPrintCallback(self._handleLogWritten)
        self._maxLogBufferSize = 0
        self._logBuffer        = []
        self._returnCode         = None
        self._output           = None
        self._error            = None
        self._explicitComplete = ArgsUtils.get('explicitComplete', False, kwargs)

        # Add the thread to the static active thread storage so that it won't be garbage collected
        # until the thread completes.
        self.__class__._ACTIVE_THREAD_STORAGE.append(self)

        self._connectSignals(**kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: success
    @property
    def success(self):
        return self.returnCode == 0

#___________________________________________________________________________________________________ GS: log
    @property
    def log(self):
        return self._log

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        warnings.warn(
            'RemoteExceutionThread.response is deprecated in favor of .returnCode',
            DeprecationWarning)
        self._log.write('[DEPRECATION WARNING]: Use returnCode instead of response', traceStack=True)
        return self._returnCode

#___________________________________________________________________________________________________ GS: returnCode
    @property
    def returnCode(self):
        return self._returnCode

#___________________________________________________________________________________________________ GS: output
    @property
    def output(self):
        return self._output

#___________________________________________________________________________________________________ GS: error
    @property
    def error(self):
        return self._error

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ dispatchEvent
    def dispatchEvent(self, signal, identifier =None, data =None):
        signal.emit(RemoteThreadEvent(
            identifier=identifier,
            target=self,
            data=data))

#___________________________________________________________________________________________________ execute
    def execute(
            self, callback =None, logCallback =None, progressCallback =None,
            eventCallback =None, **kwargs
    ):
        self._connectSignals(
            callback=callback,
            logCallback=logCallback,
            progressCallback=progressCallback,
            eventCallback=eventCallback,
            **kwargs)

        self.start()

#___________________________________________________________________________________________________ run
    def run(self):
        """ Thread run method."""
        response = self._runImpl()
        if self._explicitComplete:
            return

        self._runComplete(response)

#___________________________________________________________________________________________________ connectSignals
    def connectSignals(self, onComplete =None, onLog =None, onProgress =None, onEvent =None):
        """ Quick access method to connect callbacks to the various remote thread signals. """

        return self._connectSignals(
            callback=onComplete,
            logCallback=onLog,
            progressCallback=onProgress,
            eventCallback=onEvent)

#___________________________________________________________________________________________________ enableLogBuffer
    def enableLogBuffer(self, maxLength = 0):
        self._maxLogBufferSize = maxLength

#___________________________________________________________________________________________________ disableLogBuffer
    def disableLogBuffer(self):
        self.flushLogBuffer(disable=True)

#___________________________________________________________________________________________________ flushLogBuffer
    def flushLogBuffer(self, disable =False):
        if disable:
            self._maxLogBufferSize = 0

        if self._logBuffer:
            b = self._logBuffer
            self._logBuffer = []
            self.dispatchEvent(self.logSignal, 'log', {'message':'\n'.join(b)})

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectSignals
    def _connectSignals(self, **kwargs):
        logCallback = ArgsUtils.get('logCallback', None, kwargs)
        if logCallback:
            self.logSignal.connect(logCallback)

        completeCallback = ArgsUtils.get('callback', None, kwargs)
        if completeCallback:
            self.completeSignal.connect(completeCallback)

        progressCallback = ArgsUtils.get('progressCallback', None, kwargs)
        if progressCallback:
            self.progressSignal.connect(progressCallback)

        eventCallback = ArgsUtils.get('eventCallback', None, kwargs)
        if eventCallback:
            self.eventSignal.connect(eventCallback)

#___________________________________________________________________________________________________ _runComplete
    def _runComplete(self, response):
        self._returnCode = response
        if self._returnCode is None:
            self._returnCode = 0

        self.dispatchEvent(self.completeSignal, 'complete', {
            'response':self._returnCode,
            'error':self._error,
            'output':self._output,
            'thread':self,
            'userData':self.userData })

        # Remove the thread from the active thread storage so that it can be garbage collected.
        self.__class__._ACTIVE_THREAD_STORAGE.remove(self)

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        return 0

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleLogWritten
    def _handleLogWritten(self, logger, value):
        if self._maxLogBufferSize > 0:
            self._logBuffer.append(value)
            if len(self._logBuffer) > self._maxLogBufferSize:
                self.flushLogBuffer()
        else:
            self.dispatchEvent(self.logSignal, 'log', {'message':value})

# RemoteExecutionThread.py
# (C)2012-2014
# Scott Ernst

from PySide import QtCore

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger

#___________________________________________________________________________________________________ RemoteExecutionThread
class RemoteExecutionThread(QtCore.QThread):
    """ Threaded external processor execution"""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVE_THREAD_STORAGE = []

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
        self._response         = None
        self._output           = None
        self._error            = None
        self._explicitComplete = ArgsUtils.get('explicitComplete', False, kwargs)

        class RETCompleteSignal(QtCore.QObject):
            signal = QtCore.Signal(dict)
        self._completeSignal = RETCompleteSignal()

        class RETLogSignal(QtCore.QObject):
            signal = QtCore.Signal(str)
        self._logSignal = RETLogSignal()

        class RETProgressSignal(QtCore.QObject):
            signal = QtCore.Signal(dict)
        self._progressSignal = RETProgressSignal()

        class RETEventSignal(QtCore.QObject):
            signal = QtCore.Signal(dict)
        self._eventSignal = RETEventSignal()

        # Add the thread to the static active thread storage so that it won't be garbage collected
        # until the thread completes.
        self.__class__._ACTIVE_THREAD_STORAGE.append(self)

        self._connectSignals(**kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: log
    @property
    def log(self):
        return self._log

#___________________________________________________________________________________________________ GS: logSignal
    @property
    def logSignal(self):
        return self._logSignal

#___________________________________________________________________________________________________ GS: completeSignal
    @property
    def completeSignal(self):
        return self._completeSignal

#___________________________________________________________________________________________________ GS: progressSignal
    @property
    def progressSignal(self):
        return self._progressSignal

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        return self._response

#___________________________________________________________________________________________________ GS: returnCode
    @property
    def returnCode(self):
        return self._response

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
    def dispatchEvent(self, identifier, target =None, data =None):
        self._eventSignal.signal.emit({
            'id':identifier,
            'source':self,
            'target':target if target else self,
            'data':data })

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
            self._logSignal.signal.emit(u'\n'.join(b))

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _connectSignals
    def _connectSignals(self, **kwargs):
        logCallback = ArgsUtils.get('logCallback', None, kwargs)
        if logCallback:
            self._logSignal.signal.connect(logCallback)

        completeCallback = ArgsUtils.get('callback', None, kwargs)
        if completeCallback:
            self._completeSignal.signal.connect(completeCallback)

        progressCallback = ArgsUtils.get('progressCallback', None, kwargs)
        if progressCallback:
            self._progressSignal.signal.connect(progressCallback)

        eventCallback = ArgsUtils.get('eventCallback', None, kwargs)
        if eventCallback:
            self._eventSignal.signal.connect(eventCallback)

#___________________________________________________________________________________________________ _runComplete
    def _runComplete(self, response):
        self._response = response
        if self._response is None:
            self._response = 0

        self._completeSignal.signal.emit({
            'response':self._response,
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
            self._logSignal.signal.emit(value)

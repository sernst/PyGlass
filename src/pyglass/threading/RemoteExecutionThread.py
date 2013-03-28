# RemoteExecutionThread.py
# (C)2012-2013
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

        self._log              = Logger(self)
        self._log.addPrintCallback(self._handleLogWritten)
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

        # Add the thread to the static active thread storage so that it won't be garbage collected
        # until the thread completes.
        self.__class__._ACTIVE_THREAD_STORAGE.append(self)

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

#___________________________________________________________________________________________________ run
    def run(self):
        """ Thread run method."""
        response = self._runImpl()
        if self._explicitComplete:
            return

        self._runComplete(response)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runComplete
    def _runComplete(self, response):
        self._response = response
        if self._response is None:
            self._response = 0

        self._completeSignal.signal.emit({
            'response':self._response,
            'error':self._error,
            'output':self._output,
            'thread':self
        })

        # Remove the thread from the active thread storage so that it can be garbage collected.
        self.__class__._ACTIVE_THREAD_STORAGE.remove(self)

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        return 0

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleLogWritten
    def _handleLogWritten(self, logger, value):
        self._logSignal.signal.emit(value)

# FunctionRemoteExecutionThread.py
# (C)2014
# Scott Ernst

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

#___________________________________________________________________________________________________ FunctionRemoteExecutionThread
class FunctionRemoteExecutionThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, function, *args, **kwargs):
        """Creates a new instance of FunctionRemoteExecutionThread."""

        super(FunctionRemoteExecutionThread, self).__init__(parent)
        self._function = function
        self._args = args
        self._kwargs = kwargs

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        """Doc..."""

        self._output = self._function(*self._args, **self._kwargs)


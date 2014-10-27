# RemoteThreadEvent.py
# (C)2014
# Scott Ernst

from pyglass.event.PyGlassSignalEvent import PyGlassSignalEvent

#___________________________________________________________________________________________________ RemoteThreadEvent
class RemoteThreadEvent(PyGlassSignalEvent):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, identifier, target, data =None):
        """Creates a new instance of RemoteThreadEvent."""
        self._id = identifier
        super(RemoteThreadEvent, self).__init__(target=target, data=data)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: id
    @property
    def id(self):
        return self._id

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None):
        """get doc..."""
        try:
            self.data[key]
        except Exception, err:
            return defaultValue

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __getitem__
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        return super(RemoteThreadEvent, self).__getitem__(key)

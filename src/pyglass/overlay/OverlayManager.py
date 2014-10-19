# OverlayManager.py
# (C)2014
# Scott Ernst

from pyglass.data.PyGlassObject import PyGlassObject

#___________________________________________________________________________________________________ OverlayManager
class OverlayManager(PyGlassObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, owner):
        """Creates a new instance of OverlayManager."""
        self._owner = owner
        self._overlays = []
        super(OverlayManager, self).__init__()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: overlays
    @property
    def overlays(self):
        return self._overlays

#___________________________________________________________________________________________________ GS: parent
    @property
    def owner(self):
        return self._owner

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ resize
    def resize(self):
        """resize doc..."""
        if not self._overlays:
            return

        size = self.owner.size()
        for overlay in self._overlays:
            overlay.changeSize(size.width(), size.height())

#___________________________________________________________________________________________________ add
    def add(self, overlay):
        """add doc..."""
        if overlay in self._overlays:
            return True
        self._overlays.append(overlay)
        overlay.manager = self
        overlay.setParent(self.owner)
        size = self.owner.size()
        overlay.changeSize(size.width(), size.height())
        return True

#___________________________________________________________________________________________________ show
    def show(self, name):
        """show doc..."""
        try:
            self.getByName(name).show()
            return True
        except Exception, err:
            return False

#___________________________________________________________________________________________________ hide
    def hide(self, name):
        """hideByName doc..."""
        try:
            self.getByName(name).hide()
            return True
        except Exception, err:
            return False

#___________________________________________________________________________________________________ getByName
    def getByName(self, name):
        """getByName doc..."""
        for overlay in self._overlays:
            if overlay.name == name:
                return overlay
        return None

#___________________________________________________________________________________________________ removeByName
    def removeByName(self, name, delete =False):
        """removeByName doc..."""
        overlay = self.getByName(name)
        if not overlay:
            return False
        return self.remove(overlay, delete=delete)

#___________________________________________________________________________________________________ remove
    def remove(self, overlay, delete =False):
        if overlay in self._overlays:
            self._overlays.remove(overlay)
            overlay.setParent(None)
            if delete:
                overlay.deleteLater()
            return True
        return False

#___________________________________________________________________________________________________ clear
    def clear(self):
        """clear doc..."""
        while len(self.overlays) > 0:
            self.remove(self.overlays[0])

#___________________________________________________________________________________________________ dispose
    def dispose(self):
        """dispose doc..."""
        self.clear()



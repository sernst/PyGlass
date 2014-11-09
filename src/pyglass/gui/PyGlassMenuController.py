# PyGlassMenuController.py
# (C)2012
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtCore
from PySide import QtGui

from pyaid.string.StringUtils import StringUtils

#___________________________________________________________________________________________________ PyGlassMenuController
class PyGlassMenuController(QtCore.QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, window, menu, **kwargs):
        """Creates a new instance of PyGlassMenuController."""
        QtCore.QObject.__init__(self, window)
        self._window = window

        assert type(menu) is QtGui.QMenuBar, "Inavlid menu assignment"

        self._menu = menu

        if self.fileExitAction:
            self.fileExitAction.triggered.connect(self._handleExitAction)

        self._findMenus()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: menuBar
    @property
    def menuBar(self):
        return self._menu

#___________________________________________________________________________________________________ GS: fileExitAction
    @property
    def fileExitAction(self):
        if hasattr(self._window, 'fileExitAction'):
            return self._window.fileExitAction
        return None

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ enable
    def enable(self):
        """Doc..."""
        for menu in self._findMenus():
            menu.setEnabled(True)

#___________________________________________________________________________________________________ disable
    def disable(self):
        """Doc..."""
        for menu in self._findMenus():
            menu.setEnabled(False)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _findMenus
    def _findMenus(self):
        out = []
        for item in dir(self._window):
            item = getattr(self._window, item)
            if isinstance(item, QtGui.QMenu) and item.parent() == self._menu:
                out.append(item)

        return out

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleExitAction
    def _handleExitAction(self, *args, **kwargs):
        self._window.exit()

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


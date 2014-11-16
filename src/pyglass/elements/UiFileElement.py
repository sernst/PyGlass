# UiFileElement.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.gui.UiFileLoader import UiFileLoader

#*************************************************************************************************** UiFileElement
class UiFileElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, pathNoExtension, **kwargs):
        """Creates a new instance of UiFileElement."""
        super(UiFileElement, self).__init__(parent=parent, **kwargs)
        self._widgetData = UiFileLoader.loadUiFile(self, pathNoExtension, True)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: widgetData
    @property
    def widgetData(self):
        return self._widgetData

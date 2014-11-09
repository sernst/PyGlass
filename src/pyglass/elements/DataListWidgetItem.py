# DataListWidgetItem.py
# (C)2012-2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

#___________________________________________________________________________________________________ DataListWidgetItem
class DataListWidgetItem(QtGui.QListWidgetItem):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of DataListWidgetItem."""
        self._itemData = ArgsUtils.extract('data', None, kwargs)
        self._itemId   = ArgsUtils.extract('ident', None, kwargs)
        super(DataListWidgetItem, self).__init__(*args, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: ident
    @property
    def ident(self):
        return self._itemId
    @ident.setter
    def ident(self, value):
        self._itemId = value

#___________________________________________________________________________________________________ GS: itemData
    @property
    def itemData(self):
        return self._itemData
    @itemData.setter
    def itemData(self, value):
        self._itemData = value

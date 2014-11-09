# GridListElement.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import math

from PySide import QtGui

from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.layouts.ResponsiveFlowLayout import ResponsiveFlowLayout

#___________________________________________________________________________________________________ GridListElement
class GridListElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of GridListElement."""
        super(GridListElement, self).__init__(parent=parent, **kwargs)
        self._widgetItems = []
        self._spacers = []

        self._lastColumnWidth = -100
        self._maxColumnWidth = 1024.0
        self._lastColumnCount = -1
        self._lastItemCount = 0
        self._updating = False

        # layout = QtGui.QGridLayout()
        layout = ResponsiveFlowLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        self.setLayout(layout)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isCenterAligned
    @property
    def isCenterAligned(self):
        return self.layout().isCentered
    @isCenterAligned.setter
    def isCenterAligned(self, value):
        self.layout().isCentered = value

#___________________________________________________________________________________________________ GS: maxColumnWidth
    @property
    def maxColumnWidth(self):
        return self._maxColumnWidth
    @maxColumnWidth.setter
    def maxColumnWidth(self, value):
        if self._maxColumnWidth == value:
            return
        self._maxColumnWidth = value
        self.updateItems()

#___________________________________________________________________________________________________ GS: columnWidth
    @property
    def columnWidth(self):
        count = self.columnCount
        w = float(self.size().width()) - 12.0*float(count)
        return min(self.maxColumnWidth, int(w/float(count)))

#___________________________________________________________________________________________________ GS: columnCount
    @property
    def columnCount(self):
        wMax = self.maxColumnWidth
        if wMax <= 0:
            return 1

        w = self.size().width()
        return float(max(1, math.ceil(float(w)/float(wMax))))

#___________________________________________________________________________________________________ GS: widgetItems
    @property
    def widgetItems(self):
        return self._widgetItems

#___________________________________________________________________________________________________ GS: widgetCount
    @property
    def widgetCount(self):
        return len(self.widgetItems)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getGridCoordinatesFromIndex
    def getGridCoordinatesFromIndex(self, index):
        cols = self.columnCount
        return math.floor(float(index)/cols), index % cols

#___________________________________________________________________________________________________ updateItems
    def updateItems(self, reorder =True):
        if self._updating:
            return
        self._updating = True

        index  = 0
        layout = self.layout()
        count  = self.columnCount

        for widget in self._widgetItems:
            if reorder:
                layout.removeWidget(widget)
                layout.addWidget(widget)
            widget.setVisible(True)
            index += 1

        self._lastColumnCount = count
        self._lastItemCount = len(self._widgetItems)
        self._updating = False
        self.updateGeometry()
        self.update()

#___________________________________________________________________________________________________ insertItem
    def insertItems(self, index, *widgets):
        for widget in widgets:
            if widget in self._widgetItems:
                if self._widgetItems.index(widget) == index:
                    return
                self._widgetItems.remove(widget)
            self._widgetItems.insert(index, widget)
            widget.setParent(self)
            index += 1
        self.updateItems()

#___________________________________________________________________________________________________ addItems
    def addItems(self, *widgets):
        """Doc..."""
        for widget in widgets:
            if widget in self._widgetItems:
                self._widgetItems.remove(widget)
            self._widgetItems.append(widget)
            widget.setParent(self)
        self.updateItems()

#___________________________________________________________________________________________________ removeItems
    def removeItems(self, *widgets):
        out = []
        for widget in widgets:
            if not widget in self._widgetItems:
                continue
            self._widgetItems.remove(widget)
            widget.setParent(None)
            self.layout().removeWidget(widget)
            out.append(widget)
        self.updateItems()
        return out

#___________________________________________________________________________________________________ clear
    def clear(self):
        while len(self._widgetItems) > 0:
            widget = self._widgetItems.pop()
            self.layout().removeWidget(widget)
            widget.setParent(None)
        self.updateItems()

#___________________________________________________________________________________________________ getIndexOfWidget
    def getIndexOfWidget(self, widget):
        try:
            return self._widgetItems.index(widget)
        except Exception as err:
            return -1

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getSpacer
    def _getSpacer(self, index):
        """_getSpacer doc..."""
        if index < len(self._spacers):
            return self._spacers[index]

        spacer, layout = self._createWidget(self, QtGui.QHBoxLayout)
        layout.addStretch()
        spacer.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        self._spacers.append(spacer)
        return spacer

#___________________________________________________________________________________________________ _resizeImpl
    def _resizeImpl(self, *args, **kwargs):
        super(GridListElement, self)._resizeImpl(*args, **kwargs)

        columnWidth = self.columnWidth

        if columnWidth - self._lastColumnWidth:
            self._lastColumnWidth = columnWidth
            self.layout().itemWidth = columnWidth
            self.updateItems(reorder=False)

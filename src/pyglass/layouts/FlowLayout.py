# FlowLayout.py
# (C)2014
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

#___________________________________________________________________________________________________ FlowLayout
class FlowLayout(QtGui.QLayout):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, spacing =-1):
        super(FlowLayout, self).__init__(parent)
        self.setSpacing(spacing)
        self.itemList = []
        self._isCentered = False
        self._isAlignedPerRow = False

#___________________________________________________________________________________________________ __del__
    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: isAlignedPerRow
    @property
    def isAlignedPerRow(self):
        return self._isAlignedPerRow
    @isAlignedPerRow.setter
    def isAlignedPerRow(self, value):
        self._isAlignedPerRow = value
        self.update()

#___________________________________________________________________________________________________ GS: isCentered
    @property
    def isCentered(self):
        return self._isCentered
    @isCentered.setter
    def isCentered(self, value):
        self._isCentered = value
        self.update()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addItem
    def addItem(self, item):
        self.itemList.append(item)

#___________________________________________________________________________________________________ count
    def count(self):
        return len(self.itemList)

#___________________________________________________________________________________________________ itemAt
    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

#___________________________________________________________________________________________________ takeAt
    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

#___________________________________________________________________________________________________ expandingDirections
    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

#___________________________________________________________________________________________________ hasHeightForWidth
    def hasHeightForWidth(self):
        return True

#___________________________________________________________________________________________________ heightForWidth
    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

#___________________________________________________________________________________________________ setGeometry
    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

#___________________________________________________________________________________________________ sizeHint
    def sizeHint(self):
        return self.minimumSize()

#___________________________________________________________________________________________________ minimumSize
    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.getContentsMargins()
        size += QtCore.QSize(margins[0] + margins[2], margins[1] + margins[3])
        return size

#___________________________________________________________________________________________________ doLayout
    def doLayout(self, rect, testOnly):
        margins = self.getContentsMargins()
        spaceX  = self.spacing()
        spaceY  = self.spacing()

        x = rect.x() + margins[0]
        y = rect.y() + margins[1]
        lineHeight = 0

        maxWide = rect.right() - margins[2]
        xMax = 0

        row = {'xMax':0, 'items':[]}
        rowList = [row]
        for item in self.itemList:
            widgetSize = self._getWidgetSize(item)
            nextX = x + widgetSize.width() + spaceX
            if (nextX - spaceX) > maxWide and lineHeight > 0:
                x = rect.x() + margins[0]
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

                row = {'xMax':0, 'items':[]}
                rowList.append(row)

            row['xMax'] = max(row['xMax'], nextX - spaceX)
            xMax = max(xMax, nextX - spaceX)

            if not testOnly:
                try:
                    item.widget().setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), widgetSize))
                except Exception, err:
                    pass
                row['items'].append((item, x, y, widgetSize))

            x = nextX
            lineHeight = max(lineHeight, widgetSize.height())

        # Skip actual layout if running in test only mode
        if testOnly:
            return y + lineHeight - rect.y()

        #-------------------------------------------------------------------------------------------
        # APPLY LAYOUT
        #       Use the layout calculations above to apply the layouts to each child item of the
        #       layout.
        for row in rowList:
            if not row['items']:
                continue

            rowWide = row['xMax'] if self.isAlignedPerRow else xMax
            xOffset = int(0.5*float(maxWide - rowWide)) if self.isCentered else 0
            for data in row['items']:
                data[0].setGeometry(QtCore.QRect(
                    QtCore.QPoint(data[1] + xOffset, data[2]), data[3]))

        return y + lineHeight - rect.y()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getWidgetSize
    def _getWidgetSize(self, widget):
        """_getWidgetSize doc..."""
        return widget.sizeHint()

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

#___________________________________________________________________________________________________ __del__
    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

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

        for item in self.itemList:
            widgetSize = self._getWidgetSize(item)
            nextX = x + widgetSize.width() + spaceX
            if (nextX - spaceX) > (rect.right() - margins[2]) and lineHeight > 0:
                x = rect.x() + margins[0]
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                try:
                    item.widget().setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), widgetSize))
                except Exception, err:
                    pass
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), widgetSize))

            x = nextX
            lineHeight = max(lineHeight, widgetSize.height())

        return y + lineHeight - rect.y()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getWidgetSize
    def _getWidgetSize(self, widget):
        """_getWidgetSize doc..."""
        return widget.sizeHint()

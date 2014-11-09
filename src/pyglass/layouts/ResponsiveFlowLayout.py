# ResponsiveFlowLayout.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.layouts.FlowLayout import FlowLayout

#___________________________________________________________________________________________________ ResponsiveFlowLayout
class ResponsiveFlowLayout(FlowLayout):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, spacing =-1):
        """Creates a new instance of ResponsiveFlowLayout."""
        super(ResponsiveFlowLayout, self).__init__(parent=parent, spacing=spacing)
        self._itemWidth = 0

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: itemWidth
    @property
    def itemWidth(self):
        return self._itemWidth
    @itemWidth.setter
    def itemWidth(self, value):
        self._itemWidth = value

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getWidgetSize
    def _getWidgetSize(self, widgetItem):
        """_getWidgetSize doc..."""

        try:
            widget = widgetItem.widget()
        except Exception as err:
            return super(ResponsiveFlowLayout, self)._getWidgetSize(widgetItem)

        w = self.itemWidth
        if w <= 0:
            return super(ResponsiveFlowLayout, self)._getWidgetSize(widget)
        try:
            return widget.getSizeForWidth(self.itemWidth)
        except Exception as err:
            pass

        return super(ResponsiveFlowLayout, self)._getWidgetSize(widget)

# SimpleScrollArea.py
# (C)2013
# Scott Ernst

from PySide import QtGui
from pyaid.ArgsUtils import ArgsUtils

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ SimpleScrollArea
class SimpleScrollArea(PyGlassWidget):
    """ This is a basic QScrollArea wrapped in such a way to make it possible for the scroll area
        to have a transparent background in such a way that the transparent background styling
        doesn't get inherited by the child widgets of the scroll area.
    """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of SimpleScrollArea."""
        PyGlassWidget.__init__(self, parent, widgetFile=False)

        class SimpleScrollerInternal(QtGui.QScrollArea):
            pass

        class SimpleScrollerQWidget(QtGui.QWidget):
            pass

        self._borderColor = ArgsUtils.get('borderColor', None, kwargs)

        layout         = self._getLayout(self, QtGui.QVBoxLayout)
        self._scroller = SimpleScrollerInternal(self)
        self._scroller.setViewport(SimpleScrollerQWidget(self._scroller))
        layout.addWidget(self._scroller)

        self._scroller.setFrameShape(QtGui.QFrame.NoFrame)
        self._scroller.setFrameShadow(QtGui.QFrame.Plain)
        self._scroller.setLineWidth(0)

        self._innerWidget = SimpleScrollerQWidget(self._scroller)
        self._scroller.setWidget(self._innerWidget)
        self._scroller.setWidgetResizable(True)

        self._updateStyle()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: scrollArea
    @property
    def scrollArea(self):
        return self._scroller

#___________________________________________________________________________________________________ GS: containerWidget
    @property
    def containerWidget(self):
        return self._innerWidget

#___________________________________________________________________________________________________ GS: borderColor
    @property
    def borderColor(self):
        return self._borderColor
    @borderColor.setter
    def borderColor(self, value):
        if self._borderColor == value:
            return
        self._borderColor = value
        self._updateStyle()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateStyle
    def _updateStyle(self):
        styles = [
            u'background-color:transparent',
            u'border: 1px solid ' + (self._borderColor if self._borderColor else u'transparent')]

        s = u"SimpleScrollArea, SimpleScrollerInternal, SimpleScrollerQWidget { %s; }" % u'; '.join(styles)
        print u'STYLES:', s
        self.setStyleSheet(s)

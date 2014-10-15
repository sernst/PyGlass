# ApplicationLevelWidget.py
# (C)2014
# Scott Ernst

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ ApplicationLevelWidget
class ApplicationLevelWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of ApplicationLevelWidget."""
        super(ApplicationLevelWidget, self).__init__(parent=parent, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ activateWidgetDisplay
    def activateWidgetDisplay(self, **kwargs):
        if self._isWidgetActive:
            return

        self._displayCount += 1
        self._activateWidgetDisplayImpl(**kwargs)
        self._isWidgetActive = True
        self.updateGeometry()
        self.update()

#___________________________________________________________________________________________________ refreshWidgetDisplay
    def refreshWidgetDisplay(self):
        if not self._isWidgetActive:
            return
        self._refreshWidgetDisplayImpl()


#___________________________________________________________________________________________________ deactivateWidgetDisplay
    def deactivateWidgetDisplay(self, **kwargs):
        if not self._isWidgetActive:
            return

        self._deactivateWidgetDisplayImpl(**kwargs)
        self._isWidgetActive = False

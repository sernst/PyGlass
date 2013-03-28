# LoadingWidget.py
# (C)2012-2013
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ LoadingWidget
class LoadingWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    DEFAULT_HEADER = 'LOADING'
    DEFAULT_INFO   = '(one moment please)'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of LoadingWidget."""
        PyGlassWidget.__init__(self, parent, **kwargs)

        self._animatedIcon = QtGui.QMovie(self.getResourcePath('horizontal-loader.gif'))
        self.loadImageLabel.setMovie(self._animatedIcon)
        self.loadImageLabel.setVisible(False)
        self._displayInfo = None

        self._updateDisplay(**kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _refreshWidgetDisplayImpl
    def _refreshWidgetDisplayImpl(self):
        data = self._displayInfo if self._displayInfo is not None else dict()
        self._updateDisplay(**data)

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        self._displayInfo = kwargs
        self._refreshWidgetDisplayImpl()

#___________________________________________________________________________________________________ _deactivateWidgetDisplayImpl
    def _deactivateWidgetDisplayImpl(self, **kwargs):
        self._animatedIcon.stop()

#___________________________________________________________________________________________________ _updateDisplay
    def _updateDisplay(self, **kwargs):
        cls = self.__class__
        self.headerLabel.setText(ArgsUtils.get('header', cls.DEFAULT_HEADER, kwargs))
        self.infoLabel.setText(ArgsUtils.get('message', cls.DEFAULT_INFO, kwargs))

        showIcon = ArgsUtils.get('animated', True, kwargs)
        self.loadImageLabel.setVisible(showIcon)
        if showIcon:
            self._animatedIcon.start()
        else:
            self._animatedIcon.stop()

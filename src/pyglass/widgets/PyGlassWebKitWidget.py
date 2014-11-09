# PyGlassWebKitWidget.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.web.PyGlassWebView import PyGlassWebView

#___________________________________________________________________________________________________ PyGlassWebKitWidget
class PyGlassWebKitWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PyGlassWebKitWidget."""
        self._communicator = ArgsUtils.extract('communicator', None, kwargs)
        self._debug        = ArgsUtils.extract('debug', False, kwargs)
        url                = ArgsUtils.extract('url', None, kwargs)
        localUrl           = ArgsUtils.extract('localUrl', None, kwargs)
        PyGlassWidget.__init__(self, parent, widgetFile=False, **kwargs)

        layout = self._getLayout(self, QtGui.QVBoxLayout)
        layout.setContentsMargins(0, 0, 0, 0)

        self._webView = PyGlassWebView(
            self,
            communicator=self._communicator,
            debug=self._debug
        )
        layout.addWidget(self._webView)
        self.setLayout(layout)

        if url:
            self._webView.openUrl(url)
        elif localUrl:
            self._webView.openLocalWebUrl(url)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: webView
    @property
    def webView(self):
        return self._webView

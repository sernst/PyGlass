# HelloWorldMainWindow.py
# (C)2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyglass.elements.buttons.PyGlassPushButton import PyGlassPushButton
from pyglass.themes.ColorSchemes import ColorSchemes
from pyglass.windows.PyGlassWindow import PyGlassWindow

#___________________________________________________________________________________________________ HelloWorldMainWindow
class HelloWorldMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        PyGlassWindow.__init__(self, **kwargs)

        widget = QtGui.QWidget(self)
        self.setCentralWidget(widget)

        layout = QtGui.QVBoxLayout(widget)
        widget.setLayout(layout)

        label = QtGui.QLabel(widget)
        label.setText(u'Hello World')
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        button = PyGlassPushButton(
            self,
            colorScheme=ColorSchemes.GREY,
            toggleColorScheme=ColorSchemes.BLUE,
            toggles=True
        )
        button.setText(u'Hello!')
        layout.addWidget(button)

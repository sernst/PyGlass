# HelloWorldMainWindow.py
# (C)2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyglass.elements.buttons.PyGlassPushButton import PyGlassPushButton
from pyglass.elements.icons.IconSheetMap import IconSheetMap
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
            icon=IconSheetMap.ATOMIC,
            text=u'Atomic',
            colorScheme=ColorSchemes.GREY,
            toggleColorScheme=ColorSchemes.BLUE,
            toggles=True
        )
        #button.setText(u'Hello!')
        layout.addWidget(button)

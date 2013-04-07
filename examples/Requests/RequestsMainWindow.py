# RequestsMainWindow.py
# (C)2013
# Scott Ernst

import re

from PySide import QtCore
from PySide import QtGui

from pyglass.web.request.Request import Request
from pyglass.windows.PyGlassWindow import PyGlassWindow

#___________________________________________________________________________________________________ RequestsMainWindow
class RequestsMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        PyGlassWindow.__init__(self, title=u'Requests Example', **kwargs)

        widget = self._createCentralWidget()
        layout = QtGui.QVBoxLayout(widget)
        widget.setLayout(layout)

        label = QtGui.QLabel(widget)
        label.setText(u'Request In Progress')
        label.setStyleSheet("QLabel { font-size:14px; color:#444; }")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)
        self._label = label

        Request.send(
            parent=self,
            url='http://www.google.com',
            callback=self._handleRequestComplete
        )

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleRequestComplete
    def _handleRequestComplete(self, response):
        if not response.success:
            self._label.setText(u'Request Failed')
            return

        pattern = re.compile(u'<[a-zA-Z0-9]+')
        counts  = dict()
        for tag in pattern.findall(response.content):
            tagName = tag[1:].lower()
            if tagName not in counts:
                counts[tagName] = 1
            else:
                counts[tagName] += 1

        counts = counts.items()
        counts.sort(key=lambda x: x[1], reverse=True)

        out = []
        for item in counts:
            out.append(item[0] + u': ' + unicode(item[1]))
        self._label.setText(u'\n'.join(out))

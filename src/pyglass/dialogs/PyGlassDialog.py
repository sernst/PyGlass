# PyGlassDialog.py
# (C)2012-2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

#___________________________________________________________________________________________________ PyGlassDialog
class PyGlassDialog(QtGui.QDialog):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PySideGui."""
        flags = ArgsUtils.extract('flags', None, kwargs)
        if flags is None:
            # By default the close button is hidden (only title shows)
            flags = QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint

        title          = ArgsUtils.extract('title', 'Dialog', kwargs)
        modal          = ArgsUtils.extract('modal', True, kwargs)
        widgetClass    = ArgsUtils.extract('widget', None, kwargs)
        self._callback = ArgsUtils.extract('callback', None, kwargs)
        self._canceled = True

        QtGui.QDialog.__init__(self, parent, flags)

        self.setStyleSheet(self.owner.styleSheetPath)
        if widgetClass is None:
            self._widget = None
        else:
            layout       = self._getLayout(self)
            self._widget = widgetClass(parent=self, **kwargs)
            layout.addWidget(self._widget)

        self.setModal(modal)
        self.setWindowTitle(title)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: canceled
    @property
    def canceled(self):
        return self._canceled

#___________________________________________________________________________________________________ GS: isDialogWindow
    @property
    def isDialogWindow(self):
        return True

#___________________________________________________________________________________________________ GS: allowsOwnership
    @property
    def allowsOwnership(self):
        return False

#___________________________________________________________________________________________________ GS: owner
    @property
    def owner(self):
        out = self.parent()
        while out:
            if hasattr(out, 'allowsOwnership') and getattr(out, 'allowsOwnership', False):
                return out
            out = out.parent()

        return None

#___________________________________________________________________________________________________ GS: dialogWindow
    @property
    def dialogWindow(self):
        return self

#___________________________________________________________________________________________________ GS: contentWidget
    @property
    def contentWidget(self):
        return self._widget

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        if self._mainWindow is None:
            out = self.parent()
            while out:
                if hasattr(out, 'mainWindow'):
                    self._mainWindow = out.mainWindow
                    return self._mainWindow

                if hasattr(out, 'isMainWindow') and out.isMainWindow:
                    self._mainWindow = out
                    return out

                out = out.parent()

        return self._mainWindow

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ refreshGui
    def refreshGui(self):
        self.owner.refreshGui()

#___________________________________________________________________________________________________ closeEvent
    def closeEvent(self, *args, **kwargs):
        if self._callback is None:
            return

        self.refreshGui()
        self._callback(self)

#___________________________________________________________________________________________________ cancelClose
    def cancelClose(self):
        self._canceled = True
        self.close()

#___________________________________________________________________________________________________ successClose
    def successClose(self):
        self._canceled = False
        self.close()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getLayout
    def _getLayout(self, targetWidget, layoutClass =None, force =False, cleanupForceRemoval =True):
        layout = targetWidget.layout()
        if layout and (layoutClass is None or isinstance(layout, layoutClass)):
            return layout

        if layout and force:
            layout.setParent(None)
            layout.deleteLater()
            for child in targetWidget.children():
                child.setParent(None)
                if cleanupForceRemoval:
                    child.deleteLater()
        elif layout:
            print 'WARNING: Invalid layout change attempt:', targetWidget, layoutClass, layout
            return layout

        if not layoutClass:
            layoutClass = QtGui.QVBoxLayout
        layout = layoutClass(targetWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        targetWidget.setLayout(layout)
        return layout

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

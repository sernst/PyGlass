# PyGlassWidget.py
# (C)2012-2014
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

#AS NEEDED: from pyglass.widgets.LoadingWidget import LoadingWidget
from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.gui.PyGlassBackgroundParent import PyGlassBackgroundParent
from pyglass.gui.UiFileLoader import UiFileLoader

#___________________________________________________________________________________________________ PyGlassWidget
class PyGlassWidget(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    RESOURCE_FOLDER_PREFIX = None
    RESOURCE_FOLDER_NAME   = None

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, **kwargs):
        """Creates a new instance of PyGlassWidget."""
        PyGlassElement.__init__(self, parent, **kwargs)
        print 'CREATING: %s | PARENTED TO: %s' % (self, parent)
        self.setStyleSheet(self.owner.styleSheetPath)

        self._displayCount  = 0
        self._widgetClasses = dict()
        self._widgetParent  = None
        self._currentWidget = None
        self._widgets       = dict()
        self._widgetFlags   = ArgsUtils.get('widgetFlags', None, kwargs)
        self._widgetID      = ArgsUtils.get('widgetID', None, kwargs)

        widgetFile = ArgsUtils.get('widgetFile', True, kwargs)

        if widgetFile:
            self._widgetData = UiFileLoader.loadWidgetFile(self)
        else:
            self._widgetData = None

        name = ArgsUtils.get('containerWidgetName', None, kwargs)
        self._containerWidget = getattr(self, name) if name and hasattr(self, name) else None
        if not self._containerWidget:
            return

        self._widgetClasses = ArgsUtils.get('widgets', self._widgetClasses, kwargs)
        if 'loading' not in self._widgetClasses:
            from pyglass.widgets.LoadingWidget import LoadingWidget
            self._widgetClasses['loading'] = LoadingWidget

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: displayCount
    @property
    def displayCount(self):
        return self._displayCount

#___________________________________________________________________________________________________ GS: allowsOwnership
    @property
    def allowsOwnership(self):
        return True

#___________________________________________________________________________________________________ GS: styleSheetPath
    @property
    def styleSheetPath(self):
        return self.owner.styleSheetPath

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ addWidgetChild
    def addWidgetChild(self, key, widgetClass, setActive =False):
        self._widgetClasses[key] = widgetClass
        if setActive:
            return self.setActiveWidget(key)
        return True

#___________________________________________________________________________________________________ refresh
    def refresh(self, **kwargs):
        for widgetID, widget in self._widgets.iteritems():
            widget.refresh(**kwargs)

#___________________________________________________________________________________________________ clearActiveWidget
    def clearActiveWidget(self, containerWidget =None, doneArgs =None):
        if not self._currentWidget:
            return

        if doneArgs is None:
            doneArgs = dict()
        self._currentWidget.deactivateWidgetDisplay(**doneArgs)

        try:
            containerWidget.layout().removeWidget(self._currentWidget)
        except Exception, err:
            p = self._currentWidget.parent()
            if p:
                p.layout().removeWidget(self._currentWidget)

        self._currentWidget.setParent(self._widgetParent)
        self._currentWidget = None

#___________________________________________________________________________________________________ setActiveWidget
    def setActiveWidget(self, widgetID, containerWidget =None, force =False, args =None, doneArgs =None):
        if widgetID is None or widgetID not in self._widgetClasses:
            return False

        if containerWidget is None:
            containerWidget = self._containerWidget
        if containerWidget is None:
            return False

        if not force and self._currentWidget and self._currentWidget.widgetID == widgetID:
            return True

        if widgetID not in self._widgets:
            self.loadWidgets(widgetID)
        widget = self._widgets[widgetID]

        containerLayout = containerWidget.layout()
        if not containerLayout:
            containerLayout = self._getLayout(containerWidget, QtGui.QVBoxLayout)

        self.clearActiveWidget(containerWidget=containerWidget, doneArgs=doneArgs)
        self._currentWidget = widget
        containerLayout.addWidget(widget)
        containerWidget.setContentsMargins(0, 0, 0, 0)

        self.refreshGui()
        if args is None:
            args = dict()

        if self._isWidgetActive:
            widget.activateWidgetDisplay(**args)

        return True

#___________________________________________________________________________________________________ loadWidgets
    def loadWidgets(self, widgetIdents =None):
        if not widgetIdents:
            widgetIdents = self._widgetClasses.keys()
        elif isinstance(widgetIdents, basestring):
            widgetIdents = [widgetIdents]

        if self._widgetParent is None:
            self._widgetParent = PyGlassBackgroundParent(proxy=self)

        for widgetID in widgetIdents:
            if widgetID in self._widgets:
                continue

            if widgetID not in self._widgetClasses:
                self._log.write(
                    'ERROR: Unrecognized widgetID "%s" in %s' % (str(widgetID), str(self)) )

            widget = self._widgetClasses[widgetID](
                self._widgetParent, flags=self._widgetFlags, widgetID=widgetID)
            self._widgets[widgetID] = widget

#___________________________________________________________________________________________________ refreshWidgetDisplay
    def refreshWidgetDisplay(self):
        if self._currentWidget:
            self._currentWidget.refreshWidgetDisplay()
        self._refreshWidgetDisplayImpl()

#___________________________________________________________________________________________________ activateWidgetDisplay
    def activateWidgetDisplay(self, **kwargs):
        if self._isWidgetActive:
            return

        self._displayCount += 1
        self._activateWidgetDisplayImpl(**kwargs)

        if self._currentWidget:
            self._currentWidget.activateWidgetDisplay(**kwargs)

        self._isWidgetActive = True

#___________________________________________________________________________________________________ deactivateWidgetDisplay
    def deactivateWidgetDisplay(self, **kwargs):
        if not self._isWidgetActive:
            return

        self._deactivateWidgetDisplayImpl(**kwargs)

        if self._currentWidget:
            self._currentWidget.deactivateWidgetDisplay(**kwargs)

        self._isWidgetActive = False

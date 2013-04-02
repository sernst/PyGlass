# PyGlassGuiUtils.py
# (C)2013
# Scott Ernst

import inspect

from PySide.QtCore import QObject
from PySide import QtGui

from pyaid.ClassUtils import ClassUtils

#___________________________________________________________________________________________________ PyGlassGuiUtils
class PyGlassGuiUtils(QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    RESOURCE_FOLDER_PREFIX = 'RESOURCE_FOLDER_PREFIX'
    RESOURCE_FOLDER_NAME   = 'RESOURCE_FOLDER_NAME'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ GS: getOwner
    @classmethod
    def getOwner(cls, target):
        out = target.parent()
        if not out:
            try:
                return target.mainWindow.owner
            except Exception, err:
                pass
            return None

        while out:
            if hasattr(out, 'isBackgroundParent') and out.isBackgroundParent:
                out = out.backgroundTarget

            if hasattr(out, 'allowsOwnership') and getattr(out, 'allowsOwnership', False):
                return out
            out = out.parent()
        return None

#___________________________________________________________________________________________________ GS: getMainWindow
    @classmethod
    def getMainWindow(cls, target):
        out = target
        while out:
            if hasattr(out, 'isBackgroundParent') and out.isBackgroundParent:
                return out.backgroundTarget.mainWindow

            if hasattr(out, 'isMainWindow'):
                return out if out.isMainWindow else out.mainWindow

            out = out.parent()
        return None

#___________________________________________________________________________________________________ GS: getResourceFolderParts
    @classmethod
    def getResourceFolderParts(cls, target):
        if not inspect.isclass(target):
            target = target.__class__

        out = []
        prefix = ClassUtils.getAttrFromClass(target, cls.RESOURCE_FOLDER_PREFIX, None)
        if prefix:
            out.extend(prefix.split('/') if isinstance(prefix, basestring) else prefix)
        out.append(ClassUtils.getAttrFromClass(
            target, cls.RESOURCE_FOLDER_NAME, target.__name__
        ))
        return out

#___________________________________________________________________________________________________ gradientPainter
    @classmethod
    def gradientPainter(cls, target, size, upperColor, lowerColor):
        """ This method must be called within a paint event. It will paint a gradient background
            on the target widget for the specified size.
        """
        w     = size.width()
        h     = size.height()
        halfW = round(float(w)/2.0)
        halfH = round(float(h)/2.0)

        matrix = QtGui.QMatrix()
        matrix.translate(halfW, halfH)

        gradient = QtGui.QLinearGradient(halfW, -halfH, halfW, halfH)
        gradient.setColorAt(0, upperColor)
        gradient.setColorAt(1, lowerColor)

        brush = QtGui.QBrush(gradient)
        brush.setMatrix(matrix)

        painter = QtGui.QPainter(target)
        painter.setBrush(brush)
        painter.drawRect(0, 0, w, h)

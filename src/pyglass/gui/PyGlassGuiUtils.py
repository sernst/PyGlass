# PyGlassGuiUtils.py
# (C)2013-2014
# Scott Ernst

import os
import math
import inspect

from PySide import QtCore
from PySide import QtGui

from pyaid.ClassUtils import ClassUtils
from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ PyGlassGuiUtils
class PyGlassGuiUtils(QtCore.QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    RESOURCE_FOLDER_PREFIX = 'RESOURCE_FOLDER_PREFIX'
    RESOURCE_FOLDER_NAME   = 'RESOURCE_FOLDER_NAME'
    RESOURCE_WIDGET_FILE   = 'RESOURCE_WIDGET_FILE'

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

        resourceName = ClassUtils.getAttrFromClass(target, cls.RESOURCE_FOLDER_NAME, None)
        widget = ClassUtils.getAttrFromClass(target, cls.RESOURCE_WIDGET_FILE, None)
        if widget:
            widget = widget.split('/') if isinstance(widget, basestring) else widget
            out.extend(widget[:-1])

        if resourceName or not widget:
            out.append(resourceName if resourceName else target.__name__)
        return out

#___________________________________________________________________________________________________ gradientPainter
    @classmethod
    def gradientPainter(cls, target, size, upperColor, lowerColor):
        """ This method must be called within a paint event. It will paint a gradient background
            on the target widget for the specified size. """

        w     = size.width()
        h     = size.height()
        halfW = math.ceil(float(w)/2.0)
        halfH = math.ceil(float(h)/2.0)

        matrix = QtGui.QMatrix()
        matrix.translate(halfW, halfH)

        gradient = QtGui.QLinearGradient(halfW, -halfH - 1, halfW, halfH + 1)
        gradient.setColorAt(0.0, upperColor)
        gradient.setColorAt(1.0, lowerColor)

        brush = QtGui.QBrush(gradient)
        brush.setMatrix(matrix)

        painter = QtGui.QPainter(target)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(0, 0, w, h)

#___________________________________________________________________________________________________ fillPainter
    @classmethod
    def fillPainter(cls, target, size, color, roundness =0):
        """ This method must be called within a paint event. It will paint a gradient background
            on the target widget for the specified size. """

        w     = size.width()
        h     = size.height()
        brush = QtGui.QBrush(color)

        painter = QtGui.QPainter(target)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        if roundness > 0:
            painter.drawRoundedRect(0, 0, w, h, roundness, roundness)
        else:
            painter.drawRect(0, 0, w, h)
        painter.end()

#___________________________________________________________________________________________________ createIcon
    @classmethod
    def createIcon(cls, iconsPath):
        """ Creates a window icon from a path, adding the standard icon sizes for multiple
            operating systems. """

        if not os.path.exists(iconsPath):
            return None

        iconsPath = FileUtils.cleanupPath(iconsPath, isDir=True)
        icon      = QtGui.QIcon()
        sizes     = [512, 256, 180, 128, 96, 72, 64, 48, 32, 24, 16]
        for size in sizes:
            path = FileUtils.createPath(iconsPath, str(size) + '.png', isFile=True)
            if os.path.exists(path):
                icon.addFile(path)
        return icon

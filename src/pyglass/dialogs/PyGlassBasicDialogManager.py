# PyGlassBasicDialogManager.py
# (C)2012-2014
# Scott Ernst

import os

from PySide import QtCore
from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ PyGlassBasicDialogManager
class PyGlassBasicDialogManager(QtCore.QObject):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ openAbout
    @classmethod
    def openAbout(cls, parent, title, text, windowTitle ='About'):
        return cls._showMessageDialg(
            parent=parent,
            title=windowTitle,
            label=title,
            message=text,
            buttons=QtGui.QMessageBox.Ok,
            defaultButton=QtGui.QMessageBox.Ok)

#___________________________________________________________________________________________________ openYesNo
    @classmethod
    def openYesNo(cls, parent, header, message =None, defaultToYes =True, windowTitle ='Confirm?'):
        result = cls._showMessageDialg(
            parent=parent,
            title=windowTitle,
            label=header,
            message=message,
            buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            defaultButton=QtGui.QMessageBox.Yes if defaultToYes else QtGui.QMessageBox.No)
        return result == QtGui.QMessageBox.Yes

#___________________________________________________________________________________________________ openOk
    @classmethod
    def openOk(cls, parent, header, message =None, windowTitle =None):
        cls._showMessageDialg(
            parent=parent,
            title=windowTitle,
            label=header,
            message=message,
            buttons=QtGui.QMessageBox.Ok,
            defaultButton=QtGui.QMessageBox.Ok)
        return True

#___________________________________________________________________________________________________ openTextQuery
    @classmethod
    def openTextQuery(cls, parent, header, message =None, defaultText =None):
        """ Opens a text query dialog. If the dialog was canceled the method returns None,
            otherwise it returns the string set by the user. """

        if defaultText is None:
            defaultText = u''
        result = QtGui.QInputDialog.getText(parent, header, message, text=defaultText)
        if not result[-1]:
            return None
        return result[0]

#___________________________________________________________________________________________________ browseForDirectory
    @classmethod
    def browseForDirectory(cls, parent, caption =None, defaultPath =None):
        out = QtGui.QFileDialog.getExistingDirectory(
            parent,
            caption=caption if caption else u'Select a Directory',
            dir=defaultPath if defaultPath else os.path.expanduser('~'))

        if not out:
            return out
        return FileUtils.cleanupPath(out, isDir=True)

#___________________________________________________________________________________________________ browseForFileOpen
    @classmethod
    def browseForFileOpen(cls, parent, caption =None, defaultPath =None):
        out = QtGui.QFileDialog.getOpenFileName(
            parent,
            caption=caption if caption else u'Select a File',
            dir=defaultPath if defaultPath else os.path.expanduser('~'))

        if not out or not out[0]:
            return out
        return FileUtils.cleanupPath(out[0], isFile=True)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _showMessageDialg
    @classmethod
    def _showMessageDialg(cls, parent, title, label, message, buttons, defaultButton):
        dlg = QtGui.QMessageBox(parent)
        dlg.setWindowTitle(title)
        dlg.setText(label)
        if message:
            dlg.setInformativeText(message)

        dlg.setStandardButtons(buttons)
        dlg.setDefaultButton(defaultButton)

        return dlg.exec_()

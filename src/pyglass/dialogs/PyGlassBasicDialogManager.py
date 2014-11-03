# PyGlassBasicDialogManager.py
# (C)2012-2014
# Scott Ernst

from collections import namedtuple
import os

from PySide import QtCore
from PySide import QtGui

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ PyGlassBasicDialogManager
class PyGlassBasicDialogManager(QtCore.QObject):

#===================================================================================================
#                                                                                       C L A S S

    FILE_FILTER_DEFINITION = namedtuple('FILE_FILTER_DEFINITION', ['label', 'extensions'])

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
            return None
        return FileUtils.cleanupPath(out, isDir=True)

#___________________________________________________________________________________________________ browseForFileOpen
    @classmethod
    def browseForFileOpen(cls, parent, caption =None, defaultPath =None, allowMultiple =False, filterDefs =None):
        QFD = QtGui.QFileDialog
        f = QFD.getOpenFileNames if allowMultiple else QFD.getOpenFileName
        out = f(
            parent,
            caption=caption if caption else u'Select a File',
            dir=defaultPath if defaultPath else os.path.expanduser('~'),
            filter=cls.getFileFilterString(filterDefs))

        if not out or not out[0]:
            return None

        if not allowMultiple:
            return FileUtils.cleanupPath(out[0], isFile=True)

        items = []
        for item in out[0]:
            items.append(FileUtils.cleanupPath(item, isFile=True))
        return items

#___________________________________________________________________________________________________ browseForFileSave
    @classmethod
    def browseForFileSave(cls, parent, caption =None, defaultPath =None, filterDefs =None):
        out = QtGui.QFileDialog.getSaveFileName(
            parent,
            caption=caption if caption else u'Specify File',
            dir=defaultPath if defaultPath else os.path.expanduser('~'),
            options=QtGui.QFileDialog.AnyFile,
            filter=cls.getFileFilterString(filterDefs))

        if not out or not out[0]:
            return None
        return FileUtils.cleanupPath(out[0], isFile=True)

#___________________________________________________________________________________________________ getFileFilterString
    @classmethod
    def getFileFilterString(cls, filterDefs =None):
        """getFileFilterString doc..."""
        if not filterDefs:
            return None

        if isinstance(filterDefs, cls.FILE_FILTER_DEFINITION):
            filterDefs = [filterDefs]

        out = []
        for fd in filterDefs:
            result = cls._makeFilterString(fd)
            if result:
               out.append(result)

        return ';;'.join(out)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _makeFilterString
    @classmethod
    def _makeFilterString(cls, filterDef):
        """_makeFilterString doc..."""
        extensions = filterDef.extensions
        if not extensions:
            return None
        elif not isinstance(extensions, (list, tuple)):
            extensions = [extensions]

        for i in range(len(extensions)):
            extensions[i] = unicode(extensions[i]).strip('.*')

        label = filterDef.label
        if not label:
            label = u'Files'

        return u'%s (*.%s)' % (label, ' *.'.join(extensions))

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

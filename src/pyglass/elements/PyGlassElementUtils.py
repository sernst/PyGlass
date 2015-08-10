# PyGlassElementUtils.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import functools

from PySide import QtCore
from PySide import QtGui

#___________________________________________________________________________________________________ PyGlassElementUtils
class PyGlassElementUtils(object):
    """A static class"""

#===================================================================================================
#                                                                                       C L A S S

    CURSOR_END       = 'end'
    CURSOR_LAST_LINE = 'lastLine'

#___________________________________________________________________________________________________ moveTextEditCursor
    @classmethod
    def moveTextEditCursor(cls, textEdit, mode):
        if mode == cls.CURSOR_END:
            textEdit.moveCursor(QtGui.QTextCursor.End)
        elif mode == cls.CURSOR_LAST_LINE:
            textEdit.moveCursor(QtGui.QTextCursor.End)
            textEdit.moveCursor(QtGui.QTextCursor.StartOfLine)

#___________________________________________________________________________________________________ setCheckState
    @classmethod
    def setCheckState(cls, target, value =None):
        """ Updates the specified checkbox with to the checked state specified by the value. The
            default value of None leaves the checkbox state unchanged. """

        if value is not None:
            target.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

#___________________________________________________________________________________________________ registerCheckBox
    @classmethod
    def registerCheckBox(
            cls, owner, target, value =None, changedCallback =None, configSetting =None,
            saveToConfigOnChange =None):
        """ Registers a checkbox with the specified value and to signal the specified
            changedCallback function when the value of the checkbox changes. If the configSetting
            value is set instead of the value, the value is retrieved from the
            MainWindow.appConfig. """

        if value is None and configSetting is not None:
            value = owner.mainWindow.appConfig.get(configSetting)
        cls.setCheckState(target, value)

        if saveToConfigOnChange is None:
            saveToConfigOnChange = configSetting is not None

        if changedCallback is None and not saveToConfigOnChange:
            return

        callback = functools.partial(
            cls._handleCheckStateChanged,
            owner=owner,
            configSetting=configSetting if saveToConfigOnChange else None,
            target=target,
            callback=changedCallback)
        target.stateChanged.connect(callback)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCheckStateChanged
    @classmethod
    def _handleCheckStateChanged(cls, state, owner, configSetting, target, callback):
        if configSetting and owner:
            owner.mainWindow.appConfig.set(configSetting, target.isChecked())

        if callback is not None:
            try:
                callback(target, state)
            except TypeError as err:
                print(
                    '[ERROR]: Incorrect arguments in "%s"'
                    % callback.__name__)
                raise

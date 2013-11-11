# PyGlassElementUtils.py
# (C)2013
# Scott Ernst

import functools

from PySide import QtCore

from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils

#___________________________________________________________________________________________________ PyGlassElementUtils
class PyGlassElementUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

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
            callback(target, state)

# ApplicationConfig.py
# (C)2012-2013
# Scott Ernst

from pyaid.config.SettingsConfig import SettingsConfig
from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ ApplicationConfig
class ApplicationConfig(SettingsConfig):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _APP_CONFIG_FILENAME        = 'app_settings.vcd'
    _APP_COMMON_CONFIG_FILENAME = 'app_common_settings.vcd'

#___________________________________________________________________________________________________ __init__
    def __init__(self, applicationGui, common =False, pretty =False):
        """Creates a new instance of ApplicationConfig."""
        self._gui    = applicationGui
        self._common = common
        super(ApplicationConfig, self).__init__(self.path, pretty)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: common
    @property
    def common(self):
        return self._common

#___________________________________________________________________________________________________ GS: path
    @property
    def path(self):
        if self._common:
            return FileUtils.createPath(
                self._gui.appResourcePath,
                ApplicationConfig._APP_COMMON_CONFIG_FILENAME)

        return FileUtils.createPath(
            self._gui.localAppResourcePath,
            ApplicationConfig._APP_CONFIG_FILENAME)

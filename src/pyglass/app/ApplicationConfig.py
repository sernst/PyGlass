# ApplicationConfig.py
# (C)2012-2013
# Scott Ernst

import os

from pyaid.NullUtils import NullUtils
from pyaid.file.FileUtils import FileUtils
from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ ApplicationConfig
class ApplicationConfig(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _APP_CONFIG_FILENAME        = 'app_settings.vcd'
    _APP_COMMON_CONFIG_FILENAME = 'app_common_settings.vcd'

#___________________________________________________________________________________________________ __init__
    def __init__(self, applicationGui, common =False):
        """Creates a new instance of ApplicationConfig."""
        self._gui      = applicationGui
        self._settings = None
        self._common   = common

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
                ApplicationConfig._APP_COMMON_CONFIG_FILENAME
            )

        return FileUtils.createPath(
            self._gui.localAppResourcePath,
            ApplicationConfig._APP_CONFIG_FILENAME
        )

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ get
    def get(self, key, defaultValue =None):
        self._loadSettings()
        if not key:
            return self._settings

        if isinstance(key, basestring):
            key = [key]
        value = self._settings
        for k in key:
            if k in value:
                value = value[k]
            else:
                return defaultValue

        return value

#___________________________________________________________________________________________________ set
    def set(self, key, value):
        self._loadSettings()
        self._updateSetting(key, value)
        self._saveSettings()

#___________________________________________________________________________________________________ setFromDict
    def setFromDict(self, keysAndValues):
        if not keysAndValues:
            return

        self._loadSettings()
        for key, value in keysAndValues.iteritems():
            self._updateSetting(key, value)
        self._saveSettings()

#___________________________________________________________________________________________________ remove
    def remove(self, key):
        nullTest = NullUtils.NULL('REMOVE_TEST_NULL')
        value    = self.get(key, nullTest)
        if value is nullTest:
            return True

        if isinstance(key, basestring):
            key = [key]
        value = self._settings
        for k in key[:-1]:
            if k in value:
                value = value[k]
            else:
                return True
        del value[key[-1]]

        self._cleanupSettings()
        self._saveSettings()
        return True

#___________________________________________________________________________________________________ refresh
    def refresh(self):
        """Doc..."""
        self._settings = None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _updateSetting
    def _updateSetting(self, key, value):
        if isinstance(key, basestring):
            key = [key]

        src = self._settings
        for k in key[:-1]:
            if k not in src:
                src[k] = dict()
            src = src[k]
        src[key[-1]] = value

#___________________________________________________________________________________________________ _cleanupSettings
    def _cleanupSettings(self, target =None):
        if not target:
            target = self._settings

        for n,v in target.iteritems():
            if isinstance(v, dict):
                self._cleanupSettings(target=v)
                if not v:
                    del target[n]
        return True

#___________________________________________________________________________________________________ _saveSettings
    def _saveSettings(self):
        if self._settings is None:
            return

        try:
            f = open(self.path, 'w+')
            f.write(JSON.asString(self._settings))
            f.close()
        except Exception, err:
            print 'ERROR: Unable to save application settings file: ' + self.path
            return False

        return True

#___________________________________________________________________________________________________ _loadSettings
    def _loadSettings(self):
        """Doc..."""
        if self._settings is not None:
            return self._settings

        if not os.path.exists(self.path):
            self._settings = dict()
            return self._settings

        try:
            f   = open(self.path, 'r+')
            res = f.read()
            f.close()
        except Exception, err:
            print 'ERROR: Unable to load applications setting file: ' + self.path
            self._settings = dict()
            return self._settings

        try:
            self._settings = JSON.fromString(res)
        except Exception, err:
            print 'ERROR: Unable to parse applications setting file: ' + self.path
            self._settings.dict()
            return self._settings

        return self._settings

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

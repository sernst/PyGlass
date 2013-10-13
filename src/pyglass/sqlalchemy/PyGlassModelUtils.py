# PyGlassModelUtils.py
# (C)2012-2013
# Scott Ernst

import os
import re
import zipfile

from pyaid.debug.Logger import Logger
from pyaid.decorators.ClassGetter import ClassGetter

#AS NEEDED: pyglass.alembic.AlembicUtils import AlembicUtils
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ ModelUtils
class PyGlassModelUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ZIP_FIND = os.sep + 'library.zip' + os.sep

    _logger = Logger('SQLAlchemyModels')

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ logger
    @ClassGetter
    def logger(cls):
        return cls._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ modelsInit
    @classmethod
    def modelsInit(cls, initPath, initName):
        out = dict()
        zipIndex = initPath[0].find(PyGlassModelUtils._ZIP_FIND)
        if  zipIndex == -1:
            moduleList = os.listdir(initPath[0])
        else:
            splitIndex = zipIndex+len(PyGlassModelUtils._ZIP_FIND)
            zipPath    = initPath[0][:splitIndex-1]
            modulePath = initPath[0][splitIndex:]
            z          = zipfile.ZipFile(zipPath)
            moduleList = []
            for item in z.namelist():
                item = os.sep.join(item.split('/'))
                if item.startswith(modulePath):
                    moduleList.append(item.rsplit(os.sep, 1)[-1])

        items = []
        for module in moduleList:
            if module.startswith('__init__.py') or module.find('_') == -1:
                continue

            parts    = module.rsplit('.', 1)
            parts[0] = parts[0].rsplit(os.sep, 1)[-1]
            if not parts[-1].startswith('py') or parts[0] in items:
                continue
            items.append(parts[0])

            m = None
            n = None
            r = None
            c = None
            try:
                n = module.rsplit('.', 1)[0]
                m = initName + '.' + n
                r = __import__(m, locals(), globals(), [n])
                c = getattr(r, n)
                out[n] = c
                if not c.__table__.exists(c.ENGINE):
                    c.__table__.create(c.ENGINE, True)

                    from pyglass.alembic.AlembicUtils import AlembicUtils
                    if AlembicUtils.hasAlembic:
                        AlembicUtils.stampDatabase(c.DATABASE_URL)
                        cls._logger.write(
                            u'CREATED: ' + unicode(c) + u' ' + unicode(c.__table__)
                            + u' [STAMPED head]'
                        )
            except Exception, err:
                cls._logger.writeError([
                    u'MODEL INITIALIZATION FAILURE:',
                    u'INIT PATH: ' + unicode(initPath),
                    u'INIT NAME: ' + unicode(initName),
                    u'MODULE IMPORT: ' + unicode(m),
                    u'IMPORT CLASS: ' + unicode(n),
                    u'IMPORT RESULT: ' + unicode(r),
                    u'CLASS RESULT: ' + unicode(c)
                ], err)

        return out

#___________________________________________________________________________________________________ getMigrationPathFromDatabaseUrl
    @classmethod
    def getMigrationPathFromDatabaseUrl(cls, databaseUrl, root =False):
        urlParts = databaseUrl.split(u'://')
        if urlParts[0].lower() == u'shared':
            path = [u'shared', u'migration']
        else:
            path = [u'apps', urlParts[0], u'migration']

        if not root:
            path += urlParts[-1].split(u'/')

            # Remove the extension
            if path[-1].endswith(u'.vdb'):
                path[-1] = path[-1][:-4]

        return PyGlassEnvironment.getResourcePath(*path)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromDatabaseUrl(cls, databaseUrl):
        urlParts = databaseUrl.split(u'://')

        # Determine the sqlite database path
        if urlParts[0].lower() == u'shared':
            path = [u'shared', u'data']
        else:
            path = [u'apps', urlParts[0], u'data']

        path += urlParts[1].strip(u'/').split(u'/')
        if not path[-1].endswith(u'.vdb'):
            path[-1] += u'.vdb'

        return PyGlassEnvironment.getRootLocalResourcePath(*path)

#___________________________________________________________________________________________________ getPathFromDatabaseUrl
    @classmethod
    def getPathFromEngineUrl(cls, engineUrl):
        out = engineUrl.split(u'://')[-1]
        if PyGlassEnvironment.isWindows and re.compile('^/.{1}:').match(out):
            return out[1:]
        else:
            return u'/' + out
        return out

#___________________________________________________________________________________________________ getEngineUrl
    @classmethod
    def getEngineUrl(cls, databaseUrl):
        databasePath = cls.getPathFromDatabaseUrl(databaseUrl)

        d = os.path.dirname(databasePath)
        if not os.path.exists(d):
            os.makedirs(d)

        # Windows compatibility requires an additional slash before the drive letter to conform
        # to a unix type root path.
        if not databasePath.startswith(u'/'):
            databasePath = u'/' + databasePath

        return u'sqlite://' + databasePath

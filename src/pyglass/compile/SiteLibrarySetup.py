# SiteLibrarySetup.py
# (C)2013
# Scott Ernst

import sys
import os
from collections import namedtuple

from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum

_EXTERNAL_SOURCE_NT = namedtuple('EXTERNAL_SOURCE_NT', ['id', 'packages', 'includes', 'dataFiles'])

#---------------------------------------------------------------------------------------------------
# PySide Data File Generation
pySideDataFiles = []
pluginsPath     = os.path.join(sys.exec_prefix, 'Lib', 'site-packages', 'PySide', 'plugins')

for item in os.listdir(pluginsPath):
    itemPath = os.path.join(pluginsPath, item)
    items    = []
    for f in os.listdir(itemPath):
        fpath = os.path.join(itemPath, f)
        if os.path.isfile(fpath):
            items.append(fpath)
    pySideDataFiles.append((item, items))

#___________________________________________________________________________________________________ LIBRARY_INCLUDES
class LIBRARY_INCLUDES(object):

#===================================================================================================
#                                                                                     P U B L I C

    COMMON = _EXTERNAL_SOURCE_NT(
        id=SiteLibraryEnum.COMMON,
        packages=['lxml','logging.config'],
        includes=['_ssl'],
        dataFiles=[]
    )

    SQL_ALCHEMY = _EXTERNAL_SOURCE_NT(
        id=SiteLibraryEnum.SQL_ALCHEMY,
        packages=[
            'sqlalchemy.databases',
            'sqlalchemy.util.queue',
            'sqlalchemy.testing'
        ],
        includes=[],
        dataFiles=[]
    )

    PYSIDE = _EXTERNAL_SOURCE_NT(
        id=SiteLibraryEnum.PYSIDE,
        packages=[],
        includes=[
            'PySide.QtXml',
            'PySide.QtXmlPatterns',
            'PySide.QtTest',
            'PySide.QtSvg',
            'PySide.QtWebKit',
            'PySide.QtSql',
            'PySide.QtOpenGL',
            'PySide.QtNetwork',
            'PySide.QtGui',
            'PySide.QtCore',
            'PySide.QtUiTools',
            'PySide.QtScriptTools',
            'PySide.QtMultimedia',
            'PySide.QtHelp',
            'PySide.QtDeclarative',
            'PySide.QtScript'
        ],
        dataFiles=pySideDataFiles
    )

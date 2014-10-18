# TextureAtlas.py
# (C)2014
# Scott Ernst

from xml.dom import minidom
from collections import namedtuple

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils

from pyglass.elements.icons.IconElement import IconElement

#___________________________________________________________________________________________________ TextureAtlas
class TextureAtlas(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TEXTURE_ATLAS_ENTRY = namedtuple(
        'TEXTURE_ATLAS_ENTRY',
        ['name', 'x', 'y', 'width', 'height', 'frameX', 'frameY', 'frameWidth', 'frameHeight'])

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, name, texturePath =None, definitionPath =None, **kwargs):
        """Creates a new instance of TextureAtlas."""
        self.name            = name
        self._texturePath    = texturePath
        self._definitionPath = definitionPath
        self._texture        = ArgsUtils.get('texture', None, kwargs)
        self._image          = None
        self._bitmap         = None
        self._definition     = ArgsUtils.get('definition', None, kwargs)

        self._mainWindow     = None
        self._parent         = None
        self.parent          = parent

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: parent
    @property
    def parent(self):
        return None
    @parent.setter
    def parent(self, value):
        if self._parent == value:
            return
        self._parent = value
        self._mainWindow = None

#___________________________________________________________________________________________________ GS: mainWindow
    @property
    def mainWindow(self):
        if self._mainWindow:
            return self._mainWindow

        parent = self.parent
        while parent is not None:
            try:
                if parent.isMainWindow:
                    self._mainWindow = parent
                    return self._mainWindow
            except Exception, err:
                pass
            parent = parent.parent()

#___________________________________________________________________________________________________ GS: definition
    @property
    def definition(self):
        if not self._definition and self._definitionPath:
            self._definition = self._getDefinitionFile(self._definitionPath)
        return self._definition

#___________________________________________________________________________________________________ GS: propertyName
    @property
    def image(self):
        if self._image is None:
            self._image = self._getImageFile(self._texturePath)
        return self._image

#___________________________________________________________________________________________________ GS: bitmap
    @property
    def bitmap(self):
        if not self._bitmap:
            self._bitmap = QtGui.QBitmap.fromImage(self.image)
        return self._bitmap

#___________________________________________________________________________________________________ GS: texture
    @property
    def texture(self):
        if not self._texture and self._texturePath:
            self._texture = self._getTextureFile(self._texturePath)
        return self._texture

#___________________________________________________________________________________________________ GS: texturePath
    @property
    def texturePath(self):
        return self._texturePath
    @texturePath.setter
    def texturePath(self, value):
        if self._texturePath == value:
            return
        self._texturePath = value

#___________________________________________________________________________________________________ GS: definitionPath
    @property
    def definitionPath(self):
        return self._definitionPath
    @definitionPath.setter
    def definitionPath(self, value):
        if self._definitionPath == value:
            return
        self._definitionPath = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ load
    def load(self):
        d = self.definition
        t = self.texture
        return True

#___________________________________________________________________________________________________ getDefinition
    def getDefinition(self, name):
        d = self.definition
        if name in d:
            return d[name]
        return None

#___________________________________________________________________________________________________ getIcon
    def getIcon(self, parent, name, **kwargs):
        """Doc..."""
        return IconElement(parent=parent, name=name, atlas=self, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _getImageFile
    @classmethod
    def _getImageFile(cls, path):
        img = QtGui.QImage()
        img.load(path)
        return img

#___________________________________________________________________________________________________ _getTexture
    @classmethod
    def _getTextureFile(cls, path):
        """Doc..."""
        pix = QtGui.QPixmap()
        pix.load(path)
        return pix

#___________________________________________________________________________________________________ _getDefinition
    @classmethod
    def _getDefinitionFile(cls, path):
        out = dict()
        xmlDom = minidom.parse(path)
        for entry in xmlDom.documentElement.getElementsByTagName('SubTexture'):
            name        = entry.getAttribute('name')
            x           = int(entry.getAttribute('x'))
            y           = int(entry.getAttribute('y'))
            width       = int(entry.getAttribute('width'))
            height      = int(entry.getAttribute('height'))

            try:
                frameX = int(entry.getAttribute('frameX'))
            except Exception, err:
                frameX = 0

            try:
                frameY = int(entry.getAttribute('frameY'))
            except Exception, err:
                frameY = 0

            try:
                frameWidth = int(entry.getAttribute('frameWidth'))
            except Exception, err:
                frameWidth = width

            try:
                frameHeight = int(entry.getAttribute('frameHeight'))
            except Exception, err:
                frameHeight = height

            out[name] = cls.TEXTURE_ATLAS_ENTRY(
                name=name, x=x, y=y, width=width, height=height, frameX=frameX, frameY=frameY,
                frameWidth=frameWidth, frameHeight=frameHeight)

        return out

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


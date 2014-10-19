# TextureAtlasManager.py
# (C)2014
# Scott Ernst

from collections import namedtuple

from pyglass.elements.icons.TextureAtlas import TextureAtlas

#___________________________________________________________________________________________________ TextureAtlasManager
class TextureAtlasManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TEXTURE_BUNDLE = namedtuple('TEXTURE_BUNDLE', ['atlas', 'icon'])

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent):
        """Creates a new instance of TextureAtlasManager."""
        self._atlases = dict()

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: atlases
    @property
    def atlases(self):
        return self._atlases

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ create
    def create(self, name, texturePath, definitionPath, parent =None, **kwargs):
        atlas = TextureAtlas(
            parent=parent,
            name=name,
            texturePath=texturePath,
            definitionPath=definitionPath, **kwargs)
        self.add(name, atlas)
        return atlas

#___________________________________________________________________________________________________ addAtlas
    def add(self, name, atlas):
        self._atlases[name] = atlas

#___________________________________________________________________________________________________ getBundle
    def getBundle(self, atlasName, iconName):
        """getBundle doc..."""
        return self.TEXTURE_BUNDLE(self.get(atlasName), iconName)

#___________________________________________________________________________________________________ get
    def get(self, name):
        """Doc..."""
        if name in self._atlases:
            return self._atlases[name]
        return None

#___________________________________________________________________________________________________ remove
    def remove(self, name):
        if not name in self._atlases:
            return
        del self._atlases[name]

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


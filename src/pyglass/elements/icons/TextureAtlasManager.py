# TextureAtlasManager.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.string.StringUtils import StringUtils

from pyglass.elements.icons.TextureAtlas import TextureAtlas

#___________________________________________________________________________________________________ TextureAtlasManager
class TextureAtlasManager(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self):
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

#___________________________________________________________________________________________________ add
    def add(self, name, atlas):
        self._atlases[name] = atlas

#___________________________________________________________________________________________________ getDefinition
    def getDefinition(self, name):
        """getDefinition doc..."""
        parts = name.split(':')
        if len(parts) != 2 or not parts[0] in self._atlases:
            return None
        return self._atlases[parts[0]].getDefinition(parts[1])

#___________________________________________________________________________________________________ getAtlas
    def getAtlas(self, name):
        """getAtlas doc..."""
        if not name:
            return None
        return self.get(name.split(':')[0])

#___________________________________________________________________________________________________ get
    def get(self, name, parent =None):
        """Doc..."""
        if not name:
            return None

        parts = name.split(':')
        if len(parts) == 1 and name in self._atlases:
            return self._atlases[name]
        elif len(parts) == 2 and parts[0] in self._atlases:
            return self._atlases[parts[0]].getIcon(parts[1], parent=parent)
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
        return StringUtils.toUnicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


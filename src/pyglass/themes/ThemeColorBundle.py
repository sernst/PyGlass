# ThemeColorBundle.py
# (C)2013
# Scott Ernst

from pyglass.themes.ColorQValue import ColorQValue

#___________________________________________________________________________________________________ ThemeColorBundle
class ThemeColorBundle(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, colorScheme):
        """Creates a new instance of ThemeColorBundle."""
        self._scheme = colorScheme
        self._strong = ColorQValue(colorScheme[0])
        self._weak   = ColorQValue(colorScheme[1])
        self._lightBackground = ColorQValue(colorScheme[2])
        self._darkBackground  = ColorQValue(colorScheme[3])

        self._colors = (self._strong, self._weak, self._lightBackground, self._darkBackground)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: strong
    @property
    def strong(self):
        return self._strong

#___________________________________________________________________________________________________ GS: weak
    @property
    def weak(self):
        return self._weak

#___________________________________________________________________________________________________ GS: light
    @property
    def light(self):
        return self._lightBackground

#___________________________________________________________________________________________________ GS: dark
    @property
    def dark(self):
        return self._darkBackground

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ clone
    def clone(self, invert =False):
        if invert:
            scheme = list(self._scheme) + []
            scheme.reverse()
        else:
            scheme = self._scheme
        return ThemeColorBundle(scheme)

#___________________________________________________________________________________________________ hsvShift
    def hsvShift(self, **kwargs):
        for color in self._colors:
            color.hsvShift(**kwargs)

#___________________________________________________________________________________________________ opacityShift
    def opacityShift(self, opacityDelta):
        for color in self._colors:
            color.opacity = min(1.0, max(0.0, color.opacity + opacityDelta))

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


# StyledLabel.py
# (C)2014
# Scott Ernst

from PySide import QtGui

from pyaid.ArgsUtils import ArgsUtils
from pyglass.themes.ColorQValue import ColorQValue

#___________________________________________________________________________________________________ StyledLabel
class StyledLabel(QtGui.QLabel):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    BORDER      = 'border: 0px solid black'
    FONT_FAMILY = 'font-family:%s'
    FONT_SIZE   = 'font-size:%spx'
    COLOR       = 'color: rgba(%s, %s, %s, %s%%)'
    FONT_WEIGHT = 'font-weight:%s'
    ITALIC_FONT = 'font-style:italic'

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent =None, *args, **kwargs):
        """Creates a new instance of StyledLabel."""
        self._fontFamily    = ArgsUtils.extract('fontFamily', None, kwargs)
        self._fontSize      = ArgsUtils.extract('fontSize', None, kwargs)
        self._color         = ArgsUtils.extract('color', None, kwargs)
        self._fontWeight    = ArgsUtils.extract('fontWeight', None, kwargs)
        self._isItalic      = ArgsUtils.extract('isItalic', None, kwargs)
        self._isBold        = ArgsUtils.extract('isBold', None, kwargs)
        self._isBorderless  = ArgsUtils.extract('isBorderless', True, kwargs)
        super(StyledLabel, self).__init__(parent, *args, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: fontSize
    @property
    def fontSize(self):
        return self._fontSize
    @fontSize.setter
    def fontSize(self, value):
        if self._fontSize == value:
            return
        self._fontSize = value
        self._update()

#___________________________________________________________________________________________________ GS: color
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if value is None:
            if self._color is None:
                return
            self._color = None
            self._update()
            return

        c = self._color
        if isinstance(value, QtGui.QColor):
            self._color = value
        else:
            self._color = ColorQValue(value).qColor

        if not ColorQValue.compareQColors(value, c):
            self._update()

#___________________________________________________________________________________________________ GS: isItalic
    @property
    def isItalic(self):
        return self._isItalic
    @isItalic.setter
    def isItalic(self, value):
        if self._isItalic == value:
            return
        self._isItalic = value
        self._update()

#___________________________________________________________________________________________________ GS: fontFamily
    @property
    def fontFamily(self):
        return self._fontFamily
    @fontFamily.setter
    def fontFamily(self, value):
        if self._fontFamily == value:
            return
        self._fontFamily = value
        self._update()

#___________________________________________________________________________________________________ GS: isBold
    @property
    def isBold(self):
        return self._isBold
    @isBold.setter
    def isBold(self, value):
        if self._isBold == value:
            return
        self._isBold = value
        self._update()

#___________________________________________________________________________________________________ GS: fontWeight
    @property
    def fontWeight(self):
        return self._fontWeight
    @fontWeight.setter
    def fontWeight(self, value):
        if self._fontWeight == value:
            return
        self._fontWeight = value
        self._update()

#___________________________________________________________________________________________________ GS: isBorderless
    @property
    def isBorderless(self):
        return self._isBorderless
    @isBorderless.setter
    def isBorderless(self, value):
        if self._isBorderless == value:
            return
        self._isBorderless = value
        self._update()

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ updateStyles
    def updateStyles(
            self, fontFamily =None, fontSize =None, color =None, fontWeight =None, isBold =None,
            isItalic =None, isBorderless =None
    ):
        """updateStyle doc..."""
        if fontFamily:
            self._fontFamily = fontFamily
        if fontSize:
            self._fontSize = fontSize
        if fontWeight:
            self._fontWeight = fontWeight
        if isBold is not None:
            self._isBold = isBold
        if isItalic is not None:
            self._isItalic = isItalic
        if isBorderless is not None:
            self._isBorderless = isBorderless

        if color:
            self._color = ColorQValue.getAsQColor(color)
        self._update()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _update
    def _update(self):
        """_update doc..."""
        items = []

        if self.isBorderless:
            items.append(self.BORDER)

        if self.fontFamily:
            items.append(self.FONT_FAMILY % self.fontFamily)

        if self.fontSize:
            items.append(self.FONT_SIZE % int(self.fontSize))

        if self.fontWeight:
            items.append(self.FONT_WEIGHT % int(self.fontWeight))
        elif self.isBold:
            items.append(self.FONT_WEIGHT % 'bold')
        else:
            items.append(self.FONT_WEIGHT % 'normal')

        if self.isItalic:
            items.append(self.ITALIC_FONT)

        if self.color:
            c = self.color
            items.append(self.COLOR % (c.red(), c.green(), c.blue(), int(round(100.0*c.alphaF()))))

        if not items:
            self.setStyleSheet(None)
            return

        css = '; '.join(items)
        self.setStyleSheet(css)

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


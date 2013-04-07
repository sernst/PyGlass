# InteractiveButtonBase.py
# (C)2013
# Scott Ernst

from pyglass.elements.InteractiveElement import InteractiveElement

#___________________________________________________________________________________________________ InteractiveButtonBase
class InteractiveButtonBase(InteractiveElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, toggles =False, clickOn =False, **kwargs):
        """Creates a new instance of InteractiveButtonBase."""
        super(InteractiveButtonBase, self).__init__(
            parent=parent, toggles=toggles, clickOn=clickOn, **kwargs
        )

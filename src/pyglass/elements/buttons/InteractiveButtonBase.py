# InteractiveButtonBase.py
# (C)2013-2014
# Scott Ernst

from pyglass.elements.InteractiveElement import InteractiveElement
from pyglass.enum.InteractionStatesEnum import InteractionStatesEnum

#___________________________________________________________________________________________________ InteractiveButtonBase
class InteractiveButtonBase(InteractiveElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, toggles =False, clickOn =False, **kwargs):
        """Creates a new instance of InteractiveButtonBase."""
        super(InteractiveButtonBase, self).__init__(
            parent=parent, toggles=toggles, clickOn=clickOn, **kwargs)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getInteractionState
    def getInteractionState(self):
        if not self.isEnabled():
            return InteractionStatesEnum.DISABLED_MODE
        elif self.checked:
            return InteractionStatesEnum.SELECTED_MODE
        return self._mode

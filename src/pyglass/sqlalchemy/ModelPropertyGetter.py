# ModelPropertyGetter.py
# (C)2012
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.sqlalchemy.ModelProperty import ModelProperty

#___________________________________________________________________________________________________ ModelPropertyGetter
class ModelPropertyGetter(ModelProperty):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedSelf):
        return getattr(wrappedSelf, self._name)

# ModelPropertyExpression.py
# (C)2012
# Eric David Wills and Scott Ernst

from pyglass.sqlalchemy.ModelProperty import ModelProperty

#___________________________________________________________________________________________________ ModelPropertyExpression
class ModelPropertyExpression(ModelProperty):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedCls):
        return getattr(wrappedCls, self._name)

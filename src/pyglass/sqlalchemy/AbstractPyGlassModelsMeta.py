# AbstractPyGlassModelsMeta.py
# (C)2012-2014
# Scott Ernst and Eric David Wills

from __future__ import print_function, absolute_import, unicode_literals, division

from sqlalchemy import Column
from sqlalchemy import orm
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.hybrid import hybrid_property

from pyaid.debug.Logger import Logger

from pyglass.sqlalchemy.ExternalKeyProperty import ExternalKeyProperty
from pyglass.sqlalchemy.ModelPropertyExpression import ModelPropertyExpression
from pyglass.sqlalchemy.ModelPropertyGetter import ModelPropertyGetter
from pyglass.sqlalchemy.ModelPropertySetter import ModelPropertySetter
# AS NEEDED: from pyglass.sqlalchemy.ConcretePyGlassModelsMeta import ConcretePyGlassModelsMeta

#___________________________________________________________________________________________________ AbstractPyGlassModelsMeta
class AbstractPyGlassModelsMeta(DeclarativeMeta):

#===================================================================================================
#                                                                                       C L A S S

    _registry = dict()
    _logger   = Logger('Models')

#___________________________________________________________________________________________________ __new__
    def __new__(cls, name, bases, attrs):
        for n, v in attrs.items():
            attrName = n[1:]
            if isinstance(v, Column) and n.startswith('_') and not attrs.has_key(attrName):
                v.key  = attrName
                v.name = attrName

                # Add dynamic property
                attrs[attrName] = hybrid_property(
                    ModelPropertyGetter(n),
                    ModelPropertySetter(n),
                    None,
                    ModelPropertyExpression(n))

                # Add external-key property
                info = getattr(v, 'info')
                if info and 'model' in info:
                    columnName = info['column'] if 'column' in info else 'i'
                    attrs[info['get']] = property(
                        ExternalKeyProperty(attrName, info['model'], columnName))

        return DeclarativeMeta.__new__(cls, name, bases, attrs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: MASTER
    @property
    def MASTER(cls):
        return cls.getModel()

#___________________________________________________________________________________________________ GS: _log
    @property
    def _log(cls):
        return AbstractPyGlassModelsMeta._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getModel
    def getModel(cls, modelType =None):
        this = AbstractPyGlassModelsMeta
        name = cls.__name__ + '_Master'

        if name in this._registry:
            return this._registry[name]

        # New method to be wrapped as the ORM reconstructor
        def reconstructor(self):
            self.ormInit()

        from pyglass.sqlalchemy.ConcretePyGlassModelsMeta import ConcretePyGlassModelsMeta
        this._registry[name] = ConcretePyGlassModelsMeta(
            name, (cls,), {
                '__module__':cls.__module__,
                'IS_MASTER':True,
                'ormReconstructor':orm.reconstructor(reconstructor) })

        return this._registry[name]

#___________________________________________________________________________________________________ __str__
    def __str__(cls):
        return '<ModelClass %s>' % cls.__name__

# AbstractPyGlassModelsMeta.py
# (C)2012-2013
# Scott Ernst and Eric David Wills

from sqlalchemy import Column
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

    _registry = {}
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
                    ModelPropertyExpression(n)
                )

                # Add external-key property
                info = getattr(v, 'info')
                if info and 'model' in info:
                    columnName = info['column'] if 'column' in info else 'i'
                    attrs[info['get']] = property(
                        ExternalKeyProperty(
                            attrName, info['model'], columnName
                        )
                    )

        return DeclarativeMeta.__new__(cls, name, bases, attrs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: MASTER
    @property
    def MASTER(cls):
        return cls.getModel(True)

#___________________________________________________________________________________________________ GS: _log
    @property
    def _log(cls):
        return AbstractPyGlassModelsMeta._logger

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getModel
    def getModel(cls, isMaster):
        name = cls.__name__ + '_Master'
        if name not in AbstractPyGlassModelsMeta._registry:
            attrs = {'__module__':cls.__module__, 'IS_MASTER':True}

            from pyglass.sqlalchemy.ConcretePyGlassModelsMeta import ConcretePyGlassModelsMeta
            AbstractPyGlassModelsMeta._registry[name] = ConcretePyGlassModelsMeta(name, (cls,), attrs)

        return AbstractPyGlassModelsMeta._registry[name]

#___________________________________________________________________________________________________ __str__
    def __str__(cls):
        return '<ModelClass %s>' % cls.__name__

#___________________________________________________________________________________________________ getClass
    @staticmethod
    def getClass(modelName):
        """Returns a model class based on the specified database and model names."""

        modelNameParts = modelName.split('_')
        databaseName   = modelNameParts[0].lower()
        moduleName     = 'vmi.models.' + databaseName + '.' + modelName
        res            = __import__(moduleName, globals(), locals(), [modelName])
        base           = getattr(res, modelName)
        return base.MASTER

# ConcretePyGlassModelsMeta.py
# (C)2012-2013
# Scott Ernst and Eric D. Wills

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.string.StringUtils import StringUtils
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from pyglass.sqlalchemy.SQLAlchemyResult import SQLAlchemyResult
from pyglass.sqlalchemy.AbstractPyGlassModelsMeta import AbstractPyGlassModelsMeta
from pyglass.sqlalchemy.PyGlassModelUtils import PyGlassModelUtils

#___________________________________________________________________________________________________ ConcretePyGlassModelsMeta
class ConcretePyGlassModelsMeta(AbstractPyGlassModelsMeta):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _engines = dict()

#___________________________________________________________________________________________________ __new__
    def __new__(mcs, name, bases, attrs):

        binding = ConcretePyGlassModelsMeta._engines.get(name)
        if binding is None:

            # Retrieve the database URL from the __init__.py for the package in which the model class
            # resides.
            module  = attrs['__module__']
            package = module[:module.rfind('.')]
            res     = __import__(package, globals(), locals(), ['DATABASE_URL'])

            try:
                sourceUrl = getattr(res, 'DATABASE_URL')
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'ERROR: Unable to get DATABASE_URL from %s.__init__.py' % package,
                    'NAME: ' + StringUtils.toUnicode(name) ], err)
                raise

            try:
                url = PyGlassModelUtils.getEngineUrl(sourceUrl)
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'ERROR: Unable to get url from database url',
                    'DATABASE URL: ' + StringUtils.toUnicode(sourceUrl) ], err)
                raise

            try:
                engine = create_engine(url, echo=False)
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'DATABASE FAILURE: Unable to create engine for database',
                    'URL: ' + StringUtils.toUnicode(url),
                    'NAME: ' + StringUtils.toUnicode(name)
                ], err)
                raise

            try:
                Session = scoped_session(sessionmaker(bind=engine))
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'DATABASE FAILURE: Unable to create bound Session.',
                    'URL: ' + StringUtils.toUnicode(url),
                    'ENGINE: ' + StringUtils.toUnicode(engine)
                ], err)
                raise

            try:
                Base = declarative_base(bind=engine)
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'DATABASE FAILURE: Unable to create database engine Base.',
                    'URL: ' + StringUtils.toUnicode(url),
                    'ENGINE: ' + StringUtils.toUnicode(engine)
                ], err)
                raise

            try:
                Base.metadata.create_all(engine)
            except Exception as err:
                PyGlassModelUtils.logger.writeError([
                    'DATABASE FAILURE: Unable to create models.'
                    'URL: ' + StringUtils.toUnicode(url),
                    'ENGINE: ' + StringUtils.toUnicode(engine),
                    'BASE: ' + StringUtils.toUnicode(Base)
                ], err)
                raise

            binding = {
                'engine':engine,
                'SessionClass':Session,
                'BaseClass':Base,
                'url':url,
                'databaseUrl':sourceUrl }
            ConcretePyGlassModelsMeta._engines[name] = binding

        attrs['ENGINE']        = binding['engine']
        attrs['SESSION_CLASS'] = binding['SessionClass']
        attrs['BASE']          = binding['BaseClass']
        attrs['URL']           = binding['url']
        attrs['MODEL_NAME']    = name

        attrs['DATABASE_URL']  = binding['databaseUrl']
        attrs['BINDING']       = binding

        # Add the declarative base to inheritance
        declaredBase = (binding['BaseClass'],)
        try:
            bases = bases + declaredBase
        except Exception as err:
            bases = declaredBase

        out = AbstractPyGlassModelsMeta.__new__(mcs, name, bases, attrs)
        return out

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createSession
    def createSession(cls):
        return cls.SESSION_CLASS()

#___________________________________________________________________________________________________ query
    def query(cls, session, modelFilter =None, modelOrderBy =None, limit =None, offset =None,
              joinModels =None):
        query = cls.createQuery(session)
        if joinModels is not None:
            for model in joinModels:
                query = query.join(model)

        if modelFilter is not None:
            query = query.filter(modelFilter)
        if modelOrderBy is not None:
            query = query.order_by(modelOrderBy)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return cls.createResult(query)

#___________________________________________________________________________________________________ createQuery
    def createQuery(cls, session, *args):
        try:
            return session.createQuery(*args if args else [cls])
        except Exception as err:
            ConcretePyGlassModelsMeta._logger.writeError([
                'Query Creation Failure: ' + StringUtils.toUnicode(cls.__name__)
                + '\nMETA: ' + StringUtils.toUnicode(cls.__base__.metadata)
                + '\nREGISTRY: ' + StringUtils.toUnicode(cls.__base__._decl_class_registry)
            ], err)
            raise err

#___________________________________________________________________________________________________ createResult
    def createResult(cls, query, lock =False):
        return SQLAlchemyResult(cls, query, lock)

#___________________________________________________________________________________________________ echoAll
    def echoAll(cls):
        session = cls.createSession()
        for res in session.query(cls).all():
            PyGlassModelUtils.logger.write(StringUtils.toUnicode(res))
        session.close()

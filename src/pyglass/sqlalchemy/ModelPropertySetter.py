# ModelPropertySetter.py
# (C)2012
# Eric David Wills and Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from sqlalchemy import Unicode
from sqlalchemy import UnicodeText

from pyglass.sqlalchemy.ModelProperty import ModelProperty

#___________________________________________________________________________________________________ ModelPropertySetter
class ModelPropertySetter(ModelProperty):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __call__
    def __call__(self, wrappedSelf, value):
        if isinstance(value, str):
            try:
                # Automatically decodes bytestrings to UTF-8 for storage in the database
                c = getattr(wrappedSelf.__class__, self._name).property.columns[0]
                if isinstance(c, Unicode) or isinstance(c, UnicodeText):
                    value = value.decode('utf-8')
            except Exception as err:
                pass

        setattr(wrappedSelf, self._name, value)

# RequestUtils.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from collections import namedtuple
from pyaid.string.StringUtils import StringUtils

import requests
from requests import exceptions
from requests import utils as requestUtils
from PySide import QtCore

from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#=================================================================================================== RequestUtils
class RequestUtils(QtCore.QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    CONNECTION_FAILURE    = 'connection_failure'
    ATTEMPT_FAILURE       = 'attempt_failure'

    REQUEST_FAILURE_NT = namedtuple(
        'REQUEST_FAILURE_NT', ['ident', 'message', 'error', 'response', 'requestData']
    )

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ executeRequest
    @classmethod
    def executeRequest(cls, url, args =None, logger =None):
        """ Executes the request specified. """
        reqData  = {'url':url, 'args':args, 'logger':logger}
        response = None

        try:
            #---------------------------------------------------------------------------------------
            # EXECUTE REQUEST
            #       Make the request securely with verification using the CA bundle file contained
            #       within the requests python site library. The location of this file varies
            #       depending on where the Python installation is located.
            #       See PyGlassEnvironment.requestsCABundle getter for more details.
            if url.startswith('https:'):
                bundle= PyGlassEnvironment.requestsCABundle
                if args is None:
                    return requests.get(url, verify=bundle)
                else:
                    return requests.post(url, data=args, verify=bundle)
            else:
                if args is None:
                    return requests.get(url)
                else:
                    return requests.post(url, data=args)

        except exceptions.SSLError as err:
            logger.writeError([
                'SSL Request Error:',
                'Default CA Bundle Path: ' + StringUtils.toUnicode(requestUtils.DEFAULT_CA_BUNDLE_PATH)
            ], err)

            return cls._createError(
                ident=RequestUtils.CONNECTION_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message='Unable to establish secure connection.'
            )

        except requests.ConnectionError as err:
            return cls._createError(
                ident=RequestUtils.CONNECTION_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message='Unable to create connection. No available internet connection was found.'
            )
        except Exception as err:
            return cls._createError(
                ident=RequestUtils.ATTEMPT_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message='Unable to connect to remote server at this time.'
            )

#___________________________________________________________________________________________________ logError
    @classmethod
    def logError(cls, logger, error):
        if not isinstance(error, cls.REQUEST_FAILURE_NT):
            return False

        echo = [
            'ERROR: RequestUtils failure:',
            'ID: ' + StringUtils.toUnicode(error.ident),
            'MESSAGE: ' + StringUtils.toUnicode(error.message),
            'ERROR: ' + StringUtils.toUnicode(error.error),
            'RESPONSE: ' + StringUtils.toUnicode(error.response)
        ]

        if error.response:
            r = error.response
            echo.append('STATUS_CODE: ' + StringUtils.toUnicode(getattr(r, 'status_code', 'NONE')))
            try:
                json = r.json()
                if len(json) > 525:
                    json = json[:500] + '...'
                echo.append('JSON: ' + StringUtils.toUnicode(json))
            except Exception as err:
                echo.append('JSON: NONE')

        if error.error:
            logger.writeError(echo, error.error)
        else:
            logger.write(echo)

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createError
    @classmethod
    def _createError(cls, ident, error, message, response, requestData):
        out = cls.REQUEST_FAILURE_NT(
            ident=ident,
            error=error,
            message=message,
            response=response,
            requestData=requestData
        )
        cls.logError(requestData.logger, out)
        return out

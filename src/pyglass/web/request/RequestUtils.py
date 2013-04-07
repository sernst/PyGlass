# RequestUtils.py
# (C)2013
# Scott Ernst

from collections import namedtuple

import requests
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

        except requests.exceptions.SSLError, err:
            logger.writeError([
                u'SSL Request Error:',
                u'Default CA Bundle Path: ' + unicode(requestUtils.DEFAULT_CA_BUNDLE_PATH)
            ], err)

            return cls._createError(
                ident=RequestUtils.CONNECTION_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message=u'Unable to establish secure connection.'
            )

        except requests.ConnectionError, err:
            return cls._createError(
                ident=RequestUtils.CONNECTION_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message=u'Unable to create connection. No available internet connection was found.'
            )
        except Exception, err:
            return cls._createError(
                ident=RequestUtils.ATTEMPT_FAILURE,
                error=err,
                response=response,
                requestData=reqData,
                message=u'Unable to connect to remote server at this time.'
            )

#___________________________________________________________________________________________________ logError
    @classmethod
    def logError(cls, logger, error):
        if not isinstance(error, cls.REQUEST_FAILURE_NT):
            return False

        echo = [
            u'ERROR: RequestUtils failure:',
            u'ID: ' + unicode(error.ident),
            u'MESSAGE: ' + unicode(error.message),
            u'ERROR: ' + unicode(error.error),
            u'RESPONSE: ' + unicode(error.response)
        ]

        if error.response:
            r = error.response
            echo.append(u'STATUS_CODE: ' + unicode(getattr(r, 'status_code', u'NONE')))
            try:
                json = r.json()
                if len(json) > 525:
                    json = json[:500] + u'...'
                echo.append(u'JSON: ' + unicode(json))
            except Exception, err:
                echo.append(u'JSON: NONE')

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

# Request.py
# (C)2012-2013
# Scott Ernst

from PySide.QtCore import QObject

from pyaid.ArgsUtils import ArgsUtils
from pyaid.debug.Logger import Logger
from pyaid.decorators.ClassInstanceMethod import ClassInstanceMethod

from pyglass.web.request.RequestThread import RequestThread
from pyglass.web.request.RequestUtils import RequestUtils

#___________________________________________________________________________________________________ Request
class Request(QObject):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _activeRequests = []

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, url, args =None, **kwargs):
        """Creates a new instance of Request."""
        self._localData = ArgsUtils.extract('localData', None, kwargs)
        self._dead      = ArgsUtils.extract('dead', False, kwargs)
        QObject.__init__(self, parent, **kwargs)
        self._url       = url
        self._owner     = parent
        self._log       = parent.log if parent else Logger(self)
        self._callback  = None
        self._args      = args
        self._request   = None
        self._result    = None
        self._sent      = False
        self._async     = False

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: args
    @property
    def args(self):
        """The dictionary of arguments sent with the Request."""
        return self._args

#___________________________________________________________________________________________________ GS: localData
    @property
    def localData(self):
        """ The arbitrary local data associated with the Request object. That is, data not sent
            to the server with the request, but stored with the request usually for use after the
            request has completed.
        """
        return self._localData
    @localData.setter
    def localData(self, value):
        self._localData = value

#___________________________________________________________________________________________________ GS: url
    @property
    def url(self):
        """The URL endpoint for the Request."""
        return self._url

#___________________________________________________________________________________________________ GS: isAsynchronous
    @property
    def isAsynchronous(self):
        """Specifies whether or not the request is asynchronous."""
        return self._async

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        """The raw response object returned by the requests module."""
        return self._result

#___________________________________________________________________________________________________ GS: content
    @property
    def content(self):
        """The raw content returned by the requests."""
        return self._result.content if self._result else None

#___________________________________________________________________________________________________ GS: json
    @property
    def json(self):
        try:
            return self._result.json()
        except Exception, err:
            return None

#___________________________________________________________________________________________________ GS: error
    @property
    def error(self):
        return None if self.success else self._result

#___________________________________________________________________________________________________ GS: success
    @property
    def success(self):
        return bool(self._result is not None and hasattr(self._result, 'status_code'))

#___________________________________________________________________________________________________ GS: isDead
    @property
    def isDead(self):
        return self._dead

#___________________________________________________________________________________________________ GS: isConnectionError
    @property
    def isConnectionError(self):
        return self._result and self._result in [
            RequestUtils.CONNECTION_FAILURE, RequestUtils.ATTEMPT_FAILURE
        ]

#___________________________________________________________________________________________________ GS: isInvalidResponse
    @property
    def isInvalidResponse(self):
        return self._result and self._result.ident == RequestUtils.RESPONSE_FAILURE

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ echo
    def echo(self):
        s = '\n\t'.join([
            u'Request[%s]:' % unicode(self.url),
            u'SUCCESS: ' + unicode(self.success),
            u'DEAD: ' + unicode(self.isDead),
            u'RAW: ' + unicode(self.rawResponse),
            u'RESULT: ' + unicode(self.result),
            u'ERROR: ' + unicode(self.error)
        ])
        print s
        return s

#___________________________________________________________________________________________________ send
    @ClassInstanceMethod
    def send(self, cls, *args, **kwargs):
        """ Sends an API request to the Vizme servers and handles the response. This can be sent
            either synchronously or asynchronously depending on whether or not a callback argument
            is included in the request. Asynchronous requests must be handled within the context
            of a running PySide application loop, as the threading is managed by PySide.
        """

        callback = ArgsUtils.extract('callback', None, kwargs, args, 0)
        if self:
            return self._sendRequest(callback=callback, **kwargs)
        return cls._createAndSend(callback=callback, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _sendRequest
    def _sendRequest(self, callback, *args, **kwargs):
        if self._sent or self._dead:
            return None

        self._sent = True
        if callback:
            return self._sendAsync(callback)

        self._result = RequestUtils.executeRequest(url=self._url, args=self._args, logger=self._log)
        if self._callback is not None:
            self._callback(self)
        self._callback = None
        return self

#___________________________________________________________________________________________________ _createAndSend
    @classmethod
    def _createAndSend(cls, parent, url, callback =None, args =None, **kwargs):
        dead = ArgsUtils.extract('dead', False, kwargs)
        req  = Request(parent=parent, url=url, args=args, dead=dead, **kwargs)
        if dead:
            return req.dead
        return req.send(callback)

#___________________________________________________________________________________________________ _sendAsync
    def _sendAsync(self, callback):
        """Doc..."""
        self._async    = True
        self._callback = callback
        Request._activeRequests.append(self)

        thread = RequestThread(self._owner, url=self._url, args=self._args)
        self._request = thread
        thread.logSignal.signal.connect(self._handleUpdateResults)
        thread.completeSignal.signal.connect(self._handleRemoteThreadComplete)
        thread.start()

        return self

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleUpdateResults
    def _handleUpdateResults(self, value):
        self._owner.refreshGui()

#___________________________________________________________________________________________________ _handleRemoteThreadComplete
    def _handleRemoteThreadComplete(self, value):
        self._result  = value['output']
        self._request = None
        if self._callback is not None:
            self._callback(self)
        self._callback = None

        if self in Request._activeRequests:
            Request._activeRequests.remove(self)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


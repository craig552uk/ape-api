"""
    flask_json
    ~~~~~~~~~~

    A Flask extension providing better JSON support.

    :copyright: (c) 2015 by Sergey Kozlov
    :license: BSD, see LICENSE for more details.
"""
import sys
import collections
from functools import wraps
from datetime import datetime, date, time
try:
    from speaklater import _LazyString
# Don't cover since simulated in test_encoder_nospeaklater().
except ImportError:  # pragma: no cover
    _LazyString = None
from flask import current_app, jsonify, request, Request, Response
from flask import json

__version__ = '0.2.0'

text_type = unicode if sys.version_info[0] == 2 else str


def json_response(status_=200, headers_=None, **kwargs):
    """Helper function to build JSON response
    with the given HTTP status and fields(``kwargs``).

    It also puts HTTP status code to the JSON response if
    :ref:`JSON_ADD_STATUS <opt_add_status>` is ``True``::

        app.config['JSON_ADD_STATUS'] = True
        json_response(test=12)
        # {"status": 200, "test": 12}, response HTTP status is 200.

        json_response(400, test=12)
        # {"status": 400, "test": 12}, response HTTP status is 400.

        json_response(status_=401, test=12)
        # {"status": 401, "test": 12}, response HTTP status is 401.

        app.config['JSON_ADD_STATUS'] = False
        json_response(test=12)
        # {"test": 12}, response HTTP status is 200.

    Name of the HTTP status filed is configurable and can be changed with
    :ref:`JSON_STATUS_FIELD_NAME <opt_status_name>`::

        app.config['JSON_ADD_STATUS'] = True
        app.config['JSON_STATUS_FIELD_NAME'] = 'http_status'
        json_response(test=12)
        # {"http_status": 200, "test": 12}, response HTTP status is 200.

    If ``kwargs`` already contains key with the same name as
    ``JSON_STATUS_FIELD_NAME`` then it's value will be used instead of HTTP
    status code::

        app.config['JSON_ADD_STATUS'] = True

        json_response(status_=400, status=100500, test=12)
        # {"status": 100500, "test": 12}, but response HTTP status is 400.

        json_response(status=100500, test=12)
        # {"status": 100500, "test": 12}, but response HTTP status is 200.

        app.config['JSON_STATUS_FIELD_NAME'] = 'http_status'
        json_response(http_status=100500, test=12)
        # {"http_status": 100500, "test": 12}, but response HTTP status is 200.

    You also may add custom headers to the JSON response by passing iterable or
    dict to `headers_`::

        # One way.
        headers = {'MY-HEADER': value, 'X-EXTRA': 123}
        json_response(headers_=headers, test=12)

        # Another way (tuple, list, iterable).
        headers = (('MY-HEADER', value), ('X-EXTRA', 123))
        json_response(headers_=headers, test=12)

    Args:
        `status_`: HTTP response status code.
        `headers_`: iterable or dictionary with header values.
        kwargs: keyword arguments to put in result JSON.

    Returns:
        flask.Response: Response with the JSON content.
    """
    if current_app.config['JSON_ADD_STATUS']:
        field = current_app.config['JSON_STATUS_FIELD_NAME']
        if field not in kwargs:
            kwargs[field] = status_
    response = jsonify(**kwargs)
    response.status_code = status_

    if headers_ is not None:
        response.headers.extend(headers_)

    return response


# Helper function to normalize view return values for @as_json decorator.
# It always returns (dict, status, headers). Missing values will be None.
# For example in such cases when tuple_ is
#   (dict, status), (dict, headers), (dict, status, headers),
#   (dict, headers, status)
#
# It assumes what status is int, so this construction will not work:
# (dict, None, headers) - it doesn't make sense because you just use
# (dict, headers) if you want to skip status.
def _normalize_view_tuple(tuple_):
    v = tuple_ + (None,) * (3 - len(tuple_))
    return v if isinstance(v[1], int) else (v[0], v[2], v[1])


def as_json(f):
    """This decorator converts view's return value to JSON response.

    The decorator expects the following return values:
        * Flask :class:`~flask.Response` instance (see note bellow);
        * a ``dict`` with JSON content;
        * a tuple of ``(dict, status)`` or ``(dict, headers)`` or
          ``(dict, status, headers)`` or ``(dict, headers, status)``.

    Instead of ``dict`` you may pass ``None`` and it will be treated as empty
    JSON (same as ``dict()`` or ``{}``).

    In all other cases it raises an error.

    The decorator provides the same features as :func:`.json_response`.

    Usage::

        @as_json
        def view_simple():
            return dict(param=value, param2=value2)

        @as_json
        def view_comp():
            return dict(param=value, param2=value2), 400

    Note:
        If wrapped view returns Flask :class:`~flask.Response` then it will be
        used as is without passing to :func:`.json_response`. But the response
        must be a JSON response (mimetype must contain ``application/json``),
        otherwise ``AssertionError`` will be raised.

    Returns:
        flask.Response: Response with the JSON content.

    Raises:
        ValueError: if return value is not supported.

    See Also:
        :func:`.json_response`
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs)
        callback = request.args.get("callback", "")

        if rv is None:
            response = json_response()
        elif isinstance(rv, dict):
            response = json_response(**rv)
        elif isinstance(rv, Response):
            assert 'application/json' in rv.mimetype
            response = rv
        elif isinstance(rv, tuple):
            d, status, headers = _normalize_view_tuple(rv)
            response = json_response(status_=status or 200, headers_=headers,
                                 **(d or dict()))
        else:
            raise ValueError('Unsupported return value.')

        if (callback):
            # JSONP response
            response.status_code = 200
            response.headers['Content-Type'] = "application/javascript"
            response.data = "%s(%s);" % (callback, response.data)

        return response
    return wrapper


# TODO: maybe subclass from HTTPException?
class JsonError(Exception):
    """Exception which will be converted to JSON response.

    Usage::

        raise JsonError(description='text')
        raise JsonError(status_=401, one='text', two=12)
    """
    def __init__(self, status_=400, headers_=None, **kwargs):
        """Construct error object.

        Parameters are the same as for :func:`.json_response`.

        Args:
            `status_`: HTTP response status code.
            `headers_`: iterable or dictionary with header values.
            kwargs: keyword arguments to put in result JSON.

        See Also:
            :func:`.json_response`,
            :meth:`@error_handler <.FlaskJSON.error_handler>`.
        """
        super(JsonError, self).__init__()
        assert status_ != 200
        self.status = status_
        self.headers = headers_
        self.data = kwargs


class JsonRequest(Request):
    """This class changes :class:`flask.Request` behaviour on JSON parse errors.

    :meth:`flask.Request.get_json` will raise :class:`.JsonError`
    by default on invalid JSON content.

    See Also:
        :ref:`JSON_DECODE_ERROR_MESSAGE <opt_decode_error_msg>`,
        :meth:`@invalid_json_error <.FlaskJSON.invalid_json_error>`
    """
    def on_json_loading_failed(self, e):
        # Try decoder error hook firstly; see FlaskJSON.invalid_json_error().
        func = current_app.extensions['json']._decoder_error_func
        if func is not None:
            response = func(e)
            if response is not None:
                return response

        # By default we raise json error with description.
        # If there is no description config or it's text is empty then
        # raise without a description.
        desc = current_app.config.get('JSON_DECODE_ERROR_MESSAGE')
        if desc:
            raise JsonError(description=desc)
        else:
            raise JsonError()


class JSONEncoderEx(json.JSONEncoder):
    """Extends default Flask JSON encoder with more types:

    * iterable;
    * :class:`~datetime.datetime`;
    * :class:`~datetime.date`;
    * :class:`~datetime.time`;
    * `speaklater <https://pypi.python.org/pypi/speaklater>`_ lazy strings;
    * objects with ``__json__()`` or ``for_json()`` methods.

    Time related values will be converted to ISO 8601 format by default.

    See Also:
        :ref:`JSON_DATETIME_FORMAT <opt_fmt_datetime>`,
        :ref:`JSON_DATE_FORMAT <opt_fmt_date>`,
        :ref:`JSON_TIME_FORMAT <opt_fmt_time>`,
        :ref:`JSON_USE_ENCODE_METHODS <opt_use_enc_methods>`.
    """
    def default(self, o):
        # We have to test _LazyString before Iterable to prevent
        # converting string to list of chars, since string is iterable too.
        if _LazyString is not None and isinstance(o, _LazyString):
            return text_type(o)
        elif isinstance(o, collections.Iterable):
            # All iterables will be converted to list.
            return list(o)
        elif isinstance(o, datetime):
            fmt = current_app.config.get('JSON_DATETIME_FORMAT')
            return o.strftime(fmt) if fmt else o.isoformat()
        elif isinstance(o, date):
            fmt = current_app.config.get('JSON_DATE_FORMAT')
            return o.strftime(fmt) if fmt else o.isoformat()
        elif isinstance(o, time):
            fmt = current_app.config.get('JSON_TIME_FORMAT')
            return o.strftime(fmt) if fmt else o.isoformat()
        elif current_app.config.get('JSON_USE_ENCODE_METHODS'):
            if hasattr(o, '__json__'):
                return o.__json__()
            elif hasattr(o, 'for_json'):
                return o.for_json()
        return super(JSONEncoderEx, self).default(o)


class JsonTestResponse(Response):
    """JSON Response class for testing.

    It provides convenient access to JSON content without explicit response
    data decoding.

    Flask-JSON replaces Flask's response class with this one
    on initialization if testing mode enabled.

    Usage:

    .. code-block:: py

        app = Flask()
        app.config['TESTING'] = True
        FlaskJSON(app)
        ...
        client = app.test_client()
        r = client.get('/view')  # suppose it returns json_response(param='12)
        assert r.json['param'] == 12

    If you enable testing after Flask-JSON initialization the you have to
    set :class:`.JsonTestResponse` by yourself:

    .. code-block:: py

        app = Flask()
        FlaskJSON(app)
        app.config['TESTING'] = True
        app.response_class = JsonTestResponse

    """
    _json_cache = None

    @property
    def json(self):
        """Response JSON content."""
        if self._json_cache is None:
            assert self.mimetype == 'application/json'
            self._json_cache = json.loads(self.data)
        return self._json_cache


class FlaskJSON(object):
    """Flask-JSON extension class."""
    def __init__(self, app=None):
        self._app = app
        self._error_handler_func = None
        self._decoder_error_func = None
        self._encoder_class = JSONEncoderEx
        if app is not None:
            self.init_app(app)

    def _error_handler(self, e):
        if self._error_handler_func is not None:
            return self._error_handler_func(e)
        return json_response(e.status, e.headers, **e.data)

    def init_app(self, app):
        """Initializes the application with the extension.

        Args:
            app: Flask application object.
        """
        app.config.setdefault('JSON_ADD_STATUS', True)
        app.config.setdefault('JSON_STATUS_FIELD_NAME', 'status')
        app.config.setdefault('JSON_DECODE_ERROR_MESSAGE', 'Not a JSON.')

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['json'] = self

        self._app = app
        app.request_class = JsonRequest
        app.json_encoder = self._encoder_class
        app.errorhandler(JsonError)(self._error_handler)

        if app.testing:
            app.response_class = JsonTestResponse

    def error_handler(self, func):
        """This decorator allows to set custom handler for the
        :class:`.JsonError` exceptions.

        In custom handler you may return :class:`flask.Response` or raise
        an exception. If user defined handler returns ``None`` then default
        action takes place (generate JSON response from the exception).

        Example:

            ::

                json = FlaskJson(app)
                ...

                @json.error_handler
                def custom_error_handler(e):
                    # e is JsonError.
                    return json_response(status=401)

        See Also:
            :meth:`.invalid_json_error`.
        """
        self._error_handler_func = func
        return func

    def invalid_json_error(self, func):
        """This decorator allows to set custom handler for the invalid
        JSON requests.

        It will be called by the
        :meth:`request.get_json() <flask.Request.get_json>`.

        If the handler returns or raises nothing then Flask-JSON
        raises :class:`.JsonError`.

        Example:

            ::

                json = FlaskJson(app)
                ...

                @json.invalid_json_error
                def invalid_json_error(e):
                    raise SomeException

        By default JSON response will be generated with HTTP 400::

            {"status": 400, "description": "Not a JSON."}

        You also may return a value from the handler then it will be used as
        :meth:`request.get_json() <flask.Request.get_json>` result on errors.

        See Also:
            :ref:`JSON_DECODE_ERROR_MESSAGE <opt_decode_error_msg>`
        """
        self._decoder_error_func = func
        return func

    def encoder(self, func):
        """This decorator allows to set extra JSON encoding step on response
        building.

        JSON encoding order:

        * User defined encoding.
        * Flask-JSON encoding.
        * Flask encoding.

        If user defined encoder returns None then default encoders takes place
        (Flask-JSON and then Flask).

        Example:

            ::

                json = FlaskJson(app)
                ...

                @json.encoder
                def custom_encoder(o):
                    if isinstance(o, MyClass):
                        return o.to_string()
        """
        class JSONEncoderWithHook(JSONEncoderEx):
            def default(self, o):
                result = func(o)
                if result is not None:
                    return result
                return JSONEncoderEx.default(self, o)
        if self._app is not None:
            self._app.json_encoder = JSONEncoderWithHook
        else:
            self._encoder_class = JSONEncoderWithHook
        return func
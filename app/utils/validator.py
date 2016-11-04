# -*- coding: utf-8 -*-
"""
A validator for flask request

Usage:

    from validator import Validator

    v = Validator()

    @app.route('/user/<user_id>')
    @v.param({
        'name': v.str(),
        v.optional('age', default=20): v.int(min=18, max=99)
    })
    def user(user_id, name, age):
        return jsonify(data=[user_id, name, age])

Custom validator:

    from schema import And, Use
    @v.register('int')
    def v_int(min=-sys.maxsize, max=sys.maxsize):
        return And(Use(int), lambda x: min <= x <= max)

Built-in validators:

    int, bool, str, float, enum
    email, url, ipv4, ipv6, domain, mac, uuid, iban

See https://github.com/keleshev/schema for detail about schema
See https://validators.readthedocs.io/en/latest for detail abort validators
"""
import sys
import functools
import collections
import validators
from schema import Schema, SchemaError, And, Use, Optional, Regex
from flask import make_response, request, abort
from app.utils.ResponseUtil import standard_response

PY3 = sys.version_info.major > 2
if PY3:
    text_type = str
else:
    text_type = unicode  # noqa


class Validator(object):

    def __init__(self):
        self.optional = Optional
        self.regex = Regex
        self.bool = lambda: bool
        for name in ['email', 'ipv4', 'ipv6', 'domain',
                     'url', 'mac_address', 'uuid', 'iban']:
            setattr(self, name, self._make_validator(name))

    def _make_validator(self, name):
        validate = getattr(validators, name)
        return lambda: And(validate)

    def int(self, min=-sys.maxsize, max=sys.maxsize):
        return And(Use(int), lambda x: min <= x <= max)

    def float(self, min=-sys.float_info.max, max=sys.float_info.max):
        return And(Use(float), lambda x: min <= x <= max)

    def str(self, minlen=0, maxlen=1024 * 1024):
        return And(text_type, lambda x: minlen <= len(x) <= maxlen)

    def enum(self, *items):
        return And(text_type, lambda x: x in items)

    def register(self, name):
        """A decorator for register validator"""
        def decorator(f):
            setattr(self, name, f)
            return f
        return decorator

    def get_data(self):
        """
        Get request data based on request.method and request.mimetype

        Returns:
            A regular dict which can be modified(scheme will modify data
            on validating)
        """
        if request.method in ['GET', 'DELETE']:
            return request.args.to_dict()
        else:
            if request.mimetype == 'application/json':
                data = request.get_json()
                if not isinstance(data, collections.Mapping):
                    self.handle_error('JSON content must be object')
                return data
            else:
                return request.form.to_dict()

    def handle_error(self, message):
        """Abort with suitable error response"""
        message = standard_response(0, message)
        abort(400, response=make_response(message, 200))

    def param(self, schema):
        """A decorator for validate request data"""
        if not isinstance(schema, collections.Mapping):
            raise TypeError('schema must be Mapping')
        # add error message
        schema = {k: And(v, error='%s invalid' % k)
                  for k, v in schema.items()}
        validate = Schema(schema).validate

        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                data = self.get_data()
                try:
                    data = validate(data)
                except SchemaError as ex:
                    self.handle_error(str(ex))
                kwargs.update(data)
                return f(*args, **kwargs)
            return wrapper
        return decorator

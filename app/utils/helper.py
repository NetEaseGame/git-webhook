# -*- coding: utf-8 -*-
import functools
import collections
from schema import Schema, SchemaError
from flask import make_response, request, abort as flask_abort


def abort(code, message=None):
    """
    Abort with suitable error response

    Args:
        code (int): status code
        message (str): error message
    """
    if message is None:
        flask_abort(code)
    else:
        flask_abort(code, response=make_response(message, code))


def get_request_data():
    """
    Get request data based on request.method and request.mimetype

    Returns:
        A regular dict which can be modified(scheme will modify data
        on validating)
    Raises:
        BadRequest: JSON content must be object
    """
    if request.method in ['GET', 'DELETE']:
        return request.args.to_dict()
    else:
        if request.mimetype == 'application/json':
            data = request.get_json()
            if not isinstance(data, collections.Mapping):
                abort(400, 'JSON content must be object')
            return data
        else:
            return request.form.to_dict()


def param(schema, get_data=get_request_data):
    """
    A decorator for validate request data

    Usage:

        from schema import And, Use

        @app.route('/user/<user_id>')
        @param({
            'name': str,
            'age': And(Use(int), lambda x: 18 <= x <= 99)
        })
        def user(user_id, name, age):
            print([user_id, name, age])

    See https://github.com/keleshev/schema for detail about schema
    """
    validate = Schema(schema).validate

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            data = get_data()
            try:
                data = validate(data)
            except SchemaError as ex:
                abort(400, str(ex))
            kwargs.update(data)
            return f(*args, **kwargs)
        return wrapper
    return decorator

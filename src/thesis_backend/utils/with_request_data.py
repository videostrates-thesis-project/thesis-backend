from functools import wraps

from flask import request
from marshmallow import Schema, ValidationError


def with_request_data(schema: Schema) -> callable:
    """
    Validates the request data using the provided schema and injects it into the decorated function as a keyword
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request_data = schema.load(request.get_json())
            except ValidationError as err:
                return {"error": err.normalized_messages()}, 400

            return func(*args, request_data=request_data, **kwargs)

        return wrapper

    return decorator

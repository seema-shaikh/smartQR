from functools import wraps
from flask import jsonify

def header_required(request):
    def header_decorator(func):
        @wraps(func)
        def header_view(*args, **kwargs):
            if request.content_type != 'application/json':
                return jsonify({'error': 'Unsupported Media Type'})
            return func(*args, **kwargs)
        return header_view
    return header_decorator
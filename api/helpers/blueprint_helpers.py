from functools import wraps

import jwt
from flask import current_app, jsonify, make_response, request

# Authentication decorator
# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         # ensure the jwt-token is passed with the headers
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         if not token: # throw error if no token provided
#             return make_response(jsonify({"message": "A valid token is missing!"}), 401)
#         try:
#            # decode the token to obtain user public_id
#             data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
#         except:
#             return make_response(jsonify({"message": "Invalid token!"}), 401)
#          # Return the user information attached to the token
#         return f(*args, **kwargs)
#     return decorator


def token_required(fn):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            print("Hello")

        return decorator

    return wrapper

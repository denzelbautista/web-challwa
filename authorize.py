from flask import request, jsonify
import sys
import jwt
from config.local import config
from functools import wraps

def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'X-ACCESS-TOKEN' in request.headers:
            token = request.headers['X-ACCESS-TOKEN']

        if token is None:
            return jsonify({
                'success': False,
                'message': 'Unauthenticated user, please provide your credentials'
            }), 401
        
        try:
            decoded_token = jwt.decode(token, config['SECRET_KEY'], algorithms=[config['ALGORYTHM']])
            user_created_id = decoded_token['user_created_id']
        except Exception as e:
            print('e: ', e)
            print('sys.exc_info(): ', sys.exc_info())
            return jsonify({
                'success': False,
                'message': 'Invalid Token, try a new token'
            }), 401
        
        # Pass the user_created_id to the decorated function
        return f(user_created_id=user_created_id, *args, **kwargs)
    
    decorator.__name__ = f.__name__
    return decorator

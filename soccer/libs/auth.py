from functools import wraps

from flask import g, request
from werkzeug.local import LocalProxy

from soccer.exceptions import BadRequest, Forbidden
from configuration import SoccerConfig

# object user ter-authentifikasi
user = LocalProxy(lambda: getattr(g, 'user_auth', None))

role_scope = SoccerConfig.ROLE_SCOPE

def internal():
    """Decorateor to protect using in internal only"""

    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            _auth_internal()
            return f(*args, **kwargs)

        return decorator_function
    
    return decorator


def scope(*scopes):
    """Decorator for endpoint scope

    Args:
        scopes: type scope
    """

    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            _auth(*scopes)
            return f(*args, **kwargs)

        return decorator_function

    return decorator


def _auth(*scopes):
    if not user:
        raise BadRequest("Missing auth header")

    for s in scopes:
        if s not in role_scope[user.role]:
            raise Forbidden("you don't have access to perform this action")


def _auth_internal():
    token = request.headers.get("Authorization")
    if not token:
        raise BadRequest("Missing auth header")

    if token != SoccerConfig.INTERNAL_TOKEN:
        raise BadRequest("Wrong token")
import time

from flask import g, request
from functools import wraps

from soccer.exceptions import BadRequest


class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.rest = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        value = cache.incr(self.key)
        cache.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(value, limit)

    @property
    def remaining(self):
        return self.limit - self.current

    @property
    def over_limit(self):
        return self.current >= self.limit


def get_view_rate_limit():
    return getattr(g, "_view_rate_limit", None)


def ratelimit(limit, per=300, send_x_headers=True,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        @wraps(f)
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            rlimit = RateLimit(key, limit, per, send_x_headers)
            g._view_rate_limit = rlimit
            if rlimit.over_limit:
                raise BadRequest("You hit the rate limit")
            return f(*args, **kwargs)
        return rate_limited
    return decorator
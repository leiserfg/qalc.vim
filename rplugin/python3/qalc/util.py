import time
from functools import wraps


def throttle(s):
    """Decorator ensures function that can only be called once every `s` seconds.
    """

    def decorate(fn):
        t = None
        @wraps(fn)
        def wrapped(*args, **kwargs):
            nonlocal t
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = fn(*args, **kwargs)
                t = time.time()
                return result

        return wrapped

    return decorate

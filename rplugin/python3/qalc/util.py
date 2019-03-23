import re
from functools import wraps
from threading import Timer

_ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def ansi_escape(text):
    return _ansi_re.sub("", text)




def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked.
        From https://gist.github.com/walkermatt/2871026
        """
    def decorator(fn):
        @wraps(fn)
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)

            try:
                debounced.t.cancel()
            except (AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator

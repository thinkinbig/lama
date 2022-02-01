import functools
from datetime import time
import logging
import os

from log import LOG_DIR


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def _wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return _wrapper_timer


def enable_logging(filename, level=logging.DEBUG):
    def _wrap_decorator(func):
        @functools.wraps(func)
        def _wrapper_logging_decorator(*args, **kwargs):
            _log_name = os.path.join(LOG_DIR, filename)
            logging.basicConfig(filename=_log_name,
                                encoding='utf-8', level=level)
            logging.log(f"Entering into the function {func}.")
            func(*args, **kwargs)
            logging.log(f"Leaving the function {func}.\n")
        return _wrapper_logging_decorator
    return _wrap_decorator


def suppress(excepts, action=lambda _: None):
    def _warning_decorator(func):
        @functools.wraps(func)
        def _wrapper_warning_decorator(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except excepts as e:
                action(e)
            return res
        return _wrapper_warning_decorator
    return _warning_decorator


def experimental(cls):
    """
    Decorator to indicate the class definition is not stable

    Returns:
        cls: class to be decorated
    """
    # Make copy of original __init__, so we can call it without recursion
    cls_init = cls.__init__

    def __init__(self, *args, **kwargs):
        cls_init(self, *args, **kwargs)

    # Set the class' __init__ to the new one
    cls.__init__ = __init__

    return cls

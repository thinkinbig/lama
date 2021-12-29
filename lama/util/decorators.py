import functools
import logging
import sys
from datetime import time


def debug(func, stream=sys.stdout):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        logging.basicConfig(stream=stream, level=logging.DEBUG)
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        logging.debug(msg=f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logging.debug(msg=f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


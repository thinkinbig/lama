import functools
from datetime import time
import warnings
from numpy import result_type


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


def suppress_warning(warning):
    def _warning_decorator(func):
        @functools.wraps(func)
        def _wrapper_warning_decorator(*args, **kwargs):
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=warning)
                res = func(*args, **kwargs)
            return res
        return _wrapper_warning_decorator
    return _warning_decorator
import functools
from datetime import time
import logging
import os

from log import LOG_DIR


__all__ = ['enable_logging', 'suppress', 'experimental']


def enable_logging(filename, level=logging.NOTSET, logger_name=None):
    def _wrap_decorator(func):
        @functools.wraps(func)
        def _wrapper_logging_decorator(*args, **kwargs):
            _log_name = os.path.join(LOG_DIR, filename)
            # create logger for prd_ci
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)

            # create formatter and add it to the handlers
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(_log_name)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)

            # add handler
            logger.addHandler(fh)
            logger.addHandler(ch)

            logger.info(msg=f"Entering into the function {func.__name__}.")
            try:
                value = func(*args, **kwargs)
                # check not None
                if value is not None:
                    logger.info(msg=f'Returned value is: {value}')
            except Exception as e:
                logger.error(str(e))
            logger.info(msg=f"Leaving the function {func.__name__}.\n")
            return value
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

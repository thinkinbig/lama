import functools
import logging
import os

from log import LOG_DIR


__all__ = ['enable_logging', 'suppress', 'experimental']


_handler_pool = {}


def enable_logging(filename, level=logging.NOTSET, logger_name=None):

    def _get_handler_from_pool(key):
        # if not _handler_pool[key]:
        if key not in _handler_pool:
            _handler_pool[key] = logging.FileHandler(key)
            _handler_pool[key].flush()
        return _handler_pool[key]

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
            fh = _get_handler_from_pool(_log_name)
            fh.setLevel(level)
            fh.setFormatter(formatter)

            # add handler
            logger.addHandler(fh)

            logger.info(msg=f"Entering into the function {func.__name__}.")
            value = None
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

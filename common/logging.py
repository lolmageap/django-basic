from typing import Callable
import logging

def query_logging(level: logging.Level) -> None:
    def logging_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(level)
            logger.addHandler(logging.StreamHandler())
            return func(*args, **kwargs)
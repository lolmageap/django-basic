import functools
import logging
from typing import Callable, Optional, Union

from django.db import connection


def query_logging(level: Optional[int] = None) -> Union[Callable, Callable[[Callable], Callable]]:
    if level is None or callable(level):
        func = level
        logging_level = logging.INFO

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("django.db.backends")
            logger.setLevel(logging_level)

            if not logger.hasHandlers():
                logger.addHandler(logging.StreamHandler())

            connection.queries.clear()

            result = func(*args, **kwargs)

            if logger.level == logging.INFO:
                for query in connection.queries:
                    logger.info(f"SQL: {query['sql']} (Time: {query['time']}s)")
            if logger.level == logging.DEBUG:
                for query in connection.queries:
                    logger.debug(f"SQL: {query['sql']} (Time: {query['time']}s)")
            if logger.level == logging.WARNING:
                for query in connection.queries:
                    logger.warning(f"SQL: {query['sql']} (Time: {query['time']}s)")
            if logger.level == logging.ERROR:
                for query in connection.queries:
                    logger.error(f"SQL: {query['sql']} (Time: {query['time']}s)")
            if logger.level == logging.CRITICAL:
                for query in connection.queries:
                    logger.critical(f"SQL: {query['sql']} (Time: {query['time']}s)")
            if logger.level == logging.NOTSET:
                for query in connection.queries:
                    logger.log(logging.NOTSET, f"SQL: {query['sql']} (Time: {query['time']}s)")
            return result

        return wrapper

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("django.db.backends")
            logger.setLevel(level)

            if not logger.hasHandlers():
                logger.addHandler(logging.StreamHandler())

            connection.queries.clear()

            result = func(*args, **kwargs)

            for query in connection.queries:
                logger.debug(f"SQL: {query['sql']} (Time: {query['time']}s)")

            return result

        return wrapper

    return decorator

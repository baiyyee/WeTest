import logging
import functools
from ..util import date


def timeit(func):
    """Get function exec duration"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = date.get_time()
        logging.info(f"START    : {start}")

        func(*args, **kwargs)

        end = date.get_time()
        logging.info(f"END      : {end}")

        duration = date.get_timedelta(start, end).seconds
        logging.info(f"DURATION : {duration}(s)")

    return wrapper

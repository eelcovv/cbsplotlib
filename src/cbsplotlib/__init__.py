import functools
import logging
# -*- coding: utf-8 -*-
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

LOGGER_BASE_NAME = __name__

__tool_name__ = Path(__file__).parent.stem

_log = logging.getLogger(__name__)


@functools.lru_cache()
def _ensure_handler():
    """
    The first time this function is called, attach a `StreamHandler` using the
    same format as `logging.basicConfig` to the Matplotlib root logger.

    Return this handler every time this function is called.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    _log.addHandler(handler)
    return handler


def set_loglevel(level):
    """
    Set Matplotlib's root logger and root logger handler level, creating
    the handler if it does not exist yet.

    Typically, one should call ``set_loglevel("info")`` or
    ``set_loglevel("debug")`` to get additional debugging information.

    Parameters
    ----------
    level : {"notset", "debug", "info", "warning", "error", "critical"}
        The log level of the handler.

    Notes
    -----
    The first time this function is called, an additional handler is attached
    to Matplotlib's root handler; this handler is reused every time and this
    function simply manipulates the logger and handler's level.
    """
    _log.setLevel(level.upper())
    _ensure_handler().setLevel(level.upper())

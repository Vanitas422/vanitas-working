"""Logging helpers for the add-on."""

from __future__ import annotations

import logging
from typing import Final

from .constants import ADDON_ID

_LOGGER: Final[logging.Logger] = logging.getLogger(ADDON_ID)


def get_logger() -> logging.Logger:
    """Return a configured logger for add-on modules."""
    if not _LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    return _LOGGER

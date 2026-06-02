"""Safe JSON file helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .logger import get_logger

LOGGER = get_logger()


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from disk with explicit error reporting."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise RuntimeError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON file {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write a JSON object to disk using stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    LOGGER.info("Wrote JSON: %s", path)

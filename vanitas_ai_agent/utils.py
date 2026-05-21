"""Utility helpers for logging, file persistence, and JSON handling."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def utc_timestamp() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    """Create directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def append_jsonl(log_file: Path, payload: Dict[str, Any]) -> None:
    """Append one JSON object to a JSONL file."""
    ensure_dir(log_file.parent)
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    """Save dictionary to JSON file."""
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

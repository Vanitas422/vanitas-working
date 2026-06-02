"""Singleton user-configuration manager."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, ClassVar

import bpy

from .constants import ADDON_ID, CONFIG_FILENAME, USER_PRESET_DIRNAME
from .file_io import read_json, write_json
from .logger import get_logger

LOGGER = get_logger()


@dataclass(slots=True)
class UserSettings:
    """Serializable user preferences for persistent add-on state."""

    last_style: str = "genshin_impact"
    last_outline_mode: str = "INVERTED_HULL"
    api_provider: str = "HEURISTIC"
    openai_api_key: str = ""
    deepseek_api_key: str = ""
    batch_output: str = ""
    user_presets: list[str] = field(default_factory=list)


class SettingsManager:
    """Small singleton that persists settings in Blender's user resource path."""

    _instance: ClassVar["SettingsManager | None"] = None

    def __new__(cls) -> "SettingsManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = UserSettings()
        return cls._instance

    def base_dir(self) -> Path:
        """Return the add-on user directory."""
        resource = bpy.utils.user_resource("CONFIG", path=ADDON_ID, create=True)
        return Path(resource)

    def config_path(self) -> Path:
        """Return the user settings JSON path."""
        return self.base_dir() / CONFIG_FILENAME

    def user_preset_dir(self) -> Path:
        """Return the user preset directory."""
        path = self.base_dir() / USER_PRESET_DIRNAME
        path.mkdir(parents=True, exist_ok=True)
        return path

    def load(self) -> UserSettings:
        """Load settings from disk, keeping defaults for missing keys."""
        path = self.config_path()
        if not path.exists():
            return self.settings
        data = read_json(path)
        valid_keys = set(UserSettings.__dataclass_fields__.keys())
        merged: dict[str, Any] = asdict(self.settings)
        merged.update({key: value for key, value in data.items() if key in valid_keys})
        self.settings = UserSettings(**merged)
        LOGGER.info("Loaded settings from %s", path)
        return self.settings

    def save(self) -> None:
        """Persist settings to disk."""
        write_json(self.config_path(), asdict(self.settings))


settings_manager = SettingsManager()

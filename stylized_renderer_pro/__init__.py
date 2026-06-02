"""Stylized Renderer Pro add-on entry point."""

from __future__ import annotations

import bpy
from bpy.props import PointerProperty

from .operators import CLASSES as OPERATOR_CLASSES
from .styles.manager import style_manager
from .ui.panel import CLASSES as UI_CLASSES
from .utils.addon_properties import SRPProperties
from .utils.constants import ADDON_NAME, MIN_BLENDER_VERSION
from .utils.logger import get_logger
from .utils.settings import settings_manager

bl_info = {
    "name": ADDON_NAME,
    "author": "OpenAI Codex",
    "version": (1, 0, 0),
    "blender": MIN_BLENDER_VERSION,
    "location": "View3D > Sidebar > Stylized Renderer Pro",
    "description": "One-click game and animation style NPR renderer for Eevee Next and Cycles.",
    "category": "Render",
}

LOGGER = get_logger()
CLASSES = (SRPProperties, *OPERATOR_CLASSES, *UI_CLASSES)


def register() -> None:
    """Register Blender RNA classes and initialize presets/settings."""
    style_manager.load_all()
    settings_manager.load()
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.srp_props = PointerProperty(type=SRPProperties)
    LOGGER.info("%s registered", ADDON_NAME)


def unregister() -> None:
    """Unregister classes in reverse order and save settings."""
    if hasattr(bpy.types.Scene, "srp_props"):
        del bpy.types.Scene.srp_props
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    settings_manager.save()
    LOGGER.info("%s unregistered", ADDON_NAME)


if __name__ == "__main__":
    register()

"""Constants used by Stylized Renderer Pro.

The constants live in a standalone module so Blender-version-specific names can be
updated in one place when future Blender 5.x releases change defaults.
"""

from __future__ import annotations

from pathlib import Path

ADDON_ID = "stylized_renderer_pro"
ADDON_NAME = "Stylized Renderer Pro"
MIN_BLENDER_VERSION = (5, 1, 0)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PRESET_DIR = PACKAGE_ROOT / "styles" / "presets"
USER_PRESET_DIRNAME = "presets"
CONFIG_FILENAME = "settings.json"
STYLE_PROPERTY_NAME = "srp_style_preset"
MATERIAL_CATEGORY_PROPERTY = "srp_material_category"
OUTLINE_COLLECTION_NAME = "SRP_Inverted_Hull_Outlines"
LIGHTING_COLLECTION_NAME = "SRP_Lighting_Rig"
BATCH_OUTPUT_DIRNAME = "stylized_renderer_pro_batch"

MATERIAL_CATEGORIES = (
    "Skin",
    "Hair",
    "Eyes",
    "Metal",
    "Cloth",
    "Weapon",
    "Environment",
)

OUTLINE_MODES = (
    ("INVERTED_HULL", "Inverted Hull Outline", "Duplicate mesh shells with flipped-normal outline material"),
    ("FREESTYLE", "Freestyle Outline", "Use Blender Freestyle line rendering"),
    ("GEOMETRY_NODES", "Geometry Nodes Outline", "Use a Geometry Nodes modifier for outline metadata"),
)

LIGHTING_RIGS = (
    ("ANIME", "Anime Lighting", "Soft key light with strong rim and fill"),
    ("STUDIO", "Studio Lighting", "Three-point studio lighting"),
    ("OUTDOOR", "Outdoor Lighting", "Sun and cool sky fill"),
    ("NIGHT", "Night Lighting", "Low-key moonlight and colored rim"),
)

SKY_TYPES = (
    ("ANIME", "Anime Sky", "Clean saturated blue sky"),
    ("SUNSET", "Sunset Sky", "Warm sunset gradient"),
    ("NIGHT", "Night Sky", "Dark blue night atmosphere"),
    ("CYBERPUNK", "Cyberpunk Sky", "Neon magenta and cyan city mood"),
)

AI_PROVIDERS = (
    ("HEURISTIC", "Offline Heuristic", "Generate style settings without network access"),
    ("OPENAI", "OpenAI API", "Use an OpenAI-compatible style generation endpoint"),
    ("DEEPSEEK", "DeepSeek API", "Use a DeepSeek-compatible style generation endpoint"),
)

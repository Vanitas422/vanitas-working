"""Blender RNA properties for Stylized Renderer Pro."""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, FloatVectorProperty, StringProperty
from bpy.types import PropertyGroup

from ..styles.manager import style_manager
from .constants import AI_PROVIDERS, LIGHTING_RIGS, OUTLINE_MODES, SKY_TYPES


def style_items(self: PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dynamic preset enum items loaded from JSON presets."""
    return style_manager.enum_items()


class SRPProperties(PropertyGroup):
    """Scene-level UI state and style controls."""

    style_preset: EnumProperty(name="Style Preset", description="Active JSON style preset", items=style_items)
    blend_preset: EnumProperty(name="Blend Target", description="Second preset for style mixing", items=style_items)
    blend_factor: FloatProperty(name="Blend", min=0.0, max=1.0, default=0.0, description="Mix factor between active and target presets")
    outline_mode: EnumProperty(name="Outline Mode", items=OUTLINE_MODES, default="INVERTED_HULL")
    lighting_rig: EnumProperty(name="Lighting Rig", items=LIGHTING_RIGS, default="ANIME")
    sky_type: EnumProperty(name="Sky", items=SKY_TYPES, default="ANIME")
    ai_provider: EnumProperty(name="AI Provider", items=AI_PROVIDERS, default="HEURISTIC")
    ai_prompt: StringProperty(name="Prompt", default="赛博朋克原神风", description="Prompt used by AI style generator")
    openai_api_key: StringProperty(name="OpenAI API Key", subtype="PASSWORD", default="")
    deepseek_api_key: StringProperty(name="DeepSeek API Key", subtype="PASSWORD", default="")
    batch_output: StringProperty(name="Batch Output", subtype="DIR_PATH", default="")
    outline_width: FloatProperty(name="Outline Width", min=0.0, max=10.0, default=1.5)
    outline_color: FloatVectorProperty(name="Outline Color", subtype="COLOR", size=4, min=0.0, max=1.0, default=(0.03, 0.025, 0.02, 1.0))
    shadow_steps: FloatProperty(name="Shadow Steps", min=1.0, max=8.0, default=3.0)
    rim_light: FloatProperty(name="Rim Light", min=0.0, max=2.0, default=0.5)
    saturation: FloatProperty(name="Saturation", min=0.0, max=3.0, default=1.0)
    contrast: FloatProperty(name="Contrast", min=0.0, max=3.0, default=1.0)
    auto_save_config: BoolProperty(name="Auto Save User Config", default=True)

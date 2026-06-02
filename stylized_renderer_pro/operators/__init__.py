"""Operator registration list."""

from __future__ import annotations

from .ai_ops import SRP_OT_generate_ai_style
from .asset_ops import SRP_OT_mark_assets
from .batch_ops import SRP_OT_batch_render
from .light_ops import SRP_OT_create_lighting
from .material_ops import SRP_OT_apply_materials
from .outline_ops import SRP_OT_apply_outline
from .preset_ops import SRP_OT_apply_style, SRP_OT_export_preset, SRP_OT_import_preset, SRP_OT_reload_presets, SRP_OT_reset_defaults
from .render_ops import SRP_OT_setup_render_settings
from .sky_ops import SRP_OT_apply_sky

CLASSES = (
    SRP_OT_apply_style,
    SRP_OT_reload_presets,
    SRP_OT_import_preset,
    SRP_OT_export_preset,
    SRP_OT_reset_defaults,
    SRP_OT_apply_materials,
    SRP_OT_apply_outline,
    SRP_OT_create_lighting,
    SRP_OT_apply_sky,
    SRP_OT_generate_ai_style,
    SRP_OT_setup_render_settings,
    SRP_OT_batch_render,
    SRP_OT_mark_assets,
)

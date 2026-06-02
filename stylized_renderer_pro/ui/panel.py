"""N-panel UI for Stylized Renderer Pro."""

from __future__ import annotations

import bpy
from bpy.types import Panel


class SRP_PT_main_panel(Panel):
    """Root N-panel for the add-on."""

    bl_label = "Stylized Renderer Pro"
    bl_idname = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stylized Renderer Pro"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.label(text="Professional NPR Renderer", icon="SHADING_RENDERED")
        layout.operator("srp.apply_style", icon="PLAY")
        layout.operator("srp.reset_defaults", icon="LOOP_BACK")


class SRP_PT_style_presets(Panel):
    """Style preset controls."""

    bl_label = "Style Presets"
    bl_idname = "SRP_PT_style_presets"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        layout = self.layout
        layout.prop(props, "style_preset")
        layout.prop(props, "blend_preset")
        layout.prop(props, "blend_factor", slider=True)
        row = layout.row(align=True)
        row.operator("srp.reload_presets", icon="FILE_REFRESH")
        row.operator("srp.import_preset", icon="IMPORT")
        row.operator("srp.export_preset", icon="EXPORT")


class SRP_PT_lighting(Panel):
    """Lighting rig controls."""

    bl_label = "Lighting"
    bl_idname = "SRP_PT_lighting"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        self.layout.prop(props, "lighting_rig")
        self.layout.operator("srp.create_lighting", icon="LIGHT")


class SRP_PT_sky(Panel):
    """Sky controls."""

    bl_label = "Sky"
    bl_idname = "SRP_PT_sky"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        self.layout.prop(props, "sky_type")
        self.layout.operator("srp.apply_sky", icon="WORLD")


class SRP_PT_outline(Panel):
    """Outline controls."""

    bl_label = "Outline"
    bl_idname = "SRP_PT_outline"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        self.layout.prop(props, "outline_mode")
        self.layout.prop(props, "outline_width")
        self.layout.prop(props, "outline_color")
        self.layout.operator("srp.apply_outline", icon="MOD_SOLIDIFY")


class SRP_PT_materials(Panel):
    """Material automation controls."""

    bl_label = "Materials"
    bl_idname = "SRP_PT_materials"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        layout.label(text="Auto categories: Skin, Hair, Eyes, Metal, Cloth, Weapon, Environment")
        layout.operator("srp.apply_materials", icon="MATERIAL")
        layout.operator("srp.mark_assets", icon="ASSET_MANAGER")


class SRP_PT_ai_generator(Panel):
    """AI generator panel."""

    bl_label = "AI Generator"
    bl_idname = "SRP_PT_ai_generator"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        layout = self.layout
        layout.prop(props, "ai_provider")
        layout.prop(props, "ai_prompt")
        if props.ai_provider == "OPENAI":
            layout.prop(props, "openai_api_key")
        if props.ai_provider == "DEEPSEEK":
            layout.prop(props, "deepseek_api_key")
        layout.operator("srp.generate_ai_style", icon="SPARKLES")


class SRP_PT_render_settings(Panel):
    """Render settings and batch tools."""

    bl_label = "Render Settings"
    bl_idname = "SRP_PT_render_settings"
    bl_parent_id = "SRP_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        props = context.scene.srp_props
        layout = self.layout
        layout.prop(props, "shadow_steps")
        layout.prop(props, "rim_light")
        layout.prop(props, "saturation")
        layout.prop(props, "contrast")
        layout.operator("srp.setup_render_settings", icon="RENDER_STILL")
        layout.prop(props, "batch_output")
        layout.operator("srp.batch_render", icon="RENDER_ANIMATION")
        layout.prop(props, "auto_save_config")


CLASSES = (
    SRP_PT_main_panel,
    SRP_PT_style_presets,
    SRP_PT_lighting,
    SRP_PT_sky,
    SRP_PT_outline,
    SRP_PT_materials,
    SRP_PT_ai_generator,
    SRP_PT_render_settings,
)

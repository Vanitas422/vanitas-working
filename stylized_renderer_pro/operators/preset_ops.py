"""Style preset operators."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.props import StringProperty
from bpy.types import Operator

from ..materials.applier import material_applier
from ..outline.manager import outline_manager
from ..styles.manager import style_manager
from ..styles.preset import StyleParameters
from ..utils.settings import settings_manager


def active_parameters(scene: bpy.types.Scene) -> StyleParameters:
    """Resolve active style parameters, including optional blending."""
    props = scene.srp_props
    if props.blend_factor > 0.0:
        return style_manager.blend(props.style_preset, props.blend_preset, props.blend_factor).parameters
    return style_manager.get(props.style_preset).parameters


def sync_ui_from_parameters(scene: bpy.types.Scene, params: StyleParameters) -> None:
    """Copy parameter values into editable UI controls."""
    props = scene.srp_props
    props.outline_width = params.outline_width
    props.outline_color = params.outline_color
    props.shadow_steps = float(params.shadow_steps)
    props.rim_light = params.rim_light
    props.saturation = params.saturation
    props.contrast = params.contrast


class SRP_OT_apply_style(Operator):
    """Apply the active style preset to render settings, materials, and outlines."""

    bl_idname = "srp.apply_style"
    bl_label = "Apply Style"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        params = active_parameters(context.scene)
        sync_ui_from_parameters(context.scene, params)
        material_count = material_applier.apply_to_scene(context.scene, params)
        outline_manager.apply(context.scene, context.scene.srp_props.outline_mode, params)
        self._apply_render_settings(context.scene, params)
        settings_manager.settings.last_style = context.scene.srp_props.style_preset
        settings_manager.settings.last_outline_mode = context.scene.srp_props.outline_mode
        if context.scene.srp_props.auto_save_config:
            settings_manager.save()
        self.report({"INFO"}, f"Applied style to {material_count} material slots")
        return {"FINISHED"}

    def _apply_render_settings(self, scene: bpy.types.Scene, params: StyleParameters) -> None:
        """Configure Eevee Next/Cycles-friendly render effects."""
        scene.render.engine = scene.render.engine if scene.render.engine in {"BLENDER_EEVEE_NEXT", "CYCLES"} else "BLENDER_EEVEE_NEXT"
        if hasattr(scene, "eevee"):
            scene.eevee.use_gtao = params.ambient_occlusion > 0.0
            scene.eevee.gtao_distance = max(1.0, params.ambient_occlusion * 4.0)
            scene.eevee.use_bloom = params.bloom > 0.0
            scene.eevee.bloom_intensity = params.bloom
        scene.view_settings.view_transform = "Standard"
        valid_looks = {item.identifier for item in scene.view_settings.bl_rna.properties["look"].enum_items}
        scene.view_settings.look = params.color_grading if params.color_grading in valid_looks else "None"
        scene.view_settings.exposure = 0.0
        scene.view_settings.gamma = max(0.1, 1.0 / max(0.1, params.contrast))
        if scene.camera:
            scene.camera.data.dof.use_dof = params.depth_of_field > 0.0
            scene.camera.data.dof.aperture_fstop = max(0.1, 5.6 - params.depth_of_field * 4.0)


class SRP_OT_reload_presets(Operator):
    """Reload preset JSON files from disk."""

    bl_idname = "srp.reload_presets"
    bl_label = "Reload Presets"
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        style_manager.load_all()
        self.report({"INFO"}, "Reloaded Stylized Renderer Pro presets")
        return {"FINISHED"}


class SRP_OT_import_preset(Operator):
    """Import a preset JSON file into the user preset library."""

    bl_idname = "srp.import_preset"
    bl_label = "Import Preset"
    bl_options = {"REGISTER", "UNDO"}
    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context: bpy.types.Context) -> set[str]:
        preset = style_manager.import_preset(Path(self.filepath))
        context.scene.srp_props.style_preset = preset.identifier
        self.report({"INFO"}, f"Imported preset {preset.display_name}")
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class SRP_OT_export_preset(Operator):
    """Export the active preset JSON file."""

    bl_idname = "srp.export_preset"
    bl_label = "Export Preset"
    bl_options = {"REGISTER"}
    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context: bpy.types.Context) -> set[str]:
        style_manager.export_preset(context.scene.srp_props.style_preset, Path(self.filepath))
        self.report({"INFO"}, "Exported active preset")
        return {"FINISHED"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class SRP_OT_reset_defaults(Operator):
    """Restore the default Genshin-style preset and outline mode."""

    bl_idname = "srp.reset_defaults"
    bl_label = "Restore Defaults"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        context.scene.srp_props.style_preset = "genshin_impact"
        context.scene.srp_props.blend_factor = 0.0
        context.scene.srp_props.outline_mode = "INVERTED_HULL"
        return bpy.ops.srp.apply_style()

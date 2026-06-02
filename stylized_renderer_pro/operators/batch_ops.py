"""Batch render operators."""

from __future__ import annotations

from pathlib import Path

import bpy
from bpy.types import Operator

from ..styles.manager import style_manager
from ..utils.constants import BATCH_OUTPUT_DIRNAME


class SRP_OT_batch_render(Operator):
    """Render the scene once per style preset."""

    bl_idname = "srp.batch_render"
    bl_label = "Batch Render Styles"
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        props = context.scene.srp_props
        output_dir = Path(props.batch_output or bpy.path.abspath(f"//{BATCH_OUTPUT_DIRNAME}"))
        output_dir.mkdir(parents=True, exist_ok=True)
        original_path = context.scene.render.filepath
        original_style = props.style_preset
        for preset in style_manager.presets():
            props.style_preset = preset.identifier
            bpy.ops.srp.apply_style()
            context.scene.render.filepath = str(output_dir / f"{preset.identifier}.png")
            bpy.ops.render.render(write_still=True)
        props.style_preset = original_style
        context.scene.render.filepath = original_path
        self.report({"INFO"}, f"Batch rendered {len(style_manager.presets())} presets")
        return {"FINISHED"}

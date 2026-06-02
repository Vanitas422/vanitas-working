"""Asset Browser support operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator


class SRP_OT_mark_assets(Operator):
    """Mark generated SRP materials and worlds as Asset Browser assets."""

    bl_idname = "srp.mark_assets"
    bl_label = "Mark SRP Assets"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        count = 0
        for material in bpy.data.materials:
            if material.get("SRP_Unified_NPR_Shader"):
                material.asset_mark()
                material.asset_data.description = "Stylized Renderer Pro NPR material"
                count += 1
        if context.scene.world:
            context.scene.world.asset_mark()
            context.scene.world.asset_data.description = "Stylized Renderer Pro world sky"
            count += 1
        self.report({"INFO"}, f"Marked {count} assets")
        return {"FINISHED"}

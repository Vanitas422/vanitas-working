"""Material operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator

from .preset_ops import active_parameters
from ..materials.applier import material_applier


class SRP_OT_apply_materials(Operator):
    """Apply the unified NPR shader to all scene objects."""

    bl_idname = "srp.apply_materials"
    bl_label = "Apply to All Objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        count = material_applier.apply_to_scene(context.scene, active_parameters(context.scene))
        self.report({"INFO"}, f"Updated {count} material slots")
        return {"FINISHED"}

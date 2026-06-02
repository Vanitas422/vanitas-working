"""Lighting operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator

from ..lighting.manager import lighting_manager


class SRP_OT_create_lighting(Operator):
    """Create the selected stylized lighting rig."""

    bl_idname = "srp.create_lighting"
    bl_label = "Create Lighting Rig"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        lighting_manager.create_rig(context.scene, context.scene.srp_props.lighting_rig)
        self.report({"INFO"}, "Created lighting rig")
        return {"FINISHED"}

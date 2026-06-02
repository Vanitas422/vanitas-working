"""Sky operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator

from ..sky.manager import sky_manager


class SRP_OT_apply_sky(Operator):
    """Apply the selected stylized sky."""

    bl_idname = "srp.apply_sky"
    bl_label = "Apply Sky"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        sky_manager.apply(context.scene, context.scene.srp_props.sky_type)
        self.report({"INFO"}, "Applied stylized sky")
        return {"FINISHED"}

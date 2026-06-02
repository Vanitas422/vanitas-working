"""Outline operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator

from .preset_ops import active_parameters
from ..outline.manager import outline_manager


class SRP_OT_apply_outline(Operator):
    """Apply the selected outline mode."""

    bl_idname = "srp.apply_outline"
    bl_label = "Apply Outline"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        outline_manager.apply(context.scene, context.scene.srp_props.outline_mode, active_parameters(context.scene))
        self.report({"INFO"}, "Applied outline mode")
        return {"FINISHED"}

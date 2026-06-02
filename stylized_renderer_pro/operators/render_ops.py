"""Render settings operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator


class SRP_OT_setup_render_settings(Operator):
    """Configure renderer defaults for Eevee Next or Cycles NPR workflows."""

    bl_idname = "srp.setup_render_settings"
    bl_label = "Setup Render Settings"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        if scene.render.engine not in {"BLENDER_EEVEE_NEXT", "CYCLES"}:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        scene.render.film_transparent = False
        scene.view_settings.view_transform = "Standard"
        scene.view_settings.look = "None"
        scene.render.resolution_percentage = 100
        self.report({"INFO"}, "Configured Stylized Renderer Pro render settings")
        return {"FINISHED"}

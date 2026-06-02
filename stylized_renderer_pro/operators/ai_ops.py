"""AI generator operators."""

from __future__ import annotations

import bpy
from bpy.types import Operator

from ..ai.generator import ai_generator
from ..styles.manager import style_manager
from ..utils.settings import settings_manager


class SRP_OT_generate_ai_style(Operator):
    """Generate and apply a new style preset from prompt text."""

    bl_idname = "srp.generate_ai_style"
    bl_label = "Generate AI Style"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        props = context.scene.srp_props
        settings_manager.settings.api_provider = props.ai_provider
        settings_manager.settings.openai_api_key = props.openai_api_key
        settings_manager.settings.deepseek_api_key = props.deepseek_api_key
        try:
            parameters = ai_generator.generate_parameters(props.ai_prompt)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        preset = style_manager.add_generated(ai_generator.identifier_for_prompt(props.ai_prompt), f"AI: {props.ai_prompt[:32]}", parameters)
        props.style_preset = preset.identifier
        settings_manager.save()
        bpy.ops.srp.apply_style()
        self.report({"INFO"}, "Generated AI style preset")
        return {"FINISHED"}

"""Apply unified NPR materials to scene objects."""

from __future__ import annotations

import bpy
from bpy.types import Object

from ..shaders.npr_shader import shader_builder
from ..styles.preset import StyleParameters
from ..utils.logger import get_logger
from .classifier import classifier

LOGGER = get_logger()


class MaterialApplier:
    """Assign style-aware NPR settings to materials."""

    def apply_to_object(self, obj: Object, params: StyleParameters) -> int:
        """Apply the style to every material slot on an object."""
        count = 0
        if not hasattr(obj.data, "materials"):
            return count
        for slot in obj.material_slots:
            material = slot.material
            if material is None:
                material = bpy.data.materials.new(f"SRP_{obj.name}_Material")
                slot.material = material
            category = classifier.classify(material, obj)
            shader_builder.apply(material, params, category)
            count += 1
        if not obj.material_slots and obj.type == "MESH":
            material = bpy.data.materials.new(f"SRP_{obj.name}_Material")
            obj.data.materials.append(material)
            category = classifier.classify(material, obj)
            shader_builder.apply(material, params, category)
            count += 1
        return count

    def apply_to_scene(self, scene: bpy.types.Scene, params: StyleParameters) -> int:
        """Apply the active style to all mesh-like scene objects."""
        total = 0
        for obj in scene.objects:
            if obj.type in {"MESH", "CURVE", "SURFACE"}:
                total += self.apply_to_object(obj, params)
        LOGGER.info("Applied NPR material style to %d material slots", total)
        return total


material_applier = MaterialApplier()

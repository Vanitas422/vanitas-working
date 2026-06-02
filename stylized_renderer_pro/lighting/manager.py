"""Lighting rig creation utilities."""

from __future__ import annotations

import bpy
from mathutils import Vector

from ..utils.constants import LIGHTING_COLLECTION_NAME


class LightingManager:
    """Create named production lighting rigs."""

    def create_rig(self, scene: bpy.types.Scene, rig: str) -> None:
        """Replace the current SRP rig with the requested rig."""
        self.clear(scene)
        collection = bpy.data.collections.new(LIGHTING_COLLECTION_NAME)
        scene.collection.children.link(collection)
        if rig == "STUDIO":
            specs = [("Key", "AREA", (3, -4, 5), 650, 4), ("Fill", "AREA", (-4, 3, 3), 180, 5), ("Rim", "POINT", (-2, 4, 4), 260, 0)]
        elif rig == "OUTDOOR":
            specs = [("Sun", "SUN", (0, 0, 5), 2.8, 0), ("Sky Fill", "AREA", (-3, 2, 5), 220, 6)]
        elif rig == "NIGHT":
            specs = [("Moon", "SUN", (0, 0, 5), 0.8, 0), ("Blue Rim", "POINT", (3, 4, 3), 350, 0), ("Warm Window", "AREA", (-3, -2, 2), 80, 3)]
        else:
            specs = [("Anime Key", "AREA", (3, -4, 4), 450, 5), ("Anime Fill", "AREA", (-4, 3, 3), 120, 6), ("Anime Rim", "POINT", (-2, 4, 4), 320, 0)]
        for name, kind, location, energy, size in specs:
            light_data = bpy.data.lights.new(f"SRP {name}", kind)
            light_data.energy = energy
            if kind == "AREA":
                light_data.size = size
            obj = bpy.data.objects.new(f"SRP {name}", light_data)
            obj.location = location
            self._look_at_origin(obj)
            collection.objects.link(obj)

    def clear(self, scene: bpy.types.Scene) -> None:
        """Remove the existing SRP lighting collection."""
        collection = bpy.data.collections.get(LIGHTING_COLLECTION_NAME)
        if collection is None:
            return
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)

    def _look_at_origin(self, obj: bpy.types.Object) -> None:
        """Aim an object at world origin."""
        direction = Vector((0.0, 0.0, 0.0)) - obj.location
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


lighting_manager = LightingManager()

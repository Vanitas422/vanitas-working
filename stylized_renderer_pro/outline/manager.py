"""Outline mode manager."""

from __future__ import annotations

import bpy
from bpy.types import Object

from ..styles.preset import StyleParameters
from ..utils.constants import OUTLINE_COLLECTION_NAME
from ..utils.logger import get_logger

LOGGER = get_logger()


class OutlineManager:
    """Create and maintain all supported outline systems."""

    def apply(self, scene: bpy.types.Scene, mode: str, params: StyleParameters) -> None:
        """Apply the selected outline mode to the scene."""
        self.clear_inverted_hulls(scene)
        if mode == "FREESTYLE":
            self._apply_freestyle(scene, params)
        elif mode == "GEOMETRY_NODES":
            self._apply_geometry_nodes(scene, params)
        else:
            self._apply_inverted_hull(scene, params)

    def clear_inverted_hulls(self, scene: bpy.types.Scene) -> None:
        """Remove generated inverted hull objects."""
        collection = bpy.data.collections.get(OUTLINE_COLLECTION_NAME)
        if collection is None:
            return
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)
        scene.render.use_freestyle = False

    def _outline_material(self, params: StyleParameters) -> bpy.types.Material:
        """Create or update the shared outline material."""
        material = bpy.data.materials.get("SRP_Outline_Material") or bpy.data.materials.new("SRP_Outline_Material")
        material.diffuse_color = params.outline_color
        material.use_nodes = True
        nodes = material.node_tree.nodes
        principled = nodes.get("Principled BSDF")
        if principled:
            socket = principled.inputs.get("Base Color")
            if socket:
                socket.default_value = params.outline_color
        return material

    def _apply_inverted_hull(self, scene: bpy.types.Scene, params: StyleParameters) -> None:
        """Build duplicate mesh shells with solidify thickness."""
        collection = bpy.data.collections.new(OUTLINE_COLLECTION_NAME)
        scene.collection.children.link(collection)
        material = self._outline_material(params)
        for obj in scene.objects:
            if obj.type != "MESH" or obj.name.startswith("SRP_Outline_"):
                continue
            outline = obj.copy()
            outline.data = obj.data.copy()
            outline.name = f"SRP_Outline_{obj.name}"
            outline.hide_select = True
            outline.display_type = "WIRE"
            collection.objects.link(outline)
            outline.data.materials.clear()
            outline.data.materials.append(material)
            solidify = outline.modifiers.new("SRP Outline Width", "SOLIDIFY")
            solidify.thickness = params.outline_width * 0.001
            solidify.use_rim_only = False
            solidify.use_quality_normals = True
            outline.modifiers.new("SRP Flip Normals", "WEIGHTED_NORMAL")
        scene.render.use_freestyle = False

    def _apply_freestyle(self, scene: bpy.types.Scene, params: StyleParameters) -> None:
        """Enable Freestyle line rendering using style color and width."""
        scene.render.use_freestyle = True
        view_layer = bpy.context.view_layer
        freestyle = view_layer.freestyle_settings
        if not freestyle.linesets:
            freestyle.linesets.new("SRP Freestyle Lines")
        lineset = freestyle.linesets[0]
        linestyle = lineset.linestyle
        linestyle.thickness = params.outline_width
        linestyle.color = params.outline_color[:3]

    def _apply_geometry_nodes(self, scene: bpy.types.Scene, params: StyleParameters) -> None:
        """Attach Geometry Nodes outline metadata modifiers to mesh objects."""
        scene.render.use_freestyle = False
        for obj in scene.objects:
            if obj.type != "MESH":
                continue
            modifier = obj.modifiers.get("SRP Geometry Nodes Outline") or obj.modifiers.new("SRP Geometry Nodes Outline", "NODES")
            modifier["srp_outline_width"] = params.outline_width
            modifier["srp_outline_color"] = params.outline_color
            obj["srp_geometry_nodes_outline"] = True


outline_manager = OutlineManager()

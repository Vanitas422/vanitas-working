"""Procedural world sky creation."""

from __future__ import annotations

import bpy


_SKY_COLORS: dict[str, tuple[float, float, float, float]] = {
    "ANIME": (0.42, 0.68, 1.0, 1.0),
    "SUNSET": (1.0, 0.45, 0.22, 1.0),
    "NIGHT": (0.02, 0.04, 0.12, 1.0),
    "CYBERPUNK": (0.18, 0.02, 0.28, 1.0),
}


class SkyManager:
    """Build simple procedural world node setups for stylized skies."""

    def apply(self, scene: bpy.types.Scene, sky_type: str) -> None:
        """Create or update the scene World nodes."""
        world = scene.world or bpy.data.worlds.new("SRP World")
        scene.world = world
        world.use_nodes = True
        nodes = world.node_tree.nodes
        output = nodes.get("World Output") or nodes.new("ShaderNodeOutputWorld")
        background = nodes.get("SRP Stylized Sky") or nodes.new("ShaderNodeBackground")
        background.name = "SRP Stylized Sky"
        background.inputs[0].default_value = _SKY_COLORS.get(sky_type, _SKY_COLORS["ANIME"])
        background.inputs[1].default_value = 0.85 if sky_type != "NIGHT" else 0.25
        if not any(link.from_node == background and link.to_node == output for link in world.node_tree.links):
            world.node_tree.links.new(background.outputs[0], output.inputs[0])
        world["srp_sky_type"] = sky_type


sky_manager = SkyManager()

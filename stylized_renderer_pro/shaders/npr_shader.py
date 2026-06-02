"""Unified NPR shader graph construction.

Every preset uses this single material architecture. Presets only alter node
values and material custom properties, which keeps the add-on maintainable and
future Blender 5.x upgrades localized to this module.
"""

from __future__ import annotations

import bpy
from bpy.types import Material

from ..styles.preset import CategoryOverride, StyleParameters
from ..utils.constants import MATERIAL_CATEGORY_PROPERTY
from ..utils.logger import get_logger

LOGGER = get_logger()


class NPRShaderBuilder:
    """Build and update the shared stylized material node tree."""

    SHADER_TAG = "SRP_Unified_NPR_Shader"

    def apply(self, material: Material, params: StyleParameters, category: str) -> None:
        """Apply the unified NPR graph and category-adjusted parameters."""
        material.use_nodes = True
        material[MATERIAL_CATEGORY_PROPERTY] = category
        material[self.SHADER_TAG] = True
        override = params.material_overrides.get(category, CategoryOverride())
        self._ensure_nodes(material, params, override)
        self._store_custom_properties(material, params, override)

    def _ensure_nodes(
        self,
        material: Material,
        params: StyleParameters,
        override: CategoryOverride,
    ) -> None:
        """Create or update a Principled-based NPR node layout."""
        node_tree = material.node_tree
        nodes = node_tree.nodes
        links = node_tree.links
        output = nodes.get("Material Output") or nodes.new("ShaderNodeOutputMaterial")
        principled = nodes.get("SRP NPR Principled") or nodes.new("ShaderNodeBsdfPrincipled")
        principled.name = "SRP NPR Principled"
        principled.label = "Unified NPR Surface"
        principled.location = (100, 120)

        ramp = nodes.get("SRP Toon Shadow Ramp") or nodes.new("ShaderNodeValToRGB")
        ramp.name = "SRP Toon Shadow Ramp"
        ramp.label = "Shadow Steps"
        ramp.location = (-420, 160)
        ramp.color_ramp.interpolation = "CONSTANT"
        self._configure_shadow_ramp(ramp, params)

        color = nodes.get("SRP Base Color") or nodes.new("ShaderNodeRGB")
        color.name = "SRP Base Color"
        color.label = "Style-Tinted Base Color"
        color.location = (-650, 220)
        color.outputs[0].default_value = self._adjust_color(material.diffuse_color, params, override)

        emission = nodes.get("SRP Rim Emission") or nodes.new("ShaderNodeEmission")
        emission.name = "SRP Rim Emission"
        emission.label = "Rim Light Metadata"
        emission.location = (-130, -160)
        emission.inputs[0].default_value = params.rim_light_color
        emission.inputs[1].default_value = params.rim_light

        self._set_input(principled, "Base Color", color.outputs[0].default_value)
        self._set_input(principled, "Metallic", override.metallic)
        self._set_input(principled, "Roughness", override.roughness)
        self._set_input(principled, "Specular IOR Level", override.specular_strength)
        self._set_input(principled, "Specular", override.specular_strength)

        if not self._has_link(links, principled, output):
            links.new(principled.outputs[0], output.inputs[0])

    def _configure_shadow_ramp(self, ramp: bpy.types.Node, params: StyleParameters) -> None:
        """Create constant ramp stops matching the requested shadow step count."""
        color_ramp = ramp.color_ramp
        while len(color_ramp.elements) < max(2, params.shadow_steps):
            color_ramp.elements.new(0.5)
        while len(color_ramp.elements) > max(2, params.shadow_steps):
            color_ramp.elements.remove(color_ramp.elements[-1])
        count = len(color_ramp.elements)
        for index, element in enumerate(color_ramp.elements):
            factor = index / max(1, count - 1)
            element.position = factor
            element.color = tuple(
                params.shadow_color[channel] * (1.0 - factor) + factor
                for channel in range(4)
            )

    def _store_custom_properties(
        self,
        material: Material,
        params: StyleParameters,
        override: CategoryOverride,
    ) -> None:
        """Store parameters for render operators and pipeline tooling."""
        material["srp_outline_width"] = params.outline_width
        material["srp_shadow_steps"] = params.shadow_steps
        material["srp_rim_light"] = params.rim_light
        material["srp_saturation"] = params.saturation * override.saturation
        material["srp_contrast"] = params.contrast * override.contrast
        material["srp_color_grading"] = params.color_grading

    def _adjust_color(
        self,
        color: tuple[float, float, float, float],
        params: StyleParameters,
        override: CategoryOverride,
    ) -> tuple[float, float, float, float]:
        """Approximate saturation and contrast adjustment for material base color."""
        r, g, b, a = color
        luminance = r * 0.2126 + g * 0.7152 + b * 0.0722
        saturation = params.saturation * override.saturation
        contrast = params.contrast * override.contrast
        adjusted = []
        for channel in (r, g, b):
            saturated = luminance + (channel - luminance) * saturation
            contrasted = 0.5 + (saturated - 0.5) * contrast
            adjusted.append(max(0.0, min(1.0, contrasted)))
        return (adjusted[0], adjusted[1], adjusted[2], a)

    def _set_input(self, node: bpy.types.Node, name: str, value: object) -> None:
        """Set a node input when it exists in the current Blender version."""
        socket = node.inputs.get(name)
        if socket is not None:
            socket.default_value = value

    def _has_link(self, links: bpy.types.NodeLinks, source: bpy.types.Node, target: bpy.types.Node) -> bool:
        """Return whether two nodes are already linked."""
        return any(link.from_node == source and link.to_node == target for link in links)


shader_builder = NPRShaderBuilder()

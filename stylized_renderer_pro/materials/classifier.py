"""Automatic material-category recognition."""

from __future__ import annotations

import re

import bpy
from bpy.types import Material, Object

from ..utils.constants import MATERIAL_CATEGORIES, MATERIAL_CATEGORY_PROPERTY

_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Skin": ("skin", "face", "body", "hand", "leg", "肌", "皮肤", "body"),
    "Hair": ("hair", "bang", "ponytail", "braid", "头发", "发"),
    "Eyes": ("eye", "iris", "pupil", "瞳", "眼"),
    "Metal": ("metal", "steel", "iron", "gold", "silver", "chrome", "金属"),
    "Cloth": ("cloth", "fabric", "shirt", "coat", "dress", "skirt", "衣", "布"),
    "Weapon": ("weapon", "sword", "gun", "blade", "bow", "rifle", "武器", "刀", "枪"),
    "Environment": ("env", "ground", "wall", "tree", "rock", "building", "terrain", "场景"),
}


class MaterialClassifier:
    """Classify materials into NPR semantic categories."""

    def classify(self, material: Material | None, obj: Object | None = None) -> str:
        """Return the best category for a material/object pair."""
        if material and material.get(MATERIAL_CATEGORY_PROPERTY) in MATERIAL_CATEGORIES:
            return str(material[MATERIAL_CATEGORY_PROPERTY])
        haystack = " ".join(filter(None, [material.name if material else "", obj.name if obj else ""]))
        normalized = re.sub(r"[^\w\u4e00-\u9fff]+", " ", haystack.lower())
        for category, keywords in _KEYWORDS.items():
            if any(keyword in normalized for keyword in keywords):
                return category
        if material and self._looks_metallic(material):
            return "Metal"
        if obj and obj.type in {"MESH", "CURVE", "SURFACE"} and any(token in obj.name.lower() for token in ("prop", "scene", "level")):
            return "Environment"
        return "Cloth"

    def _looks_metallic(self, material: Material) -> bool:
        """Inspect common Principled BSDF sockets for a metallic hint."""
        if not material.use_nodes or not material.node_tree:
            return False
        for node in material.node_tree.nodes:
            if node.bl_idname == "ShaderNodeBsdfPrincipled":
                socket = node.inputs.get("Metallic")
                return bool(socket and socket.default_value > 0.45)
        return False


classifier = MaterialClassifier()

"""Dataclasses representing style presets and parameter blending."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

Color = tuple[float, float, float, float]


def _color(value: Any, default: Color) -> Color:
    """Normalize JSON color arrays to RGBA tuples."""
    if isinstance(value, (list, tuple)) and len(value) in {3, 4}:
        items = [float(channel) for channel in value]
        if len(items) == 3:
            items.append(1.0)
        return (items[0], items[1], items[2], items[3])
    return default


@dataclass(slots=True)
class CategoryOverride:
    """Per-material-category scalar modifiers."""

    saturation: float = 1.0
    contrast: float = 1.0
    specular_strength: float = 0.35
    roughness: float = 0.55
    metallic: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "CategoryOverride":
        """Create an override from optional JSON data."""
        data = data or {}
        return cls(
            saturation=float(data.get("saturation", 1.0)),
            contrast=float(data.get("contrast", 1.0)),
            specular_strength=float(data.get("specular_strength", 0.35)),
            roughness=float(data.get("roughness", 0.55)),
            metallic=float(data.get("metallic", 0.0)),
        )


@dataclass(slots=True)
class StyleParameters:
    """Unified NPR parameter block shared by every style."""

    outline_width: float = 1.5
    outline_color: Color = (0.03, 0.025, 0.02, 1.0)
    shadow_steps: int = 3
    shadow_color: Color = (0.45, 0.38, 0.42, 1.0)
    rim_light: float = 0.45
    rim_light_color: Color = (0.85, 0.95, 1.0, 1.0)
    specular_strength: float = 0.35
    saturation: float = 1.0
    contrast: float = 1.0
    ambient_occlusion: float = 0.6
    bloom: float = 0.25
    depth_of_field: float = 0.0
    fog: float = 0.0
    color_grading: str = "Neutral"
    material_overrides: dict[str, CategoryOverride] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StyleParameters":
        """Parse style parameters from a JSON object."""
        overrides = {
            key: CategoryOverride.from_dict(value)
            for key, value in data.get("material_overrides", {}).items()
            if isinstance(value, dict)
        }
        return cls(
            outline_width=float(data.get("outline_width", data.get("outline", 1.5))),
            outline_color=_color(data.get("outline_color"), (0.03, 0.025, 0.02, 1.0)),
            shadow_steps=int(data.get("shadow_steps", 3)),
            shadow_color=_color(data.get("shadow_color"), (0.45, 0.38, 0.42, 1.0)),
            rim_light=float(data.get("rim_light", 0.45)),
            rim_light_color=_color(data.get("rim_light_color"), (0.85, 0.95, 1.0, 1.0)),
            specular_strength=float(data.get("specular_strength", 0.35)),
            saturation=float(data.get("saturation", 1.0)),
            contrast=float(data.get("contrast", 1.0)),
            ambient_occlusion=float(data.get("ambient_occlusion", 0.6)),
            bloom=float(data.get("bloom", 0.25)),
            depth_of_field=float(data.get("depth_of_field", 0.0)),
            fog=float(data.get("fog", 0.0)),
            color_grading=str(data.get("color_grading", "Neutral")),
            material_overrides=overrides,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize parameters to JSON-compatible values."""
        data = asdict(self)
        data["outline_color"] = list(self.outline_color)
        data["shadow_color"] = list(self.shadow_color)
        data["rim_light_color"] = list(self.rim_light_color)
        return data

    def blended(self, other: "StyleParameters", factor: float) -> "StyleParameters":
        """Return a linear blend between this parameter set and another."""
        factor = max(0.0, min(1.0, factor))

        def lerp(a: float, b: float) -> float:
            return a + (b - a) * factor

        def lerp_color(a: Color, b: Color) -> Color:
            return tuple(lerp(a[index], b[index]) for index in range(4))  # type: ignore[return-value]

        result = StyleParameters(
            outline_width=lerp(self.outline_width, other.outline_width),
            outline_color=lerp_color(self.outline_color, other.outline_color),
            shadow_steps=round(lerp(float(self.shadow_steps), float(other.shadow_steps))),
            shadow_color=lerp_color(self.shadow_color, other.shadow_color),
            rim_light=lerp(self.rim_light, other.rim_light),
            rim_light_color=lerp_color(self.rim_light_color, other.rim_light_color),
            specular_strength=lerp(self.specular_strength, other.specular_strength),
            saturation=lerp(self.saturation, other.saturation),
            contrast=lerp(self.contrast, other.contrast),
            ambient_occlusion=lerp(self.ambient_occlusion, other.ambient_occlusion),
            bloom=lerp(self.bloom, other.bloom),
            depth_of_field=lerp(self.depth_of_field, other.depth_of_field),
            fog=lerp(self.fog, other.fog),
            color_grading=other.color_grading if factor >= 0.5 else self.color_grading,
            material_overrides={**self.material_overrides, **other.material_overrides},
        )
        return result


@dataclass(slots=True)
class StylePreset:
    """Named style preset loaded from JSON."""

    identifier: str
    display_name: str
    category: str
    description: str
    parameters: StyleParameters

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StylePreset":
        """Build a style preset from JSON data."""
        return cls(
            identifier=str(data["identifier"]),
            display_name=str(data.get("display_name", data["identifier"])),
            category=str(data.get("category", "Custom")),
            description=str(data.get("description", "")),
            parameters=StyleParameters.from_dict(data.get("parameters", data)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize a preset to a JSON object."""
        return {
            "identifier": self.identifier,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "parameters": self.parameters.to_dict(),
        }

"""AI provider abstractions for prompt-to-style generation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class GeneratedStyle:
    """Normalized AI output used by the UI and style manager."""

    outline: float = 1.5
    shadow_steps: int = 3
    rim_light: float = 0.5
    saturation: float = 1.0
    contrast: float = 1.0
    fog: float = 0.0
    bloom: float = 0.25

    def to_parameters_dict(self) -> dict[str, float | int]:
        """Return keys matching StyleParameters JSON aliases."""
        return {
            "outline_width": self.outline,
            "shadow_steps": self.shadow_steps,
            "rim_light": self.rim_light,
            "saturation": self.saturation,
            "contrast": self.contrast,
            "fog": self.fog,
            "bloom": self.bloom,
        }


class AIProvider(ABC):
    """Abstract API for external and offline style generators."""

    @abstractmethod
    def generate(self, prompt: str) -> GeneratedStyle:
        """Generate style settings from user text."""


class HeuristicStyleProvider(AIProvider):
    """Offline deterministic provider used when no external API is configured."""

    def generate(self, prompt: str) -> GeneratedStyle:
        """Generate plausible settings from Chinese/English style keywords."""
        text = prompt.lower()
        style = GeneratedStyle()
        if any(token in text for token in ("赛博", "cyber", "neon")):
            style.outline = 1.9
            style.rim_light = 0.78
            style.saturation = 1.32
            style.contrast = 1.22
            style.fog = 0.24
            style.bloom = 0.65
        if any(token in text for token in ("原神", "genshin", "fantasy")):
            style.outline = (style.outline + 1.6) / 2.0
            style.shadow_steps = 3
            style.saturation = max(style.saturation, 1.18)
            style.contrast = max(style.contrast, 1.08)
        if any(token in text for token in ("黑白", "manga", "漫画")):
            style.outline = 2.7
            style.shadow_steps = 2
            style.saturation = 0.05
            style.contrast = 1.7
            style.bloom = 0.0
        if any(token in text for token in ("水彩", "watercolor")):
            style.outline = 1.0
            style.shadow_steps = 5
            style.saturation = 0.88
            style.contrast = 0.78
            style.fog = 0.18
        return style

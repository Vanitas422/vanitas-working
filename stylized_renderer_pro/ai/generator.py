"""AI style-generation facade."""

from __future__ import annotations

from ..styles.preset import StyleParameters
from ..utils.settings import settings_manager
from .base import AIProvider, GeneratedStyle, HeuristicStyleProvider
from .providers.deepseek import DeepSeekStyleProvider
from .providers.openai import OpenAIStyleProvider


def _safe_slug(text: str) -> str:
    """Create a dependency-free-ish slug fallback if python-slugify is unavailable."""
    slug = "".join(char.lower() if char.isalnum() else "_" for char in text).strip("_")
    return slug or "generated_style"


class AIStyleGenerator:
    """Select AI providers and normalize generated parameters."""

    def provider(self) -> AIProvider:
        """Instantiate the provider selected in user settings."""
        settings = settings_manager.settings
        if settings.api_provider == "OPENAI":
            return OpenAIStyleProvider(settings.openai_api_key)
        if settings.api_provider == "DEEPSEEK":
            return DeepSeekStyleProvider(settings.deepseek_api_key)
        return HeuristicStyleProvider()

    def generate_parameters(self, prompt: str) -> StyleParameters:
        """Generate a StyleParameters object from a prompt."""
        generated: GeneratedStyle = self.provider().generate(prompt)
        return StyleParameters.from_dict(generated.to_parameters_dict())

    def identifier_for_prompt(self, prompt: str) -> str:
        """Return a stable generated-preset identifier."""
        return f"ai_{_safe_slug(prompt)[:48]}"


ai_generator = AIStyleGenerator()

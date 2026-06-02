"""DeepSeek-compatible style provider."""

from __future__ import annotations

from .openai import OpenAIStyleProvider


class DeepSeekStyleProvider(OpenAIStyleProvider):
    """DeepSeek currently exposes an OpenAI-compatible chat API shape."""

    def __init__(self, api_key: str, endpoint: str = "https://api.deepseek.com/chat/completions") -> None:
        super().__init__(api_key=api_key, endpoint=endpoint)

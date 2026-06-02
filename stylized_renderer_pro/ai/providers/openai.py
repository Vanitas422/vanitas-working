"""OpenAI-compatible style provider.

This module intentionally keeps the integration small and replaceable. Users can
point it at OpenAI or an OpenAI-compatible gateway by changing the endpoint.
"""

from __future__ import annotations

import json
import urllib.request

from ..base import AIProvider, GeneratedStyle


class OpenAIStyleProvider(AIProvider):
    """Generate style parameters with an OpenAI-compatible chat endpoint."""

    def __init__(self, api_key: str, endpoint: str = "https://api.openai.com/v1/chat/completions") -> None:
        self.api_key = api_key
        self.endpoint = endpoint

    def generate(self, prompt: str) -> GeneratedStyle:
        """Call the provider and parse a compact JSON response."""
        if not self.api_key:
            raise RuntimeError("OpenAI API key is not configured")
        payload = {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "Return only JSON with outline, shadow_steps, rim_light, saturation, contrast, fog, bloom."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        return GeneratedStyle(**json.loads(content))

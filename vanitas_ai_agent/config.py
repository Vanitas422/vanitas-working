"""Configuration management for vanitas_ai_agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    openai_api_key: str
    model_name: str = "gpt-4"
    temperature: float = 0.2
    max_tokens: int = 800
    data_dir: Path = Path("./data")
    logs_dir: Path = Path("./logs")


    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your environment.")

        model_name = os.getenv("OPENAI_MODEL", "gpt-4").strip() or "gpt-4"
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

        data_dir = Path(os.getenv("VANITAS_DATA_DIR", "./data"))
        logs_dir = Path(os.getenv("VANITAS_LOGS_DIR", "./logs"))

        return cls(
            openai_api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            data_dir=data_dir,
            logs_dir=logs_dir,
        )

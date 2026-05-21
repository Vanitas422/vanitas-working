"""Core AI agent logic using OpenAI GPT-4 family models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from vanitas_ai_agent.config import Settings
from vanitas_ai_agent.executor import TaskExecutor
from vanitas_ai_agent.utils import append_jsonl, ensure_dir, utc_timestamp


class VanitasAgent:
    """A simple AI agent that can answer prompts and execute local actions."""

    SYSTEM_PROMPT = (
        "You are vanitas_ai_agent. "
        "When needed, propose structured actions for local execution using JSON format: "
        '{"action": "write_file|read_file|fetch_url|save_data", "params": {...}}. '
        "If no tool action is needed, return a direct answer."
    )

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        from openai import OpenAI

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.executor = TaskExecutor(settings.data_dir)
        ensure_dir(settings.logs_dir)
        self.log_file = settings.logs_dir / "interactions.jsonl"

    def _chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.model_name,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""

    def _try_parse_action(self, text: str) -> Optional[Dict[str, Any]]:
        try:
            payload = json.loads(text)
            if isinstance(payload, dict) and "action" in payload:
                return payload
        except json.JSONDecodeError:
            return None
        return None

    def process(self, user_message: str) -> str:
        model_output = self._chat(user_message)
        action = self._try_parse_action(model_output)

        if action:
            result = self.executor.run_action(action["action"], action.get("params", {}))
            final_output = f"Action executed: {action['action']}\nResult: {result}"
        else:
            final_output = model_output

        self._log_interaction(user_message, model_output, final_output)
        return final_output

    def _log_interaction(self, user_input: str, model_output: str, final_output: str) -> None:
        append_jsonl(
            self.log_file,
            {
                "timestamp": utc_timestamp(),
                "user_input": user_input,
                "model_output": model_output,
                "final_output": final_output,
            },
        )

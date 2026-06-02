"""Task execution module: file operations, network requests, and data persistence."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from vanitas_ai_agent.utils import ensure_dir, save_json


class TaskExecutor:
    """Provides a safe set of local actions the agent can invoke."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = ensure_dir(data_dir)

    def write_file(self, relative_path: str, content: str) -> Path:
        target = self.data_dir / relative_path
        ensure_dir(target.parent)
        target.write_text(content, encoding="utf-8")
        return target

    def read_file(self, relative_path: str) -> str:
        target = self.data_dir / relative_path
        return target.read_text(encoding="utf-8")

    def fetch_url(self, url: str, method: str = "GET", timeout: int = 15) -> Dict[str, Any]:
        import requests

        response = requests.request(method=method.upper(), url=url, timeout=timeout)
        response.raise_for_status()
        try:
            body: Any = response.json()
        except ValueError:
            body = response.text

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body,
        }

    def save_data(self, relative_path: str, data: Dict[str, Any]) -> Path:
        target = self.data_dir / relative_path
        save_json(target, data)
        return target

    def run_action(self, action: str, params: Optional[Dict[str, Any]] = None) -> Any:
        params = params or {}
        if action == "write_file":
            return str(self.write_file(params["path"], params["content"]))
        if action == "read_file":
            return self.read_file(params["path"])
        if action == "fetch_url":
            return self.fetch_url(
                url=params["url"],
                method=params.get("method", "GET"),
                timeout=int(params.get("timeout", 15)),
            )
        if action == "save_data":
            return str(self.save_data(params["path"], params["data"]))
        raise ValueError(f"Unsupported action: {action}")

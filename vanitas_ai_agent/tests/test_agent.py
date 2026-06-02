from pathlib import Path

from vanitas_ai_agent.agent import VanitasAgent
from vanitas_ai_agent.config import Settings


class DummyAgent(VanitasAgent):
    def __init__(self, settings: Settings, output: str):
        self.settings = settings
        self.client = None
        self.executor = __import__("vanitas_ai_agent.executor", fromlist=["TaskExecutor"]).TaskExecutor(settings.data_dir)
        self.log_file = settings.logs_dir / "interactions.jsonl"
        self._output = output
        Path(settings.logs_dir).mkdir(parents=True, exist_ok=True)

    def _chat(self, user_message: str) -> str:
        return self._output


def test_process_plain_text(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        data_dir=tmp_path / "data",
        logs_dir=tmp_path / "logs",
    )
    agent = DummyAgent(settings, "hello")
    result = agent.process("hi")
    assert result == "hello"
    assert agent.log_file.exists()


def test_process_action_write_file(tmp_path: Path) -> None:
    settings = Settings(
        openai_api_key="test",
        data_dir=tmp_path / "data",
        logs_dir=tmp_path / "logs",
    )
    action_json = '{"action":"write_file","params":{"path":"note.txt","content":"abc"}}'
    agent = DummyAgent(settings, action_json)
    result = agent.process("write a file")
    assert "Action executed: write_file" in result
    assert (tmp_path / "data" / "note.txt").read_text(encoding="utf-8") == "abc"

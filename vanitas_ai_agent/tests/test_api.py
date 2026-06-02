from fastapi.testclient import TestClient

from vanitas_ai_agent import api


class DummyAgent:
    def process(self, prompt: str) -> str:
        return f"echo:{prompt}"


def test_health() -> None:
    client = TestClient(api.app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_run_agent(monkeypatch) -> None:
    monkeypatch.setattr(api, 'Settings', type('S', (), {'from_env': staticmethod(lambda: object())}))
    monkeypatch.setattr(api, 'VanitasAgent', lambda _settings: DummyAgent())

    client = TestClient(api.app)
    response = client.post('/agent/run', json={'prompt': 'hello'})
    assert response.status_code == 200
    assert response.json()['result'] == 'echo:hello'

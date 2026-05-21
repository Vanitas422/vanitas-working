"""FastAPI interface for vanitas_ai_agent."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from vanitas_ai_agent.agent import VanitasAgent
from vanitas_ai_agent.config import Settings


class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Natural language instruction for the agent")


class AgentResponse(BaseModel):
    result: str


app = FastAPI(title="vanitas_ai_agent API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/agent/run", response_model=AgentResponse)
def run_agent(payload: AgentRequest) -> AgentResponse:
    try:
        settings = Settings.from_env()
        agent = VanitasAgent(settings)
        output = agent.process(payload.prompt)
        return AgentResponse(result=output)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {exc}") from exc

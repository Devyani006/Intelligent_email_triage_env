from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from env.environment import EmailTriageEnv
from env.models import (
    ResetResponse, StepAction, StepResult,
    EnvState, HealthResponse
)

app = FastAPI(
    title="Email Triage OpenEnv",
    description="OpenEnv environment for AI email triage agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single global env instance (stateless per call for HF Spaces)
env = EmailTriageEnv()


class ResetRequest(BaseModel):
    task_id: Optional[str] = None
    difficulty: Optional[str] = None


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check — must return 200 for HF Space ping."""
    return HealthResponse()


@app.post("/reset", response_model=ResetResponse)
def reset(req: ResetRequest = ResetRequest()):
    try:
        result = env.reset(task_id=req.task_id, difficulty=req.difficulty)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state", response_model=EnvState)
def state():
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step", response_model=StepResult)
def step(action: StepAction):
    try:
        return env.step(action)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "name": "email-triage-env",
        "version": "1.0.0",
        "endpoints": ["/health", "/reset", "/state", "/step"],
        "docs": "/docs",
    }
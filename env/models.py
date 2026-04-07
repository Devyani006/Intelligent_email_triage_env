from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TaskDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Email(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    timestamp: str


class Task(BaseModel):
    task_id: str
    difficulty: TaskDifficulty
    description: str
    email: Email


class EnvState(BaseModel):
    task_id: str
    difficulty: TaskDifficulty
    email: Email
    description: str
    step_count: int = 0
    done: bool = False


class ResetResponse(BaseModel):
    state: EnvState
    message: str = "Environment reset successfully"


class PriorityAction(BaseModel):
    priority: Priority
    reason: Optional[str] = None


class ActionExtractionAction(BaseModel):
    action_items: List[str] = Field(..., min_length=1)
    deadline_mentioned: Optional[str] = None


class FullTriageAction(BaseModel):
    priority: Priority
    action_items: List[str]
    sender_intent: str
    response_strategy: str
    escalate: bool = False


class StepAction(BaseModel):
    task_id: str
    answer: dict  # raw dict; validated inside env based on task type


class StepResult(BaseModel):
    reward: float = Field(..., ge=0.0, le=1.0)
    done: bool
    info: dict
    feedback: str


class HealthResponse(BaseModel):
    status: str = "ok"
    env: str = "email-triage-env"
    version: str = "1.0.0"
import random
from copy import deepcopy
from typing import Optional

from env.models import (
    EnvState, ResetResponse, StepAction, StepResult,
    Email, Task, TaskDifficulty
)
from tasks.task_bank import TASK_BANK
from graders.grader import grade


class EmailTriageEnv:
    def __init__(self):
        self._task_bank = TASK_BANK
        self._state: Optional[EnvState] = None
        self._current_rubric: Optional[dict] = None

    def reset(self, task_id: Optional[str] = None, difficulty: Optional[str] = None) -> ResetResponse:
        """
        Reset the environment.
        Optionally filter by task_id or difficulty.
        Returns a fresh state with a new email task.
        """
        pool = self._task_bank

        if task_id:
            pool = [t for t in pool if t["task_id"] == task_id]
        if difficulty:
            pool = [t for t in pool if t["difficulty"] == difficulty]

        if not pool:
            pool = self._task_bank  # fallback to full pool

        task_data = random.choice(pool)

        email = Email(**task_data["email"])
        self._current_rubric = task_data["rubric"]

        self._state = EnvState(
            task_id=task_data["task_id"],
            difficulty=TaskDifficulty(task_data["difficulty"]),
            email=email,
            description=task_data["description"],
            step_count=0,
            done=False,
        )

        return ResetResponse(state=deepcopy(self._state))

    def state(self) -> EnvState:
        """Return the current environment state."""
        if self._state is None:
            # Auto-reset if not initialised
            return self.reset().state
        return deepcopy(self._state)

    def step(self, action: StepAction) -> StepResult:
        if self._state is None or self._state.done:
            # Auto-reset on first call or after done
            self.reset()

        if action.task_id != self._state.task_id:
            return StepResult(
                reward=0.0,
                done=True,
                info={"error": f"task_id mismatch: expected {self._state.task_id}, got {action.task_id}"},
                feedback="Task ID mismatch. Please reset and check the current task.",
            )

        reward, feedback = grade(
            task_id=self._state.task_id,
            answer=action.answer,
            rubric=self._current_rubric,
        )

        self._state.step_count += 1
        self._state.done = True  # single-step tasks

        return StepResult(
            reward=reward,
            done=True,
            info={
                "task_id": self._state.task_id,
                "difficulty": self._state.difficulty,
                "email_id": self._state.email.id,
                "step_count": self._state.step_count,
            },
            feedback=feedback,
        )
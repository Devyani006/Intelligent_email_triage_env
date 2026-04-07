"""
Agent grader — scores agent responses using an LLM-based rubric.
Returns a float in [0.0, 1.0] with partial credit.
"""

import os
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=os.environ.get("HF_TOKEN", ""),
    base_url=os.environ.get("API_BASE_URL", "https://api.openai.com/v1"),
)
MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")


def _call_grader_llm(prompt: str) -> dict:
    """Call LLM and parse JSON score response."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict but fair grader. "
                        "You will evaluate an AI agent's answer against a rubric. "
                        "Always respond with valid JSON only. No markdown, no explanation outside JSON."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=300,
        )
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        logger.error(f"Grader LLM call failed: {e}")
        return {"score": 0.0, "feedback": f"Grading error: {str(e)}"}


def grade_priority(answer: dict, rubric: dict) -> tuple[float, str]:
    """Grade priority classification (easy task). Returns (score, feedback)."""
    expected = rubric.get("expected_priority", "").lower()
    given = str(answer.get("priority", "")).lower()

    if given == expected:
        return 1.0, f"Correct! Priority is '{expected}'."

    # Partial credit: adjacent levels get 0.5
    levels = ["low", "medium", "high", "urgent"]
    if expected in levels and given in levels:
        dist = abs(levels.index(expected) - levels.index(given))
        if dist == 1:
            return 0.5, f"Close — correct answer is '{expected}', you answered '{given}'."

    return 0.0, f"Incorrect. Expected '{expected}', got '{given}'."


def grade_action_extraction(answer: dict, rubric: dict) -> tuple[float, str]:
    """Grade action extraction using LLM semantic matching."""
    expected_actions = rubric.get("expected_actions", [])
    given_actions = answer.get("action_items", [])

    if not given_actions:
        return 0.0, "No action items provided."

    prompt = f"""
You are grading an AI agent's action extraction task.

Expected action items (from rubric):
{json.dumps(expected_actions, indent=2)}

Agent's extracted action items:
{json.dumps(given_actions, indent=2)}

For each expected action item, check if the agent captured the same intent (exact wording not required, semantic match counts).

Respond ONLY with this JSON:
{{
  "matched": <number of expected actions captured>,
  "total": {len(expected_actions)},
  "score": <float 0.0-1.0, = matched/total>,
  "feedback": "<brief explanation>"
}}
"""
    result = _call_grader_llm(prompt)
    score = float(result.get("score", 0.0))
    feedback = result.get("feedback", "")
    return round(min(max(score, 0.0), 1.0), 3), feedback


def grade_full_triage(answer: dict, rubric: dict) -> tuple[float, str]:
    """Grade full triage response using LLM rubric (4 components)."""
    prompt = f"""
You are grading a full email triage response.

Rubric (ground truth):
- Expected priority: {rubric.get('expected_priority')}
- Expected action items: {json.dumps(rubric.get('expected_actions', []))}
- Expected sender intent: {rubric.get('expected_intent')}
- Escalate required: {rubric.get('expected_escalate')}

Agent's answer:
- Priority: {answer.get('priority')}
- Action items: {json.dumps(answer.get('action_items', []))}
- Sender intent: {answer.get('sender_intent')}
- Response strategy: {answer.get('response_strategy')}
- Escalate: {answer.get('escalate')}

Score each component (0.0-1.0):
1. priority_score: 1.0 if correct, 0.5 if adjacent level, 0.0 if wrong
2. actions_score: fraction of rubric actions semantically captured
3. intent_score: 1.0 if intent is correctly identified (semantic match), 0.5 if partially correct
4. escalate_score: 1.0 if escalate matches rubric, 0.0 if not

Final score = 0.25*priority + 0.35*actions + 0.25*intent + 0.15*escalate

Respond ONLY with this JSON:
{{
  "priority_score": <float>,
  "actions_score": <float>,
  "intent_score": <float>,
  "escalate_score": <float>,
  "final_score": <float>,
  "feedback": "<brief explanation>"
}}
"""
    result = _call_grader_llm(prompt)
    score = float(result.get("final_score", 0.0))
    feedback = result.get("feedback", "")
    return round(min(max(score, 0.0), 1.0), 3), feedback


def grade(task_id: str, answer: dict, rubric: dict) -> tuple[float, str]:
    """Main grading entry point. Routes to correct grader."""
    if task_id == "priority_classification":
        return grade_priority(answer, rubric)
    elif task_id == "action_extraction":
        return grade_action_extraction(answer, rubric)
    elif task_id == "full_triage":
        return grade_full_triage(answer, rubric)
    else:
        return 0.0, f"Unknown task_id: {task_id}"
import os
import json
import time
import requests
from openai import OpenAI

# ── Config ──────────────────────────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

TASK_PROMPTS = {
    "priority_classification": """
You are an email triage agent. Classify the priority of this email.

Email Subject: {subject}
From: {sender}
Body:
{body}

Respond with ONLY valid JSON:
{{"priority": "<low|medium|high|urgent>", "reason": "<one sentence>"}}
""",
    "action_extraction": """
You are an email triage agent. Extract all required action items from this email.

Email Subject: {subject}
From: {sender}
Body:
{body}

Respond with ONLY valid JSON:
{{"action_items": ["<action 1>", "<action 2>", ...], "deadline_mentioned": "<deadline or null>"}}
""",
    "full_triage": """
You are an expert email triage agent. Perform a full triage of this email.

Email Subject: {subject}
From: {sender}
Body:
{body}

Respond with ONLY valid JSON:
{{
  "priority": "<low|medium|high|urgent>",
  "action_items": ["<action 1>", ...],
  "sender_intent": "<one sentence describing sender's goal>",
  "response_strategy": "<one sentence on how to respond>",
  "escalate": <true|false>
}}
""",
}


def call_agent(task_id: str, email: dict) -> dict:
    """Call the LLM agent to triage the given email."""
    prompt_template = TASK_PROMPTS[task_id]
    prompt = prompt_template.format(
        subject=email["subject"],
        sender=email["sender"],
        body=email["body"],
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert email triage agent. Always respond with valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=500,
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_task(task_id: str, difficulty: str) -> dict:
    """Run one full episode: reset → state → agent → step."""
    print(f"\n{'─'*50}")
    print(f"Task: {task_id}  |  Difficulty: {difficulty}")

    # 1. Reset environment
    resp = requests.post(f"{ENV_URL}/reset", json={"task_id": task_id, "difficulty": difficulty})
    resp.raise_for_status()
    state = resp.json()["state"]
    email = state["email"]
    print(f"Email: [{email['id']}] {email['subject']}")

    # 2. Call agent
    answer = call_agent(task_id, email)
    print(f"Agent answer: {json.dumps(answer, indent=2)}")

    # 3. Step
    step_resp = requests.post(
        f"{ENV_URL}/step",
        json={"task_id": task_id, "answer": answer},
    )
    step_resp.raise_for_status()
    result = step_resp.json()

    reward = result["reward"]
    feedback = result["feedback"]
    print(f"Reward: {reward:.3f}")
    print(f"Feedback: {feedback}")

    assert 0.0 <= reward <= 1.0, f"Reward out of range: {reward}"
    return {"task_id": task_id, "difficulty": difficulty, "reward": reward, "feedback": feedback}


def main():
    print("=" * 60)
    print("Email Triage OpenEnv — Baseline Inference")
    print("=" * 60)

    # Verify env is up
    health = requests.get(f"{ENV_URL}/health")
    health.raise_for_status()
    print(f"Environment healthy: {health.json()}")

    tasks_to_run = [
        ("priority_classification", "easy"),
        ("action_extraction", "medium"),
        ("full_triage", "hard"),
    ]

    results = []
    for task_id, difficulty in tasks_to_run:
        result = run_task(task_id, difficulty)
        results.append(result)
        time.sleep(1)  # be polite to the API

    # Summary
    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")
    total = 0.0
    for r in results:
        print(f"  {r['task_id']} ({r['difficulty']}): {r['reward']:.3f}")
        total += r["reward"]
    avg = total / len(results)
    print(f"\n  Average score: {avg:.3f}")
    print(f"  Tasks completed: {len(results)}/3")

    # Validate all scores are in [0, 1]
    for r in results:
        assert 0.0 <= r["reward"] <= 1.0, f"Invalid reward: {r}"

    print("\nAll checks passed.")
    return results


if __name__ == "__main__":
    main()
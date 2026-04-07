import os
import sys
import json
import subprocess
import requests
import yaml

ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")
PASS = "✅"
FAIL = "❌"
results = []


def check(name: str, ok: bool, detail: str = ""):
    status = PASS if ok else FAIL
    msg = f"{status} {name}"
    if detail:
        msg += f"  →  {detail}"
    print(msg)
    results.append((name, ok))
    return ok


def run_all():
    print("=" * 60)
    print("Email Triage OpenEnv — Pre-Submission Validator")
    print("=" * 60)

    # 1. Health check
    try:
        r = requests.get(f"{ENV_URL}/health", timeout=10)
        check("Health endpoint returns 200", r.status_code == 200, str(r.json()))
    except Exception as e:
        check("Health endpoint returns 200", False, str(e))

    # 2. reset() works
    try:
        r = requests.post(f"{ENV_URL}/reset", json={}, timeout=10)
        ok = r.status_code == 200 and "state" in r.json()
        check("reset() endpoint works", ok, f"status={r.status_code}")
    except Exception as e:
        check("reset() endpoint works", False, str(e))

    # 3. state() works
    try:
        r = requests.get(f"{ENV_URL}/state", timeout=10)
        state = r.json()
        ok = r.status_code == 200 and "email" in state and "task_id" in state
        check("state() returns email + task_id", ok)
    except Exception as e:
        check("state() returns email + task_id", False, str(e))

    # 4. step() works (easy task)
    try:
        requests.post(f"{ENV_URL}/reset", json={"task_id": "priority_classification"}, timeout=10)
        r = requests.post(
            f"{ENV_URL}/step",
            json={"task_id": "priority_classification", "answer": {"priority": "urgent"}},
            timeout=30,
        )
        result = r.json()
        score = result.get("reward", -1)
        ok = r.status_code == 200 and 0.0 <= score <= 1.0
        check("step() returns reward in [0.0, 1.0]", ok, f"reward={score}")
    except Exception as e:
        check("step() returns reward in [0.0, 1.0]", False, str(e))

    # 5. All 3 task types run without error
    for task_id, difficulty, answer in [
        ("priority_classification", "easy", {"priority": "high"}),
        ("action_extraction", "medium", {"action_items": ["do X", "do Y"]}),
        ("full_triage", "hard", {
            "priority": "urgent",
            "action_items": ["fix X", "notify Y"],
            "sender_intent": "test intent",
            "response_strategy": "escalate to manager",
            "escalate": True,
        }),
    ]:
        try:
            requests.post(f"{ENV_URL}/reset", json={"task_id": task_id}, timeout=10)
            r = requests.post(
                f"{ENV_URL}/step",
                json={"task_id": task_id, "answer": answer},
                timeout=30,
            )
            result = r.json()
            score = result.get("reward", -1)
            ok = r.status_code == 200 and 0.0 <= score <= 1.0
            check(f"Task '{task_id}' grader score in [0.0, 1.0]", ok, f"reward={score}")
        except Exception as e:
            check(f"Task '{task_id}' grader score in [0.0, 1.0]", False, str(e))

    # 6. openenv.yaml exists and is valid
    try:
        with open("openenv.yaml") as f:
            spec = yaml.safe_load(f)
        ok = "name" in spec and "tasks" in spec and len(spec["tasks"]) >= 3
        check("openenv.yaml valid with 3+ tasks", ok)
    except Exception as e:
        check("openenv.yaml valid with 3+ tasks", False, str(e))

    # 7. Dockerfile exists
    check("Dockerfile exists", os.path.exists("Dockerfile"))

    # 8. inference.py in root
    check("inference.py in root directory", os.path.exists("inference.py"))

    # 9. Required env vars
    for var in ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]:
        val = os.environ.get(var, "")
        check(f"Env var {var} defined", bool(val), "(set)" if val else "NOT SET")

    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    if passed == total:
        print("🎉 All checks passed! Ready to submit.")
        return 0
    else:
        failed = [name for name, ok in results if not ok]
        print(f"Failed checks: {failed}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all())
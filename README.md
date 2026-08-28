# Intelligent Email Triage OpenEnv

A real-world **OpenEnv** environment for the OpenEnv × Scaler Hackathon.

An AI agent learns to triage corporate emails — classifying priority, extracting action items, and performing full triage — through the standard `step()` / `reset()` / `state()` API.

## Project Structure

email-triage-env/
├── app.py                  
├── inference.py            
├── validate.py             
├── openenv.yaml            
├── requirements.txt
├── Dockerfile
├── env/
│   ├── environment.py      
│   └── models.py          
├── tasks/
│   └── task_bank.py        
└── graders/
    └── grader.py           



## Tasks

| Task ID | Difficulty | Description |
|---|---|---|
| `priority_classification` | Easy | Classify email as low / medium / high / urgent |
| `action_extraction` | Medium | Extract all required action items |
| `full_triage` | Hard | Priority + actions + intent + response strategy |

All tasks use **partial credit scoring** (0.0–1.0).



## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/reset` | Reset env, load a task |
| GET | `/state` | Get current email + task |
| POST | `/step` | Submit answer, get reward |

### Step payload examples

**Easy (priority_classification):**
```json
{
  "task_id": "priority_classification",
  "answer": {"priority": "urgent", "reason": "Production is down"}
}
```

**Medium (action_extraction):**
```json
{
  "task_id": "action_extraction",
  "answer": {
    "action_items": ["Fix the bug", "Send RCA by tomorrow"],
    "deadline_mentioned": "tomorrow EOD"
  }
}
```

**Hard (full_triage):**
```json
{
  "task_id": "full_triage",
  "answer": {
    "priority": "urgent",
    "action_items": ["Enable encryption", "Review admin accounts"],
    "sender_intent": "External compliance audit with regulatory deadline",
    "response_strategy": "Escalate to CTO and legal immediately",
    "escalate": true
  }
}
```



## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"

# Start the server
uvicorn app:app --host 0.0.0.0 --port 7860

# In another terminal: run baseline inference
python inference.py

# Run pre-submission validator
python validate.py
```


## Docker

```bash
docker build -t email-triage-env .
docker run -p 7860:7860 \
  -e API_BASE_URL=https://api.openai.com/v1 \
  -e MODEL_NAME=gpt-4o-mini \
  -e HF_TOKEN=your-key \
  email-triage-env
```

## Deploying to Hugging Face Spaces

1. Create a new Space (Docker SDK)
2. Push this repo to the Space
3. Add secrets in Space settings:
   - `API_BASE_URL`
   - `MODEL_NAME`
   - `HF_TOKEN`
4. Space will auto-build and deploy


## Reward Function

| Task | Scoring Logic |
|---|---|
| Easy | 1.0 exact, 0.5 adjacent level, 0.0 wrong |
| Medium | LLM semantic match: `matched / total` expected actions |
| Hard | Weighted: 25% priority + 35% actions + 25% intent + 15% escalate |
=======
---
title: EmailTriage
emoji: 🌖
colorFrom: indigo
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

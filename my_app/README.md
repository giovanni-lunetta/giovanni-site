---
title: career_conversation
sdk: docker
---

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Create a .env file in this directory with at least OPENAI_API_KEY=...
uvicorn app:app --reload --port 7860
```

## Required Environment Variables

- `OPENAI_API_KEY`: required for chat generation and OpenAI fallback evaluation.

## Optional Environment Variables

- `GOOGLE_API_KEY`: enables Gemini-based evaluator.
- `CHAT_MODEL`: default `gpt-4o-mini`.
- `EVAL_MODEL`: default `gpt-4o-mini`.
- `GEMINI_EVALUATOR_MODEL`: default `gemini-3.1-flash-lite-preview`.
- `GEMINI_EVALUATOR_FALLBACK_MODELS`: comma-separated fallback list.
- `PUSHOVER_TOKEN`: enables Pushover notifications.
- `PUSHOVER_USER`: enables Pushover notifications.

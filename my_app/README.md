---
title: career_conversation
app_file: app.py
sdk: gradio
sdk_version: 5.34.2
---

## Local Development

From the repository root:

```bash
cd my_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python app.py
```

## Required Environment Variables

- `OPENAI_API_KEY`: required for chat generation and OpenAI fallback evaluation.

## Optional Environment Variables

- `GOOGLE_API_KEY`: enables Gemini-based evaluator.
- `CHAT_MODEL`: default `gpt-4o-mini`.
- `EVAL_MODEL`: default `gpt-4o-mini`.
- `GEMINI_EVALUATOR_MODEL`: default `gemini-3.1-flash-lite-preview`.
- `GEMINI_EVALUATOR_FALLBACK_MODELS`: comma-separated fallback list used if the preferred Gemini model is unavailable.
- `PUSHOVER_TOKEN`: enables notification pushes.
- `PUSHOVER_USER`: enables notification pushes.

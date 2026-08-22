# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Two-part system that deploys independently:

**Static site** (`index.html`, `chat.html`, `resume.pdf`, `favicon.*`) — React 18 via CDN with Babel standalone. No build step. Netlify serves the repo root directly (`publish = "."` in `netlify.toml`). Push to `main` on GitHub triggers an automatic Netlify deploy.

**FastAPI backend** (`my_app/`) — Python app deployed as a Docker container on Hugging Face Spaces. Has its own `.git` repo pointing to `space` remote. The `chat.html` frontend hardcodes the HF Space URL (`https://glunetta02-career-conversation.hf.space/chat`).

These are **two separate git repos**. The parent repo pushes to GitHub; `my_app/` pushes to HF Spaces independently.

## Running Locally

**Static site:**
```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

**Backend:**
```bash
cd my_app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Create .env with at minimum: OPENAI_API_KEY=...
uvicorn app:app --reload --port 7860
```

## Deployment

**Static site → Netlify:**
```bash
git push origin main  # Netlify auto-deploys
```

**Backend → HF Spaces:**
```bash
cd my_app
git push space main  # triggers Docker build on HF
```

The HF Space must have environment variables set under **Settings → Variables and secrets** — they are not baked into the image. Required: `OPENAI_API_KEY`. Optional: `GOOGLE_API_KEY`, `CHAT_MODEL`, `EVAL_MODEL`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`.

## Backend internals (`my_app/`)

`Me` class in `app.py` is instantiated once at startup. It reads all context files from `me/` into memory and builds the system prompt:

| File | Purpose |
|------|---------|
| `me/resume.txt` | Professional resume — primary career context |
| `me/linkedin.txt` | LinkedIn profile text |
| `me/personal_context.txt` | Personality, hobbies, values |
| `me/summary.txt` | Short bio used in the system prompt opener |

Two OpenAI function-call tools are registered: `record_user_details` (logs email + sends Pushover notification) and `record_unknown_question` (logs to `data/unknown_questions.jsonl` + Pushover). Evaluations are logged to `data/evaluations.jsonl`.

`GOOGLE_API_KEY` enables a Gemini-based evaluator; without it the app falls back to OpenAI for evaluation. Model resolution for Gemini queries the API at startup to pick the best available model from `GEMINI_EVALUATOR_FALLBACK_MODELS`.

Endpoints: `GET /health` → `{"status": "ok"}`, `POST /chat` → `{"reply": "...", "success": true}`.

## Important constraints

- `my_app/.gitignore` excludes `*.pdf` — PDFs in `my_app/me/` are local-only and never pushed to HF.
- `chat.html` has a hardcoded `apiUrl` constant near the top — update it if the HF Space URL changes.
- `my_app/.git/config` stores the HF token in the `space` remote URL (local only, never committed).
- The README.md at root is stale — trust this file and the actual code over it.

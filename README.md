# Giovanni Lunetta — Personal Site

Personal portfolio and AI chat companion for [giovannilunetta.com](https://giovannilunetta.com).

## Structure

```
/
├── index.html      # Main portfolio (Home, Hobbies, Resume, Chat pages)
├── chat.html       # Standalone AI chat interface
├── resume.pdf      # Resume (PDF), served on the Resume page
├── favicon.svg / favicon.png
├── netlify.toml    # Netlify config (publish = ".")
└── my_app/         # FastAPI AI chat backend (separate git repo, deployed to Hugging Face Spaces)
```

## Running Locally

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## AI Chat Backend

The chat backend lives in `my_app/` and is deployed independently to Hugging Face Spaces. See `my_app/README.md` and the root `CLAUDE.md` for setup and deployment details. `chat.html` calls the API URL configured in its `TWEAK_DEFAULTS`.

## Deployment

Deployed via Netlify. Push to `main` triggers a deploy automatically. No build step — Netlify serves the repo root directly.

## Environment Variables

The FastAPI backend uses a local-only `.env` file (gitignored). See `my_app/README.md` for required variables.

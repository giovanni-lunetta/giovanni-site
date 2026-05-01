# Giovanni Lunetta — Personal Site

Personal portfolio and AI chat companion for [giovannilunetta.com](https://giovannilunetta.com).

## Structure

```
/
├── index.html          # Main portfolio (Home, Hobbies, Resume, Chat pages)
├── chat.html           # Standalone AI chat interface
├── resume.pdf          # Resume (PDF)
├── resume.md           # Resume (full markdown — chatbot context)
├── resume_condensed.md # Resume (condensed markdown — chatbot context)
├── favicon.ico         # Site favicon
├── netlify.toml        # Netlify config (publish = ".")
├── my_app/             # Python AI chat backend
├── .env                # Local environment variables (not committed)
└── .env.example        # Environment variable template
```

## Running Locally

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## AI Chat Backend

The chat backend lives in `my_app/`. See `API_SETUP.md` (in `my_app/`) for setup instructions. The `chat.html` frontend calls the API URL configured in its `TWEAK_DEFAULTS`.

## Deployment

Deployed via Netlify. Push to `main` triggers a deploy automatically. No build step — Netlify serves the repo root directly.

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. Never commit `.env`.

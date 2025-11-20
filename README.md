# Giovanni Lunetta - Personal Site & AI Companion

This is the personal website and AI companion project for Giovanni Lunetta. It features a static portfolio site and an embedded AI chat interface powered by a Python backend.

## Project Structure

- **Root Directory**: Contains the static HTML files (`index.html`, `chat.html`, `resume.html`) for the website.
- **`assets/`**: Stores static assets like images, PDFs (resume), and stylesheets.
- **`my_app/`**: Contains the source code for the AI companion application (Python/Gradio).
- **`scripts/`**: Helper scripts for maintenance tasks.

## Getting Started

### Running the Website Locally

To view the static website locally, you can use Python's built-in HTTP server:

```bash
python3 -m http.server
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

### Running the AI App

The AI application code resides in `my_app/`. Refer to `my_app/README.md` for specific instructions on running and deploying the Python application.

## Maintenance

### Syncing the Resume

The master copy of the resume is located in `my_app/me/resume.pdf`. To update the website's version (`assets/resume.pdf`), run the sync script:

```bash
./scripts/sync_resume.sh
```

# Universal AI Code Review Assistant

A fast hybrid AI code review tool that supports multiple programming languages, detects bugs and security issues, and returns a fixed version of the code when possible.

## Features
- Auto language detection
- Multi-language file analysis
- Python AST + linting
- JavaScript/TypeScript rule checks
- Safe auto-fix output
- FastAPI backend
- Render-ready deployment

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy on Render
- Push to GitHub
- Create a new Render Web Service
- Use `render.yaml` or manually set:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
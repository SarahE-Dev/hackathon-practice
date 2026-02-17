# Groq Chat - GitHub Workflow Practice

A minimal FastAPI app with intentional anti-patterns, built for practicing GitHub workflows (Issues, Project Boards, branches, PRs) before a hackathon.

## Anti-patterns to find and fix

1. **Hardcoded secret** - API key is hardcoded instead of using env vars
2. **Copy-pasted logic** - The Groq API call is duplicated across endpoints
3. **No error handling** - Crashes if Groq returns an error response

## Setup

### Get a Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / log in
3. Create an API key

### Install and run

**Using uv (recommended):**

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
# Edit .env with your actual GROQ_API_KEY
uvicorn main:app --reload
```

**Using pip (fallback):**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your actual GROQ_API_KEY
uvicorn main:app --reload
```

### Test it

```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Summarize
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Some long text to summarize..."}'
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Branch naming conventions

| Type       | Pattern              | Example                        |
|------------|----------------------|--------------------------------|
| Feature    | `feature/<name>`     | `feature/add-streaming`        |
| Bug fix    | `fix/<name>`         | `fix/use-env-var-for-api-key`  |
| Refactor   | `refactor/<name>`    | `refactor/extract-groq-client` |

## Workflow

See [practice-guide.md](practice-guide.md) for a step-by-step walkthrough of the GitHub workflow exercises.

# GitHub Workflow Practice Guide

Work through these exercises before the hackathon to get comfortable with the full GitHub workflow.

## 1. Push this repo to GitHub

```bash
gh repo create groq-chat-practice --public --source . --push
```

Or create it manually on github.com and push:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## 2. Create a Project Board

1. Go to your repo on GitHub
2. Click **Projects** tab > **New project**
3. Choose **Board** view
4. Create three columns: **To Do**, **In Progress**, **Done**

## 3. Create Issues

Create these 5 issues using the templates in `.github/ISSUE_TEMPLATE/`. You can do this from GitHub's UI or with the CLI:

### Issue 1 (bug): Hardcoded API key

```bash
gh issue create --title "fix: API key is hardcoded in main.py" \
  --label bug \
  --body "The Groq API key is hardcoded on line 14 instead of reading from the environment variable.

## Steps to Reproduce
1. Open main.py
2. See hardcoded key on line 14

## Expected Behavior
Should read from GROQ_API_KEY env var.

## Actual Behavior
Key is hardcoded as a string literal."
```

### Issue 2 (bug): No error handling on API calls

```bash
gh issue create --title "fix: No error handling for Groq API responses" \
  --label bug \
  --body "Both /chat and /summarize will crash if Groq returns an error response (rate limit, invalid key, etc).

## Steps to Reproduce
1. Set an invalid API key
2. Send a request to /chat
3. App crashes with KeyError

## Expected Behavior
Should return a helpful error message.

## Actual Behavior
Unhandled exception."
```

### Issue 3 (refactor): Extract duplicated API call logic

```bash
gh issue create --title "refactor: Extract duplicated Groq API call logic" \
  --label enhancement \
  --body "The Groq API call is copy-pasted in both /chat and /summarize endpoints.

## Acceptance Criteria
- [ ] Single helper function for Groq API calls
- [ ] Both endpoints use the shared function
- [ ] No behavior changes"
```

### Issue 4 (feature): Add a .gitignore

```bash
gh issue create --title "feat: Add .gitignore for Python projects" \
  --label enhancement \
  --body "Repo is missing a .gitignore file.

## Acceptance Criteria
- [ ] Ignores .env, __pycache__, .venv
- [ ] Follows standard Python .gitignore patterns"
```

### Issue 5 (feature): Add conversation history

```bash
gh issue create --title "feat: Support multi-turn conversation in /chat" \
  --label enhancement \
  --body "Currently /chat only sends a single message. Add support for passing conversation history.

## Acceptance Criteria
- [ ] Accept optional messages array in request body
- [ ] Pass full history to Groq API
- [ ] Backwards compatible (single message still works)"
```

After creating issues, drag them into your Project Board's **To Do** column.

## 4. Work on an Issue (full workflow)

Pick Issue 1 (hardcoded API key) and walk through the complete flow:

### Create a branch

```bash
git checkout -b fix/use-env-var-for-api-key
```

### Make the fix

In `main.py`, replace the hardcoded key:

```python
# Before
GROQ_API_KEY = "gsk_abc123_fake_key_replace_me"

# After
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")
```

### Commit and push

```bash
git add main.py
git commit -m "fix: read API key from environment variable

Closes #1"
git push -u origin fix/use-env-var-for-api-key
```

### Open a PR

```bash
gh pr create --title "fix: Read API key from env var" \
  --body "## Linked Issue
Closes #1

## What Changed
Replaced hardcoded API key with os.getenv() and added a startup check.

## How to Test
1. Remove any hardcoded key from main.py
2. Set GROQ_API_KEY in .env
3. Run the app - should work
4. Unset the var - should raise ValueError on startup

## Checklist
- [x] Code runs without errors
- [x] Tested locally
- [x] No secrets committed
- [x] PR title follows convention"
```

### Move the issue to In Progress on your Project Board.

## 5. Practice Code Review

On your own PR:

1. Go to the PR on GitHub
2. Click **Files changed**
3. Leave a review comment on a line (click the `+` icon next to a line)
4. Try "Suggest a change" using GitHub's suggestion block:
   ````
   ```suggestion
   GROQ_API_KEY = os.environ["GROQ_API_KEY"]  # fail fast if missing
   ```
   ````
5. Submit the review as **Comment** (or **Approve**)

## 6. Merge and clean up

```bash
# Merge the PR
gh pr merge --squash

# Back to main and pull
git checkout main
git pull

# Delete the branch
git branch -d fix/use-env-var-for-api-key
```

Move the issue to **Done** on your Project Board.

## 7. Repeat

Work through the remaining issues (2-5) following the same flow:
1. Create branch with proper naming convention
2. Make changes
3. Commit with a message referencing the issue
4. Open PR using the template
5. Review your own PR
6. Merge and clean up

## Quick Reference

| Action | Command |
|--------|---------|
| Create issue | `gh issue create` |
| List issues | `gh issue list` |
| Create branch | `git checkout -b feature/name` |
| Open PR | `gh pr create` |
| View PR | `gh pr view` |
| Merge PR | `gh pr merge --squash` |
| Link PR to issue | Put `Closes #N` in PR body |

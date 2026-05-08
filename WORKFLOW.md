# Workflow Rules

## Branch & PR Policy
- All work on `main` via pull requests
- PRs max 100 lines changed
- 2 approvals required to merge
- No force pushes to `main`

## Pre-commit Hook (pre-push)
Before pushing, the following runs automatically:
1. `pytest tests/` - must pass 95%+ of tests
2. `mypy` - must pass type checking

## Local Setup
```bash
pip install pre-commit
pre-commit install --hook-type pre-push
```

## Branch Naming
```
feature/<short-description>
bugfix/<short-description>
```

## PR Process
1. Create branch from `main`
2. Make changes, commit
3. Push and open PR
4. Address review feedback
5. Merge after approval
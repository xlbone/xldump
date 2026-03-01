# xldump - Project Overview

## Purpose
xldump is an xlsx dump tool - a utility for working with Excel files. The project is currently in early development (v0.0.1).

## Tech Stack
- **Language**: Python 3.12+
- **Package Manager**: uv (NOT pip)
- **Task Runner**: Poe the Poet (poethepoet)
- **Linting/Formatting**: Ruff
- **Type Checking**: mypy
- **Testing**: pytest + pytest-cov
- **Git Hooks**: pre-commit + gitlint
- **CI/CD**: GitHub Actions with reviewdog integration

## Key Dependencies
- Production: twine (for PyPI publishing)
- Development: ruff, mypy, pytest, pytest-cov, pre-commit, gitlint, poethepoet

## Version Control
- Uses Conventional Commits
- Auto-versioning via release-please
- Branch flow: feature → main → staging → production

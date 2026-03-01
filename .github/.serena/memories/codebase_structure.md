# Codebase Structure

```
xldump/
├── .github/
│   ├── scripts/
│   │   ├── mypy-review.sh    # reviewdog mypy integration
│   │   └── ruff-review.sh    # reviewdog ruff integration
│   ├── workflows/
│   │   ├── mypy.yml          # Type checking workflow
│   │   ├── ruff.yml          # Linting workflow
│   │   ├── test.yml          # Testing workflow
│   │   ├── renovate.yml      # Dependency updates
│   │   └── pr-auto-labeler.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── pull_request_template.md
│   ├── reviewdog.yml
│   ├── renovate.json
│   ├── release-please-config.json
│   └── .release-please-manifest.json
├── tests/
│   ├── __init__.py
│   └── test_example.py       # Example test patterns
├── .vscode/                  # VS Code settings
├── main.py                   # Main entry point
├── pyproject.toml           # Project config, dependencies, tool configs
├── ruff.toml                # Ruff linting/formatting config
├── uv.lock                  # Dependency lock file
├── .gitlint                 # Commit message validation rules
├── .pre-commit-config.yaml  # Pre-commit hooks config
├── .python-version          # Python version (3.12)
├── Claude.md                # Project rules for Claude Code
├── CHANGELOG.md             # Auto-generated changelog
└── README.md                # Project documentation
```

## Key Files

### Configuration
- **pyproject.toml**: Main config - dependencies, pytest, mypy, poe tasks
- **ruff.toml**: Linting and formatting rules
- **.gitlint**: Conventional Commits validation rules
- **.pre-commit-config.yaml**: Git hooks

### Entry Points
- **main.py**: Main application entry point (`python main.py`)

### Tests
- Located in `tests/` directory
- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Uses pytest markers: `@pytest.mark.slow`, `@pytest.mark.integration`, `@pytest.mark.unit`

### GitHub Actions
Workflows trigger on push/PR:
- **ruff.yml**: Linting, auto-format + commit
- **mypy.yml**: Type checking with reviewdog
- **test.yml**: pytest + coverage reporting
- **renovate.yml**: Weekly dependency updates (Saturday 3:00 JST)

### Deleted/Modified Files (from git status)
Note: Some workflow files appear deleted:
- workflows/promote-to-staging.yml (deleted)
- workflows/promote-to-production.yml (deleted)  
- workflows/release.yml (deleted)

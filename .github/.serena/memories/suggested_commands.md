# Suggested Commands for xldump

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `uv sync --all-groups` or `poe install` |
| Run all checks | `poe check` |
| Run tests | `poe test` |
| Run tests with coverage | `poe test-cov` |
| Lint code | `poe lint` |
| Auto-fix lint issues | `poe lint-fix` |
| Format code | `poe format` |
| Check formatting | `poe format-check` |
| Type check | `poe typecheck` |
| Type check specific files | `poe typecheck path/to/file.py` |
| Clean caches | `poe clean` |
| Setup git hooks | `poe setup-hooks` |
| Validate commit | `poe validate-commit` |

## Common Development Workflows

### Starting Work
```bash
uv sync --all-groups  # Install/update dependencies
poe setup-hooks       # Ensure hooks are installed
```

### Before Commit
```bash
poe fix              # Auto-fix lint + format
poe check            # Run all checks (lint + format-check + typecheck + test)
```

### Testing
```bash
poe test              # Run all tests
poe test-cov          # Run tests with coverage
poe test-verbose      # Verbose output
pytest tests/test_example.py  # Run specific test file
pytest -k "test_name"         # Run specific test by name
pytest -m slow                # Run slow-marked tests
pytest -m "not slow"          # Skip slow tests
```

### Adding Dependencies
```bash
uv add <package>         # Add runtime dependency
uv add --dev <package>   # Add dev dependency
uv remove <package>      # Remove dependency
uv lock --upgrade        # Update dependencies (or poe update)
```

### Running Python
```bash
uv run python main.py    # Run Python scripts
uv run python            # Interactive Python
```

## CI Commands
```bash
poe ci    # Full CI pipeline (lint + format-check + typecheck + test-cov)
```

## Git Commands
```bash
git checkout -b feat/feature-name main  # Create feature branch
git add .
git commit -m "feat: description"       # Must use Conventional Commits
git push -u origin feat/feature-name
gh pr create --base main                # Create PR
```

## System Utilities (Linux)
- `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`
- `find /path -name "*.py"` - Find files
- `grep -r "pattern" .` - Search in files
- `git status`, `git diff`, `git log`

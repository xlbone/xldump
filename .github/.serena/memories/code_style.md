# Code Style and Conventions

## Python Style (enforced by Ruff)

### Formatting
- Line length: 88 characters (Black-compatible)
- Indent: 4 spaces
- Quotes: Double quotes (`"`)
- Line endings: Auto-detect
- Magic trailing comma enabled

### Linting Rules (from ruff.toml)
Enabled rule sets:
- **E**: pycodestyle errors (PEP 8)
- **F**: Pyflakes (unused imports/variables)
- **I**: isort (import sorting)
- **N**: pep8-naming
- **W**: pycodestyle warnings
- **UP**: pyupgrade (modern Python syntax)
- **B**: flake8-bugbear
- **C4**: flake8-comprehensions
- **SIM**: flake8-simplify
- **S**: flake8-bandit (security)
- **D**: pydocstyle (docstrings)

### Per-file Ignores
- `tests/**/*.py`: S101 (assert allowed), D (no docstrings required)
- `__init__.py`: F401 (unused imports allowed)

## Type Hints (mypy)
- Python version: 3.12
- `disallow_untyped_defs = false` (project is early stage)
- `no_implicit_optional = true`
- `check_untyped_defs = true`
- `strict_equality = true`

## Docstrings
- Required for non-test code (pydocstyle enabled)
- Test files exempt from docstring requirements

## Naming Conventions
- snake_case for functions, variables
- PascalCase for classes
- UPPER_CASE for constants

## Import Order (isort)
1. Standard library
2. Third-party packages
3. Local imports
- Alphabetically sorted within sections

## Commit Messages (Conventional Commits - REQUIRED)
Format: `<type>: <description>`

Types:
- `feat`: New feature (MINOR version bump)
- `fix`: Bug fix (PATCH version bump)
- `feat!` or `BREAKING CHANGE`: Breaking change (MAJOR bump)
- `chore`: Maintenance (no version bump)
- `docs`: Documentation (no version bump)
- `refactor`: Refactoring (no version bump)
- `test`: Tests (no version bump)
- `ci`: CI/CD changes (no version bump)

Examples:
```
feat: add xlsx parsing capability
fix: resolve memory leak in parser
docs: update README with usage examples
```

## Branch Naming
- `feat/<description>` - New features
- `fix/<description>` - Bug fixes
- `chore/<description>` - Maintenance
- `docs/<description>` - Documentation
- `refactor/<description>` - Refactoring
- `test/<description>` - Tests
- `ci/<description>` - CI/CD changes

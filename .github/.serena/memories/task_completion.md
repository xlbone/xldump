# Task Completion Checklist

## Before Marking a Task Complete

### Code Quality Checks (Required)
```bash
poe check   # Runs: lint + format-check + typecheck + test
```

Or individually:
```bash
poe lint          # Check for lint errors
poe format-check  # Verify formatting
poe typecheck     # Run mypy type checks
poe test          # Run all tests
```

### If Checks Fail
```bash
poe fix      # Auto-fix lint + format issues
poe lint-fix # Just fix lint issues
poe format   # Just fix formatting
```

Then re-run `poe check` to verify.

## Committing Changes

### 1. Use Conventional Commits (MANDATORY)
Commit messages MUST follow the format:
```
<type>: <description>
```

Example types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`

### 2. Validate Commit Message
The pre-commit hook validates automatically, but you can check:
```bash
poe validate-commit
```

### 3. Never Push Directly to Protected Branches
Protected branches: `main`, `staging`, `production`

Always create a feature branch and PR:
```bash
git checkout -b feat/feature-name main
# ... make changes ...
git push -u origin feat/feature-name
gh pr create --base main
```

## After Creating a PR

### Be Aware of Auto-Commits
GitHub Actions may auto-format code. Before continuing work:
```bash
git fetch origin
git rebase origin/<your-branch-name>
```

## Full Workflow Summary
1. ✅ Make code changes
2. ✅ Run `poe check` - all must pass
3. ✅ Commit with Conventional Commits format
4. ✅ Push to feature branch
5. ✅ Create PR to main
6. ✅ Wait for CI checks to pass
7. ✅ Merge PR (auto-promotion to staging/production follows)

# Pillar 1: Style & Validation — guidance

Extended guidance for Pillar 1 of the agent-readiness audit (`SKILL.md`,
Step 2). The criterion table (S1–S7) lives in `SKILL.md`.

## S7 — Linter scope guidance

Both pre-commit and CI must scope linting to **changed files** — not the full
project and not individual changed lines.

- **Pre-commit**: Runs on staged files automatically (hooks handle file
  filtering natively).
- **CI**: Must explicitly lint only **git-changed files** (e.g.,
  `git diff --name-only origin/main... | xargs ruff check`). Pre-commit does
  not apply in CI; the pipeline must replicate the scoping.
- **Full project**: Only acceptable as a **justfile task** for manual developer
  use (e.g., `just lint-all`). Mark as ❌ if full-project linting is in
  pre-commit or CI.

**Legacy projects with high violation volume**: When a large project has many
pre-existing lint violations in files that are frequently touched, file-level
linting on changed files may block unrelated PRs. In this case, recommend a
**CI skip flag** (e.g., `[skip lint]` in commit message, or a workflow
conditional like `if: !contains(...)`) as a **transitional** escape hatch. The
skip flag must be paired with a lint-fix phase plan: a scheduled effort to
resolve existing violations so the flag can be removed.

> [!NOTE]
> Line-level linting (scoping to changed lines within files) is an alternative
> for legacy repos, but it is fragile, tool-dependent, and hard to configure
> consistently. Teams that prefer it may use `git diff --unified=0` piped to
> the linter, but this is not the default recommendation.

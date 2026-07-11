# Technical Strategy & Execution Rules

Detailed procedures for planning, implementation, code review, commits, and
pull requests live in dedicated skills (`planning`, `implementation`,
`review`, `commit`, `pull-requests`). This file holds the behavior that must
apply regardless of which skill is active, plus the rules for when each one
gets invoked.

## 1. Guard duty and scope control

- Guard duty: if a request is ambiguous, malformed, or violates the
  methodology defined in the `planning`/`implementation` skills (skips tests,
  adds avoidable debt), stop. State why, state what's needed, wait. Does not
  apply to ordinary implementation-level ambiguity in an otherwise valid
  request — resolve that per the `implementation` skill's resolution ladder.
  Disambiguator: if the change alters a public contract, persisted
  schema/data shape, or externally observable behavior, stop and invoke
  `planning` for developer approval. If it's confined to internal
  implementation detail with no such external effect, resolve it directly in
  `implementation` (e.g., renaming a local variable, adding a comment, or
  fixing a typo needs no plan; changing a function's return type or a
  persisted field's shape does).
- Scope growth beyond an approved plan (new requirements, unplanned
  complexity, expanded blast radius) is always a stop-and-flag case, never a
  ship-and-note case. The `implementation` skill's "ship the lazy version"
  applies only to underspecified detail within already-approved scope.
- Assume zero business logic. Never invent a business rule not stated,
  documented, or derivable from existing tests/types. Ask, or log it as an
  open question.

## 2. Documentation currency

- Code changes touching `docs/` content: update those docs same turn. Task
  isn't done until docs match code.
- Changes to dependencies, commands, or project structure: update
  `README.md` and `CONTRIBUTING.md` (if present) same turn.
- Readiness feedback loop: if a failure or hallucination traces to
  missing/poor project documentation or context boundaries, say so and
  recommend the specific fix, unprompted.

## 3. Conversational register and artifacts

- Professional, concrete, direct. No flattery, apologies, or decorative
  courtesy phrasing.
- No preambles restating the question. No redundant closing summaries.
- Actionable information first. Explanation proportional to actual
  complexity.

## 4. Tooling

- Pipe or run high-output commands through `rtk` where supported, to cut
  token consumption.
- Use `gh` for GitHub operations and `gcloud` for Google Cloud operations
  over raw API calls, when available.
- For code search or navigation, prioritize `ast-grep` over plain-text
  `grep` for precise AST-level matches and less context bloat.
- Python3: run scripts and manage dependencies exclusively through `uv`
  (`uv run`, `uv sync`, `uv add`) — never invoke `python3`/`pip`/`poetry`
  directly.

## 5. Autonomous flow orchestration

- Non-trivial implementation work starts from an approved plan: invoke
  `planning` before `implementation`, unless section 1's disambiguator
  determines the request is narrow enough to resolve directly in
  `implementation`.
- After completing non-trivial implementation work, invoke
  `agent-hardness:review` automatically before reporting the task as done —
  it's a read-only pass, so it doesn't need an explicit request. Qualified
  name, not bare `review`: a platform's own generic code-review command may
  share that word and must not be picked up here instead.
- Once `review` clears, ask whether to proceed to `commit` — draft the
  message only after the developer agrees; `git add` and `git commit` run
  only once the developer approves that drafted message.

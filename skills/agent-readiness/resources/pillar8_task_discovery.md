# Pillar 8: Task Discovery — guidance

Extended guidance for Pillar 8 of the agent-readiness audit (`SKILL.md`,
Step 2). The criterion table (K1–K4) lives in `SKILL.md`.

## K1 — Issue template content guidance (per repo type)

- `issues-only` / `both` → Must have at minimum **bug report** and **feature
  request** templates with structured fields (description, steps to reproduce,
  expected behavior). ✅ if both exist with structured fields; ⚠️ if only one
  template or unstructured; ❌ if no templates.
- `pr-only` → K1 is **N/A**.

## K2 — PR template content quality (per repo type)

| #    | Sub-criterion       | What to Look For                                                         |
| ---- | ------------------- | ------------------------------------------------------------------------ |
| K2.1 | Issue link          | Template includes issue link placeholder (`Closes #...` or `Related issue:`) |
| K2.2 | Template content    | Description section, testing checklist, and changelog fragment reminder   |

- `pr-only` / `both` → K2 evaluates existence **and** content (K2.1 + K2.2).
- `issues-only` → K2 is **N/A**.

**Scoring K2**: ✅ K2.1 + K2.2; ⚠️ template exists but missing sub-criteria;
❌ no template.

## K3 — Label consistency (per repo type)

Labels must be semantically consistent with the repo type:

- `issues-only` → labels describe issue nature: `bug`, `feature`,
  `enhancement`, `fix` (report doesn't warrant work). Labels like
  `ready-for-review` don't make sense here.
- `pr-only` → labels describe PR workflow/type: `bug`, `feature`,
  `breaking-change`, `ready-for-review`, `needs-tests`. Labels like `fix`
  (issue triage) don't apply. `bug`/`feature` are valid on PRs to clarify
  the type of change.
- `both` → labels span both categories.

The evaluator should flag labels semantically mismatched for the repo type.
Mark as ⚠️ if labels exist but include mismatched entries.

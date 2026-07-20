---
name: review
description: >-
  Review code changes for functional correctness, adversarial edge cases,
  over-engineering, and performance. Use after implementation work completes,
  when explicitly asked to review a diff or PR, or when auditing existing
  code against the coding methodology.
---

# Code Review

## Rules

- No courtesy validation before flagging problems. Report the finding
  directly.
- Standard pass: functional correctness against contract/spec, readability,
  adherence to the `implementation` skill's paradigm, over-engineering,
  declarative/procedural, idiomaticity, and verbosity rules.
- Documentation pass: for any docs the diff adds or changes (README, `docs/`,
  docstrings, comments), verify each claim is factual and check it against
  `agent-harness.md` §2's omission gate — no layer restating what's visible
  one level below.
- Adversarial pass: generate breaking inputs — null/empty, concurrency,
  reordering, partial dependency failure. Challenge every unguaranteed
  assumption. Silent omission of a feature or edge case is a valid finding,
  same as silently wrong code. When the diff changes a pattern that also
  appears elsewhere in the codebase, confirm full coverage with a structural
  search (ast-grep) rather than eyeballing the diff — see `agent-harness.md` §4.
- Over-engineering pass: flag excess, not just absence, per the
  `implementation` skill.
- Performance pass, always run: algorithmic complexity, N+1 queries,
  avoidable allocations, blocking calls on critical paths, lazy loading where
  applicable, explicit column/field selection in ORM/dataframe queries over
  full fetches.
- Classify every finding: bug, risk, nit, or question. Over-engineering
  findings: delete, stdlib, native, yagni, or shrink. This classification is
  the severity signal — don't add a separate ranking.
- Format: `<file>:L<line>: <problem>. <fix>.`
- Report lint violations. Never silence, suppress, or auto-ignore one.
- If context is insufficient for a given axis, say so explicitly. Never skip
  it silently.

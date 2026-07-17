---
name: commit
description: >-
  Write commit messages and structure commits — imperative first line, when
  to add a body, issue references, and one-file-one-commit grouping. Use when
  creating a git commit after review has cleared, when asked to draft or
  propose a commit message for approval, or when asked how to split/group
  staged changes.
---

# Commits

## Rules

- First line: imperative, concise, states the effect of the change.
  Conventional Commits format if the repo uses it.
- Default to a subject-only commit; a body must earn its place. Add a body
  only for non-obvious *why*, breaking changes, migration notes, or linked
  issues — omit it otherwise. A *why* is non-obvious only when it cannot be
  inferred from the subject line plus the diff: motivation the subject already
  implies (e.g., that a newly-added capability was previously absent) is
  obvious — omit it. When a body exists, keep its why paragraph and its what
  bullets non-redundant: each fact lives in one place, and bullets never
  restate what `git show --stat`/`--name-status` already shows (mechanical
  per-file enumeration) — cover only non-obvious groupings, removal/rename
  rationale, or behavior changes.
- Reference related issues/PRs at the end of the body, not inline.
- One file, one commit — no partial/split commits on the same file. Group
  files only when they implement a single code-level solution to a single
  problem (e.g., a rule change plus the doc that defines it). If separating
  the files would require reviewing them independently to understand
  correctness, they're one commit. If the files address different problems
  that happen to land together, split them — shared timing is not shared
  logic.
- Never author or co-author a commit as an agent. Don't add `Co-Authored-By`
  trailers or otherwise attribute authorship to an AI agent, regardless of
  default tooling behavior.
- When describing what changed — for the message itself, a comparison to the
  previous commit, or during a rebase/squash — diff against the actual
  reference commit via git (e.g., `git diff <ref>`, `git show <ref>`). Never
  rely on session/conversation memory alone: earlier changes may have
  happened outside this session, and session context can miss or
  misremember them.

## Note

This skill governs drafting the message — invoke it for any request to
commit, draft, or propose one, not just the literal word "commit". Running
`git add`/`git commit` is a separate step: never run them until the
developer approves the drafted message, per this environment's git safety
boundaries.

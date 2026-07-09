---
name: pull-requests
description: >-
  Write pull request titles and descriptions — scope-specific titles, neutral
  impact descriptions, and explicit out-of-scope notes. Use when opening a PR
  or drafting PR body content after commits are ready to ship.
---

# Pull Requests

## Rules

- Title: specific about scope and observable effect. No "fix bug" or "update
  logic".
- Body: neutral, verifiable impact description. No promotional tone.
- Skip template sections that don't apply. Include only what's relevant to
  this PR.
- State explicitly what was left out of scope. Don't assume it's inferred
  from the diff.
- Compute the PR's described changes/impact against the remote default
  branch, not local state that may be stale or diverged.

## Branches

- Ensure the branch is up to date with the remote default branch before
  pushing (fetch, then rebase or merge as the repo convention dictates).
  Resolve any conflicts first — never push a branch that's behind and let
  the PR surface a stale diff.

## Note

Never open a pull request without an explicit developer request — see
`AGENTS.md`'s orchestration rule and this environment's git safety
boundaries.

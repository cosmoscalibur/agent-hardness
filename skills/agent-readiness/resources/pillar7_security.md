# Pillar 7: Security — guidance

Extended guidance for Pillar 7 of the agent-readiness audit (`SKILL.md`,
Step 2). The criterion table (X1–X5) lives in `SKILL.md`.

## X3 — Review cooldown

Dependency update PRs (Dependabot, Renovate) should be configured with a
**review cooldown between 15 days and 2 months** (default: 15 days) to batch
reviews and reduce churn. This is the delay before the team acts on a
dependency update PR — not the check frequency. Evaluate whether the project
configures a review schedule or auto-merge delay. Mark as ⚠️ if scanning
exists but PRs are reviewed immediately with no batching strategy.

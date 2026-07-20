# Pillar 3: Testing — guidance

Extended guidance for Pillar 3 of the agent-readiness audit (`SKILL.md`,
Step 2). The criterion table (T1–T9) lives in `SKILL.md`.

## T9 — TDD methodology

Evaluate whether the project follows test-driven development discipline:

- **Tests-first**: Contributing guide (D6) or coding patterns (D8) document
  the TDD workflow (write tests before or alongside implementation).
- **Positive tests**: Tests verify expected/happy-path behavior.
- **Negative tests**: Tests verify error handling, edge cases, invalid inputs,
  and failure modes (e.g., `test_*_invalid`, `test_*_error`,
  `should_fail_when_*`).

**Scoring T9**: ✅ TDD documented **and** both positive + negative patterns
present; ⚠️ partial (one without the other); ❌ neither.

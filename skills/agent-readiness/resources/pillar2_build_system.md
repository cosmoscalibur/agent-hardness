# Pillar 2: Build System — guidance

Extended guidance for Pillar 2 of the agent-readiness audit (`SKILL.md`,
Step 2). The criterion table (B1–B5) lives in `SKILL.md`.

## B5 — Docker best practices

| #    | Sub-criterion     | What to Look For                                                   |
| ---- | ----------------- | ------------------------------------------------------------------ |
| B5.1 | Dockerfile exists | Dockerfile or compose file present                                 |
| B5.2 | Multi-stage build | Separate build and runtime stages to reduce image size             |
| B5.3 | `.dockerignore`   | Excludes build artifacts, secrets, and dev files from context      |
| B5.4 | Non-root user     | `USER` directive runs the container as a non-root user             |
| B5.5 | Pinned base image | Base image uses a specific tag or digest, not `latest`             |

**Scoring B5**:

- ✅ **Pass**: B5.1 + ≥ 3 of B5.2–B5.5
- ⚠️ **Partial**: B5.1 present but < 3 best practices
- ❌ **Fail**: no Dockerfile

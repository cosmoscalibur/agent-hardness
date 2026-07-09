#!/usr/bin/env bash
# Copy this plugin's rule and skills into Zed and Claude Code's own config
# locations, for environments that don't support Antigravity plugin install.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Zed
mkdir -p ~/.config/zed ~/.agents/skills
cp "$REPO_ROOT/rules/AGENTS.md" ~/.config/zed/AGENTS.md
cp -r "$REPO_ROOT/skills/." ~/.agents/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp "$REPO_ROOT/rules/AGENTS.md" ~/.claude/CLAUDE.md
cp -r "$REPO_ROOT/skills/." ~/.claude/skills/

# Repository-specific rules

Project-specific guidance for developing this plugin. The generic methodology
lives in `rules/agent-harness.md` and the stage skills. For the plugin's
structure, cross-tool references, and contribution flow, read `CONTRIBUTING.md`
and `docs/`.

## Documentation maintenance

`docs/` is the maintenance reference for this plugin and must stay current.
In particular, update `docs/rules-and-skills.md` and `docs/mcp.md` in the same
change whenever `scripts/sync.py` or the install flow changes, `docs/lsp.md`
whenever `.lsp.json` changes, and `docs/hooks.md` whenever `hooks/` or a hook
script changes.

## Versioning

For bump timing and levels, see `CONTRIBUTING.md`.

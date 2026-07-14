# Repository-specific rules

Project-specific guidance for developing this plugin. The generic methodology
lives in `rules/AGENTS.md` and the stage skills; this file holds only what is
specific to this repository.

## Versioning

This plugin follows SemVer. Any change that bumps the version must update
**both** manifests in lockstep, in the same change:

- `plugin.json` (root)
- `.claude-plugin/plugin.json`

(`.claude-plugin/marketplace.json` carries no version field.)

Bump level by change type:

| Change | Bump |
| --- | --- |
| Skill text modification | patch |
| New skill | minor |
| `rules/AGENTS.md` modification | patch |
| `scripts/` — removes a flag/option | minor |
| `scripts/` — supports a new option/flag | minor |
| `scripts/` — no functional change / bug fix | patch |

When a single change spans several rows, the highest bump wins.

Documentation-only changes (`README.md`, `CLAUDE.md`, `docs/`, and code
docstrings/comments) require no version bump.

## Documentation

`docs/` is the maintenance reference for this plugin and must stay current.
In particular, update `docs/rules-and-skills.md` and `docs/mcp.md` in the same
change whenever `scripts/sync.py` or the install flow changes,
`docs/lsp.md` whenever `.lsp.json` changes, and `docs/hooks.md` whenever
`hooks/` or a hook script changes.

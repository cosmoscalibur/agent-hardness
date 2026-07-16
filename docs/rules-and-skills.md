# Rules and skills

How to extend the always-on ruleset (`rules/AGENTS.md`) and add methodology
skills (`skills/`) — the form each must take — and how the two supported
clients deploy them.

## Extending `rules/AGENTS.md`

`rules/AGENTS.md` is a single consolidated file organized into numbered
top-level sections (guard duty, documentation currency, register, tooling, flow
orchestration). A rule addition must fit that form:

- Place the rule under the existing section whose topic it matches. Add a new
  top-level section only for a genuinely new topic, not a variant of one that
  exists.
- Write it as an imperative bullet. Where the behavior runs counter to a
  model's default, state the rationale — the file exists largely as
  counterweights to training bias, so the *why* is what makes a rule hold.
- Keep it generic and project-agnostic. Anything specific to one repository
  belongs in that repo's own `CLAUDE.md`, not here.
- Keep it lean. `rules/AGENTS.md` is copied to `~/.claude/CLAUDE.md` and loaded
  on every session, so every line is a standing cost — add only what must
  always apply, and move anything else into a skill.
- Keep it factual and verifiable, and respect the layered-docs discipline the
  file itself defines (§2): don't restate what a lower layer already shows.
- If the guidance is a stage-specific procedure rather than always-on behavior,
  it belongs in a skill, not here.

## Adding a skill

A skill is a directory under `skills/` whose form is fixed:

- Create `skills/<name>/SKILL.md`, where `<name>` is the kebab-case skill id and
  matches the directory name.
- Begin `SKILL.md` with YAML frontmatter:
  - `name` — the skill id (same as the directory).
  - `description` — what the skill does **and when to use it**. The client
    matches on this string to auto-invoke the skill, so it must state the
    trigger conditions ("Use when …"), not just summarize the content. Use a
    `>-` block scalar for a multi-line value.
- Follow the frontmatter with the skill's instructions in Markdown.
- Put any templates or deep references the skill uses in a subdirectory
  (`resources/` or `references/`) and link them from `SKILL.md`; they load only
  when the skill pulls them in.
- Mind the size split: a skill's `description` is always-on (loaded every
  session whether or not the skill fires), so keep it tight; the body and
  bundled files load only on invoke, so keep `SKILL.md` focused and push bulky
  reference material into `resources/`/`references/`. `claude plugin details`
  reports a skill's projected always-on and on-invoke token cost.
- Register the skill in the README's *Skills* table.

## Per-client deployment

### Antigravity

`agy plugin install <repo>` auto-discovers `rules/`, `skills/`, and
`plugin.json` from the plugin root, so both the ruleset and the skills install
natively — no copy step, nothing for a script to add.

### Claude Code

Claude loads the skills from the installed plugin but doesn't read a plugin's
rules file as global context, so the ruleset is deployed separately. Manually,
that is three steps:

1. Copy `rules/AGENTS.md` over `~/.claude/CLAUDE.md` — a plain overwrite;
   `rules/AGENTS.md` is the single source of truth.
2. Register this repo as a marketplace:
   `claude plugin marketplace add <repo>`.
3. Install the plugin: `claude plugin install agent-hardness@agent-hardness`
   (`claude plugin update …` once it's already installed). This carries the
   skills and the bundled `.lsp.json`/`hooks/`; the ruleset copy in step 1 is
   not part of it.

`scripts/sync.py` automates these three steps — adjust it there when the flow
changes.

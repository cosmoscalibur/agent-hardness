# Language servers (Claude Code)

This plugin declares its language servers internally, in
[`.lsp.json`](../.lsp.json) at the repo root. Installing the plugin registers
the invocations; the **binaries are a developer prerequisite** — install them
before running the Claude setup. LSP is set up on Claude Code only.

## Why declared internally

The official `claude-plugins-official` LSP plugins declare only the *invocation*
of a language server (the command to launch it), not the binary — and the
marketplace doesn't cover every language this project needs (Markdown, Bash,
HTML/CSS). Declaring the set in `.lsp.json` gives the same invocation contract
for every language in one place, with no dependency on the official
marketplace. A standalone `.lsp.json` (rather than an inline `lspServers` block
in `plugin.json`) also keeps LSP config out of the version-bumped manifest.

Where a language needs capabilities its server doesn't cover — Python
formatting and lint-autofix, which `basedpyright` doesn't do — that gap is
filled by a hook, not a second LSP; see [`hooks.md`](hooks.md) for why.

## The declared set

| Language            | Server                        | Binary                       |
| ------------------- | ----------------------------- | ---------------------------- |
| Python              | basedpyright                  | `basedpyright-langserver`    |
| Markdown            | marksman                      | `marksman`                   |
| Bash                | bash-language-server          | `bash-language-server`       |
| TypeScript / JS     | typescript-language-server    | `typescript-language-server` |
| HTML                | vscode-langservers-extracted  | `vscode-html-language-server`|
| CSS / SCSS / Less   | vscode-langservers-extracted  | `vscode-css-language-server` |
| Rust                | rust-analyzer                 | `rust-analyzer`              |

## `.lsp.json` schema

Each entry maps a server name to its launch config:

```json
{
  "<name>": {
    "command": "<binary on PATH>",
    "args": ["<flag>", "..."],
    "extensionToLanguage": { ".ext": "<language-id>" }
  }
}
```

- `command` (required) — the binary; must be on `PATH`.
- `extensionToLanguage` (required) — file extensions → LSP language identifiers.
- `args` (optional) — launch arguments (most servers use `--stdio` or a
  `start`/`server` subcommand).

Optional fields Claude Code also accepts: `transport` (`stdio` default or
`socket`), `env`, `initializationOptions`, `settings`.

## Adding a new language server

1. Install the server binary (see the install guidance below) and confirm it's
   on `PATH`.
2. Add an entry to [`.lsp.json`](../.lsp.json): pick a name, set `command`, add
   the `extensionToLanguage` map, and `args` if the server needs them (check the
   server's docs for its stdio invocation).
3. Add the language row to the table above and to the server-install section
   below.
4. Add the row to the README's *Language Servers* table.
5. Update the installed plugin (`claude plugin update agent-harness@agent-harness`)
   and restart Claude Code; edit a file of that type and confirm the server
   attaches (diagnostics/hover appear).

## Installing the servers

Install each server with its language's own package manager. Only servers
without one fall back to an OS package or release binary, given per OS.

### basedpyright (Python)

```zsh
uv tool install basedpyright
```

### marksman (Markdown)

No language package manager — install per OS:

- macOS: `brew install marksman`
- Arch: `pamac install marksman`
- Other Linux: `sudo snap install marksman`
- Windows: a release binary from
  [marksman releases](https://github.com/artempyanykh/marksman/releases)

### bash-language-server (Bash)

```zsh
npm install -g bash-language-server
```

Diagnostics also need [`shellcheck`](https://github.com/koalaman/shellcheck):

```zsh
sudo apt install shellcheck   # Ubuntu
pamac install shellcheck      # Arch
brew install shellcheck       # macOS
```

### typescript-language-server (TypeScript / JavaScript)

```zsh
npm install -g typescript-language-server typescript
```

### vscode-langservers-extracted (HTML, CSS)

Provides both `vscode-html-language-server` and `vscode-css-language-server`.

```zsh
npm install -g vscode-langservers-extracted
```

### rust-analyzer (Rust)

```zsh
rustup component add rust-analyzer
```

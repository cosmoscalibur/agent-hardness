# CLI tools

Install commands for the required CLI tools (the README lists them and their
purpose). `gh` follows its own official installer, linked from the README.

## uv

- macOS: `brew install uv`
- Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## rtk

- Linux / macOS: `curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh`
- Windows: a prebuilt binary from the
  [rtk releases](https://github.com/rtk-ai/rtk/releases)

Enabling its command-intercept hook (`rtk init -g`) is covered in the README.

## ast-grep

On PyPI as `ast-grep-cli`, so install it as a uv tool (provides the `ast-grep`
and `sg` binaries):

```zsh
uv tool install ast-grep-cli
```

## mergiraf

- Arch: `pamac install mergiraf`
- Ubuntu: `sudo snap install mergiraf`
- Any platform (Rust): `cargo install --locked mergiraf`

See the [mergiraf install docs](https://mergiraf.org/installation.html) for
more. Configuring it as git's merge driver is covered in the README.

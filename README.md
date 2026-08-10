# Steve-s-Agents

Personal agent guidance shared across development machines.

## Contents

- `shared/global-guidance/`: global engineering defaults for Codex and Claude.
- `shared/`: reusable workflow skills.
- `dotnet/`: .NET and ASP.NET Core domain skills.
- `configs/macos/`: reference copies of the local macOS configuration, including BOS project guidance.

## Adapting To Another Machine

Clone this repository in the target environment and ask the local agent to inspect `configs/macos/`, `shared/`, and `dotnet/`. The macOS files are reference material: adapt paths, shell commands, SDK setup, repository locations, and local excludes before installing them on Linux or WSL.

Do not replace an existing `~/.codex/config.toml` wholesale. Merge only the safe settings needed by the target environment, and never commit credentials, tokens, secrets, trust state, or machine-generated configuration.

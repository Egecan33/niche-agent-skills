# Local installation and platform adapters

Official documentation checked 2026-10-16. The shared `skills/` source tree uses the Agent Skills format; installation is a thin host-specific layer.

| Host | Project location | Personal location | Explicit invocation |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | `/skill-name` |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` | `$skill-name` in CLI/IDE |

Sources: [Claude Code skills](https://code.claude.com/docs/en/skills), [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills). Codex CLI/IDE also exposes `/skills`.

## Manual install

1. Read the selected `skills/<name>/SKILL.md`, its example and source references.
2. Inspect the destination for an existing directory with the same name. Resolve a collision deliberately before copying.
3. Copy the entire selected skill directory, retaining `references/` and `assets/`, under one location from the table. The repository root is not itself a skill.
4. Start a fresh session if discovery is stale. Confirm the loaded file path and run a synthetic behavior case before trusting automatic selection.
5. Install external tools only when a task needs actual execution and scope allows it; consult the pinned source and current dependency documentation first.

To uninstall a manual copy, identify and remove only that installed skill directory after preserving any local edits. Nothing in this repository installs itself or edits user settings.

## Distribution

OpenAI recommends plugins for reusable distribution. Its current portable packaging uses root `plugin.json` with `skills/`; a Codex compatibility manifest is a separate option. See [package your plugin](https://developers.openai.com/plugins/build/plugins) and [supported plugin surfaces](https://learn.chatgpt.com/docs/plugins). Plugin catalog submission is separate from publishing this GitHub source. No catalog manifest or submission is included in this first release; direct skill folders are the tested static artifact.

Claude plugin packaging is a separate adapter, and its manifest is not assumed interchangeable with OpenAI's. Claude.ai/Cowork/API uploads are outside the initial runtime target. A local Claude Code personal directory does not install to those services.

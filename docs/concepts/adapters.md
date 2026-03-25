# Adapters

Adapters bridge AI tools to the ANRS protocol.

## What is an Adapter?

An adapter is a configuration file that:
- Tells AI tools about ANRS
- Redirects to `.anrs/ENTRY.md`
- Uses "trampoline" pattern (minimal config)

## Available Adapters

| Adapter | Tool | Config File |
|---------|------|-------------|
| cursor | Cursor IDE | `.cursorrules` |
| claude-code | Claude Code | `CLAUDE.md` |
| codex | OpenAI Codex | `AGENTS.md` |
| opencode | OpenCode | `opencode.json` |

## Installation

```bash
# List adapters
anrs adapter list

# Install adapter
anrs adapter install cursor
anrs adapter install claude-code
```

## Trampoline Pattern

Adapters use minimal configuration:

```markdown
# .cursorrules

You are operating in an ANRS-governed repository.

Before taking ANY action, you MUST read and follow:
→ `.anrs/ENTRY.md`
```

**Why trampoline?**
- Adapter file never changes
- All rules in `.anrs/ENTRY.md`
- Easy upgrades via `anrs upgrade`

## Custom Adapters

Create adapter for new tools:

1. Create config file pointing to `.anrs/ENTRY.md`
2. Use the trampoline pattern (minimal redirect)
3. Contribute to ANRS project via PR

## Modes

Adapters may support different operation modes:

| Mode | Purpose |
|------|---------|
| build | Default - code writing mode |
| plan | Read-only planning mode |
| review | Code review mode |

Mode switching via CLI (coming soon) or manual file replacement.

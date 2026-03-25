---
name: adapters-index
description: |
  Vendor adapter configurations. Read when:
  (1) Setting up ANRS with a specific AI platform
  (2) Configuring system prompts for different vendors
  (3) Understanding vendor-specific integration
---

# Adapters

Vendor-specific configurations for integrating ANRS with different AI platforms.

## Available Adapters

| Adapter | Platform | Modes | Files |
|---------|----------|-------|-------|
| [claude-code/](claude-code/) | Claude Code CLI | build, plan, review | CLAUDE.md, modes/*.md |
| [cursor/](cursor/) | Cursor IDE | build, plan | .cursorrules, modes/* |
| [codex/](codex/) | OpenAI Codex CLI | build, plan, review | AGENTS.md, modes/*.md |
| [opencode/](opencode/) | OpenCode CLI/TUI | build, plan, review | opencode.json, agents/*.md |

## Quick Comparison

| Mode | Capability | Use When |
|------|------------|----------|
| **build** | Read, Write, Execute | Implementing features, fixing bugs |
| **plan** | Read only | Analyzing code, creating plans |
| **review** | Read only | Code review, quality checks |

## Usage

### Claude Code

```bash
# Quick start (build mode)
cp adapters/claude-code/CLAUDE.md your-project/CLAUDE.md

# Global configuration
mkdir -p ~/.claude
cp adapters/claude-code/CLAUDE.md ~/.claude/CLAUDE.md

# Switch modes
cp adapters/claude-code/modes/CLAUDE-plan.md your-project/CLAUDE.md
```

See [claude-code/README.md](claude-code/README.md) for subagents and model selection.

### Cursor

```bash
# Quick start (build mode)
cp adapters/cursor/.cursorrules your-project/.cursorrules

# Switch to plan mode
cp adapters/cursor/modes/cursorrules-plan your-project/.cursorrules
```

See [cursor/README.md](cursor/README.md) for Composer tips.

### Codex CLI

```bash
# Quick start (build mode)
cp adapters/codex/AGENTS.md your-project/AGENTS.md

# Global configuration
mkdir -p ~/.codex
cp adapters/codex/AGENTS.md ~/.codex/AGENTS.md

# Switch modes
cp adapters/codex/modes/AGENTS-plan.md your-project/AGENTS.md
```

See [codex/README.md](codex/README.md) for approval modes and model selection.

### OpenCode

```bash
mkdir -p .opencode/agents
cp adapters/opencode/opencode.json .opencode/
cp adapters/opencode/agents/*.md .opencode/agents/
```

See [opencode/README.md](opencode/README.md) for detailed setup.

## Adding New Adapters

1. Create a directory: `adapters/{vendor}/`
2. Add configuration files following the vendor's format
3. Ensure the system prompt includes:
   - ANRS protocol reference
   - Execution loop
   - Key file locations
   - Prohibited actions

## Core Protocol (All Adapters)

All adapters enforce the same ANRS protocol:

```
1. READ state    → ai/state/state.json
2. LOCATE task   → plans/active/
3. SELECT skill  → ai/skills/index.json
4. EXECUTE       → Follow SKILL.md
5. RUN harness   → Pass before commit
```

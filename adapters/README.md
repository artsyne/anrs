---
name: adapters-index
description: |
  Vendor adapter configurations. Read when:
  (1) Setting up AHES with a specific AI platform
  (2) Configuring system prompts for different vendors
  (3) Understanding vendor-specific integration
---

# Adapters

Vendor-specific configurations for integrating AHES with different AI platforms.

## Available Adapters

| Adapter | Platform | Modes | Files |
|---------|----------|-------|-------|
| [claude/](claude/) | Claude (Anthropic) | build, plan | system-prompt.txt, projects/*.md |
| [cursor/](cursor/) | Cursor IDE | build, plan | .cursorrules, modes/* |
| [openai/](openai/) | OpenAI API/Assistants | build, plan, review | system-prompt.txt, assistants/*.json |
| [opencode/](opencode/) | OpenCode CLI/TUI | build, plan, review | opencode.json, agents/*.md |

## Quick Comparison

| Mode | Capability | Use When |
|------|------------|----------|
| **build** | Read, Write, Execute | Implementing features, fixing bugs |
| **plan** | Read only | Analyzing code, creating plans |
| **review** | Read only | Code review, quality checks |

## Usage

### Claude

```bash
# Quick start (build mode)
cat adapters/claude/system-prompt.txt  # Copy to Claude system prompt

# For Claude Projects
# Copy adapters/claude/projects/ahes-build.md or ahes-plan.md
```

See [claude/README.md](claude/README.md) for API and Projects setup.

### Cursor

```bash
# Quick start (build mode)
cp adapters/cursor/.cursorrules your-project/.cursorrules

# Switch to plan mode
cp adapters/cursor/modes/cursorrules-plan your-project/.cursorrules
```

See [cursor/README.md](cursor/README.md) for Composer tips.

### OpenAI

```bash
# Chat Completions API
cat adapters/openai/system-prompt.txt  # Use as system message

# Assistants API (recommended)
# Use adapters/openai/assistants/ahes-{build,plan,review}.json
```

See [openai/README.md](openai/README.md) for code examples.

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
   - AHES protocol reference
   - Execution loop
   - Key file locations
   - Prohibited actions

## Core Protocol (All Adapters)

All adapters enforce the same AHES protocol:

```
1. READ state    → ai/state/state.json
2. LOCATE task   → plans/active/
3. SELECT skill  → ai/skills/index.json
4. EXECUTE       → Follow SKILL.md
5. RUN harness   → Pass before commit
```

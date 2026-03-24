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

| Adapter | Platform | Files |
|---------|----------|-------|
| [claude/](claude/) | Claude (Anthropic) | system-prompt.txt |
| [cursor/](cursor/) | Cursor IDE | .cursorrules |
| [openai/](openai/) | OpenAI Agents | system-prompt.txt, agent-config.json |
| [opencode/](opencode/) | OpenCode CLI/TUI | opencode.json, agents/*.md |

## Usage

### Claude

Copy `claude/system-prompt.txt` content to your Claude project's system prompt.

### Cursor

Copy `cursor/.cursorrules` to your project root as `.cursorrules`.

```bash
cp adapters/cursor/.cursorrules /your-project/.cursorrules
```

### OpenAI

Use `openai/agent-config.json` for OpenAI Agents configuration, or copy `system-prompt.txt` for custom setups.

### OpenCode

Copy the entire `opencode/` directory to your project:

```bash
mkdir -p .opencode/agents
cp adapters/opencode/opencode.json .opencode/
cp adapters/opencode/agents/*.md .opencode/agents/
```

See [opencode/README.md](opencode/README.md) for detailed instructions.

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

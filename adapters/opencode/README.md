---
name: opencode-adapter
description: |
  OpenCode adapter configuration. Read when:
  (1) Setting up AHES with OpenCode CLI/TUI
  (2) Configuring AHES-compliant agents in OpenCode
  (3) Understanding OpenCode-specific integration
---

# OpenCode Adapter

Configuration files for integrating AHES with [OpenCode](https://opencode.ai/).

## Files

```
opencode/
├── README.md           # This file
├── opencode.json       # Main configuration
└── agents/
    ├── ahes-build.md   # Primary agent (full access)
    ├── ahes-plan.md    # Primary agent (read-only)
    └── ahes-review.md  # Subagent (code review)
```

## Installation

### Option 1: Project-level (Recommended)

Copy to your project's `.opencode/` directory:

```bash
# From your project root
mkdir -p .opencode/agents
cp adapters/opencode/opencode.json .opencode/
cp adapters/opencode/agents/*.md .opencode/agents/
```

### Option 2: Global

Copy to your global OpenCode config:

```bash
cp adapters/opencode/agents/*.md ~/.config/opencode/agents/
```

Then add agent configurations to your global `~/.config/opencode/opencode.json`.

## Agents

### ahes-build (Primary)

Full-access agent for implementation work.

- **Mode**: primary
- **Tools**: write, edit, bash
- **Use**: Tab to switch, or default agent

### ahes-plan (Primary)

Read-only agent for planning and analysis.

- **Mode**: primary
- **Tools**: none (read-only)
- **Use**: Tab to switch when planning

### ahes-review (Subagent)

Code review subagent following AHES two-phase review.

- **Mode**: subagent
- **Tools**: none (read-only)
- **Use**: `@ahes-review review this code`

## Usage

1. **Start with planning**: Switch to `ahes-plan` to analyze and create a plan
2. **Execute with build**: Switch to `ahes-build` to implement changes
3. **Review changes**: Invoke `@ahes-review` for code review

## Customization

Modify `opencode.json` to:
- Change models (e.g., `openai/gpt-4o`, `google/gemini-pro`)
- Adjust temperature settings
- Enable/disable specific tools

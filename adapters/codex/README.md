---
name: codex-adapter
description: |
  OpenAI Codex CLI adapter configuration. Read when:
  (1) Setting up AHES with Codex CLI
  (2) Configuring AGENTS.md for AHES protocol
  (3) Understanding Codex-specific integration
---

# Codex Adapter

Configuration files for integrating AHES with [OpenAI Codex CLI](https://github.com/openai/codex).

## Files

```
codex/
├── README.md              # This file
├── AGENTS.md              # Default AHES instructions (build mode)
└── modes/
    ├── AGENTS-build.md    # Execution mode (full capability)
    ├── AGENTS-plan.md     # Planning mode (read-only)
    └── AGENTS-review.md   # Code review mode
```

## Installation

### Quick Start

Copy `AGENTS.md` to your project root:

```bash
cp adapters/codex/AGENTS.md your-project/AGENTS.md
```

### Global Configuration

For all projects, copy to `~/.codex/`:

```bash
mkdir -p ~/.codex
cp adapters/codex/AGENTS.md ~/.codex/AGENTS.md
```

### Switching Modes

```bash
# Build mode (default - full capability)
cp adapters/codex/AGENTS.md your-project/AGENTS.md

# Plan mode (read-only analysis)
cp adapters/codex/modes/AGENTS-plan.md your-project/AGENTS.md

# Review mode (code review)
cp adapters/codex/modes/AGENTS-review.md your-project/AGENTS.md
```

## Modes

### AGENTS.md / AGENTS-build.md (Default)

Full-capability mode for implementing changes.

- **Capability**: Read, Write, Execute
- **Use when**: Implementing features, fixing bugs, refactoring
- **Harness**: Required before commit

### AGENTS-plan.md

Read-only mode for planning and analysis.

- **Capability**: Read only
- **Use when**: Analyzing code, creating plans, reviewing architecture
- **Harness**: Not required (no changes made)

### AGENTS-review.md

Code review mode following AHES two-phase review.

- **Capability**: Read only
- **Use when**: Reviewing PRs, code quality checks
- **Output**: Spec compliance + Code quality report

## Codex-Specific Features

### AGENTS.md Discovery

Codex automatically discovers `AGENTS.md` files:
1. `~/.codex/AGENTS.md` - Global preferences
2. `./AGENTS.md` - Project-specific instructions

Both are loaded and combined.

### Approval Modes

Codex supports different approval modes:

```bash
# Auto-approve file changes (careful!)
codex --approval-mode full-auto

# Require approval for each change
codex --approval-mode suggest

# Auto-approve safe operations only
codex --approval-mode auto-edit
```

For AHES workflow, recommend `auto-edit` to auto-approve reads.

### Model Selection

```bash
# Use specific model
codex --model o3

# Use faster model for planning
codex --model gpt-4.1-mini
```

## Best Practices

1. **Start with State**: Always check `ai/state/state.json` first
2. **Follow Skills**: Use only registered skills from `ai/skills/index.json`
3. **Run Harness**: Verify with `python harness/quality_gate.py` before commit
4. **Atomic Commits**: One logical change per commit

## Troubleshooting

### AGENTS.md Not Loading?

1. Ensure file is named exactly `AGENTS.md` (case-sensitive)
2. Check file is in project root or `~/.codex/`
3. Run `codex` and check the startup message

### Codex Not Following Protocol?

1. Explicitly reference: "Follow the AHES protocol in AGENTS.md"
2. Start with: "Read ai/state/state.json and tell me the current status"
3. Use `--model o3` for better instruction following

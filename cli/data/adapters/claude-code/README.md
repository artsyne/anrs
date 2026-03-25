---
name: claude-code-adapter
description: |
  Claude Code adapter configuration. Read when:
  (1) Setting up ANRS with Claude Code CLI
  (2) Configuring CLAUDE.md for ANRS protocol
  (3) Understanding Claude Code-specific integration
---

# Claude Code Adapter

Configuration files for integrating ANRS with [Claude Code](https://code.claude.com/).

## Files

```
claude-code/
├── README.md              # This file
├── CLAUDE.md              # Default ANRS instructions (build mode)
└── modes/
    ├── CLAUDE-build.md    # Execution mode (full capability)
    ├── CLAUDE-plan.md     # Planning mode (read-only)
    └── CLAUDE-review.md   # Code review mode
```

## Installation

### Quick Start

Copy `CLAUDE.md` to your project root:

```bash
cp adapters/claude-code/CLAUDE.md your-project/CLAUDE.md
```

### Global Configuration

For all projects, copy to `~/.claude/`:

```bash
mkdir -p ~/.claude
cp adapters/claude-code/CLAUDE.md ~/.claude/CLAUDE.md
```

### Switching Modes

```bash
# Build mode (default - full capability)
cp adapters/claude-code/CLAUDE.md your-project/CLAUDE.md

# Plan mode (read-only analysis)
cp adapters/claude-code/modes/CLAUDE-plan.md your-project/CLAUDE.md

# Review mode (code review)
cp adapters/claude-code/modes/CLAUDE-review.md your-project/CLAUDE.md
```

## Modes

### CLAUDE.md / CLAUDE-build.md (Default)

Full-capability mode for implementing changes.

- **Capability**: Read, Write, Execute
- **Use when**: Implementing features, fixing bugs, refactoring
- **Harness**: Required before commit

### CLAUDE-plan.md

Read-only mode for planning and analysis.

- **Capability**: Read only
- **Use when**: Analyzing code, creating plans, reviewing architecture
- **Harness**: Not required (no changes made)

### CLAUDE-review.md

Code review mode following ANRS two-phase review.

- **Capability**: Read only
- **Use when**: Reviewing PRs, code quality checks
- **Output**: Spec compliance + Code quality report

## Claude Code-Specific Features

### CLAUDE.md Discovery

Claude Code automatically discovers CLAUDE.md files:
1. `~/.claude/CLAUDE.md` - Global preferences
2. `./CLAUDE.md` - Project-specific instructions

Both are loaded and combined.

### Subagents

Claude Code supports subagents for parallel work:
- Use `@explore` for codebase exploration
- Use `@plan` for detailed planning
- Use custom subagents for specialized tasks

### Model Selection

```bash
# Use Opus for complex reasoning
claude --model opus

# Use Sonnet for general work
claude --model sonnet

# Use Haiku for fast exploration
claude --model haiku
```

### Permission System

Claude Code has a layered permission system:
- Auto-approve safe operations
- Require approval for writes
- Always ask for destructive commands

## Best Practices

1. **Start with State**: Always check `.anrs/state.json` first
2. **Follow Skills**: Use only registered skills from `.anrs/skills/index.json`
3. **Run Harness**: Verify with `python harness/quality_gate.py` before commit
4. **Use Subagents**: Delegate exploration to keep main context clean

## Troubleshooting

### CLAUDE.md Not Loading?

1. Ensure file is named exactly `CLAUDE.md` (case-sensitive)
2. Check file is in project root or `~/.claude/`
3. Run `claude` and check the startup message

### Claude Not Following Protocol?

1. Explicitly reference: "Follow the ANRS protocol in CLAUDE.md"
2. Start with: "Read .anrs/state.json and tell me the current status"
3. Use `--model opus` for better instruction following

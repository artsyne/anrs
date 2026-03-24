---
name: cursor-adapter
description: |
  Cursor adapter configuration. Read when:
  (1) Setting up AHES with Cursor IDE
  (2) Configuring .cursorrules for AHES
  (3) Understanding Cursor-specific integration
---

# Cursor Adapter

Configuration files for integrating AHES with [Cursor IDE](https://cursor.com/).

## Files

```
cursor/
├── README.md              # This file
├── .cursorrules           # Default rules (build mode)
└── modes/
    ├── cursorrules-build  # Execution mode (full capability)
    └── cursorrules-plan   # Planning mode (read-only)
```

## Installation

### Quick Start

Copy `.cursorrules` to your project root:

```bash
cp adapters/cursor/.cursorrules your-project/.cursorrules
```

### Switching Modes

**For execution work** (implementing, coding):
```bash
cp adapters/cursor/modes/cursorrules-build your-project/.cursorrules
```

**For planning/analysis** (reviewing, planning):
```bash
cp adapters/cursor/modes/cursorrules-plan your-project/.cursorrules
```

## Modes

### cursorrules-build (Default)

Full-capability mode for implementing changes.

- **Capability**: Read, Write, Execute
- **Features**: Composer, Inline Edit, Terminal
- **Use when**: Implementing features, fixing bugs, refactoring

### cursorrules-plan

Read-only mode for planning and analysis.

- **Capability**: Read only
- **Features**: Chat, Code analysis
- **Use when**: Analyzing code, creating plans, reviewing

## Cursor-Specific Features

### Composer Mode

Cursor's Composer is ideal for AHES multi-file changes:

1. Open Composer (Cmd/Ctrl + I)
2. Reference the task: `@plans/active/task-001.md`
3. Cursor will follow AHES protocol from `.cursorrules`

### Inline References

Use `@` to reference AHES files in chat:
- `@ai/ENTRY.md` - Entry point
- `@ai/state/state.json` - Current state
- `@ai/skills/index.json` - Available skills

### Codebase Context

Cursor indexes your codebase. Leverage this:
- Ask "What skills are available?" → Cursor reads `ai/skills/`
- Ask "What's the current state?" → Cursor reads `ai/state/state.json`

## Best Practices

### 1. Start with State

Always begin by checking state:
```
Read ai/state/state.json and tell me the current status
```

### 2. Use Composer for Multi-File Changes

For tasks touching multiple files, use Composer mode with AHES context.

### 3. Verify with Terminal

After changes, run harness in Cursor's terminal:
```bash
python harness/quality_gate.py
```

### 4. Atomic Commits

Use Cursor's Git integration for atomic commits after harness passes.

## Troubleshooting

### Rules Not Loading?

1. Ensure `.cursorrules` is in project root
2. Restart Cursor or reload window
3. Check Cursor Settings → Rules

### AI Not Following Protocol?

1. Explicitly reference: "Follow the AHES protocol in .cursorrules"
2. Use `@.cursorrules` to include rules in context
3. Switch to a more detailed mode file

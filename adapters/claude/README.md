---
name: claude-adapter
description: |
  Claude adapter configuration. Read when:
  (1) Setting up AHES with Claude (API or Projects)
  (2) Configuring Claude system prompts for AHES
  (3) Understanding Claude-specific integration
---

# Claude Adapter

Configuration files for integrating AHES with [Claude](https://claude.ai/) (Anthropic).

## Files

```
claude/
├── README.md              # This file
├── system-prompt.txt      # Universal system prompt (API)
└── projects/              # Claude Projects configurations
    ├── ahes-build.md      # Execution mode (full capability)
    └── ahes-plan.md       # Planning mode (analysis only)
```

## Installation

### Option 1: Claude API

Use `system-prompt.txt` content as your system prompt:

```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=open("adapters/claude/system-prompt.txt").read(),
    messages=[{"role": "user", "content": "..."}]
)
```

### Option 2: Claude Projects (Recommended)

Claude Projects allow custom instructions per project:

1. Go to [claude.ai](https://claude.ai/) → Projects
2. Create a new project for your AHES-enabled repo
3. In Project Settings → Custom Instructions:
   - For **execution work**: Copy content from `projects/ahes-build.md`
   - For **planning/analysis**: Copy content from `projects/ahes-plan.md`
4. Add your project files to the Project Knowledge

### Option 3: Claude Code (CLI)

```bash
# Set AHES as default instructions
claude config set systemPrompt "$(cat adapters/claude/system-prompt.txt)"
```

## Modes

### ahes-build (Execution Mode)

Full-capability mode for implementing changes.

- **Capability**: Read, Write, Execute
- **Use when**: Implementing features, fixing bugs, refactoring
- **Harness**: Required before commit

### ahes-plan (Planning Mode)

Analysis-only mode for planning and review.

- **Capability**: Read only
- **Use when**: Analyzing code, creating plans, reviewing
- **Harness**: Not required (no changes made)

## Best Practices

1. **Start with Planning**: Use `ahes-plan` to analyze and create a detailed plan
2. **Switch to Build**: Use `ahes-build` to implement the plan
3. **Verify with Harness**: Always run harness before committing

## Claude-Specific Features

- **Artifacts**: Claude can output structured artifacts (code, documents)
- **Projects**: Persistent context across conversations
- **Extended Thinking**: Enable for complex reasoning tasks

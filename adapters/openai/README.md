---
name: openai-adapter
description: |
  OpenAI adapter configuration. Read when:
  (1) Setting up AHES with OpenAI API or Assistants
  (2) Configuring GPT-4/GPT-5 agents for AHES
  (3) Understanding OpenAI-specific integration
---

# OpenAI Adapter

Configuration files for integrating AHES with [OpenAI](https://platform.openai.com/) APIs and Assistants.

## Files

```
openai/
├── README.md              # This file
├── system-prompt.txt      # Universal system prompt
├── agent-config.json      # Generic agent configuration
└── assistants/            # OpenAI Assistants configurations
    ├── ahes-build.json    # Execution assistant
    ├── ahes-plan.json     # Planning assistant
    └── ahes-review.json   # Code review assistant
```

## Installation

### Option 1: Chat Completions API

Use `system-prompt.txt` as your system message:

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": open("adapters/openai/system-prompt.txt").read()},
        {"role": "user", "content": "..."}
    ]
)
```

### Option 2: Assistants API (Recommended)

Create AHES-compliant assistants:

```python
from openai import OpenAI
import json

client = OpenAI()

# Load assistant config
with open("adapters/openai/assistants/ahes-build.json") as f:
    config = json.load(f)

# Create assistant
assistant = client.beta.assistants.create(
    name=config["name"],
    instructions=config["instructions"],
    model=config["model"],
    tools=config["tools"]
)
```

### Option 3: Custom GPT

For ChatGPT Plus users creating a Custom GPT:

1. Go to ChatGPT → Explore GPTs → Create
2. In Configure → Instructions, paste content from `system-prompt.txt`
3. Upload your project files as Knowledge

## Assistants

### ahes-build (Execution)

Full-capability assistant for implementing changes.

- **Model**: gpt-4o
- **Tools**: Code Interpreter, File Search
- **Use when**: Implementing features, fixing bugs

### ahes-plan (Planning)

Analysis-only assistant for planning and review.

- **Model**: gpt-4o
- **Tools**: File Search only
- **Use when**: Analyzing code, creating plans

### ahes-review (Code Review)

Specialized assistant for two-phase code review.

- **Model**: gpt-4o
- **Tools**: File Search only
- **Use when**: Reviewing PRs, code quality checks

## API Integration Example

### Complete Workflow

```python
from openai import OpenAI
import json

client = OpenAI()

# 1. Create assistants
def create_ahes_assistants():
    assistants = {}
    for mode in ["build", "plan", "review"]:
        with open(f"adapters/openai/assistants/ahes-{mode}.json") as f:
            config = json.load(f)
        assistants[mode] = client.beta.assistants.create(**config)
    return assistants

# 2. Run with assistant
def run_ahes_task(assistant_id, task_description):
    thread = client.beta.threads.create()
    
    # Add task message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=task_description
    )
    
    # Run assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Get response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

# Usage
assistants = create_ahes_assistants()
result = run_ahes_task(
    assistants["build"].id,
    "Implement the greet function following the plan in plans/active/task-001.md"
)
```

## Function Calling

For advanced integration, use function calling with AHES skills:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_state",
            "description": "Read current AHES state from ai/state/state.json",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_harness",
            "description": "Run AHES harness evaluation",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["security", "L1", "L2", "L3", "all"]
                    }
                }
            }
        }
    }
]
```

## Best Practices

1. **Use Assistants API** for persistent context and file handling
2. **Enable Code Interpreter** for build mode (code execution)
3. **Use File Search** for accessing project knowledge
4. **Implement function calling** for harness integration

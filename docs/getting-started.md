# Getting Started

Get up and running with ANRS in 5 minutes.

## Prerequisites

- Python 3.9+
- Git

## Quick Start

### 1. Install CLI

```bash
pip install anrs
```

### 2. Initialize Project

```bash
cd your-project
anrs init
```

This creates:
```
your-project/
├── .anrs/
│   ├── ENTRY.md      # AI reads this first
│   ├── state.json    # Current state
│   └── config.json   # Configuration
└── plans/
    ├── active/
    └── backlog/
```

### 3. Add AI Adapter

```bash
anrs adapter install cursor
# or
anrs adapter install claude-code
```

### 4. Start Using

Point your AI tool to `.anrs/ENTRY.md` and start working!

## What's Next?

- [Installation Guide](installation.md) - Detailed setup options
- [Concepts](concepts/overview.md) - Understanding ANRS architecture
- [Examples](https://github.com/artsyne/anrs/tree/main/examples) - Sample projects

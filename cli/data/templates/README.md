# ANRS Templates

Template files and installation manifests for `anrs init`.

## Directory Structure

```
templates/
├── files/           # Template file pool (single source)
│   ├── ENTRY.md
│   ├── config.json
│   ├── state.template.json
│   ├── scratchpad.md
│   ├── plans/
│   ├── skills/
│   └── failure-cases/
└── manifests/       # Installation levels
    ├── minimal.json   # Level 0
    ├── standard.json  # Level 1
    └── full.json      # Level 2
```

## Installation Levels

| Level | Name | Contents |
|-------|------|----------|
| 0 | minimal | `.anrs/` with ENTRY + state + config |
| 1 | standard | + plans/ + scratchpad |
| 2 | full | + skills/ + harness/ + failure-cases/ |

## Usage

```bash
# Install with default level (standard)
anrs init

# Install specific level
anrs init --level minimal
anrs init --level full
```

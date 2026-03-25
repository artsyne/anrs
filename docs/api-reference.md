# CLI API Reference

Complete reference documentation for the ANRS command-line interface.

---

## Global Options

```bash
anrs --version    # Show version
anrs --help       # Show help for all commands
```

---

## anrs init

Initialize ANRS in a repository.

### Syntax

```bash
anrs init [OPTIONS] [PATH]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--level` | `-l` | `standard` | Installation level: `minimal`, `standard`, `full` |
| `--adapter` | `-a` | - | Install adapter: `cursor`, `claude-code`, `codex`, `opencode` |
| `--force` | `-f` | `false` | Overwrite existing files (with automatic backup) |
| `--merge` | `-m` | `false` | Merge with existing configuration |
| `--dry-run` | - | `false` | Preview changes without applying |

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PATH` | `.` | Target directory |

### Installation Levels

| Level | Contents |
|-------|----------|
| `minimal` | `.anrs/` (ENTRY.md, state.json, config.json) |
| `standard` | + scratchpad.md, `.anrs/plans/` |
| `full` | + `.anrs/skills/`, `.anrs/failure-cases/`, `.anrs/harness/` |

### Examples

```bash
# Standard initialization (default)
anrs init

# Minimal setup
anrs init --level minimal

# Full setup with Cursor adapter
anrs init --level full --adapter cursor

# Initialize specific directory
anrs init /path/to/project

# Preview what would be created
anrs init --dry-run

# Force overwrite (with backup)
anrs init --force

# Merge with existing config
anrs init --merge
```

### Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | Error (directory not found, permission denied, etc.) |
| `2` | User aborted (conflict resolution) |

---

## anrs status

Show ANRS status for a repository.

### Syntax

```bash
anrs status [PATH]
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PATH` | `.` | Target directory |

### Output

Displays:
- Component presence (ENTRY, State, Config, Scratchpad, Plans, Skills, Harness)
- Current state (status, current_task, last_completed)

### Examples

```bash
# Check current directory
anrs status

# Check specific directory
anrs status /path/to/project
```

---

## anrs upgrade

Upgrade .anrs/ directory to latest ANRS version.

### Syntax

```bash
anrs upgrade [OPTIONS] [PATH]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` | `false` | Preview changes without applying |
| `--force` | `false` | Force upgrade even if same version |
| `--no-backup` | `false` | Skip backup (not recommended) |
| `--list-backups` | `false` | List available backups |

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PATH` | `.` | Target directory |

### Preserved Data

During upgrade, the following are preserved:
- `current_task`
- `status`
- `last_completed`
- `history`
- `context`
- `project` configuration

### Examples

```bash
# Upgrade current directory
anrs upgrade

# Preview upgrade
anrs upgrade --dry-run

# Force upgrade
anrs upgrade --force

# List available backups
anrs upgrade --list-backups
```

---

## anrs adapter

Manage AI tool adapters.

### Syntax

```bash
anrs adapter <SUBCOMMAND> [OPTIONS]
```

### Subcommands

#### anrs adapter list

List available adapters.

```bash
anrs adapter list
```

Output shows:
- Adapter name
- Description
- Config file created

#### anrs adapter install

Install an adapter for an AI tool.

```bash
anrs adapter install <ADAPTER_NAME> [OPTIONS] [PATH]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--force` | `false` | Overwrite existing adapter (with backup) |
| `--skip` | `false` | Skip if adapter already exists |
| `--dry-run` | `false` | Preview without installing |

**Available Adapters:**

| Name | Config File | Description |
|------|------------|-------------|
| `cursor` | `.cursorrules` | Cursor AI editor |
| `claude-code` | `CLAUDE.md` | Anthropic Claude Code |
| `codex` | `AGENTS.md` | OpenAI Codex CLI |
| `opencode` | `opencode.json` | OpenCode AI |

### Examples

```bash
# List adapters
anrs adapter list

# Install Cursor adapter
anrs adapter install cursor

# Install with force overwrite
anrs adapter install cursor --force

# Preview installation
anrs adapter install claude-code --dry-run
```

---

## anrs harness

Run ANRS harness quality checks.

### Syntax

```bash
anrs harness [OPTIONS] [PATH]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--level` | `-l` | `all` | Harness level: `L1`, `L2`, `L3`, `security`, `all` |
| `--strict` | - | `false` | Fail on any check failure |

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PATH` | `.` | Target directory |

### Harness Levels

| Level | Description |
|-------|-------------|
| `L1` | Static checks (syntax, lint, complexity) |
| `L2` | Dynamic tests (unit tests, coverage) |
| `L3` | Stability analysis (risk assessment) |
| `security` | Security scans |
| `all` | Run all levels |

### Examples

```bash
# Run all checks
anrs harness

# Run only L1 (static)
anrs harness --level L1

# Run with strict mode
anrs harness --strict

# Check specific directory
anrs harness /path/to/project
```

### Exit Codes

| Code | Description |
|------|-------------|
| `0` | All checks passed |
| `1` | One or more checks failed |

---

## anrs doctor

Diagnose and repair ANRS installation.

### Syntax

```bash
anrs doctor [OPTIONS] [PATH]
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--fix` | - | `false` | Attempt to auto-fix detected issues |
| `--verbose` | `-v` | `false` | Show detailed diagnostic information |

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PATH` | `.` | Target directory |

### Health Checks

| Check | Description |
|-------|-------------|
| Python Version | Verifies Python >= 3.9 |
| .anrs Directory | Checks directory exists |
| ENTRY.md | Validates entry point file |
| state.json | Validates state file format and fields |
| config.json | Validates configuration |
| Adapters | Checks for installed adapters |
| Plans Directory | Validates plans structure |
| Harness | Checks harness configuration |

### Examples

```bash
# Run diagnostics
anrs doctor

# Run with verbose output
anrs doctor --verbose

# Attempt auto-fix
anrs doctor --fix

# Check specific directory
anrs doctor /path/to/project
```

### Exit Codes

| Code | Description |
|------|-------------|
| `0` | All checks passed |
| `1` | One or more checks failed |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANRS_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `NO_COLOR` | Disable colored output |

---

## Configuration Files

### .anrs/config.json

```json
{
  "version": "0.1",
  "project": {
    "name": "your-project-name"
  },
  "harness": {
    "strict_mode": false,
    "coverage_threshold": 80
  }
}
```

### .anrs/state.json

```json
{
  "status": "idle",
  "current_task": null,
  "last_completed": null,
  "metadata": {
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

---

## See Also

- [Getting Started](getting-started.md)
- [Installation Guide](installation.md)
- [Concepts Overview](concepts/overview.md)

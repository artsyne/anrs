# Migration Guide

Migrate existing projects to ANRS.

## From Scratch

If your project doesn't use any AI workflow:

```bash
cd your-project
anrs init
anrs adapter install cursor
```

Done! Your AI tool can now read `.anrs/ENTRY.md`.

## From Custom .cursorrules

If you have an existing `.cursorrules` file:

### 1. Backup existing rules

```bash
mv .cursorrules .cursorrules.backup
```

### 2. Initialize ANRS

```bash
anrs init
anrs adapter install cursor
```

### 3. Merge custom rules

Review `.cursorrules.backup` and add any project-specific rules to:
- `.anrs/config.json` - for configuration
- `.anrs/ENTRY.md` - for AI instructions (add to "Project-Specific" section)

## From Other AI Frameworks

### General Migration Steps

1. **Identify state management**
   - Where does AI track current task?
   - Where are plans stored?

2. **Initialize ANRS**
   ```bash
   anrs init --level minimal
   ```

3. **Migrate state**
   - Copy current task info to `.anrs/state.json`

4. **Migrate plans**
   - Move task plans to `.anrs/plans/active/`
   - Move backlog to `.anrs/plans/backlog/`

5. **Install adapter**
   ```bash
   anrs adapter install <your-tool>
   ```

6. **Test**
   ```bash
   anrs status
   ```

## Version Migration

### From Pre-0.1 to 0.1

If you have an older `ai/` or `spec/` directory structure:

```bash
# Rename to .anrs/
mv ai .anrs
# or
mv spec .anrs

# Reinstall adapter
anrs adapter install cursor --force
```

## Troubleshooting

### "Not an ANRS repository"

Run `anrs init` to initialize.

### State conflicts

```bash
# Backup and reinitialize
mv .anrs .anrs.backup
anrs init
# Manually merge state from .anrs.backup/state.json
```

### Adapter not working

Ensure your AI tool is configured to read the adapter file:
- Cursor: `.cursorrules`
- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`

# Versioning Policy

ANRS uses a dual-versioning strategy to clearly separate the specification from its tooling.

## Two Version Tracks

### Specification Version

The **ANRS Specification** defines the protocol, file formats, and execution model.

- Format: `ANRS Spec vX.Y.Z`
- Current: `ANRS Spec v1.0.0`
- Location: Defined in `spec/ENTRY.md` header

**Versioning rules:**
- **Major (X)**: Breaking changes to core concepts (state schema, execution loop)
- **Minor (Y)**: New optional features, new skills, new adapter types
- **Patch (Z)**: Clarifications, typo fixes, documentation improvements

### Tool Version

The **ANRS CLI** implements the specification as a command-line tool.

- Format: `anrs vX.Y.Z`
- Current: `anrs v0.1.0`
- Location: Defined in `cli/pyproject.toml`

**Versioning rules:**
- **Major (X)**: Breaking CLI changes, removed commands
- **Minor (Y)**: New commands, new options
- **Patch (Z)**: Bug fixes, performance improvements

## Version Compatibility

| CLI Version | Spec Version | Notes |
|-------------|--------------|-------|
| 0.1.x | 1.0.x | Initial release |

The CLI should always specify which spec version it implements:

```bash
$ anrs --version
anrs 0.1.0 (ANRS Spec v1.0.0)
```

## Release Process

### Specification Releases

1. All spec changes require an [RFC](../rfcs/README.md)
2. RFC must be accepted before implementation
3. Breaking changes require at least 1 minor version deprecation period
4. Spec version bumped in `spec/ENTRY.md`

### CLI Releases

1. All changes require PR review
2. Tests must pass (coverage >= 95%)
3. Version bumped in `cli/pyproject.toml`
4. Release created via GitHub Releases
5. Package published to PyPI

## Deprecation Policy

### Specification

- Features deprecated in minor versions
- Removed in next major version
- Minimum 6 months between deprecation and removal

### CLI

- Options deprecated with warning messages
- Removed in next major version
- Migration guide provided for breaking changes

## Version History

### Specification

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2024-01 | Initial stable release |

### CLI

| Version | Date | Changes |
|---------|------|---------|
| v0.1.0 | 2024-01 | Initial release |

## Pre-1.0 Stability

While the CLI is pre-1.0 (v0.x.x):
- Minor versions may include breaking changes
- Patch versions are always backward compatible
- Check CHANGELOG.md before upgrading

The specification is stable at v1.0.0 and follows strict semantic versioning.

## Checking Versions

```bash
# CLI version
anrs --version

# Check installed spec version
anrs status  # Shows spec version in header
```

## See Also

- [CHANGELOG.md](../CHANGELOG.md) - Detailed release notes
- [RFC Process](../rfcs/README.md) - How spec changes are proposed
- [Contributing Guide](../CONTRIBUTING.md) - How to submit changes

# Changelog

All notable changes to AHES will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-24

### Added

- Initial AHES framework structure
- Core specification layer (`ai/`)
  - Entry point (`ai/ENTRY.md`)
  - Rules and constraints (`ai/rules/`)
  - State management with SSOT (`ai/state/`)
  - Orchestrator protocol (`ai/orchestrator/`)
  - Skills registry and definitions (`ai/skills/`)
  - JSON Schema contracts (`ai/contracts/`)
- Harness evaluation system (`harness/`)
  - L1 static checks
  - L2 dynamic tests
  - L3 stability/risk analysis
  - Error codes definition
- Vendor adapters (`adapters/`)
  - Cursor adapter
  - Claude adapter
  - OpenAI adapter
- Example projects (`examples/`)
  - hello-world: Minimal 5-minute example
  - todo-app: Complete workflow demonstration
- Documentation (`docs/`)
  - Core beliefs
  - System architecture
  - API contracts reference
- Utility scripts (`scripts/`)
  - run_harness.sh
  - run_task.sh
  - rollback.sh
  - generate_adapters.sh

### Notes

- This is the initial release of AHES as a specification framework
- Harness evaluators are protocol skeletons, not production implementations
- Example code is intentionally incomplete for AI practice scenarios

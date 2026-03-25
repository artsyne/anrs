# Contributing to ANRS

Thank you for your interest in contributing to ANRS (AI-Native Repo Spec)!

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Contribution Types](#contribution-types)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

---

## 📜 Code of Conduct

Please be respectful and constructive in all interactions. We are building an open standard for the community.

---

## 🤝 How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/artsyne/anrs.git
cd anrs
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

Follow the [Style Guidelines](#style-guidelines) below.

### 4. Test Your Changes

```bash
./scripts/run_harness.sh
```

### 5. Submit a Pull Request

---

## 📦 Contribution Types

### Adding a New Skill

1. Create a new directory under `spec/skills/{category}/`
2. Include:
   - `SKILL.md` — Skill definition
   - `checklist.md` — Execution checklist (optional)
3. Register the skill in `spec/skills/index.json`

### Adding a New Adapter

1. Create a new directory under `adapters/{tool-name}/`
2. Include the tool-specific configuration
3. Update `scripts/generate_adapters.sh`

### Improving Documentation

- Documentation lives in `docs/`
- Keep it concise and actionable

### Adding Evaluators

1. Add new evaluator under `harness/evaluators/`
2. Follow the L1/L2/L3 hierarchy
3. Register error codes in `harness/error_codes.json`

---

## 🛠 Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+ (for some evaluators)
- Git

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📝 Style Guidelines

### Markdown Files

- Use clear, concise language
- Include comments explaining design intent
- Keep files under 200 lines when possible

### JSON Schema Files

- Use `$schema` declaration
- Include `description` for all fields
- Follow JSON Schema Draft-07

### Python Files

- Follow PEP 8
- Include docstrings
- Type hints encouraged

### Shell Scripts

- Use `#!/bin/bash`
- Include error handling
- Add comments for complex logic

---

## 🎯 Pull Request Guidelines

1. **One feature per PR** — Keep changes focused
2. **Include tests** — If applicable
3. **Update documentation** — If behavior changes
4. **Reference issues** — Link related issues

---

## 🙏 Thank You!

Every contribution helps make AI-driven development more reliable and predictable.

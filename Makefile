# ANRS Makefile
# Usage: make <target>

.PHONY: help install dev test lint typecheck ci clean pre-commit docs

# Default target
help:
	@echo "ANRS Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install CLI in development mode"
	@echo "  make dev          Install with all dev dependencies + pre-commit"
	@echo ""
	@echo "Quality:"
	@echo "  make test         Run tests with coverage"
	@echo "  make lint         Run ruff linter"
	@echo "  make typecheck    Run mypy type checker"
	@echo "  make ci           Run full CI pipeline (lint + typecheck + test)"
	@echo ""
	@echo "Utilities:"
	@echo "  make pre-commit   Run pre-commit on all files"
	@echo "  make clean        Remove build artifacts"
	@echo ""

# =============================================================================
# Setup
# =============================================================================

install:
	pip install -e cli/

dev:
	pip install -e "cli/[all]"
	pip install pre-commit
	pre-commit install
	@echo ""
	@echo "✓ Development environment ready!"
	@echo "  Pre-commit hooks installed."
	@echo "  Run 'make ci' to verify setup."

# =============================================================================
# Quality Checks
# =============================================================================

test:
	cd cli && python3 -m pytest tests/ --cov=anrs --cov-report=term-missing -v

lint:
	ruff check cli/src/ cli/tests/
	ruff format --check cli/src/ cli/tests/

typecheck:
	mypy cli/src/anrs/ --ignore-missing-imports

ci: lint typecheck test
	@echo ""
	@echo "✓ CI pipeline passed!"

# =============================================================================
# Utilities
# =============================================================================

pre-commit:
	pre-commit run --all-files

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf cli/.coverage cli/htmlcov 2>/dev/null || true
	@echo "✓ Cleaned build artifacts"

# =============================================================================
# Documentation
# =============================================================================

docs:
	pip install mkdocs-material mkdocs-minify-plugin
	mkdocs serve

docs-build:
	mkdocs build

docs-deploy:
	mkdocs gh-deploy

"""Tests for ANRS CLI constants module."""

import pytest
from pathlib import Path

from anrs.constants import (
    get_adapter_config_file,
    get_adapter_files,
    ADAPTERS,
    LEVELS,
    HARNESS_LEVELS,
    TEMPLATES_DIR,
    ADAPTERS_DIR,
)


class TestGetAdapterConfigFile:
    """Tests for get_adapter_config_file function."""

    def test_get_cursor_config(self):
        """Test getting cursor adapter config file."""
        result = get_adapter_config_file("cursor")
        assert result == ".cursorrules"

    def test_get_claude_code_config(self):
        """Test getting claude-code adapter config file."""
        result = get_adapter_config_file("claude-code")
        assert result == "CLAUDE.md"

    def test_get_codex_config(self):
        """Test getting codex adapter config file."""
        result = get_adapter_config_file("codex")
        assert result == "AGENTS.md"

    def test_get_opencode_config(self):
        """Test getting opencode adapter config file."""
        result = get_adapter_config_file("opencode")
        assert result == "opencode.json"

    def test_get_unknown_adapter_raises(self):
        """Test that unknown adapter raises ValueError."""
        with pytest.raises(ValueError) as exc:
            get_adapter_config_file("nonexistent")
        assert "Unknown adapter" in str(exc.value)


class TestGetAdapterFiles:
    """Tests for get_adapter_files function."""

    def test_get_adapter_files_returns_list(self):
        """Test that get_adapter_files returns list of tuples."""
        result = get_adapter_files("cursor")
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(item, tuple) and len(
            item) == 2 for item in result)


class TestConstants:
    """Tests for constant values."""

    def test_adapters_defined(self):
        """Test that all adapters are defined."""
        assert "cursor" in ADAPTERS
        assert "claude-code" in ADAPTERS
        assert "codex" in ADAPTERS
        assert "opencode" in ADAPTERS

    def test_levels_defined(self):
        """Test that levels are defined."""
        assert "minimal" in LEVELS
        assert "standard" in LEVELS
        assert "full" in LEVELS

    def test_harness_levels_defined(self):
        """Test that harness levels are defined."""
        assert "L1" in HARNESS_LEVELS
        assert "L2" in HARNESS_LEVELS
        assert "L3" in HARNESS_LEVELS
        assert "all" in HARNESS_LEVELS

    def test_directories_exist(self):
        """Test that template and adapter directories exist."""
        assert TEMPLATES_DIR.exists()
        assert ADAPTERS_DIR.exists()

"""Edge case tests for mdformat-slw plugin."""

from __future__ import annotations

import pytest

from mdformat_slw._sentence_wrapper import (
    DEFAULT_SENTENCE_MARKERS,
    ConfigurationError,
    get_sentence_markers,
    get_slw_wrap_width,
)


def test_empty_sentence_markers_raises_error() -> None:
    """Test that empty sentence markers raises ConfigurationError."""
    options = {"mdformat": {"plugin": {"slw": {"slw_markers": ""}}}}
    with pytest.raises(ConfigurationError, match="sentence_markers cannot be empty"):
        get_sentence_markers(options)


def test_too_long_sentence_markers_raises_error() -> None:
    """Test that excessively long sentence markers raises ConfigurationError."""
    options = {"mdformat": {"slw_markers": "x" * 51}}
    with pytest.raises(ConfigurationError, match="sentence_markers too long"):
        get_sentence_markers(options)


def test_slw_wrap_width_not_set() -> None:
    """Test get_slw_wrap_width when --slw-wrap is not set."""
    options = {"mdformat": {}}
    result = get_slw_wrap_width(options)
    assert result == 80  # noqa: PLR2004  # Default is now 80 per guidance.md


def test_slw_wrap_width_zero() -> None:
    """Test get_slw_wrap_width when --slw-wrap is 0 (disabled)."""
    options = {"mdformat": {"plugin": {"slw": {"slw_wrap": 0}}}}
    result = get_slw_wrap_width(options)
    assert result == 0


def test_slw_wrap_width_number() -> None:
    """Test get_slw_wrap_width when --slw-wrap is a number."""
    options = {"mdformat": {"slw_wrap": 80}}
    result = get_slw_wrap_width(options)
    assert result == 80  # noqa: PLR2004


def test_slw_wrap_width_plugin_config() -> None:
    """Test get_slw_wrap_width when set via plugin config."""
    options = {"mdformat": {"plugin": {"slw": {"slw_wrap": 100}}}}
    result = get_slw_wrap_width(options)
    assert result == 100  # noqa: PLR2004


def test_default_sentence_markers() -> None:
    """Test default sentence markers when none specified."""
    options = {"mdformat": {}}
    result = get_sentence_markers(options)
    assert result == DEFAULT_SENTENCE_MARKERS


def test_custom_sentence_markers() -> None:
    """Test custom sentence markers."""
    options = {"mdformat": {"slw_markers": ".!?"}}
    result = get_sentence_markers(options)
    assert result == ".!?"


def test_special_characters_in_sentence_markers() -> None:
    """Test sentence markers with special regex characters."""
    options = {"mdformat": {"slw_markers": ".!?*+[]"}}
    result = get_sentence_markers(options)
    assert result == ".!?*+[]"

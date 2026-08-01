"""General Helpers for configuration management."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias

from . import __plugin_name__

ContextOptions: TypeAlias = Mapping[str, Any]


def get_conf(options: ContextOptions, key: str) -> bool | str | int | None:
    """Read setting from mdformat configuration Context.

    Configuration can be provided via:
    1. API call: mdformat.text(..., options={key: value})
    2. CLI/TOML: stored in options["mdformat"]["plugin"]["slw"][key]

    Args:
        options: Configuration options from mdformat rendering context
        key: Configuration key to retrieve

    Returns:
        Configuration value (bool, str, int, or None if not found)

    """
    mdformat_opts = options.get("mdformat") or {}
    if (api := mdformat_opts.get(key)) is not None:
        return api  # From API
    return (
        mdformat_opts.get("plugin", {}).get(__plugin_name__, {}).get(key)
    )  # from cli_or_toml

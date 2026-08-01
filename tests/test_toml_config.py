"""Tests that `.mdformat.toml` configuration reaches the plugin."""

from __future__ import annotations

import warnings
from pathlib import Path

from mdformat._cli import run

TOML_CONFIG = """\
[plugin.slw]
slw_markers = ".!?:"
slw_min_line = 0
"""


def _write_case(tmp_path: Path, toml: str) -> Path:
    (tmp_path / ".mdformat.toml").write_text(toml)
    md = tmp_path / "test.md"
    md.write_text("First part: second part. Done.\n")
    return md


def test_toml_markers_are_applied(tmp_path: Path) -> None:
    md = _write_case(tmp_path, TOML_CONFIG)
    assert run([str(md)]) == 0
    assert md.read_text() == "First part:\nsecond part.\nDone.\n"


def test_cli_flag_overrides_toml(tmp_path: Path) -> None:
    md = _write_case(tmp_path, TOML_CONFIG)
    assert run([str(md), "--slw-markers", ".!?"]) == 0
    assert md.read_text() == "First part: second part.\nDone.\n"


def test_cli_arguments_have_no_defaults(tmp_path: Path) -> None:
    md = _write_case(tmp_path, "")
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        assert run([str(md)]) == 0

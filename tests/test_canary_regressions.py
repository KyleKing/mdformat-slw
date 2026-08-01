"""Regressions found by running the canary corpus over real downstream repos."""

from __future__ import annotations

import mdformat

NBSP = "\u00a0"


def _format(text: str) -> str:
    return mdformat.text(text, extensions={"slw"})


def test_shortcut_reference_link_keeps_plain_spaces() -> None:
    text = "See the [Contributing Guide] for details.\n\n[contributing guide]: https://example.com\n"
    result = _format(text)
    assert NBSP not in result
    assert "[Contributing Guide]" in result
    assert _format(result) == result


def test_link_text_is_not_split_across_lines() -> None:
    text = (
        "A really long sentence that goes on and on so that wrapping kicks in here "
        "[Contributing Guide To The Project](https://example.com/x) trailing words follow.\n"
    )
    result = _format(text)
    assert "[Contributing Guide To The Project]" in result
    assert _format(result) == result


def test_authored_non_breaking_space_survives() -> None:
    text = f"Author wrote a real{NBSP}nbsp here and it should survive.\n"
    result = _format(text)
    assert NBSP in result
    assert _format(result) == result

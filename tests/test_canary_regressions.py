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


def test_code_span_is_not_split_across_lines() -> None:
    text = (
        "Once you have a script with dependencies declared you can run it with "
        "`python <script>.py` and it will work exactly as expected here.\n"
    )
    result = _format(text)
    assert "`python <script>.py`" in result
    assert _format(result) == result


def test_multi_backtick_code_span_is_not_split() -> None:
    text = (
        "Text with a double backtick span ``a ` b c`` that also needs to stay "
        "together across a long enough line to wrap.\n"
    )
    result = _format(text)
    assert "`` a ` b c ``" in result
    assert _format(result) == result


def test_dash_fragment_does_not_become_a_setext_heading() -> None:
    text = (
        "This reveals another problem, which could easily be missed in a quick visual "
        "inspection -- our new developer has also deleted the number 4!\n"
    )
    result = _format(text)
    assert not any(line.strip() == "--" for line in result.split("\n"))
    assert not result.startswith("#")
    assert _format(result) == result


def test_shortcode_angle_bracket_does_not_open_a_blockquote() -> None:
    text = (
        'You can refer to the [`pyproject.toml`]({{< relref "pyproject#exclude-and-include" '
        ">}}) documentation for more.\n"
    )
    result = _format(text)
    assert not any(line.startswith(">") for line in result.split("\n"))
    assert _format(result) == result


def test_reference_link_split_by_soft_break_is_idempotent() -> None:
    text = (
        "The bare minimum required for a custom theme is a `main.html` [Jinja2\n"
        "template][jinja2 template] file which is placed in a directory.\n\n"
        "[jinja2 template]: https://jinja.palletsprojects.com/\n"
    )
    result = _format(text)
    assert _format(result) == result


def test_ordered_list_marker_does_not_start_a_wrapped_line() -> None:
    text = (
        "Prose that runs right up to the wrapping boundary and then keeps going "
        "along with 1. numbered thing after.\n"
    )
    result = _format(text)
    assert not any(line.startswith("1.") for line in result.split("\n"))
    assert _format(result) == result

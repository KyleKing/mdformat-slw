"""Unit tests for the configuration helpers."""

from __future__ import annotations

import pytest

from mdformat_slw._helpers import get_conf

EXPECTED_WRAP = 60


@pytest.mark.parametrize(
    "options",
    [{}, {"mdformat": None}, {"mdformat": {}}],
)
def test_get_conf_without_configuration(options: dict) -> None:
    assert get_conf(options, "slw_wrap") is None


def test_get_conf_from_api() -> None:
    assert (
        get_conf({"mdformat": {"slw_wrap": EXPECTED_WRAP}}, "slw_wrap") == EXPECTED_WRAP
    )


def test_get_conf_from_cli_or_toml() -> None:
    options = {"mdformat": {"plugin": {"slw": {"slw_wrap": EXPECTED_WRAP}}}}
    assert get_conf(options, "slw_wrap") == EXPECTED_WRAP

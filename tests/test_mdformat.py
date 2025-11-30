from pathlib import Path

import mdformat


def test_mdformat_text():
    """Verify that using mdformat works as expected."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text(encoding="utf-8")

    result = mdformat.text(content, extensions={"slw"})

    pth.write_text(result, encoding="utf-8")  # Easier to debug with git
    assert result == content, "Differences found in format. Review in git."

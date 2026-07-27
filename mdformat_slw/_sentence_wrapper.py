"""Sentence wrapping logic inspired by slw."""

from __future__ import annotations

import functools
import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import wcwidth

from ._helpers import get_conf
from ._language_data import DEFAULT_LANG, LANG_SUPPRESSIONS

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from mdformat.renderer import RenderContext, RenderTreeNode

    ContextOptions = Mapping[str, Any]

# Default configuration constants
DEFAULT_SENTENCE_MARKERS = ".!?"
DEFAULT_MIN_LINE_LENGTH = 40
DEFAULT_WRAP_WIDTH = 88

# Pattern to detect table-like text
# Tables start with | and contain | separators
# This detects: | cell | cell | or |cell|cell|
TABLE_LINE_PATTERN = re.compile(r"^\s*\|.*\|?\s*$")


def _display_width(text: str) -> int:
    """Calculate display width of text in terminal columns.

    Handles wide characters (CJK, emoji) that take 2 columns,
    zero-width characters (combining marks), and regular ASCII.

    Args:
        text: Text to measure

    Returns:
        Display width in columns, or len(text) as fallback for control chars

    """
    width = wcwidth.wcswidth(text)
    # wcswidth returns -1 if text contains non-printable control characters
    return width if width >= 0 else len(text)


def _is_table_text(text: str) -> bool:
    """Check if text looks like markdown table content.

    Tables should not be wrapped because it breaks their syntax.
    A table is detected if ALL lines match the table pattern
    (start with | and optionally end with |).

    Args:
        text: The text to check

    Returns:
        True if the text appears to be table content

    """
    lines = text.strip().split("\n")
    if not lines:
        return False

    # All lines must look like table rows
    return all(TABLE_LINE_PATTERN.match(line) for line in lines if line.strip())


class ConfigurationError(ValueError):
    """Raised when configuration values are invalid."""


def _validate_sentence_markers(markers: str) -> None:
    """Validate sentence markers string.

    Args:
        markers: String of sentence ending characters

    Raises (via _validate_sentence_markers):
        ConfigurationError: If markers is empty or invalid

    """
    if not markers:
        msg = "sentence_markers cannot be empty"
        raise ConfigurationError(msg)
    if len(markers) > 50:  # ruff: ignore[magic-value-comparison]
        msg = f"sentence_markers too long (max 50 chars): {len(markers)}"
        raise ConfigurationError(msg)


@functools.lru_cache(maxsize=128)
def _compile_sentence_pattern(sentence_markers: str) -> re.Pattern[str]:
    """Compile regex pattern for sentence ending detection.

    Compiles regex pattern with standard quantifiers for Python 3.10+ compatibility
    The pattern is cached to improve performance.

    Args:
        sentence_markers: String of characters that mark sentence endings

    Returns:
        Compiled regex pattern

    """
    _validate_sentence_markers(sentence_markers)
    marker_class = re.escape(sentence_markers)
    # Note: Using standard quantifiers (*) - possessive quantifiers not available in Python 3.10
    # Pattern: (marker)(optional closing chars)(whitespace)
    pattern = r"([" + marker_class + r"])(\s*[\"'\)\]\}]*)\s+"
    return re.compile(pattern)


def should_wrap_sentences(options: ContextOptions) -> bool:
    """Check if sentence wrapping is enabled via CLI or config.

    Sentence wrapping is ENABLED by default. Use --no-wrap-sentences to disable.

    Args:
        options: Configuration options from mdformat context

    Returns:
        True if sentence wrapping is enabled (default: True)

    """
    no_wrap = get_conf(options, "no_wrap_sentences")
    if no_wrap is not None:
        return not bool(no_wrap)
    return True  # Default: enabled


def get_sentence_markers(options: ContextOptions) -> str:
    """Get sentence ending markers from config.

    Args:
        options: Configuration options from mdformat context

    Returns:
        String of sentence ending characters (default: .!?:)

    Raises (via _validate_sentence_markers):
        ConfigurationError: If markers are invalid

    """
    markers = get_conf(options, "slw_markers")
    result = str(markers) if markers is not None else DEFAULT_SENTENCE_MARKERS
    _validate_sentence_markers(result)
    return result


def get_slw_wrap_width(options: ContextOptions) -> int:
    """Get line wrap width from slw's --slw-wrap setting.

    Args:
        options: Configuration options from mdformat context

    Returns:
        Maximum line width in characters, or 0 to disable wrapping (default: 88)

    """
    wrap_width = get_conf(options, "slw_wrap")
    return int(wrap_width) if wrap_width is not None else DEFAULT_WRAP_WIDTH


def get_min_line_length(options: ContextOptions) -> int:
    """Get minimum line length before sentence wrapping applies.

    This implements "soft wrap" behavior - only insert a sentence break
    if the current line length exceeds this threshold.

    Args:
        options: Configuration options from mdformat context

    Returns:
        Minimum line length in characters before wrapping (default: 40, 0=always wrap)

    """
    min_line = get_conf(options, "slw_min_line")
    return int(min_line) if min_line is not None else DEFAULT_MIN_LINE_LENGTH


def _get_suppression_words(options: ContextOptions) -> set[str]:
    """Build set of words that suppress sentence wrapping.

    Uses language-specific defaults, optionally extended with custom abbreviations.
    Always case-insensitive, single language only.

    Args:
        options: Configuration options from mdformat context

    Returns:
        Set of words (lowercase) that should not trigger sentence breaks

    """
    words: set[str] = set()

    # Check if user wants only custom abbreviations
    abbreviations_only = get_conf(options, "abbreviations_only")

    # Load language list (unless override mode)
    if not abbreviations_only:
        lang = get_conf(options, "lang")
        lang_code = str(lang) if lang else DEFAULT_LANG
        words.update(LANG_SUPPRESSIONS.get(lang_code, []))

    # Add custom abbreviations (comma-separated)
    custom = get_conf(options, "abbreviations")
    if custom:
        custom_words = [w.strip() for w in str(custom).split(",")]
        words.update(custom_words)

    # Always case-insensitive
    return {w.lower() for w in words}


def _wrap_long_line(line: str, max_width: int) -> list[str]:
    """Wrap a single long line preserving indentation.

    Per guidance.md: "Wrap lines that are longer than the maximum line width,
    if set, without splitting words or splitting at non-breaking spaces while
    also keeping indents in tact."

    Args:
        line: The line to wrap
        max_width: Maximum width in characters

    Returns:
        List of wrapped lines with preserved indentation

    """
    # Extract leading whitespace (indentation)
    indent_match = re.match(r"^(\s*)", line)
    indent = indent_match.group(1) if indent_match else ""
    content = line[len(indent) :]

    # Don't wrap if line fits within max_width
    if _display_width(line) <= max_width:
        return [line]

    # Split on regular spaces but NOT on non-breaking spaces (U+00A0)
    # Use a pattern that treats nbsp as part of the word
    nbsp = "\u00a0"
    # Replace nbsp with a placeholder, split, then restore
    # Note: Use \x01 instead of \x00 because mdformat uses \x00 for FILLER/WRAP_POINT
    placeholder = "\x01"
    content_normalized = content.replace(nbsp, placeholder)
    words = content_normalized.split()
    # Restore nbsp in each word
    words = [w.replace(placeholder, nbsp) for w in words]

    wrapped_lines = []
    current_line: list[str] = []
    # Start with indent display width
    current_length = _display_width(indent)

    for word in words:
        word_len = _display_width(word)
        # Calculate space needed: word length + 1 for space (if not first word)
        space_needed = word_len + (1 if current_line else 0)

        if current_length + space_needed > max_width and current_line:
            # Current line would exceed max_width, flush it with indent
            wrapped_lines.append(indent + " ".join(current_line))
            current_line = [word]
            # Reset length to indent display width + word display width
            current_length = _display_width(indent) + word_len
        else:
            # Add word to current line
            current_line.append(word)
            current_length += space_needed

    if current_line:
        wrapped_lines.append(indent + " ".join(current_line))

    return wrapped_lines


def _find_protected_regions(text: str) -> list[tuple[int, int]]:  # ruff: ignore[complex-structure, too-many-branches, too-many-statements]
    """Find regions where sentence wrapping should not occur.

    Per guidance.md: "Not in a context where auto-wrapping is possible:
    - Inline code, links, definition lists, etc."

    Returns:
        List of (start, end) tuples marking protected character positions

    """
    protected = []

    # Find inline code spans: `code`
    # Handle both single and multiple backticks
    i = 0
    while i < len(text):
        if text[i] == "`":
            # Count consecutive backticks
            backtick_count = 0
            start = i
            while i < len(text) and text[i] == "`":
                backtick_count += 1
                i += 1

            # Find matching close
            close_start = i
            while i < len(text):
                if text[i] == "`":
                    close_count = 0
                    while i < len(text) and text[i] == "`":
                        close_count += 1
                        i += 1
                    if close_count == backtick_count:
                        # Found matching close - protect entire span
                        protected.append((start, i))
                        break
                else:
                    i += 1
            else:
                # No matching close found - unclosed code span, skip
                i = close_start
        else:
            i += 1

    # Find links: [text](url) or [text][ref]
    # Pattern: \[...\](\(...\)|[...])
    i = 0
    while i < len(text):  # ruff: ignore[too-many-nested-blocks]
        if text[i] == "[":
            bracket_start = i
            i += 1
            # Find closing ]
            depth = 1
            while i < len(text) and depth > 0:
                if text[i] == "[":
                    depth += 1
                elif text[i] == "]":
                    depth -= 1
                i += 1

            if depth == 0 and i < len(text):
                # Found ], check for ( or [
                if text[i] == "(":
                    # Inline link: [text](url)
                    i += 1
                    depth = 1
                    while i < len(text) and depth > 0:
                        if text[i] == "(":
                            depth += 1
                        elif text[i] == ")":
                            depth -= 1
                        i += 1
                    if depth == 0:
                        # Complete link found
                        protected.append((bracket_start, i))
                elif text[i] == "[":
                    # Reference link: [text][ref]
                    i += 1
                    depth = 1
                    while i < len(text) and depth > 0:
                        if text[i] == "[":
                            depth += 1
                        elif text[i] == "]":
                            depth -= 1
                        i += 1
                    if depth == 0:
                        # Complete reference link found
                        protected.append((bracket_start, i))
        else:
            i += 1

    return protected


def _is_position_protected(pos: int, protected_regions: list[tuple[int, int]]) -> bool:
    """Check if a position falls within any protected region.

    Args:
        pos: Character position to check
        protected_regions: List of (start, end) tuples

    Returns:
        True if position is protected, False otherwise

    """
    return any(start <= pos < end for start, end in protected_regions)


def _replace_spaces_in_link_text(text: str) -> str:  # ruff: ignore[complex-structure, too-many-branches]
    """Replace spaces in link text with non-breaking spaces.

    Per guidance.md: "Before line wrapping, replace all spaces in link texts
    by non-breaking spaces (and similar inline content that can't be wrapped)"

    Args:
        text: Text to process

    Returns:
        Text with spaces in link text replaced by nbsp (U+00A0)

    """
    nbsp = "\u00a0"
    result = []
    i = 0

    while i < len(text):  # ruff: ignore[too-many-nested-blocks]
        if text[i] == "[":
            # Start of potential link
            result.append(text[i])
            i += 1

            # Find closing ]
            depth = 1
            link_text_chars = []
            while i < len(text) and depth > 0:
                if text[i] == "[":
                    depth += 1
                    link_text_chars.append(text[i])
                elif text[i] == "]":
                    depth -= 1
                    if depth > 0:
                        link_text_chars.append(text[i])
                elif text[i] == " ":
                    # Replace space with nbsp in link text
                    link_text_chars.append(nbsp)
                else:
                    link_text_chars.append(text[i])
                i += 1

            # Add link text with nbsp replacements
            result.extend(link_text_chars)

            if depth == 0:
                # Found closing ], add it
                result.append("]")

                # Check if this is actually a link (has ( or [ following)
                if i < len(text) and text[i] in {"(", "["}:
                    # Copy the rest of the link (URL or reference) as-is
                    open_char = text[i]
                    close_char = ")" if open_char == "(" else "]"
                    result.append(text[i])
                    i += 1
                    depth = 1

                    while i < len(text) and depth > 0:
                        if text[i] == open_char:
                            depth += 1
                        elif text[i] == close_char:
                            depth -= 1
                        result.append(text[i])
                        i += 1
        else:
            result.append(text[i])
            i += 1

    return "".join(result)


def _collapse_whitespace(text: str) -> str:
    """Collapse consecutive whitespace while preserving non-breaking spaces.

    Per guidance.md algorithm:
    - Collapse consecutive whitespace into single space
    - Preserve non-breaking spaces (U+00A0)
    - Preserve linebreaks preceded by non-breaking spaces

    Args:
        text: Text to process

    Returns:
        Text with collapsed whitespace

    """
    # Non-breaking space character (U+00A0)
    nbsp = "\u00a0"

    # Replace sequences of regular spaces with single space
    # But preserve non-breaking spaces and their adjacent linebreaks
    result = []
    i = 0
    while i < len(text):
        char = text[i]

        if char == nbsp:
            # Preserve non-breaking space
            result.append(char)
            i += 1
            # If followed by newline, preserve it too
            if i < len(text) and text[i] == "\n":
                result.append(text[i])
                i += 1
        elif char in " \t":
            # Collapse consecutive regular whitespace (spaces/tabs) to single space
            result.append(" ")
            i += 1
            while i < len(text) and text[i] in " \t":
                i += 1
        else:
            result.append(char)
            i += 1

    return "".join(result)


@dataclass(frozen=True)
class _WrapConfig:
    """Configuration for sentence wrapping."""

    sentence_markers: str
    wrap_width: int
    min_line_length: int
    suppression_words: set[str]
    boundary_pattern: re.Pattern[str]


def _build_wrap_config(options: ContextOptions) -> _WrapConfig:
    """Build configuration for sentence wrapping from options."""
    sentence_markers = get_sentence_markers(options)
    wrap_width = get_slw_wrap_width(options)
    min_line_length = get_min_line_length(options)
    suppression_words = _get_suppression_words(options)

    marker_class = re.escape(sentence_markers)
    boundary_pattern = re.compile(r"([" + marker_class + r"])(\s*[\"'\)\]\}]*)\s+")

    return _WrapConfig(
        sentence_markers=sentence_markers,
        wrap_width=wrap_width,
        min_line_length=min_line_length,
        suppression_words=suppression_words,
        boundary_pattern=boundary_pattern,
    )


def _is_suppressed(text_before: str, suppression_words: set[str]) -> bool:
    """Check if text ends with a suppression word (case-insensitive).

    Args:
        text_before: Text to check (will be lowercased)
        suppression_words: Set of suppression words (already lowercase)

    Returns:
        True if text ends with a suppression word

    """
    if not suppression_words:
        return False
    text_lower = text_before.lower()
    for supp_word in suppression_words:
        pattern = r"\b" + re.escape(supp_word) + r"$"
        if re.search(pattern, text_lower):
            return True
    return False


def _apply_sentence_breaks(
    text: str,
    protected_regions: list[tuple[int, int]],
    config: _WrapConfig,
) -> str:
    """Apply sentence breaks with min_line_length threshold."""
    result_parts: list[str] = []
    last_end = 0
    current_line_start = 0

    for match in config.boundary_pattern.finditer(text):
        marker = match.group(1)
        closing = match.group(2)
        marker_pos = match.start() + match.group(0).index(marker)

        result_parts.append(text[last_end : match.start()])

        if _is_position_protected(marker_pos, protected_regions):
            result_parts.append(match.group(0))
            last_end = match.end()
            continue

        text_before = text[: match.start()]
        if _is_suppressed(text_before, config.suppression_words):
            result_parts.append(match.group(0))
            last_end = match.end()
            continue

        current_result = "".join(result_parts)
        current_line_text = current_result[current_line_start:]
        line_length = (
            _display_width(current_line_text)
            + _display_width(marker)
            + _display_width(closing)
        )

        if config.min_line_length > 0 and line_length < config.min_line_length:
            result_parts.append(match.group(0))
            last_end = match.end()
            continue

        result_parts.append(f"{marker}{closing}\n")
        last_end = match.end()
        current_line_start = len("".join(result_parts))

    result_parts.append(text[last_end:])
    return "".join(result_parts)


def _apply_line_wrapping(text: str, wrap_width: int) -> str:
    """Wrap long lines using specified wrap width."""
    if wrap_width <= 0:
        return text

    lines = text.split("\n")
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(_wrap_long_line(line, wrap_width))
    return "\n".join(wrapped_lines)


def wrap_sentences(
    text: str,
    _node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Wrap text by inserting line breaks after sentences.

    This is inspired by slw's sentence-wrapping behavior:
    - Insert line breaks after sentence-ending punctuation
    - Collapse consecutive whitespace per guidance.md
    - Optionally wrap long lines using --slw-wrap setting
    - Preserve existing formatting for code blocks and special syntax
    - Respect abbreviations and suppression words
    - Skip wrapping table-like text to preserve table syntax

    Note: The _node parameter is required by mdformat's postprocessor
    interface but is not used in this implementation.

    Args:
        text: The rendered text to process
        _node: The syntax tree node being rendered (required by interface)
        context: The rendering context with configuration options

    Returns:
        The text with sentence breaks applied

    Raises (via _validate_sentence_markers):
        ConfigurationError: If configuration values are invalid

    """
    if not should_wrap_sentences(context.options):
        return text

    if _is_table_text(text):
        return text

    if not text or not text.strip():
        return text

    mdformat_wrap = context.options.get("mdformat", {}).get("wrap")
    if mdformat_wrap is not None and mdformat_wrap not in {"keep", None}:
        logger.warning(
            "mdformat's --wrap is set to '%s'. "
            "Consider using --wrap=keep to avoid conflicts with slw sentence wrapping. "
            "Use --slw-wrap instead for line width control.",
            mdformat_wrap,
        )

    config = _build_wrap_config(context.options)

    text = _collapse_whitespace(text)
    protected_regions = _find_protected_regions(text)
    wrapped = _apply_sentence_breaks(text, protected_regions, config)
    wrapped = _replace_spaces_in_link_text(wrapped)
    return _apply_line_wrapping(wrapped, config.wrap_width)

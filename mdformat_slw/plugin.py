"""Public Extension for slw-style sentence wrapping.

This module provides the mdformat plugin interface for sentence wrapping
functionality. It registers CLI arguments and postprocessors that wrap
text by inserting line breaks after sentence-ending punctuation.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer.typing import Postprocess, Render

from ._sentence_wrapper import wrap_sentences


def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
    """Add options to the mdformat CLI.

    Configuration is stored in `mdit.options["mdformat"]["plugin"]["slw"]`

    Note: When using --slw-wrap, consider disabling mdformat's line wrapping
    with --wrap=keep to avoid conflicts between the two wrapping mechanisms.

    Args:
        group: Argument group to add options to

    """
    group.add_argument(
        "--no-wrap-sentences",
        action="store_const",
        const=True,
        help="Disable slw sentence wrapping (enabled by default)",
    )
    group.add_argument(
        "--slw-markers",
        type=str,
        help="Characters that mark sentence endings for slw (default: .!?)",
    )
    group.add_argument(
        "--slw-wrap",
        type=int,
        help="Wrap lines at specified width (default: 88). "
        "Set to 0 to disable. Use with --wrap=keep to disable mdformat's wrapping.",
    )
    group.add_argument(
        "--slw-min-line",
        type=int,
        dest="slw_min_line",
        help="Minimum line length before sentence wrapping (default: 40). "
        "Set to 0 to always wrap after sentences (aggressive mode).",
    )
    group.add_argument(
        "--slw-lang",
        type=str,
        dest="lang",
        help="Language code for abbreviation list (default: ac). "
        "Supported: ac, en, de, es, fr, it",
    )
    group.add_argument(
        "--slw-abbreviations",
        type=str,
        dest="abbreviations",
        help="Comma-separated custom abbreviations (extends language list by default)",
    )
    group.add_argument(
        "--slw-abbreviations-only",
        action="store_const",
        const=True,
        dest="abbreviations_only",
        help="Use only custom abbreviations, ignore language lists",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the markdown-it parser.

    The slw plugin doesn't add new markdown syntax, so no parser
    modifications are needed. All functionality is implemented via
    postprocessors that run after rendering.

    Note: We don't enable table parsing here because that would require
    adding full table renderers. Instead, we detect table-like patterns
    in the postprocessor and skip wrapping them.

    Args:
        mdit: The markdown-it parser instance (unused)

    """


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
# The slw plugin doesn't need custom renderers, only postprocessors.
RENDERERS: Mapping[str, Render] = {}

# A mapping from `RenderTreeNode.type` to a `Postprocess` that does
# postprocessing for the output of the `Render` function. Unlike
# `Render` funcs, `Postprocess` funcs are collaborative: any number of
# plugins can define a postprocessor for a syntax type and all of them
# will run in series.
#
# Apply sentence wrapping to paragraphs and other text-containing nodes.
# The postprocessor is active by default; use --no-wrap-sentences to disable.
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "paragraph": wrap_sentences,
}

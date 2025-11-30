"""Public Extension for mdslw-style sentence wrapping.

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

    Configuration is stored in `mdit.options["mdformat"]["plugin"]["mdslw"]`

    Note: When using --mdslw-wrap, consider disabling mdformat's line wrapping
    with --wrap=keep to avoid conflicts between the two wrapping mechanisms.

    Args:
        group: Argument group to add options to

    """
    group.add_argument(
        "--no-wrap-sentences",
        action="store_const",
        const=True,
        help="Disable mdslw sentence wrapping (enabled by default)",
    )
    group.add_argument(
        "--mdslw-markers",
        type=str,
        default=".!?:",
        help="Characters that mark sentence endings for mdslw (default: .!?:)",
    )
    group.add_argument(
        "--mdslw-wrap",
        type=int,
        default=0,
        help="Wrap lines at specified width (default: 0 = disabled). "
        "Use with --wrap=keep to disable mdformat's wrapping.",
    )


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the markdown-it parser.

    The mdslw plugin doesn't add new markdown syntax, so no parser
    modifications are needed. All functionality is implemented via
    postprocessors that run after rendering.

    Args:
        mdit: The markdown-it parser instance (unused)

    """
    # No markdown-it plugins needed for sentence wrapping
    # This function is required by mdformat's plugin interface


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
# The mdslw plugin doesn't need custom renderers, only postprocessors.
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

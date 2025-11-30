# mdformat-slw

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for semantic line wrapping (slw).

This plugin wraps markdown text by inserting line breaks after sentence-ending punctuation, making diffs cleaner and easier to review.

## Features

- **Automatic sentence wrapping** at configurable punctuation marks (default: `.!?:`)
- **Enabled by default** - no flags needed to activate
- Optional maximum line width enforcement with `--slw-wrap`
- Preserves markdown formatting (bold, italic, links, etc.)
- Handles edge cases: quoted text, parentheses, brackets

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. Sentence wrapping is **enabled by default**. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### CLI

```sh
# Sentence wrapping enabled by default
mdformat document.md

# With line width enforcement
mdformat document.md --slw-wrap 80 --wrap=keep

# Disable sentence wrapping
mdformat document.md --no-wrap-sentences
```

#### Options

**Basic Options:**

- `--no-wrap-sentences`: Disable sentence wrapping (enabled by default)
- `--slw-markers TEXT`: Characters that mark sentence endings (default: `.!?:`)
- `--slw-wrap INTEGER`: Maximum line width for wrapping (default: 80)

**Abbreviation Detection:**

- `--slw-lang TEXT`: Space-separated language codes for abbreviation lists (default: `ac`)
    - Supported: `ac` (all-caps only), `en`, `de`, `es`, `fr`, `it`
- `--slw-abbreviations-mode TEXT`: Abbreviation detection mode (default: `default`)
    - `default`: Use built-in language lists
    - `off`: Disable abbreviation detection
    - `extend`: Add custom abbreviations to built-in lists
    - `override`: Replace built-in lists with custom abbreviations
- `--slw-abbreviations TEXT`: Comma-separated custom abbreviations (e.g., `Dr.,Prof.,etc.`)
- `--slw-suppressions TEXT`: Space-separated words to add to suppression list
- `--slw-ignores TEXT`: Space-separated words to remove from suppression list
- `--slw-case-sensitive`: Enable case-sensitive abbreviation matching (default: case-insensitive)

> **Note:** When using `--slw-wrap`, consider adding `--wrap=keep` to disable mdformat's built-in line wrapping and avoid conflicts.

### Configuration File

Create a `.mdformat.toml` file in your project root:

```toml
[plugin.slw]
# Disable sentence wrapping (enabled by default)
no_wrap_sentences = false

# Customize sentence markers
slw_markers = ".!?:"

# Set line width wrapping (default: 80)
slw_wrap = 80

# Configure abbreviation detection
lang = "en de"  # Use English and German abbreviations
abbreviations_mode = "extend"  # Add custom to built-in lists
abbreviations = "Dr.,Prof.,etc."  # Custom abbreviations
case_sensitive = false  # Case-insensitive matching (default)

# Recommended: disable mdformat's wrapping to avoid conflicts
[mdformat]
wrap = "keep"
```

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 1.0.0
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-slw
```

### uvx

```sh
uvx --with mdformat-slw mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-slw
mdformat document.md
```

### Python API

```python
import mdformat

text = """
This is a test. It has multiple sentences! Does it work?
"""

# Sentence wrapping enabled by default
result = mdformat.text(text, extensions={"slw"})

print(result)
# Output:
# This is a test.
# It has multiple sentences!
# Does it work?

# With line width wrapping
result = mdformat.text(
    text,
    extensions={"slw"},
    options={"slw_wrap": 80}
)

# Disable sentence wrapping
result = mdformat.text(
    text,
    extensions={"slw"},
    options={"no_wrap_sentences": True}
)
```

## Example

### Basic Wrapping

**Input:**

```markdown
This is a long sentence. It contains multiple clauses! Does it work? Yes it does.
```

**Output (default behavior):**

```markdown
This is a long sentence.
It contains multiple clauses!
Does it work?
Yes it does.
```

### Abbreviation Detection

**Input:**

```markdown
Dr. Smith met with Prof. Johnson at 3 p.m. They discussed the project etc. and other topics.
```

**Output (abbreviations preserved):**

```markdown
Dr. Smith met with Prof. Johnson at 3 p.m.
They discussed the project etc. and other topics.
```

### Link Protection

**Input:**

```markdown
Check [example.com](https://example.com). Use `config.json` for settings. Done!
```

**Output (links and code preserved):**

```markdown
Check [example.com](https://example.com).
Use `config.json` for settings.
Done!
```

## How It Works

### Wrapping Rules

When one of the limited number of characters (`.!?:` by default) which serve as end-of-sentence markers occur alone, mdformat-slw will wrap **except** when:

1. Not in a context where auto-wrapping is possible:
    - Inline code, links, definition lists, etc.
    - Code Blocks
    - Tables
    - HTML Blocks
1. When the wrapped term is an abbreviation:
    - Multiple end-of-sentence markers occur (such as `p.m.` or `e.g.`)
    - Identified as an abbreviation from language-specific lists (`Dr.`, `Prof.`, `etc.`, etc.)
    - Matched against custom abbreviations specified via `--slw-abbreviations`
    - Part of user-specified suppression words via `--slw-suppressions`
1. Abbreviation matching is case-insensitive by default (use `--slw-case-sensitive` to change)

### Algorithm

1. Insert a line break after every character that ends a sentence which complies with the above rules and exceptions
1. Collapse all consecutive whitespace into a single space. While doing so, preserve both non-breaking spaces and linebreaks that are preceded by non-breaking spaces
1. Before line wrapping, replace all spaces in link texts by non-breaking spaces (and similar inline content that can't be wrapped)
1. Wrap lines that are longer than the maximum line width, if set, (80 characters by default) without splitting words or splitting at non-breaking spaces while also keeping indents in tact.

## Acknowledgments

This plugin is inspired by and named after [mdslw](https://github.com/razziel89/mdslw) by [@razziel89](https://github.com/razziel89). The original `mdslw` is an excellent standalone tool for semantic line wrapping of markdown files.

**Why create mdformat-slw?**

The [mdformat](https://github.com/executablebooks/mdformat) ecosystem uses a plugin architecture where formatters must integrate with mdformat's AST-based processing pipeline. While `mdslw` works great as a standalone tool, it cannot be used as an mdformat plugin directly. This plugin reimplements semantic line wrapping concepts to work natively within mdformat, enabling:

- Seamless integration with other mdformat plugins
- Consistent formatting when mdformat is your primary markdown formatter
- Use in pre-commit hooks alongside mdformat's other capabilities

The plugin is named `slw` (not `mdslw`) to clearly distinguish it from the original tool and avoid confusion, since the implementations differ.

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-slw/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-slw/actions/workflows/tests.yml/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-slw/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-slw.svg
[pypi-link]: https://pypi.org/project/mdformat-slw

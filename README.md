# mdformat-slw

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for semantic line wrapping (slw).

This plugin wraps markdown text by inserting line breaks after sentence-ending punctuation, making diffs cleaner and easier to review.

## Features

- **Automatic sentence wrapping** at configurable punctuation marks (default: `.!?`)
- **Soft wrapping mode** - only wraps when lines exceed a threshold (default: 40 chars)
- **Enabled by default** - no flags needed to activate
- Optional maximum line width enforcement with `--slw-wrap` (default: 88)
- Preserves markdown formatting (bold, italic, links, etc.)
- Handles edge cases: quoted text, parentheses, brackets

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. Sentence wrapping is **enabled by default**. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### CLI

```sh
# Sentence wrapping enabled by default
mdformat document.md

# With line width enforcement
mdformat document.md --slw-wrap 88 --wrap=keep

# Disable sentence wrapping
mdformat document.md --no-wrap-sentences

# Aggressive mode (always wrap after sentences)
mdformat document.md --slw-min-line 0
```

#### Options

**Wrapping Behavior:**

- `--no-wrap-sentences`: Disable sentence wrapping (enabled by default)
- `--slw-markers TEXT`: Characters that mark sentence endings (default: `.!?`)
- `--slw-wrap INTEGER`: Maximum line width for wrapping (default: 88, set to `0` to disable)
- `--slw-min-line INTEGER`: Minimum line length before sentence wrapping (default: 40)
    - Set to `0` for aggressive mode (always wrap after sentences)
    - Lines shorter than this threshold won't be wrapped, creating a "soft wrap" effect

**Abbreviation Handling:**

- `--slw-lang TEXT`: Language code for abbreviation list (default: `ac`)
    - Supported: `ac` (Author's Choice), `en`, `de`, `es`, `fr`, `it`
- `--slw-abbreviations TEXT`: Comma-separated custom abbreviations (extends language list by default)
- `--slw-abbreviations-only`: Use only custom abbreviations, ignore language lists

> **Note:** When using `--slw-wrap`, consider adding `--wrap=keep` to disable mdformat's built-in line wrapping and avoid conflicts.

## Common Patterns

Use default abbreviations (Author's Choice):

```bash
mdformat document.md
```

Use language-specific abbreviations:

```bash
mdformat document.md --slw-lang=en
```

Extend language list with custom abbreviations:

```bash
mdformat document.md --slw-lang=en --slw-abbreviations="NASA,FBI,CustomCorp"
```

Use only custom abbreviations:

```bash
mdformat document.md --slw-abbreviations-only --slw-abbreviations="NASA,FBI"
```

Aggressive wrapping (always wrap after sentences):

```bash
mdformat document.md --slw-min-line=0
```

Disable sentence wrapping:

```bash
mdformat document.md --no-wrap-sentences
```

### Configuration File

Create a `.mdformat.toml` file in your project root:

```toml
[plugin.slw]
# Disable sentence wrapping (enabled by default)
no_wrap_sentences = false

# Customize sentence markers (default: ".!?")
slw_markers = ".!?"

# Set line width wrapping (default: 88)
slw_wrap = 88

# Minimum line length before wrapping (default: 40)
# Set to 0 for aggressive mode (always wrap)
slw_min_line = 40

# Configure abbreviation detection
lang = "en"  # Language for abbreviation list (ac, en, de, es, fr, it)
abbreviations = "Corp,Inc,NASA"  # Custom abbreviations (extends language list)
abbreviations_only = false  # Set to true to use only custom abbreviations

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
uvx --with=mdformat-slw mdformat
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
result = mdformat.text(text, extensions={"slw"}, options={"slw_wrap": 88})

# Aggressive mode (always wrap)
result = mdformat.text(text, extensions={"slw"}, options={"slw_min_line": 0})

# Disable sentence wrapping
result = mdformat.text(text, extensions={"slw"}, options={"no_wrap_sentences": True})
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

When one of the limited number of characters (`.!?` by default) which serve as end-of-sentence markers occur alone, mdformat-slw will wrap **except** when:

1. **Soft wrap mode (default)**: Line doesn't exceed minimum length threshold (40 chars by default)
    - Short sentences stay on the same line for better readability
    - Set `--slw-min-line 0` for aggressive mode (always wrap)
1. Not in a context where auto-wrapping is possible:
    - Inline code, links, definition lists, etc.
    - Code Blocks
    - Tables
    - HTML Blocks
1. When the wrapped term is an abbreviation:
    - Multiple end-of-sentence markers occur (such as `p.m.` or `e.g.`)
    - Identified as an abbreviation from language-specific lists (`Dr.`, `Prof.`, `etc.`, etc.)
    - Matched against custom abbreviations specified via `--slw-abbreviations`
1. Abbreviation matching is always case-insensitive

### Algorithm

1. Collapse all consecutive whitespace into a single space. While doing so, preserve both non-breaking spaces and linebreaks that are preceded by non-breaking spaces
1. Find protected regions (inline code, links) where sentence breaks should not occur
1. Insert a line break after every character that ends a sentence which complies with the above rules and exceptions
1. Replace all spaces in link texts by non-breaking spaces (and similar inline content that can't be wrapped)
1. Wrap lines that are longer than the maximum line width, if set, (88 characters by default) without splitting words or splitting at non-breaking spaces while also keeping indents in tact

## Language Support and Limitations

### Supported Languages

mdformat-slw provides built-in abbreviation lists for:

- **ac** (Author's Choice - default): 77 common abbreviations including titles, time, Latin terms, academic, business, and geography
- **en** (English): 17 abbreviations
- **de** (German): 54 abbreviations
- **es** (Spanish): 36 abbreviations
- **fr** (French): 42 abbreviations
- **it** (Italian): 40 abbreviations

These languages work well with the default ASCII punctuation markers (`.!?`).

### Out of Scope by Design

mdformat-slw targets non-symbolic, left-to-right languages. Sentence detection relies on
whitespace after a punctuation marker, and line wrapping relies on space-delimited word
boundaries, neither of which holds for CJK or RTL scripts. Supporting them properly means
Unicode line breaking (UAX #14), kinsoku shori, CJK word segmentation, and bidi handling,
which is a different scope of project. These are not planned:

- **CJK languages (Chinese, Japanese, Korean)**: natural text has no spaces between
  sentences, so sentence-boundary detection won't find them. Text still passes through
  unchanged (wcwidth accounts for double-width characters when computing line width), but
  wrapping only kicks in if you manually space sentences, e.g.
  `これは最初の文です。 これは2番目の文です。`, and configure CJK markers with
  `--slw-markers=".!?。！？"`. See `tests/format/fixtures/lang_ja.md` and `lang_ko.md`.
- **Arabic and other RTL languages**: no bidi handling, and native punctuation
  (`؟` U+061F, `،` U+060C, `؛` U+061B) isn't in the default marker set. ASCII markers
  (`.!?`) still work, and `--slw-markers` / `--slw-abbreviations` can add Arabic-specific
  ones if you want partial support, but this isn't a design target.

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

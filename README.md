# mdformat-slw

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for semantic line wrapping (slw), which breaks lines after sentence-ending punctuation so that diffs stay small and readable.

Wrapping is on by default. A break is inserted after each end-of-sentence marker (`.!?`) except when:

- The line is shorter than the minimum length (40 characters by default), which keeps short sentences together. Set `--slw-min-line=0` to always wrap
- The text can't be wrapped: inline code, links, definition lists, code blocks, tables, and HTML blocks
- The marker ends an abbreviation, either because multiple markers occur (`p.m.`, `e.g.`) or because the word is in the language list or in `--slw-abbreviations`. Matching is case-insensitive

The algorithm collapses consecutive whitespace to a single space (preserving non-breaking spaces and the linebreaks that follow them), finds the protected regions, inserts the sentence breaks, replaces spaces in link text with non-breaking spaces, and finally wraps anything still longer than `--slw-wrap` without splitting words or indents.

For examples, see [./tests/pre-commit-test.md](https://raw.githubusercontent.com/KyleKing/mdformat-slw/main/tests/pre-commit-test.md) and [./tests/format/fixtures](https://github.com/KyleKing/mdformat-slw/tree/main/tests/format/fixtures)

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. For additional information on plugins, see [the official `mdformat` documentation here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

```sh
mdformat document.md

# Recommended when using --slw-wrap, because --wrap=keep turns off mdformat's own wrapping
mdformat document.md --slw-wrap=88 --wrap=keep
```

### pre-commit/prek

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
```

## Configuration

`mdformat-slw` adds the CLI arguments:

- `--no-wrap-sentences` to turn off sentence wrapping
- `--slw-markers` for the characters that end a sentence (default: `.!?`)
- `--slw-wrap` for the maximum line width (default: `88`, set to `0` to disable)
- `--slw-min-line` for the shortest line that may be wrapped (default: `40`, set to `0` to always wrap)
- `--slw-lang` for the built-in abbreviation list (default: `ac`, one of `ac`, `en`, `de`, `es`, `fr`, or `it`)
- `--slw-abbreviations` for a comma-separated list of extra abbreviations, such as `"NASA,FBI,CustomCorp"`
- `--slw-abbreviations-only` to use only those abbreviations and skip the language list

You can also use the toml configuration (https://mdformat.readthedocs.io/en/stable/users/configuration_file.html):

```toml
# .mdformat.toml

[plugin.slw]
no_wrap_sentences = false
slw_markers = ".!?"
slw_wrap = 88
slw_min_line = 40
lang = "en"
abbreviations = "Corp,Inc,NASA"
abbreviations_only = false

[mdformat]
wrap = "keep"
```

Or the Python API:

```py
import mdformat

mdformat.text("This is a test. It has multiple sentences!", extensions={"slw"})
# 'This is a test. It has multiple sentences!\n'

mdformat.text("This is a test. It has multiple sentences!", extensions={"slw"}, options={"slw_min_line": 0})
# 'This is a test.\nIt has multiple sentences!\n'
```

## Example

```markdown
Dr. Smith met with Prof. Johnson at 3 p.m. to review the draft. They discussed the wrapping rules etc. and agreed on the defaults.
```

Becomes:

```markdown
Dr. Smith met with Prof. Johnson at 3 p.m. to review the draft.
They discussed the wrapping rules etc. and agreed on the defaults.
```

`p.m.` and `etc.` are abbreviations, so no break follows them.

## Language Support

Abbreviation lists are built in for `ac` (Author's Choice, the default, which covers titles, time, Latin, academic, business, and geography terms), `en`, `de`, `es`, `fr`, and `it`. The lists are in [`_language_data.py`](https://github.com/KyleKing/mdformat-slw/blob/main/mdformat_slw/_language_data.py).

`mdformat-slw` targets non-symbolic, left-to-right languages. Sentence detection relies on whitespace after a marker and wrapping relies on space-delimited words, but neither are applicable CJK or RTL scripts. Doing those properly means Unicode line breaking (UAX #14), kinsoku shori, word segmentation, and bidi handling, which is a different project, so they aren't planned:

- CJK text has no spaces between sentences, so no boundaries are found. The text passes through unchanged (wcwidth accounts for double-width characters when measuring line length), and wrapping only applies if you space the sentences yourself, e.g. `これは最初の文です。 これは2番目の文です。`, and set `--slw-markers=".!?。！？"`. See `tests/format/fixtures/lang_ja.md` and `lang_ko.md`
- Arabic and other RTL text gets no bidi handling, and the native punctuation (`؟` U+061F, `،` U+060C, `؛` U+061B) isn't in the default marker set. ASCII markers still work and `--slw-markers` / `--slw-abbreviations` can add the rest for partial support

## Acknowledgments

This plugin is inspired by and named after [razziel89/mdslw](https://github.com/razziel89/mdslw), which is an excellent standalone tool for semantic line wrapping. `mdslw` can't be used as an mdformat plugin because mdformat formats from its own AST, so this package reimplements the idea natively, which lets it run alongside other mdformat plugins and in the same pre-commit hook. Overtime, the implementations have diverged, but I'm always open to submissions and feature requests to continually improve the developer experience.

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-slw/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-slw/actions/workflows/tests.yml/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-slw/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-slw.svg
[pypi-link]: https://pypi.org/project/mdformat-slw

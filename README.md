# mdformat-mdsf

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for [mdslw](https://github.com/razziel89/mdslw)-style sentence wrapping.

This plugin wraps markdown text by inserting line breaks after sentences, making diffs more readable for version control. Inspired by mdslw, but implemented as a native mdformat plugin

## Features

- **Sentence wrapping**: Inserts line breaks after sentences for better version control diffs
- **Configurable sentence markers**: Default `.!?:` can be customized
- **Line width control**: Optional maximum line width (default 80 characters)
- **TOML configuration**: Configure via `.mdformat.toml` or CLI arguments

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized.

### CLI Arguments

```sh
# Enable sentence wrapping
mdformat --wrap-sentences README.md

# Customize sentence markers
mdformat --wrap-sentences --sentence-markers ".!?" README.md

# Set maximum line width
mdformat --wrap-sentences --max-line-width 100 README.md
```

### TOML Configuration

Create a `.mdformat.toml` file:

```toml
[plugin.mdslw]
wrap_sentences = true
sentence_markers = ".!?:"
max_line_width = 80
```

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.19
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mdsf
```

### uvx

```sh
uvx --from mdformat-mdsf mdformat --wrap-sentences README.md
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-mdsf
```

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mdsf/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mdsf/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mdsf/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mdsf.svg
[pypi-link]: https://pypi.org/project/mdformat-mdsf

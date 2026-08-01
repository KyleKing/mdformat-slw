# mdformat-mkdocs drops the start of an ordered list that does not begin at 1

Filed from `mdformat-slw` on 2026-07-27. The fix belongs in
[mdformat-mkdocs](https://github.com/KyleKing/mdformat-mkdocs), not here.

Versions used to reproduce: `mdformat` 1.0.0, `mdformat-mkdocs` 5.2.1.

## Context

`mdformat` verifies that the formatted output renders to the same HTML as the input
before it writes a file. When a plugin changes the HTML, `mdformat` refuses to write
and exits non-zero, so the `mdformat` pre-commit hook fails the commit and CI with:

```
Formatted Markdown renders to different HTML than input Markdown. This is a bug
in mdformat or one of its installed plugins.
```

An ordered list whose first item is a number other than 1 carries that number into the
HTML as `<ol start="N">`. Core `mdformat` preserves it: `_context.py` reads
`node.attrs.get("start")` and prefixes the first item with the starting number, then
uses `1.` for the rest (or counts up from the start when `number` is enabled).

## Expectation

Formatting `5. one` / `6. two` with the `mkdocs` extension keeps the list starting at
5, so the HTML keeps `<ol start="5">` and the file is written.

## Actual behavior

The list is renumbered down to 1, `<ol start="5">` becomes `<ol>`, and the file is
never written.

```
in                : '5. one\n6. two\n'
out (default)     : '1. one\n1. two\n'
out (number=true) : '1. one\n2. two\n'
html in           : '<ol start="5">\n<li>one</li>\n<li>two</li>\n</ol>\n'
html out          : '<ol>\n<li>one</li>\n<li>two</li>\n</ol>\n'
```

Both the default and `number = true` modes lose the start.

## Minimal repro

```bash
printf '5. one\n6. two\n' > ol.md
mdformat ol.md   # with mdformat-mkdocs installed; exits 1, file unchanged
```

Or through the API:

```python
import mdformat

mdformat.text("5. one\n6. two\n", extensions={"mkdocs"})  # -> '1. one\n1. two\n'
```

## Where the code goes wrong

`mdformat_mkdocs/_normalize_list.py`, `_format_new_content` (around line 400). The
postprocessor works on the already-rendered text and re-derives the numbering from
scratch:

```python
first_peer = line.prev_list_peers[-1] if line.prev_list_peers else line.parsed
base_num = 0 if first_peer.content.startswith("0.") else 1
counter = len(line.prev_list_peers) + base_num if inc_numbers else base_num
new_bullet = f"{counter}."
```

`base_num` only knows about two starts, 0 and 1. Every other start collapses to 1. The
`0.` branch is the shape a general fix wants, applied to one value instead of all of
them.

The start is available. `normalize_list` receives the `ordered_list`
`RenderTreeNode`, and `node.attrs` holds `{'start': 5}` for the repro above, so the
value core `mdformat` uses is already in hand at the point where the numbering is
recomputed.

## Options

**Thread the node's `start` through as the base.** Read `node.attrs.get("start", 1)`
in `normalize_list` and pass it to `_format_new_content` in place of the hardcoded
`base_num`, matching core `mdformat`: the first item keeps the start, later items get
`1.` by default and count up from the start under `number = true`. This is the only
option that both preserves the HTML and keeps normalizing the list. The work is in
nested lists, because `base_num` is currently derived per line while the start belongs
to the owning list node, so each sublist needs its own base rather than one value for
the whole call. Output changes for documents that start at N other than 1, and none of
those documents format today, so nothing that currently works regresses.

**Leave a non-1 start alone.** Detect that the first item is not `1.` or `0.` and skip
renumbering for that list. Smaller change and smaller blast radius, but it also drops
indentation normalization and semantic-break alignment for those lists, so two files
with the same content get formatted differently depending on the first number.

**Do nothing upstream and restart lists at 1 in the consuming repo.** This is the
workaround applied in `mdformat-slw` (see below). It costs nothing upstream and leaves
a trap: the failure surfaces as a generic "report a bug in mdformat" message with no
pointer to the list that caused it.

The first option is the one worth doing. The third is what every affected repo has to
do in the meantime.

## How this surfaced

`mdformat-slw` CI was red from 2025-12-01 until 2026-07-26. The failing job was `prek`,
and the file was `MULTILINGUAL_ANALYSIS.md`, which numbered an implementation plan 1
through 10 continuously across three `Phase` headings. The blank-line-separated headings
split it into three lists starting at 1, 5, and 8, so the Phase 2 and Phase 3 lists each
tripped the check. The fix applied there was restarting each phase list at 1. The file
was deliberately kept out of the hook's exclude list, so the repo picks up the real fix
as soon as it lands upstream.

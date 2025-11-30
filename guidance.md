When one of the limited number of characters (.!?: by default) which serve as end-of-sentence markers occur alone, mdformat-mdslw will wrap except when:

1. Not in a context where auto-wrapping is possible:
    - Inline code, links, definition lists, etc.
    - Code Blocks
    - Tables
    - HTML Blocks
1. When the wrapped term is an abbreviation (either multiple end-of-sentence markers occur (such as p.m. or e.g.) or when identified as an abbreviation (Dr. etc., or similar) (TBD on how abbreviations will be identified?)
1. When the last word is part of a user-specified set of case-insensitive known words (either by specific language or global)

Algorithm

1. Insert a line break after every character that ends a sentence which complies with the above rules and exceptions
1. Collapse all consecutive whitespace into a single space. While doing so, preserve both non-breaking spaces and linebreaks that are preceded by non-breaking spaces
1. Before line wrapping, replace all spaces in link texts by non-breaking spaces (and similar inline content that can't be wrapped)
1. Wrap lines that are longer than the maximum line width, if set, (80 characters by default) without splitting words or splitting at non-breaking spaces while also keeping indents in tact.

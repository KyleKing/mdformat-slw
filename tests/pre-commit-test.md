# Test file for slw sentence wrapping

## Basic Sentences with Different Punctuation

This is a test paragraph with multiple sentences.
It should wrap after periods!
Does it handle question marks correctly?
Of course it does:
even colons work as sentence markers.

## Abbreviation Detection (Phase 1)

Dr. Smith arrived at 3 p.m. yesterday.
Prof. Johnson met with him at the university.
They discussed the project etc. and other important topics.
The meeting lasted approx.
two hours.

Common abbreviations like e.g. and i.e. should not trigger wrapping.
Mrs. Taylor joined them later.
Mr. Brown sent his regards via email.

Multiple periods like p.m. or a.m. are preserved correctly.
The file size was 2.5 MB.
Temperature readings showed 98.6 degrees.

## Whitespace Collapsing (Phase 3)

This sentence has excessive spaces.
They should be collapsed!
Does it work?
Yes:
whitespace is normalized.

Line breaks with regular spaces should collapse.
But non-breaking spaces should be preserved.
This maintains formatting!

## Indentation Preservation (Phase 4)

- First list item has one sentence.
  Second sentence here!
- Second list item has multiple sentences.
  It should wrap correctly.
  Even with exclamation marks!
- This third item asks a question.
  Does it wrap properly?
  Let's add more:
  it definitely should.
  - Nested items work too.
    They maintain proper indentation.
    The wrapping respects list structure!
  - Another nested item here.
    With several sentences of varying lengths.
    Some short.
    Some much longer to test the constraints.

1. Ordered lists work similarly.
   Each sentence gets its own line.
   This maintains readability!
1. The second item continues the pattern.
   Multiple sentences here too?
   Absolutely:
   they all wrap.
1. Even complex numbered items.
   With many sentences.
   And different punctuation marks!
   Does it work?
   Yes:
   it handles everything.

## Inline Code Protection (Phase 5)

This sentence contains `code.py` in the middle.
Another sentence!
The code should not trigger wrapping.

Check `import sys.path` for the module.
It works correctly!
Multiple code spans like `file.txt` and `config.json` are handled.
Great!

Double backticks work too:
`` code with `backticks`.txt `` is preserved.
Another sentence follows!

## Link Protection (Phase 5 & 6)

See [example.com](https://example.com) for more info.
Another sentence here!
Links are protected.

Visit [the site](https://test.example.com/page.html) for details.
Done!
Link URLs with periods work fine.

Check [this out][ref] for more.
Another sentence!
Reference links work too.

Read [section 2.1][ref] carefully.
Important information!
Links with periods in text are handled.

Multiple links like [link1](url1) and [link2](url2) work.
Done!
All preserved correctly.

## Mixed Inline Elements (Phase 5)

Use `config.json` and see [docs](url) for help.
Both work!
Code and links together.

This is `` code with `backticks`.txt `` and [example.com](url) combined.
Another sentence!
Everything preserved.

## Line Width Wrapping (Phase 7)

This extraordinarily verbose and unnecessarily elongated sentence is
specifically crafted to exceed the standard eighty-character line width
limitation.
Following that long sentence, here's a short one.
Then another medium-length sentence to vary the rhythm.

## Blockquotes with Sentences

> This is a blockquote with multiple sentences.
> Each one should wrap properly.
> The quote marker should be preserved!
>
> Even with paragraph breaks in quotes.
> The formatting remains consistent?
> Yes, it does:
> perfectly.

> Nested quotes can be tricky.
>
> > But they should work fine.
> > Each level maintains its markers.
> > Sentence wrapping respects the structure!

## Inline Formatting Preservation

This paragraph contains **bold text that spans a sentence boundary.
It should wrap correctly!** And *italic text works the same way.
Even with multiple sentences?* Yes, it does:
the formatting is preserved.

Combining different elements like **bold**, *italic*, `code`, and
[links](https://test.com) with multiple sentences.
Does everything work together?
It absolutely should:
the plugin must handle mixed content!

## Language-Specific Abbreviations

### German Abbreviations (lang: de)

Dr. Müller traf Frau Schmidt um 15 Uhr.
Sie besprachen das Projekt bzw.
die kommenden Aufgaben.
Die Besprechung dauerte ca. zwei Stunden.

### French Abbreviations (lang: fr)

M.
Dubois a rencontré Mme Martin à Paris.
Ils ont discuté du projet etc. et d'autres sujets importants.

### Spanish Abbreviations (lang: es)

El Dr. García se reunió con la Sra.
López.
Discutieron el proyecto etc. y otros temas relevantes.

## Edge Cases and Special Scenarios

### Periods in Numbers

The value is 3.14159 for pi.
Another sentence!
Numbers with decimals work fine.

Version 2.5.1 was released yesterday.
Great news!
Semantic versions are preserved.

### URLs and Domain Names

Visit https://example.com for details.
Another sentence!
URLs are protected.

Check out test.example.co.uk for more.
Done!
Complex domains work fine.

### Abbreviations at End of Sentence

He works for NASA.
Another sentence here!
Acronyms at sentence end are tricky.

The meeting is at 3 p.m. We should arrive early!
Time abbreviations work correctly.

### Mixed Content in Lists

- Item with `code.py` and [link](url) elements.
  Multiple sentences!
  Everything works.
- Dr. Smith mentioned the e.g. example.
  Another sentence!
  Abbreviations in lists work.
- Visit [site](https://example.com) for info.
  Done!
  Links in lists are protected.

## Code Blocks Should Not Be Affected

```python
# This code block should never be modified by sentence wrapping.
def test_function():
    print("Hello. World. Test.")  # Periods in code don't trigger wrapping.
    return True
```

```markdown
# Even markdown code blocks remain untouched. With periods. And other punctuation!
This is not wrapped. Despite having sentences. The code block protects it.
```

## Tables

| Column 1 | Column 2 | Column 3 |
| --------------------------------- | ------------------------ | ---------------
| This cell has sentences. Multiple | Another cell. More text! | Final cell. End |
| Row two. More content! | Testing. Works! | Great. Done! |

## Custom Abbreviation Override

Testing with custom abbreviations like Corp. and Inc. should work.
These are business terms!
They need special handling.

## Case Sensitivity Tests

Both Dr. and dr. should be handled based on case-sensitive flag.
Testing uppercase vs lowercase!
Default is case-insensitive.

## Suppression Words

Testing custom suppression words that prevent wrapping.
The word "test" might be suppressed.
Another sentence!

## Multiple Markers in Sequence

What about questions?
Or exclamations!
Yes:
all markers work correctly.

Quick succession of sentences.
One.
Two.
Three!
All wrapped properly.

## Very Long Sentences for Width Testing

This is an extraordinarily long sentence that contains numerous clauses,
subordinate phrases, descriptive elements, and sufficient verbose content to
substantially exceed the configured maximum line width of eighty characters that
serves as the default wrapping threshold for the mdformat-slw plugin when the
slw-wrap option is set.
After that monster sentence, here's a short one.
Medium length sentence here too!

## Combining All Features

Dr. Smith checked `config.json` and visited [the site](https://example.com) at 3
p.m. yesterday.
He found the information e.g. the system settings were correct!
Prof. Johnson confirmed the results.
Everything worked perfectly:
all features integrated seamlessly.

Testing `code.py` with [multiple](url1) links [here](url2) and abbreviations
like etc. works!
The system handles Dr. titles and i.e. abbreviations correctly.
Great results!

## Unicode and Special Characters

Testing with émojis and spécial characters works perfectly!
Even with Japanese text like これは文章です。 And mathematical expressions:
x² + y² = z².
Does it handle all of these?
Certainly:
Unicode support is essential!

## Horizontal Rules

Text before the rule.
Multiple sentences here.
They should wrap!

______________________________________________________________________

Text after the rule.
Again with sentences.
Proper wrapping continues!

## Conclusion

This comprehensive test file thoroughly validates all implemented phases from
guidance.md!
It tests abbreviation detection across multiple languages.
Whitespace collapsing is verified!
Indentation preservation works correctly.

Context detection for inline code and links is tested extensively.
Non-breaking spaces in links are handled!
The default wrap width of 80 characters is validated.
Everything integrates seamlessly:
the implementation is complete and robust!

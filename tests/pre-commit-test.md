# Test file for mdslw sentence wrapping

## Basic Sentences with Different Punctuation

This is a test paragraph with multiple sentences.
It should wrap after periods!
Does it handle question marks correctly?
Of course it does:
even colons work as sentence markers.

## Varying Sentence Lengths

Short sentence.
This is a medium-length sentence that contains more words but is still
manageable.
Now here's a really long sentence that goes on and on with multiple clauses,
subordinate phrases, and enough content to potentially exceed the default line
width of eighty characters when rendered in a typical terminal window.

## Edge Cases and Special Characters

The temperature is 98.6 degrees.
Dr.
Smith arrived at 3 p.m.
yesterday.
The file size is 2.5 MB.
These abbreviations like e.g.
and i.e.
should be handled carefully!
What about URLs like https://example.com?
They should work fine:
the plugin must handle them correctly.

## Lists with Multiple Sentences

- First list item has one sentence.
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
    Some much longer to test the line width constraints.

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

## Blockquotes and Special Blocks

> This is a blockquote with multiple sentences.
> Each one should wrap properly.
> The quote marker should be preserved on each line!
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
> >
> > > Even deeply nested quotes.
> > > They all wrap correctly.
> > > This is essential for proper formatting!

## Inline Formatting and Links

This paragraph contains **bold text that spans a sentence boundary.
It should wrap correctly!** And *italic text works the same way.
Even with multiple sentences?* Yes, it does:
the formatting is preserved.

Here's a [link that contains a complete sentence.
It should not break!](https://example.com) And here's another sentence.
Code like `const x = 1; console.log(x);` should remain intact.
Even when it contains periods!

## Mixed Content Types

Combining different elements in one paragraph like **bold**, *italic*, `code`,
and [links](https://test.com) with multiple sentences.
Does everything work together?
It absolutely should:
the plugin must handle mixed content!
Even with ~~strikethrough text that spans sentences.
This needs proper handling!~~

## Unicode and Special Characters

Testing with émojis and spécial characters works perfectly!
Even with Japanese text like これは文章です。これも文章です！ And mathematical expressions:
x² + y² = z².
Does it handle all of these?
Certainly:
Unicode support is essential!

## Long Lines and Wrapping

This extraordinarily verbose and unnecessarily elongated sentence is
specifically crafted to exceed the standard eighty-character line width
limitation that many terminal emulators and text editors use as their default
display width, thereby testing whether the plugin correctly implements its
line-wrapping functionality when the `--max-line-width` parameter is configured.
Following that monster of a sentence, here's a short one.
Then another medium-length sentence to vary the rhythm.
Finally, we end with a question:
does the mixture of sentence lengths create a good test case?

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

## HTML and Raw Content

<div>
This HTML content may or may not be processed. It depends on the implementation. But it's good to test!
</div>

Some raw HTML inline:
<span>This is inline HTML.
Should it wrap?
Maybe!</span> The behavior might vary.

## Tables (If Supported)

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| This cell has sentences.
They might wrap.
Or might not!
| Another cell here.
With multiple sentences?
Yes indeed!
| Final cell.
Short sentence.
Done!
|
| Row two continues.
More test content.
Wrapping behavior?
| Testing continues here.
Multiple sentences work.
Great!
| Last cell here.
All good!
|

## Horizontal Rules and Breaks

Text before the rule.
Multiple sentences here.
They should wrap!

______________________________________________________________________

Text after the rule.
Again with sentences.
Proper wrapping continues!

______________________________________________________________________

Another separator style.
Still wrapping sentences correctly?
Absolutely!

## Footnotes and References

This sentence has a footnote[^1].
Another sentence follows it.
Does the footnote marker interfere?
It shouldn't:
the wrapping should work correctly!

\[^1\]:
This is the footnote content.
It also has multiple sentences.
They should wrap properly too!

## Conclusion

This comprehensive test file covers numerous edge cases and scenarios.
Each section tests different aspects of the sentence wrapping functionality!
From basic punctuation to complex nested structures, everything should work
correctly.
The plugin must handle all these cases gracefully:
that's what makes it robust and reliable.

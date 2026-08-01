inline code with period
.
This is `code.py`. Another sentence!
.
This is `code.py`. Another sentence!
.

inline code with period aggressive mode
.
This is `code.py`. Another sentence!
.
This is `code.py`.
Another sentence!
.
--slw-min-line=0

inline code with multiple periods
.
Check `import sys.path`. It works!
.
Check `import sys.path`. It works!
.

inline code with multiple periods aggressive mode
.
Check `import sys.path`. It works!
.
Check `import sys.path`.
It works!
.
--slw-min-line=0

link with period in text
.
See [example.com](https://example.com). More text!
.
See [example.com](https://example.com). More text!
.

link with period in text aggressive mode
.
See [example.com](https://example.com). More text!
.
See [example.com](https://example.com).
More text!
.
--slw-min-line=0

link with period in URL (line exceeds min-line)
.
Visit [the site](https://test.example.com/page.html). Done!
.
Visit [the site](https://test.example.com/page.html).
Done!
.

link with period in URL aggressive mode
.
Visit [the site](https://test.example.com/page.html). Done!
.
Visit [the site](https://test.example.com/page.html).
Done!
.
--slw-min-line=0

reference link (under min-line, no wrap)
.
Check [this out][ref]. Another sentence!
.
Check [this out][ref]. Another sentence!
.

reference link aggressive mode
.
Check [this out][ref]. Another sentence!
.
Check [this out][ref].
Another sentence!
.
--slw-min-line=0

reference link with period in text (under min-line, no wrap)
.
Read [section 2.1][ref]. Important information!
.
Read [section 2.1][ref]. Important information!
.

reference link with period in text aggressive mode
.
Read [section 2.1][ref]. Important information!
.
Read [section 2.1][ref].
Important information!
.
--slw-min-line=0

mixed inline code and links
.
Use `config.json` and see [docs](url). Both work!
.
Use `config.json` and see [docs](url). Both work!
.

mixed inline code and links aggressive mode
.
Use `config.json` and see [docs](url). Both work!
.
Use `config.json` and see [docs](url).
Both work!
.
--slw-min-line=0

double backtick code (line exceeds min-line)
.
This is ``code with `backticks`.txt`` file. Another sentence!
.
This is `` code with `backticks`.txt `` file.
Another sentence!
.

double backtick code aggressive mode
.
This is ``code with `backticks`.txt`` file. Another sentence!
.
This is `` code with `backticks`.txt `` file.
Another sentence!
.
--slw-min-line=0

code span at end
.
First sentence. Then `code.py`!
.
First sentence. Then `code.py`!
.

code span at end aggressive mode
.
First sentence. Then `code.py`!
.
First sentence.
Then `code.py`!
.
--slw-min-line=0

nested brackets in link text
.
See [array[0]](url). More info!
.
See [array[0]](url). More info!
.

nested brackets in link text aggressive mode
.
See [array[0]](url). More info!
.
See [array[0]](url).
More info!
.
--slw-min-line=0

multiple links (line exceeds min-line)
.
Check [link1](url1). Also [link2](url2). Done!
.
Check [link1](url1). Also [link2](url2).
Done!
.

multiple links aggressive mode
.
Check [link1](url1). Also [link2](url2). Done!
.
Check [link1](url1).
Also [link2](url2).
Done!
.
--slw-min-line=0

normal period should still wrap (when exceeds min-line)
.
Regular sentence that is long enough to trigger wrapping behavior. Another one! No protection here?
.
Regular sentence that is long enough to trigger wrapping behavior.
Another one! No protection here?
.

normal period aggressive mode
.
Regular sentence. Another one! No protection here?
.
Regular sentence.
Another one!
No protection here?
.
--slw-min-line=0

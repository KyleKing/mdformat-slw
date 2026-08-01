# Multilingual Support Analysis for mdformat-slw

## Executive Summary

The current implementation of mdformat-slw has significant limitations for Arabic (RTL) and CJK languages. This document identifies specific issues and proposes concrete improvements.

## Current Implementation Analysis

### Text Wrapping Algorithm (mdformat_slw/\_sentence_wrapper.py)

**Phase 1: Sentence Breaking**

- Uses regex pattern: `([.!?])(\s*[\"'\)\]\}]*)\s+` (line 117)
- **Requires whitespace after sentence markers** to detect boundaries
- Only supports ASCII punctuation markers (default: `.!?`)
- Case-insensitive abbreviation suppression (lines 542-560)

**Phase 2: Long Line Wrapping**

- Splits on space characters only (line 256)
- Uses wcwidth for character width calculation (lines 37-52)
- No language-specific line breaking rules

**Character Width Handling**

- Properly uses `wcwidth.wcswidth()` for CJK double-width characters (line 50)
- Handles zero-width combining marks correctly
- Falls back to `len(text)` for control characters

---

## Issues Identified

### 1. Arabic/RTL Language Issues

#### 1.1 Punctuation Markers (CRITICAL)

**Current:** Only supports ASCII punctuation (`.!?`) **Problem:** Arabic uses different punctuation:

- Arabic Question Mark: `؟` (U+061F)
- Arabic Comma: `،` (U+060C)
- Arabic Semicolon: `؛` (U+061B)
- Arabic Full Stop: `٪` (U+066A) and others

**Evidence:** `tests/format/fixtures/lang_ar.md` only tests ASCII punctuation with Arabic text.

**Impact:** Arabic documents using native punctuation won't wrap at sentence boundaries.

#### 1.2 No RTL/Bidi Support

**Current:** No handling of Unicode bidirectional text **Problem:**

- No detection of RTL text direction
- No handling of bidirectional override marks (LRM, RLM, etc.)
- Mixed RTL/LTR text (e.g., Arabic with English code terms) may display incorrectly

**Impact:** Text may appear correctly in the source file but render incorrectly in some viewers.

#### 1.3 Missing Arabic Language Data

**Current:** No Arabic-specific abbreviation list in `_language_data.py` **Problem:** Common Arabic abbreviations not recognized:

- إلخ (etc.)
- د. (Dr.)
- م. (Mr.)
- ص. (p./page)

**Evidence:** Test at line 25-29 of `lang_ar.md` uses custom abbreviations flag.

---

### 2. CJK Language Issues

#### 2.1 Space Dependency (CRITICAL)

**Current:** Sentence breaking requires `\s+` (whitespace) after markers **Problem:** Natural CJK text often has NO spaces between sentences

**Evidence:**

- `tests/format/fixtures/lang_ja.md:3-5` - Japanese without spaces **doesn't wrap**
- `tests/format/fixtures/lang_ja.md:114-116` - Documented as "limitation"
- `tests/format/fixtures/lang_ko.md:114-116` - Same limitation for Korean

**Impact:** Most natural CJK writing won't wrap at all.

#### 2.2 No Kinsoku Shori (禁則処理) Support

**Current:** No line breaking rules **Problem:** CJK has specific characters that cannot start/end lines:

**Japanese Kinsoku Rules:**

- Cannot start line: `）」』】〉》、。，．・：；？！゛゜ヽヾゝゞ々` etc.
- Cannot end line: `（「『【〈《` etc.
- No breaking inside: `——…‥` (multi-character punctuation)

**Chinese Similar Rules:**

- Cannot start: `）】｝〕〉》」』〗！％），．：；？］｀｜｝～` etc.
- Cannot end: `（【｛〔〈《「『〖［｛￡￥` etc.

**Korean Rules:**

- Different rules when mixing Hangul with Hanja
- Specific handling of Korean punctuation

**Impact:** Even if wrapping works, line breaks may occur at prohibited positions.

#### 2.3 No Intelligent Word Boundary Detection

**Current:** Splits only on spaces (line 256) **Problem:** CJK text needs linguistic analysis to find optimal break points

**Example:** Chinese sentence without spaces:

```
今天天气很好我们去公园散步吧
```

Optimal break points require understanding where words/phrases end.

**Solutions exist:**

- ICU library's line break iterator
- Unicode Line Breaking Algorithm (UAX #14)
- Language-specific libraries (e.g., jieba for Chinese, TinySegmenter for Japanese)

#### 2.4 CJK Punctuation Not in Default Markers

**Current:** Default markers: `.!?` (ASCII only) **Problem:** CJK uses different punctuation:

- Japanese: `。！？` (U+3002, U+FF01, U+FF1F)
- Chinese: `。！？` (same as Japanese)
- Korean: `。！？` (also uses same)
- Also: `、` (ideographic comma), `：` (fullwidth colon)

---

## Proposed Solutions

### Priority 1: Critical Fixes

#### A. Make Space Optional After Sentence Markers

**Change:** Modify sentence boundary pattern to make whitespace optional

**Current (line 117):**

```python
pattern = r"([" + marker_class + r"])(\s*[\"'\)\]\}]*)\s+"
```

**Proposed:**

```python
pattern = r"([" + marker_class + r"])(\s*[\"'\)\]\}]*)(?:\s+|(?=[^\s]))"
```

**Impact:** Allows CJK text to wrap without requiring spaces.

**Tradeoff:** May need adjustment to avoid over-wrapping in some cases.

#### B. Add CJK Punctuation to Default Markers

**Change:** Expand `DEFAULT_SENTENCE_MARKERS` to include CJK

**Current (line 27):**

```python
DEFAULT_SENTENCE_MARKERS = ".!?"
```

**Proposed:**

```python
DEFAULT_SENTENCE_MARKERS = ".!?。！？"  # Add U+3002, U+FF01, U+FF1F
```

**Impact:** CJK text will wrap at proper sentence boundaries.

**Configuration:** Users can override via `--slw-markers` if needed.

#### C. Add Arabic Punctuation Support

**Change:** Allow configuration to include Arabic markers

**Proposed:**

```python
# Could be added to default or as preset
ARABIC_SENTENCE_MARKERS = ".!?؟"  # Include U+061F (Arabic question mark)
```

**Usage:** `--slw-markers=".!?؟،؛"` or `--slw-lang=ar` with preset

### Priority 2: Important Enhancements

#### D. Add Language-Specific Presets

**Create preset configurations:**

```python
# In _language_data.py or new _language_presets.py
LANGUAGE_PRESETS = {
    "ar": {
        "markers": ".!?؟",  # Arabic question mark
        "additional_markers": "،؛",  # Optional: comma, semicolon
    },
    "ja": {
        "markers": ".!?。！？",
        "space_required": False,  # Don't require space after markers
    },
    "zh": {
        "markers": ".!?。！？",
        "space_required": False,
    },
    "ko": {
        "markers": ".!?。！？",
        "space_required": False,
    },
}
```

**CLI Usage:** `--slw-lang=ja` would automatically configure Japanese settings.

#### E. Add Arabic Abbreviations to Language Data

**Add to `_language_data.py`:**

```python
LANG_SUPPRESSIONS = {
    # ... existing ...
    "ar": [
        "إلخ",  # etc.
        "د",  # Dr.
        "م",  # Mr.
        "ص",  # page
        "هـ",  # Hijri year marker
        # ... more common Arabic abbreviations
    ],
}
```

#### F. Implement Unicode Line Breaking Algorithm

**For long line wrapping**, integrate Unicode Line Breaking (UAX #14):

**Option 1:** Use Python `regex` module with `\X` (grapheme cluster)

```python
import regex

words = regex.split(r"(?<=\s)|(?=\s)|\b", text)
```

**Option 2:** Use ICU library (PyICU)

```python
from icu import BreakIterator, Locale


def _find_line_breaks(text: str, locale: str) -> list[int]:
    bi = BreakIterator.createLineInstance(Locale(locale))
    bi.setText(text)
    breaks = []
    pos = bi.nextBoundary()
    while pos != BreakIterator.DONE:
        breaks.append(pos)
        pos = bi.nextBoundary()
    return breaks
```

**Benefits:**

- Proper line breaking for all Unicode scripts
- No need to maintain language-specific rules
- Handles kinsoku shori automatically

**Tradeoff:** Adds dependency (PyICU is ~8MB)

### Priority 3: Advanced Features

#### G. Implement Kinsoku Rules (If Not Using ICU)

If avoiding PyICU dependency, implement basic kinsoku:

```python
# In new module: _cjk_line_breaking.py

KINSOKU_START_JA = "）」』】〉》、。，．・：；？！"
KINSOKU_END_JA = "（「『【〈《"
KINSOKU_START_ZH = "）】｝〉》」』！％），．：；？］｜～"
KINSOKU_END_ZH = "（【｛〈《「『［｛"


def _can_break_at(text: str, pos: int, lang: str) -> bool:
    if pos <= 0 or pos >= len(text):
        return False

    char_before = text[pos - 1]
    char_after = text[pos] if pos < len(text) else ""

    if lang == "ja":
        if char_before in KINSOKU_END_JA:
            return False
        if char_after in KINSOKU_START_JA:
            return False
    elif lang == "zh":
        if char_before in KINSOKU_END_ZH:
            return False
        if char_after in KINSOKU_START_ZH:
            return False

    return True
```

**Integration:** Use in `_wrap_long_line()` to validate break positions.

#### H. Add CJK Word Segmentation

**For optimal wrapping**, integrate word segmentation:

**Japanese:**

```python
# Option: TinySegmenter (pure Python, no dependencies)
from tinysegmenter import TinySegmenter

segmenter = TinySegmenter()
words = segmenter.tokenize(text)
```

**Chinese:**

```python
# Option: jieba (popular, lightweight)
import jieba

words = jieba.cut(text)
```

**Tradeoff:** Adds dependencies and processing overhead.

**Alternative:** Use grapheme clusters as minimum break units without full segmentation.

#### I. RTL/Bidi Text Support

**Add detection and handling:**

```python
import unicodedata


def _detect_text_direction(text: str) -> str:
    """Detect if text is primarily RTL or LTR."""
    rtl_count = 0
    ltr_count = 0

    for char in text:
        bidi = unicodedata.bidirectional(char)
        if bidi in ("R", "AL", "RLE", "RLO"):  # RTL types
            rtl_count += 1
        elif bidi in ("L", "LRE", "LRO"):  # LTR types
            ltr_count += 1

    return "rtl" if rtl_count > ltr_count else "ltr"


def _insert_bidi_marks_if_needed(text: str) -> str:
    """Add LRM/RLM marks for mixed-direction text if needed."""
    # Implementation would analyze and insert U+200E (LRM) or U+200F (RLM)
    pass
```

**Note:** Most markdown renderers handle bidi automatically, so this may be lower priority.

---

## Recommended Implementation Plan

### Phase 1: Quick Wins (Low Effort, High Impact)

1. Add CJK punctuation to default markers (`.!?。！？`)
1. Make space optional in sentence boundary regex
1. Add Arabic abbreviations to language data
1. Add language preset system with `--slw-lang` supporting `ar`, `ja`, `zh`, `ko`

**Estimated Effort:** 4-8 hours **Files Changed:** `_sentence_wrapper.py`, `_language_data.py`, `plugin.py`

### Phase 2: Enhanced Line Breaking (Medium Effort, High Impact)

5. Integrate PyICU for proper line breaking across all languages
5. Add basic kinsoku rules as fallback if PyICU unavailable
5. Comprehensive test coverage for all supported languages

**Estimated Effort:** 16-24 hours **Files Changed:** Add `_unicode_line_breaking.py`, update `_sentence_wrapper.py`, add tests

### Phase 3: Advanced Features (High Effort, Medium Impact)

8. Add CJK word segmentation (optional, behind feature flag)
8. Add RTL/bidi detection and handling
8. Performance optimization for large documents

**Estimated Effort:** 24-40 hours

---

## Testing Requirements

### New Test Cases Needed

1. **Arabic:**

    - Text with Arabic punctuation (؟ ، ؛)
    - Mixed RTL/LTR with code snippets
    - Arabic abbreviations

1. **Japanese:**

    - Natural text without spaces between sentences
    - Mixed hiragana/katakana/kanji
    - Test kinsoku rules (if implemented)

1. **Chinese:**

    - Simplified and Traditional Chinese
    - No spaces between sentences
    - Test kinsoku rules

1. **Korean:**

    - Hangul with no spaces
    - Mixed Hangul/Hanja

### Test File Structure

```
tests/format/fixtures/
  lang_ar_native_punct.md      # Arabic with ؟ ، ؛
  lang_ja_no_spaces.md          # Update existing to expect wrapping
  lang_zh_simplified.md         # New
  lang_zh_traditional.md        # New
  lang_ko_no_spaces.md          # Update existing
```

---

## Configuration Examples

### After Implementation

```bash
# Japanese documentation with CJK punctuation
mdformat --slw-lang=ja document.md

# Arabic documentation with native punctuation
mdformat --slw-lang=ar --slw-markers=".؟!" document.md

# Custom: Chinese with specific markers
mdformat --slw-lang=zh --slw-markers="。！？；" document.md

# Disable space requirement for CJK
mdformat --slw-no-space-required document.md
```

### TOML Configuration

```toml
[plugin.slw]
lang = "ja"
markers = "。！？"
no_space_required = true
wrap = 88
min_line = 40
```

---

## Breaking Changes Assessment

### Backward Compatibility

**Phase 1 changes are backward compatible:**

- Adding punctuation to default markers extends functionality
- Making space optional broadens applicability
- Existing English/European documents unaffected

**Phase 2+ may have minor impacts:**

- PyICU dependency (optional, with fallback)
- Line breaking positions may change slightly with better algorithms
- Can be mitigated with version bump and changelog

---

## Alternatives Considered

### 1. Use Python `regex` Module Instead of PyICU

**Pros:** Lighter dependency, supports Unicode grapheme clusters **Cons:** Still requires manual kinsoku implementation, less comprehensive

### 2. Keep CJK Space Requirement

**Pros:** No code changes **Cons:** Unusable for natural CJK text (primary issue)

### 3. Separate Plugins per Language

**Pros:** Smaller, focused codebases **Cons:** Poor user experience, maintenance burden

---

## References

- Unicode Line Breaking Algorithm: https://unicode.org/reports/tr14/
- Unicode Bidirectional Algorithm: https://unicode.org/reports/tr9/
- Japanese Kinsoku Shori: https://www.w3.org/TR/jlreq/
- PyICU Documentation: https://pypi.org/project/PyICU/
- wcwidth Library: https://pypi.org/project/wcwidth/

---

## Appendix: Current Language Support Matrix

| Language | Abbreviations  | Punctuation | Wrapping           | Line Breaking | Status   |
| -------- | -------------- | ----------- | ------------------ | ------------- | -------- |
| English  | ✅ 17          | ✅ .!?      | ✅                 | ✅            | Good     |
| German   | ✅ 54          | ✅ .!?      | ✅                 | ✅            | Good     |
| Spanish  | ✅ 36          | ✅ .!?      | ✅                 | ✅            | Good     |
| French   | ✅ 42          | ✅ .!?      | ✅                 | ✅            | Good     |
| Italian  | ✅ 40          | ✅ .!?      | ✅                 | ✅            | Good     |
| Russian  | ❌ 0           | ✅ .!?      | ✅                 | ✅            | Fair     |
| Japanese | ❌ 0           | ⚠️ .!? only | ⚠️ Spaces required | ❌ No kinsoku | **Poor** |
| Korean   | ❌ 0           | ⚠️ .!? only | ⚠️ Spaces required | ❌            | **Poor** |
| Chinese  | ❌ 0           | ⚠️ .!? only | ⚠️ Spaces required | ❌ No kinsoku | **Poor** |
| Arabic   | ⚠️ Custom only | ⚠️ .!? only | ✅                 | ❌ No RTL     | **Poor** |

**Legend:**

- ✅ Fully supported
- ⚠️ Partial support / Workarounds needed
- ❌ Not supported

---

## Conclusion

The current implementation works well for Western European languages but has critical limitations for Arabic and CJK languages. The proposed Phase 1 improvements would significantly improve multilingual support with minimal effort and no breaking changes. Phase 2 and 3 would bring mdformat-slw to production-quality support for these language families.

The most critical issue is the space requirement for CJK sentence detection, which makes the plugin essentially non-functional for natural CJK text. This should be the highest priority fix.

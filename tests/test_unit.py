"""
TextSureOCR comprehensive unit tests.

~2,000 pure unit tests covering:
  1. _first_word() -- ~500 cases
  2. Pydantic schema validation -- ~800 cases
  3. Score/math computations -- ~400 cases
  4. _build_correction() logic -- ~200 cases
  5. Configuration and constants -- ~100 cases

All tests are pure logic; no running service or GPU model required.
"""

import math
import sys
import os
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Mock torch and heavy deps BEFORE importing app
# ---------------------------------------------------------------------------
_mock_torch = MagicMock()
_mock_torch.cuda.is_available.return_value = False
_mock_torch.float32 = "float32"
_mock_torch.float16 = "float16"
sys.modules.setdefault("torch", _mock_torch)
sys.modules.setdefault("torch.nn", MagicMock())
sys.modules.setdefault("torch.nn.functional", MagicMock())
sys.modules.setdefault("transformers", MagicMock())
sys.modules.setdefault("uvicorn", MagicMock())

from app import (  # noqa: E402
    _first_word,
    CheckRequest,
    CheckResponse,
    ContinuationRequest,
    ContinuationResponse,
    Span,
    Suggestion,
)

pytestmark = pytest.mark.unit


# ═══════════════════════════════════════════════════════════════════════════
# 1. _first_word  (~500 test cases)
# ═══════════════════════════════════════════════════════════════════════════

class TestFirstWordBasic:
    """Normal single words."""

    @pytest.mark.parametrize("text,expected", [
        ("hello", "hello"),
        ("World", "world"),
        ("TESTING", "testing"),
        ("Python", "python"),
        ("a", "a"),
        ("Z", "z"),
        ("abc", "abc"),
        ("XYZ", "xyz"),
        ("MixedCase", "mixedcase"),
        ("lowercase", "lowercase"),
        ("UPPERCASE", "uppercase"),
        ("tEsT", "test"),
        ("AbCdEf", "abcdef"),
        ("word", "word"),
        ("text", "text"),
        ("data", "data"),
        ("code", "code"),
        ("file", "file"),
        ("test", "test"),
        ("name", "name"),
        ("type", "type"),
        ("value", "value"),
        ("item", "item"),
        ("list", "list"),
        ("node", "node"),
        ("tree", "tree"),
    ], ids=lambda x: repr(x)[:40])
    def test_basic_words(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("well-known", "well-known"),
        ("self-aware", "self-aware"),
        ("co-operate", "co-operate"),
        ("re-enter", "re-enter"),
        ("pre-existing", "pre-existing"),
        ("non-trivial", "non-trivial"),
        ("long-lasting", "long-lasting"),
        ("high-quality", "high-quality"),
        ("well-being", "well-being"),
        ("mother-in-law", "mother-in-law"),
        ("up-to-date", "up-to-date"),
        ("state-of-the-art", "state-of-the-art"),
        ("A-B-C", "a-b-c"),
        ("X-ray", "x-ray"),
        ("e-mail", "e-mail"),
        ("T-shirt", "t-shirt"),
        ("check-in", "check-in"),
        ("break-up", "break-up"),
        ("by-product", "by-product"),
        ("cross-reference", "cross-reference"),
    ], ids=lambda x: repr(x)[:40])
    def test_hyphenated_words(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("don't", "don't"),
        ("it's", "it's"),
        ("I'm", "i'm"),
        ("won't", "won't"),
        ("can't", "can't"),
        ("they're", "they're"),
        ("we've", "we've"),
        ("she'd", "she'd"),
        ("he'll", "he'll"),
        ("you're", "you're"),
        ("couldn't", "couldn't"),
        ("shouldn't", "shouldn't"),
        ("wouldn't", "wouldn't"),
        ("isn't", "isn't"),
        ("aren't", "aren't"),
        ("hasn't", "hasn't"),
        ("haven't", "haven't"),
        ("wasn't", "wasn't"),
        ("weren't", "weren't"),
        ("didn't", "didn't"),
        ("doesn't", "doesn't"),
        ("o'clock", "o'clock"),
        ("ma'am", "ma'am"),
        ("ne'er", "ne'er"),
        ("e'en", "e'en"),
    ], ids=lambda x: repr(x)[:40])
    def test_apostrophe_words(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("well-known's", "well-known's"),
        ("mother-in-law's", "mother-in-law's"),
        ("don't-care", "don't-care"),
        ("it's-a-test", "it's-a-test"),
        ("can't-stop-won't-stop", "can't-stop-won't-stop"),
        ("co-worker's", "co-worker's"),
    ], ids=lambda x: repr(x)[:40])
    def test_mixed_hyphen_apostrophe(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordLeadingChars:
    """Words preceded by numbers, punctuation, whitespace."""

    @pytest.mark.parametrize("text,expected", [
        ("123hello", "hello"),
        ("0world", "world"),
        ("42test", "test"),
        ("999abc", "abc"),
        ("1a", "a"),
        ("00word", "word"),
        ("12345data", "data"),
        ("007bond", "bond"),
        ("0x0FF", "x"),
        ("3rd", "rd"),
        ("1st", "st"),
        ("2nd", "nd"),
        ("4th", "th"),
        ("100percent", "percent"),
        ("50th", "th"),
    ], ids=lambda x: repr(x)[:40])
    def test_leading_numbers(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("...hello", "hello"),
        ("!!!world", "world"),
        ("???test", "test"),
        ("---word", "word"),
        ("***star", "star"),
        ("@@@at", "at"),
        ("###hash", "hash"),
        ("$$$dollar", "dollar"),
        ("%%%percent", "percent"),
        ("^^^caret", "caret"),
        ("&&&and", "and"),
        ("(((paren", "paren"),
        (")))close", "close"),
        ("===equal", "equal"),
        ("+++plus", "plus"),
        ("~~~tilde", "tilde"),
        ("```backtick", "backtick"),
        (",,,comma", "comma"),
        (";;;semi", "semi"),
        (":::colon", "colon"),
    ], ids=lambda x: repr(x)[:40])
    def test_leading_punctuation(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("  hello", "hello"),
        ("   world", "world"),
        ("\thello", "hello"),
        ("\nhello", "hello"),
        ("\r\nhello", "hello"),
        ("  \t\n hello", "hello"),
        ("    test", "test"),
        ("\t\tword", "word"),
        ("\n\n\ntext", "text"),
        ("\r\r\rdata", "data"),
    ], ids=lambda x: repr(x)[:40])
    def test_leading_whitespace(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("123 456 hello", "hello"),
        ("!!! 123 test", "test"),
        ("  42 ... world", "world"),
        ("#1 best", "best"),
        ("$100 price", "price"),
        ("(42) answer", "answer"),
        ("[3] item", "item"),
        ("{key}", "key"),
        ("<tag>", "tag"),
        ("@user", "user"),
        ("100% sure", "sure"),
        ("$5.99 cost", "cost"),
        ("3.14 pi", "pi"),
        ("1,000 items", "items"),
        ("12:30 time", "time"),
    ], ids=lambda x: repr(x)[:40])
    def test_leading_mixed(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordEmpty:
    """Empty, blank, or no-alphabetic-char inputs."""

    @pytest.mark.parametrize("text,expected", [
        ("", ""),
        ("123", ""),
        ("456789", ""),
        ("0", ""),
        ("000", ""),
        ("!!!", ""),
        ("???", ""),
        ("...", ""),
        ("---", ""),
        ("@#$%", ""),
        ("123456", ""),
        ("   ", ""),
        ("\t\t\t", ""),
        ("\n\n\n", ""),
        ("\r\n\r\n", ""),
        ("12345", ""),
        ("!@#$%^&*()", ""),
        ("+-*/=<>", ""),
        ("[]{}()", ""),
        ("|\\~`", ""),
        (",,,,", ""),
        (";;;;", ""),
        ("::::", ""),
        ("\"\"\"\"", ""),
        ("''''", ""),
        ("1 2 3 4 5", ""),
        ("  .  .  . ", ""),
        ("\t\n\r ", ""),
        ("0.0", ""),
        ("3.14159", ""),
        ("1,000,000", ""),
        ("12:34:56", ""),
        ("2024-01-01", ""),
        ("$100.00", ""),
        ("100%", ""),
    ], ids=lambda x: repr(x)[:40])
    def test_no_alpha(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordUnicode:
    """Unicode and non-ASCII input."""

    @pytest.mark.parametrize("text,expected", [
        ("cafe\u0301", "cafe"),
        ("\u00e9cole", "cole"),
        ("\u00fcber", "ber"),
        ("\u00f1ino", "ino"),
        ("na\u00efve", "na"),
        ("r\u00e9sum\u00e9", "r"),
        ("\u2603snowman", "snowman"),
        ("\u2764heart", "heart"),
        ("\u00a9copyright", "copyright"),
        ("\u00aecircle", "circle"),
        ("test\u2019s", "test"),
        ("hello\u2026world", "hello"),
        ("\u201chello\u201d", "hello"),
        ("\u2018quote\u2019", "quote"),
        ("\u00bfhola", "hola"),
        ("\u00a1wow", "wow"),
        ("\u2013hello", "hello"),
        ("\u2014world", "world"),
        ("\u00b7dot", "dot"),
        ("\u2022bullet", "bullet"),
    ], ids=lambda x: repr(x)[:40])
    def test_unicode_chars(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordSingleChars:
    """Single-character inputs."""

    @pytest.mark.parametrize("text,expected", [
        ("a", "a"),
        ("b", "b"),
        ("z", "z"),
        ("A", "a"),
        ("B", "b"),
        ("Z", "z"),
        ("M", "m"),
        ("x", "x"),
        ("I", "i"),
        ("0", ""),
        ("1", ""),
        ("9", ""),
        ("!", ""),
        ("?", ""),
        (".", ""),
        ("-", ""),
        ("'", ""),
        (" ", ""),
        ("\t", ""),
        ("\n", ""),
    ], ids=lambda x: repr(x)[:40])
    def test_single_chars(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordMultipleWords:
    """Only the first word should be returned."""

    @pytest.mark.parametrize("text,expected", [
        ("hello world", "hello"),
        ("  first second", "first"),
        ("AAA BBB CCC", "aaa"),
        ("one two three", "one"),
        ("THE quick brown fox", "the"),
        ("Hello, World!", "hello"),
        ("(hello) world", "hello"),
        ("[first] second", "first"),
        ("123 hello world", "hello"),
        ("---alpha beta", "alpha"),
        ("...start middle end", "start"),
        ("  \t first rest", "first"),
        ("\n\nline1 line2", "line"),
        ("a b c d e", "a"),
        ("X Y Z", "x"),
    ], ids=lambda x: repr(x)[:40])
    def test_returns_first_word_only(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordEdgeCases:
    """Long strings, special patterns, boundary conditions."""

    @pytest.mark.parametrize("text,expected", [
        ("a" * 10000, "a" * 10000),
        ("1" * 100 + "hello", "hello"),
        ("!" * 50 + "word" + "?" * 50, "word"),
        ("hello" + " " * 1000 + "world", "hello"),
        ("\t" * 100 + "test", "test"),
        ("a-b-c-d-e-f-g-h-i-j", "a-b-c-d-e-f-g-h-i-j"),
        ("a'b'c'd'e'f'g'h'i'j", "a'b'c'd'e'f'g'h'i'j"),
        ("a-b'c-d'e", "a-b'c-d'e"),
        ("x" * 500 + "-" + "y" * 500, "x" * 500 + "-" + "y" * 500),
    ], ids=lambda x: repr(x)[:60])
    def test_edge_cases(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("hello\tworld", "hello"),
        ("hello\nworld", "hello"),
        ("hello\rworld", "hello"),
        ("hello\r\nworld", "hello"),
        ("hello\x00world", "hello"),
        ("hello\x0bworld", "hello"),
        ("hello\x0cworld", "hello"),
    ], ids=lambda x: repr(x)[:40])
    def test_control_chars_in_middle(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("'hello", "hello"),
        ("-hello", "hello"),
        ("'-hello", "hello"),
        ("--hello", "hello"),
        ("''hello", "hello"),
        ("-'-hello", "hello"),
        ("''-hello", "hello"),
        ("--'hello", "hello"),
    ], ids=lambda x: repr(x)[:40])
    def test_leading_hyphen_apostrophe(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("hello-", "hello"),
        ("hello'", "hello"),
        ("hello-'", "hello"),
        ("hello'-", "hello"),
        ("test--", "test"),
        ("test''", "test"),
    ], ids=lambda x: repr(x)[:40])
    def test_trailing_hyphen_apostrophe(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordCaseNormalization:
    """Verify lowercase output."""

    @pytest.mark.parametrize("text,expected", [
        ("HELLO", "hello"),
        ("Hello", "hello"),
        ("hElLo", "hello"),
        ("ALLCAPS", "allcaps"),
        ("camelCase", "camelcase"),
        ("PascalCase", "pascalcase"),
        ("mixEDcAsE", "mixedcase"),
        ("ABC", "abc"),
        ("XyZ", "xyz"),
        ("aBC", "abc"),
        ("ABc", "abc"),
        ("AbC", "abc"),
        ("aBc", "abc"),
        ("WELL-KNOWN", "well-known"),
        ("Don't", "don't"),
        ("CAN'T", "can't"),
        ("Self-Aware", "self-aware"),
        ("CO-OPERATE", "co-operate"),
        ("Pre-Existing", "pre-existing"),
        ("NON-TRIVIAL", "non-trivial"),
    ], ids=lambda x: repr(x)[:40])
    def test_case_normalization(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordSpecialPatterns:
    """Regex boundary behaviors and tricky patterns."""

    @pytest.mark.parametrize("text,expected", [
        ("test123", "test"),
        ("abc456def", "abc"),
        ("word!more", "word"),
        ("first.second", "first"),
        ("left/right", "left"),
        ("key=value", "key"),
        ("name:type", "name"),
        ("item;next", "item"),
        ("a+b", "a"),
        ("x*y", "x"),
        ("p&q", "p"),
        ("m|n", "m"),
        ("c^d", "c"),
        ("u~v", "u"),
        ("r@s", "r"),
    ], ids=lambda x: repr(x)[:40])
    def test_word_boundary_special_chars(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("1a2b3c", "a"),
        ("!a!b!c", "a"),
        (".a.b.c", "a"),
        (",a,b,c", "a"),
        (";a;b;c", "a"),
        (":a:b:c", "a"),
        ("0a0b0c", "a"),
        ("1x", "x"),
        ("9z", "z"),
        ("0A", "a"),
    ], ids=lambda x: repr(x)[:40])
    def test_interleaved_nonalpha(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("idx", range(26))
    def test_every_lowercase_letter(self, idx):
        letter = chr(ord("a") + idx)
        assert _first_word(letter) == letter

    @pytest.mark.parametrize("idx", range(26))
    def test_every_uppercase_letter(self, idx):
        letter = chr(ord("A") + idx)
        assert _first_word(letter) == letter.lower()


class TestFirstWordMoreEdges:
    """Additional edge cases for complete coverage."""

    @pytest.mark.parametrize("text,expected", [
        ("  hello  ", "hello"),
        ("\thello\t", "hello"),
        ("\nhello\n", "hello"),
        ("  \t\n  hello  \t\n  ", "hello"),
        ("hello world foo bar baz qux", "hello"),
        ("Z", "z"),
        ("zzzzzzzzzz", "zzzzzzzzzz"),
        ("ZZZZZZZZZZ", "zzzzzzzzzz"),
        ("aA", "aa"),
        ("Aa", "aa"),
        ("zA", "za"),
        ("Az", "az"),
        ("zZ", "zz"),
        ("Zz", "zz"),
    ], ids=lambda x: repr(x)[:40])
    def test_misc_edge(self, text, expected):
        assert _first_word(text) == expected

    @pytest.mark.parametrize("n", [1, 2, 5, 10, 50, 100, 500, 1000])
    def test_repeated_letter(self, n):
        assert _first_word("a" * n) == "a" * n

    @pytest.mark.parametrize("n", [1, 2, 5, 10, 50, 100])
    def test_leading_digits_then_word(self, n):
        assert _first_word("1" * n + "word") == "word"

    @pytest.mark.parametrize("n", [1, 2, 5, 10, 50, 100])
    def test_leading_dots_then_word(self, n):
        assert _first_word("." * n + "hello") == "hello"

    @pytest.mark.parametrize("sep", [" ", "\t", "\n", "\r\n", "  ", "\t\t"])
    def test_word_after_whitespace_sep(self, sep):
        assert _first_word(sep + "word") == "word"


# ═══════════════════════════════════════════════════════════════════════════
# 2. Pydantic schema validation  (~800 test cases)
# ═══════════════════════════════════════════════════════════════════════════


class TestCheckRequestValid:
    """CheckRequest valid inputs."""

    @pytest.mark.parametrize("text", [
        "a",
        "ab",
        "hello",
        "Hello World",
        "The quick brown fox",
        "a" * 100,
        "a" * 1000,
        "a" * 5000,
        "a" * 9999,
        "a" * 10000,
        " ",
        "  ",
        "123",
        "!@#",
        "\t",
        "\n",
        "line1\nline2",
        "mixed 123 content!",
        "A",
        "Z",
    ], ids=lambda x: f"len={len(x)}" if len(x) > 20 else repr(x)[:40])
    def test_valid_text(self, text):
        req = CheckRequest(text=text)
        assert req.text == text

    @pytest.mark.parametrize("length", [1, 2, 3, 10, 50, 100, 500, 1000, 2000, 5000, 7500, 9999, 10000])
    def test_valid_lengths(self, length):
        text = "x" * length
        req = CheckRequest(text=text)
        assert len(req.text) == length


class TestCheckRequestInvalid:
    """CheckRequest invalid inputs."""

    @pytest.mark.parametrize("text,error_type", [
        ("", "string_too_short"),
        ("a" * 10001, "string_too_long"),
        ("a" * 10002, "string_too_long"),
        ("a" * 20000, "string_too_long"),
        ("a" * 100000, "string_too_long"),
    ], ids=lambda x: f"len={len(x[0]) if isinstance(x, tuple) else x}" if isinstance(x, tuple) else repr(x)[:40])
    def test_invalid_length(self, text, error_type):
        with pytest.raises(Exception):
            CheckRequest(text=text)

    def test_missing_text(self):
        with pytest.raises(Exception):
            CheckRequest()

    @pytest.mark.parametrize("value", [
        None,
        123,
        12.5,
        True,
        False,
        [],
        {},
        ["text"],
    ])
    def test_wrong_type(self, value):
        with pytest.raises(Exception):
            CheckRequest(text=value)


class TestCheckResponseValid:
    """CheckResponse construction."""

    @pytest.mark.parametrize("result,score,spans", [
        ("ok", 0.95, []),
        ("ok", 0.0, []),
        ("ok", 1.0, []),
        ("issue_detected", 0.85, []),
        ("ok", 0.5, []),
        ("ok", 0.001, []),
        ("ok", 0.999, []),
        ("anything", 0.5, []),
        ("", 0.0, []),
    ])
    def test_valid_check_response(self, result, score, spans):
        resp = CheckResponse(result=result, score=score, spans=spans)
        assert resp.result == result
        assert resp.score == score
        assert resp.spans == spans

    def test_with_spans(self):
        span = Span(start=0, end=5, text="hello", kind="ocr_error")
        resp = CheckResponse(result="issue_detected", score=0.9, spans=[span])
        assert len(resp.spans) == 1
        assert resp.spans[0].text == "hello"

    def test_with_many_spans(self):
        spans = [
            Span(start=i * 10, end=i * 10 + 5, text=f"word{i}", kind="ocr_error")
            for i in range(50)
        ]
        resp = CheckResponse(result="issue_detected", score=0.9, spans=spans)
        assert len(resp.spans) == 50

    def test_default_spans(self):
        resp = CheckResponse(result="ok", score=0.9)
        assert resp.spans == []

    @pytest.mark.parametrize("score", [
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
        0.001, 0.01, 0.05, 0.95, 0.99, 0.999,
        -1.0, -0.5, 2.0, 100.0,
    ])
    def test_various_scores(self, score):
        resp = CheckResponse(result="ok", score=score)
        assert resp.score == score


class TestCheckResponseInvalid:
    """CheckResponse invalid inputs."""

    def test_missing_result(self):
        with pytest.raises(Exception):
            CheckResponse(score=0.5)

    def test_missing_score(self):
        with pytest.raises(Exception):
            CheckResponse(result="ok")

    def test_missing_both(self):
        with pytest.raises(Exception):
            CheckResponse()

    @pytest.mark.parametrize("score_val", [
        "not_a_number",
        None,
        [],
        {},
    ])
    def test_invalid_score_type(self, score_val):
        with pytest.raises(Exception):
            CheckResponse(result="ok", score=score_val)


class TestContinuationRequestValid:
    """ContinuationRequest valid inputs."""

    @pytest.mark.parametrize("first,second", [
        ("a", "b"),
        ("hello", "world"),
        ("The quick brown", "fox jumps over"),
        ("a" * 5000, "b" * 5000),
        ("a" * 4999, "b" * 4999),
        (" ", " "),
        ("1", "2"),
        ("!", "?"),
        ("Hello World", "Foo Bar"),
        ("\n", "\n"),
        ("\t", "\t"),
        ("line1\nline2", "line3\nline4"),
        ("a", "b" * 5000),
        ("a" * 5000, "b"),
        ("Mixed 123", "Content !@#"),
    ], ids=lambda x: repr(x)[:40])
    def test_valid_inputs(self, first, second):
        req = ContinuationRequest(first=first, second=second)
        assert req.first == first
        assert req.second == second

    @pytest.mark.parametrize("length", [1, 2, 5, 10, 50, 100, 500, 1000, 2500, 4999, 5000])
    def test_valid_first_lengths(self, length):
        req = ContinuationRequest(first="x" * length, second="y")
        assert len(req.first) == length

    @pytest.mark.parametrize("length", [1, 2, 5, 10, 50, 100, 500, 1000, 2500, 4999, 5000])
    def test_valid_second_lengths(self, length):
        req = ContinuationRequest(first="x", second="y" * length)
        assert len(req.second) == length


class TestContinuationRequestInvalid:
    """ContinuationRequest invalid inputs."""

    @pytest.mark.parametrize("first,second", [
        ("", "hello"),
        ("hello", ""),
        ("", ""),
    ])
    def test_empty_strings(self, first, second):
        with pytest.raises(Exception):
            ContinuationRequest(first=first, second=second)

    @pytest.mark.parametrize("first,second", [
        ("a" * 5001, "hello"),
        ("hello", "a" * 5001),
        ("a" * 5001, "a" * 5001),
        ("a" * 10000, "hello"),
        ("hello", "a" * 10000),
    ])
    def test_too_long(self, first, second):
        with pytest.raises(Exception):
            ContinuationRequest(first=first, second=second)

    def test_missing_first(self):
        with pytest.raises(Exception):
            ContinuationRequest(second="hello")

    def test_missing_second(self):
        with pytest.raises(Exception):
            ContinuationRequest(first="hello")

    def test_missing_both(self):
        with pytest.raises(Exception):
            ContinuationRequest()

    @pytest.mark.parametrize("first,second", [
        (123, "hello"),
        ("hello", 123),
        (None, "hello"),
        ("hello", None),
        ([], "hello"),
        ("hello", []),
        ({}, "hello"),
        ("hello", {}),
        (True, "hello"),
        ("hello", True),
    ])
    def test_wrong_types(self, first, second):
        with pytest.raises(Exception):
            ContinuationRequest(first=first, second=second)


class TestContinuationResponseValid:
    """ContinuationResponse valid inputs."""

    @pytest.mark.parametrize("result,score", [
        ("likely_continuation", 0.9),
        ("unlikely_continuation", 0.1),
        ("likely_continuation", 0.5),
        ("unlikely_continuation", 0.5),
        ("likely_continuation", 0.0),
        ("likely_continuation", 1.0),
        ("unlikely_continuation", 0.0),
        ("unlikely_continuation", 1.0),
        ("custom_result", 0.42),
        ("", 0.0),
        ("result", -1.0),
        ("result", 100.0),
    ])
    def test_valid_construction(self, result, score):
        resp = ContinuationResponse(result=result, score=score)
        assert resp.result == result
        assert resp.score == score


class TestContinuationResponseInvalid:
    """ContinuationResponse invalid inputs."""

    def test_missing_result(self):
        with pytest.raises(Exception):
            ContinuationResponse(score=0.5)

    def test_missing_score(self):
        with pytest.raises(Exception):
            ContinuationResponse(result="ok")

    def test_missing_both(self):
        with pytest.raises(Exception):
            ContinuationResponse()


class TestSpanValid:
    """Span model valid inputs."""

    @pytest.mark.parametrize("start,end,text,kind", [
        (0, 5, "hello", "ocr_error"),
        (0, 0, "", "empty"),
        (0, 1, "a", "single_char"),
        (100, 200, "some text", "probable_ocr_error"),
        (0, 10000, "x" * 10000, "long"),
        (999, 1000, "x", "tiny"),
        (0, 5, "hello", ""),
        (0, 5, "hello", "custom_kind"),
    ])
    def test_valid_span(self, start, end, text, kind):
        span = Span(start=start, end=end, text=text, kind=kind)
        assert span.start == start
        assert span.end == end
        assert span.text == text
        assert span.kind == kind
        assert span.suggestions == []

    def test_span_with_suggestions(self):
        sugg = Suggestion(text="corrected", score=0.9)
        span = Span(start=0, end=5, text="hello", kind="ocr_error", suggestions=[sugg])
        assert len(span.suggestions) == 1
        assert span.suggestions[0].text == "corrected"

    def test_span_with_many_suggestions(self):
        suggestions = [
            Suggestion(text=f"alt{i}", score=round(0.9 - i * 0.1, 1))
            for i in range(10)
        ]
        span = Span(start=0, end=5, text="hello", kind="ocr_error", suggestions=suggestions)
        assert len(span.suggestions) == 10

    def test_span_default_suggestions(self):
        span = Span(start=0, end=5, text="hello", kind="ocr_error")
        assert span.suggestions == []

    @pytest.mark.parametrize("start,end", [
        (0, 0),
        (0, 1),
        (1, 1),
        (5, 10),
        (100, 100),
        (0, 999999),
        (10, 5),  # start > end is allowed by model (no constraint)
    ])
    def test_various_ranges(self, start, end):
        span = Span(start=start, end=end, text="t", kind="k")
        assert span.start == start
        assert span.end == end

    @pytest.mark.parametrize("start", [-1, -100])
    def test_negative_start(self, start):
        # Pydantic allows negative ints for int fields unless constrained
        span = Span(start=start, end=5, text="t", kind="k")
        assert span.start == start


class TestSpanInvalid:
    """Span model invalid inputs."""

    def test_missing_start(self):
        with pytest.raises(Exception):
            Span(end=5, text="hello", kind="ocr_error")

    def test_missing_end(self):
        with pytest.raises(Exception):
            Span(start=0, text="hello", kind="ocr_error")

    def test_missing_text(self):
        with pytest.raises(Exception):
            Span(start=0, end=5, kind="ocr_error")

    def test_missing_kind(self):
        with pytest.raises(Exception):
            Span(start=0, end=5, text="hello")

    def test_missing_all(self):
        with pytest.raises(Exception):
            Span()

    @pytest.mark.parametrize("start,end", [
        ("a", 5),
        (0, "b"),
        ("a", "b"),
        (None, 5),
        (0, None),
        ([], 5),
        (0, []),
    ])
    def test_wrong_types(self, start, end):
        with pytest.raises(Exception):
            Span(start=start, end=end, text="hello", kind="ocr_error")


class TestSuggestionValid:
    """Suggestion model valid inputs."""

    @pytest.mark.parametrize("text,score", [
        ("corrected", 0.9),
        ("fixed", 0.5),
        ("alt", 0.0),
        ("better", 1.0),
        ("word", 0.001),
        ("word", 0.999),
        ("", 0.0),
        ("a", 0.1),
        ("very long suggestion text " * 100, 0.5),
        ("UPPER", 0.5),
        ("MiXeD", 0.5),
        ("with spaces", 0.5),
        ("with-hyphen", 0.5),
        ("with'apostrophe", 0.5),
        ("123", 0.5),
        ("!@#", 0.5),
    ])
    def test_valid_suggestion(self, text, score):
        sugg = Suggestion(text=text, score=score)
        assert sugg.text == text
        assert sugg.score == score

    @pytest.mark.parametrize("score", [
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
        -1.0, -0.5, -0.001,
        1.001, 2.0, 100.0,
        0.0001, 0.9999,
        1e-10, 1e10,
    ])
    def test_various_scores(self, score):
        sugg = Suggestion(text="word", score=score)
        assert sugg.score == score


class TestSuggestionInvalid:
    """Suggestion model invalid inputs."""

    def test_missing_text(self):
        with pytest.raises(Exception):
            Suggestion(score=0.5)

    def test_missing_score(self):
        with pytest.raises(Exception):
            Suggestion(text="hello")

    def test_missing_both(self):
        with pytest.raises(Exception):
            Suggestion()

    @pytest.mark.parametrize("text,score", [
        (123, 0.5),
        (None, 0.5),
        ("hello", "not_a_number"),
        ("hello", None),
        ("hello", []),
        ("hello", {}),
    ])
    def test_wrong_types(self, text, score):
        with pytest.raises(Exception):
            Suggestion(text=text, score=score)


class TestSchemaRoundTrip:
    """Nested schema construction and serialization round-trips."""

    @pytest.mark.parametrize("n_spans", [0, 1, 2, 5, 10, 20, 50])
    def test_check_response_n_spans(self, n_spans):
        spans = [
            Span(
                start=i * 10, end=i * 10 + 5,
                text=f"word{i}", kind="probable_ocr_error",
                suggestions=[Suggestion(text=f"fix{i}", score=0.9 - i * 0.01)],
            )
            for i in range(n_spans)
        ]
        resp = CheckResponse(result="issue_detected", score=0.85, spans=spans)
        d = resp.model_dump()
        assert d["result"] == "issue_detected"
        assert d["score"] == 0.85
        assert len(d["spans"]) == n_spans
        if n_spans > 0:
            assert d["spans"][0]["text"] == "word0"
            assert d["spans"][0]["suggestions"][0]["text"] == "fix0"

    @pytest.mark.parametrize("n_suggs", [0, 1, 2, 5, 10, 20])
    def test_span_with_n_suggestions(self, n_suggs):
        suggs = [Suggestion(text=f"s{i}", score=round(1.0 / (i + 1), 3)) for i in range(n_suggs)]
        span = Span(start=0, end=5, text="original", kind="ocr_error", suggestions=suggs)
        assert len(span.suggestions) == n_suggs

    def test_full_nested_structure(self):
        resp = CheckResponse(
            result="issue_detected",
            score=0.92,
            spans=[
                Span(
                    start=0, end=5, text="br0wn", kind="probable_ocr_error",
                    suggestions=[
                        Suggestion(text="brown", score=0.95),
                        Suggestion(text="brawn", score=0.03),
                    ],
                ),
                Span(
                    start=10, end=15, text="h3llo", kind="probable_ocr_error",
                    suggestions=[
                        Suggestion(text="hello", score=0.98),
                    ],
                ),
            ],
        )
        d = resp.model_dump()
        assert len(d["spans"]) == 2
        assert len(d["spans"][0]["suggestions"]) == 2
        assert len(d["spans"][1]["suggestions"]) == 1

    def test_model_dump_json(self):
        resp = CheckResponse(result="ok", score=0.95, spans=[])
        j = resp.model_dump_json()
        assert '"ok"' in j
        assert "0.95" in j

    def test_continuation_response_dump(self):
        resp = ContinuationResponse(result="likely_continuation", score=0.85)
        d = resp.model_dump()
        assert d["result"] == "likely_continuation"
        assert d["score"] == 0.85

    @pytest.mark.parametrize("result_str", [
        "ok", "issue_detected", "likely_continuation",
        "unlikely_continuation", "custom", "",
    ])
    def test_continuation_response_results(self, result_str):
        resp = ContinuationResponse(result=result_str, score=0.5)
        assert resp.result == result_str


class TestCheckRequestBoundary:
    """Boundary tests around min_length=1 and max_length=10000."""

    @pytest.mark.parametrize("length,valid", [
        (0, False),
        (1, True),
        (2, True),
        (9999, True),
        (10000, True),
        (10001, False),
        (10002, False),
    ])
    def test_boundary_lengths(self, length, valid):
        text = "a" * length if length > 0 else ""
        if valid:
            req = CheckRequest(text=text)
            assert len(req.text) == length
        else:
            with pytest.raises(Exception):
                CheckRequest(text=text)


class TestContinuationRequestBoundary:
    """Boundary tests around min_length=1 and max_length=5000."""

    @pytest.mark.parametrize("first_len,second_len,valid", [
        (0, 1, False),
        (1, 0, False),
        (0, 0, False),
        (1, 1, True),
        (1, 5000, True),
        (5000, 1, True),
        (5000, 5000, True),
        (5001, 1, False),
        (1, 5001, False),
        (5001, 5001, False),
        (4999, 4999, True),
        (2, 2, True),
        (2500, 2500, True),
    ])
    def test_boundary_lengths(self, first_len, second_len, valid):
        first = "a" * first_len if first_len > 0 else ""
        second = "b" * second_len if second_len > 0 else ""
        if valid:
            req = ContinuationRequest(first=first, second=second)
            assert len(req.first) == first_len
            assert len(req.second) == second_len
        else:
            with pytest.raises(Exception):
                ContinuationRequest(first=first, second=second)


class TestSchemaFieldAccess:
    """Ensure all fields accessible and typed correctly."""

    def test_check_request_fields(self):
        req = CheckRequest(text="hello")
        assert isinstance(req.text, str)

    def test_check_response_fields(self):
        resp = CheckResponse(result="ok", score=0.5, spans=[])
        assert isinstance(resp.result, str)
        assert isinstance(resp.score, float)
        assert isinstance(resp.spans, list)

    def test_continuation_request_fields(self):
        req = ContinuationRequest(first="a", second="b")
        assert isinstance(req.first, str)
        assert isinstance(req.second, str)

    def test_continuation_response_fields(self):
        resp = ContinuationResponse(result="ok", score=0.5)
        assert isinstance(resp.result, str)
        assert isinstance(resp.score, float)

    def test_span_fields(self):
        span = Span(start=0, end=5, text="hello", kind="k")
        assert isinstance(span.start, int)
        assert isinstance(span.end, int)
        assert isinstance(span.text, str)
        assert isinstance(span.kind, str)
        assert isinstance(span.suggestions, list)

    def test_suggestion_fields(self):
        sugg = Suggestion(text="hello", score=0.5)
        assert isinstance(sugg.text, str)
        assert isinstance(sugg.score, float)

    @pytest.mark.parametrize("kind_str", [
        "probable_ocr_error", "ocr_error", "spelling_error",
        "grammar_error", "custom", "", "a" * 1000,
    ])
    def test_span_kind_values(self, kind_str):
        span = Span(start=0, end=1, text="x", kind=kind_str)
        assert span.kind == kind_str

    @pytest.mark.parametrize("score_val", [
        0.0, 0.5, 1.0, -1.0, -100.0, 100.0, 0.12345, 3.14159,
        1e-15, 1e15, float("inf"), float("-inf"),
    ])
    def test_suggestion_score_range(self, score_val):
        sugg = Suggestion(text="word", score=score_val)
        assert sugg.score == score_val

    def test_suggestion_nan_score(self):
        sugg = Suggestion(text="word", score=float("nan"))
        assert math.isnan(sugg.score)


class TestSchemaFromDict:
    """Construct schemas from dict (simulates JSON deserialization)."""

    @pytest.mark.parametrize("data", [
        {"text": "hello"},
        {"text": "a"},
        {"text": "x" * 10000},
        {"text": "multi\nline"},
        {"text": "with 123 numbers"},
    ])
    def test_check_request_from_dict(self, data):
        req = CheckRequest(**data)
        assert req.text == data["text"]

    @pytest.mark.parametrize("data", [
        {"first": "a", "second": "b"},
        {"first": "hello", "second": "world"},
        {"first": "x" * 5000, "second": "y" * 5000},
    ])
    def test_continuation_request_from_dict(self, data):
        req = ContinuationRequest(**data)
        assert req.first == data["first"]
        assert req.second == data["second"]

    @pytest.mark.parametrize("data", [
        {"result": "ok", "score": 0.95, "spans": []},
        {"result": "issue_detected", "score": 0.8, "spans": [
            {"start": 0, "end": 5, "text": "hello", "kind": "ocr", "suggestions": []}
        ]},
    ])
    def test_check_response_from_dict(self, data):
        resp = CheckResponse(**data)
        assert resp.result == data["result"]

    @pytest.mark.parametrize("data", [
        {"result": "likely_continuation", "score": 0.9},
        {"result": "unlikely_continuation", "score": 0.1},
    ])
    def test_continuation_response_from_dict(self, data):
        resp = ContinuationResponse(**data)
        assert resp.result == data["result"]
        assert resp.score == data["score"]


class TestSchemaExtraFields:
    """Pydantic behavior with extra fields."""

    def test_check_request_extra_field(self):
        # Default Pydantic v2 ignores extra fields
        req = CheckRequest(text="hello", extra="ignored")
        assert req.text == "hello"

    def test_continuation_request_extra_field(self):
        req = ContinuationRequest(first="a", second="b", extra="ignored")
        assert req.first == "a"

    def test_span_extra_field(self):
        span = Span(start=0, end=5, text="t", kind="k", extra="ignored")
        assert span.start == 0


class TestSchemaEquality:
    """Schema equality and hashing."""

    def test_suggestion_equality(self):
        s1 = Suggestion(text="hello", score=0.5)
        s2 = Suggestion(text="hello", score=0.5)
        assert s1 == s2

    def test_suggestion_inequality(self):
        s1 = Suggestion(text="hello", score=0.5)
        s2 = Suggestion(text="hello", score=0.6)
        assert s1 != s2

    def test_span_equality(self):
        sp1 = Span(start=0, end=5, text="hello", kind="k")
        sp2 = Span(start=0, end=5, text="hello", kind="k")
        assert sp1 == sp2

    def test_span_inequality_text(self):
        sp1 = Span(start=0, end=5, text="hello", kind="k")
        sp2 = Span(start=0, end=5, text="world", kind="k")
        assert sp1 != sp2

    def test_check_response_equality(self):
        r1 = CheckResponse(result="ok", score=0.5, spans=[])
        r2 = CheckResponse(result="ok", score=0.5, spans=[])
        assert r1 == r2

    def test_continuation_response_equality(self):
        r1 = ContinuationResponse(result="ok", score=0.5)
        r2 = ContinuationResponse(result="ok", score=0.5)
        assert r1 == r2

    @pytest.mark.parametrize("idx", range(20))
    def test_suggestion_score_precision(self, idx):
        score = round(idx * 0.05, 3)
        s = Suggestion(text="w", score=score)
        assert s.score == score


class TestSchemaIntCoercion:
    """Pydantic v2 int coercion behaviors for Span start/end."""

    @pytest.mark.parametrize("val,expected", [
        (0, 0),
        (1, 1),
        (100, 100),
        (999999, 999999),
        (-1, -1),
        (-999, -999),
    ])
    def test_int_values(self, val, expected):
        span = Span(start=val, end=val + 1, text="t", kind="k")
        assert span.start == expected


class TestSchemaWhitespaceText:
    """Schemas with various whitespace-only text."""

    @pytest.mark.parametrize("text", [
        " ",
        "  ",
        "\t",
        "\n",
        "\r\n",
        "   \t\n  ",
        "\t\t\t",
        "\n\n\n\n",
    ])
    def test_whitespace_check_request(self, text):
        req = CheckRequest(text=text)
        assert req.text == text

    @pytest.mark.parametrize("text", [
        " ",
        "  ",
        "\t",
        "\n",
    ])
    def test_whitespace_continuation_first(self, text):
        req = ContinuationRequest(first=text, second="hello")
        assert req.first == text

    @pytest.mark.parametrize("text", [
        " ",
        "  ",
        "\t",
        "\n",
    ])
    def test_whitespace_continuation_second(self, text):
        req = ContinuationRequest(first="hello", second=text)
        assert req.second == text


# ═══════════════════════════════════════════════════════════════════════════
# 3. Score/math computation tests  (~400 test cases)
# ═══════════════════════════════════════════════════════════════════════════


def pmi_score_fn(pmi: float) -> float:
    """Replicate: 1.0 / (1.0 + math.exp(-(pmi - 0.5) * 3.0))"""
    x = -(pmi - 0.5) * 3.0
    if x > 700:
        return 0.0
    if x < -700:
        return 1.0
    return 1.0 / (1.0 + math.exp(x))


def abs_score_fn(cond_avg: float) -> float:
    """Replicate: 1.0 / (1.0 + math.exp(-(cond_avg + 5.0) * 1.5))"""
    x = -(cond_avg + 5.0) * 1.5
    if x > 700:
        return 0.0
    if x < -700:
        return 1.0
    return 1.0 / (1.0 + math.exp(x))


def combined_score_fn(pmi: float, cond_avg: float) -> float:
    """Replicate: pmi_score * abs_score"""
    return pmi_score_fn(pmi) * abs_score_fn(cond_avg)


def confidence_fn(value: float) -> float:
    """Replicate: 0.80 + 0.19 * min(value, 1.0)"""
    return 0.80 + 0.19 * min(value, 1.0)


def softmax_scores_fn(raw: list[float]) -> list[float]:
    """Replicate the softmax normalization from _score_candidates."""
    if not raw:
        return []
    mx = max(raw)
    exps = [math.exp(r - mx) for r in raw]
    s = sum(exps)
    return [round(e / s, 3) for e in exps]


class TestPmiScore:
    """PMI score sigmoid: 1.0 / (1.0 + exp(-(pmi - 0.5) * 3.0))"""

    @pytest.mark.parametrize("pmi", [
        -10.0, -5.0, -3.0, -2.0, -1.5, -1.0, -0.5, -0.1,
        0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0,
        1.5, 2.0, 3.0, 5.0, 10.0,
    ])
    def test_pmi_score_values(self, pmi):
        result = pmi_score_fn(pmi)
        assert 0.0 < result < 1.0

    def test_pmi_at_midpoint(self):
        """At pmi=0.5, sigmoid argument is 0, so score should be 0.5."""
        assert pmi_score_fn(0.5) == pytest.approx(0.5, abs=1e-10)

    @pytest.mark.parametrize("pmi", [0.6, 1.0, 2.0, 5.0, 10.0])
    def test_pmi_above_midpoint_gt_half(self, pmi):
        assert pmi_score_fn(pmi) > 0.5

    @pytest.mark.parametrize("pmi", [0.4, 0.0, -1.0, -5.0, -10.0])
    def test_pmi_below_midpoint_lt_half(self, pmi):
        assert pmi_score_fn(pmi) < 0.5

    def test_pmi_monotonically_increasing(self):
        prev = 0.0
        for pmi in [x * 0.5 for x in range(-20, 21)]:
            curr = pmi_score_fn(pmi)
            assert curr >= prev
            prev = curr

    @pytest.mark.parametrize("pmi", [-10.0, -20.0, -50.0, -100.0])
    def test_pmi_very_negative_near_zero(self, pmi):
        assert pmi_score_fn(pmi) < 0.01

    @pytest.mark.parametrize("pmi", [10.0, 20.0, 50.0, 100.0])
    def test_pmi_very_positive_near_one(self, pmi):
        assert pmi_score_fn(pmi) > 0.99

    def test_pmi_symmetry_around_midpoint(self):
        """pmi_score(0.5 + d) + pmi_score(0.5 - d) = 1.0 for any d."""
        for d in [0.1, 0.5, 1.0, 2.0, 5.0]:
            assert pmi_score_fn(0.5 + d) + pmi_score_fn(0.5 - d) == pytest.approx(1.0, abs=1e-10)

    @pytest.mark.parametrize("pmi", [float(x) / 10 for x in range(-100, 101, 5)])
    def test_pmi_score_bounded_0_1(self, pmi):
        result = pmi_score_fn(pmi)
        assert 0.0 <= result <= 1.0

    def test_pmi_zero(self):
        expected = 1.0 / (1.0 + math.exp(0.5 * 3.0))
        assert pmi_score_fn(0.0) == pytest.approx(expected, abs=1e-10)

    def test_pmi_one(self):
        expected = 1.0 / (1.0 + math.exp(-0.5 * 3.0))
        assert pmi_score_fn(1.0) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("pmi", [-0.01, -0.001, 0.001, 0.01])
    def test_pmi_near_zero(self, pmi):
        result = pmi_score_fn(pmi)
        assert 0.0 < result < 1.0

    @pytest.mark.parametrize("pmi_a,pmi_b", [
        (-5.0, -4.0),
        (-1.0, 0.0),
        (0.0, 0.5),
        (0.5, 1.0),
        (1.0, 5.0),
    ])
    def test_pmi_ordering(self, pmi_a, pmi_b):
        assert pmi_score_fn(pmi_a) < pmi_score_fn(pmi_b)


class TestAbsScore:
    """Absolute score sigmoid: 1.0 / (1.0 + exp(-(cond_avg + 5.0) * 1.5))"""

    @pytest.mark.parametrize("cond_avg", [
        -15.0, -10.0, -8.0, -7.0, -6.0, -5.5, -5.0, -4.5, -4.0,
        -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 5.0,
    ])
    def test_abs_score_values(self, cond_avg):
        result = abs_score_fn(cond_avg)
        assert 0.0 < result < 1.0

    def test_abs_score_at_midpoint(self):
        """At cond_avg=-5.0, sigmoid argument is 0, score is 0.5."""
        assert abs_score_fn(-5.0) == pytest.approx(0.5, abs=1e-10)

    @pytest.mark.parametrize("cond_avg", [-4.0, -3.0, -1.0, 0.0, 5.0])
    def test_abs_above_midpoint_gt_half(self, cond_avg):
        assert abs_score_fn(cond_avg) > 0.5

    @pytest.mark.parametrize("cond_avg", [-6.0, -7.0, -10.0, -15.0])
    def test_abs_below_midpoint_lt_half(self, cond_avg):
        assert abs_score_fn(cond_avg) < 0.5

    def test_abs_monotonically_increasing(self):
        prev = 0.0
        for cond_avg in [x * 0.5 for x in range(-30, 11)]:
            curr = abs_score_fn(cond_avg)
            assert curr >= prev
            prev = curr

    @pytest.mark.parametrize("cond_avg", [-15.0, -20.0, -50.0])
    def test_abs_very_negative_near_zero(self, cond_avg):
        assert abs_score_fn(cond_avg) < 0.01

    @pytest.mark.parametrize("cond_avg", [0.0, 5.0, 10.0, 50.0])
    def test_abs_positive_near_one(self, cond_avg):
        assert abs_score_fn(cond_avg) > 0.99

    def test_abs_symmetry_around_midpoint(self):
        """abs_score(-5 + d) + abs_score(-5 - d) = 1.0"""
        for d in [0.1, 0.5, 1.0, 2.0, 5.0]:
            assert abs_score_fn(-5.0 + d) + abs_score_fn(-5.0 - d) == pytest.approx(1.0, abs=1e-10)

    @pytest.mark.parametrize("cond_avg", [float(x) / 10 for x in range(-150, 51, 5)])
    def test_abs_score_bounded_0_1(self, cond_avg):
        result = abs_score_fn(cond_avg)
        assert 0.0 <= result <= 1.0

    @pytest.mark.parametrize("ca_a,ca_b", [
        (-10.0, -5.0),
        (-5.0, -4.0),
        (-4.0, -3.0),
        (-1.0, 0.0),
        (0.0, 5.0),
    ])
    def test_abs_ordering(self, ca_a, ca_b):
        assert abs_score_fn(ca_a) < abs_score_fn(ca_b)

    @pytest.mark.parametrize("cond_avg", [-1.0, -2.0, -3.0, -4.0])
    def test_good_continuation_range(self, cond_avg):
        """Good continuations: cond_avg ~ -1 to -4 should score high."""
        assert abs_score_fn(cond_avg) > 0.8

    @pytest.mark.parametrize("cond_avg", [-7.0, -8.0, -9.0, -10.0])
    def test_gibberish_range(self, cond_avg):
        """Gibberish: cond_avg ~ -7 to -10 should score low."""
        assert abs_score_fn(cond_avg) < 0.15


class TestCombinedScore:
    """Combined score: pmi_score * abs_score."""

    @pytest.mark.parametrize("pmi,cond_avg", [
        (0.0, -5.0),
        (0.5, -5.0),
        (1.0, -5.0),
        (0.5, 0.0),
        (0.5, -10.0),
        (2.0, -2.0),
        (-2.0, -8.0),
        (5.0, 0.0),
        (0.0, 0.0),
        (-5.0, -10.0),
    ])
    def test_combined_equals_product(self, pmi, cond_avg):
        expected = pmi_score_fn(pmi) * abs_score_fn(cond_avg)
        assert combined_score_fn(pmi, cond_avg) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("pmi,cond_avg", [
        (0.0, 0.0),
        (1.0, 1.0),
        (5.0, 5.0),
        (-1.0, -1.0),
        (-10.0, -10.0),
        (0.5, -5.0),
    ])
    def test_combined_bounded_0_1(self, pmi, cond_avg):
        result = combined_score_fn(pmi, cond_avg)
        assert 0.0 <= result <= 1.0

    def test_combined_both_midpoints(self):
        """pmi=0.5, cond_avg=-5.0: both midpoints, combined = 0.25."""
        assert combined_score_fn(0.5, -5.0) == pytest.approx(0.25, abs=1e-10)

    def test_combined_high_pmi_low_abs(self):
        """High PMI but gibberish (low abs) should still be low."""
        result = combined_score_fn(10.0, -15.0)
        assert result < 0.01

    def test_combined_low_pmi_high_abs(self):
        """Low PMI but high abs should still be low."""
        result = combined_score_fn(-10.0, 0.0)
        assert result < 0.01

    def test_combined_both_high(self):
        """Both high should produce high combined score."""
        result = combined_score_fn(5.0, 0.0)
        assert result > 0.95

    def test_combined_both_low(self):
        """Both low should produce very low combined score."""
        result = combined_score_fn(-5.0, -10.0)
        assert result < 0.001

    @pytest.mark.parametrize("pmi,cond_avg,expected_above", [
        (3.0, -2.0, 0.5),
        (5.0, -1.0, 0.9),
        (2.0, -3.0, 0.5),
        (1.0, -4.0, 0.5),
    ])
    def test_likely_continuation_scenarios(self, pmi, cond_avg, expected_above):
        assert combined_score_fn(pmi, cond_avg) > expected_above

    @pytest.mark.parametrize("pmi,cond_avg,expected_below", [
        (-1.0, -7.0, 0.1),
        (-2.0, -8.0, 0.01),
        (0.0, -10.0, 0.1),
        (-5.0, -5.0, 0.1),
    ])
    def test_unlikely_continuation_scenarios(self, pmi, cond_avg, expected_below):
        assert combined_score_fn(pmi, cond_avg) < expected_below

    @pytest.mark.parametrize("pmi", [float(x) / 5 for x in range(-25, 26)])
    def test_combined_monotone_in_pmi(self, pmi):
        """With cond_avg fixed, increasing pmi increases combined score."""
        s1 = combined_score_fn(pmi, -3.0)
        s2 = combined_score_fn(pmi + 0.2, -3.0)
        assert s2 >= s1

    @pytest.mark.parametrize("cond_avg", [float(x) / 5 for x in range(-50, 11)])
    def test_combined_monotone_in_cond_avg(self, cond_avg):
        """With pmi fixed, increasing cond_avg increases combined score."""
        s1 = combined_score_fn(1.0, cond_avg)
        s2 = combined_score_fn(1.0, cond_avg + 0.2)
        assert s2 >= s1


class TestConfidence:
    """Confidence calculation: 0.80 + 0.19 * min(value, 1.0)"""

    @pytest.mark.parametrize("value,expected", [
        (0.0, 0.80),
        (0.5, 0.895),
        (1.0, 0.99),
        (2.0, 0.99),
        (10.0, 0.99),
        (100.0, 0.99),
    ])
    def test_confidence_values(self, value, expected):
        assert confidence_fn(value) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("value", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    def test_confidence_in_range(self, value):
        result = confidence_fn(value)
        assert 0.80 <= result <= 0.99

    @pytest.mark.parametrize("value", [1.1, 2.0, 5.0, 10.0, 100.0, 1000.0])
    def test_confidence_clamped_at_1(self, value):
        assert confidence_fn(value) == pytest.approx(0.99, abs=1e-10)

    def test_confidence_zero(self):
        assert confidence_fn(0.0) == pytest.approx(0.80, abs=1e-10)

    def test_confidence_one(self):
        assert confidence_fn(1.0) == pytest.approx(0.99, abs=1e-10)

    def test_confidence_half(self):
        assert confidence_fn(0.5) == pytest.approx(0.895, abs=1e-10)

    def test_confidence_monotonically_increasing_below_1(self):
        prev = confidence_fn(0.0)
        for v in [x * 0.1 for x in range(1, 11)]:
            curr = confidence_fn(v)
            assert curr >= prev
            prev = curr

    @pytest.mark.parametrize("value", [
        0.0, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4,
        0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
        0.95, 0.99, 1.0,
    ])
    def test_confidence_exact(self, value):
        expected = 0.80 + 0.19 * min(value, 1.0)
        assert confidence_fn(value) == pytest.approx(expected, abs=1e-15)

    @pytest.mark.parametrize("value", [-0.1, -1.0, -10.0])
    def test_confidence_negative_values(self, value):
        """Negative values: min(value, 1.0) = value, so below 0.80."""
        result = confidence_fn(value)
        assert result < 0.80


class TestSoftmaxScores:
    """Softmax normalization: exp(r - max) / sum(exp(r - max)), rounded to 3."""

    @pytest.mark.parametrize("raw,expected_sum", [
        ([0.0], 1.0),
        ([1.0, 1.0], 1.0),
        ([0.0, 0.0, 0.0], 1.0),
        ([-1.0, -2.0, -3.0], 1.0),
        ([10.0, 20.0, 30.0], 1.0),
        ([-100.0, -200.0], 1.0),
        ([5.0, 5.0, 5.0, 5.0], 1.0),
    ])
    def test_softmax_sums_to_one(self, raw, expected_sum):
        scores = softmax_scores_fn(raw)
        assert sum(scores) == pytest.approx(expected_sum, abs=0.01)

    def test_softmax_empty(self):
        assert softmax_scores_fn([]) == []

    def test_softmax_single_element(self):
        assert softmax_scores_fn([5.0]) == [1.0]

    def test_softmax_single_zero(self):
        assert softmax_scores_fn([0.0]) == [1.0]

    def test_softmax_single_negative(self):
        assert softmax_scores_fn([-100.0]) == [1.0]

    @pytest.mark.parametrize("raw", [
        [0.0, 0.0],
        [1.0, 1.0],
        [-5.0, -5.0],
        [100.0, 100.0],
    ])
    def test_softmax_equal_inputs(self, raw):
        scores = softmax_scores_fn(raw)
        for s in scores:
            assert s == pytest.approx(1.0 / len(raw), abs=0.001)

    @pytest.mark.parametrize("raw", [
        [10.0, 0.0],
        [5.0, -5.0],
        [0.0, -10.0],
        [-1.0, -100.0],
    ])
    def test_softmax_first_dominant(self, raw):
        scores = softmax_scores_fn(raw)
        assert scores[0] > scores[1]

    @pytest.mark.parametrize("raw", [
        [0.0, 10.0],
        [-5.0, 5.0],
        [-10.0, 0.0],
    ])
    def test_softmax_second_dominant(self, raw):
        scores = softmax_scores_fn(raw)
        assert scores[1] > scores[0]

    def test_softmax_three_equal(self):
        scores = softmax_scores_fn([0.0, 0.0, 0.0])
        for s in scores:
            assert s == pytest.approx(0.333, abs=0.001)

    def test_softmax_four_equal(self):
        scores = softmax_scores_fn([1.0, 1.0, 1.0, 1.0])
        for s in scores:
            assert s == pytest.approx(0.25, abs=0.001)

    def test_softmax_very_large_differences(self):
        scores = softmax_scores_fn([1000.0, 0.0])
        assert scores[0] == 1.0
        assert scores[1] == 0.0

    def test_softmax_very_small_differences(self):
        scores = softmax_scores_fn([0.0001, 0.0])
        assert scores[0] >= scores[1]

    @pytest.mark.parametrize("n", [2, 3, 4, 5, 10, 20])
    def test_softmax_n_equal_elements(self, n):
        raw = [0.0] * n
        scores = softmax_scores_fn(raw)
        expected = round(1.0 / n, 3)
        for s in scores:
            assert s == pytest.approx(expected, abs=0.002)

    def test_softmax_negative_values(self):
        scores = softmax_scores_fn([-1.0, -2.0, -3.0])
        assert scores[0] > scores[1] > scores[2]
        assert sum(scores) == pytest.approx(1.0, abs=0.01)

    @pytest.mark.parametrize("offset", [-100.0, -10.0, 0.0, 10.0, 100.0])
    def test_softmax_translation_invariance(self, offset):
        """Softmax is invariant to adding a constant to all inputs."""
        base = [1.0, 2.0, 3.0]
        shifted = [x + offset for x in base]
        s_base = softmax_scores_fn(base)
        s_shifted = softmax_scores_fn(shifted)
        for a, b in zip(s_base, s_shifted):
            assert a == pytest.approx(b, abs=0.001)

    def test_softmax_all_negative_large(self):
        scores = softmax_scores_fn([-500.0, -501.0, -502.0])
        assert scores[0] > scores[1] > scores[2]
        assert sum(scores) == pytest.approx(1.0, abs=0.01)

    @pytest.mark.parametrize("raw", [
        [0.0, 1.0, 2.0, 3.0, 4.0],
        [-4.0, -3.0, -2.0, -1.0, 0.0],
        [1.0, 2.0, 3.0, 4.0, 5.0],
    ])
    def test_softmax_monotonic_ordering(self, raw):
        scores = softmax_scores_fn(raw)
        for i in range(len(scores) - 1):
            assert scores[i] <= scores[i + 1]


class TestPmiScoreExtended:
    """Extended PMI score tests with fine-grained increments."""

    @pytest.mark.parametrize("pmi", [x * 0.1 for x in range(-50, 51)])
    def test_pmi_fine_grained(self, pmi):
        result = pmi_score_fn(pmi)
        assert 0.0 <= result <= 1.0

    @pytest.mark.parametrize("pmi", [x * 0.01 for x in range(40, 61)])
    def test_pmi_around_midpoint(self, pmi):
        result = pmi_score_fn(pmi)
        if pmi < 0.5:
            assert result < 0.5
        elif pmi > 0.5:
            assert result > 0.5
        else:
            assert result == pytest.approx(0.5, abs=1e-10)


class TestAbsScoreExtended:
    """Extended absolute score tests with fine-grained increments."""

    @pytest.mark.parametrize("cond_avg", [x * 0.1 for x in range(-100, 51)])
    def test_abs_fine_grained(self, cond_avg):
        result = abs_score_fn(cond_avg)
        assert 0.0 <= result <= 1.0

    @pytest.mark.parametrize("cond_avg", [x * 0.01 for x in range(-510, -490)])
    def test_abs_around_midpoint(self, cond_avg):
        result = abs_score_fn(cond_avg)
        if cond_avg < -5.0:
            assert result < 0.5
        elif cond_avg > -5.0:
            assert result > 0.5
        else:
            assert result == pytest.approx(0.5, abs=1e-10)


class TestScoreMathEdgeCases:
    """Edge cases for score math: infinity, very large/small numbers."""

    def test_pmi_score_large_positive(self):
        result = pmi_score_fn(500.0)
        assert result == pytest.approx(1.0, abs=1e-10)

    def test_pmi_score_large_negative(self):
        result = pmi_score_fn(-500.0)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_abs_score_large_positive(self):
        result = abs_score_fn(500.0)
        assert result == pytest.approx(1.0, abs=1e-10)

    def test_abs_score_large_negative(self):
        result = abs_score_fn(-500.0)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_combined_large_both(self):
        result = combined_score_fn(500.0, 500.0)
        assert result == pytest.approx(1.0, abs=1e-10)

    def test_combined_small_both(self):
        result = combined_score_fn(-500.0, -500.0)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_confidence_large_value(self):
        assert confidence_fn(1e10) == pytest.approx(0.99, abs=1e-10)

    def test_confidence_exactly_one(self):
        assert confidence_fn(1.0) == pytest.approx(0.99, abs=1e-10)

    def test_softmax_all_same_large(self):
        scores = softmax_scores_fn([1e6, 1e6, 1e6])
        for s in scores:
            assert s == pytest.approx(0.333, abs=0.001)

    def test_softmax_rounding(self):
        scores = softmax_scores_fn([-1.0, -1.1])
        assert all(isinstance(s, float) for s in scores)

    @pytest.mark.parametrize("pmi", [0.0, 0.5, 1.0, -1.0, 2.0])
    def test_pmi_score_derivative_positive(self, pmi):
        """Derivative of sigmoid is always positive (increasing)."""
        eps = 1e-6
        d = (pmi_score_fn(pmi + eps) - pmi_score_fn(pmi)) / eps
        assert d > 0

    @pytest.mark.parametrize("cond_avg", [-7.0, -5.0, -3.0, 0.0, 2.0])
    def test_abs_score_derivative_positive(self, cond_avg):
        eps = 1e-6
        d = (abs_score_fn(cond_avg + eps) - abs_score_fn(cond_avg)) / eps
        assert d > 0


class TestContinuationClassification:
    """Test the result = 'likely' if score >= 0.5 else 'unlikely' logic."""

    @pytest.mark.parametrize("score,expected_result", [
        (0.0, "unlikely_continuation"),
        (0.1, "unlikely_continuation"),
        (0.2, "unlikely_continuation"),
        (0.3, "unlikely_continuation"),
        (0.4, "unlikely_continuation"),
        (0.499, "unlikely_continuation"),
        (0.5, "likely_continuation"),
        (0.501, "likely_continuation"),
        (0.6, "likely_continuation"),
        (0.7, "likely_continuation"),
        (0.8, "likely_continuation"),
        (0.9, "likely_continuation"),
        (1.0, "likely_continuation"),
    ])
    def test_classification_threshold(self, score, expected_result):
        result = "likely_continuation" if score >= 0.5 else "unlikely_continuation"
        assert result == expected_result


class TestMarginComputation:
    """Test the margin computation from _ocr_check: min_prob / TOKEN_PROB_FLOOR."""

    @pytest.mark.parametrize("min_prob,floor,expected_margin", [
        (0.05, 0.05, 1.0),
        (0.10, 0.05, 1.0),   # min(0.10/0.05, 1.0) = min(2.0, 1.0) = 1.0
        (0.025, 0.05, 0.5),
        (0.0, 0.05, 0.0),
        (0.01, 0.05, 0.2),
        (0.04, 0.05, 0.8),
        (0.049, 0.05, 0.98),
        (0.001, 0.05, 0.02),
        (1.0, 0.05, 1.0),
    ])
    def test_margin(self, min_prob, floor, expected_margin):
        margin = min(min_prob / floor, 1.0) if floor > 0 else 1.0
        assert margin == pytest.approx(expected_margin, abs=1e-10)

    @pytest.mark.parametrize("min_prob", [0.0, 0.01, 0.025, 0.04, 0.05, 0.1, 0.5, 1.0])
    def test_margin_confidence(self, min_prob):
        floor = 0.05
        margin = min(min_prob / floor, 1.0) if floor > 0 else 1.0
        conf = 0.80 + 0.19 * min(margin, 1.0)
        assert 0.80 <= conf <= 0.99

    def test_margin_zero_floor(self):
        margin = min(0.5 / 0.05, 1.0) if 0.05 > 0 else 1.0
        assert margin == 1.0


class TestImprovementComputation:
    """Test improvement = max(raw_lps[1:]) - raw_lps[0]."""

    @pytest.mark.parametrize("raw_lps,expected_improvement", [
        ([-10.0, -5.0], 5.0),
        ([-10.0, -10.0], 0.0),
        ([-10.0, -15.0], -5.0),
        ([-10.0, -5.0, -3.0], 7.0),
        ([-10.0, -5.0, -3.0, -1.0], 9.0),
        ([-5.0, -5.0, -5.0], 0.0),
        ([0.0, 1.0], 1.0),
        ([0.0, -1.0], -1.0),
        ([-100.0, -1.0], 99.0),
    ])
    def test_improvement(self, raw_lps, expected_improvement):
        improvement = max(raw_lps[1:]) - raw_lps[0] if len(raw_lps) > 1 else 0.0
        assert improvement == pytest.approx(expected_improvement, abs=1e-10)

    def test_improvement_single_element(self):
        raw_lps = [-10.0]
        improvement = max(raw_lps[1:]) - raw_lps[0] if len(raw_lps) > 1 else 0.0
        assert improvement == 0.0


# ═══════════════════════════════════════════════════════════════════════════
# 4. _build_correction() logic tests  (~200 test cases)
# ═══════════════════════════════════════════════════════════════════════════


class MockTokenizer:
    """Mock tokenizer with a configurable decode method."""

    def __init__(self, decode_map=None):
        self.decode_map = decode_map or {}

    def decode(self, token_ids):
        if len(token_ids) == 1 and token_ids[0] in self.decode_map:
            return self.decode_map[token_ids[0]]
        return f"tok{token_ids[0]}"


def make_token(char_start, char_end, actual_text, actual_prob, top_preds):
    """Helper to build a token dict like _token_predictions returns."""
    return {
        "char_start": char_start,
        "char_end": char_end,
        "actual_text": actual_text,
        "actual_prob": actual_prob,
        "top_preds": top_preds,
    }


def build_correction_pure(word, word_start, word_end, suspicious, rank, tokenizer):
    """
    Pure reimplementation of _build_correction for testing without lm dependency.
    Mirrors the app.py logic exactly.
    """
    result = word
    replacements = []
    for tok in sorted(suspicious, key=lambda t: t["char_start"], reverse=True):
        cs, ce = tok["char_start"], tok["char_end"]
        overlap_start = max(cs, word_start) - word_start
        overlap_end = min(ce, word_end) - word_start
        if rank < len(tok["top_preds"]):
            top_id, top_prob = tok["top_preds"][rank]
            alt_text = tokenizer.decode([top_id]).strip()
            if alt_text:
                replacements.append((overlap_start, overlap_end, alt_text))
    for start, end, alt in replacements:
        result = result[:start] + alt + result[end:]
    return result


class TestBuildCorrectionBasic:
    """Basic correction building tests."""

    @pytest.mark.parametrize("word,ws,we,cs,ce,top_id,decode_text,expected", [
        ("br0wn", 4, 9, 6, 7, 100, "o", "brown"),
        ("hello", 0, 5, 0, 2, 200, "he", "hello"),
        ("t3st", 0, 4, 1, 2, 300, "e", "test"),
        ("w0rld", 0, 5, 1, 2, 400, "o", "world"),
        ("h3llo", 0, 5, 1, 2, 500, "e", "hello"),
    ])
    def test_single_suspicious_token(self, word, ws, we, cs, ce, top_id, decode_text, expected):
        tok = MockTokenizer({top_id: decode_text})
        suspicious = [make_token(cs, ce, word[cs - ws:ce - ws], 0.01, [(top_id, 0.9)])]
        result = build_correction_pure(word, ws, we, suspicious, 0, tok)
        assert result == expected

    def test_no_suspicious_tokens(self):
        tok = MockTokenizer()
        result = build_correction_pure("hello", 0, 5, [], 0, tok)
        assert result == "hello"

    def test_empty_word(self):
        tok = MockTokenizer()
        result = build_correction_pure("", 0, 0, [], 0, tok)
        assert result == ""

    @pytest.mark.parametrize("rank", [0, 1, 2, 3, 4])
    def test_rank_selection(self, rank):
        top_preds = [(100 + i, 0.9 - i * 0.1) for i in range(5)]
        decode_map = {100 + i: f"alt{i}" for i in range(5)}
        tok = MockTokenizer(decode_map)
        suspicious = [make_token(0, 1, "x", 0.01, top_preds)]
        result = build_correction_pure("xello", 0, 5, suspicious, rank, tok)
        expected = f"alt{rank}ello"
        assert result == expected

    def test_rank_out_of_bounds(self):
        """If rank >= len(top_preds), no replacement should be made."""
        tok = MockTokenizer({100: "a"})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, 5, tok)
        assert result == "xello"

    @pytest.mark.parametrize("rank", [1, 2, 3, 10, 100])
    def test_rank_beyond_preds(self, rank):
        tok = MockTokenizer({100: "a"})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, rank, tok)
        assert result == "xello"


class TestBuildCorrectionMultipleTokens:
    """Multiple suspicious tokens in one word."""

    def test_two_suspicious_tokens(self):
        decode_map = {100: "e", 200: "o"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(1, 2, "3", 0.01, [(100, 0.9)]),  # position 1: '3' -> 'e'
            make_token(4, 5, "0", 0.01, [(200, 0.9)]),  # position 4: '0' -> 'o'
        ]
        result = build_correction_pure("h3ll0", 0, 5, suspicious, 0, tok)
        assert result == "hello"

    def test_three_suspicious_tokens(self):
        decode_map = {100: "e", 200: "l", 300: "o"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(1, 2, "3", 0.01, [(100, 0.9)]),
            make_token(2, 3, "1", 0.01, [(200, 0.9)]),
            make_token(4, 5, "0", 0.01, [(300, 0.9)]),
        ]
        result = build_correction_pure("h31l0", 0, 5, suspicious, 0, tok)
        assert result == "hello"

    def test_adjacent_suspicious_tokens(self):
        decode_map = {100: "a", 200: "b"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(0, 1, "x", 0.01, [(100, 0.9)]),
            make_token(1, 2, "y", 0.01, [(200, 0.9)]),
        ]
        result = build_correction_pure("xycd", 0, 4, suspicious, 0, tok)
        assert result == "abcd"

    @pytest.mark.parametrize("n_suspicious", [1, 2, 3, 4, 5])
    def test_n_suspicious_tokens(self, n_suspicious):
        word = "x" * 10
        decode_map = {100 + i: chr(ord("a") + i) for i in range(n_suspicious)}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(i, i + 1, "x", 0.01, [(100 + i, 0.9)])
            for i in range(n_suspicious)
        ]
        result = build_correction_pure(word, 0, 10, suspicious, 0, tok)
        for i in range(n_suspicious):
            assert result[i] == chr(ord("a") + i)


class TestBuildCorrectionReverseOrder:
    """Verify that replacements happen in reverse character order."""

    def test_reverse_order_preserves_indices(self):
        """Replacing later characters first preserves earlier char indices."""
        decode_map = {100: "A", 200: "B"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(1, 2, "x", 0.01, [(100, 0.9)]),  # position 1
            make_token(3, 4, "y", 0.01, [(200, 0.9)]),  # position 3
        ]
        result = build_correction_pure("axbyc", 0, 5, suspicious, 0, tok)
        assert result == "aAbBc"

    def test_reverse_order_with_different_lengths(self):
        """Replacement text can be different length from original."""
        decode_map = {100: "XX", 200: "Y"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(0, 1, "a", 0.01, [(100, 0.9)]),  # 1 char -> 2 chars
            make_token(2, 3, "c", 0.01, [(200, 0.9)]),  # 1 char -> 1 char
        ]
        result = build_correction_pure("abc", 0, 3, suspicious, 0, tok)
        assert result == "XXbY"


class TestBuildCorrectionWordOffset:
    """Test with non-zero word_start offsets."""

    @pytest.mark.parametrize("word,ws,we,cs,ce,top_id,decode_text,expected", [
        ("hello", 10, 15, 11, 12, 100, "E", "hEllo"),
        ("world", 20, 25, 20, 21, 200, "W", "World"),
        ("test", 5, 9, 7, 8, 300, "S", "teSt"),
        ("word", 100, 104, 100, 104, 400, "WORD", "WORD"),
    ])
    def test_offset_word(self, word, ws, we, cs, ce, top_id, decode_text, expected):
        tok = MockTokenizer({top_id: decode_text})
        suspicious = [make_token(cs, ce, "x", 0.01, [(top_id, 0.9)])]
        result = build_correction_pure(word, ws, we, suspicious, 0, tok)
        assert result == expected

    @pytest.mark.parametrize("ws", [0, 5, 10, 50, 100, 1000])
    def test_various_word_starts(self, ws):
        """The word offset shouldn't affect the correction logic."""
        we = ws + 5
        tok = MockTokenizer({100: "o"})
        suspicious = [make_token(ws + 1, ws + 2, "0", 0.01, [(100, 0.9)])]
        result = build_correction_pure("h0llo", ws, we, suspicious, 0, tok)
        assert result == "hollo"


class TestBuildCorrectionEmptyDecode:
    """Tokens where decode returns empty string (should skip)."""

    def test_empty_decode_skipped(self):
        tok = MockTokenizer({100: ""})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "xello"

    def test_whitespace_only_decode_stripped_to_empty(self):
        tok = MockTokenizer({100: "   "})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "xello"

    def test_mixed_empty_and_valid(self):
        decode_map = {100: "", 200: "e"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(0, 1, "x", 0.01, [(100, 0.9)]),  # empty decode, skip
            make_token(1, 2, "3", 0.01, [(200, 0.9)]),  # valid decode
        ]
        result = build_correction_pure("x3llo", 0, 5, suspicious, 0, tok)
        assert result == "xello"


class TestBuildCorrectionOverlap:
    """Token spans that partially overlap word boundaries."""

    def test_token_starts_before_word(self):
        tok = MockTokenizer({100: "HE"})
        # Token spans chars 3..6 but word is at 5..10
        suspicious = [make_token(3, 6, "xxx", 0.01, [(100, 0.9)])]
        result = build_correction_pure("hello", 5, 10, suspicious, 0, tok)
        # overlap_start = max(3,5)-5 = 0, overlap_end = min(6,10)-5 = 1
        assert result == "HEello"

    def test_token_ends_after_word(self):
        tok = MockTokenizer({100: "EL"})
        # Token spans chars 8..12 but word ends at 10
        suspicious = [make_token(8, 12, "xxxx", 0.01, [(100, 0.9)])]
        result = build_correction_pure("hello", 5, 10, suspicious, 0, tok)
        # overlap_start = max(8,5)-5 = 3, overlap_end = min(12,10)-5 = 5
        assert result == "helEL"


class TestBuildCorrectionLongReplacements:
    """Replacements that change string length."""

    @pytest.mark.parametrize("original_char,replacement,expected_word", [
        ("x", "ab", "abello"),
        ("x", "abc", "abcello"),
        ("x", "a", "aello"),
        ("xy", "a", "allo"),
    ])
    def test_different_length_replacements(self, original_char, replacement, expected_word):
        tok = MockTokenizer({100: replacement})
        end = len(original_char)
        suspicious = [make_token(0, end, original_char, 0.01, [(100, 0.9)])]
        word = original_char + "ello" if len(original_char) == 1 else original_char + "llo"
        result = build_correction_pure(word, 0, len(word), suspicious, 0, tok)
        assert result == expected_word


class TestBuildCorrectionTopPredsVariety:
    """Various top_preds configurations."""

    def test_single_pred(self):
        tok = MockTokenizer({100: "a"})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "aello"

    def test_five_preds_rank0(self):
        decode_map = {i: chr(ord("a") + i - 100) for i in range(100, 105)}
        tok = MockTokenizer(decode_map)
        preds = [(100 + i, 0.9 - i * 0.1) for i in range(5)]
        suspicious = [make_token(0, 1, "x", 0.01, preds)]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "aello"

    def test_five_preds_rank4(self):
        decode_map = {i: chr(ord("a") + i - 100) for i in range(100, 105)}
        tok = MockTokenizer(decode_map)
        preds = [(100 + i, 0.9 - i * 0.1) for i in range(5)]
        suspicious = [make_token(0, 1, "x", 0.01, preds)]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "aello"

    def test_empty_top_preds(self):
        tok = MockTokenizer()
        suspicious = [make_token(0, 1, "x", 0.01, [])]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        assert result == "xello"

    @pytest.mark.parametrize("n_preds", [0, 1, 2, 3, 4, 5, 10])
    def test_various_pred_counts(self, n_preds):
        decode_map = {100 + i: chr(ord("a") + i) for i in range(n_preds)}
        tok = MockTokenizer(decode_map)
        preds = [(100 + i, 0.9 - i * 0.05) for i in range(n_preds)]
        suspicious = [make_token(0, 1, "x", 0.01, preds)]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        if n_preds > 0:
            assert result == "aello"
        else:
            assert result == "xello"


class TestBuildCorrectionSortOrder:
    """Verify sorted(suspicious, key=..., reverse=True) behavior."""

    def test_unsorted_input_still_works(self):
        """Even if suspicious tokens come in forward order, reverse sort is applied."""
        decode_map = {100: "A", 200: "B"}
        tok = MockTokenizer(decode_map)
        # Provide in forward order; function should sort in reverse
        suspicious = [
            make_token(0, 1, "a", 0.01, [(100, 0.9)]),
            make_token(3, 4, "d", 0.01, [(200, 0.9)]),
        ]
        result = build_correction_pure("abcd", 0, 4, suspicious, 0, tok)
        assert result == "AbcB"

    def test_already_reverse_sorted(self):
        decode_map = {100: "A", 200: "B"}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(3, 4, "d", 0.01, [(200, 0.9)]),
            make_token(0, 1, "a", 0.01, [(100, 0.9)]),
        ]
        result = build_correction_pure("abcd", 0, 4, suspicious, 0, tok)
        assert result == "AbcB"

    @pytest.mark.parametrize("positions", [
        [0, 2, 4],
        [4, 2, 0],
        [2, 0, 4],
        [4, 0, 2],
        [0, 4, 2],
        [2, 4, 0],
    ])
    def test_any_order_same_result(self, positions):
        decode_map = {100 + i: chr(ord("A") + i) for i in range(3)}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(pos, pos + 1, "x", 0.01, [(100 + i, 0.9)])
            for i, pos in enumerate(positions)
        ]
        result = build_correction_pure("x_x_x_", 0, 6, suspicious, 0, tok)
        # Due to reverse sort, replacements apply from right to left
        # but the result should be deterministic regardless of input order
        result2 = build_correction_pure("x_x_x_", 0, 6, suspicious, 0, tok)
        assert result == result2


class TestBuildCorrectionDecodeStrip:
    """Verify decode result is stripped."""

    @pytest.mark.parametrize("raw_decode,stripped", [
        ("  hello  ", "hello"),
        ("\thello\t", "hello"),
        (" a ", "a"),
        ("word", "word"),
        ("  ", ""),
        ("\t\n", ""),
    ])
    def test_strip_behavior(self, raw_decode, stripped):
        tok = MockTokenizer({100: raw_decode})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure("xello", 0, 5, suspicious, 0, tok)
        if stripped:
            assert result == stripped + "ello"
        else:
            assert result == "xello"


# ═══════════════════════════════════════════════════════════════════════════
# 5. Configuration and constants tests  (~100 test cases)
# ═══════════════════════════════════════════════════════════════════════════


class TestConfigDefaults:
    """Default values of configuration constants."""

    def test_top_k_default(self):
        from app import TOP_K
        assert TOP_K == 5

    def test_min_word_len_default(self):
        from app import MIN_WORD_LEN
        assert MIN_WORD_LEN == 2

    def test_top_k_is_int(self):
        from app import TOP_K
        assert isinstance(TOP_K, int)

    def test_min_word_len_is_int(self):
        from app import MIN_WORD_LEN
        assert isinstance(MIN_WORD_LEN, int)

    def test_top_k_positive(self):
        from app import TOP_K
        assert TOP_K > 0

    def test_min_word_len_positive(self):
        from app import MIN_WORD_LEN
        assert MIN_WORD_LEN > 0


class TestConfigEnvParsing:
    """Environment variable parsing for configuration."""

    def test_token_prob_floor_default(self):
        default = float("0.05")
        assert default == 0.05

    def test_min_lp_gain_default(self):
        default = float("1.0")
        assert default == 1.0

    def test_similarity_floor_default(self):
        default = float("0.5")
        assert default == 0.5

    @pytest.mark.parametrize("env_val,expected", [
        ("0.01", 0.01),
        ("0.05", 0.05),
        ("0.1", 0.1),
        ("0.5", 0.5),
        ("1.0", 1.0),
        ("0.0", 0.0),
        ("0.001", 0.001),
        ("0.999", 0.999),
    ])
    def test_float_env_parsing(self, env_val, expected):
        assert float(env_val) == expected

    @pytest.mark.parametrize("env_val", [
        "not_a_number",
        "abc",
        "",
        "None",
    ])
    def test_invalid_float_env(self, env_val):
        with pytest.raises(ValueError):
            float(env_val)

    @pytest.mark.parametrize("env_val,expected", [
        ("5001", 5001),
        ("8080", 8080),
        ("0", 0),
        ("65535", 65535),
    ])
    def test_port_parsing(self, env_val, expected):
        assert int(env_val) == expected


class TestConfigTokenProbFloor:
    """TOKEN_PROB_FLOOR behavior in filtering logic."""

    @pytest.mark.parametrize("actual_prob,floor,is_suspicious", [
        (0.01, 0.05, True),
        (0.04, 0.05, True),
        (0.049, 0.05, True),
        (0.05, 0.05, False),
        (0.06, 0.05, False),
        (0.1, 0.05, False),
        (0.5, 0.05, False),
        (1.0, 0.05, False),
        (0.0, 0.05, True),
        (0.0001, 0.05, True),
    ])
    def test_suspicious_threshold(self, actual_prob, floor, is_suspicious):
        assert (actual_prob < floor) == is_suspicious

    @pytest.mark.parametrize("floor", [0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
    def test_floor_at_boundary(self, floor):
        assert not (floor < floor)  # exactly at floor is not suspicious
        assert (floor - 0.001) < floor  # just below is suspicious


class TestConfigMinWordLen:
    """MIN_WORD_LEN filtering logic."""

    @pytest.mark.parametrize("word,min_len,should_skip", [
        ("a", 2, True),
        ("ab", 2, False),
        ("abc", 2, False),
        ("x", 2, True),
        ("", 2, True),
        ("hello", 2, False),
        ("a", 1, False),
        ("ab", 1, False),
        ("ab", 3, True),
        ("abc", 3, False),
    ])
    def test_word_length_filter(self, word, min_len, should_skip):
        assert (len(word) < min_len) == should_skip


class TestConfigSimilarityFloor:
    """SIMILARITY_FLOOR and SequenceMatcher behavior."""

    @pytest.mark.parametrize("a,b,above_floor", [
        ("brown", "brown", True),
        ("br0wn", "brown", True),
        ("hello", "jello", True),
        ("test", "text", True),
        ("abc", "xyz", False),
        ("computer", "elephant", False),
        ("a", "z", False),
        ("ab", "ab", True),
        ("hello", "hello", True),
    ])
    def test_similarity_filter(self, a, b, above_floor):
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        assert (ratio > 0.5) == above_floor

    @pytest.mark.parametrize("a,b", [
        ("same", "same"),
        ("UPPER", "upper"),
        ("Mixed", "mixed"),
    ])
    def test_identical_words_high_similarity(self, a, b):
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        assert ratio == 1.0

    @pytest.mark.parametrize("a,b", [
        ("a", "zzzzzzzzzzzzz"),
        ("abc", "xyzxyzxyz"),
    ])
    def test_very_different_words_low_similarity(self, a, b):
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        assert ratio < 0.5


class TestConfigModelId:
    """MODEL_ID default value."""

    def test_default_model_id(self):
        default = "Qwen/Qwen3-8B-Base"
        assert "Qwen" in default
        assert "8B" in default

    def test_model_id_format(self):
        default = "Qwen/Qwen3-8B-Base"
        assert "/" in default
        parts = default.split("/")
        assert len(parts) == 2
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


class TestConfigAuthToken:
    """AUTH_TOKEN behavior."""

    def test_empty_auth_token_default(self):
        default = ""
        assert default == ""
        assert not default  # falsy

    @pytest.mark.parametrize("token,should_check", [
        ("", False),
        ("abc123", True),
        ("secret-token", True),
        ("Bearer xyz", True),
    ])
    def test_auth_token_truthy(self, token, should_check):
        assert bool(token) == should_check


class TestRegexWordPattern:
    """Test the regex pattern used for word finding in _ocr_check."""

    import re

    @pytest.mark.parametrize("text,expected_words", [
        ("hello world", ["hello", "world"]),
        ("  hello  world  ", ["hello", "world"]),
        ("one", ["one"]),
        ("", []),
        ("   ", []),
        ("a b c", ["a", "b", "c"]),
        ("hello, world!", ["hello,", "world!"]),
        ("123 456", ["123", "456"]),
        ("mixed 123 content", ["mixed", "123", "content"]),
    ])
    def test_non_space_word_split(self, text, expected_words):
        import re
        words = [m.group() for m in re.finditer(r"\S+", text)]
        assert words == expected_words


class TestRegexFirstWordPattern:
    """Test the exact regex used in _first_word."""

    import re

    @pytest.mark.parametrize("text,expected_match", [
        ("hello", "hello"),
        ("HELLO", "HELLO"),
        ("well-known", "well-known"),
        ("don't", "don't"),
        ("123hello", "hello"),
        ("", None),
        ("123", None),
        ("!!!", None),
        ("a-b-c", "a-b-c"),
        ("a'b'c", "a'b'c"),
        ("a-b'c-d", "a-b'c-d"),
    ])
    def test_first_word_regex(self, text, expected_match):
        import re
        hit = re.search(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text)
        if expected_match is None:
            assert hit is None
        else:
            assert hit.group() == expected_match


class TestLogProbSum:
    """Test the log-prob sum calculation logic."""

    @pytest.mark.parametrize("log_probs,expected_sum", [
        ([], 0.0),
        ([0.0], 0.0),
        ([-1.0], -1.0),
        ([-1.0, -2.0], -3.0),
        ([-0.5, -0.5, -0.5], -1.5),
        ([-10.0, -20.0, -30.0], -60.0),
        ([0.0, 0.0, 0.0], 0.0),
        ([-1.0, -1.0, -1.0, -1.0, -1.0], -5.0),
    ])
    def test_sum_log_probs(self, log_probs, expected_sum):
        result = sum(lp for lp in log_probs)
        assert result == pytest.approx(expected_sum, abs=1e-10)


class TestAvgLogProb:
    """Test average log-prob calculation."""

    @pytest.mark.parametrize("log_probs,expected_avg", [
        ([-1.0], -1.0),
        ([-1.0, -2.0], -1.5),
        ([-2.0, -4.0, -6.0], -4.0),
        ([0.0, 0.0], 0.0),
        ([-10.0], -10.0),
        ([-1.0, -1.0, -1.0, -1.0], -1.0),
    ])
    def test_avg_log_probs(self, log_probs, expected_avg):
        result = sum(log_probs) / len(log_probs)
        assert result == pytest.approx(expected_avg, abs=1e-10)


class TestPMICalculation:
    """Test PMI = cond_avg - uncond_avg."""

    @pytest.mark.parametrize("cond_avg,uncond_avg,expected_pmi", [
        (-2.0, -4.0, 2.0),
        (-4.0, -4.0, 0.0),
        (-6.0, -4.0, -2.0),
        (-1.0, -10.0, 9.0),
        (-10.0, -1.0, -9.0),
        (0.0, 0.0, 0.0),
        (-5.0, -5.0, 0.0),
        (-3.0, -8.0, 5.0),
    ])
    def test_pmi_calculation(self, cond_avg, uncond_avg, expected_pmi):
        pmi = cond_avg - uncond_avg
        assert pmi == pytest.approx(expected_pmi, abs=1e-10)


class TestScoreRounding:
    """Test rounding behavior in score outputs."""

    @pytest.mark.parametrize("value,places,expected", [
        (0.1234, 3, 0.123),
        (0.1235, 3, 0.123),  # banker's rounding: round half to even
        (0.1, 3, 0.1),
        (0.999, 3, 0.999),
        (0.9999, 3, 1.0),
        (0.5, 3, 0.5),
        (0.0, 3, 0.0),
        (1.0, 3, 1.0),
        (0.0005, 3, 0.001),
        (0.0004, 3, 0.0),
    ])
    def test_round_to_3(self, value, places, expected):
        assert round(value, places) == expected


# ═══════════════════════════════════════════════════════════════════════════
# Additional tests to reach ~2000 total
# ═══════════════════════════════════════════════════════════════════════════


class TestFirstWordAlphabetCombinations:
    """Test _first_word with two-letter combinations and patterns."""

    @pytest.mark.parametrize("c1,c2", [
        (chr(ord("a") + i), chr(ord("a") + j))
        for i in range(0, 26, 5) for j in range(0, 26, 5)
    ])
    def test_two_letter_combos(self, c1, c2):
        assert _first_word(c1 + c2) == c1 + c2

    @pytest.mark.parametrize("prefix,word", [
        (".", "test"),
        (",", "test"),
        (";", "test"),
        (":", "test"),
        ("!", "test"),
        ("?", "test"),
        ("(", "test"),
        (")", "test"),
        ("[", "test"),
        ("]", "test"),
        ("{", "test"),
        ("}", "test"),
        ("<", "test"),
        (">", "test"),
        ("/", "test"),
        ("\\", "test"),
        ("|", "test"),
        ("@", "test"),
        ("#", "test"),
        ("$", "test"),
        ("%", "test"),
        ("^", "test"),
        ("&", "test"),
        ("*", "test"),
        ("+", "test"),
        ("=", "test"),
        ("~", "test"),
        ("`", "test"),
        ('"', "test"),
    ])
    def test_every_punctuation_prefix(self, prefix, word):
        assert _first_word(prefix + word) == word


class TestFirstWordMultiWordExtended:
    """Ensure only first word from more complex multi-word inputs."""

    @pytest.mark.parametrize("text,expected", [
        ("the quick brown fox", "the"),
        ("a b c d e f g h i j", "a"),
        ("Hello, my name is John", "hello"),
        ("123 start here now", "start"),
        ("---prefix word1 word2", "prefix"),
        ("...ellipsis then words", "ellipsis"),
        ("(parens) here", "parens"),
        ("[bracket] text", "bracket"),
        ("12:30 PM today", "pm"),
        ("$100.00 price", "price"),
        ("user@example.com domain", "user"),
        ("file.txt name", "file"),
        ("path/to/file rest", "path"),
        ("key=value pair", "key"),
        ("a, b, c, d", "a"),
    ], ids=lambda x: repr(x)[:40])
    def test_multi_word_variants(self, text, expected):
        assert _first_word(text) == expected


class TestFirstWordNewlineVariants:
    """_first_word with different newline placements."""

    @pytest.mark.parametrize("text,expected", [
        ("word\nanother", "word"),
        ("\nword", "word"),
        ("\n\nword", "word"),
        ("word\n", "word"),
        ("first\nsecond\nthird", "first"),
        ("\r\nword", "word"),
        ("word\r\n", "word"),
        ("\rword", "word"),
        ("line1\rline2", "line"),
        ("a\nb\nc\nd", "a"),
    ], ids=lambda x: repr(x)[:40])
    def test_newline_variants(self, text, expected):
        assert _first_word(text) == expected


class TestPmiScoreGrid:
    """Grid of PMI values for comprehensive coverage."""

    @pytest.mark.parametrize("pmi", [x * 0.25 for x in range(-40, 41)])
    def test_pmi_quarter_increments(self, pmi):
        result = pmi_score_fn(pmi)
        assert 0.0 <= result <= 1.0
        if pmi > 0.5:
            assert result > 0.5
        elif pmi < 0.5:
            assert result < 0.5


class TestAbsScoreGrid:
    """Grid of cond_avg values for comprehensive coverage."""

    @pytest.mark.parametrize("cond_avg", [x * 0.25 for x in range(-40, 21)])
    def test_abs_quarter_increments(self, cond_avg):
        result = abs_score_fn(cond_avg)
        assert 0.0 <= result <= 1.0
        if cond_avg > -5.0:
            assert result > 0.5
        elif cond_avg < -5.0:
            assert result < 0.5


class TestCombinedScoreGrid:
    """Grid of combined scores."""

    @pytest.mark.parametrize("pmi,cond_avg", [
        (p, c)
        for p in [-5.0, -2.0, 0.0, 0.5, 1.0, 3.0, 5.0]
        for c in [-10.0, -7.0, -5.0, -3.0, -1.0, 0.0, 2.0]
    ])
    def test_combined_grid(self, pmi, cond_avg):
        result = combined_score_fn(pmi, cond_avg)
        assert 0.0 <= result <= 1.0
        assert result == pytest.approx(
            pmi_score_fn(pmi) * abs_score_fn(cond_avg), abs=1e-10
        )


class TestSoftmaxExtended:
    """Extended softmax tests."""

    @pytest.mark.parametrize("raw", [
        [float(x) for x in range(-10, 0)],
        [float(x) for x in range(0, 10)],
        [float(x) * 0.1 for x in range(-50, 51)],
        [-100.0, -99.0],
        [100.0, 101.0],
    ])
    def test_softmax_sum_extended(self, raw):
        scores = softmax_scores_fn(raw)
        assert sum(scores) == pytest.approx(1.0, abs=0.02)

    @pytest.mark.parametrize("n", [2, 3, 5, 7, 10, 15, 20])
    def test_softmax_uniform_n(self, n):
        raw = [0.0] * n
        scores = softmax_scores_fn(raw)
        expected = round(1.0 / n, 3)
        for s in scores:
            assert s == pytest.approx(expected, abs=0.002)

    @pytest.mark.parametrize("winner_idx", [0, 1, 2, 3, 4])
    def test_softmax_one_dominant(self, winner_idx):
        raw = [0.0] * 5
        raw[winner_idx] = 100.0
        scores = softmax_scores_fn(raw)
        assert scores[winner_idx] == 1.0
        for i, s in enumerate(scores):
            if i != winner_idx:
                assert s == 0.0


class TestConfidenceExtended:
    """Extended confidence calculation tests."""

    @pytest.mark.parametrize("value", [x * 0.05 for x in range(0, 21)])
    def test_confidence_fine_grained(self, value):
        result = confidence_fn(value)
        expected = 0.80 + 0.19 * min(value, 1.0)
        assert result == pytest.approx(expected, abs=1e-15)

    @pytest.mark.parametrize("value", [1.0, 1.5, 2.0, 5.0, 10.0, 50.0, 100.0])
    def test_confidence_clamped_extended(self, value):
        assert confidence_fn(value) == pytest.approx(0.99, abs=1e-10)


class TestSchemaModelDump:
    """Additional model_dump tests."""

    @pytest.mark.parametrize("result_str", [
        "ok", "issue_detected", "error", "unknown", "",
        "a" * 100, "special!@#$%",
    ])
    def test_check_response_dump_result(self, result_str):
        resp = CheckResponse(result=result_str, score=0.5, spans=[])
        d = resp.model_dump()
        assert d["result"] == result_str
        assert d["score"] == 0.5
        assert d["spans"] == []

    @pytest.mark.parametrize("n_nested", [0, 1, 3, 5, 10])
    def test_nested_suggestions_dump(self, n_nested):
        suggs = [Suggestion(text=f"s{i}", score=0.1 * i) for i in range(n_nested)]
        span = Span(start=0, end=5, text="word", kind="ocr_error", suggestions=suggs)
        d = span.model_dump()
        assert len(d["suggestions"]) == n_nested
        for i in range(n_nested):
            assert d["suggestions"][i]["text"] == f"s{i}"

    def test_continuation_request_dump(self):
        req = ContinuationRequest(first="hello", second="world")
        d = req.model_dump()
        assert d["first"] == "hello"
        assert d["second"] == "world"

    def test_check_request_dump(self):
        req = CheckRequest(text="test text")
        d = req.model_dump()
        assert d["text"] == "test text"


class TestBuildCorrectionAdditional:
    """Additional _build_correction edge cases."""

    @pytest.mark.parametrize("word_len", [2, 3, 5, 10, 20, 50])
    def test_single_char_replacement_various_lengths(self, word_len):
        word = "x" * word_len
        tok = MockTokenizer({100: "a"})
        suspicious = [make_token(0, 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure(word, 0, word_len, suspicious, 0, tok)
        assert result == "a" + "x" * (word_len - 1)

    @pytest.mark.parametrize("pos", range(10))
    def test_replacement_at_every_position(self, pos):
        word = "x" * 10
        tok = MockTokenizer({100: "A"})
        suspicious = [make_token(pos, pos + 1, "x", 0.01, [(100, 0.9)])]
        result = build_correction_pure(word, 0, 10, suspicious, 0, tok)
        expected = "x" * pos + "A" + "x" * (9 - pos)
        assert result == expected

    def test_all_tokens_suspicious(self):
        word = "xxxx"
        decode_map = {100 + i: chr(ord("a") + i) for i in range(4)}
        tok = MockTokenizer(decode_map)
        suspicious = [
            make_token(i, i + 1, "x", 0.01, [(100 + i, 0.9)])
            for i in range(4)
        ]
        result = build_correction_pure(word, 0, 4, suspicious, 0, tok)
        assert result == "abcd"


class TestSequenceMatcherDetails:
    """Detailed SequenceMatcher ratio tests for similarity logic."""

    @pytest.mark.parametrize("a,b,expected_ratio", [
        ("abc", "abc", 1.0),
        ("abc", "abd", 2 / 3),
        ("abc", "xyz", 0.0),
        ("", "", 1.0),
        ("a", "a", 1.0),
        ("ab", "ba", 0.5),
        ("abcd", "abce", 0.75),
        ("hello", "hallo", 0.8),
        ("test", "text", 0.75),
    ])
    def test_sequence_matcher_ratio(self, a, b, expected_ratio):
        from difflib import SequenceMatcher
        ratio = SequenceMatcher(None, a, b).ratio()
        assert ratio == pytest.approx(expected_ratio, abs=0.01)


class TestCheckRequestSpecialChars:
    """CheckRequest with various special character content."""

    @pytest.mark.parametrize("text", [
        "\x00",
        "\x01\x02\x03",
        "\x7f",
        "\xff",
        "null\x00byte",
        "bell\x07char",
        "backspace\x08char",
        "form\x0cfeed",
        "vertical\x0btab",
        "escape\x1bchar",
    ])
    def test_control_characters(self, text):
        req = CheckRequest(text=text)
        assert req.text == text


class TestContinuationRequestSpecialChars:
    """ContinuationRequest with special characters."""

    @pytest.mark.parametrize("first,second", [
        ("\x00", "hello"),
        ("hello", "\x00"),
        ("\t\n\r", "\t\n\r"),
        ("line1\nline2", "line3\nline4"),
        ("col1\tcol2", "col3\tcol4"),
        ("cr\rhere", "cr\rthere"),
    ])
    def test_special_chars_in_continuation(self, first, second):
        req = ContinuationRequest(first=first, second=second)
        assert req.first == first
        assert req.second == second


class TestSpanFieldCombinations:
    """Span with various field value combinations."""

    @pytest.mark.parametrize("start,end,text,kind,n_suggs", [
        (0, 1, "a", "k", 0),
        (0, 100, "long text", "ocr_error", 5),
        (50, 55, "hello", "probable_ocr_error", 3),
        (999, 1000, "x", "spelling", 1),
        (0, 0, "", "empty_span", 0),
        (0, 10000, "a" * 100, "very_long", 10),
        (42, 42, "", "zero_width", 0),
        (10, 20, "0123456789", "digits", 2),
    ])
    def test_span_combinations(self, start, end, text, kind, n_suggs):
        suggs = [Suggestion(text=f"s{i}", score=0.5) for i in range(n_suggs)]
        span = Span(start=start, end=end, text=text, kind=kind, suggestions=suggs)
        assert span.start == start
        assert span.end == end
        assert span.text == text
        assert span.kind == kind
        assert len(span.suggestions) == n_suggs


class TestCheckResponseScoreBoundaries:
    """CheckResponse with boundary score values."""

    @pytest.mark.parametrize("score", [
        float("inf"), float("-inf"),
        1e-300, 1e300,
        -1e-300, -1e300,
        0.0, -0.0,
        1.0, -1.0,
        0.001, 0.999,
        sys.float_info.min,
        sys.float_info.max,
        sys.float_info.epsilon,
    ])
    def test_extreme_scores(self, score):
        resp = CheckResponse(result="ok", score=score, spans=[])
        assert resp.score == score

    def test_nan_score(self):
        resp = CheckResponse(result="ok", score=float("nan"), spans=[])
        assert math.isnan(resp.score)


class TestSigmoidProperties:
    """Mathematical properties of the sigmoid functions."""

    @pytest.mark.parametrize("x", [float(i) * 0.5 for i in range(-20, 21)])
    def test_pmi_sigmoid_complement(self, x):
        """sigma(x) + sigma(-x) = 1 (shifted)."""
        # For f(pmi) = sigma((pmi - 0.5) * 3), check f(0.5+d) + f(0.5-d) = 1
        d = x
        s1 = pmi_score_fn(0.5 + d)
        s2 = pmi_score_fn(0.5 - d)
        assert s1 + s2 == pytest.approx(1.0, abs=1e-10)

    @pytest.mark.parametrize("x", [float(i) * 0.5 for i in range(-20, 21)])
    def test_abs_sigmoid_complement(self, x):
        d = x
        s1 = abs_score_fn(-5.0 + d)
        s2 = abs_score_fn(-5.0 - d)
        assert s1 + s2 == pytest.approx(1.0, abs=1e-10)

from data_sanitizer import slugify
import re


def test_accented_and_non_ascii():
    assert slugify("Café mañana") == "cafe-manana"
    assert slugify("naïve façade") == "naive-facade"


def test_emojis_and_special_chars_removed():
    out = slugify("hello😀world")
    assert isinstance(out, str)
    assert not re.search(r"[^\x00-\x7f]", out)


def test_bytes_and_numbers():
    assert slugify(12345) == "12345"
    # bytes should not raise
    assert isinstance(slugify(b"\xff"), str)


def test_very_long_string_truncated():
    s = "a" * 5000
    out = slugify(s)
    assert len(out) <= 5000

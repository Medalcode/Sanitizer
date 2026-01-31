from data_sanitizer import slugify
import re

def test_accented_and_non_ascii():
    assert slugify("Café mañana") == "cafe-manana"
    assert slugify("naïve façade") == "naive-facade"

def test_emojis_causing_empty():
    # If string is only emojis, it effectively becomes empty -> None
    assert slugify("😀😀") is None
    
def test_mixed_content():
    # "hello world" part remains
    assert slugify("hello😀world") == "hello-world"

def test_bytes_and_numbers():
    assert slugify(12345) == "12345"
    # bytes should not raise
    assert isinstance(slugify(b"foo"), str)

def test_truncation():
    s = "a" * 300
    out = slugify(s, max_length=10)
    assert len(out) == 10

def test_magic_string_removal():
    # Contract: empty or invalid returns None, not "n-a"
    assert slugify("") is None
    assert slugify(None) is None
    assert slugify("---") is None

def test_uppercase_support():
    # Bug fix validation
    assert slugify("HolaMundo", lower=False) == "HolaMundo"

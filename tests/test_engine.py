"""Unified test suite for the data_sanitizer engine."""
import pytest
import datetime
from data_sanitizer import (
    standardize_date,
    slugify,
    is_email,
    is_url,
    to_float,
    to_int,
    is_strong_password,
    infer_boolean
)

# ==========================================
# 1. Date Tests
# ==========================================

def test_date_basics():
    assert standardize_date(None) is None
    assert standardize_date("") is None
    assert standardize_date("   ") is None
    assert standardize_date("32/13/2020") is None
    assert standardize_date("29-02-2019") is None

def test_date_epoch():
    out = standardize_date(1609459200)
    assert out is not None
    assert "2021-01-01" in out

# ==========================================
# 2. Text & Slug Tests
# ==========================================

def test_slugify_basics():
    assert slugify("Café mañana") == "cafe-manana"
    assert slugify("naïve façade") == "naive-facade"
    assert slugify("😀😀") is None
    assert slugify("hello😀world") == "hello-world"
    assert slugify(12345) == "12345"
    assert slugify("HolaMundo", lower=False) == "HolaMundo"

def test_slugify_limits():
    s = "a" * 300
    assert len(slugify(s, max_length=10)) == 10
    assert slugify("---") is None

# ==========================================
# 3. Validation Tests
# ==========================================

def test_validation_basics():
    assert is_email("user@example.com")
    assert not is_email("not-an-email")
    assert is_url("https://example.com")
    assert not is_url("ftp://example.com")
    assert is_strong_password("Aa1!aaaa")
    assert not is_strong_password("weak")

# ==========================================
# 4. Conversion Tests
# ==========================================

def test_conversion_basics():
    # Numeric
    assert to_float("1,234.56") == 1234.56
    assert to_float("1.234,56", decimal_separator=",") == 1234.56
    assert to_float("$100") is None
    assert to_int("42.9") == 42
    assert to_int("nope", default=0) == 0
    
    # Boolean
    assert infer_boolean("yes") is True
    assert infer_boolean("0") is False
    assert infer_boolean("maybe") is None

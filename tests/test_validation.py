from data_sanitizer import is_email, is_url, to_float, to_int, is_strong_password, infer_boolean

def test_is_email_basic():
    assert is_email("user@example.com")
    assert not is_email("not-an-email")
    assert not is_email(None)

def test_is_url_basic():
    assert is_url("https://example.com")
    assert is_url("http://localhost")
    assert not is_url("ftp://example.com")

def test_to_float_explicit():
    # US Format (default)
    assert to_float("1,234.56") == 1234.56
    
    # European Format (explicit config)
    assert to_float("1.234,56", decimal_separator=",") == 1234.56
    
    # Currency symbols (should NOT be stripped by default, so it returns default/None)
    # OLD behavior: stripped everything. NEW behavior: safe failure.
    assert to_float("$100") is None
    
    # Primitives
    assert to_float(100) == 100.0
    assert to_float(None) is None

def test_to_int_and_default():
    assert to_int("42") == 42
    assert to_int("42.9") == 42
    # use 'default', not 'fallback'
    assert to_int("nope", default=0) == 0

def test_password_strength():
    assert is_strong_password("Aa1!aaaa")
    assert not is_strong_password("weakpass")

def test_infer_boolean():
    assert infer_boolean("yes") is True
    assert infer_boolean("0") is False
    assert infer_boolean("maybe") is None

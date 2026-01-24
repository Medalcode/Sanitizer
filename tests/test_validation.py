from data_sanitizer import is_email, is_url, to_float, to_int, is_strong_password, infer_boolean


def test_is_email_basic():
    assert is_email("user@example.com")
    assert not is_email("not-an-email")


def test_is_url_basic():
    assert is_url("https://example.com")
    assert not is_url("ftp://example.com")


def test_to_float_various():
    assert to_float("1,234.56") == 1234.56
    assert to_float("1.234,56") == 1234.56
    assert to_float("$1 234,56") == 1234.56
    assert to_float(100) == 100.0
    assert to_float(None) is None


def test_to_int_and_fallback():
    assert to_int("42") == 42
    assert to_int("42.9") == 42
    assert to_int("nope", fallback=None) is None


def test_password_strength():
    assert is_strong_password("Aa1!aaaa")
    assert not is_strong_password("weakpass")


def test_infer_boolean():
    assert infer_boolean("yes") is True
    assert infer_boolean("0") is False
    assert infer_boolean("maybe") is None

import pytest
from data_sanitizer import standardize_date


def test_none_returns_none():
    assert standardize_date(None) is None


def test_empty_and_whitespace():
    assert standardize_date("") is None
    assert standardize_date("   ") is None


def test_invalid_dates_return_none():
    assert standardize_date("32/13/2020") is None
    assert standardize_date("2020-99-99") is None


def test_non_leap_feb29_returns_none():
    assert standardize_date("29-02-2019") is None


def test_epoch_int_parsed():
    out = standardize_date(1609459200)
    assert out is not None
    assert out.startswith("2021-01-01")

import importlib


def test_package_exposes_api():
    pkg = importlib.import_module('data_sanitizer')
    assert hasattr(pkg, 'standardize_date')
    assert hasattr(pkg, 'slugify')

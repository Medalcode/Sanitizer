"""Validadores y conversiones comunes: email, URL, numeric, password strength, boolean inference."""
from __future__ import annotations
import re
from typing import Optional, Union
from urllib.parse import urlparse


def is_email(value: Optional[str]) -> bool:
    if not value:
        return False
    s = str(value).strip()
    # Simplified but practical regex
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return bool(pattern.match(s))


def is_url(value: Optional[str]) -> bool:
    if not value:
        return False
    try:
        p = urlparse(str(value))
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def to_float(value: Union[str, int, float, None]) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return float(value)
        except Exception:
            return None
    s = str(value).strip()
    if s == "":
        return None
    # remove currency symbols and spaces
    s = re.sub(r"[\s\$€£¥]", "", s)
    # handle common formats
    try:
        return float(s)
    except Exception:
        pass

    # If contains only commas (e.g. '1.234,56' or '1234,56')
    if "," in s and "." not in s:
        s2 = s.replace('.', '').replace(',', '.')
        try:
            return float(s2)
        except Exception:
            return None

    # If contains both, decide by last occurrence
    if "," in s and "." in s:
        last_dot = s.rfind('.')
        last_comma = s.rfind(',')
        if last_dot > last_comma:
            # assume '.' decimal, remove commas
            s2 = s.replace(',', '')
        else:
            # assume ',' decimal, remove dots
            s2 = s.replace('.', '').replace(',', '.')
        try:
            return float(s2)
        except Exception:
            return None

    # last resort: remove non numeric except dot and minus
    s3 = re.sub(r"[^0-9\.-]", "", s)
    try:
        return float(s3)
    except Exception:
        return None


def to_int(value: Union[str, int, float, None], fallback: Optional[int] = None) -> Optional[int]:
    if value is None:
        return fallback
    if isinstance(value, int):
        return value
    try:
        return int(float(str(value)))
    except Exception:
        return fallback


def is_strong_password(pw: Optional[str], min_length: int = 8, require_upper: int = 1, require_digit: int = 1, require_special: int = 1) -> bool:
    if not pw or not isinstance(pw, str):
        return False
    if len(pw) < min_length:
        return False
    upper = sum(1 for c in pw if c.isupper())
    digits = sum(1 for c in pw if c.isdigit())
    special = sum(1 for c in pw if not c.isalnum())
    return upper >= require_upper and digits >= require_digit and special >= require_special


def infer_boolean(value: Union[str, int, bool, None]) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in ("1", "true", "t", "yes", "y", "on"):
        return True
    if s in ("0", "false", "f", "no", "n", "off"):
        return False
    return None

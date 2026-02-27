"""Core logic engine for data_sanitizer.

Consolidates conversion, normalization, and validation logic into a single high-performance module.
"""
from __future__ import annotations
import datetime
import re
import unicodedata
from typing import Any, Optional, Union
from urllib.parse import urlparse

# Optional dependency for dates
try:
    from dateutil import parser as _dateutil_parser
    HAS_DATEUTIL = True
except Exception:
    HAS_DATEUTIL = False

# ==========================================
# 1. Conversion & Casting (formerly converters.py)
# ==========================================

def to_int(
    value: Any, 
    /, *, 
    default: Optional[int] = None, 
    fallback: Optional[int] = None,
    strict: bool = False
) -> Optional[int]:
    """Convierte value a int de forma segura."""
    if fallback is not None and default is None:
        default = fallback

    if value is None:
        return default
    
    if isinstance(value, int):
        return value
        
    try:
        return int(float(value)) if isinstance(value, (str, float)) else int(value)
    except (ValueError, TypeError):
        if strict:
            raise
        return default

def to_float(
    value: Any, 
    /, *, 
    default: Optional[float] = None, 
    fallback: Optional[float] = None,
    decimal_separator: str = ".",
    strict: bool = False
) -> Optional[float]:
    """Convierte value a float de forma determinista."""
    if fallback is not None and default is None:
        default = fallback

    if value is None:
        return default

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip().replace(' ', '')

    if re.search(r"[^0-9\.,\-+]", s):
        if strict:
            raise ValueError(f"Valor no numérico: {value}")
        return default

    if "," in s and "." in s:
        if s.find('.') < s.find(','):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif "," in s and "." not in s:
        s = s.replace(',', '.')
    else:
        s = s.replace(',', '')

    try:
        return float(s)
    except (ValueError, TypeError):
        if strict:
            raise
        return default

def infer_boolean(
    value: Any, 
    /, *, 
    default: Optional[bool] = None, 
    strict: bool = False
) -> Optional[bool]:
    """Convierte input a bool basándose en strings comunes (yes/no, on/off)."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
        
    s = str(value).strip().lower()
    if s in ("1", "true", "t", "yes", "y", "on"):
        return True
    if s in ("0", "false", "f", "no", "n", "off"):
        return False
        
    if strict:
        raise ValueError(f"No se puede inferir booleano de: {value}")
    return default

# ==========================================
# 2. Date Normalization (formerly dates.py)
# ==========================================

def standardize_date(
    date_input: Union[str, int, float, datetime.date, datetime.datetime, None],
    prefer_day_first: Optional[bool] = None,
    tz: Optional[str] = None,
) -> Optional[str]:
    """Parsea varias representaciones de fecha y devuelve ISO 8601 o None."""
    if date_input is None:
        return None

    if isinstance(date_input, (int, float)):
        try:
            dt = datetime.datetime.fromtimestamp(int(date_input), tz=datetime.timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        except Exception:
            return None

    if isinstance(date_input, datetime.date) and not isinstance(date_input, datetime.datetime):
        try:
            return date_input.isoformat()
        except Exception:
            return None

    s = str(date_input).strip()
    if s == "":
        return None

    if HAS_DATEUTIL:
        try:
            dt = _dateutil_parser.parse(s, dayfirst=prefer_day_first)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        except Exception:
            pass

    formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d %b %Y", "%d %B %Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(s, fmt)
            return dt.date().isoformat()
        except Exception:
            continue
    return None

# ==========================================
# 3. Text & Slugification (formerly text.py)
# ==========================================

def remove_accents(text: Any) -> str:
    """Elimina acentos y diacríticos de un texto."""
    if text is None:
        return ""
    s: str
    if isinstance(text, (bytes, bytearray)):
        try:
            s = text.decode('utf-8')
        except Exception:
            s = text.decode('latin-1', errors='replace')
    else:
        s = str(text)
    nk = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nk if not unicodedata.combining(c))

def normalize_whitespace(text: Any) -> str:
    """Colapsa múltiples espacios en uno solo y trimmea."""
    if text is None:
        return ""
    return ' '.join(str(text).split())

def slugify(
    value: Any, 
    /, *, 
    lower: bool = True, 
    max_length: int = 255
) -> Optional[str]:
    """Genera un slug ASCII seguro para URLs."""
    if value is None:
        return None
    s = remove_accents(value)
    if lower:
        s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s, flags=re.IGNORECASE)
    s = s.strip('-')
    if max_length:
        s = s[:max_length]
    return s if s else None

# ==========================================
# 4. Pure Validation (formerly validation.py)
# ==========================================

def is_email(value: Any) -> bool:
    """Valida si un string parece un email."""
    if not value or not isinstance(value, str):
        return False
    s = value.strip()
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return bool(pattern.match(s))

def is_url(value: Any) -> bool:
    """Valida si un string es una URL HTTP(s) válida."""
    if not value or not isinstance(value, str):
        return False
    try:
        p = urlparse(value)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False

def is_strong_password(
    value: Any, 
    min_length: int = 8, 
    require_upper: int = 1, 
    require_digit: int = 1, 
    require_special: int = 1
) -> bool:
    """Valida complejidad de contraseña."""
    if not value or not isinstance(value, str):
        return False
    if len(value) < min_length:
        return False
    upper = sum(1 for c in value if c.isupper())
    digits = sum(1 for c in value if c.isdigit())
    special = sum(1 for c in value if not c.isalnum())
    return upper >= require_upper and digits >= require_digit and special >= require_special

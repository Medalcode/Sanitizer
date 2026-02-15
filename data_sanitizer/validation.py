"""Validadores booleanos puros.

Reglas:
1. Siempre retornan bool.
2. Nunca lanzan excepciones (fail-safe).
3. No transforman el dato.
"""
from __future__ import annotations
import re
from typing import Any, Optional
from urllib.parse import urlparse

def is_email(value: Any) -> bool:
    """Valida si un string parece un email."""
    if not value or not isinstance(value, str):
        return False
        
    s = value.strip()
    # Regex simplificado pero práctico
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return bool(pattern.match(s))

def is_url(value: Any) -> bool:
    """Valida si un string es una URL HTTP(s) válida."""
    if not value or not isinstance(value, str):
        return False
    try:
        p = urlparse(value)
        # Requiere scheme y netloc (dominio)
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
    
    return (upper >= require_upper and 
            digits >= require_digit and 
            special >= require_special)


# Re-exportes para compatibilidad y conveniencia
# Algunos tests y usuarios esperan importar funciones de conversión
# desde el módulo `data_sanitizer.validation`.
from .converters import to_int, to_float, infer_boolean  # noqa: F401

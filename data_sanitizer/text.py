"""Funciones de texto: slugify, remove_accents, normalize_whitespace."""
from __future__ import annotations
import re
import unicodedata
from typing import Optional, Union


def remove_accents(text: Optional[Union[str, bytes]]) -> str:
    if text is None:
        return ""
    if isinstance(text, (bytes, bytearray)):
        s = None
        try:
            s = text.decode('utf-8')
        except Exception:
            s = text.decode('latin-1', errors='replace')
    else:
        s = str(text)
    nk = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nk if not unicodedata.combining(c))


def normalize_whitespace(text: Optional[str]) -> str:
    if text is None:
        return ""
    return ' '.join(str(text).split())


def slugify(value: Optional[Union[str, bytes, int, float]], lower: bool = True, max_length: Optional[int] = 255) -> str:
    """Genera un slug ASCII simple a partir de `value`.

    - Usa `remove_accents` para normalizar acentos.
    - Reemplaza cualquier secuencia de caracteres no alfanuméricos por '-' y recorta guiones.
    - Si el resultado queda vacío devuelve 'n-a'.
    """
    if value is None:
        return 'n-a'
    s = remove_accents(value)
    if lower:
        s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    if max_length:
        s = s[:max_length]
    return s or 'n-a'

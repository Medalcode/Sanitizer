"""Funciones de normalización de texto."""
from __future__ import annotations
import re
import unicodedata
from typing import Optional, Union, Any

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
    """Genera un slug ASCII seguro para URLs.
    
    Retorna None si el resultado es vacío tras sanitizar.
    """
    if value is None:
        return None
        
    s = remove_accents(value)
    
    if lower:
        s = s.lower()
        
    # Reemplaza todo lo que NO sea alfanumérico por guión
    # Bug fix: Agregamos IGNORECASE para soportar mayúsculas si lower=False
    s = re.sub(r'[^a-z0-9]+', '-', s, flags=re.IGNORECASE)
    s = s.strip('-')
    
    if max_length:
        s = s[:max_length]
        
    return s if s else None

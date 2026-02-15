"""Módulo de conversión de tipos (Casting & Parsing).

Este módulo se encarga de transformar inputs sucios a tipos nativos de Python.
Filosofía:
- No adivinar (Explicit > Implicit).
- No lanzar excepciones por defecto (Fail-safe).
- Retornar None (o default) si la conversión no es posible.
"""
from __future__ import annotations
from typing import Any, Optional, Union
import re

def to_int(
    value: Any, 
    /, *, 
    default: Optional[int] = None, 
    fallback: Optional[int] = None,
    strict: bool = False
) -> Optional[int]:
    """Convierte value a int de forma segura.
    
    Args:
        value: Dato a convertir.
        default: Valor a retornar si falla la conversión.
        strict: Si True, lanza ValueError/TypeError en lugar de retornar default.
    """
    # Compatibilidad: `fallback` es alias histórico de `default`
    if fallback is not None and default is None:
        default = fallback

    if value is None:
        return default
    
    if isinstance(value, int):
        return value
        
    try:
        # Intenta conversión directa (maneja float a int truncando)
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
    """Convierte value a float de forma determinista.
    
    Args:
        value: Dato a convertir.
        default: Valor a retornar si falla.
        decimal_separator: Caracter usado como decimal ('.' o ',').
        strict: Si True, lanza excepción en fallo.
    """
    # Compatibilidad `fallback` alias de `default`
    if fallback is not None and default is None:
        default = fallback

    if value is None:
        return default

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    # Normalizar espacios internos
    s = s.replace(' ', '')

    # Si hay caracteres fuera del conjunto permitido (dígitos, punto, coma, signo),
    # consideramos que no es un número limpio (p. ej. incluye símbolo de moneda)
    if re.search(r"[^0-9\.,\-+]", s):
        if strict:
            raise ValueError(f"Valor no numérico: {value}")
        return default

    # Heurística para resolver ambigüedades entre punto y coma:
    if "," in s and "." in s:
        # Ej: "1.234,56" -> '.' aparece antes de ',' => estilo europeo
        if s.find('.') < s.find(','):
            s = s.replace('.', '').replace(',', '.')
        else:
            # Ej: "1,234.56" -> estilo US
            s = s.replace(',', '')
    elif "," in s and "." not in s:
        # Solo coma -> tratar coma como decimal
        s = s.replace(',', '.')
    else:
        # Solo punto o ninguno -> eliminar comas (separadores de miles)
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

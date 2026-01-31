"""Módulo de conversión de tipos (Casting & Parsing).

Este módulo se encarga de transformar inputs sucios a tipos nativos de Python.
Filosofía:
- No adivinar (Explicit > Implicit).
- No lanzar excepciones por defecto (Fail-safe).
- Retornar None (o default) si la conversión no es posible.
"""
from __future__ import annotations
from typing import Any, Optional, Union

def to_int(
    value: Any, 
    /, *, 
    default: Optional[int] = None, 
    strict: bool = False
) -> Optional[int]:
    """Convierte value a int de forma segura.
    
    Args:
        value: Dato a convertir.
        default: Valor a retornar si falla la conversión.
        strict: Si True, lanza ValueError/TypeError en lugar de retornar default.
    """
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
    if value is None:
        return default

    if isinstance(value, (int, float)):
        return float(value)
        
    s = str(value).strip()
    
    # Limpieza determinista basada en el separador decimal esperado
    if decimal_separator == ",":
        # Formato Europeo: 1.234,56 -> 1234.56
        # Eliminamos puntos (miles) y reemplazamos coma por punto
        s = s.replace(".", "").replace(",", ".")
    else:
        # Formato US: 1,234.56 -> 1234.56
        # Eliminamos comas (miles)
        s = s.replace(",", "")
        
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

"""Módulo de normalización de fechas.

Función principal: standardize_date
Intenta usar python-dateutil si está disponible, y cae a múltiples formatos conocidos.
Devuelve ISO-8601 como cadena o None si no puede parsear.
"""
from __future__ import annotations
import datetime
from typing import Optional, Union

try:
    from dateutil import parser as _dateutil_parser
    HAS_DATEUTIL = True
except Exception:
    HAS_DATEUTIL = False


def standardize_date(
    date_input: Union[str, int, float, datetime.date, datetime.datetime, None],
    prefer_day_first: Optional[bool] = None,
    tz: Optional[str] = None,
) -> Optional[str]:
    """Parsea varias representaciones de fecha y devuelve ISO 8601 o None.

    - Si recibe int/float se interpreta como timestamp (segundos desde epoch).
    - Si dateutil está disponible, se usa como parser tolerante.
    - En fallback, intenta formatos comunes.
    - No depende de la zona local: devuelve 'Z' para UTC cuando sea apropiado.
    """
    if date_input is None:
        return None

    # epoch numeric
    if isinstance(date_input, (int, float)):
        try:
            dt = datetime.datetime.fromtimestamp(int(date_input), tz=datetime.timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        except Exception:
            return None

    # date object (no time)
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

    # fallback formats
    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
        "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(s, fmt)
            # treat as date-only
            return dt.date().isoformat()
        except Exception:
            continue

    return None

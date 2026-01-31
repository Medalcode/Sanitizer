# Diseño de API: Estrategia de Crecimiento Sostenible

Este documento esboza los patrones de diseño para permitir que `data_sanitizer` escale sin introducir "Breaking Changes".

## 1. El Patrón "Keyword-Only Arguments" (Defensa contra roturas)

Para permitir añadir configuración futura (`strict`, `locale`, `formats`) sin romper llamadas existentes, debemos forzar el uso de argumentos nombrados para todo lo que no sea el dato principal.

**Propuesta:** Usar el separador `*` en todas las firmas.

```python
# ANTES (Frágil si añadimos argumentos en medio)
def to_int(value, default, strict): ...

# DESPUÉS (Robusto)
def to_int(value: Any, /, *, default: Any = None, strict: bool = False, locale: Optional[str] = None) -> Optional[int]:
    ...
```

- **Beneficio:** Podemos añadir `timezone=...` o `currency=...` en el futuro en cualquier orden sin afectar a `to_int("123", default=0)`.

## 2. Manejo de Modos (Strict vs Safe)

Actualmente la librería es "Fail-safe" por defecto. Para soportar usuarios que necesitan validación estricta, introducimos el flag `strict`.

**Contrato:**

- `strict=False` (Default): Devuelve `None` (o `default`) si falla.
- `strict=True`: Levanta `data_sanitizer.errors.SanitizationError` con detalles del fallo.

```python
try:
    val = to_int("invalid", strict=True)
except SanitizationError:
    # Manejo explícito
    pass
```

## 3. Configuración Regional (Context Objects)

Evitar la "explosión de argumentos" (pasar `decimal_sep`, `thousand_sep`, `currency_symbol` función por función).

**Patrón: Objetos de Configuración (Dataclasses)**

En lugar de añadir lógica compleja de parsing dentro de `to_float`, permitimos inyectar una "estrategia" o configuración.

```python
from dataclasses import dataclass

@dataclass
class NumberFormat:
    decimal: str = '.'
    thousand: str = ','

# Uso
to_float("1.234,56", config=NumberFormat(decimal=',', thousand='.'))
```

Esto extrae la complejidad de localización fuera del núcleo de la función.

## 4. Extensibilidad de Tipos (Registry Pattern - Opcional)

Si en el futuro necesitamos sanitizar objetos complejos (ej. `UserDTO`), no sobrecargamos la librería.

**Patrón: Composición Funcional**
La librería no debe intentar validar todo tipo de objeto. Debe proveer los "ladrillos" para que el usuario construya su validador.

```python
# No hacer esto en la librería:
# def sanitize_user(user_dict): ...

# Hacer esto (Documentación):
def sanitize_user(data):
    return {
        "age": to_int(data.get("age")),
        "email": data.get("email") if is_email(data.get("email")) else None
    }
```

## Resumen de Reglas para Contribuidores

1.  El primer argumento es siempre el `value` (Positional-Only `/`).
2.  Todos los argumentos de configuración son `Keyword-Only` (`*`).
3.  Nunca usar booleanos para lógica compleja (`is_date(v, european=True)` ❌ -> `is_date(v, formats=['%d-%m'])` ✅).
4.  Si un argumento cambia el comportamiento drásticamente, encapsularlo en un objeto de configuración.

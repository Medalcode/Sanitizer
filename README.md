# Data Sanitizer

> **Validación y limpieza de datos robusta para el mundo real.**
> Diseñado para ingerir inputs caóticos y devolver tipos predecibles.

`data_sanitizer` es una librería Python ligera enfocada en la **defensibilidad**: su objetivo es parsear, validar y normalizar datos de entrada (archivos CSV sucios, excels de usuario, APIs legacy) sin lanzar excepciones inesperadas.

## ¿Por qué Data Sanitizer?

Cuando procesas datos del mundo real, no quieres un `ValueError` porque un usuario escribió "N/A" en un campo de edad. Quieres un flujo de datos continuo y predecible.

- **Fail-safe**: Las funciones de limpieza nunca rompen tu pipeline. Si no se puede limpiar, devuelven `None` (o un default), pero no explotan.
- **Tipado Fuerte**: Completamente anotada con Type Hints para integrarse con `mypy` y editores modernos.
- **Cero Magia**: Sin cadenas extrañas como `"error"` o `-1`. El fallo se representa explícitamente como ausencia de valor (`None`).

## Instalación

```bash
pip install data-sanitizer
```

## Guía Rápida

### Validación (Predicados booleanos)

Responden con seguridad si un dato cumple un criterio, manejando `None` y tipos incorrectos por ti.

```python
from data_sanitizer.validation import is_email, is_url

is_email("usuario@empresa.com")  # -> True
is_email("no es un email")       # -> False
is_email(None)                   # -> False
is_email(12345)                  # -> False (Seguro, no lanza error)
```

### Transformación (Conversión de tipos)

Convierte inputs sucios a tipos nativos.

```python
from data_sanitizer.validation import to_int, to_float, infer_boolean

# Números sucios
to_int("123")           # -> 123
to_int("Approx 100", fallback=0)  # -> 0

# Decimales ambiguos
to_float("1,200.50")    # -> 1200.5
to_float(None)          # -> None

# Inferencias lógicas
infer_boolean("Yes")    # -> True
infer_boolean("Off")    # -> False
```

### Normalización (Fechas y Texto)

Estandariza formatos para guardar en base de datos.

```python
from data_sanitizer.dates import standardize_date
from data_sanitizer.text import slugify

# Fechas caóticas -> ISO 8601
standardize_date("31/01/2023")  # -> "2023-01-31"
standardize_date("Jan 5th 2022") # -> "2022-01-05"

# Slugs para URLs
slugify("¡Hola Mundo!")  # -> "hola-mundo"
```

## Filosofía: Qué NO es esta librería

- **No es Pydantic/Marshmallow**: No define esquemas ni modelos de objetos completos. Es una colección de utilidades de bajo nivel para limpiar el dato _antes_ de pasarlo a tu validador de esquema.
- **No es Pandas**: No está optimizada para limpiar millones de filas vectorialmente (aunque puede usarse en un `apply`). Está pensada para lógica de negocio y ETLs de complejidad media.

## Contribuir

El código sigue estrictamente el estilo PEP 8 y Type Hinting. Antes de enviar un PR, asegúrate de que los tests pasen y no introduzcas dependencias pesadas innecesarias.

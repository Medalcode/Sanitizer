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
 
Todos los métodos son accesibles directamente desde el paquete raíz, gracias a la nueva arquitectura unificada.
 
```python
import data_sanitizer as ds
 
# 1. Validación (Siempre devuelven bool)
ds.is_email("usuario@empresa.com")  # -> True
ds.is_strong_password("Aa1!aaaa")   # -> True
 
# 2. Conversión (Casting seguro)
ds.to_int("42.9")                   # -> 42
ds.to_float("1.200,50", decimal_separator=",") # -> 1200.5
ds.infer_boolean("Yes")             # -> True
 
# 3. Normalización (ISO y ASCII)
ds.standardize_date("31/01/2023")   # -> "2023-01-31"
ds.slugify("¡Hola Mundo!")          # -> "hola-mundo"
```

## Filosofía: Qué NO es esta librería

- **No es Pydantic/Marshmallow**: No define esquemas ni modelos. Limpia el dato _antes_ del esquema.
- **No es Pandas**: No está vectorizada (aunque funciona perfecto en `df.apply`).

## Arquitectura y Mantenimiento

Este proyecto sigue una arquitectura **"Lean"** (mínima y eficiente):
- **Motor Central**: Toda la lógica reside en `data_sanitizer/engine.py`.
- **Agente de IA**: El mantenimiento está optimizado para Agentes mediante [agent.md](docs/agent.md) y [skills.md](docs/skills.md).
- **Roadmap**: Consulta el plan de futuro en [ARCHITECTURE.md](ARCHITECTURE.md#4-hoja-de-ruta-roadmap).

## Estado del Proyecto

- **Versión**: 0.2.0 (Refactorización Lean completada).
- **Calidad**: Suite de tests unificada en `tests/`.
- **CI**: GitHub Actions configurado en `.github/workflows/ci.yml`.

---
*Desarrollado con foco en la robustez y la simplicidad.*

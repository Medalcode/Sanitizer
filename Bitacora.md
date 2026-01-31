# Bitácora de cambios — Data Sanitizer

Fecha: 2026-01-23

Resumen: Registro de tareas realizadas y pendientes durante la creación del paquete `data_sanitizer`.

## Tareas completadas

- Crear paquete base y metadata (pyproject.toml)
- Añadir `data_sanitizer/__init__.py` y `_version.py`
- Implementar `data_sanitizer/dates.py` con `standardize_date` (uso de dateutil si disponible)
- Implementar `data_sanitizer/text.py` con `slugify`, `remove_accents`, `normalize_whitespace`
- Implementar `data_sanitizer/validation.py` con: `is_email`, `is_url`, `to_float`, `to_int`, `is_strong_password`, `infer_boolean`
- Crear tests unitarios en `tests/`: `test_standardize_date.py`, `test_slugify.py`, `test_validation.py`, `test_package_init.py`
- Crear entorno virtual local `.venv` para ejecutar tests (en entorno de desarrollo)
- Ejecutar suite de tests: todos los tests pasan (16 passed)

## Archivos añadidos

- `data_sanitizer/__init__.py`
- `data_sanitizer/_version.py`
- `data_sanitizer/dates.py`
- `data_sanitizer/text.py`
- `data_sanitizer/validation.py`
- `tests/test_standardize_date.py`
- `tests/test_slugify.py`
- `tests/test_validation.py`
- `tests/test_package_init.py`
- `pyproject.toml`
- `BITACORA.md`

## Pendientes / Recomendaciones

1. Mejorar validación de emails (usar `email-validator` o regex más completo).
2. Añadir sanitización HTML segura (`strip_html`) con `bleach` para XSS.
3. Añadir integración `pandas`-friendly (vectorizar funciones, ofrecer `apply` helpers).
4. Añadir CI formal en `.github/workflows/ci.yml` para ejecutar tests en PRs.
5. Preparar `setup.cfg` o `setup.py` y publicar en PyPI (definir extras: `[date]`, `[text]`).

## Notas de uso rápido

Instalar en editable (desarrollo):

```bash
# desde la raíz del repo
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install -e .
```

Ejecutar tests:

```bash
.venv/bin/python -m pytest -q
```

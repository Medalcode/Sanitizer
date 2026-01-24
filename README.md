
Data Sanitizer — paquete inicial

Este repositorio contiene la librería `data_sanitizer`, diseñada para validar y limpiar datos comunes (fechas, textos, números y validadores básicos).

Funciones principales incluidas:

- `standardize_date` (en `data_sanitizer.dates`)
- `slugify` (en `data_sanitizer.text`)
- Varios validadores en `data_sanitizer.validation` (`is_email`, `is_url`, `to_float`, `to_int`, `is_strong_password`, `infer_boolean`)

Instalación en modo editable (desarrollo):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install -e .
```

Ejecutar tests:

```bash
.venv/bin/python -m pytest -q
```

Consulta la bitácora con el historial de cambios y tareas en `BITACORA.md`.

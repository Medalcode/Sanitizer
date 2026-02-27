# Skills del agente para `data_sanitizer`

Resumen
- Este documento describe las habilidades (skills) que el agente puede ejecutar para mantener y mejorar el proyecto. Cada skill incluye propósito, entradas, salidas, ejemplos de comandos y criterios de éxito.

Skill: QualityAudit (Paramétrica)
- Objetivo: Ejecutar verificaciones de calidad (tests, linting, tipos) según parámetros.
- Parámetros: 
  - `tools`: Lista de herramientas a correr (`["pytest", "ruff", "mypy", "black"]`).
  - `fix`: Booleano para aplicar correcciones automáticas (p.ej. `ruff --fix`, `black`).
- Comando ejemplo: `pytest` / `ruff . --fix` / `mypy --strict`.
- Criterio de éxito: 0 errores detectados por las herramientas activadas.

Skill: ProjectDynamics (Paramétrica)
- Objetivo: Gestionar metadatos, documentación y automatización de CI.
- Parámetros:
  - `action`: `bump_version`, `update_changelog`, `generate_docs`, `init_ci`.
  - `scope`: `patch`, `minor`, `major`.
- Procedimiento: Actualizar `data_sanitizer/_version.py`, `CHANGELOG.md` o generar `.github/workflows/ci.yml`.
- Criterio de éxito: Archivos actualizados correctamente según el `scope` y persistencia de cambios en git.


- Referencias a tests y símbolos
- `standardize_date` — [data_sanitizer/dates.py](data_sanitizer/dates.py) — ver [tests/test_standardize_date.py](tests/test_standardize_date.py).
- `slugify` — [data_sanitizer/text.py](data_sanitizer/text.py) — ver [tests/test_slugify.py](tests/test_slugify.py).
- `to_int`, `to_float`, `infer_boolean` — [data_sanitizer/converters.py](data_sanitizer/converters.py) — ver [tests/test_validation.py](tests/test_validation.py) y [tests/test_audit_cases.py](tests/test_audit_cases.py).
- Validadores (`is_email`, `is_url`) — [data_sanitizer/validation.py](data_sanitizer/validation.py).

Contratos y comportamiento esperado (resumen de `ARCHITECTURE.md`)
- `is_*` (validadores): siempre retornan `bool` y nunca levantan excepciones; ante `None` devuelven `False`.
- `to_*` (convertidores): retornan `Optional[T]` (o `default`); no deben devolver cadenas "mágicas" y deben capturar fallos de parseo.
- `standardize_*` / `slugify` (normalizadores): devuelven una representación canónica o `None`; nunca retornar valores como `"n-a"`.
- Argumentos de configuración deben ser `Keyword-Only` y la librería favorece objetos de configuración (`NumberFormat`, etc.) para localización.

- Reglas de seguridad / intervención humana
- Cualquier cambio que modifique la firma pública de funciones exportadas en [data_sanitizer/__init__.py](data_sanitizer/__init__.py) debe crear un issue y requerir aprobación humana.
- Releases automáticas están deshabilitadas hasta que exista un pipeline de CI aprobado por los mantenedores.

Ejemplos de mensajes que el agente puede usar en un PR/issue
- Título PR sugerido: `fix: corregir parsing de fecha en standardize_date (test failing)`
- Cuerpo PR: breve descripción del fallo, comando para reproducir, archivos modificados, tests añadidos, y nota sobre version bump si aplica.

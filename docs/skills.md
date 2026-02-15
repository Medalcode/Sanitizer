# Skills del agente para `data_sanitizer`

Resumen
- Este documento describe las habilidades (skills) que el agente puede ejecutar para mantener y mejorar el proyecto. Cada skill incluye propósito, entradas, salidas, ejemplos de comandos y criterios de éxito.

Skill: RunTests
- Objetivo: Ejecutar la suite de pruebas y resumir resultados.
- Entrada: commit/branch a evaluar.
- Comando ejemplo: `pytest --maxfail=5 -q` y `python tests/run_tests.py`.
- Salida esperada: número de tests, lista de fallos con stack traces, categoría del fallo.
- Criterio de éxito: 0 tests fallidos. En caso contrario, crear issue o PR con fix mínimo y test que asegure la corrección.

Skill: LintAndType
- Objetivo: Verificar estilo y tipos, proponer fixes automáticos cuando sea seguro.
- Entrada: código modificado en PR/branch.
- Comandos ejemplo: `black --check .`, `ruff . --fix`, `mypy --strict` (si está configurado).
- Salida: lista de problemas, dif con fixes sugeridos.
- Criterio de éxito: formateo y ruff pasan; errores de mypy documentados o resueltos.

Skill: BumpVersionAndChangelog
- Objetivo: Aplicar bump de versión para parches/fixes y añadir changelog mínimo.
- Entrada: PR con arreglo de bug/feature menor.
- Procedimiento: actualizar `data_sanitizer/_version.py`, actualizar `pyproject.toml` si aplica, añadir sección en `CHANGELOG.md` o en la descripción del PR.
- Criterio de éxito: versión coherente (SemVer), tests pasan, PR documentado.

Skill: CreateReleaseCI (plantilla)
- Objetivo: Proponer un workflow de GitHub Actions para tests + publish (publish requiere aprobación humana).
- Output: archivo sugerido `.github/workflows/ci.yml` con jobs: test, lint, coverage-report.

Skill: AddDocs
- Objetivo: Generar o actualizar documentación en `docs/` con ejemplos de uso.
- Entrada: cambios en API o ejemplos de usuario.
- Ejemplo: añadir ejemplos de limpieza de CSV, normalización de fechas locales.

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

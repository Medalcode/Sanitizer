# Agente del repositorio: data_sanitizer

Propósito
- Proveer un agente autónomo seguro y auditable que ejecute comprobaciones, proponga cambios y mantenga la calidad del paquete `data_sanitizer`.

Alcance y límites
- Permitido: ejecutar tests, ejecutar linters/type checks (si existen), proponer PRs con cambios no disruptivos (correcciones de tests, formateo, documentación, bump de parche).
- Prohibido sin revisión humana: modificaciones a la API pública, cambios de diseño en `API_DESIGN.md` o `ARCHITECTURE.md`, y publicaciones a PyPI.

Comandos permitidos (ejemplos)
- Ejecutar tests: `pytest`.
- Lint/type (si se incorporan): `black --check`, `ruff --fix`, `mypy --strict`.

Playbook: Agente Generalista (Operaciones de Ciclo de Vida)
- Auditoría Técnica:
  - Acción: Ejecutar `Skill: QualityAudit` con `tools=["pytest", "ruff", "mypy", "black"]`.
  - Objetivo: Detectar regresiones y problemas de estilo. Prioridad a fixes automáticos (`fix=True`).
- Gestión de Versiones y Docs:
  - Acción: Ejecutar `Skill: ProjectDynamics` para `bump_version`, `update_changelog` o `generate_docs`.
  - Política: Seguir SemVer estrictamente. Parches automáticos permitidos.
- Contribución Segura:
  - Acción: Crear PR incluyendo descripción de cambios, resultados de auditoría y notas de versión.


Referencias clave
- API pública y versión: [data_sanitizer/__init__.py](data_sanitizer/__init__.py)
- Funciones críticas: [data_sanitizer/dates.py](data_sanitizer/dates.py), [data_sanitizer/text.py](data_sanitizer/text.py), [data_sanitizer/converters.py](data_sanitizer/converters.py), [data_sanitizer/validation.py](data_sanitizer/validation.py)
- Diseño y reglas: [API_DESIGN.md](API_DESIGN.md), [ARCHITECTURE.md](ARCHITECTURE.md)

Buenas prácticas
- No publicar releases automáticamente sin pasar gates de CI (tests + mypy + coverage).
- Registrar en cada PR los comandos ejecutados y los resultados para trazabilidad.

Modo `strict` vs `safe` y manejo de errores
- Este repositorio implementa el patrón `strict` vs `safe` descrito en [API_DESIGN.md](API_DESIGN.md):
  - `strict=False` (por defecto): funciones como `to_int`/`to_float` retornan `None` o `default` ante fallos.
  - `strict=True`: las funciones pueden levantar `data_sanitizer.errors.SanitizationError` con detalles del fallo.
- El agente debe respetar este contrato: no cambiar el valor por defecto de `strict` sin aprobación humana y no suprimir excepciones de `strict=True` en cambios automatizados.

Localización y objetos de configuración
- `API_DESIGN.md` propone usar objetos de configuración (p.ej. `NumberFormat` dataclass) para evitar explotar la firma de funciones con muchos kwargs de localización. El agente puede proponer la adición de estos objetos si detecta parsing repetido por locales, pero cualquier cambio debe documentarse en el PR y respetar `Keyword-Only Arguments`.

Escalado y mejoras futuras (recomendadas)
- Integrar CI (GitHub Actions) con jobs para tests, type-checks y coverage.
- Añadir `pre-commit` con `black`, `isort` y `ruff`.
- Documentar políticas de versionado y release (CHANGELOG.md, release checklist).

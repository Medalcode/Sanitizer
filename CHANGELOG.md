# Changelog

Todas las modificaciones notables a este proyecto se registran en este archivo.

## [0.2.0] - 2026-02-26
- **Refactorización Lean**: Consolidación de lógica dispersa en `data_sanitizer/engine.py`.
- **Simplificación de Tests**: Fusión de tests unitarios en `tests/test_engine.py` y eliminación de runners manuales.
- **Consolidación de Agentes**: Merge de playbooks y skills en `docs/` hacia un Agente Generalista paramétrico.
- **Limpieza de Deuda**: Eliminación de archivos redundantes (`converters.py`, `dates.py`, `text.py`, `validation.py`, `Bitacora.md`, etc.).

## [0.1.0] - initial
- Versión inicial con soporte para fechas, slugs y validaciones básicas.
- Añadidos docs operativos: `docs/agent.md`, `docs/skills.md`.
- Plantilla de CI: `.github/workflows/ci.yml`.
- Versión inicial según `pyproject.toml` / `data_sanitizer/_version.py`.

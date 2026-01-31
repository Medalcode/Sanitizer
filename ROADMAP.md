# Roadmap del Proyecto: Data Sanitizer

Este documento outlinea el plan de desarrollo para evolucionar `data_sanitizer` hacia una versión 1.0 estable y lista para producción.

---

## 📅 Milestone 0.2.0: Estabilización del Core (Actual)

**Objetivo:** Reparar la deuda técnica existente y alinear la implementación con el contrato de arquitectura (`ARCHITECTURE.md`).

### High Priority Fixes

- [ ] **Refactor `validation.py`**: Separar validadores puros (`is_*`) de convertidores (`to_*`). Mover lógica de conversión a nuevo módulo `converters.py`.
- [ ] **Estandarizar API de Retorno**:
  - Eliminar retorno mágico `"n-a"` en `slugify` (cambiar a `None` o string vacío).
  - Asegurar que todos los convertidores acepten parámetro `default=...`.
- [ ] **Bugfix Critical**: Corregir regex en `slugify` para soportar mayúsculas correctamente cuando `lower=False`.

### Quality Assurance

- [ ] **Type Hinting Estricto**: Asegurar cobertura 100% de tipos y pase de `mypy --strict`.
- [ ] **Test Coverage**: Alcanzar >90% de cobertura, incluyendo casos de regresión detectados en auditoría.

---

## 📅 Milestone 0.3.0: Robustez y Localización

**Objetivo:** Hacer la librería útil internacionalmente y manejar edge cases comunes (monedas, fechas ambiguas).

### Nuevas Features

- [ ] **Soporte de Localización en `to_float`**:
  - Añadir argumento `decimal_separator` o `locale`.
  - Eliminar la lógica de "adivinanza" peligrosa actual.
  - Soportar formatos financieros explícitos (ej. "1.234,00 €").
- [ ] **Mejoras en Fechas**:
  - Soportar zonas horarias explícitas en `standardize_date`.
  - Permitir definir formato de salida (ej. devolver objeto `date` nativo vs string ISO).

---

## 📅 Milestone 0.4.0: Ecosistema y DX

**Objetivo:** Mejorar la experiencia de desarrollo (DX) y facilitar la integración.

### Developer Experience

- [ ] **Manejo de Excepciones Opcional**: Añadir modo `strict=True` en convertidores para que lancen errores (`SanitizerError`) en lugar de devolver `None`, para usuarios que prefieren control de flujo por excepciones.
- [ ] **Decoradores de Limpieza**: Crear decoradores `@sanitize_arguments` para limpiar inputs de funciones automáticamente.

### Documentación

- [ ] Publicar documentación en ReadTheDocs o similar.
- [ ] Añadir recetas comunes ("Cookbook"): Limpieza de CSVs, integración con Flask/FastAPI.

---

## 📅 Milestone 1.0.0: Release Major

**Objetivo:** API estable congelada. Garantía de no breaking changes.

- [ ] Auditoría de seguridad final.
- [ ] Optimización de rendimiento (cythonización opcional para funciones críticas como `slugify`).
- [ ] SemVer estricto a partir de este punto.

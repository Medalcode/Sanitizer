# Arquitectura y Contrato de API - Data Sanitizer

Este documento define la filosofía de diseño y el contrato estricto que deben seguir todas las funciones dentro de la librería `data_sanitizer`. El objetivo es garantizar **predictibilidad**, **seguridad de tipos** y **facilidad de uso**.

## 1. Filosofía General

1.  **Fail-safe (Seguridad ante fallos):** Las funciones de limpieza no deben romper la ejecución del programa principal por datos sucios inesperados.
2.  **Sin cadenas mágicas (No Magic Strings):** Nunca devolver valores de dominio como `"n-a"`, `"unknown"` o `-1` para indicar error. Usar `None` o excepciones tipadas.
3.  **Tipado fuerte (Type Hinting):** Todas las funciones deben estar completamente tipadas (`PEP 484`).

## 2. Contrato de Funciones

Distinguimos tres familias de funciones con contratos distintos:

### A. Validadores (`is_*`)

Funciones puras booleanas que responden a la pregunta: _"¿Cumple el dato X con el criterio Y?"_

- **Firma:** `def is_algo(value: Any, **kwargs) -> bool`
- **Retorno:** Estrictamente `bool` (`True` / `False`).
- **Comportamiento ante `None`:** Devuelve `False`.
- **Manejo de Errores:**
  - **Nunca levantar excepciones** por datos mal formados.
  - Si el input es de un tipo incomparable (ej. lista en lugar de string), devolver `False`.
- **Ejemplo:**
  ```python
  is_email("bad@email") -> False
  is_email(None) -> False
  is_email(123) -> False  # No lanza AttributeError
  ```

### B. Convertidores (`to_*`)

Funciones que intentan transformar un dato sucio a un tipo primitivo de Python (int, float, bool).

- **Firma:** `def to_tipo(value: Any, default: Optional[T] = None) -> Optional[T]`
- **Retorno:** El tipo destino `T` o `None`.
- **Parámetro `default`:** Opcional. Valor a devolver si la conversión falla.
- **Comportamiento ante `None`:** Devuelve `None` (o `default` si se provee).
- **Manejo de Errores:**
  - Capturar errores de parseo (`ValueError`, `TypeError`).
  - No realizar limpiezas destructivas agresivas (ej. no eliminar letras arbitrarias para forzar un número) a menos que se especifique explícitamente.
  - Si la conversión no es segura/evidente, fallar retornando `None`.
- **Ejemplo:**
  ```python
  to_int("123") -> 123
  to_int("abc", default=0) -> 0
  to_int(None) -> None
  ```

### C. Normalizadores (`standardize_*` / `slugify`)

Funciones complejas que aplican reglas de negocio para devolver un formato canónico.

- **Firma:** `def standardize_algo(value: Any, **options) -> Optional[str]` (u otro tipo complejo)
- **Retorno:** Una representación canónica (usualmente `str` en formato estándar ej. ISO-8601) o `None`.
- **Manejo de Errores:**
  - Devolver `None` si la normalización no es posible.
  - Evitar adivinación excesiva ("magic guessing"). Si hay ambigüedad crítica (ej. fechas ambiguas), preferir `None` o requerir configuración explícita.
- **Ejemplo:**
  ```python
  slugify("Hola Mundo") -> "hola-mundo"
  slugify(None) -> None  # JAMÁS "n-a"
  standardize_date("2023/12/31") -> "2023-12-31"
  ```

## 3. Guía de Estilo

- **Argumentos:** Los inputs principales deben llamarse `value` para validar/convertir, o nombres específicos (`text`, `date_input`) si el dominio es restringido.
- **Depuración:** No usar `print`. Si se requiere logging, inyectar un logger o usar el módulo `logging` estándar de forma silenciosa.

## 4. Hoja de Ruta (Roadmap)
 
### Milestone 0.3.0: Robustez y Localización
- [ ] **Soporte de Localización en `to_float`**:
  - Parámtero `locale` para formatos específicos (ej. "1.234,00 €").
  - Gestión mejorada de símbolos de moneda.
- [ ] **Mejoras en Fechas**:
  - Soporte de zonas horarias (`pytz` / `zoneinfo`).
  - Retorno opcional de objetos `datetime` nativos.
 
### Milestone 0.4.0: Ecosistema y DX
- [ ] **Manejo de Excepciones**: Modo `strict=True` para levantar `SanitizerError`.
- [ ] **Decoradores**: `@sanitize_arguments` para limpieza automática de inputs en funciones de usuario.
- [ ] **Pandas Integration**: Helpers para `df.apply()` eficientes.
 
### Milestone 1.0.0: Release Major
- [ ] Auditoría de seguridad final (XSS/SQL injection checks).
- [ ] Congelación de API y SemVer estricto.

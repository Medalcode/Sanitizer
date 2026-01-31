
import pytest
import datetime
from data_sanitizer.validation import (
    is_email,
    is_url,
    to_float,
    to_int,
    infer_boolean,
    is_strong_password,
)
from data_sanitizer.dates import standardize_date
from data_sanitizer.text import slugify, remove_accents, normalize_whitespace

# ==========================================
# 1. Tests de Validación (Validation vs Transformation)
# ==========================================

class TestValidation:
    """Verifica que los validadores solo retornen bool y manejen inputs sucios."""

    def test_is_email_edge_cases(self):
        # Empty/None
        assert is_email(None) is False
        assert is_email("") is False
        assert is_email("   ") is False
        
        # Valid but tricky
        assert is_email("user.name+tag@example.co.uk") is True
        
        # Invalid structures
        assert is_email("user@example") is False # Missing TLD? Depends on regex
        assert is_email("user@.com") is False
        assert is_email("@example.com") is False
        
        # Non-string injection checking (should handle gracefully)
        assert is_email(123) is False 
        assert is_email(None) is False

    def test_is_url_edge_cases(self):
        # Empty/None
        assert is_url(None) is False
        
        # Scheme validation
        assert is_url("google.com") is False # Missing scheme check
        assert is_url("ftp://example.com") is False # Code allows only http/https?
        
        # Malformed
        assert is_url("http://") is False # No netloc
        assert is_url("http://??") is False 

# ==========================================
# 2. Tests de Transformación Numérica (Conversion)
# ==========================================

class TestNumericConversion:
    """Prueba la lógica de inferencia y limpieza."""

    def test_to_float_ambiguity_and_locales(self):
        # Punto decimal
        assert to_float("10.5") == 10.5
        
        # Coma decimal
        assert to_float("10,5") == 10.5
        
        # Miles y decimales mezclados (Ambiguous)
        # Case: "1.234,56" -> 1234.56 (European style)
        assert to_float("1.234,56") == 1234.56
        
        # Case: "1,234.56" -> 1234.56 (US style)
        assert to_float("1,234.56") == 1234.56
        
        # Case: "1.234" -> Could be 1.234 or 1234.0. 
        # Current logic might treat this ambiguously.
        # Check actual behavior for documentation.
        result = to_float("1.234")
        # Si la lógica detecta ',' y '.' decide, pero si solo hay uno...
        # El código actual: if ',' not in s and '.' in s -> float("1.234") -> 1.234
        assert result == 1.234

    def test_to_float_destructive_behavior(self):
        """Test para detectar si la transformación destruye datos válidos (Ip address, version numbers)."""
        # IP Address - Riesgo de que se convierta en número gigante
        # "192.168.0.1" -> float() might fail, fallback regex removes non-numeric?
        # Código actual tiene un "last resort" que remueve chars regex `[^0-9\.-]`
        # "192.168.0.1" -> mantiene puntos -> "192.168.0.1" -> float() falla (Multiple dots)
        assert to_float("192.168.0.1") is None 
        
        # Currency
        assert to_float("$ 100.00") == 100.0

    def test_to_int_types(self):
        assert to_int("10.5") == 10 # Truncates? Or rounds? int(float(s)) truncates.
        assert to_int(None, fallback=0) == 0
        assert to_int("invalid", fallback=-1) == -1

# ==========================================
# 3. Tests de Fechas (Parsing & Normalization)
# ==========================================

class TestDateSanitization:
    
    def test_standardize_date_formats(self):
        # YYYY-MM-DD
        assert standardize_date("2023-01-31") == "2023-01-31T00:00:00Z" or standardize_date("2023-01-31") == "2023-01-31" 
        # Note: The code behavior (isoformat()) includes time 'T00:00:00' if it parsed as datetime, 
        # or just date if logic branch differs. Need to verifying consistency.

    def test_standardize_date_ambiguity(self):
        # 01/02/2023 -> Jan 2nd or Feb 1st?
        # Code has prefer_day_first arg.
        res_default = standardize_date("01/02/2023")
        res_day_first = standardize_date("01/02/2023", prefer_day_first=True)
        assert res_default is not None
        # Verify if API signature actually respects this.

    def test_standardize_date_invalid(self):
        # Feb 30th
        assert standardize_date("2023-02-30") is None
        
        # Garbage
        assert standardize_date("Not a date") is None

    def test_standardize_date_timestamps(self):
        # Epoch
        ts = 1672531200 # 2023-01-01 00:00:00 UTC
        assert "2023-01-01" in standardize_date(ts)

# ==========================================
# 4. Tests de Texto (Edge Cases & Bugs)
# ==========================================

class TestTextSanitization:

    def test_slugify_integrity(self):
        # Basic
        assert slugify("Hola Mundo") == "hola-mundo"
        
        # Unicode
        assert slugify("Camión") == "camion"
        
        # Bug Hunt: Uppercase handling when lower=False
        # El código usa regex [^a-z0-9] que excluye mayúsculas.
        # Expectation: "Hola" -> "Hola"
        # Actual implementation might strip H if regex is lower case only.
        result = slugify("HolaMundo", lower=False)
        # Si el código está roto, esto devolverá "ola-undo" o similar.
        # Definimos el test esperando el comportamiento CORRECTO (o documentando el fallo).
        # En un test suite de QA reportamos lo que *debería* pasar.
        assert "HolaMundo" in result or result == "HolaMundo", f"Got broken slug: {result}"

    def test_slugify_empty_magic_string(self):
        # Empty input returns 'n-a' logic check
        assert slugify("") == "n-a"
        assert slugify(None) == "n-a"
        # Is this desirable? Usually QA flags magic strings.

    def test_infer_boolean_extended(self):
        assert infer_boolean("Yes") is True
        assert infer_boolean("OFF") is False
        assert infer_boolean(1) is True
        assert infer_boolean(0) is False
        
        # Ambiguous
        assert infer_boolean("maybe") is None

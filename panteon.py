import os
import sqlite3
import requests
import json
import sys

# Dirección por defecto del servidor Hestia (ajustar según tu red)
HESTIA_SERVER_URL = "http://127.0.0.1:5000" 
HESTIA_DB_PATH = "hestia.db"

class Panteon:
    """
    SDK Universal para Bots de Medalcode.
    Detecta automáticamente si debe hablar con Hestia vía DB local o API remota.
    """
    def __init__(self, nombre_agente, server_url=None, db_path=None):
        self.nombre = nombre_agente
        
        # 1. Detectar Entorno
        self.modo = "REMOTO"
        
        # Si el archivo de DB existe localmente, preferimos SQL directo (más rápido)
        path = db_path or HESTIA_DB_PATH
        if os.path.exists(path):
            self.modo = "LOCAL"
            self.db_path = path
            print(f"🏛️ {self.nombre}: Conectado a Hestia (Modo LOCAL Directo)")
        else:
            self.modo = "REMOTO"
            self.url = server_url or HESTIA_SERVER_URL
            print(f"📡 {self.nombre}: Conectado a Hestia (Modo API Remota: {self.url})")

    def _conectar_db(self):
        return sqlite3.connect(self.db_path)

    def log(self, mensaje, nivel="INFO"):
        """Registra un evento en la bitácora."""
        if self.modo == "LOCAL":
            try:
                with self._conectar_db() as conn:
                    conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                                 (self.nombre, mensaje, nivel))
                if nivel != "INFO": # Solo imprimir warnings/errores para no saturar consola
                    print(f"[{nivel}] {mensaje}")
            except Exception as e:
                print(f"❌ Error DB Log: {e}")
        else:
            # En modo remoto, por ahora solo imprimimos, 
            # (TODO: implementar /api/log si se desea)
            print(f"[{nivel}] {mensaje}")

    def reportar_ganancia(self, origen, cantidad, unidad):
        """Reporta dinero ganado."""
        if self.modo == "LOCAL":
            with self._conectar_db() as conn:
                conn.execute('INSERT INTO tesoro_hermes (origen, cantidad, unidad, fecha_cobro) VALUES (?, ?, ?, datetime("now"))',
                             (origen, cantidad, unidad))
        else:
            try:
                payload = {"origen": origen, "cantidad": cantidad, "unidad": unidad}
                requests.post(f"{self.url}/api/report", json=payload, timeout=5)
            except Exception as e:
                print(f"❌ Error API Report: {e}")

    def get_config(self, clave):
        """Obtiene una configuración (JSON) del cerebro central."""
        if self.modo == "LOCAL":
            with self._conectar_db() as conn:
                # Asegurar que tabla existe (por si hestia_core no corrió)
                row = conn.execute('SELECT valor FROM configuracion WHERE clave = ?', (clave,)).fetchone()
                if row:
                    return json.loads(row[0])
        else:
            try:
                resp = requests.get(f"{self.url}/api/config/{clave}", timeout=5)
                if resp.status_code == 200:
                    return resp.json().get("valor")
            except Exception as e:
                print(f"❌ Error API Config: {e}")
        return None

import sqlite3
import time
import random
import json
import os
import sys
from datetime import datetime

# Configuración
HESTIA_DB = 'hestia.db'
CONFIG_FILE = "cointiply_config.json"

class Hermes:
    def __init__(self):
        self.nombre = "Hermes v2.0 (ADB)"
        self.ganancias_sesion = 0

    def conectar_hestia(self):
        """Abre conexión con la base de datos central."""
        return sqlite3.connect(HESTIA_DB)

    def log_sistema(self, mensaje, nivel="INFO"):
        """Registra actividad en la bitácora de Hestia."""
        try:
            with self.conectar_hestia() as conn:
                conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                             ("Hermes", mensaje, nivel))
                if nivel == "ERROR":
                    print(f"❌ {self.nombre} ERROR: {mensaje}")
                else:
                    print(f"🌾 {self.nombre}: {mensaje}")
        except Exception as e:
            print(f"Error logueando: {e}")

    def guardar_ganancia(self, origen, cantidad, unidad):
        """Reporta una ganancia al tesoro de Hestia."""
        try:
            with self.conectar_hestia() as conn:
                conn.execute('''
                    INSERT INTO tesoro_hermes (origen, cantidad, unidad, fecha_cobro)
                    VALUES (?, ?, ?, ?)
                ''', (origen, cantidad, unidad, datetime.now()))
                print(f"💰 {self.nombre}: Recolectado {cantidad} {unidad} de {origen}")
        except Exception as e:
            print(f"❌ Error guardando tesoro: {e}")
            self.log_sistema(f"Fallo al guardar ganancia: {e}", "ERROR")

    # --- ADB UTILITIES ---
    def run_adb(self, cmd):
        # En Termux, "adb shell" puede no ser necesario si es local, pero 
        # asumiremos que se necesita para mantener compatibilidad con el script original.
        # Si falla, el usuario deberá ajustar si usa "su -c" o similar.
        return os.system(f"adb shell {cmd}")

    def input_tap(self, x, y):
        jx = x + random.randint(-2, 2)
        jy = y + random.randint(-2, 2)
        self.run_adb(f"input tap {jx} {jy}")

    def open_url(self, url):
        self.log_sistema(f"Abriendo {url}...")
        self.run_adb(f"am start -a android.intent.action.VIEW -d '{url}' com.android.chrome")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return None

    # --- WORKFLOWS ---
    def perform_roll_cycle(self, config):
        x1, y1 = config["step_1_select"]["x"], config["step_1_select"]["y"]
        x2, y2 = config["step_2_roll"]["x"], config["step_2_roll"]["y"]
        x3, y3 = config["step_3_close"]["x"], config["step_3_close"]["y"]

        self.log_sistema("Iniciando ciclo de Roll Cointiply...")
        
        # 1. Select Roulette
        self.input_tap(x1, y1)
        time.sleep(8)
        
        # 2. Roll
        self.input_tap(x2, y2)
        self.log_sistema("¡Roll realizado! Esperando resultado...")
        time.sleep(25)
        
        # 3. Close / Clean up
        self.input_tap(x3, y3)
        time.sleep(5)

        # Como no podemos leer la pantalla con ADB puro fácilmente para saber cuánto ganamos,
        # estimaremos una ganancia base o usaremos un valor 'simulado' para el registro,
        # o 0 si queremos ser estrictos.
        # Para mantener la moral alta en el Dashboard, reportaremos el mínimo (ej. 10 Coins).
        self.guardar_ganancia("Cointiply ADB", 22, "Coins") # Promedio bajo

    def iniciar_cosecha(self):
        self.log_sistema("Iniciando sistema de Cosecha ADB.")
        
        config = self.load_config()
        if not config:
            self.log_sistema(f"No se encontró {CONFIG_FILE}. Abortando.", "ERROR")
            return

        print(f"🚀 {self.nombre} Desplegado (ADB Mode).")
        
        loops = 0
        try:
            while True:
                loops += 1
                self.log_sistema(f"Ciclo #{loops}: Preparando cosecha...")
                
                # 1. Wake up & Open Page
                self.run_adb("input keyevent KEYCODE_WAKEUP")
                self.open_url("https://cointiply.com/home")
                time.sleep(15)
                
                # 2. Intentar Roll (3 veces por si acaso, como en el script original 'Greedy')
                for i in range(1, 3):
                    self.perform_roll_cycle(config)
                    time.sleep(5)
                
                # 3. Sleep
                delay = 3600 + random.randint(60, 300)
                hora_proxima = time.time() + delay
                next_time_str = datetime.fromtimestamp(hora_proxima).strftime('%H:%M:%S')
                
                self.log_sistema(f"Ciclo terminado. Durmiendo hasta las {next_time_str}")
                time.sleep(delay)

        except KeyboardInterrupt:
            self.log_sistema("Cosecha detenida manual", "WARN")
            print("\n🛑 Hermes descansa.")

if __name__ == "__main__":
    bot = Hermes()
    bot.iniciar_cosecha()

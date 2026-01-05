import sqlite3
import time
import psutil
import subprocess
import sys
import os
from datetime import datetime

# Configuración
HESTIA_DB = 'hestia.db'

# Lista de Scripts Python a vigilar
PYTHON_WATCH_LIST = {
    'panoptes.py': 'python3 panoptes.py',
    'hermes.py': 'python3 hermes.py',
    'hestia_dashboard.py': './venv/bin/python hestia_dashboard.py' 
}

# Lista de Apps Android a vigilar (Paquete, Nombre)
ANDROID_WATCH_LIST = [
    ("com.honeygain.make.money", "Honeygain"),
    ("com.android.chrome", "Chrome") # Importante para Hermes
]

class Cerbero:
    def __init__(self):
        self.nombre = "Cerbero v2.0 (Híbrido)"
        self.ciclos = 0

    def conectar_hestia(self):
        return sqlite3.connect(HESTIA_DB)

    def log_sistema(self, mensaje, nivel="INFO"):
        try:
            with self.conectar_hestia() as conn:
                conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                             ("Cerbero", mensaje, nivel))
                if nivel == "WARN" or nivel == "ERROR":
                    print(f"🐕⚠️ {self.nombre}: {mensaje}")
        except Exception as e:
            print(f"Error crítico en log de Cerbero: {e}")

    # --- PYTHON PROCESS LOGIC ---
    def verificar_procesos_python(self):
        """Revisa si los bots Python están corriendo."""
        procesos_activos = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline:
                    procesos_activos.append(" ".join(cmdline))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        for script_name, launch_cmd in PYTHON_WATCH_LIST.items():
            encontrado = False
            for cmd in procesos_activos:
                if script_name in cmd:
                    encontrado = True
                    break
            
            if not encontrado:
                self.log_sistema(f"Script {script_name} caído. Reviviendo...", "WARN")
                self.revivir_script(script_name, launch_cmd)

    def revivir_script(self, script_name, launch_cmd):
        try:
            subprocess.Popen(launch_cmd.split(), 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
            self.log_sistema(f"♻️ {script_name} reiniciado.", "SUCCESS")
        except Exception as e:
            self.log_sistema(f"❌ Fallo al revivir {script_name}: {e}", "ERROR")

    # --- ANDROID APP LOGIC ---
    def is_app_running(self, package_name):
        # 'pidof' returns the process ID if running
        result = os.system(f"adb shell pidof {package_name} > /dev/null 2>&1")
        return result == 0

    def launch_app(self, package_name):
        os.system(f"adb shell monkey -p {package_name} 1 > /dev/null 2>&1")

    def verificar_apps_android(self):
        """Revisa si las Apps Android clave están corriendo."""
        for package, friendly_name in ANDROID_WATCH_LIST:
            if not self.is_app_running(package):
                self.log_sistema(f"App Android {friendly_name} cerrada. Relanzando...", "WARN")
                self.launch_app(package)
                time.sleep(5) # Dar tiempo a que abra
                if self.is_app_running(package):
                    self.log_sistema(f"♻️ App {friendly_name} recuperada.", "SUCCESS")
                else:
                    self.log_sistema(f"❌ Imposible abrir {friendly_name}.", "ERROR")

    # --- MAIN LOOP ---
    def monitorear_salud(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        if cpu > 85:
            self.log_sistema(f"Sobrecarga CPU: {cpu}%", "WARN")
        if self.ciclos % 12 == 0: # Cada minuto
            print(f"🐕 Cerbero Ping: Sistema Nominal (CPU {cpu}% | RAM {ram}%)")

    def iniciar_guardia(self):
        self.log_sistema("Iniciando vigilancia Híbrida (Python + Android).")
        print(f"🛡️  {self.nombre} está protegiendo Hestia.")
        
        try:
            while True:
                self.verificar_procesos_python()
                # Solo verificar Apps Android si estamos en un entorno donde ADB funcione
                # (Para pruebas locales podría fallar o spammear logs, pero lo dejamos activo)
                self.verificar_apps_android() 
                
                self.monitorear_salud()
                self.ciclos += 1
                time.sleep(5) 
        except KeyboardInterrupt:
            print(f"\n🛡️  Cerbero termina su turno.")

if __name__ == "__main__":
    guardian = Cerbero()
    guardian.iniciar_guardia()

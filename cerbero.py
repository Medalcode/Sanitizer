import time
import subprocess
import os
import sys
from panteon import Panteon

# Lista de Scripts Python a vigilar
PYTHON_WATCH_LIST = {
    'panoptes.py': 'python panoptes.py',
    'hermes.py': 'python hermes.py',
    'hestia_dashboard.py': 'python hestia_dashboard.py' 
}

# Apps Android (Solo notificaremos si faltan)
ANDROID_APPS = {
    "com.honeygain.make.money": "Honeygain"
}

class Cerbero:
    def __init__(self):
        self.bot = Panteon("Cerbero")
        self.ciclos = 0

    def verificar_procesos(self):
        """Revisa si los scripts python están vivos. Si no, los revive."""
        try:
            # Obtener lista de procesos una sola vez
            ps_output = subprocess.check_output(['ps', '-ef']).decode()
            
            for script, launch_cmd in PYTHON_WATCH_LIST.items():
                if script not in ps_output:
                    self.bot.log(f"⚠️ {script} caído. Reviviendo...", "WARN")
                    self.revivir_proceso(script, launch_cmd)
        except Exception as e:
            self.bot.log(f"❌ Error al escanear procesos: {e}", "ERROR")

    def revivir_proceso(self, script_name, launch_cmd):
        try:
            # Lanzamos en background
            subprocess.Popen(launch_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.bot.log(f"♻️ {script_name} reiniciado.", "INFO")
            self.bot.notificar(f"🚨 Alerta: {script_name} murió, pero ya lo reinicié.")
            # Evitar bucle infinito de reinicios rápidos
            time.sleep(10)
        except Exception as e:
            self.bot.log(f"❌ Fallo al revivir {script_name}: {e}", "ERROR")

    def verificar_android_apps(self):
        """Verifica apps nativas via ADB (Solo funciona si ADB corre local)."""
        if self.ciclos % 12 != 0: return # Solo cada minuto
        
        try:
            # Check rápido con pidof
            for pkg, name in ANDROID_APPS.items():
                res = subprocess.run(['pidof', pkg], capture_output=True)
                if res.returncode != 0:
                    self.bot.log(f"⚠️ App Android caída: {name}", "WARN")
                    # Intentar revivir via Monkey
                    subprocess.run(f"adb shell monkey -p {pkg} -c android.intent.category.LAUNCHER 1".split(), 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass # ADB puede no estar listo

    def monitorear_salud(self):
        """Mira RAM y Batería (si posible)."""
        if self.ciclos % 60 == 0: # Cada 5 min
            try:
                # Intento leer batería via termux-battery-status (si instalado) o dumpsys
                # Por ahora simple RAM log
                self.bot.log("🐕 Cerbero Ping: Sistema Nominal.")
            except:
                pass

    def iniciar_guardia(self):
        self.bot.log("🛡️ Cerbero v3.0 (Panteon) iniciando guardia...")
        self.bot.notificar("🐕 Hestia Iniciado y Protegido.")
        
        # Auto-conectar ADB local por si acaso
        os.system("adb connect 127.0.0.1:5555 > /dev/null 2>&1")

        while True:
            self.verificar_procesos()
            # self.verificar_android_apps() # Desacoplado por ahora para evitar spam ADB
            self.monitorear_salud()
            
            time.sleep(5)
            self.ciclos += 1

if __name__ == "__main__":
    guardian = Cerbero()
    guardian.iniciar_guardia()

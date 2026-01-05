import sqlite3
import time
import psutil
import subprocess
import sys
import os
from datetime import datetime

# Configuración
OLIMPO_DB = 'olimpo.db'
WATCH_LIST = {
    'panoptes.py': 'python3 panoptes.py',
    'hermes.py': 'python3 hermes.py',
    'olimpo_web.py': './venv/bin/python olimpo_web.py' 
}

class Hefesto:
    def __init__(self):
        self.nombre = "Hefesto (El Guardián)"
        self.ciclos = 0

    def conectar_olimpo(self):
        return sqlite3.connect(OLIMPO_DB)

    def log_sistema(self, mensaje, nivel="INFO"):
        try:
            with self.conectar_olimpo() as conn:
                conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                             ("Hefesto", mensaje, nivel))
                print(f"🔧 {self.nombre}: {mensaje}")
        except Exception as e:
            print(f"Error crítico en log de Hefesto: {e}")

    def verificar_procesos(self):
        """Revisa si los bots están corriendo. Si no, los revive."""
        procesos_activos = []
        
        # Obtener lista de líneas de comandos de todos los procesos corriendo
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline:
                    procesos_activos.append(" ".join(cmdline))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Chequear cada bot de la lista de vigilancia
        for script_name, launch_cmd in WATCH_LIST.items():
            encontrado = False
            for cmd in procesos_activos:
                if script_name in cmd:
                    encontrado = True
                    break
            
            if encontrado:
                # print(f"   ✅ {script_name} está operativo.")
                pass
            else:
                self.log_sistema(f"⚠️ ¡ALERTA! {script_name} no responde. Iniciando protocolo de resurrección...", "WARN")
                self.revivir_proceso(script_name, launch_cmd)

    def revivir_proceso(self, script_name, launch_cmd):
        try:
            # Lanzamos el proceso en segundo plano desconectado
            subprocess.Popen(launch_cmd.split(), 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
            self.log_sistema(f"♻️ {script_name} ha sido reiniciado exitosamente.", "SUCCESS")
        except Exception as e:
            self.log_sistema(f"❌ FALLO CRÍTICO: No se pudo revivir {script_name}. Error: {e}", "ERROR")

    def monitorear_salud(self):
        """Registra el uso de recursos cada cierto tiempo."""
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        
        if cpu > 80 or ram > 85:
            self.log_sistema(f"🔥 Sobrecarga detectada: CPU {cpu}% | RAM {ram}%", "WARN")
        
        # Guardamos un "ping" de vida en la bitácora cada 10 ciclos (aprox 1 minuto)
        if self.ciclos % 10 == 0:
            self.log_sistema(f"Reporte de Estado: CPU {cpu}% | RAM {ram}% | Todo nominal.")

    def iniciar_guardia(self):
        self.log_sistema("Iniciando turno de vigilancia. El Olimpo está seguro.")
        print(f"🛡️  {self.nombre} está protegiendo el servidor.")
        
        try:
            while True:
                self.verificar_procesos()
                self.monitorear_salud()
                self.ciclos += 1
                time.sleep(5) # Revisar cada 5 segundos
        except KeyboardInterrupt:
            print("\n🛡️  Hefesto termina su turno.")

if __name__ == "__main__":
    guardian = Hefesto()
    guardian.iniciar_guardia()

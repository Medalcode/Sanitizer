import sqlite3
import time
import random
from datetime import datetime

# Configuración
OLIMPO_DB = 'olimpo.db'

class Hermes:
    def __init__(self):
        self.nombre = "Hermes v1.0"
        self.fuentes = [
            "Cointiply Faucet", "Honeygain Passive", 
            "AdBTC Surf", "FireFaucet Daily"
        ]

    def conectar_olimpo(self):
        """Abre conexión con la base de datos central."""
        return sqlite3.connect(OLIMPO_DB)

    def log_sistema(self, mensaje, nivel="INFO"):
        """Registra actividad en la bitácora del Olimpo."""
        try:
            with self.conectar_olimpo() as conn:
                conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                             ("Hermes", mensaje, nivel))
        except Exception as e:
            print(f"Error logueando: {e}")

    def guardar_ganancia(self, origen, cantidad, unidad):
        """Reporta una ganancia al tesoro del Olimpo."""
        try:
            with self.conectar_olimpo() as conn:
                conn.execute('''
                    INSERT INTO tesoro_hermes (origen, cantidad, unidad, fecha_cobro)
                    VALUES (?, ?, ?, ?)
                ''', (origen, cantidad, unidad, datetime.now()))
                print(f"💰 {self.nombre}: Recolectado {cantidad} {unidad} de {origen}")
        except Exception as e:
            print(f"❌ Error guardando tesoro: {e}")
            self.log_sistema(f"Fallo al guardar ganancia: {e}", "ERROR")

    def trabajar_simulado(self):
        """
        SIMULACIÓN DE TRABAJO (Farming/Claims).
        En producción, aquí irían los clicks de ADB o llamadas a APIs.
        """
        print(f"\n🌾 {self.nombre} buscando tareas...")
        time.sleep(2) # Simular tiempo de carga de app/web
        
        # Simular una acción exitosa (ej. Roll de Cointiply)
        exito = random.random() > 0.3 # 70% de probabilidad de éxito
        
        if exito:
            fuente = random.choice(self.fuentes)
            
            if "Honeygain" in fuente:
                cantidad = round(random.uniform(0.01, 0.5), 3)
                unidad = "USD"
            elif "Cointiply" in fuente:
                cantidad = random.randint(15, 99)
                unidad = "Coins"
            else:
                cantidad = random.randint(5, 50)
                unidad = "Sats"
                
            self.guardar_ganancia(fuente, cantidad, unidad)
        else:
            print(f"💤 {self.nombre}: No hay tareas disponibles por ahora.")

    def iniciar_cosecha(self, intervalo=15):
        self.log_sistema("Iniciando ruta de cosecha")
        print(f"🚀 {self.nombre} Desplegado. Presiona CTRL+C para detener.")
        try:
            while True:
                self.trabajar_simulado()
                time.sleep(intervalo)
        except KeyboardInterrupt:
            self.log_sistema("Cosecha detenida manual", "WARN")
            print("\n🛑 Hermes descansa.")

if __name__ == "__main__":
    bot = Hermes()
    # Intervalo un poco más largo que Panoptes, simulando tareas más lentas
    bot.iniciar_cosecha(intervalo=8)

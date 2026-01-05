import sqlite3
import time
import random
from datetime import datetime

# Configuración
HESTIA_DB = 'hestia.db'

class Panoptes:
    def __init__(self):
        self.nombre = "Panoptes v1.0"
        self.objetivos = [
            "Laptop Gamer", "iPhone 15", "Monitor 144hz", 
            "Teclado Mecánico", "Mouse Logitech"
        ]
        self.tiendas = ["MercadoLibre", "Amazon", "AliExpress"]

    def conectar_hestia(self):
        """Abre conexión con la base de datos central."""
        return sqlite3.connect(HESTIA_DB)

    def log_sistema(self, mensaje, nivel="INFO"):
        """Registra actividad en la bitácora de Hestia."""
        try:
            with self.conectar_hestia() as conn:
                conn.execute("INSERT INTO bitacora_sistema (origen, mensaje, nivel) VALUES (?, ?, ?)",
                             ("Panoptes", mensaje, nivel))
        except Exception as e:
            print(f"Error logueando: {e}")

    def guardar_hallazgo(self, producto, precio, tienda, url):
        """Guarda una oferta detectada en la base de datos."""
        try:
            with self.conectar_hestia() as conn:
                conn.execute('''
                    INSERT INTO ofertas (producto, precio, tienda, url, fecha_captura)
                    VALUES (?, ?, ?, ?, ?)
                ''', (producto, precio, tienda, url, datetime.now()))
                print(f"✅ {self.nombre}: Guardado {producto} (${precio}) de {tienda}")
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
            self.log_sistema(f"Fallo al guardar oferta: {e}", "ERROR")

    def escanear_web_simulado(self):
        """
        SIMULACIÓN DE SCRAPING.
        En producción, aquí iría el código con 'requests' y 'BeautifulSoup'.
        """
        print(f"\n🔍 {self.nombre} escaneando el mercado...")
        time.sleep(1.5) # Simular tiempo de petición HTTP
        
        # Generar oferta aleatoria
        producto = random.choice(self.objetivos)
        precio = round(random.uniform(100, 1500), 2)
        tienda = random.choice(self.tiendas)
        url = f"https://{tienda.lower()}.com/oferta/{random.randint(1000,9999)}"
        
        # Simular que encontramos algo interesante (filtro de precio)
        if precio < 1200: 
            self.guardar_hallazgo(producto, precio, tienda, url)
        else:
            print(f"🔹 {self.nombre}: {producto} encontrado pero muy caro (${precio}). Ignorando.")

    def iniciar_vigilancia(self, intervalo=10):
        self.log_sistema("Iniciando ciclo de vigilancia")
        print(f"🚀 {self.nombre} Desplegado. Presiona CTRL+C para detener.")
        try:
            while True:
                self.escanear_web_simulado()
                time.sleep(intervalo)
        except KeyboardInterrupt:
            self.log_sistema("Apagado manual", "WARN")
            print("\n🛑 Vigilancia detenida.")

if __name__ == "__main__":
    bot = Panoptes()
    # Ejecutar cada 5 segundos para probar rápido el Dashboard
    bot.iniciar_vigilancia(intervalo=5)

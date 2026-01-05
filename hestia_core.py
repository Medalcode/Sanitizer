import sqlite3
import os
from datetime import datetime

# Configuración de Hestia
DB_NAME = 'hestia.db'

def conectar_hestia():
    """Establece la conexión con la base de datos de Hestia."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"🔥 Error conectando a Hestia: {e}")
        return None

def inicializar_hestia():
    """
    Génesis: Crea las tablas necesarias si no existen.
    Esta función se debe ejecutar al inicio para asegurar que el servidor Hestia está listo.
    """
    conn = conectar_hestia()
    if conn:
        cursor = conn.cursor()
        
        # 1. Tabla para Panoptes (El Scraper)
        # Guarda las ofertas encontradas.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ofertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                precio REAL NOT NULL,
                tienda TEXT,
                url TEXT,
                fecha_captura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Tabla para Hermes (El Cosechador)
        # Guarda las ganancias recolectadas (ej. Satoshis).
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tesoro_hermes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL, -- Ej: Cointiply, Honeygain
                cantidad REAL NOT NULL,
                unidad TEXT NOT NULL, -- Ej: Coins, USD, BTC
                fecha_cobro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. Tabla de Logs del Sistema (Salud del Servidor)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bitacora_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL, -- Quien reporta: Hefesto, Panoptes, etc.
                mensaje TEXT NOT NULL,
                nivel TEXT DEFAULT 'INFO', -- INFO, WARN, ERROR
                fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Tabla de Configuración Global (El Cerebro)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY, -- Ej: 'cointiply_coords', 'honeygain_enabled'
                valor TEXT NOT NULL,    -- JSON string o valor simple
                ultima_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print(f"🔥 Hestia inicializado correctamente en: {os.path.abspath(DB_NAME)}")
        print("   - Tablas verificadas: 'ofertas', 'tesoro_hermes', 'bitacora_sistema'.")
        conn.close()

def registrar_oferta_panoptes(producto, precio, tienda, url=""):
    """
    Función para que Panoptes registre un hallazgo en Hestia.
    """
    conn = conectar_hestia()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ofertas (producto, precio, tienda, url, fecha_captura)
            VALUES (?, ?, ?, ?, ?)
        ''', (producto, precio, tienda, url, datetime.now()))
        conn.commit()
        print(f"👁️  Panoptes ha archivado una oferta: {producto} a ${precio}")
        conn.close()

def reporte_estado():
    """Muestra un resumen rápido del estado de Hestia para el usuario (Dashboard en consola)."""
    conn = conectar_hestia()
    if conn:
        cursor = conn.cursor()
        
        # Contar ofertas
        cursor.execute("SELECT COUNT(*) FROM ofertas")
        total_ofertas = cursor.fetchone()[0]
        
        # Contar tesoro (ejemplo simple)
        cursor.execute("SELECT COUNT(*) FROM tesoro_hermes")
        total_cobros = cursor.fetchone()[0]
        
        print("\n🔥 --- ESTADO DE HESTIA ---")
        print(f"   Ofertas archivadas por Panoptes: {total_ofertas}")
        print(f"   Cobros realizados por Hermes:    {total_cobros}")
        print("----------------------------\n")
        conn.close()

if __name__ == "__main__":
    # Al ejecutar este script directamente, se inicializa el sistema y se hace una prueba.
    inicializar_hestia()
    
    # --- SIMULACIÓN DE PRUEBA ---
    # Imaginemos que Panoptes acaba de encontrar algo:
    registrar_oferta_panoptes("Laptop Gamer Asus", 200, "MercadoLibre", "http://ml.com/laptop")
    
    # Mostramos el reporte
    reporte_estado()

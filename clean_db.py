import sqlite3
import os

print("🧹 Limpiando base de datos Hestia...")
try:
    conn = sqlite3.connect('hestia.db')
    cursor = conn.cursor()
    
    # Borrar ofertas viejas (falsas)
    cursor.execute('DELETE FROM ofertas')
    print(f"✅ Ofertas eliminadas: {cursor.rowcount}")
    
    conn.commit()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

print("🚀 Reiniciando sistema...")
os.system("pkill -f python") # Matar procesos viejos
os.system("python cerbero.py") # Arrancar guardian

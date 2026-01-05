from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'hestia.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    try:
        conn = get_db_connection()
        
        # Obtener últimas ofertas de Panoptes
        ofertas = conn.execute('SELECT * FROM ofertas ORDER BY fecha_captura DESC LIMIT 10').fetchall()
        
        # Obtener últimos cobros de Hermes
        cobros = conn.execute('SELECT * FROM tesoro_hermes ORDER BY fecha_cobro DESC LIMIT 10').fetchall()
        
        # Obtener estadísticas básicas
        cursor = conn.execute('SELECT COUNT(*) FROM ofertas')
        total_ofertas = cursor.fetchone()[0]
        
        # Calcular total de monedas
        cursor = conn.execute("SELECT SUM(cantidad) FROM tesoro_hermes WHERE unidad = 'Coins'")
        res = cursor.fetchone()[0]
        total_coins = int(res) if res else 0
        
        # Obtener Logs del Sistema
        logs = conn.execute('SELECT * FROM bitacora_sistema ORDER BY fecha_evento DESC LIMIT 5').fetchall()
        
        conn.close()
        
        return render_template('index.html', ofertas=ofertas, cobros=cobros, logs=logs, total_ofertas=total_ofertas, total_coins=total_coins)
    except Exception as e:
        return f"<h1>⚠️ Error Crítico en Hestia</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    # Escuchar en todas las interfaces (0.0.0.0) para ser accesible desde la red local
    # Puerto 5000 por defecto
    print("🔥 Lanzando dashboard HESTIA en el puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
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

@app.route('/api/report', methods=['POST'])
def api_report():
    """Endpoint para recibir ganancias desde bots externos (Hefesto PC)."""
    try:
        data = request.json
        origen = data.get('origen', 'Desconocido')
        cantidad = data.get('cantidad', 0)
        unidad = data.get('unidad', 'N/A')
        
        conn = get_db_connection()
        conn.execute('INSERT INTO tesoro_hermes (origen, cantidad, unidad, fecha_cobro) VALUES (?, ?, ?, datetime("now"))',
                     (origen, cantidad, unidad))
        conn.commit()
        conn.close()
        
        print(f"📡 API: Recibido reporte de {origen}: {cantidad} {unidad}")
        return jsonify({"status": "success", "message": "Guardado en Hestia"}), 200
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/control/<accion>/<objetivo>', methods=['POST'])
def sistema_control(accion, objetivo):
    """
    Permite reiniciar bots matándolos. Cerbero se encargará de revivirlos.
    Acciones: 'restart'
    Objetivos: 'hermes', 'panoptes', 'all'
    """
    try:
        if accion == 'restart':
            if objetivo == 'all':
                # Reinicio nuclear (menos el dashboard para no cortar la respuesta)
                os.system("pkill -f panoptes.py")
                os.system("pkill -f hermes.py")
                return jsonify({"status": "success", "message": "Sistemas reiniciándose..."})
            
            elif objetivo in ['hermes', 'panoptes']:
                # Matar proceso específico
                cmd = f"pkill -f {objetivo}.py"
                os.system(cmd)
                return jsonify({"status": "success", "message": f"{objetivo} reiniciado."})
                
        return jsonify({"status": "error", "message": "Comando no reconocido"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/config/<clave>', methods=['GET'])
def get_config(clave):
    try:
        conn = get_db_connection()
        # Asegurar tabla (quick fix)
        conn.execute('CREATE TABLE IF NOT EXISTS configuracion (clave TEXT PRIMARY KEY, valor TEXT, ultima_modif TIMESTAMP)')
        row = conn.execute('SELECT valor FROM configuracion WHERE clave = ?', (clave,)).fetchone()
        conn.close()
        
        if row:
            import json
            return jsonify({"status": "success", "valor": json.loads(row[0])})
        return jsonify({"status": "error", "message": "Clave no encontrada"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Init Defaults
    try:
        import json
        c = sqlite3.connect(HESTIA_DB)
        c.execute('CREATE TABLE IF NOT EXISTS configuracion (clave TEXT PRIMARY KEY, valor TEXT, ultima_modif TIMESTAMP)')
        if not c.execute('SELECT 1 FROM configuracion WHERE clave = "cointiply_coords"').fetchone():
            # Config Cointiply
            default_config = json.dumps({
                "step_1_select": {"x": 659, "y": 1520},
                "step_2_roll": {"x": 353, "y": 1148},
                "step_3_close": {"x": 600, "y": 1490}
            })
            c.execute('INSERT INTO configuracion (clave, valor) VALUES (?, ?)', ("cointiply_coords", default_config))
            
            # Config Panoptes (Objetivos de búsqueda)
            default_search = json.dumps(["PlayStation 5", "iPhone 15", "RTX 4060"])
            c.execute('INSERT INTO configuracion (clave, valor) VALUES (?, ?)', ("panoptes_targets", default_search))
            
            c.commit()
            print("⚙️ Configuraciones iniciales inyectadas.")
        c.close()
    except Exception as e:
        print(f"Error init config: {e}")

    # Escuchar en todas las interfaces (0.0.0.0) para ser accesible desde la red local
    # Puerto 5000 por defecto
    print("🔥 Lanzando dashboard HESTIA en el puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)

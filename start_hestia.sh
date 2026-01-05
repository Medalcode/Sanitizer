#!/data/data/com.termux/files/usr/bin/sh

# Esperar a tener red (por si acaso el WiFi tarda en conectar)
echo "⏳ Esperando red..."
sleep 15

# Ir a la casa de Hestia
cd /data/data/com.termux/files/home

# Prevenir bloqueos de pantalla (Wake Lock)
termux-wake-lock

# Iniciar Cerbero (él se encargará de todo lo demás)
echo "🔥 Lanzando Hestia..."
python cerbero.py >> boot_log.txt 2>&1 &

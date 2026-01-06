import os
import socket
import subprocess
import time
import sys
import webbrowser

def get_local_ip():
    """Obtiene la IP local del PC para adivinar la subred."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def scan_network(port=5555, timeout=1):
    """Escanea la subred buscando puertos abiertos."""
    local_ip = get_local_ip()
    base_ip = '.'.join(local_ip.split('.')[:-1]) + '.'
    print(f"📡 Escaneando red {base_ip}0/24 buscando Hestia (Puerto {port})...")
    
    found_ips = []
    
    # Escaneo rápido (secuencial para no complicar dependencias, idealmente asyncio)
    # Optimizamos probando rangos comunes primero o usando arp -a si es linux
    try:
        # Intento rápido usando ARP (solo funciona si ya hubo tráfico)
        cmd = "ip neigh show"
        output = subprocess.check_output(cmd, shell=True).decode()
        possible_ips = [line.split()[0] for line in output.splitlines() if "192.168" in line]
    except:
        possible_ips = []

    # Si ARP falla o queremos ser exhaustivos, generamos lista
    if not possible_ips:
        possible_ips = [f"{base_ip}{i}" for i in range(1, 255)]

    for ip in possible_ips:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"🎯 ¡Objetivo encontrado: {ip}!")
            found_ips.append(ip)
        sock.close()
        
    return found_ips

def connect_adb(ip):
    print(f"🔗 Conectando ADB a {ip}...")
    os.system(f"adb connect {ip}:5555")

def check_dashboard(ip):
    try:
        r = subprocess.check_output(f"curl -s --max-time 2 http://{ip}:5000", shell=True)
        if b"HESTIA" in r or b"Hestia" in r:
            return True
    except:
        pass
    return False

def main():
    print("🔥 BUSCADOR DE HESTIA v1.0 🔥")
    
    # 1. Intentar USB primero (Más rápido)
    print("🔌 Verificando conexión USB...")
    usb_devs = subprocess.getoutput("adb devices").splitlines()
    usb_serial = None
    for line in usb_devs:
        if "device" in line and "192.168" not in line and "List" not in line and line.strip():
            usb_serial = line.split()[0]
            print(f"✅ USB detectado: {usb_serial}")
            break
            
    target_ip = None
    
    if usb_serial:
        # Si hay USB, forzamos modo TCP/IP y obtenemos IP
        print("🛠️  Configurando modo WiFi desde USB...")
        os.system(f"adb -s {usb_serial} tcpip 5555")
        time.sleep(2)
        # Sacar IP
        try:
            ip_out = subprocess.getoutput(f"adb -s {usb_serial} shell ip route")
            # Parseo sucio pero efectivo: buscar src X.X.X.X
            for part in ip_out.split():
                if part.count('.') == 3 and part.startswith("192.168"):
                    target_ip = part
                    break
        except:
            pass
            
    # 2. Si no hay USB o falló IP, Escaneamos
    if not target_ip:
        ips_adb = scan_network(5555)
        if ips_adb:
            target_ip = ips_adb[0] # Tomamos el primero
        else:
            # Fallback: Escanear puerto dashboard 5000 directamente
            print("⚠️ ADB no encontrado. Buscando Dashboard directo...")
            ips_dash = scan_network(5000)
            if ips_dash:
                target_ip = ips_dash[0]

    # 3. Resultado
    if target_ip:
        print(f"✅ HESTIA LOCALIZADO EN: {target_ip}")
        connect_adb(target_ip)
        
        # Verificar si Dashboard responde
        if check_dashboard(target_ip):
            print(f"🌐 Dashboard operativo: http://{target_ip}:5000")
            # webbrowser.open(f"http://{target_ip}:5000") # Opcional: Auto-abrir
        else:
            print("⚠️ Dashboard no responde (¿Cerbero caído?). Intentando revivir...")
            os.system(f"adb -s {target_ip}:5555 shell input text 'python cerbero.py' && adb -s {target_ip}:5555 shell input keyevent 66")
    else:
        print("❌ No se encontró Hestia en la red. Asegúrate de que el WiFi del móvil está encendido.")

if __name__ == "__main__":
    main()

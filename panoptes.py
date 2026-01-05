import time
import requests
import random
from bs4 import BeautifulSoup
from panteon import Panteon

class Panoptes:
    def __init__(self):
        self.bot = Panteon("Panoptes Real")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def escanear_mercadolibre(self, producto):
        """Busca un producto en MercadoLibre y extrae el primer resultado orgánico."""
        self.bot.log(f"🔎 Buscando '{producto}' en MercadoLibre...")
        
        url_busqueda = f"https://listado.mercadolibre.cl/{producto.replace(' ', '-')}_NoIndex_True"
        try:
            resp = requests.get(url_busqueda, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                self.bot.log(f"⚠️ Error {resp.status_code} al acceder a {url_busqueda}", "WARN")
                return

            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Selectores típicos de ML (pueden cambiar, pero estos son comunes)
            items = soup.find_all('li', class_='ui-search-layout__item')
            if not items:
                # Intentar layout de grilla
                items = soup.find_all('div', class_='ui-search-result__wrapper')

            if items:
                # Tomamos el primero para dar el dato "mejor posicionado"
                item = items[0]
                
                # Extraer Título (Intentar varios selectores)
                titulo_tag = item.find('h2', class_='ui-search-item__title')
                titulo = titulo_tag.text.strip() if titulo_tag else "Producto desconocido"
                
                # Extraer Precio
                precio_tag = item.find('span', class_='andes-money-amount__fraction')
                precio_texto = precio_tag.text.replace('.', '') if precio_tag else "0"
                try:
                    precio = int(precio_texto)
                except:
                    precio = 0

                # Extraer Link
                link_tag = item.find('a', class_='ui-search-link')
                link = link_tag['href'] if link_tag else "#"

                # Guardar en Hestia
                self.guardar_hallazgo(titulo, precio, "MercadoLibre", link)
            else:
                self.bot.log(f"⚠️ No encontré resultados para '{producto}'", "WARN")

        except Exception as e:
            self.bot.log(f"❌ Error scraping {producto}: {e}", "ERROR")

    def guardar_hallazgo(self, producto, precio, tienda, url):
        # Usamos conexión directa del SDK si es local
        if self.bot.modo == "LOCAL":
            with self.bot._conectar_db() as conn:
                conn.execute('''
                    INSERT INTO ofertas (producto, precio, tienda, url, fecha_captura)
                    VALUES (?, ?, ?, ?, datetime("now"))
                ''', (producto, precio, tienda, url))
                self.bot.log(f"✅ Hallazgo: {producto} a ${precio}")
        else:
            # TODO: Endpoint /api/oferta futura
            self.bot.log(f"📡 (Simulado Remoto) {producto}: ${precio}")

    def patrullar(self):
        """Ciclo principal de búsqueda."""
        self.bot.log("👁️ Panoptes v2 (Real) iniciado. Cargando objetivos...")
        
        while True:
            # 1. Leer Configuración Dinámica desde Hestia
            objetivos = self.bot.get_config("panoptes_targets")
            if not objetivos:
                objetivos = ["Bitcoin", "Laptop"] # Fallback
            
            # 2. Escanear cada objetivo
            for obj in objetivos:
                self.escanear_mercadolibre(obj)
                # Pausa humana para no ser baneado
                time.sleep(random.randint(5, 15)) 
            
            # 3. Descansar
            descanso = 1200 # 20 minutos
            self.bot.log(f"💤 Ronda terminada. Durmiendo {descanso/60:.0f} min.")
            time.sleep(descanso)

if __name__ == "__main__":
    ojo = Panoptes()
    ojo.patrullar()

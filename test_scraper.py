import requests
from bs4 import BeautifulSoup
import time

UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"

def test_ml():
    print("🔍 Probando acceso a MercadoLibre...")
    url = f"https://listado.mercadolibre.com.ar/playstation-5"
    headers = {"User-Agent": UA}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"📡 Status Code: {r.status_code}")
        
        if r.status_code != 200:
            print("❌ Bloqueo detectado o error de red.")
            return

        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Intentar selectores comunes
        items = soup.find_all('li', class_='ui-search-layout__item')
        print(f"📦 Items encontrados en HTML: {len(items)}")
        
        if len(items) > 0:
            item = items[0]
            title = item.find('h2', class_='ui-search-item__title')
            price = item.find('span', class_='andes-money-amount__fraction')
            
            print(f"📝 Título detectado: {title.text if title else 'NONE'}")
            print(f"💲 Precio detectado: {price.text if price else 'NONE'}")
        else:
            print("⚠️ No se encontraron items. Posible cambio de diseño o Captcha.")
            # Guardar HTML para debug
            with open("debug_ml.html", "w") as f:
                f.write(r.text[:5000])
            print("💾 Primeros 5kb guardados en debug_ml.html")

    except Exception as e:
        print(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    test_ml()

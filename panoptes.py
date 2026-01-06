import time
import requests
import json
from panteon import Panteon

class Panoptes:
    def __init__(self):
        self.bot = Panteon("Panoptes Finance")

    def obtener_crypto(self):
        """Consulta precios de criptomonedas en CoinGecko."""
        try:
            # Bitcoin y Ethereum (USD y CLP)
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd,clp"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # Bitcoin
                btc_usd = data.get('bitcoin', {}).get('usd', 0)
                self.guardar_dato("Bitcoin (USD)", btc_usd, "CoinGecko")
                
                # Ethereum
                eth_usd = data.get('ethereum', {}).get('usd', 0)
                self.guardar_dato("Ethereum (USD)", eth_usd, "CoinGecko")

                # Solana
                sol_usd = data.get('solana', {}).get('usd', 0)
                self.guardar_dato("Solana (USD)", sol_usd, "CoinGecko")
                
                self.bot.log(f"🪙 Crypto Update: BTC ${btc_usd} | ETH ${eth_usd}", "INFO")
            else:
                self.bot.log(f"⚠️ CoinGecko Error: {resp.status_code}", "WARN")

        except Exception as e:
            self.bot.log(f"❌ Error Crypto: {e}", "ERROR")

    def obtener_fiat_chile(self):
        """Consulta indicadores económicos de Chile (Dólar, UF)."""
        try:
            url = "https://mindicador.cl/api"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # Dólar Observado
                dolar = data.get('dolar', {}).get('valor', 0)
                self.guardar_dato("Dólar (CLP)", dolar, "Banco Central")
                
                # UF
                uf = data.get('uf', {}).get('valor', 0)
                self.guardar_dato("UF (CLP)", uf, "Banco Central")
                
                self.bot.log(f"🇨🇱 Chile Update: Dólar ${dolar} | UF ${uf}", "INFO")
            else:
                self.bot.log(f"⚠️ Mindiicador Error: {resp.status_code}", "WARN")

        except Exception as e:
            self.bot.log(f"❌ Error Fiat: {e}", "ERROR")

    def guardar_dato(self, nombre, valor, fuente):
        """Guarda el indicador en la tabla de ofertas (reciclada)."""
        if self.bot.modo == "LOCAL":
            try:
                with self.bot._conectar_db() as conn:
                    # En lugar de guardar histórico infinito, actualizamos el valor si es el mismo día
                    # O simplemente insertamos logs.
                    # Para el dashboard actual, insertamos como "Oferta"
                    
                    # 1. Limpiar dato anterior del mismo tipo hoy (para no llenar DB)
                    conn.execute("DELETE FROM ofertas WHERE producto = ? AND fecha_captura > datetime('now','-1 hour')", (nombre,))
                    
                    # 2. Insertar nuevo
                    conn.execute('''
                        INSERT INTO ofertas (producto, precio, tienda, url, fecha_captura)
                        VALUES (?, ?, ?, ?, datetime("now"))
                    ''', (nombre, int(valor), fuente, "#",)) # Guardamos como entero por ahora
            except Exception as e:
                self.bot.log(f"❌ DB Error: {e}", "ERROR")
        else:
            self.bot.log(f"📡 Mock: {nombre} -> {valor}")

    def patrullar(self):
        self.bot.log("💎 Panoptes Financial v1.0 Iniciado.")
        
        while True:
            # 1. Criptos
            self.obtener_crypto()
            
            # 2. Fiat Chile
            self.obtener_fiat_chile()
            
            # Descanso largo (los mercados no cambian tan rápido como para spammear)
            # 5 minutos
            time.sleep(300)

if __name__ == "__main__":
    ojo = Panoptes()
    ojo.patrullar()

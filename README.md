# 🔥 Hestia: Sistema de Orquestación & Vigilancia Autónoma

Hestia es un ecosistema inteligente diseñado para convertir un dispositivo Android (vía Termux) en un servidor doméstico robusto capaz de realizar web scraping, farming automatizado y monitoreo del sistema, todo controlado desde un Dashboard Web centralizado.

![Hestia Dashboard](https://via.placeholder.com/800x400?text=Hestia+Dashboard+Preview)

## 🧩 Módulos del Sistema

### 1. Hestia Core & Dashboard (`hestia_dashboard.py`)

El cerebro del sistema.

- **Web UI**: Un panel de control moderno (Flask) accesible vía navegador.
- **API Central**: Endpoints para que los bots reporten hallazgos y ganancias.
- **Base de Datos**: SQLite (`hestia.db`) que almacena configuraciones, ofertas y logs.

### 2. Panteon SDK (`panteon.py`)

La magia detrás de la comunicación.

- Librería universal que usan todos los bots.
- Detecta automáticamente si corre en local (escribiendo directo a DB) o remoto (vía API).
- Maneja notificaciones unificadas a Telegram.

### 3. Cerbero: El Guardián (`cerbero.py`)

Un sistema de vigilancia "Watchdog" con capacidades de auto-healing.

- Monitorea que `panoptes.py` y `hermes.py` estén vivos.
- Si un bot muere, **lo revive automáticamente**.
- Envía alertas a **Telegram** sobre el estado del sistema.
- Evita bucles de reinicio (Cooldown prevention).

### 4. Panoptes: El Ojo Que Todo Lo Ve (`panoptes.py`)

Scraper de precios en tiempo real.

- Busca productos definidos en la configuración (ej. "iPhone 15", "RTX 4060").
- Extrae precios reales de **MercadoLibre**.
- Guarda historial de precios para detectar ofertas.

### 5. Hermes: El Granjero (`hermes.py`)

Bot de automatización para Cointiply.

- Usa **ADB** para controlar toques en la pantalla.
- Realiza el "Roll" cada hora automáticamente.
- Reporta ganancias al Dashboard.

---

## 🚀 Instalación en Termux (Android)

### Prerrequisitos

- Android con modo Depuración ADB activado.
- **Termux** y **Termux:API** instalados.
- Python instalado en Termux (`pkg install python`).

### 1. Dependencias

```bash
pip install flask requests beautifulsoup4
```

### 2. Despliegue

Copia todos los archivos `.py` y la carpeta `templates/` al directorio home de Termux.

### 3. Configuración

Para activar las notificaciones de Telegram, inyecta tu Token y ChatID en la base de datos o usa el script auxiliar (si disponible).

### 4. Ejecución

Simplemente invoca al guardián. Él se encargará de levantar todo lo demás.

```bash
python cerbero.py
```

---

## 🎮 Comandos y Control

### Acceso Web

Desde tu PC o Red Local:
`http://<IP_TELEFONO>:5000`

### Control Remoto

El dashboard incluye botones para:

- ♻️ **Reiniciar Hermes**: Si se queda pegado.
- ♻️ **Reiniciar Panoptes**: Para forzar nueva búsqueda.
- ⚠️ **Reset All**: Reinicio nuclear de los bots.

### Auto-Arranque (Inmortalidad)

El sistema incluye `start_hestia.sh` para usarse con la app **Termux:Boot**, permitiendo que Hestia reviva solo si el teléfono se reinicia.

---

## 🛠️ Estructura de Archivos

- `hestia_dashboard.py`: Servidor Web y API.
- `cerbero.py`: Watchdog y lanzador de procesos.
- `panteon.py`: SDK de comunicación.
- `panoptes.py`: Scraper de precios.
- `hermes.py`: Bot de farming ADB.
- `templates/index.html`: Interfaz del Dashboard.
- `hestia.db`: Base de datos SQLite (se crea sola).

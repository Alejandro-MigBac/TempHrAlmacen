# TempHrAlmacén
Registro y control de temperatura y humedad relativa de un almacén farmacéutico.

## 🚀 Características

- **Dashboard Web en Tiempo Real**: Visualización de temperatura y humedad con gráficos interactivos (Plotly.js).
- **GUI de Escritorio**: Interfaz gráfica nativa con Tkinter siguiendo el patrón MVC.
- **Alertas Automáticas**: Notificaciones cuando la temperatura supera los 25°C.
- **Persistencia de Datos**: Almacenamiento en base de datos SQLite con ventana móvil de 24 horas.
- **Simulador Integrado**: Herramienta para simular lecturas de sensores sin hardware real.

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd TempHrAlmacen
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Ejecución

### Opción 1 — Interfaz local (Tkinter)

Lanza la GUI nativa de escritorio con el panel de control y visualización en tiempo real.

```bash
python main.py
```

### Opción 2 — Dashboard web (Flask)

Levanta el servidor web con la API REST y el dashboard interactivo.

```bash
python app.py
```

Accede al dashboard en: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

## 🧪 Simulación

Para probar el sistema sin hardware real, ejecuta el simulador en una tercera terminal **con `app.py` ya arrancado**:

```bash
python simulator.py
```

El simulador enviará lecturas cada 10 segundos al endpoint `/ingest` y generará picos de temperatura aleatorios (>25°C) con un 15% de probabilidad para activar las alertas.

## 📡 API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/ingest` | Recibe una lectura de sensor `{"temperatura": X, "humedad": Y}` |
| `GET` | `/dashboard` | Dashboard web interactivo en tiempo real |
| `GET` | `/api/data` | Datos históricos de las últimas 24h (JSON) |
| `GET` | `/api/static?window=<t>` | Vista estática para un intervalo (`5m`, `1h`, `24h`, `1w`) |

## 📂 Estructura del Proyecto

```
TempHrAlmacen/
├── app/
│   ├── controller/         # Controladores (patrón MVC)
│   ├── models/             # Modelos de datos
│   ├── repositories/       # Acceso a base de datos SQLite
│   ├── services/           # Lógica de negocio
│   └── view/               # Vistas Tkinter
├── app.py                  # Servidor Flask: API REST + Dashboard web
├── main.py                 # Punto de entrada de la GUI Tkinter
├── simulator.py            # Simulador de sensores
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación
```

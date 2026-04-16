"""
configdb.py - Configuración y conexión a la base de datos (SQLite / Supabase).

Provee acceso centralizado a la base de datos para almacenar
las lecturas de temperatura y humedad del almacén farmacéutico,
así como las alarmas generadas.
Si se detectan SUPABASE_URL y SUPABASE_KEY en el entorno, usa Supabase (nube).
En caso contrario, usa SQLite local.
"""

import sqlite3
import os
import logging
from datetime import datetime, timedelta

# Import opcional de supabase
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False


class ConfigDB:
    """Clase singleton para gestionar la conexión a SQLite o Supabase."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
            
        # Detectar si usar Supabase o SQLite
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
        
        self.usa_supabase = bool(self.supabase_url and self.supabase_key and HAS_SUPABASE)
        
        if self.usa_supabase:
            logging.info("ConfigDB inicializado en modo SUPABASE (Nube)")
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        else:
            logging.info("ConfigDB inicializado en modo SQLITE (Local)")
            directorio = os.path.dirname(os.path.abspath(__file__))
            self._ruta_db = os.path.join(directorio, "sqlite.db")
            self.crear_tablas_sqlite()
            
        self._inicializado = True

    # ------------------------------------------------------------------ #
    #  Conexión y DDL (Sólo SQLite)
    # ------------------------------------------------------------------ #
    def _conectar_sqlite(self):
        conn = sqlite3.connect(self._ruta_db)
        conn.row_factory = sqlite3.Row
        return conn

    def crear_tablas_sqlite(self):
        conn = self._conectar_sqlite()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lecturas (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperatura REAL    NOT NULL,
                    humedad     REAL    NOT NULL,
                    fecha       TEXT    NOT NULL,
                    hora        TEXT    NOT NULL,
                    id_almacen  INTEGER NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alarmas (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha        TEXT    NOT NULL,
                    hora         TEXT    NOT NULL,
                    valor_alarma REAL    NOT NULL,
                    almacen      INTEGER NOT NULL,
                    FOREIGN KEY (almacen) REFERENCES lecturas (id_almacen)
                )
            """)
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------ #
    #  CRUD — Lecturas
    # ------------------------------------------------------------------ #
    def insertar_lectura(self, temperatura, humedad, fecha=None, hora=None, id_almacen=1):
        ahora = datetime.now()
        if fecha is None:
            fecha = ahora.strftime("%Y-%m-%d")
        if hora is None:
            hora = ahora.strftime("%H:%M:%S")
            
        if self.usa_supabase:
            data, _ = self.supabase.table('lecturas').insert({
                "temperatura": temperatura,
                "humedad": humedad,
                "fecha": fecha,
                "hora": hora,
                "id_almacen": id_almacen
            }).execute()
            # La respuesta de data contiene la fila insertada si fue exitosa
            # Supabase crea su propia ID automagicamente en su schema.
            return data[1][0]['id'] if data and len(data) > 1 and len(data[1]) > 0 else 1
        else:
            conn = self._conectar_sqlite()
            try:
                cursor = conn.execute(
                    "INSERT INTO lecturas (temperatura, humedad, fecha, hora, id_almacen) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (temperatura, humedad, fecha, hora, id_almacen),
                )
                conn.commit()
                return cursor.lastrowid
            finally:
                conn.close()

    def obtener_lecturas(self):
        if self.usa_supabase:
            data, _ = self.supabase.table('lecturas').select('*').order('fecha').order('hora').execute()
            return data[1] if data and len(data)>1 else []
        else:
            conn = self._conectar_sqlite()
            try:
                cursor = conn.execute("SELECT * FROM lecturas ORDER BY fecha ASC, hora ASC")
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()

    def obtener_ultimas_lecturas(self, n=20):
        if self.usa_supabase:
            # Supabase orderBy: default is asc=True, but we can do asc=False to get latest
            data, _ = self.supabase.table('lecturas').select('*').order('fecha', desc=True).order('hora', desc=True).limit(n).execute()
            filas = data[1] if data and len(data)>1 else []
            filas.reverse()
            return filas
        else:
            conn = self._conectar_sqlite()
            try:
                cursor = conn.execute(
                    "SELECT * FROM lecturas ORDER BY fecha DESC, hora DESC LIMIT ?", (n,)
                )
                filas = [dict(row) for row in cursor.fetchall()]
                filas.reverse()
                return filas
            finally:
                conn.close()

    def obtener_lecturas_por_intervalo(self, minutos):
        limite = datetime.now() - timedelta(minutes=minutos)
        fecha_limite = limite.strftime("%Y-%m-%d")
        hora_limite = limite.strftime("%H:%M:%S")
        
        if self.usa_supabase:
            # En Supabase es un poco más complejo debido a gte/lte. 
            # Como optimización simple, bajamos las lecturas >= fecha_limite y filtramos en backend
            data, _ = self.supabase.table('lecturas').select('*').gte('fecha', fecha_limite).order('fecha').order('hora').execute()
            filas = data[1] if data and len(data)>1 else []
            
            # Filtrar por hora para el día limite
            filas_filtradas = []
            for f in filas:
                if f['fecha'] > fecha_limite or (f['fecha'] == fecha_limite and f['hora'] >= hora_limite):
                    filas_filtradas.append(f)
            return filas_filtradas
        else:
            conn = self._conectar_sqlite()
            try:
                cursor = conn.execute(
                    "SELECT * FROM lecturas "
                    "WHERE (fecha > ? OR (fecha = ? AND hora >= ?)) "
                    "ORDER BY fecha ASC, hora ASC",
                    (fecha_limite, fecha_limite, hora_limite),
                )
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()

    # ------------------------------------------------------------------ #
    #  CRUD — Alarmas
    # ------------------------------------------------------------------ #
    def insertar_alarma(self, fecha, hora, valor_alarma, almacen):
        if self.usa_supabase:
            self.supabase.table('alarmas').insert({
                "fecha": fecha,
                "hora": hora,
                "valor_alarma": valor_alarma,
                "almacen": almacen
            }).execute()
        else:
            conn = self._conectar_sqlite()
            try:
                conn.execute(
                    "INSERT INTO alarmas (fecha, hora, valor_alarma, almacen) "
                    "VALUES (?, ?, ?, ?)",
                    (fecha, hora, valor_alarma, almacen),
                )
                conn.commit()
            finally:
                conn.close()

    def obtener_alarmas(self):
        if self.usa_supabase:
            data, _ = self.supabase.table('alarmas').select('*').order('fecha').order('hora').execute()
            return data[1] if data and len(data)>1 else []
        else:
            conn = self._conectar_sqlite()
            try:
                cursor = conn.execute("SELECT * FROM alarmas ORDER BY fecha ASC, hora ASC")
                return [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()

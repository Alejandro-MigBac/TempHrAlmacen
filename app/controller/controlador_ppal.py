"""
controlador_ppal.py - Controlador principal (MVC).

Gestiona la lógica de negocio conectando el Modelo y la Vista.
Controla el ciclo de monitoreo, alertas y generación de gráficos.
"""

import threading
import queue
from app.models.almacen import Almacen
from app.repositories.configdb import ConfigDB
from app.services.plotly_service import PlotlyService


class ControladorPrincipal:
    """Controlador principal del sistema de monitorización."""

    # Mapeo de botones de intervalo → minutos
    INTERVALOS = {
        "5 Minutos": 5,
        "60 Minutos": 60,
        "2 Horas": 120,
        "7 Días": 10080,
    }

    INTERVALO_ACTUALIZACION_MS = 30_000  # 30 segundos

    def __init__(self, vista):
        self.vista = vista
        self.db = ConfigDB()
        self.plotly_service = PlotlyService()
        self._monitoreo_activo = False
        self._cola = queue.Queue()
        self._job_id = None  # ID del .after() activo

    # ------------------------------------------------------------------ #
    #  Ciclo de monitoreo
    # ------------------------------------------------------------------ #
    def iniciar_monitoreo(self):
        """Inicia el ciclo de captura de datos cada 30 s."""
        if self._monitoreo_activo:
            return
        self._monitoreo_activo = True
        self.vista.actualizar_estado_monitoreo(True)
        self._ciclo_lectura()

    def detener_monitoreo(self):
        """Detiene el ciclo de captura."""
        self._monitoreo_activo = False
        self.vista.actualizar_estado_monitoreo(False)
        if self._job_id is not None:
            self.vista.root.after_cancel(self._job_id)
            self._job_id = None

    # ------------------------------------------------------------------ #
    #  Captura de datos (hilo secundario)
    # ------------------------------------------------------------------ #
    def _ciclo_lectura(self):
        """Ejecuta una lectura y programa la siguiente."""
        if not self._monitoreo_activo:
            return

        # Lanzar captura en hilo secundario para no bloquear la GUI
        hilo = threading.Thread(target=self._capturar_en_hilo, daemon=True)
        hilo.start()

        # Procesar resultados de la cola
        self.vista.root.after(200, self._procesar_cola)

        # Programar siguiente ciclo
        self._job_id = self.vista.root.after(
            self.INTERVALO_ACTUALIZACION_MS, self._ciclo_lectura
        )

    def _capturar_en_hilo(self):
        """Genera una lectura simulada y la guarda en BD (hilo secundario)."""
        lectura = Almacen.generar_lectura_simulada()
        lectura_id = self.db.insertar_lectura(
            lectura.temperatura,
            lectura.humedad,
            lectura.fecha,
            lectura.hora,
            lectura.id_almacen,
        )
        # Guardar el id de la lectura para posible uso en alarmas
        lectura._db_id = lectura_id
        self._cola.put(lectura)

    def _procesar_cola(self):
        """Procesa los resultados pendientes de la cola (hilo principal)."""
        try:
            while True:
                lectura = self._cola.get_nowait()
                self._actualizar_vista(lectura)
        except queue.Empty:
            pass

    # ------------------------------------------------------------------ #
    #  Actualización de la vista
    # ------------------------------------------------------------------ #
    def _actualizar_vista(self, lectura):
        """Actualiza todos los elementos de la vista con la nueva lectura."""
        # Actualizar indicadores
        self.vista.actualizar_indicador_temperatura(lectura.temperatura)
        self.vista.actualizar_indicador_humedad(lectura.humedad)

        # Actualizar tabla de historial y gráfico en tiempo real
        ultimas = self.db.obtener_ultimas_lecturas(60)
        self.vista.actualizar_tabla(ultimas)
        self.vista.actualizar_grafico(ultimas)

        # Verificar alertas
        self._verificar_alertas(lectura)

    def _verificar_alertas(self, lectura):
        """Verifica si la lectura dispara una alerta y la registra en BD."""
        if lectura.alerta_temperatura:
            # Registrar la alarma en la base de datos
            lectura_id = getattr(lectura, '_db_id', None)
            if lectura_id is not None:
                self.db.insertar_alarma(
                    fecha=lectura.fecha,
                    hora=lectura.hora,
                    valor_alarma=lectura.temperatura,
                    almacen=lectura.id_almacen,
                )
            self.vista.mostrar_alerta(lectura.temperatura)
        else:
            self.vista.restaurar_estado_normal()

    # ------------------------------------------------------------------ #
    #  Gráficos por intervalo
    # ------------------------------------------------------------------ #
    def mostrar_grafico_intervalo(self, etiqueta):
        """
        Genera el gráfico Plotly para el intervalo seleccionado.
        Se ejecuta en un hilo secundario para no bloquear la GUI.
        """
        minutos = self.INTERVALOS.get(etiqueta)
        if minutos is None:
            return

        def _generar():
            lecturas = self.db.obtener_lecturas_por_intervalo(minutos)
            if lecturas:
                self.plotly_service.generar_grafico_intervalo(lecturas, etiqueta)
            else:
                # Notificar en el hilo principal que no hay datos
                self.vista.root.after(0, lambda: self.vista.mostrar_info_sin_datos(etiqueta))

        hilo = threading.Thread(target=_generar, daemon=True)
        hilo.start()

    def mostrar_grafico_general(self):
        """Genera el gráfico Plotly con todas las lecturas disponibles."""
        def _generar():
            lecturas = self.db.obtener_lecturas()
            if lecturas:
                self.plotly_service.generar_grafico_combinado(lecturas)

        hilo = threading.Thread(target=_generar, daemon=True)
        hilo.start()

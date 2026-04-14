"""
plotly_service.py - Servicio de visualización con Plotly.

Genera gráficos HTML interactivos de temperatura y humedad
que se abren en el navegador del usuario.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import tempfile
import webbrowser


class PlotlyService:
    """Servicio para generar gráficos dinámicos con Plotly."""

    UMBRAL_TEMP = 25.0  # °C

    def __init__(self):
        self._directorio_temp = tempfile.gettempdir()

    # ------------------------------------------------------------------ #
    #  Gráfico combinado (temperatura + humedad)
    # ------------------------------------------------------------------ #
    def generar_grafico_combinado(self, lecturas, titulo="Monitorización Climática"):
        """
        Genera un gráfico con dos subplots: temperatura y humedad.

        Args:
            lecturas: lista de dicts con claves 'fecha', 'hora', 'temperatura', 'humedad'
            titulo: título del gráfico
        """
        if not lecturas:
            return

        fechas = [f"{l['fecha']} {l['hora']}" for l in lecturas]
        temperaturas = [l["temperatura"] for l in lecturas]
        humedades = [l["humedad"] for l in lecturas]

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("🌡️ Temperatura (°C)", "💧 Humedad (%)"),
            vertical_spacing=0.12,
            shared_xaxes=True,
        )

        # --- Temperatura ---
        fig.add_trace(
            go.Scatter(
                x=fechas,
                y=temperaturas,
                mode="lines+markers",
                name="Temperatura",
                line=dict(color="#EF4444", width=2),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(239, 68, 68, 0.1)",
            ),
            row=1, col=1,
        )

        # Línea de umbral 25°C
        fig.add_hline(
            y=self.UMBRAL_TEMP,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Umbral {self.UMBRAL_TEMP}°C",
            annotation_position="top left",
            row=1, col=1,
        )

        # --- Humedad ---
        fig.add_trace(
            go.Scatter(
                x=fechas,
                y=humedades,
                mode="lines+markers",
                name="Humedad",
                line=dict(color="#3B82F6", width=2),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(59, 130, 246, 0.1)",
            ),
            row=2, col=1,
        )

        # --- Layout ---
        fig.update_layout(
            title=dict(text=titulo, font=dict(size=20)),
            template="plotly_dark",
            height=700,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=60, r=30, t=80, b=40),
        )

        fig.update_yaxes(title_text="°C", row=1, col=1)
        fig.update_yaxes(title_text="%", row=2, col=1)
        fig.update_xaxes(title_text="Fecha / Hora", row=2, col=1)

        # Guardar y abrir en navegador
        ruta = os.path.join(self._directorio_temp, "monitor_climatico.html")
        fig.write_html(ruta)
        webbrowser.open(f"file:///{ruta}")

    # ------------------------------------------------------------------ #
    #  Gráfico por intervalo
    # ------------------------------------------------------------------ #
    def generar_grafico_intervalo(self, lecturas, etiqueta_intervalo):
        """
        Genera un gráfico filtrado por intervalo de tiempo.

        Args:
            lecturas: lista de dicts filtrada por intervalo
            etiqueta_intervalo: texto descriptivo del intervalo (e.g., '5 Minutos')
        """
        titulo = f"Monitorización Climática — Últimos {etiqueta_intervalo}"
        self.generar_grafico_combinado(lecturas, titulo=titulo)

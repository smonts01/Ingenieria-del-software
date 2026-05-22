"""
Vista de estadísticas del cliente (interfaz_cliente_estadisticas.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaClienteEstadisticas(QMainWindow):
    """Vista de estadísticas personales del cliente."""

    DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_estadisticas.ui", self)

    # --- Cabecera ---
    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    # --- Tarjetas de resumen ---
    def set_calorias(self, valor: str):
        """Total calorías del período."""
        self.lblIconCalorias.setToolTip(valor)
        # El label de valor está junto al icono en la card
        if hasattr(self, "lblValorCalorias"):
            self.lblValorCalorias.setText(valor)

    def set_entrenos(self, valor: str):
        if hasattr(self, "lblValorEntrenos"):
            self.lblValorEntrenos.setText(valor)

    def set_tiempo_total(self, valor: str):
        if hasattr(self, "lblValorTiempo"):
            self.lblValorTiempo.setText(valor)

    def set_objetivo(self, valor: str):
        if hasattr(self, "lblValorObjetivo"):
            self.lblValorObjetivo.setText(valor)

    # --- Gráfico de barras semanal ---
    def set_barras_semana(self, alturas: list[int]):
        """
        Actualiza las barras del gráfico semanal.
        :param alturas: 7 valores (porcentaje 0-100), de lunes a domingo.
        """
        nombres = ["barLun", "barMar", "barMie", "barJue", "barVie", "barSab", "barDom"]
        max_px = 120
        for nombre_barra, pct in zip(nombres, alturas):
            barra = getattr(self, nombre_barra, None)
            if barra:
                barra.setFixedHeight(max(4, int(pct * max_px / 100)))

    # --- Distribución (gráfico de dona simulado) ---
    def set_distribucion(self, texto: str):
        """Texto central del gráfico de dona."""
        self.lblDona.setText(texto)

    def set_leyenda(self, idx: int, texto: str):
        """Actualiza una leyenda del gráfico (idx 1-4)."""
        lbl = getattr(self, f"lblLeyenda{idx}", None)
        if lbl:
            lbl.setText(texto)

    # --- Filtro de período ---
    def conectar_btn_periodo(self, callback):
        self.btnPeriodo.clicked.connect(callback)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnMini.clicked.connect(ctrl.cambiar_vista_grafico)
        self.btnPeriodo.clicked.connect(ctrl.cambiar_periodo)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)

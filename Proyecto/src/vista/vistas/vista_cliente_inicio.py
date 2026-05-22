"""
Vista del panel de inicio del cliente (interfaz_cliente_inicio.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class VistaClienteInicio(QMainWindow):
    """Vista del dashboard principal del cliente."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_inicio.ui", self)
        self._tabla: QTableWidget = self.findChild(QTableWidget)

    # --- Datos de bienvenida ---
    def set_bienvenida(self, nombre: str):
        self.lblBienvenida.setText(f"¡Hola, {nombre}!")

    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    # --- Tarjetas de resumen ---
    def set_num_clases(self, valor: str):
        self.lblNumClases.setText(valor)

    def set_asistencias(self, valor: str):
        self.lblAsistencias.setText(valor)

    def set_calorias_semana(self, valor: str):
        self.lblCaloriasSemana.setText(valor)

    # --- Tarjeta de pago ---
    def set_estado_pago(self, estado: str):
        self.lblEstadoPago.setText(estado)

    def set_cantidad_pago(self, cantidad: str):
        self.lblCantidadPago.setText(cantidad)

    def set_mes_pago(self, mes: str):
        self.lblMesPago.setText(mes)

    def set_cuota(self, cuota: str):
        self.lblCuota.setText(cuota)

    def set_pendiente_pago(self, visible: bool):
        self.lblPendientePago.setVisible(visible)

    # --- Próximas clases (tabla) ---
    def cargar_proximas_clases(self, clases: list[list], cabeceras: list[str]):
        if self._tabla is None:
            return
        self._tabla.setRowCount(len(clases))
        self._tabla.setColumnCount(len(cabeceras))
        self._tabla.setHorizontalHeaderLabels(cabeceras)
        for fila_idx, fila in enumerate(clases):
            for col_idx, valor in enumerate(fila):
                self._tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)

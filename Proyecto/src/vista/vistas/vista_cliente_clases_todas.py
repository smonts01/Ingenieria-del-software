"""
Vista de todas las clases disponibles para el cliente (interfaz_cliente_clases_todas.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class VistaClienteClasesTodas(QMainWindow):
    """Vista con el catálogo de clases disponibles para reservar."""

    # Índices de cards de clases (hasta 4 visibles)
    NUM_CARDS = 4

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_clases_todas.ui", self)

    # --- Cabecera de usuario ---
    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    # --- Filtros ---
    def get_filtro_tipo(self) -> str:
        return self.cmbTipo.currentText()

    def get_filtro_horario(self) -> str:
        return self.cmbHorario.currentText()

    def poblar_combo_tipo(self, tipos: list[str]):
        self.cmbTipo.clear()
        self.cmbTipo.addItems(["Todos"] + tipos)

    def poblar_combo_horario(self, horarios: list[str]):
        self.cmbHorario.clear()
        self.cmbHorario.addItems(["Todos"] + horarios)

    # --- Cards de clases ---
    def set_clase(self, idx: int, nombre: str, descripcion: str,
                  fecha: str, plazas: str, habilitado: bool = True):
        """
        Rellena la card de una clase (idx 1-4).
        :param idx: Número de card (1 a 4).
        :param habilitado: Si hay plazas disponibles para reservar.
        """
        getattr(self, f"lblClase{idx}").setText(nombre)
        getattr(self, f"lblDesc{idx}").setText(descripcion)
        getattr(self, f"lblFecha{idx}").setText(fecha)
        getattr(self, f"lblPlazas{idx}").setText(plazas)
        getattr(self, f"btnReservar{idx}").setEnabled(habilitado)

    def set_proxima_clase(self, nombre: str, descripcion: str):
        """Actualiza la tarjeta de 'próxima clase' del lateral."""
        if hasattr(self, "lblProxima"):
            self.lblProxima.setText(nombre)

    # --- Feedback ---
    def mostrar_mensaje(self, titulo: str, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, mensaje: str):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", mensaje)

    def confirmar_reserva(self, nombre_clase: str) -> bool:
        from PyQt5.QtWidgets import QMessageBox
        resp = QMessageBox.question(
            self, "Confirmar reserva",
            f"¿Deseas reservar la clase '{nombre_clase}'?"
        )
        return resp == QMessageBox.Yes

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnReservar1.clicked.connect(lambda: ctrl.reservar_clase(1))
        self.btnReservar2.clicked.connect(lambda: ctrl.reservar_clase(2))
        self.btnReservar3.clicked.connect(lambda: ctrl.reservar_clase(3))
        self.btnReservar4.clicked.connect(lambda: ctrl.reservar_clase(4))
        self.cmbTipo.currentIndexChanged.connect(ctrl.aplicar_filtros)
        self.cmbHorario.currentIndexChanged.connect(ctrl.aplicar_filtros)
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)

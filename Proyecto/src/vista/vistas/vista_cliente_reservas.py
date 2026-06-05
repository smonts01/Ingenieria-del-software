"""
Vista de reservas del cliente (interfaz_cliente_clases_reservas.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaClienteReservas(QMainWindow):
    """Vista con las reservas activas del cliente."""

    NUM_CARDS = 4

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_clases_reservas.ui", self)

    # --- Cabecera ---
    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    def set_info_reservas(self, texto: str):
        self.lblInfoReservas.setText(texto)

    # --- Cards de reservas ---
    def set_reserva(self, idx: int, clase: str, descripcion: str,
                    fecha: str, plazas: str, badge: str):
        """
        Rellena la card de una reserva (idx 1-4).
        :param badge: Texto del estado (p.ej. 'Confirmada', 'Pendiente').
        """
        getattr(self, f"lblReservaClase{idx}").setText(clase)
        getattr(self, f"lblReservaDesc{idx}").setText(descripcion)
        getattr(self, f"lblReservaFecha{idx}").setText(fecha)
        getattr(self, f"lblPlazasReserva{idx}").setText(plazas)
        getattr(self, f"lblBadge{idx}").setText(badge)

    def limpiar_reservas(self):
        """Oculta todas las cards de reservas."""
        for idx in range(1, self.NUM_CARDS + 1):
            card = getattr(self, f"cardReserva{idx}", None)
            if card:
                card.setVisible(False)

    def mostrar_reserva(self, idx: int, visible: bool = True):
        card = getattr(self, f"cardReserva{idx}", None)
        if card:
            card.setVisible(visible)

    # --- Botones de cancelación por card ---
    def conectar_boton_cancelar(self, idx: int, callback):
        """Conecta el botón de cancelar de una card específica."""
        btn = getattr(self, f"btnCancelarReserva{idx}", None)
        if btn:
            btn.clicked.connect(callback)

    # --- Feedback ---
    def mostrar_mensaje(self, titulo: str, mensaje: str):
        
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, mensaje: str):
        
        QMessageBox.critical(self, "Error", mensaje)

    def confirmar_cancelacion(self, nombre_clase: str) -> bool:
      
        resp = QMessageBox.question(
            self, "Cancelar reserva",
            f"¿Seguro que quieres cancelar la reserva de '{nombre_clase}'?"
        )
        return resp == QMessageBox.Yes

    # --- Señales ---
    def conectar_senales(self, ctrl):
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)

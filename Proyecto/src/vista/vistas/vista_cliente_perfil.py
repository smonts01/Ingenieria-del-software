"""
Vista del perfil del cliente (interfaz_cliente_perfil.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaClientePerfil(QMainWindow):
    """Vista de edición del perfil personal del cliente."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_cliente_perfil.ui", self)

    # --- Cabecera ---
    def set_nombre_cliente(self, nombre: str):
        self.lblNombreCliente.setText(nombre)
        self.lblNombrePerfil.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaCliente.setText(fecha)

    # --- Datos del perfil ---
    def get_email(self) -> str:
        return self.txtEmail.text().strip()

    def get_direccion(self) -> str:
        return self.txtDireccion.text().strip()

    def get_altura(self) -> str:
        return self.txtAltura.text().strip()

    def set_email(self, valor: str):
        self.txtEmail.setText(valor)
        self.lblEmailPerfil.setText(valor)

    def set_direccion(self, valor: str):
        self.txtDireccion.setText(valor)

    def set_altura(self, valor: str):
        self.txtAltura.setText(valor)

    # --- Barra de progreso de objetivo ---
    def set_progreso_objetivo(self, porcentaje: int):
        """
        Actualiza la barra de progreso visual (0-100).
        Ajusta el ancho de barraProgresoValor respecto a barraProgresoFondo.
        """
        ancho_total = self.barraProgresoFondo.width()
        ancho_valor = int(ancho_total * max(0, min(porcentaje, 100)) / 100)
        self.barraProgresoValor.setFixedWidth(ancho_valor)
        self.lblPorcentaje.setText(f"{porcentaje}%")

    def set_objetivo_semanal(self, texto: str):
        self.lblObjetivoSemanal.setText(texto)

    def set_asistencias_mes(self, valor: str):
        self.lblAsistenciasValor.setText(valor)

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_exito(self, mensaje: str):
        
        QMessageBox.information(self, "Perfil actualizado", mensaje)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        # Navegación
        self.btnInicio.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnEstadisticas.clicked.connect(ctrl.ir_estadisticas)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)

"""
Vista del perfil del entrenador (interfaz_entrenador_perfil.ui)
Patrón MVC - Capa Vista
"""
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox


class VistaEntrenadorPerfil(QMainWindow):
    """Vista de edición del perfil del entrenador."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_perfil.ui", self)

    # --- Cabecera ---
    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    # --- Datos del perfil (campos genéricos por QLineEdit) ---
    def get_campo(self, nombre_widget: str) -> str:
        w = self.findChild(QLineEdit, nombre_widget)
        return w.text().strip() if w else ""

    def set_campo(self, nombre_widget: str, valor: str):
        w = self.findChild(QLineEdit, nombre_widget)
        if w:
            w.setText(valor)

    # --- Aviso de perfil incompleto ---
    def mostrar_aviso_perfil(self, visible: bool):
        self.frameAvisoPerfil.setVisible(visible)

    # --- Feedback ---
    def mostrar_error(self, mensaje: str):
        
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_exito(self, mensaje: str):
       
        QMessageBox.information(self, "Perfil actualizado", mensaje)

    # --- Señales ---
    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnInformacion.clicked.connect(ctrl.ir_informacion)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)


class VistaEntrenadorInformacion(QMainWindow):
    """Vista de información del gimnasio para el entrenador (interfaz_entrenador_informacion.ui)."""

    def __init__(self):
        super().__init__()
        loadUi("ui/interfaz_entrenador_informacion.ui", self)

    def set_nombre(self, nombre: str):
        self.lblNombreCliente.setText(nombre)

    def set_fecha_alta(self, fecha: str):
        self.lblFechaAltaEntrenador.setText(fecha)

    def set_clases_hoy(self, valor: str):
        self.label_Num_Clases_Hoy.setText(valor)

    def set_clases_semana(self, valor: str):
        self.label_Num_Clases_semana.setText(valor)

    def set_clientes_total(self, valor: str):
        self.label_Num_Clientes_Total.setText(valor)

    def conectar_senales(self, ctrl):
        self.btnInicio_2.clicked.connect(ctrl.ir_inicio)
        self.btnClases.clicked.connect(ctrl.ir_clases)
        self.btnInscritos.clicked.connect(ctrl.ir_inscritos)
        self.btnOcupacion.clicked.connect(ctrl.ir_ocupacion)
        self.btnRegistroAsistencia.clicked.connect(ctrl.ir_registro_asistencia)
        self.btnPerfil.clicked.connect(ctrl.ir_perfil)
        self.btnCerrarSesion.clicked.connect(ctrl.cerrar_sesion)
